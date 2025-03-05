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
Module for defining and manipulating geometric lines in 3D space, specifically for use
with Gmsh.

This module includes the `GmshArc` class, which represents a curved segment in 3D space.
The class allows for the definition of a line with a unique tag, start and end points,
a name, and a type.

Classes:
    - GmshArc: Represents a line segment in 3D space with attributes for identifying
      the line, specifying its start and end points (as `GmshPoint` objects), and
      assigning a name and type to the line.

Usage:
    - Instantiate `GmshArc` with a unique tag, start and end points, and optionally
      a name and type.
    - Access and modify the line's properties through getter and setter methods.
    - Utilize the string representation for debugging and logging purposes.

Example:

.. python:

    from module_name import GmshArc, GmshPoint
    import numpy as np

    # Create GmshPoint instances
    center = GmshPoint(tag=1, coords=np.array([0.0, 0.0, 0.0]))
    start = GmshPoint(tag=2, coords=np.array([1.0, 0.0, 0.0]))
    end = GmshPoint(tag=3, coords=np.array([0.0, 1.0, 0.0]))

    # Define a line using GmshArc
    line = GmshArc(
        tag=1,
        start_point=start,
        center_point=center,
        end_point=end,
        name="Quarter circle",
    )

    # Print line details
    print(line)

Author:
    Max Schuler

Note:
    This docstring was created by ChatGPT.
"""

from typing import Literal, Union

import gmsh
import numpy as np
from numpy.typing import NDArray

from ..geometry.circleArc import CircleArc
from .gmsh_geometry import GmshGeometry
from .gmsh_point import GmshPoint


class GmshArc(CircleArc, GmshGeometry):
    """
    TODO

    Attributes:
        tag (int): The unique identifier for the line.
        start_point (GmshPoint): The starting point of the line.
        end_point (GmshPoint): The ending point of the line.
        name (str): The name of the line.
        type (str): The type of the line (e.g., "Line", "Circle").
    """

    @property
    def dim(self) -> Literal[1]:
        """Dimension of the CircleArc in Gmsh = 1"""
        return 1

    def __init__(
        self,
        tag: int = -1,
        start_point: Union[GmshPoint, None] = None,
        center_point: Union[GmshPoint, None] = None,
        end_point: Union[GmshPoint, None] = None,
        name: str = "",
    ):
        """
        Constructor for the GmshArc class. With two possible creation methods:
        1.  Specifiy a **existing** gmsh line tag with ``tag``:
            The init method will find start and end point from gmsh and try to calculate
            the center point by creating a middle point on the existing arc. For more
            details see https://gitlab.onelab.info/gmsh/gmsh/-/issues/2394
        2.  Define the arc like the classical PyEMMO CircleArc by giving 3 GmshPoint
            objects.

        Args:
            tag (int): The unique identifier for the line.
            start_point (GmshPoint, optional): The starting point of the line. Defaults
                to None.
            center_point (GmshPoint): The center point of the line. Defaults to None.
            end_point (GmshPoint, optional): The ending point of the line. Defaults to
                None.
            name (str, optional): The name of the line. Defaults to an empty string.
        """
        if tag == -1:
            if not all(
                p is not None and isinstance(p, GmshPoint)
                for p in [start_point, center_point, end_point]
            ):
                raise ValueError("All points must be of type GmshPoint for GmshArc!")
            # no tag given, but all three points are of type GmshPoint
            self._id = gmsh.model.occ.addCircleArc(
                start_point.id, center_point.id, end_point.id
            )
            self._start_point = start_point
            self._center = center_point
            self._end_point = end_point
            self.name = name
        elif tag >= 0:
            if (start_point, center_point, end_point) == (None, None, None):
                # tag is given and points are None -> try to find points from gmsh and
                # create center point.
                self._init_with_tag(tag, name)
            else:
                raise ValueError("Can not create GmshArc for input of tag AND points!")
        else:
            raise ValueError("Tag must be a positive integer or -1 if points given!")

    def _init_with_tag(self, tag: int, name: str):
        """Init GmshArc with existing tag.

        Args:
            tag (int): Gmsh OCC tag of the CircleArc.
            name (str): Name of the CircleArc.

        Raises:
            ValueError: If tag is not a CircleArc.
            ValueError: If curve tag does not exist in current Gmsh model.
        """
        gmsh.model.occ.synchronize()
        if (1, tag) not in gmsh.model.getEntities(1):
            raise ValueError(f"Curve with tag {tag=} does not exist in Gmsh model!")
        # TODO: Create separate handle for TrimmedCurve type.
        if gmsh.model.get_type(1, tag) not in ("Circle", "TrimmedCurve"):
            raise ValueError(
                f"Curve with {tag=} is not a Circle but {gmsh.model.get_type(1, tag)}!"
            )
        self._id = tag  # set tag
        if not name:
            name = gmsh.model.get_entity_name(1, tag)
        self.name = name

        # # Skip the following since point info is accessed at runtime
        # point_tags = gmsh.model.get_boundary(dimTags=[(1, tag)])
        # self._start_point = GmshPoint(
        #     point_tags[0][1], gmsh.model.get_value(0, point_tags[0][1], [])
        # )
        # self._end_point = GmshPoint(
        #     point_tags[1][1],
        #     gmsh.model.get_value(0, point_tags[1][1], []),
        # )
        # center_tag, center_coords = _get_center(tag)
        # if center_tag is None:
        #     # center point not existant yet!
        #     self.center = Point(
        #         f"Center of CircleArc {self.id}",
        #         center_coords[0],
        #         center_coords[1],
        #         center_coords[2],
        #     )
        # else:
        #     self.center = GmshPoint(center_tag, center_coords)

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshArc.

        Returns:
            str: A string containing the tag, name, type, and the start and end points
            of the line.
        """
        return (
            f"GmshArc(name={self.name}, id={self.id}, "
            f"start_point=({self.start_point.x}, {self.start_point.y}, {self.start_point.z}), "
            f"end_point=({self.end_point.x}, {self.end_point.y}, {self.end_point.z}))"
        )

    @property
    def start_point(self) -> GmshPoint:
        """
        Getter for the start_point property.

        Returns:
            GmshPoint: The starting point of the line.
        """
        gmsh.model.occ.synchronize()
        point_tags = gmsh.model.get_boundary(dimTags=[(1, self.id)])
        return GmshPoint(point_tags[0][1])

    @start_point.setter
    def start_point(self, new_start_point: GmshPoint):
        """
        Setter for the start_point property.

        Args:
            new_start_point (GmshPoint): The new starting point to set.
        """
        raise ValueError("Can not change start point of GmshArc!")

    @property
    def end_point(self) -> GmshPoint:
        """
        Getter for the end_point property.

        Returns:
            GmshPoint: The ending point of the line.
        """
        gmsh.model.occ.synchronize()
        point_tags = gmsh.model.get_boundary(dimTags=[(1, self.id)])
        return GmshPoint(point_tags[1][1])

    @end_point.setter
    def end_point(self, new_end_point: GmshPoint):
        """
        Setter for the end_point property.

        Args:
            new_end_point (GmshPoint): The new ending point to set.
        """
        raise ValueError("Can not change end point of GmshArc!")

    @property
    def center(self) -> GmshPoint:
        """
        Getter for the center property.

        Returns:
            GmshPoint: The center point of the arc.
        """
        gmsh.model.occ.synchronize()
        center_tag, center_coords = _get_center(self)
        if center_tag:
            # if center point exists
            return GmshPoint(center_tag)
        else:
            # otherwise create a new point
            return GmshPoint(coords=center_coords)

    @center.setter
    def center(self, new_center: GmshPoint):
        """
        Setter for the center property.

        Args:
            new_center (GmshPoint): The new center point to set.
        """
        raise ValueError("Can not change center point of GmshArc!")


