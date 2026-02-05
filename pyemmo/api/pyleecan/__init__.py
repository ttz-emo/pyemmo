#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""TODO"""

from __future__ import annotations

from typing import Union

from ... import use_pyleecan

if use_pyleecan:
    from pyleecan.Classes.MachineDFIM import MachineDFIM  # induction machine
    from pyleecan.Classes.MachineIPMSM import MachineIPMSM
    from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
    from pyleecan.Classes.MachineSyRM import MachineSyRM
    from pyleecan.Classes.MachineWRSM import MachineWRSM

    # from pyleecan.Classes.MachineLSPM import MachineLSPM

    PyleecanMachine = Union[
        MachineDFIM, MachineSIPMSM, MachineIPMSM, MachineWRSM, MachineSyRM
    ]
    from pyleecan.Classes.Material import Material

    # Load default air material used in create_geo_dict function for surfaces without
    # referenced material.
    PyleecanAir = Material(name="Air")
POLE_HOLE_IDEXT = "Pole Hole"  # usused for now
