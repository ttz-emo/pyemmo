#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
from __future__ import annotations

import os

import numpy as np
import pytest

from pyemmo.script.material import DATABASE_PATH
from pyemmo.script.material.electricalSteel import ElectricalSteel


def test_electrical_steel_init_properties():
    steel = ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=7650)
    assert steel.name == "M400-50A"
    assert np.isclose(steel.sheetThickness, 0.5)
    assert np.isclose(steel.density, 7650)


def test_electrical_steel_str_repr():
    steel = ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=7650)
    s = str(steel)
    assert "M400-50A" in s
    assert "Sheet Thickness [mm]: 0.5" in s
    assert "Reference Flux Density [T]: None" in s


def test_electrical_steel_equality():
    steel1 = ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=7650)
    steel2 = ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=7650)
    assert steel1 == steel2


def test_electrical_steel_inequality():
    steel1 = ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=7650)
    steel2 = ElectricalSteel(name="M400-65A", sheetThickness=0.65, density=7650)
    assert steel1 != steel2


def test_electrical_steel_invalid_sheetThickness():
    with pytest.raises(ValueError):
        ElectricalSteel(name="M400-50A", sheetThickness=-0.5, density=7650)


def test_electrical_steel_invalid_density():
    with pytest.raises(ValueError):
        ElectricalSteel(name="M400-50A", sheetThickness=0.5, density=-100)


@pytest.mark.parametrize("sheetThickness", [0.23, 0.27, 0.35, 0.5])
def test_electrical_steel_valid_sheetThickness(sheetThickness):
    steel = ElectricalSteel(
        name="TestSteel", sheetThickness=sheetThickness, density=7650
    )
    assert np.isclose(steel.sheetThickness, sheetThickness)


@pytest.mark.parametrize(
    "init_dict",
    [
        {
            "name": "Test-M400-35A",
            "sheetThickness": 0.5,
            "density": 7650,
            "lossParams": (140, 2, 0),
        },
        {
            "name": "Test-M400-35A",
            "sheetThickness": 0.5,
        },
    ],
)
def test_save_load(init_dict):
    """Test the save and load methods"""
    steel = ElectricalSteel(**init_dict)
    steel.save()
    assert os.path.isfile(os.path.join(DATABASE_PATH, f"{steel.name}.json"))
    reloaded_steel = ElectricalSteel.load(steel.name)
    assert steel == reloaded_steel
