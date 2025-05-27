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
"""Module: pyemmo_create_geo_dict

This module provides functions to convert geometry elements from pyleecan to pyemmo format.

Module dependencies:
    - pyleecan.Classes.MachineIPMSM.MachineIPMSM
    - pyleecan.Classes.MachineSIPMSM.MachineSIPMSM
    - pyleecan.Classes.MachineSyRM.MachineSyRM
    - pyleecan.Classes.Machine.Machine
    - ...functions.plot.plot
    - ...script.geometry.line.Line
    - ...script.geometry.circleArc.CircleArc
    - ...script.geometry.point.Point
    - ..json.SurfaceJSON.SurfaceAPI
    - ..logger

Functions:
    -   ``create_geo_dict``: Creates a dictionary containing geometry
        information for communication between Pyleecan and pyemmo.

Example:

    .. code:: python

        machine = MachineIPMSM(...)
        is_internal_rotor = True
        (
            geometry_list,
            rotor_contour_lines,
            stator_contour_lines,
            r_point_rotor_cont,
            l_point_rotor_cont,
            magnetization_dict
        ) = create_geo_dict(machine, is_internal_rotor)
        # Returns geometry objects, contour lines, and magnetization dictionary suitable for pyemmo.

Raises:
    TypeError: If unable to generate contours of the given machine type.
"""

from __future__ import annotations

import gmsh
import pytest
from pyleecan.Classes.LamSlot import LamSlot

from pyemmo.api.pyleecan import PyleecanMachine
from pyemmo.api.pyleecan.create_LamSlot_segment import create_LamSlot_segment

# pylint: disable=locally-disabled, unused-import
# Keep these for parameterized test!
from . import (  # nopycln: import
    IPMSM,
    SIPMSM_1,
    SIPMSM_2,
    SIPMSM_BA,
    SYNRM_ZAW,
    SYNRM_ZWW,
    Toyota_Prius,
    Toyota_Prius_2,
)


@pytest.fixture(scope="function", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.mark.parametrize(
    "machine",
    [
        "IPMSM",
        "SIPMSM_1",
        "SIPMSM_2",
        "SIPMSM_BA",
        "Toyota_Prius",
        "Toyota_Prius_2",
        "SYNRM_ZAW",
        "SYNRM_ZWW",
    ],
)
def test_create_LamSlot_segment(machine: PyleecanMachine, request):
    machine = request.getfixturevalue(machine)
    for lam in machine.get_lam_list():
        if isinstance(lam, LamSlot):
            surf_dict = create_LamSlot_segment(lam, machine)
            print(surf_dict)
    # gmsh.fltk.run()
