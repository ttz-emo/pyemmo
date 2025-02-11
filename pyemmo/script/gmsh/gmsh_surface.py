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
TODO
"""

from typing import Union

import gmsh
import numpy as np

from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from ..geometry.point import Point
from ..geometry.surface import Surface
from .gmsh_arc import GmshArc
from .gmsh_line import GmshLine


class GmshSurface(Surface):
    """
    TODO
    """

    def __init__(
        self,
        tag: int = -1,
        curves: list[Union[Line, CircleArc]] = [],
        name: str = "",
    ):
        """ """
        if tag >= 0 and curves == []:
            self._init_with_tag(tag, name)
        elif tag < 0 and all(filter(lambda l: isinstance(l, Line), curves)):
            # no tag given, but all three points are of type Point
            super().__init__(name, curves=curves)
            self.tag = self.id
        else:
            raise ValueError(
                "Can not create GmshSurface for input of tag AND line list!"
            )

    def _init_with_tag(self, tag: int, name: str):
        self.tag = tag
        assert (
            gmsh.model.get_type(2, tag) == "Plane"
        ), "Given surface tag for GmshSurface does not yeald to Gmsh Surface instance!"
        self.curve = self.get_lineloop(tag)
        if not name:
            name = gmsh.model.get_entity_name(2, tag)
        self.name = name

    def get_lineloop(self, tag: int) -> list[Union[GmshLine, GmshArc]]:
        """Get the lineloop of the surfacef from the Gmsh model.

        Args:
            tag (int): The tag of the surface in the Gmsh model.

        Raises:
            ValueError: If the line with the given tag is not of type Line or Circle.

        Returns:
            list[Union[GmshLine, GmshArc]]: The list of lines that form the lineloop.
        """
        line_tags = np.abs(np.array(gmsh.model.get_boundary(dimTags=[(2, tag)]))[:, 1])
        curves: list[Union[GmshLine, GmshArc]] = []
        for ltag in line_tags:
            if gmsh.model.getType(1, ltag) == "Line":
                curves.append(GmshLine(tag=ltag))
            elif gmsh.model.getType(1, ltag) == "Circle":
                curves.append(GmshArc(tag=ltag))
            else:
                raise ValueError(f"Line with tag {ltag} is not of type Line or Circle!")
        return curves

    @property
    def tag(self) -> int:
        """
        Getter for the tag property.

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
    def id(self) -> int:
        """
        Getter for the tag property but with name 'id' to be compatible with PyEMMO.

        Returns:
            int: The unique identifier for the line.
        """
        return self._tag

    @id.setter
    def id(self, newID: int) -> None:
        """setter of GmshArc ID

        Args:
            newID (int): New ID of Arc
        """
        if isinstance(newID, int):
            self._tag = newID
        else:
            raise TypeError("Line ID must be an integer!")

    def rotateZ(self, rotationPoint: Point, angle: float):
        """Rotates the surface around the z-axis.

        Args:
            rotationPoint (Point): The point around which the surface should be rotated.
            angle (float): The angle in degrees by which the surface should be rotated.

        example:
            >>> from pyemmo.gmsh import GmshSurface, GmshPoint
            >>> from math import pi
            >>> surface = GmshSurface()
            >>> rotationPoint = GmshPoint()
            >>> surface.rotateZ(rotationPoint, pi/2)
        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(2, self.id)], x, y, z, 0, 0, 1, angle)
        self.curve = self.get_lineloop(self.id)  # reset the line loop
