# This file is part of atooms
# Copyright 2010-2024, Daniele Coslovich

"""
Minimal simulation backend for LAMMPS (http://lammps.sandia.gov).
"""

import os
import subprocess
import tempfile
from atooms import trajectory
from atooms import system
from atooms.system import interaction
from atooms.trajectory import TrajectoryLAMMPS
from atooms.trajectory.decorators import change_species
from atooms.core.utils import rmd

# Lammps command
lammps_command = 'lmp'

# MPI environment
try:
    lammps_mpi_tasks = 1
    lammps_mpi = 'mpirun'
    _ = subprocess.check_output([lammps_mpi, '--version'],
                                stderr=subprocess.STDOUT, executable='/bin/bash')
except subprocess.CalledProcessError:
    lammps_mpi_tasks = 1
    lammps_mpi = ''


def installed():
    """Return `True` if `lammps_command` can be executed"""
    try:
        _ = subprocess.check_output(f'echo | {lammps_mpi} {lammps_command}', shell=True,
                                    stderr=subprocess.STDOUT, executable='/bin/bash')
        return True
    except subprocess.CalledProcessError:
        return False


def _get_lammps_version():
    """Return lammps version and raise an exception if lammps is not installed"""
    try:
        _ = subprocess.check_output(f'echo | {lammps_mpi} {lammps_command}', shell=True,
                                    stderr=subprocess.STDOUT, executable='/bin/bash')
        version = _.decode().split('\n')[0][8:-1]
    except subprocess.CalledProcessError:
        raise ImportError(f'lammps not installed (command is {lammps_command})')
    return version

