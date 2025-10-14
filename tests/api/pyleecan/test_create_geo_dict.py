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

import math
from os.path import abspath, join

import gmsh
import pytest
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.MachineIPMSM import MachineIPMSM

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

import pyemmo.api.pyleecan.create_geo_dict
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


@pytest.fixture(scope="module", autouse=True)
def setup_gmsh_api():
    gmsh.initialize()
    gmsh.model.add("test pyleecan api")
    yield
    gmsh.finalize()


def test_create_geo_dict():
    """function to test the creation of the api geo dict"""
    machine: MachineIPMSM = load(  # type: ignore
        abspath(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))
    )
    rotor: LamHole = machine.rotor  # type: ignore
    geo_dict = pyemmo.api.pyleecan.create_geo_dict.create_geo_dict(machine)
    # assert for geometry_list
    gmsh.model.occ.synchronize()
    gmsh.fltk.run()
    # assert len(geo_dict) == 8
