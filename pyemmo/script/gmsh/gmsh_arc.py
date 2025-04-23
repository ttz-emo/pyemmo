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
    center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
    start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
    end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

    # Define a line using GmshArc
    line = GmshArc.from_points(
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

from typing import Literal

import gmsh
import numpy as np
from numpy.typing import NDArray

from ..geometry.circleArc import CircleArc
from .gmsh_geometry import GmshGeometry
from .gmsh_line import GmshLine
from .gmsh_point import GmshPoint


class GmshArc(GmshLine, CircleArc):
    """GmshArc is a class that represents a circular arc in the Gmsh geometric modeling kernel.
    It inherits from both GmshLine and CircleArc, providing functionality to interact with
    and manipulate circular arcs in a Gmsh model.
    Attributes:
        dim (Literal[1]): The dimension of the CircleArc in Gmsh, which is always 1.
        id (int): The unique identifier (tag) of the arc in the Gmsh model.
        name (str): The name of the arc.
        center (GmshPoint): The center point of the arc.
        length (float): The length of the arc, calculated using Gmsh's geometric modeling functions.
    Methods:
        __init__(tag: int, name: str = ""):
            Initializes a GmshArc instance using an existing Gmsh line tag. Validates the tag
            and retrieves the start and end points of the arc.
        from_points(start_point: GmshPoint, center_point: GmshPoint, end_point: GmshPoint, name: str) -> GmshArc:
            Class method to create a new GmshArc instance by specifying the start, center,
            and end points of the arc.
        __str__() -> str:
            Returns a string representation of the GmshArc, including its name, ID, and
            start and end points.
        start_point (property):
            Getter for the starting point of the arc. Raises an error if an attempt is made
            to modify the start point.
        end_point (property):
            Getter for the ending point of the arc. Raises an error if an attempt is made
            to modify the end point.
        center (property):
            Getter for the center point of the arc. If the center point does not exist, it
            is created. Raises an error if an attempt is made to modify the center point.
        length (property):
            Getter for the length of the arc, calculated using Gmsh's geometric modeling
            functions.
        TypeError: If the provided tag is not a positive integer.
        ValueError: If the specified tag does not correspond to an existing curve in the
                    Gmsh model or if the provided points are not of type GmshPoint."""

    @property
    def dim(self) -> Literal[1]:
        """Dimension of the CircleArc in Gmsh = 1"""
        return 1

    def __init__(
        self,
        tag: int,
        name: str = "",
    ):
        """
        Constructor for the GmshArc class. Specifiy a **existing** gmsh line tag with ``tag``:
        The init method will find start and end point from gmsh and try to calculate
        the center point by creating a middle point on the existing arc. For more
        details see https://gitlab.onelab.info/gmsh/gmsh/-/issues/2394

        Optionally you can create a new arc by using the
        `from_points() <pyemmo.script.gmsh.gmsh_arc.GmshArc.from_points>`_ method by
        specifying the start, center and end point of the arc.

        Args:
            tag (int): The unique identifier for the line.
            name (str, optional): The name of the line. Defaults to an empty string.
        """
        if not isinstance(tag, (int, np.integer)):
            raise TypeError("Gmsh tag must be positive integer!")
        if (1, tag) not in gmsh.model.occ.getEntities(1):
            raise ValueError(f"Curve with tag {tag=} does not exist in Gmsh model!")
        # FIXME: Currently don't check line type, because synchronize() is too costly.
        # try:
        #     curve_type = gmsh.model.getType(1, tag)
        # except Exception as exce:
        #     if "does not exist" in str(exce) or "Unknown model curve" in str(exce):
        #         gmsh.model.occ.synchronize()
        #         curve_type = gmsh.model.getType(1, tag)
        #     else:
        #         raise exce
        # TODO: Create separate handle for TrimmedCurve type.
        # if curve_type not in ("Circle", "TrimmedCurve"):
        #     raise ValueError(
        #         f"Curve with {tag=} is not a Circle but {gmsh.model.get_type(1, tag)}!"
        #     )
        self._id = tag  # set tag
        self.name = name

    @classmethod
    def from_points(
        cls,
        start_point: GmshPoint,
        center_point: GmshPoint,
        end_point: GmshPoint,
        name: str = "",
    ):
        """Create a GmshArc instance from three GmshPoint objects representing the
        start point, center point, and end point of the arc.

        Args:
            start_point (GmshPoint): The starting point of the arc.
            center_point (GmshPoint): The center point of the arc.
            end_point (GmshPoint): The ending point of the arc.
            name (str): The name to assign to the arc.

        Returns:
            GmshArc: An instance of the GmshArc class.

        Raises:
            ValueError: If any of the provided points are not of type GmshPoint.
        """
        # make sure all points are of type GmshPoint
        if not all(
            isinstance(p, GmshPoint) for p in [start_point, center_point, end_point]
        ):
            raise ValueError("All points must be of type GmshPoint for GmshArc!")
        # create arc in gmsh
        arc_id = gmsh.model.occ.addCircleArc(
            start_point.id, center_point.id, end_point.id
        )
        # return class constructor with the new arc id and name
        return cls(arc_id, name)

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
        return self.points[0]

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
        return self.points[1]

        # point_dimTags = self._get_points()
        # return GmshPoint(point_dimTags[1][1])

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
        try:
            center_tag, center_coords = _get_center(self.id)
        except:
            gmsh.model.occ.synchronize()
            center_tag, center_coords = _get_center(self.id)

        if center_tag:
            # if center point exists
            return GmshPoint(center_tag)
        # otherwise create a new point
        return GmshPoint.from_coordinates(coords=center_coords)

    @center.setter
    def center(self, new_center: GmshPoint):
        """
        Setter for the center property.

        Args:
            new_center (GmshPoint): The new center point to set.
        """
        raise ValueError("Can not change center point of GmshArc!")

    @property
    def length(self) -> float:
        """Length of gmsh line by gmsh.model.occ.getMass(dim, tag)"""
        return gmsh.model.occ.getMass(self.dim, self.id)


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


def _get_center(l_tag) -> tuple[int, NDArray]:
    """
    Return (in a very complicated way) the center tag of a circle arc (if available) and
    its coordinate. Only works for points on z-normal plane.
    """
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
