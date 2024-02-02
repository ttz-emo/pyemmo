"""
Module Testing

This module contains tests for the functions `get_x_for_point` and `get_y_for_point`
from the module `get_coords_for_point`. It uses the pytest framework for testing.

Fixtures:
    general_test_data: Provides general test data for the test functions.

Test Functions:
    test_get_x_for_point: Tests the `get_x_for_point` function with various input values.
    test_get_y_for_point: Tests the `get_y_for_point` function with various input values.

"""

import math
import pytest
from .get_coords_for_point import get_x_for_point, get_y_for_point


# Fixture for general test data
@pytest.fixture
def general_test_data():
    """Fixture providing general test data for get_x_for_point and get_y_for_point."""
    return [
        {
            "radius": 2.5,
            "angle": 0.0, 
            "expected_x": 2.5,
            "expected_y": 0.0
         },
        {
            "radius": 3.0,
            "angle": math.pi / 2,
            "expected_x": 0.0,
            "expected_y": 3.0,
        },
        {
            "radius": 4.0,
            "angle": math.pi,
            "expected_x": -4.0,
            "expected_y": 0.0,
        },
        {
            "radius": 2.0,
            "angle": 3 * math.pi / 2,
            "expected_x": 0.0,
            "expected_y": -2.0,
        },
    ]


# Test function for get_x_for_point
def test_get_x_for_point(general_test_data):
    """Test get_x_for_point function with various input values."""
    for data in general_test_data:
        result = get_x_for_point(data["radius"], data["angle"])
        assert math.isclose(result, data["expected_x"], abs_tol=1e-6)


# Test function for get_y_for_point
def test_get_y_for_point(general_test_data):
    """Test get_y_for_point function with various input values."""
    for data in general_test_data:
        result = get_y_for_point(data["radius"], data["angle"])
        assert math.isclose(result, data["expected_y"], abs_tol=1e-6)
