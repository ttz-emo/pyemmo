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
"""
Module: test_build_pyemmo_material

This module provides functions for translating material properties from
pyleecan format to pyemmo format.

Functions:
    - build_pyemmo_material(pyleecan_material: pyleecan.Classes.Material) -> Material:
        Translates a pyleecan-material into a pyemmo-material.

Classes:
    - Material: Represents a material in pyemmo format.

Fixtures:
    - sample_pyleecan_material(): Fixture providing a sample pyleecan material for testing.

Test Functions:
    - test_build_pyemmo_material(sample_pyleecan_material: pyleecan.Classes.Material) -> None:
        Tests the build_pyemmo_material function with a sample pyleecan material.

"""

from __future__ import annotations

from os.path import join

import numpy as np
import pytest
from pyleecan.Classes.ImportMatrixVal import ImportMatrixVal
from pyleecan.Classes.Material import Material as PyleecanMaterial
from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load  # pylint: disable=no-name-in-module

from pyemmo.api.pyleecan.build_pyemmo_material import build_pyemmo_material
from pyemmo.script.material.material import Material


def _test_material_properies(pyemmo_material: Material, pyleecan_material):
    # misc properties
    assert pyemmo_material.name == pyleecan_material.name

    # structural properties
    assert pyemmo_material.density == pyleecan_material.struct.rho

    # electrical properties
    if pyleecan_material.elec.rho != 0.0:
        # if material has conductivity
        assert pyemmo_material.conductivity == pyleecan_material.elec.get_conductivity()
    else:
        assert pyemmo_material.conductivity == 0.0

    # magnetic properties
    assert pyemmo_material.relPermeability == pyleecan_material.mag.mur_lin
    if pyleecan_material.mag.BH_curve is not None and isinstance(
        pyleecan_material.mag.BH_curve, ImportMatrixVal  # abstract class
    ):
        np.testing.assert_array_equal(
            pyemmo_material.BH, pyleecan_material.mag.BH_curve.value[:, [1, 0]]
        )
    else:
        assert pyemmo_material.linear == True

    assert pyemmo_material.tempCoefRem == pyleecan_material.mag.alpha_Br
    assert pyemmo_material.remanence == pyleecan_material.mag.get_Brm()

    # thermal properties
    # set to default by now in build_pyemmo_material!
    assert pyemmo_material.thermalCapacity == 0.0
    assert pyemmo_material.thermalConductivity == 0.0
    return


@pytest.mark.parametrize(
    "mat_name",
    [
        "Air",
        "Copper2",
        "M19",  # Elec. steel with loss
        "M270-35A",  # Elec. steel
        "Magnet_N50",
    ],
)
def test_build_pyemmo_material(mat_name: str) -> None:
    """
    Tests the build_pyemmo_material function with a sample pyleecan material.

    Args:
        sample_pyleecan_material (pyleecanMat): Sample pyleecan material object.
    """
    pyleecan_material: PyleecanMaterial = load(
        join(DATA_DIR, "Material", mat_name + ".json")
    )
    pyemmo_material = build_pyemmo_material(pyleecan_material)

    _test_material_properies(pyemmo_material, pyleecan_material)


def test_nonMag_material_error():
    """Make sure build_material raises ValueError if no magnetic properties given"""
    # Material without magnetic properties:
    pyleecan_mat = load(join(DATA_DIR, "Material", "Insulator1.json"))
    pyleecan_mat.mag = None
    with pytest.raises(
        ValueError,
        match="No magnetic properties in PYLEECAN material",
    ):
        _ = build_pyemmo_material(pyleecan_mat)


def test_default_mag_material():
    """Make sure build_material raises ValueError if no magnetic properties given"""
    # Material without magnetic properties:
    pyleecan_mat = load(join(DATA_DIR, "Material", "Insulator1.json"))
    pyleecan_mat.mag = MatMagnetics()
    mat = build_pyemmo_material(pyleecan_mat)
    assert mat.relPermeability == 1.0
    np.testing.assert_array_equal(mat.BH, np.array([]))
    assert mat.linear is True
    assert mat.remanence == 0.0
