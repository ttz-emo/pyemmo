#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
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
"""
This module provides various utility functions for geometric calculations
utilizing the Gmsh library, specifically focused on handling geometrical
entities such as points, lines, and arcs within a 2D plane.

The main functionalities include:
- Extracting unique point tags from a list of geometrical dimension tags.
- Calculating the maximal and minimal radii from a set of dimensional tags.
- Filtering curves or lines based on their radius or angle relative to the x-axis.

Functions:
- get_point_tags(dim_tags): Extracts unique point tags from dimension tags.
- get_max_radius(dim_tags): Finds the maximum radius in a list of dim-tags.
- get_min_radius(dim_tags): Finds the minimum radius in a list of dim-tags.
- filter_curves_on_radius(line_list, radius): Filters curves by a specified radius.
- filter_lines_at_angle(line_list, angle): Filters lines based on their angle to the
  x-axis.

The module is part of the PyEMMO project, developed by TTZ-EMO at the Technical
University of Applied Sciences Würzburg-Schweinfurt.

Author:
    Max Schuler

Note:
    This docstring was created by OpenAI GPT-4o.
"""
from typing import Literal

import gmsh
import numpy as np

from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from .gmsh_line import GmshLine


################################## MISC FUNCTIONS ######################################
def get_point_tags(dim_tags: list[tuple[Literal[0, 1, 2], int]]) -> list[float]:
    """Extract list of _unique_ point tags from a given list of dim tags.

    This uses:
        - ``gmsh.model.get_boundary`` to get surface point tags.
        - ``gmsh.model.get_adjacencies`` to get curve point tags.

    Given point tags are directly included in the list.

    Args:
        dim_tags (list[tuple[Literal[0,1,2], int]]): List of dimension and tags

    Raises:
        ValueError: If dimension identifier is not in 0,1 or 2

    Returns:
        list[float]: List of unique point tags (= no duplicated IDs).
    """
    p_tags: list[int] = []
    for dim_tag in dim_tags:
        if dim_tag[0] == 2:
            # case surface
            p_dim_tags = gmsh.model.get_boundary(dim_tag, recursive=True)
            p_tags.extend([dt[1] for dt in p_dim_tags])
        elif dim_tag[0] == 1:
            # case curve
            _, point_tags = gmsh.model.get_adjacencies(1, dim_tag[1])
            p_tags.extend([point_tags[0], point_tags[1]])
        elif dim_tag[0] == 0:
            # case point
            p_tags.append(dim_tag[1])
        else:
            raise ValueError(
                f"Cannot handle object of dimension {dim_tag[0]} (id: {dim_tag[1]})"
            )
    return list(set(p_tags))  # remove duplicates


def get_max_radius(dim_tags: list[tuple[Literal[0, 1, 2], int]]) -> float:
    """Get the maximal radius of a list of line dim-tags.

    Args:
        surf_dim_tags (list[int]): List of surface dim tags, like ``(2, tag)``

    Returns:
        float: Maximal radius of bounding points.
    """
    max_radius = 0
    p_tags = get_point_tags(dim_tags)
    for p_tag in p_tags:
        coords = gmsh.model.get_value(0, p_tag, [])
        radius = np.linalg.norm(coords)
        max_radius = max(max_radius, radius)
    return max_radius


def get_min_radius(dim_tags: list[tuple[Literal[0, 1, 2], int]]) -> float:
    """Get the minimal radius of a list of curve dim-tags.

    Args:
        dim_tags (list[int]): List of dim tags, like ``(dim, tag)``

    Returns:
        float: Minimal radius of bounding points.
    """
    if not dim_tags:
        raise RuntimeError("Empty dim-tag list given!")
    p_tags = get_point_tags(dim_tags)  # get unique point tags in dim_tags
    min_radius = 1e18
    for p_tag in p_tags:
        coords = gmsh.model.get_value(0, p_tag, [])
        radius = np.linalg.norm(coords)
        min_radius = min(min_radius, radius)
    return min_radius


def filter_curves_on_radius(line_list: list[GmshLine], radius: float) -> list[GmshLine]:
    """Filter all lines from a list of lines that are TODO

    Args:
        line_list (list[Line]): List of (boundary) lines.
        radius (float): TODO.

    Returns:
        list[Line]: List of lines that are on the specified radius.
    """
    curved_lines = filter(lambda line: isinstance(line, CircleArc), line_list)
    lines_on_radius: list[CircleArc] = []
    for line in curved_lines:
        # we need to check start and end point angle here because there could be a line
        # on the boundary that has the same vector-angle, but is no secondary line!
        if all(
            np.isclose(
                [
                    line.start_point.radius,
                    line.end_point.radius,
                ],
                [radius, radius],
                atol=1e-6,
            )
        ):
            lines_on_radius.append(line)
    return lines_on_radius


def filter_lines_at_angle(line_list: list[Line], angle: float) -> list[Line]:
    """Filter all lines from a list of lines that are on a specific ``angle`` to the
    x-axis in the xy-plane.

    Args:
        line_list (list[Line]): List of (boundary) lines.
        angle (float): Angle of axis in xy-plane to filter.

    Returns:
        list[Line]: List of lines that are on the specified axis.
    """
    straight_lines = filter(lambda line: type(line) in (Line, GmshLine), line_list)
    lines_at_angle: list[Line] = []
    for line in straight_lines:
        # we need to check start and end point angle here because there could be a line
        # on the boundary that has the same vector-angle, but is no secondary line!
        if all(
            np.isclose(
                [
                    line.start_point.getAngleToX() % (2 * np.pi),
                    line.end_point.getAngleToX() % (2 * np.pi),
                ],
                [angle, angle],
                atol=1e-6,
            )
        ):
            lines_at_angle.append(line)
    return lines_at_angle


################################ END MISC FUNCTIONS ####################################
