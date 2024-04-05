#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
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

    if not isinstance(pyleecan_line_list, list):
        raise TypeError(
            "Type of pyleecan_line_list is not 'list'. No translation possible."
        )

    if len(pyleecan_line_list) == 0:
        raise IndexError(
            "The pyleecan_line_list provided is empty. No translation possible."
        )

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
