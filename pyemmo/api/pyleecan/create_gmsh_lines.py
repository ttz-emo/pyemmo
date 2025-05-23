#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
"""Module: create_gmsh_lines

This module provides functions to convert geometry elements from pyleecan to pyemmo format.

Module dependencies:
    - pyleecan.Classes.Segment.Segment
    - pyleecan.Classes.Arc1.Arc1
    - pyleecan.Classes.Arc2.Arc2
    - pyleecan.Classes.Arc3.Arc3
    - ...script.geometry.line.Line
    - ...script.geometry.circleArc.CircleArc
    - .build_pyemmo_point.build_pyemmo_point

Functions:
    -   ``create_gmsh_lines``: Translates a list of pyleecan curves into a
        list of pyemmo curves.

Example:

    .. code:: python

        pyleecan_line_list = [Segment(...), Arc1(...), ...]
        pyemmo_line_list = create_gmsh_lines(pyleecan_line_list)
        # Returns a list of pyemmo curves corresponding to the input pyleecan curves.

Raises:
    TypeError: If pyleecan_line_list is not of type 'list'.
    IndexError: If pyleecan_line_list is empty.
"""

from __future__ import annotations

from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc2 import Arc2
from pyleecan.Classes.Arc3 import Arc3
from pyleecan.Classes.Segment import Segment

from ...script.gmsh.gmsh_arc import GmshArc
from ...script.gmsh.gmsh_line import GmshLine
from .create_gmsh_point import create_gmsh_point


def create_gmsh_lines(
    pyleecan_lines: list[Segment | Arc1 | Arc2 | Arc3],
) -> list[GmshLine | GmshArc]:
    """Translates a list of pyleecan curves into a list of pyemmo curves.

    This function translates a list of pyleecan curves (Segment, Arc1, Arc2, Arc3)
    into a list of pyemmo curves (Line, CircleArc).

    Args:
        pyleecan_lines (list[Union[Segment, Arc1, Arc2, Arc3]]): A list of curves
            from a pyleecan-surface.

    Returns:
        list[Union[Line, CircleArc]]: A list of curves for the pyemmo-surface.

    Raises:
        TypeError: If pyleecan_lines is not of type 'list'.
        IndexError: If pyleecan_lines is empty.
    """
    pyemmo_line_list = []

    if not isinstance(pyleecan_lines, list):
        raise TypeError(
            "Type of pyleecan_line_list is not 'list'. No translation possible."
        )

    if len(pyleecan_lines) == 0:
        raise IndexError(
            "The pyleecan_line_list provided is empty. No translation possible."
        )

    for line in pyleecan_lines:
        if isinstance(line, Segment):
            # translate a Segment into a Line
            pyemmo_line_list.append(
                GmshLine.from_points(
                    start_point=create_gmsh_point(line.begin),
                    end_point=create_gmsh_point(line.end),
                    name="",
                )
            )

        else:
            # translate an Arc1, Arc2 into CircleArc
            if abs(line.get_angle(is_deg=True)) >= 180:
                # NOTE: Workaround for Gmsh handling of arcs with angle >90°. Split up
                # the arc into two arcs with angle <90°.
                pyemmo_line_list.append(
                    GmshArc.from_points(
                        start_point=create_gmsh_point(line.get_begin()),
                        end_point=create_gmsh_point(line.get_middle()),
                        center_point=create_gmsh_point(line.get_center()),
                        name="",
                    )
                )
                pyemmo_line_list.append(
                    GmshArc.from_points(
                        start_point=create_gmsh_point(line.get_middle()),
                        end_point=create_gmsh_point(line.get_end()),
                        center_point=create_gmsh_point(line.get_center()),
                        name="",
                    )
                )
            else:
                pyemmo_line_list.append(
                    GmshArc.from_points(
                        start_point=create_gmsh_point(line.get_begin()),
                        end_point=create_gmsh_point(line.get_end()),
                        center_point=create_gmsh_point(line.get_center()),
                        name="",
                    )
                )

    return pyemmo_line_list
