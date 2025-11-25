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
"""
TODO
"""

from __future__ import annotations

from ..machine_segment_surface import MachineSegmentSurface
from . import PyleecanMachine
from .create_geo_dict import create_geo_dict


def translate_machine(machine: PyleecanMachine) -> dict[str, MachineSegmentSurface]:
    """_summary_ TODO

    Args:
        machine (PyleecanMachine): Pyleecan Machine object.

    Returns:
        dict[str, MachineSegmentSurface]: TODO

    Raises:
        RuntimeError: If a surface ID is already present in the geometry
            dictionary.
    """
    # Test machine attributes to make sure its translatable
    if not machine.rotor.is_internal:
        raise NotImplementedError("Outer rotor machines not implemented in pyemmo yet!")
    # Translation of geometry and creation of rotor and stator contour:
    geo_dict = create_geo_dict(machine)
    # TODO: If the rotor is of type LamHole, maybe create a separate airgap surface to
    # close the rotor lamination and reduce the height of the airgap created by the
    # pyemmo api. By definition in ``create_param_dict`` the complete rotor airgap will
    # be 2/5 of the total mechanical airgap. So the api create two stator airgaps of
    # The same height as the moving band.
    return geo_dict
