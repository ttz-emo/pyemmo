"""This module tests the build_pyemmo_point() function.
Following functions are included in this module:
* test_normal_point()
* test_center_point()
"""

import pytest

from pyemmo.script.geometry.point import Point
from pyemmo.api.pyleecan.build_pyemmo_point import build_pyemmo_point


@pytest.mark.parametrize(
    "pyleecan_input, expected_coordinates",
    [
        (1 + 1j, (1, 1, 0)),
        (0 + 0j, (0, 0, 0)),
    ],
)
def test_build_pyemmo_point(pyleecan_input, expected_coordinates):
    """Test if the pyleecan_point is correctly translated."""
    pyemmo_point: Point = build_pyemmo_point(pyleecan_point=pyleecan_input)
    assert pyemmo_point.coordinate == expected_coordinates
    assert pyemmo_point.name == "Point"
    assert pyemmo_point.meshLength == 1e-3
