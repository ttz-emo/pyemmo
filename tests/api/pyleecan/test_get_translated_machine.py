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
"""Module to test pyemmo.api.pyleecan.get_translated_machine"""
from __future__ import annotations

import math
from os.path import abspath, join

from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

import pyemmo.api.pyleecan.translate_machine
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


def test_get_translated_machine():
    """Function to test pyemmo.api.pyleecan.get_translated_machine"""
    machine: Machine = load(
        abspath(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))
    )

    (
        movingband_r,
        magnetization_dict,
        geo_translation_dict,
    ) = pyemmo.api.pyleecan.translate_machine.translate_machine(
        machine=machine,
    )
    # check movingband radius
    assert math.isclose(movingband_r, 0.0797, abs_tol=1e-16)
    # check magnetization directions
    assert math.isclose(magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-12)
    assert math.isclose(magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-12)
    for key in (
        "Pol",
        "Lpl0",
        "Mag0",
        "Lpl1",
        "Mag1",
        "Lpl2",
        "StNut",
        "StCu0",
        "LuR1",
        "LuR2",
        "StLu1",
        "StLu2",
    ):
        assert key in geo_translation_dict
