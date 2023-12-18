import pyleecan.Classes.Segment
import pyleecan.Classes.Arc1
import pyleecan.Classes.Arc2
import pyleecan.Classes.Arc3
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from .buildPyemmoPoint import buildPyemmoPoint
from .translateArc1 import translateArc1
from .translateArc2 import translateArc2
from .translateArc3 import translateArc3


def buildPyemmoLineList(pyleecanLineList: list) -> list:
    """Translates the curves of a pyleecan-surface into Lines and CircleArcs of the pyemmo-surface.

    Args:
        pyleecanLineList (list): List of curves of the pyleecan-surface, contains (Segment, Arc1, Arc2, Arc3)

    Returns:
        list: List of curves (Line, CircleArc) of the surface
    """
    pyemmoLineList = []
    returnlist = []
    for line in pyleecanLineList:
        if isinstance(line, pyleecan.Classes.Segment.Segment):
            pyemmoLineList = Line(
                name="Line",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.end),
            )
            returnlist.append(pyemmoLineList)

        elif isinstance(line, pyleecan.Classes.Arc1.Arc1):
            print(line.get_angle(is_deg=True))
            if line.get_angle(is_deg=True) > 90 or line.get_angle(is_deg=True) < -90:
                startPoint, endPoint, centerPoint, centerPointArc = translateArc1(
                    line=line
                )
                pyemmoLineList = CircleArc(
                    name="CircleArc",
                    startPoint=startPoint,
                    endPoint=centerPointArc,
                    centerPoint=centerPoint,
                )
                returnlist.append(pyemmoLineList)

                pyemmoLineList = CircleArc(
                    name="CircleArc",
                    startPoint=centerPointArc,
                    endPoint=endPoint,
                    centerPoint=centerPoint,
                )
                returnlist.append(pyemmoLineList)

            else:
                startPoint, endPoint, centerPoint, centerPointArc = translateArc1(line=line)
                pyemmoLineList = CircleArc(
                    name="CircleArc",
                    startPoint=startPoint,
                    endPoint=endPoint,
                    centerPoint=centerPoint,
                )
                returnlist.append(pyemmoLineList)

        elif isinstance(line, pyleecan.Classes.Arc2.Arc2):
            startPoint, endPoint, centerPoint = translateArc2(line=line)
            pyemmoLineList = CircleArc(
                name="CircleArc",
                startPoint=startPoint,
                endPoint=endPoint,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)

        elif isinstance(line, pyleecan.Classes.Arc3.Arc3):
            startPoint, endPoint, centerPoint, centerPointArc = translateArc3(
                line=line
            )
            pyemmoLineList = CircleArc(
                name="CircleArc",
                startPoint=startPoint,
                endPoint=centerPointArc,
                centerPoint=centerPoint,
            )

            returnlist.append(pyemmoLineList)
            pyemmoLineList = CircleArc(
                name="CircleArc",
                startPoint=centerPointArc,
                endPoint=endPoint,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)

    return returnlist
