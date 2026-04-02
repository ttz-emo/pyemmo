#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
This module defines the function :func:`~pyemmo.api.pyleecan.translate_machine.translate_machine`
to convert a given PYLEECAN machine object to a geometry dictionary in pyemmo json-api
format.
"""

from __future__ import annotations

from ..machine_segment_surface import MachineSegmentSurface
from . import PyleecanMachine
from .create_geo_dict import create_geo_dict


def translate_machine(machine: PyleecanMachine) -> dict[str, MachineSegmentSurface]:
    """Convert a given PYLEECAN machine to a geometry dict for use in pyemmo json-api.
    This uses the :func:`~pyemmo.api.pyleecan.create_geo_dict.create_geo_dict` function
    to create a geometry dictionary.

    Args:
        machine (PyleecanMachine): PYLEECAN Machine object.

    Returns:
        dict[str, MachineSegmentSurface]: json-api compatible geometry dictionary with
        part_ids as keys and MachineSegmentSurface objects as values.
        See  `Geometry input <section-pyemmo.api.json-geo>`_ section in docs for details
        on the structure of the geometry dictionary.

    Raises:
        RuntimeError: If a surface ID is already present in the geometry
            dictionary.
    """
    # Test machine attributes to make sure its translatable
    if not machine.rotor.is_internal:
        raise NotImplementedError("Outer rotor machines not implemented in pyemmo yet!")
    # Translation of geometry and creation of rotor and stator contour:
    geo_dict = create_geo_dict(machine)
    return geo_dict
