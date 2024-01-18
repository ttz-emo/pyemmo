from pyemmo.script.geometry.point import Point


def build_pyemmo_point(pyleecan_point: complex) -> Point:
    """Translates the coordinates of a point in ``pyleecan`` into a ``pyemmo`` point.

    Args:
        pyleecanPoint (complex): coordinates of the pyleecan point

    Returns:
        Point: ``pyemmoPoint``: pyemmo point
    """
    coords = [pyleecan_point.real, pyleecan_point.imag]

    pyemmo_point = Point(
        name="Point", x=coords[0], y=coords[1], z=0, meshLength=1e-3
    )

    return pyemmo_point
