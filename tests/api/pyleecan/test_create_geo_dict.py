#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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
"""Module to test the creation of the api geo dict."""
from __future__ import annotations

import pytest
from pyleecan.Classes.LamHole import LamHole

import pyemmo.api.pyleecan.create_geo_dict

from . import Toyota_Prius  # pylint: disable=W0611


@pytest.mark.parametrize("machine", ["Toyota_Prius"])
def test_create_geo_dict(machine, request):
    """function to test the creation of the api geo dict"""
    machine = request.getfixturevalue(machine)
    rotor: LamHole = machine.rotor  # type: ignore
    geo_dict = pyemmo.api.pyleecan.create_geo_dict.create_geo_dict(machine)
    # assert for geometry_list
    # gmsh.model.occ.synchronize()
    # gmsh.fltk.run()
    # assert len(geo_dict) == 8
