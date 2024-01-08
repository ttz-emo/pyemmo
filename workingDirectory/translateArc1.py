"""imports"""
import pyleecan.Classes.Arc1

from pyemmo.script.geometry.point import Point
from .buildPyemmoPoint import buildPyemmoPoint


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

    startPoint = buildPyemmoPoint(line.begin)
    endPoint = buildPyemmoPoint(line.end)
    centerPoint = buildPyemmoPoint(line.get_center())
    centerPointArc = buildPyemmoPoint(line.get_middle())

    
    
    
    return startPoint, endPoint, centerPoint, centerPointArc
