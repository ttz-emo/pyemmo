"""imports"""
import pyleecan.Classes.Arc1

from pyemmo.script.geometry.point import Point
from .build_pyemmo_point import build_pyemmo_point


# =======================================
# Definition of function 'translateArc1':
# =======================================
def translateArc1(
    line: pyleecan.Classes.Arc1.Arc1,
) -> tuple[Point, Point, Point, Point]:
    """Translates a pyleecan Arc1 into a pyemmo CircleArc.

    Args:
        line (pyleecan.Classes.Arc1.Arc1): a pyleecan Arc1 object

    Returns:
        tuple[Point, Point, Point, Point]: startPoint, endPoint, center point of the arc
        and the middle point on the arc
    """
    # Translation for Pyleecan Arc1 to Pyemmo CircleArc
    # (An arc between two points (defined by a radius)):

    startPoint = build_pyemmo_point(line.begin)
    endPoint = build_pyemmo_point(line.end)
    centerPoint = build_pyemmo_point(line.get_center())
    centerPointArc = build_pyemmo_point(line.get_middle())

    
    
    
    return startPoint, endPoint, centerPoint, centerPointArc
