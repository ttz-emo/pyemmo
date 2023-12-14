from pyemmo.script.geometry.point import Point


def buildPyemmoPoint(pyleecanPoint: complex) -> Point:
    """Translates the coordinates of a point in ``pyleecan`` into a ``pyemmo`` point.

    Args:
        pyleecanPoint (complex): coordinates of the pyleecan point

    Returns:
        Point: ``pyemmoPoint``: pyemmo point
    """
    coords = [pyleecanPoint.real, pyleecanPoint.imag]

    pyemmoPoint = Point(
        name="Point", x=coords[0], y=coords[1], z=0, meshLength=1e-3
    )

    return pyemmoPoint
