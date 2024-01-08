"""imports"""
import pyleecan.Classes.Arc2

from pyemmo.script.geometry.point import Point
from .buildPyemmoPoint import buildPyemmoPoint


# =======================================
# Definition of function 'translateArc2':
# =======================================
def translateArc2(
    line: pyleecan.Classes.Arc2.Arc2,
) -> tuple[Point, Point, Point]:
    """Translates a pyleecan Arc2 into a pyemmo CircleArc.

    Args:
        line (pyleecan.Classes.Arc2.Arc2): a pyleecan Arc2 object

    Returns:
        _type_: _description_
    """
    # Calculation for Arc2
    # (An arc between two points (defined by the begin  point and a center and angle))

    startPoint = buildPyemmoPoint(line.begin)
    centerPoint = buildPyemmoPoint(line.center)
    middlePoint = buildPyemmoPoint(line.get_middle())
    endPoint = buildPyemmoPoint(line.get_end())

    return startPoint, endPoint, centerPoint, middlePoint
