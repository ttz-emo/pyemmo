"""imports"""
from typing import Union

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc2 import Arc2
from pyleecan.Classes.Arc3 import Arc3

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from .buildPyemmoPoint import buildPyemmoPoint


def buildPyemmoLineList(
    pyleecanLineList: list[Union[Segment, Arc1, Arc2, Arc3]],
) -> list[Union[Line, CircleArc]]:
    """Translates the line list (Segment, Arc1, Arc2, Arc3) of a pyleecan-surface
    into line list (Line, CircleArc) of the pyemmo-surface.

    Args:
        pyleecanLineList (list[Union[Segment, Arc1, Arc2, Arc3]]): List of curves of 
        the pyleecan-surface

    Returns:
        list[Union[Line, CircleArc]]: List of curves of the surface
    """

    pyemmoLineList = []

    for line in pyleecanLineList:
        if isinstance(line, Segment):
            # translate a Segment into a Line
            translatedLine = Line(
                name="Line",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.end),
            )
            pyemmoLineList.append(translatedLine)

        elif isinstance(line, Arc1):
            # translate an Arc1 into CircleArc
            if (
                line.get_angle(is_deg=True) > 90
                or line.get_angle(is_deg=True) < -90
            ):
                translatedLine = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.begin),
                    endPoint=buildPyemmoPoint(line.get_middle()),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmoLineList.append(translatedLine)

                translatedLine = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.get_middle()),
                    endPoint=buildPyemmoPoint(line.end),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmoLineList.append(translatedLine)

            else:
                translatedLine = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.begin),
                    endPoint=buildPyemmoPoint(line.end),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmoLineList.append(translatedLine)

        elif isinstance(line, Arc2):
            # translate an Arc2 into CircleArc
            translatedLine = CircleArc(
                name="CircleArc",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.get_end()),
                centerPoint=buildPyemmoPoint(line.center),
            )
            pyemmoLineList.append(translatedLine)

        elif isinstance(line, Arc3):
            # translate an Arc3 into CircleArc
            translatedLine = CircleArc(
                name="CircleArc",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.get_middle()),
                centerPoint=buildPyemmoPoint(line.get_center()),
            )

            pyemmoLineList.append(translatedLine)
            translatedLine = CircleArc(
                name="CircleArc",
                startPoint=buildPyemmoPoint(line.get_middle()),
                endPoint=buildPyemmoPoint(line.end),
                centerPoint=buildPyemmoPoint(line.get_center()),
            )
            pyemmoLineList.append(translatedLine)

    return pyemmoLineList
