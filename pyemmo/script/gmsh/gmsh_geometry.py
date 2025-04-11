#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
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
"""Module gmsh_geometry.py for the abstract class GmshGeometry."""
import numbers
from abc import ABC, abstractmethod
from typing import Literal

import gmsh

from ..geometry import defaultCenterPoint
from ..geometry.point import Point
from . import DimTag


class GmshGeometry(ABC):
    """Abstract class GmshGeometry for geometry entities in Gmsh.
    This class implements all common properties of a geometry entity in Gmsh. These are:
    -   id: The unique ID of the geometry entity in Gmsh.
    -   name:  The name of the geometry entity in Gmsh.
    -   dim: The dimension of the geometry entity in Gmsh.

    This class implements the getter and setter methods for name and id, aswell as the
    abstract property dim for the geometric dimension.
    """

    @property
    @abstractmethod
    def dim(self) -> Literal[0, 1, 2, 3]:
        """Dimension of the Geometry in Gmsh
        -   0: Poin
        -   1: Line, CircleArc
        -   2: Surface
        -   3: Volume
        """

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """Property id of geo classes"""
        return self._id

    @id.setter
    def id(self, new_id) -> None:
        """Setter for ID.

        This only resets the id to a new id (if possible). The private attribute _id is
        only set once at initialization.
        """
        if not isinstance(new_id, int):
            raise TypeError(f"ID must be an integer, but is {type(new_id)}")
        self._reset_id(new_id)

    def _reset_id(self, new_id) -> None:
        """Reset the ID of the geometry object"""
        gmsh.model.occ.synchronize()
        # check that given tag does not exist in gmsh model
        if (1, new_id) in gmsh.model.get_entities(1):
            raise RuntimeError(f"Given line tag={new_id} allready exists in gmsh!")
        gmsh.model.set_tag(self.dim, self.id, new_id)  # set new tag
        self._id = new_id  # update id

    @property
    def name(self) -> str:
        """
        Getter for the name property.

        Returns:
            str: The name of the line.
        """
        gmsh.model.occ.synchronize()
        return gmsh.model.getEntityName(self.dim, self.id)

    @name.setter
    def name(self, new_name: str):
        """
        Setter for the name property.

        Args:
            new_name (str): The new name to set.
        """
        gmsh.model.occ.synchronize()
        gmsh.model.setEntityName(self.dim, self.id, new_name)
        self._name = new_name

    def translate(self, dx, dy, dz):
        """
        Translates the geometric entity by the given offsets in the x, y, and z
        directions.

        Parameters:
        dx (float): The offset in the x direction.
        dy (float): The offset in the y direction.
        dz (float): The offset in the z direction.
        """
        if not all(isinstance(shift, numbers.Number) for shift in (dx, dy, dz)):
            raise TypeError("Translation inputs dx,dy,dz must be a number!")
        gmsh.model.occ.translate([(self.dim, self.id)], dx, dy, dz)

    def rotateZ(self, rotationPoint: Point = defaultCenterPoint, angle=0.0):
        """Mit rotateZ() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Z-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point, optional): Rotation center point.
            Defaults to gobal center point at (0,0,0).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:
            from math import pi\n
            L1 = GmshLine(-1, 'l1', P1, P2)\n
            L1.rotateZ(P0, pi)\n
        """
        if not isinstance(rotationPoint, Point):
            # pylint: disable=locally-disabled, consider-using-f-string
            raise TypeError(
                "Rotation center point must be of type point but is %s!"
                % type(rotationPoint),
            )
        if not isinstance(angle, numbers.Number):
            raise TypeError("Rotation angle must be a number!")
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(self.dim, self.id)], x, y, z, 0, 0, 1, angle=angle)

    def rotateX(self, rotationPoint: Point = defaultCenterPoint, angle=0.0):
        """Mit rotateX() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        X-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point, optional): Rotation center point.
            Defaults to gobal center point at (0,0,0).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:
            from math import pi\n
            L1 = GmshLine(-1, 'l1', P1, P2)\n
            L1.rotateX(P0, pi)\n
        """
        if not isinstance(rotationPoint, Point):
            # pylint: disable=locally-disabled, consider-using-f-string
            raise TypeError(
                "Rotation center point must be of type point but is %s!"
                % type(rotationPoint),
            )
        if not isinstance(angle, numbers.Number):
            raise TypeError("Rotation angle must be a number!")
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(self.dim, self.id)], x, y, z, 1, 0, 0, angle=angle)

    def rotateY(self, rotationPoint: Point = defaultCenterPoint, angle=0.0):
        """Mit rotateY() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Y-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point, optional): Rotation center point.
            Defaults to gobal center point at (0,0,0).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:
            from math import pi\n
            L1 = GmshLine(-1, 'l1', P1, P2)\n
            L1.rotateX(P0, pi)\n
        """
        if not isinstance(rotationPoint, Point):
            # pylint: disable=locally-disabled, consider-using-f-string
            raise TypeError(
                "Rotation center point must be of type point but is %s!"
                % type(rotationPoint),
            )
        if not isinstance(angle, numbers.Number):
            raise TypeError("Rotation angle must be a number!")
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(self.dim, self.id)], x, y, z, 0, 1, 0, angle=angle)

    def duplicate(self, name=""):
        """Create a copy of the gmsh instance.

        Args:
            name (str, optional): Name of duplicate. Defaults to "".

        Returns:
            GmshObj: A copy of the gmsh class instance.
        """

        dim_tags: list[DimTag] = gmsh.model.occ.copy([(self.dim, self.id)])
        if len(dim_tags) != 1:
            raise RuntimeError(f"Error while duplicating gmsh object ({self})!")
        new_instance = type(self)(tag=dim_tags[0][1], name=name)
        # set new instance name
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                new_instance.name = f"{parentName}_dup"
            else:
                new_instance.name = parentName
        return new_instance

    def combine(self, add_obj):
        """Combine two objects to one using opencascade fuse command.
        The old objects will be removed!

        Args:
            add_obj (Gmsh*): Gmsh class instance.

        Returns:
            Gmsh*: Combined Gmsh class objects.

        Example:
            from pyemmo.script.gmsh.gmsh_line import GmshArc\n
            L1 = GmshArc(-1, 'L1', P1, P2)\n
            L2 = GmshArc(-1, 'L2', P2, P3)\n
            L3 = L1.combine(L2)\n
        """
        assert isinstance(add_obj, type(self))
        out_dim_tags, out_dim_tags_map = gmsh.model.occ.fuse(
            [(self.dim, self.id)], [(add_obj.dim, add_obj.id)]
        )
        assert len(out_dim_tags) == 1, "Error while combining objects!"
        new_obj = type(self)(tag=out_dim_tags[0][1])
        return new_obj
