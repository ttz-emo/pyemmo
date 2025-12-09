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
from __future__ import annotations

import logging
from typing import Literal

import gmsh
import numpy as np

from ...definitions import DEFAULT_GEO_TOL
from ..geometry import defaultCenterPoint
from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from ..geometry.physicalElement import PhysicalElement
from ..geometry.surface import Surface
from . import DimTag
from .gmsh_arc import GmshArc
from .gmsh_line import GmshLine
from .gmsh_point import GmshPoint

# TODO: add tests for misc functions!!


def get_dim_tags(geo_list: list[Line | Surface | PhysicalElement]) -> list[DimTag]:
    """
    Extracts dimension tag value pairs from a list of geometric elements.

    This function processes a list of elements which may include lines, surfaces,
    or physical elements, and generates a corresponding list of Gmsh dimension tags.
    Each dimension tag is represented as a tuple containing a dimension identifier
    (1 for lines, 2 for surfaces) and its Gmsh entity ID.

    If an element is a `PhysicalElement`, the function recursively processes its
    associated ``geo_list`` property to extract dimension tags for its constituent
    elements.

    Args:
        geo_list (list[Union[Line, Surface, PhysicalElement]]): A list of geometric
            elements which may include `Line`, `Surface`, or `PhysicalElement` instances.

    Returns:
        list[DimTag]: A list of dimension tags in the form of tuples, where each tuple
        consists of a dimension identifier and an entity ID.

    Raises:
        RuntimeError: If an element in the geo_list is neither a `Surface` nor a `Line`.

    Example:

    ..code::

        >>> elements = [Line(id=1), Surface(id=2), PhysicalElement(geo_list=[Line(id=3)])]
        >>> dim_tags = get_dim_tags(elements)
        >>> print(dim_tags)
        [(1, 1), (2, 2), (1, 3)]
    """
    dim_tags: list[tuple[Literal[1, 2], int]] = []
    for element in geo_list:
        if isinstance(element, PhysicalElement):
            dim_tags.extend(get_dim_tags(element.geo_list))
        elif isinstance(element, Surface):
            dim_tags.append((2, element.id))
        elif isinstance(element, Line):
            dim_tags.append((1, element.id))
        else:
            raise RuntimeError("Geometry not Surface or Line!")
    return dim_tags


def get_point_tags(dim_tags: list[DimTag]) -> list[DimTag]:
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
            try:
                p_dim_tags = gmsh.model.get_boundary([dim_tag], recursive=True)
            except Exception as exce:
                if "Unknown model face" in str(exce):
                    gmsh.model.occ.synchronize()
                    p_dim_tags = gmsh.model.get_boundary([dim_tag], recursive=True)
                else:
                    raise exce

            p_tags.extend([dt[1] for dt in p_dim_tags])
        elif dim_tag[0] == 1:
            # case curve
            try:
                _, point_tags = gmsh.model.get_adjacencies(1, dim_tag[1])
            except Exception as exce:
                if f"Curve {dim_tag[1]} does not exist" in str(exce):
                    gmsh.model.occ.synchronize()
                    _, point_tags = gmsh.model.get_adjacencies(1, dim_tag[1])
                else:
                    raise exce
            p_tags.extend([point_tags[0], point_tags[1]])
        elif dim_tag[0] == 0:
            # case point
            p_tags.append(dim_tag[1])
        else:
            raise ValueError(
                f"Cannot handle object of dimension {dim_tag[0]} (id: {dim_tag[1]})"
            )

    return list(set(p_tags))  # remove duplicates


def get_max_radius(dim_tags: list[DimTag]) -> float:
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


def get_min_radius(dim_tags: list[DimTag]) -> float:
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
    """Filter all lines from a list of lines that are on a specific ``angle`` [rad] to
    the x-axis in the xy-plane.

    Args:
        line_list (list[Line]): List of (boundary) lines.
        angle (float): Angle of axis in xy-plane to filter in radians.

    Returns:
        list[Line]: List of lines that are on the specified axis.
    """
    straight_lines = filter(lambda line: type(line) in (Line, GmshLine), line_list)
    lines_at_angle: list[Line] = []
    for line in straight_lines:
        # we need to check start and end point angle here because there could be a line
        # on the boundary that has the same vector-angle, but is no secondary line!
        # Additionally we need to check for the center point because its on every angle.
        if line.start_point.isEqual(defaultCenterPoint, DEFAULT_GEO_TOL) or np.isclose(
            line.start_point.getAngleToX() % (2 * np.pi),
            angle,
            atol=1e-6,
        ):
            # start point is center or on angle
            if line.end_point.isEqual(
                defaultCenterPoint, DEFAULT_GEO_TOL
            ) or np.isclose(
                line.end_point.getAngleToX() % (2 * np.pi),
                angle,
                atol=1e-6,
            ):
                # end point is center or at angle aswell
                lines_at_angle.append(line)
    return lines_at_angle