GmshArc.duplicate = GmshGeometry.duplicate
GmshArc.combine = GmshGeometry.combine
GmshArc.rotateX = GmshGeometry.rotateX
GmshArc.rotateY = GmshGeometry.rotateY
GmshArc.rotateZ = GmshGeometry.rotateZ


## The following is the solution to issue #2394 on the Gmsh Gitlab page on how to get
# the center point of an arc by only knowing the start and end point of the arc..
def _is_int(val):
    try:
        return int(val) == val
    except TypeError:
        return False


def _get_point_coord(tag: int):
    """
    Get coordinate of point.
    """
    return gmsh.model.get_value(0, tag, [])


def _dist(p1: int, p2: int) -> float:
    """
    Return the distance between points/3D-coordinates
    """
    if _is_int(p1):  # if tag and not coordinates
        coord1 = _get_point_coord(p1)
    else:
        coord1 = p1
    if _is_int(p2):  # if tag and not coordinates
        coord2 = _get_point_coord(p2)
    else:
        coord2 = p2

    return np.sqrt(
        (coord1[0] - coord2[0]) ** 2
        + (coord1[1] - coord2[1]) ** 2
        + (coord1[2] - coord2[2]) ** 2
    )


def _get_closest_point(coord, vtol: float = 1e-6):
    """
    Return (tag, coord) of the closest point to 'coord' up to a distance 'vtol',
    otherwise return (None, None)

    Warning: slow
    """
    dim_tags = gmsh.model.getEntitiesInBoundingBox(
        coord[0] - vtol,
        coord[1] - vtol,
        coord[2] - vtol,
        coord[0] + vtol,
        coord[1] + vtol,
        coord[2] + vtol,
        dim=0,
    )
    best_tag = None
    best_coord = None
    best_dist = np.inf
    for dim_tag in dim_tags:
        coord2 = _get_point_coord(dim_tag[1])
        d = _dist(coord, coord2)
        if d <= vtol and d < best_dist:
            best_tag = dim_tag[1]
            best_coord = coord2
            best_dist = d
    if best_tag is None:
        raise ValueError(f"Point close to coord {coord} not found.")

    return (best_tag, best_coord)


def _get_center(self) -> tuple[int, NDArray]:
    """
    Return (in a very complicated way) the center tag of a circle arc (if available) and
    its coordinate. Only works for points on z-normal plane.
    """
    l_tag = self.id
    if gmsh.model.getType(1, l_tag) not in ("Circle", "TrimmedCurve"):
        raise ValueError("Can only calculate the radius for a circle arc")

    p1, p3 = gmsh.model.getAdjacencies(1, l_tag)[1]
    coord1, coord3 = _get_point_coord(p1), _get_point_coord(p3)
    coord2 = gmsh.model.getClosestPoint(1, l_tag, (coord1 + coord3) / 2)[0]
    A = np.array(
        [
            [2 * coord1[0], 2 * coord1[1], 1],
            [2 * coord2[0], 2 * coord2[1], 1],
            [2 * coord3[0], 2 * coord3[1], 1],
        ]
    )
    B = -np.array(
        [
            coord1[0] ** 2 + coord1[1] ** 2,
            coord2[0] ** 2 + coord2[1] ** 2,
            coord3[0] ** 2 + coord3[1] ** 2,
        ]
    )
    X = np.linalg.solve(A, B)
    coord = np.array([-X[0], -X[1], coord1[2]])

    try:
        c_tag, coord = _get_closest_point(coord, vtol=1e-5)
        return c_tag, coord
    except ValueError:
        return None, coord
