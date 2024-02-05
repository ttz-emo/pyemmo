"""
Module: test_build_pyemmo_material

This module provides functions for translating material properties from pyleecan format to pyemmo format.

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

import pytest
import numpy as np
from pyleecan.Classes.Material import Material as pyleecanMat
from pyleecan.Classes.MatStructural import MatStructural
from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.Classes.MatElectrical import MatElectrical

from workingDirectory.build_pyemmo_material import build_pyemmo_material


@pytest.fixture
def sample_pyleecan_material() -> pyleecanMat:
    """
    Fixture providing a sample pyleecan material for testing.

    Returns:
        pyleecanMat: Sample pyleecan material object.
    """
    sample_pyleecan_material = pyleecanMat(name="sample_pyleecan_material")

    sample_pyleecan_material.struct = MatStructural(
        rho=7650,  # mechanische Dichte: mass per unit volume [kg/m3]
    )
    sample_pyleecan_material.elec = MatElectrical(
        rho=0.01,  # Elektrischer Widerstand [Ohm]
    )
    sample_pyleecan_material.mag = MatMagnetics(
        mur_lin=0.000345,  # Relative magnetic permeability
        alpha_Br=-0.001,  # Temperaturkoffezient für die Remanenzflussdichte /°C compared to 20°C
        Brm20=1.5,  # magnet remanence induction at 20°C [T]
        Wlam=0.35,  # lamination sheet width without insulation [m] (0 == not laminated)
    )

    sample_pyleecan_material.mag.BH_curve = [
        [0, 0],
        [1, 2],
        [2, 4],
    ]

    return sample_pyleecan_material


def test_build_pyemmo_material(sample_pyleecan_material: pyleecanMat) -> None:
    """
    Tests the build_pyemmo_material function with a sample pyleecan material.

    Args:
        sample_pyleecan_material (pyleecanMat): Sample pyleecan material object.

    Returns:
        None

    Raises:
        AssertionError: If the translated pyemmo material does not match the expected values.

    Example:
        >>> sample_pyleecan_material = pyleecanMat(name="example_material")
        >>> test_build_pyemmo_material(sample_pyleecan_material)
    """
    pyemmo_material = build_pyemmo_material(sample_pyleecan_material)
    assert pyemmo_material.name == "sample_pyleecan_material"
    assert pyemmo_material.density == 7650
    assert pyemmo_material.conductivity == 0.01
    assert pyemmo_material.relPermeability == 0.000345
    assert pyemmo_material.tempCoefRem == -0.001
    assert pyemmo_material.remanence == 1.5
    np.testing.assert_array_equal(
        pyemmo_material.BH, np.array([[0, 0], [2, 1], [4, 2]])
    )
