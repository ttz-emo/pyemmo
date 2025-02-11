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
Module: gmsh_point

This module defines the GmshPoint class, which represents a point in 3D space with a unique
identifier (tag) used in the context of Gmsh, a mesh generation software.

Dependencies:
    - numpy: Used for handling the coordinate data as a NumPy array.
    - gmsh: Assumed to be used elsewhere in the application for Gmsh-related operations.
    - logging: Included for potential logging requirements.

Classes:
    - GmshPoint: Represents a 3D point with a unique tag and coordinates.

Example:
    Create a GmshPoint instance and print its details:

    >>> import numpy as np
    >>> p = GmshPoint(tag=1, coords=np.array([0.0, 1.0, 2.0]))
    >>> print(p)
    GmshPoint(tag=1, coords=(0.0, 1.0, 2.0))

Usage:
    The GmshPoint class can be used as part of a larger system where points in 3D space need
    to be managed, tagged, and manipulated. This is particularly useful in mesh generation
    and geometric modeling tasks.

Author:
    Max Schuler

Note:
    This docstring was created by ChatGPT.
"""

import gmsh
import numpy as np

from ..geometry.point import Point


class GmshPoint(Point):
    """
    Represents a point in 3D space with a unique identifier (tag) in the context of
    Gmsh.

    This class encapsulates a point in a 3D geometric space, storing its coordinates
    (x, y, z) and a unique tag. The tag can be used to reference the point in Gmsh
    operations. The coordinates are stored as float values, and the class provides
    properties to access and modify them. Additionally, the class overrides the
    `__str__` method to provide a string representation of the point, including its
    tag and coordinates.

    Attributes:
        tag (int): The unique identifier for the point.
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        z (float): The z-coordinate of the point.

    Methods:
        __init__(self, tag: int, coords: np.ndarray):
            Initializes a new GmshPoint with the given tag and coordinates.
        __str__(self) -> str:
            Returns a string representation of the GmshPoint object.
    """

    def __init__(self, tag: int, coords: np.ndarray = np.empty(0)):
        """
        Constructor for GmshPoint class.

        Args:
            tag (int): Tag of the point.
            coords (np.ndarray, optional): Coordinates of the point as a NumPy array
                with shape (3,) or empty. When empty, try to find the point with its tag
                in Gmsh and get the coordinates from there.
        """
        self.tag = tag
        self.name = gmsh.model.get_entity_name(0, tag)
        if coords.size == 0:
            # try to get coords from gmsh:
            coords = gmsh.model.get_value(0, tag, [])  # This raises an Exception if
            # point does not exist!
        if coords.size != 3:
            raise ValueError(f"Wrong GmshPoint coordinates {coords=}!")
        self.coordinate = coords
        self._meshLength = gmsh.model.mesh.get_sizes([(0, tag)])[0]
        self._todesmerker = False

    @property
    def tag(self) -> int:
        """
        Getter for the tag property.

        Returns:
            int: Tag of the point.
        """
        return self._tag

    @tag.setter
    def tag(self, new_tag: int):
        """
        Setter for the tag property.

        Args:
            new_tag (int): New tag value to set.
        """
        if (0, new_tag) not in gmsh.model.get_entities(0):
            raise RuntimeError(
                "Given point tag is not in gmsh model! "
                "Did you forget to call gmsh.model.occ.synchronize()?"
            )
        self._id = new_tag
        self._tag = new_tag

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshPoint.

        Returns:
            str: String containing the tag and coordinates of the point.
        """
        return f"GmshPoint(tag={self.tag}, coords=({self.x}, {self.y}, {self.z}))"
