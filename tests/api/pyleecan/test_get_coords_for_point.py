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
"""Module to test the module pyemmo.api.pyleecan.get_coords_for_point"""
import math

import hypothesis.strategies as st
from hypothesis import given

from pyemmo.api.pyleecan.get_coords_for_point import (
    get_x_for_point,
    get_y_for_point,
)


# Test function for get_x_for_point
@given(
    radius=st.floats(min_value=0.0, max_value=100.0),
    angle=st.floats(min_value=0.0, max_value=2 * math.pi),
)
def test_get_x_for_point(radius, angle):
    """Test get_x_for_point function with various input values."""
    result = get_x_for_point(radius, angle)
    expected_x = radius * math.cos(angle)
    assert math.isclose(result, expected_x, abs_tol=1e-6)


# Test function for get_y_for_point
@given(
    radius=st.floats(min_value=0.0, max_value=100.0),
    angle=st.floats(min_value=0.0, max_value=2 * math.pi),
)
def test_get_y_for_point(radius, angle):
    """Test get_y_for_point function with various input values."""
    result = get_y_for_point(radius, angle)
    expected_y = radius * math.sin(angle)
    assert math.isclose(result, expected_y, abs_tol=1e-6)
