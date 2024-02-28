"""
Coordinate Calculation Module

This module provides functions to calculate the x and y coordinates of a point on a circle given its radius and angle.

Functions:
- get_x_for_point: Calculates the x-coordinate of a point on a circle.
- get_y_for_point: Calculates the y-coordinate of a point on a circle.

Classes:
None

"""

import math


def get_x_for_point(radius: float, angle: float) -> float:
    """Get the x-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: ``x``: x-coordinate of point
    """
    x = radius * math.cos(angle)
    return x


def get_y_for_point(radius: float, angle: float) -> float:
    """Get the y-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: ``y``: y-coordinate of point
    """
    y = radius * math.sin(angle)
    return y
