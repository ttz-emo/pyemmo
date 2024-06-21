#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""This module defines the function generate_simulation to generate a pyleecan
simulation object to use in pyleecan-api."""

from pyleecan.Classes.Machine import Machine as PyleecanMachine
from pyleecan.Classes.Simulation import Simulation as PyleecanSimulation
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq
import numpy as np


def create_simulation(
    machine: PyleecanMachine,
    i_d: float = 0.0,
    i_q: float = 0.0,
    speed: float = 1000.0,
) -> PyleecanSimulation:
    """Create a Pyleecan Simulation object from a given machine

    Args:
        machine (PyleecanMachine): Actual pyleecan machine
        id (float): Length axis (d-axis) current in A (eff). Defaults to 0.
        iq (float): Quadrature axis (q-axis) current in A (eff). Defaults to 0.
        speed (float): Initial speed for simulation in rpm. Defaults to 1000.0.


    Returns:
        PyleecanSimulation: Pyleecan Simulation object
    """
    simu = Simu1(name="PyEMMO_Simulation", machine=machine)
    # simu.path_result = "path/to/folder" Path to the Result folder to use
    # (will contain FEMM files)
    p = simu.machine.stator.winding.p
    # qs = simu.machine.stator.winding.qs

    # Defining Simulation Input
    simu.input = InputCurrent()
    # Rotor speed [rpm]
    simu.input.OP = OPdq(Id_ref=i_d, Iq_ref=i_q, N0=speed)

    # time discretization [s] -> one elec. period with # 32 timesteps
    time = np.linspace(start=0, stop=60 / speed / p, num=32, endpoint=True)
    simu.input.time = time

    # Angular discretization along the airgap circonference
    angular_disc = np.linspace(
        start=0, stop=2 * np.pi, num=2048, endpoint=False
    )
    simu.input.angle = angular_disc
    return simu