def is_straight(curve_tag: int) -> bool:
    """Check if the gmsh curve is straight.

    This can be especially useful if the curve type if not Line or Arc, which is the
    case for OCC TrimmedCurve type.

    Returns:
        bool: True if the line is straight, False otherwise.
    """
    # get boundary points of the curve:
    point_tags = gmsh.model.getBoundary([1, curve_tag])
    start_coords = gmsh.model.get_value(0, point_tags[0][1], [])
    end_coords = gmsh.model.get_value(0, point_tags[1][1], [])
    # calculate the distance between start and end point:
    distance = np.linalg.norm(np.array(start_coords) - np.array(end_coords))
    # if the distance is equal to gmsh.model.occ.getMass, the line is straight:
    return np.isclose(
        distance, gmsh.model.occ.getMass(1, curve_tag), atol=DEFAULT_GEO_TOL
    )


def fix_missing_mesh_sizes() -> None:
    """
    Check the mesh size of the all points in the current ``gmsh.model``.
    Due to issues with OCC it can happen that points lose their mesh size and get
    mesh size = 0. In this case, search for the closest point(s) using
    ``gmsh.model.getEntitiesInBoundingBox`` and set the mesh size to the first found
    point mesh size.
    """
    nbr_fixed = 0
    all_points = gmsh.model.getEntities(0)
    logger = logging.getLogger(__name__)
    for dim_tag in all_points:
        p = GmshPoint(dim_tag[1])
        if p.meshLength == 0:
            logger.debug("Point %s with missing mesh size.", p)
            dim_tags = []
            xmin, ymin, _, xmax, ymax, _ = gmsh.model.getBoundingBox(-1, -1)
            # initial value is 1/1000 of whole bounding box
            dl = np.mean([xmax - xmin, ymax - ymin]) / 1000
            nbr_loops = 0
            while not dim_tags:
                dim_tags = gmsh.model.getEntitiesInBoundingBox(
                    xmin=p.x - dl,
                    ymin=p.y - dl,
                    zmin=-1,
                    xmax=p.x + dl,
                    ymax=p.y + dl,
                    zmax=1,
                    dim=0,
                )
                # remove point itself because its allways found:
                dim_tags.remove((0, p.id))
                dl *= 2  # increase search radius
                nbr_loops += 1
            logger.debug("Bounding box size where next point(s) were found: %e", dl)
            p.meshLength = gmsh.model.mesh.getSizes(dimTags=[dim_tags[0]])[0]
            logger.debug(
                "Set mesh size of point %i to %.3e of point %i after %i iterations.",
                p.id,
                p.meshLength,
                dim_tags[0],
                nbr_loops,
            )
            nbr_fixed += 1
    logger.debug("Fixed %i points with missing mesh size.", nbr_fixed)


def get_global_center() -> GmshPoint:
    """Get the global center point (coordinates (0,0,0) by using
    gmsh.model.getEntitiesInBoundingBox(..) on point in origin or create the center
    point.

    Returns:
        GmshPoint: Center point for current gmsh model.
    """
    try:
        center_dimTags = gmsh.model.getEntitiesInBoundingBox(
            -DEFAULT_GEO_TOL,
            -DEFAULT_GEO_TOL,
            -DEFAULT_GEO_TOL,
            DEFAULT_GEO_TOL,
            DEFAULT_GEO_TOL,
            DEFAULT_GEO_TOL,
            0,
        )
        return GmshPoint(center_dimTags[0][1])
    except:  # pylint: disable=bare-except
        return GmshPoint.from_coordinates((0, 0), name="CenterPoint")


def create_disk(radius: float, center: GmshPoint | None = None) -> list[GmshArc]:
    """Workaround for gmsh.model.occ.addDisk() function, because the original gmsh
    kernel only supports arcs up to 90°. If we want to export our model as .geo_unrolled
    file we need to create these arcs separatly otherwise they will be exported as spline.

    Args:
        radius (float): Circle radius
        center (GmshPoint | None, optional): Circle center point. Defaults to global
            center point at (0,0).

    Returns:
        list[GmshArc]: List of four GmshArc object forming the contour of a circle.
    """
    if not center:
        # get or create default center point
        center = get_global_center()
    # create first point by x = center.x + radius
    p0 = GmshPoint.from_coordinates((center.x + radius, center.y, center.z))
    p1 = p0  # save p0 for later to construct last arc
    arcs = []  # init arc list
    for _ in range(3):
        # duplicate and rotate p1 by 90°
        p2 = p1.duplicate()
        p2.rotateZ(center, np.pi / 2)
        arcs.append(GmshArc.from_points(p1, center, p2))  # create arc
        p1 = p2  # update p1 for next iteration
    arcs.append(GmshArc.from_points(p1, center, p0))  # create final arc using p0
    return arcs
