import math

def getXforPoint(radius, angle):
    """Get the x-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: _description_
    """
    x = radius * math.cos(angle)
    return x


def getYforPoint(radius, angle):
    """Get the y-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: _description_
    """
    y = radius * math.sin(angle)
    return y