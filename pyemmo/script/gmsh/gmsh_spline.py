#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of
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
This module includes the :class:`GmshSpline` class, which represents a curved segment in 3D space.
The class allows for the definition of a line with a unique tag, start and end points,
a name, and a type.
"""

from __future__ import annotations

from typing import Literal

import gmsh
import numpy as np

from ..geometry.spline import Spline
from . import DimTag
from .gmsh_geometry import GmshGeometry
from .gmsh_line import GmshLine
from .gmsh_point import GmshPoint


class GmshSpline(GmshLine, Spline):
    """GmshSpline represents a spline type curve through the gmsh api."""

    def __init__(
        self,
        tag: int,
        name: str = "",
    ):
        """
        Constructor for the GmshSpline class. Specifiy a **existing** gmsh line tag with
        ``tag``: The init method will find the spline properties from gmsh.

        Optionally you can create a new spline by using the
        `from_points() <pyemmo.script.gmsh.gmsh_spline.GmshSpline.from_points>`_ method
        by specifying the start, end and control points of the spline.

        Args:
            tag (int): The unique identifier for the spline.
            name (str, optional): The name of the spline. Defaults to an empty string.
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
        self._id = tag  # set tag
        self.name = name

    def __eq__(self, other):
        if type(self) == type(other):
            if self.id == other.id:
                return True
        return False

    @classmethod
    def from_points(
        cls, points: list[GmshPoint], name: str = "", spline_type: Literal[0, 1, 2] = 1
    ):
        """Create a GmshSpline instance from multiple GmshPoint objects representing the
        start point, control_points and end point of the spline in `points`.

        Args:
            points (List[GmshPoint]): start, control and end point(s) of the spline.
            name (str): The name to assign to the spline.
            spline_type (Literal[0,1,2]): The type of the spline (0=BSpline, 1=Bezier,
                2=Simple Spline). Defaults to 1 (Bezier).

        Returns:
            GmshSpline: An instance of the GmshSpline class.

        Raises:
            ValueError: If any of the provided points are not of type GmshPoint.
        """
        # make sure all points are of type GmshPoint
        if not all(isinstance(p, GmshPoint) for p in points):
            raise ValueError("All points must be of type GmshPoint for GmshSpline!")
        point_tags = [p.id for p in points]
        # create spline in gmsh
        if spline_type == 0:
            spline_id = gmsh.model.occ.addBSpline(point_tags)
        elif spline_type == 1:
            spline_id = gmsh.model.occ.addBezier(point_tags)
        elif spline_type == 2:
            spline_id = gmsh.model.occ.addSpline(point_tags)
        else:
            raise ValueError(f"Invalid spline type {spline_type}!")
        # return class constructor with the new spline id and name
        return cls(spline_id, name)

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshSpline.

        Returns:
            str: A string containing the tag, name, type, and the start and end points
            of the line.
        """
        point_strings = (str(p) for p in self.points)
        return (
            f"GmshSpline(name={self.name}, id={self.id}, points="
            + ",".join(point_strings)
            + ")"
        )

    @property
    def spline_type(self) -> Literal["BSpline", "Bezier", "Spline"]:
        """Return the Gmsh spline type.
        Since we use open cascade (OCC) we can only generate C2 BSplines, which have
        index 1 according to
        `Spline.spline_type <pyemmo.script.geometry.spline.Spline.spline_type>`_

        Returns:
            Literal: 1 for C2 BSpline
        """
        # "BSpline", "Bezier", "Spline"
        spline_type: str = gmsh.model.getType(1, self.id)
        if spline_type == "BSpline":
            return 1
        elif spline_type == "Bezier":
            return 0
        elif spline_type == "Spline":
            return 2
        raise ValueError(
            f"Could not convert Gmsh spline type '{spline_type}' of spline {self} to integer!"
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
        raise ValueError("Can not change start point of GmshSpline!")

    @property
    def end_point(self) -> GmshPoint:
        """
        Getter for the end_point property.

        Returns:
            GmshPoint: The ending point of the line.
        """
        return self.points[-1]

    @end_point.setter
    def end_point(self, new_end_point: GmshPoint):
        """
        Setter for the end_point property.

        Args:
            new_end_point (GmshPoint): The new ending point to set.
        """
        raise ValueError("Can not change end point of GmshSpline!")

    @property
    def control_points(self) -> list[GmshPoint]:
        """TODO

        Returns:
            list[GmshPoint]: _description_
        """
        return self.points[1:-1]

    @property
    def length(self) -> float:
        """Length of gmsh line by gmsh.model.occ.getMass(dim, tag)"""
        return gmsh.model.occ.getMass(self.dim, self.id)

    def duplicate(self, name="") -> GmshSpline:
        """Create a copy of the spline.

        Args:
            name (str, optional): Name of duplicate. Defaults to "".

        Returns:

            GmshLine: A copy of the spline.

        Example:
            >>> from pyemmo.script.gmsh.gmsh_line import GmshLine\n
            >>> L1 = GmshSpline.from_points([P1, P2, P3],'Line 1')\n
            >>> L2 = L1.duplicate("new name")\n
        """

        dim_tags: list[DimTag] = gmsh.model.occ.copy([(1, self.id)])
        if len(dim_tags) != 1:
            raise RuntimeError("Error while duplicating spline!")
        new_spline = GmshSpline(tag=dim_tags[0][1])
        # set new line name
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                new_spline.name = f"{parentName}_dup"
            else:
                new_spline.name = parentName
        return new_spline


GmshSpline.combine = GmshGeometry.combine
GmshSpline.rotateX = GmshGeometry.rotateX
GmshSpline.rotateY = GmshGeometry.rotateY
GmshSpline.rotateZ = GmshGeometry.rotateZ
