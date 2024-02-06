"""imports"""
from typing import Union

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc2 import Arc2
from pyleecan.Classes.Arc3 import Arc3

from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from .build_pyemmo_point import build_pyemmo_point


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

    if len(pyleecan_line_list) == 0:
        raise IndexError("The pyleecan_line_list provided is empty. No translation possible.")

    for geo_element in pyleecan_line_list:
        if isinstance(geo_element, Segment):
            # translate a Segment into a Line
            translated_line = Line(
                name="Line",
                startPoint=build_pyemmo_point(geo_element.begin),
                endPoint=build_pyemmo_point(geo_element.end),
            )
            pyemmo_line_list.append(translated_line)

        else:
            # translate an Arc1, Arc2 into CircleArc
            if abs(geo_element.get_angle(is_deg=True)) >= 180:
                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=build_pyemmo_point(geo_element.get_begin()),
                    endPoint=build_pyemmo_point(geo_element.get_middle()),
                    centerPoint=build_pyemmo_point(geo_element.get_center()),
                )
                pyemmo_line_list.append(translated_line)

                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=build_pyemmo_point(geo_element.get_middle()),
                    endPoint=build_pyemmo_point(geo_element.get_end()),
                    centerPoint=build_pyemmo_point(geo_element.get_center()),
                )
                pyemmo_line_list.append(translated_line)

            else:
                translated_line = CircleArc(
                    name="CircleArc",
                    startPoint=build_pyemmo_point(geo_element.get_begin()),
                    endPoint=build_pyemmo_point(geo_element.get_end()),
                    centerPoint=build_pyemmo_point(geo_element.get_center()),
                )
                pyemmo_line_list.append(translated_line)

    return pyemmo_line_list
