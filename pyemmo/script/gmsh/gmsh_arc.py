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

This module includes the `GmshLine` class, which represents a line segment in 3D space.
The class allows for the definition of a line with a unique tag, start and end points,
a name, and a type.

Classes:
    - GmshLine: Represents a line segment in 3D space with attributes for identifying
      the line, specifying its start and end points (as `GmshPoint` objects), and
      assigning a name and type to the line.

Usage:
    - Instantiate `GmshLine` with a unique tag, start and end points, and optionally
      a name and type.
    - Access and modify the line's properties through getter and setter methods.
    - Utilize the string representation for debugging and logging purposes.

Example:

.. python:

    from module_name import GmshLine, GmshPoint
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

from typing import Union

import gmsh

from ..geometry.circleArc import CircleArc
from ..geometry.point import Point
from .gmsh_point import GmshPoint


class GmshArc(CircleArc):
    """
    TODO

    Attributes:
        tag (int): The unique identifier for the line.
        start_point (GmshPoint): The starting point of the line.
        end_point (GmshPoint): The ending point of the line.
        name (str): The name of the line.
        type (str): The type of the line (e.g., "Line", "Circle").
    """

    def __init__(
        self,
        tag: int = -1,
        start_point: Union[GmshPoint, None] = None,
        center_point: Union[GmshPoint, None] = None,
        end_point: Union[GmshPoint, None] = None,
        name: str = "",
    ):
        """
        Constructor for the GmshLine class. With two possible creation methods:
        1.  Specifiy a **existing** gmsh line tag with ``tag``:
            The init method will find start and end point from gmsh and try to calculate
            the center point by creating a middle point on the existing arc. For more
            details see https://gitlab.onelab.info/gmsh/gmsh/-/issues/2394
        2.  Define the arc like the classical PyEMMO CircleArc by giving 3 GmshPoint
            objects. The class will then call the CircleArc.__init__() method.

        Args:
            tag (int): The unique identifier for the line.
            start_point (GmshPoint, optional): The starting point of the line.

            center_point: Union[GmshPoint, None] = None,

            end_point (GmshPoint, optional): The ending point of the line.
            name (str, optional): The name of the line. Defaults to an empty string.
        """
        if tag >= 0 and (start_point, center_point, end_point) == (None, None, None):
            # tag is given and points are None -> try to find points from gmsh and
            # create center point.
            self._init_with_tag(tag, name)
        elif tag < 0 and all(
            filter(
                lambda p: isinstance(p, Point), (start_point, center_point, end_point)
            )
        ):
            # no tag given, but all three points are of type Point
            super().__init__(name, start_point, center_point, end_point)
            self.tag = self.id
        else:
            raise ValueError("Can not create GmshArc for input of tag AND points!")

    def _init_with_tag(self, tag: int, name: str):
        self.tag = tag
        assert (
            gmsh.model.get_type(1, tag) == "Circle"
        ), "Given curve tag for GmshArc does not yeald to Gmsh Circle instance!"
        point_tags = gmsh.model.get_boundary(dimTags=[(1, tag)])
        self.start_point = GmshPoint(
            point_tags[0][1], gmsh.model.get_value(0, point_tags[0][1], [])
        )
        self.end_point = GmshPoint(
            point_tags[1][1],
            gmsh.model.get_value(0, point_tags[1][1], []),
        )
        center_tag, center_coords = get_center(tag)
        self.center = GmshPoint(center_tag, center_coords)
        if not name:
            name = gmsh.model.get_entity_name(1, tag)
        self.name = name

    @property
    def tag(self) -> int:
        """
        Getter for the tag property.

        Returns:
            int: The unique identifier for the line.
        """
        return self._tag

    @property
    def id(self) -> int:
        """
        Getter for the tag property but with name 'id' to be compatible with PyEMMO.

        Returns:
            int: The unique identifier for the line.
        """
        return self._tag

    @tag.setter
    def tag(self, new_tag: int):
        """
        Setter for the tag property.

        Args:
            new_tag (int): The new tag value to set.
        """

        self._tag = new_tag

    @property
    def start_point(self) -> GmshPoint:
        """
        Getter for the start_point property.

        Returns:
            GmshPoint: The starting point of the line.
        """
        return self._start_point

    @start_point.setter
    def start_point(self, new_start_point: GmshPoint):
        """
        Setter for the start_point property.

        Args:
            new_start_point (GmshPoint): The new starting point to set.
        """
        assert isinstance(new_start_point, GmshPoint)
        self._start_point = new_start_point

    @property
    def end_point(self) -> GmshPoint:
        """
        Getter for the end_point property.

        Returns:
            GmshPoint: The ending point of the line.
        """
        return self._end_point

    @end_point.setter
    def end_point(self, new_end_point: GmshPoint):
        """
        Setter for the end_point property.

        Args:
            new_end_point (GmshPoint): The new ending point to set.
        """
        self._end_point = new_end_point

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshLine.

        Returns:
            str: A string containing the tag, name, type, and the start and end points of the line.
        """
        return (
            f"GmshLine(tag={self.tag}, name={self.name}, type={self.type}, "
            f"start_point=({self.start_point.x}, {self.start_point.y}, {self.start_point.z}), "
            f"end_point=({self.end_point.x}, {self.end_point.y}, {self.end_point.z}))"
        )


## The following is the solution to issue #2394 on the Gmsh Gitlab page on how to get
# the center point of an arc by only knowing the start and end point of the arc..
def is_int(val):
    try:
        return int(val) == val
    except TypeError:
        return False


import numpy as np
from numpy.typing import NDArray


def get_point_coord(tag: int):
    """
    Get coordinate of point.
    """
    return gmsh.model.get_value(0, tag, [])


def dist(p1, p2):
    """
    Return the distance between points/3D-coordinates
    """
    if is_int(p1):  # if tag and not coordinates
        coord1 = get_point_coord(p1)
    else:
        coord1 = p1
    if is_int(p2):  # if tag and not coordinates
        coord2 = get_point_coord(p2)
    else:
        coord2 = p2

    return np.sqrt(
        (coord1[0] - coord2[0]) ** 2
        + (coord1[1] - coord2[1]) ** 2
        + (coord1[2] - coord2[2]) ** 2
    )


def get_closest_point(coord, vtol: float = 1e-6):
    """
    Return (tag, coord) of the closest point to 'coord' up to a distance 'vtol', otherwise return (None, None)
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
        coord2 = get_point_coord(dim_tag[1])
        d = dist(coord, coord2)
        if d <= vtol and d < best_dist:
            best_tag = dim_tag[1]
            best_coord = coord2
            best_dist = d
    if best_tag is None:
        raise ValueError(f"Point close to coord {coord} not found.")

    return (best_tag, best_coord)


def get_center(l_tag) -> tuple[int, NDArray]:
    """
    Return (in a very complicated way) the center tag of a circle arc (if available) and
    its coordinate. Only works for points on z-normal plane.
    """
    if gmsh.model.getType(1, l_tag) != "Circle":
        raise ValueError("Can only calculate the radius for a circle arc")

    p1, p3 = gmsh.model.getAdjacencies(1, l_tag)[1]
    coord1, coord3 = get_point_coord(p1), get_point_coord(p3)
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
        c_tag, coord = get_closest_point(coord, vtol=1e-5)
        return c_tag, coord
    except ValueError:
        return None, coord
