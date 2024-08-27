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
import gmsh

from ..geometry.line import Line
from .gmsh_point import GmshPoint


class GmshLine(Line):
    """
    Represents a line in 3D space defined by a start and end point, with a unique
    identifier (tag), a name, and a type. The start and end points are instances of
    GmshPoint.

    Attributes:
        tag (int): The unique identifier for the line.
        start_point (GmshPoint): The starting point of the line.
        end_point (GmshPoint): The ending point of the line.
        name (str): The name of the line.
        type (str): The type of the line (e.g., "Line", "Circle").
    """

    def __init__(
        self,
        tag: int,
        start_point: GmshPoint,
        end_point: GmshPoint,
        name: str = "",
    ):
        """
        Constructor for the GmshLine class.

        Args:
            tag (int): The unique identifier for the line.
            start_point (GmshPoint): The starting point of the line.
            end_point (GmshPoint): The ending point of the line.
            name (str, optional): The name of the line. Defaults to an empty string.
            line_type (str, optional): The type of the line. Defaults to "straight".
        """
        self.tag = tag
        self.start_point = start_point
        self.end_point = end_point
        if not name:
            name = gmsh.model.get_entity_name(1, tag)
        self.name = name
        self.type = gmsh.model.get_type(1, tag)

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

    @property
    def name(self) -> str:
        """
        Getter for the name property.

        Returns:
            str: The name of the line.
        """
        return self._name

    @name.setter
    def name(self, new_name: str):
        """
        Setter for the name property.

        Args:
            new_name (str): The new name of the line.
        """
        self._name = new_name

    @property
    def type(self) -> str:
        """
        Getter for the type property.

        Returns:
            str: The type of the line.
        """
        return self._type

    @type.setter
    def type(self, new_type: str):
        """
        Setter for the type property.

        Args:
            new_type (str): The new type of the line.
        """
        self._type = new_type

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
