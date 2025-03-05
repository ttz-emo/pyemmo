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
from abc import ABC, abstractmethod
from typing import Literal

import gmsh


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
        gmsh.model.setEntityName(1, self.id, new_name)
        self._name = new_name
