"""This module tests the build_pyemmo_point() function.
Following functions are included in this module:
* test_normal_point()
* test_center_point()
"""

import pytest
import numpy
from hypothesis import given, settings, strategies as st

from pyemmo.script.geometry.point import Point
from pyemmo.api.pyleecan.build_pyemmo_point import build_pyemmo_point


# @pytest.mark.parametrize(
#     "pyleecan_input, expected_coordinates",
#     [
#         (1 + 1j, (1, 1, 0)),
#         (0 + 0j, (0, 0, 0)),
#     ],
# )
# def test_build_pyemmo_point(pyleecan_input, expected_coordinates):
#     """Test if the pyleecan_point is correctly translated."""
#     pyemmo_point: Point = build_pyemmo_point(pyleecan_point=pyleecan_input)
#     assert pyemmo_point.coordinate == expected_coordinates
#     assert pyemmo_point.name == "Point"
#     assert pyemmo_point.meshLength == 1e-3


@settings(max_examples=50, report_multiple_bugs=True, derandomize=True)
@given(pyleecan_point=st.complex_numbers(allow_nan=False))
def test_build_pyemmo_point(pyleecan_point: complex) -> None:
    pyemmo_point: Point = build_pyemmo_point(pyleecan_point=pyleecan_point)
    assert pyemmo_point.coordinate[0] == numpy.real(pyleecan_point)
    assert pyemmo_point.coordinate[1] == numpy.imag(pyleecan_point)
    assert pyemmo_point.coordinate[2] == 0
    assert pyemmo_point.name == "point_pylc"
    assert pyemmo_point.meshLength == 1e-3
