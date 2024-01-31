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
