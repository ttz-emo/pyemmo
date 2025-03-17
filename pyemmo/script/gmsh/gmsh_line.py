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
a name.

Classes:
    - GmshLine: Represents a line segment in 3D space with attributes for identifying
      the line, specifying its start and end points (as `GmshPoint` objects), and
      assigning a name.

Usage:
    - Instantiate `GmshLine` with a unique tag, start and end points, and optionally
      a name.
    - Access and modify the line's properties through getter and setter methods.
    - Utilize the string representation for debugging and logging purposes.

Example:

.. python:

    from module_name import GmshLine, GmshPoint
    import numpy as np

    # Create GmshPoint instances
    start = GmshPoint(tag=1, coords=np.array([0.0, 0.0, 0.0]))
    end = GmshPoint(tag=2, coords=np.array([1.0, 1.0, 1.0]))

    # Define a line using GmshLine
    line = GmshLine(
        tag=1,
        start_point=start,
        end_point=end,
        name="Diagonal",
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
import numpy as np

from ..geometry import defaultCenterPoint
from ..geometry.line import Line
from ..geometry.point import Point
from . import DimTag
from .gmsh_geometry import GmshGeometry
from .gmsh_point import GmshPoint


class GmshLine(Line, GmshGeometry):
    """
    Represents a Gmsh line in 3D space defined by a start and end point, with a unique
    identifier (tag), a name. The start and end points are instances of
    GmshPoint. If they are not given the instance tries to find and create the points
    throught the gmsh api by calling:

    ..python:

        point_tags = gmsh.model.get_boundary(dimTags=[(1, tag)])
        start_point = GmshPoint(
            point_tags[0][1], gmsh.model.get_value(0, point_tags[0][1], [])
        )
        end_point = (
            point_tags[1][1],
            gmsh.model.get_value(0, point_tags[1][1], []),
        )

    Attributes:
        tag (int): The unique identifier for the line.
        start_point (GmshPoint): The starting point of the line.
        end_point (GmshPoint): The ending point of the line.
        name (str): The name of the line.
    """

    @property
    def dim(self) -> int:
        return 1

    def __init__(
        self,
        tag: int = -1,
        start_point: Union[GmshPoint, None] = None,
        end_point: Union[GmshPoint, None] = None,
        name: str = "",
    ):
        """
        Constructor for the GmshLine class.

        Args:
            tag (int): The unique identifier for the line.
            start_point (GmshPoint, optional): The starting point of the line.
            end_point (GmshPoint, optional): The ending point of the line.
            name (str, optional): The name of the line. Defaults to an empty string.
        """
        if not isinstance(tag, (int, np.integer)):
            raise TypeError("Gmsh tag must be positive integer!")

        if tag == -1:
            # init with start and end point
            self._id = gmsh.model.occ.addLine(start_point.id, end_point.id)
            self.name = name
        else:
            # init with tag
            gmsh.model.occ.synchronize()
            if (1, tag) not in gmsh.model.getEntities(1):
                raise ValueError(f"Curve with {tag=} does not exist in the model.")
            if gmsh.model.getType(1, tag) != "Line":
                raise ValueError(f"Curve with {tag=} is not of type Line.")
            self._id = tag
            # get boundary points:
            point_tags = gmsh.model.get_boundary(dimTags=[(1, tag)])
            start_point = GmshPoint(tag=point_tags[0][1])
            end_point = GmshPoint(tag=point_tags[1][1])
            # if no name given try to get it from gmsh
            if not name:
                name = gmsh.model.get_entity_name(1, tag)
            else:
                self.name = name
        # self._start_point = start_point
        # self._end_point = end_point

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshLine.

        Returns:
            str: A string containing the tag, name, type, and the start and end points
            of the line.
        """
        return (
            f"{self.__class__.__name__}(name={self.name}, id={self.id}, "
            f"start_point=({self.start_point.x:.1e}, {self.start_point.y:.1e}, {self.start_point.z:.1e}), "
            f"end_point=({self.end_point.x:.1e}, {self.end_point.y:.1e}, {self.end_point.z:.1e}))"
        )

    @property
    def start_point(self) -> GmshPoint:
        """
        Getter for the start_point property.

        Returns:
            GmshPoint: The starting point of the line.
        """
        tag = gmsh.model.getBoundary(dimTags=[(1, self.id)])[0][1]
        return GmshPoint(tag=tag)

    @start_point.setter
    def start_point(self, new_start_point: GmshPoint):
        """
        Setter for the start_point property.

        Args:
            new_start_point (GmshPoint): The new starting point to set.
        """
        raise AttributeError("Cannot set start_point of GmshLine!")

    @property
    def end_point(self) -> GmshPoint:
        """
        Getter for the end_point property.

        Returns:
            GmshPoint: The ending point of the line.
        """
        tag = gmsh.model.getBoundary(dimTags=[(1, self.id)])[1][1]
        return GmshPoint(tag=tag)

    @end_point.setter
    def end_point(self, new_end_point: GmshPoint):
        """
        Setter for the end_point property.

        Args:
            new_end_point (GmshPoint): The new ending point to set.
        """
        raise AttributeError("Cannot set end_point of GmshLine!")

    def switchPoints(self):
        raise AttributeError("Cannot switch points of GmshLine!")

    def translate(self, dx: float, dy: float, dz: float):
        """Translates the line in 3D space.

        Args:
            dx (float): x-coordinate translation in m.
            dy (float): y-coordinate translation in m.
            dz (float): z-coordinate translation in m.
        """
        gmsh.model.occ.translate([(1, self.id)], dx, dy, dz)

    def rotateZ(self, rotationPoint=defaultCenterPoint, angle=0.0):
        """Mit rotateZ() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Z-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point, optional): Rotation center point.
            Defaults to Point("tmpCenterPoint", 0, 0, 0, 1).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:
            from math import pi\n
            L1 = Line(-1, 'l1', P1, P2)\n
            L1.rotateZ(P0, pi)\n
        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(1, self.id)], x, y, z, 0, 0, 1, angle=angle)

    def rotateY(self, rotationPoint: Point, angle: float):
        """
        Mit rotateY() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Y-Achse mit einem definierten Winkel rotiert.

        Args:
           - rotationPoint (Point): rotation center point
           - angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            L1 = Line('l1', P1, P2)\n
            L1.rotateY(P0, pi)\n

        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate((1, self.id), x, y, z, 0, 1, 0, angle=angle)

    def rotateX(self, rotationPoint: Point, angle):
        """
        Mit rotateX() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        X-Achse mit einem definierten Winkel rotiert.

        Args:
           - rotationPoint (Point): rotation center point
           - angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            L1 = Line('l1', P1, P2)\n
            L1.rotateX(P0, pi)\n

        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate((1, self.id), x, y, z, 1, 0, 0, angle=angle)

    def duplicate(self, name="") -> "GmshLine":
        """Create a copy of the line.

        Args:
            name (str, optional): Name of duplicate. Defaults to "".

        Returns:

            GmshLine: A copy of the line.

        Example:
            from pyemmo.script.gmsh.gmsh_line import GmshLine\n
            L1 = GmshLine(-1, 'L1', P1, P2)\n
            L2 = L1.duplicate("new name")\n
        """

        dim_tags: list[DimTag] = gmsh.model.occ.copy([(1, self.id)])
        if len(dim_tags) != 1:
            raise RuntimeError("Error while duplicating line!")
        new_line = GmshLine(tag=dim_tags[0][1])
        # set new line name
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                new_line.name = f"{parentName}_dup"
            else:
                new_line.name = parentName
        return new_line

    def combine(self, line: "GmshLine", touchPoint=None) -> "GmshLine":
        """Combine two lines to one.

        Args:
            line (GmshLine): Line to combine with.
            name (str, optional): Name of new line. Defaults to "".
            touchPoint (GmshPoint, optional): Unused. Defaults to None.

        Returns:
            GmshLine: Combined line.

        Example:
            from pyemmo.script.gmsh.gmsh_line import GmshLine\n
            L1 = GmshLine(-1, 'L1', P1, P2)\n
            L2 = GmshLine(-1, 'L2', P2, P3)\n
            L3 = L1.combine(L2, "L3")\n
        """
        out_dim_tags, out_dim_tags_map = gmsh.model.occ.fuse(
            [(1, self.id)], [(1, line.id)]
        )
        assert len(out_dim_tags) == 1, "Error while combining lines!"
        new_line = GmshLine(tag=out_dim_tags[0][1])
        return new_line
