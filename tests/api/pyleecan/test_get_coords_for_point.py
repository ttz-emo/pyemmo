import math
from hypothesis import given
import hypothesis.strategies as st
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
