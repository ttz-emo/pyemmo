"""imports"""
from typing import Union

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc2 import Arc2
from pyleecan.Classes.Arc3 import Arc3

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from .buildPyemmoPoint import buildPyemmoPoint


def build_pyemmo_line_list(
    pyleecan_line_list: list[Union[Segment, Arc1, Arc2, Arc3]],
) -> list[Union[Line, CircleArc]]:
    """Translates the line list (Segment, Arc1, Arc2, Arc3) of a pyleecan-surface
    into line list (Line, CircleArc) of the pyemmo-surface.

    Args:
        pyleecanLineList (list[Union[Segment, Arc1, Arc2, Arc3]]): List of curves of 
        the pyleecan-surface

    Returns:
        list[Union[Line, CircleArc]]: List of curves of the surface
    """

    pyemmo_line_list = []

    for line in pyleecan_line_list:
        if isinstance(line, Segment):
            # translate a Segment into a Line
            translated_line = Line(
                name="Line",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.end),
            )
            pyemmo_line_list.append(translated_line)

        else:
            # translate an Arc1, Arc2 into CircleArc
            if (
                abs(line.get_angle(is_deg=True)) >= 180
            ):
                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.get_begin()),
                    endPoint=buildPyemmoPoint(line.get_middle()),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmo_line_list.append(translated_line)

                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.get_middle()),
                    endPoint=buildPyemmoPoint(line.get_end()),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmo_line_list.append(translated_line)

            else:
                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=buildPyemmoPoint(line.get_begin()),
                    endPoint=buildPyemmoPoint(line.get_end()),
                    centerPoint=buildPyemmoPoint(line.get_center()),
                )
                pyemmo_line_list.append(translated_line)

    return pyemmo_line_list