def _run_lammps_command(cmd):
    """Run a lammps script from the command line"""
    dirout = tempfile.mkdtemp()
    file_tmp = os.path.join(dirout, 'cmd.lammps')
    with open(file_tmp, 'w') as fh:
        fh.write(cmd)
    opt = f'-n {lammps_mpi_tasks}' if lammps_mpi else ''
    shell_cmd = f'{lammps_mpi} {opt} {lammps_command} -in {file_tmp}'
    try:
        stdout = subprocess.check_output(shell_cmd, shell=True,
                                         executable='/bin/bash',
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exception:
        print(cmd)
        if isinstance(exception.output, bytes):
            print(exception.output.decode())
        else:
            print(''.join(exception.output))
        raise

    # Clean up
    rmd(dirout)
    return stdout.decode()


class Interaction(interaction.Interaction):
    """
    Interaction wrapper for LAMMPS.

    For the time being, it assumes `self.potential` is a string
    containing appropriate lammps commands that define the
    interaction.
    """
    # TODO: assign interaction to system based on pair_style entries in cmd

    def __init__(self, potential, style='atomic', units='lj'):
        interaction.Interaction.__init__(self)
        self.style = style
        self.units = units
        self.potential = potential
        self.variables = {'particle': 'particle', 'cell': 'cell'}
        self.energy, self.virial = 0.0, 0.0

    def compute(self, observable, particle, cell):
        # We use self.potential as lammps commands
        dirout = tempfile.mkdtemp()
        file_tmp = os.path.join(dirout, 'lammps.atom')
        file_inp = os.path.join(dirout, 'lammps.atom.inp')
        # Update lammps startup file using self.system
        # This will write the .inp startup file
        with TrajectoryLAMMPS(file_tmp, 'w') as th:
            th.write(system.System(particle, cell), 0)

        # Do things in lammps order: units, read, commands, run. A
        # better approach would be to parse commands and place
        # read_data after units then pack commands again. Even better
        # using PyLammps...
        cmd = f"""\
units		{self.units}
atom_style	{self.style}
read_data {file_inp}
{self.potential}
run 0
write_dump all custom {file_tmp} fx fy fz modify format line "%.15g %.15g %.15g"
"""

        stdout = _run_lammps_command(cmd)

        found = False
        for line in stdout.split('\n'):
            if 'Step' in line:
                found = True
            elif found:
                if 'MPI' in line:
                    continue
                _, T, U, _, _, P = [float(x) for x in line.split()]
                rho = len(particle) / cell.volume
                ndim = len(cell.side)
                self.energy = U * len(particle)
                self.virial = (P - rho*T) * ndim * cell.volume
                break

        with TrajectoryLAMMPS(file_tmp) as th:
            new_system = th[-1]
            self.forces = new_system.interaction.forces

        # Clean up
        rmd(dirout)


# We use the base system class
System = system.System


class LAMMPS:

    """LAMMPS simulation backend."""

    def __init__(self, inp, commands, restart=False, verbose=False,
                 style='atomic', units='lj'):
        """
        We initialize the backend from `inp`, which can be a `System`, a
        `Trajectory` or path to a trajectory. LAMMPS `commands` must
        be a string or a file and should not contain dump or run
        commands.
        """
        self.version = _get_lammps_version()
        self.verbose = verbose
        self.style = style
        self.units = units
        
        # Actually only atomic and charge styles are supported
        assert self.style in ['atomic', 'charge']
        
        # Initialize commands
        self.commands = commands
        if os.path.exists(commands):
            with open(commands) as fh:
                self.commands = fh.read()

        # Define the initial system
        if isinstance(inp, system.System):
            # If we pass a system there is nothing to do
            self.system = inp

        elif isinstance(inp, trajectory.base.TrajectoryBase):
            # It is trajectory, we get the last frame
            self.system = inp[-1]

        elif os.path.exists(inp):
            # We accept any trajectory format, but if the format is
            # not recognized we force lammps native (atom) format
            try:
                with trajectory.Trajectory(inp) as t:
                    # We enforce fortran species layout
                    t.add_callback(change_species, 'F')
                    s = t[-1]
            except ValueError:
                with trajectory.TrajectoryLAMMPS(inp) as t:
                    s = t[-1]
            self.system = s

        else:
            raise ValueError(f'could not initialize system from {inp}')

        # Default trajectory format
        self.trajectory_class = TrajectoryLAMMPS

        # Assign commands as potentials
        # TODO: strip commands unrelated to interaction
        self.system.interaction = Interaction(commands, style=style, units=units)

        # Tmp directory for restart files
        # TODO: clean this somehow
        self.restart = restart
        if self.restart:
            self.tmpdir = tempfile.mkdtemp()

    def __str__(self):
        return 'LAMMPS'

    @property
    def rmsd(self):
        return 0.0

    def read_checkpoint(self, output_path):
        pass

    def write_checkpoint(self, output_path):
        pass

    def run(self, steps):
        dirout = tempfile.mkdtemp()
        file_tmp = os.path.join(dirout, 'lammps.atom')
        file_inp = os.path.join(dirout, 'lammps.atom.inp')
        if self.restart:
            file_res = os.path.join(self.tmpdir, 'lammps.restart')

        # Update lammps startup file using self.system
        # This will write the .inp startup file
        with TrajectoryLAMMPS(file_tmp, 'w') as th:
            th.write(self.system, 0)

        # Set fixes from the system if we find thermostat / barostat
        if 'fix' not in self.commands:
            if self.system.thermostat is not None and self.system.barostat is not None:
                # NPT ensemble
                fix = 'fix 1 all npt temp {0.temperature} {0.temperature} {0.relaxation_time} iso {1.pressure} {1.pressure} {1.relaxation_time}'.format(
                    self.system.thermostat, self.system.barostat)

            elif self.system.thermostat is not None:
                # NVT ensemble
                fix = 'fix 1 all nvt temp {0.temperature} {0.temperature} {0.relaxation_time}'.format(self.system.thermostat)

            else:
                # NVE ensemble
                fix = 'fix 1 all nve'
        else:
            # The integrator is already contained in the commands
            assert self.system.thermostat is None and self.system.barostat is None, \
                'lammps script contains a fix already'
            fix = ''

        # Do things in lammps order: units, read, commands, run. A
        # better approach would be to parse commands and place
        # read_data after units then pack commands again. Even better
        # using PyLammps...
        cmd = f"""\
units		{self.units}
atom_style	{self.style}
"""
        # Read restart file if it exists
        if self.restart and os.path.exists(file_res):
            cmd += f"""
read_restart {file_res}
"""
        else:
            cmd += f"""
read_data {file_inp}
"""

        # Rest of commands
        cmd += f"""
{self.commands}
{fix}
run {steps}
"""

        # Store system state at the end of run to update the System instance
        _dump_args = {'atomic': 'id type mass x y z vx vy vz',
                      'charge': 'id type mass q x y z vx vy vz'}
        _dump_fmt = {'atomic': '%d %d %.15g %.15g %.15g %.15g %.15g %.15g %.15g',
                     'charge': '%d %d %.15g %.15g %.15g %.15g %.15g %.15g %.15g %.15g'}
        dump_args = _dump_args[self.style]
        dump_fmt = _dump_fmt[self.style]        
        cmd += f"""
write_dump all custom {file_tmp} {dump_args} modify sort id format line "{dump_fmt}"
"""

        if self.restart:
            cmd += f"""
write_restart {file_res}
"""

        # Execute LAMMPS command
        stdout = _run_lammps_command(cmd)
        if self.verbose:
            print(stdout)
            
        # Update internal reference to self.system
        # Note that the thermostat and barostat are not touched
        with TrajectoryLAMMPS(file_tmp) as th:
            new_system = th[-1]
        self.system.update(new_system, exclude=['thermostat', 'barostat',
                                                'interaction'])
        
        # Clean up
        rmd(dirout)


class EnergyMinimization(LAMMPS):

    """LAMMPS minimization backend."""

    def __init__(self, inp, commands, method='cg', ftol=1e-4, steps=100000):
        """
        We initialize the backend from `inp`, which can be a `System`, a
        `Trajectory` or path to a trajectory. LAMMPS `commands` must
        be a string or a file and should not contain dump or minimize
        commands.
        """
        LAMMPS.__init__(self, inp, commands)
        self.steps = steps
        self.ftol = ftol
        self.method = method
        self.max_evaluations = 100000
        # Optimization backends must set a boolean reached_steps
        # attribute. It is True at the beginning.
        self.reached_steps = True

    def __str__(self):
        return 'LAMMPS energy minimization'

    def run(self, steps=None):
        if steps is not None:
            self.steps = steps

        dirout = tempfile.mkdtemp()
        file_tmp = os.path.join(dirout, 'lammps.atom')
        file_inp = os.path.join(dirout, 'lammps.atom.inp')

        # Update lammps startup file using self.system
        # This will write the .inp startup file
        with TrajectoryLAMMPS(file_tmp, 'w') as th:
            th.write(self.system, 0)

        # Do things in lammps order: units, read, commands, run. A
        # better approach would be to parse commands and place
        # read_data after units then pack commands again. Even better
        # using PyLammps...
        max_evaluations = min(100000000, self.max_evaluations)
        cmd = f"""\
units		{self.units}
atom_style	{self.style}
read_data {file_inp}
{self.commands}
min_style {self.method}
minimize 0.0 {self.ftol} {self.steps} {max_evaluations}
write_dump all custom {file_tmp} id type x y z modify sort id format line "%d %d %.15g %.15g %.15g"
"""
        stdout = _run_lammps_command(cmd)

        if self.verbose:
            print(stdout)

        # Check if we have reached the number of maximum number of steps
        if 'Stopping criterion = max iterations' in stdout:
            self.reached_steps = True
        else:
            self.reached_steps = False

        # Update internal reference to self.system
        with TrajectoryLAMMPS(file_tmp) as th:
            new_system = th[-1]
        for i in range(len(self.system.particle)):
            self.system.particle[i] = new_system.particle[i]

        # Clean up
        rmd(dirout)
