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

"""Module to test all materials can be loaded from the material database."""
from __future__ import annotations

import os

import numpy as np
import pytest

from pyemmo.script.material.material import DATABASE_PATH, Material


@pytest.mark.parametrize("material_file_name", ["air", "aluminum"])
def test_linear_material_load(material_file_name):
    """Test that all materials can be loaded from the material database."""
    # Load the material database
    mat = Material.load(material_file_name)
    assert mat.linear is True


@pytest.mark.parametrize(
    "material_file_name", ["steel_1008", "steel_1010", "M250_35A_0050Hz"]
)
def test_nonlinear_material_load(material_file_name):
    """Test that all materials can be loaded from the material database."""
    # Load the material database
    mat = Material.load(material_file_name)
    assert mat.linear is False
    assert len(mat.BH) != 0


def test_material_save_load():
    """Test the Material.save method."""
    mat = Material(
        "Test-Mat",
        relPermeability=1000,
        conductivity=1e6,
        BH=np.array(
            [[0.0, 0.0], [0.5, 100], [0.8, 200], [0.95, 280], [1.1, 500], [1.5, 1000]]
        ),
        remanence=1.3,
        density=1000,
        thermalConductivity=30,
        thermalCapacity=100,
        tempCoefRem=0.0015,
    )
    mat.save()  # save material to database path
    mat_file_name = os.path.join(DATABASE_PATH, mat.name + ".json")
    assert os.path.isfile(mat_file_name)
    reloaded_mat = Material.load(mat.name)
    assert mat == reloaded_mat
    mat.delete()  # remove test file
