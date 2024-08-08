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
from os.path import join, abspath
import math
from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR
import pyemmo.api.pyleecan.create_geo_dict


def test_create_geo_dict():
    """function to test the creation of the api geo dict"""
    machine: Machine = load(
        abspath(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))
    )

    (
        geometry_list,
        rotor_contour_line_list,
        stator_contour_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    ) = pyemmo.api.pyleecan.create_geo_dict.create_geo_dict(
        machine, machine.rotor.is_internal
    )
    # assert for geometry_list
    assert len(geometry_list) == 8

    # asserts for rotor_contour_line_list
    assert len(rotor_contour_line_list) == 1

    # assert for stator_contour_line_list
    assert len(stator_contour_line_list) == 5

    # asserts for r_point_rotor_cont
    assert math.isclose(r_point_rotor_cont.coordinate[0], 0.0795, abs_tol=1e-6)
    assert math.isclose(r_point_rotor_cont.coordinate[1], 0, abs_tol=1e-6)
    assert math.isclose(r_point_rotor_cont.coordinate[2], 0, abs_tol=1e-6)
    assert r_point_rotor_cont.meshLength == 0.001

    # asserts for l_point_rotor_cont
    assert math.isclose(
        l_point_rotor_cont.coordinate[0], 0.05621498910433053, abs_tol=1e-6
    )
    assert math.isclose(
        l_point_rotor_cont.coordinate[1], 0.05621498910433053, abs_tol=1e-6
    )
    assert math.isclose(l_point_rotor_cont.coordinate[2], 0, abs_tol=1e-6)
    assert l_point_rotor_cont.meshLength == 0.001

    # asserts magnetization_dict
    assert math.isclose(
        magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-12
    )
    assert math.isclose(
        magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-12
    )
