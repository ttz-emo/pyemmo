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
    >>> p = GmshPoint.from_coordinates(coords=[0.0, 1.0, 2.0])
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
import numbers
from typing import Literal, Tuple, Union

import gmsh
import numpy as np

from ..geometry import defaultCenterPoint
from ..geometry.point import Point
from . import DimTag
from .gmsh_geometry import GmshGeometry


class GmshPoint(GmshGeometry, Point):
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
        TODO: Add more attributes.

    Methods:
        __init__(self, tag: int, coords: np.ndarray):
            Initializes a new GmshPoint with the given tag and coordinates.
        __str__(self) -> str:
            Returns a string representation of the GmshPoint object.
    """

    @property
    def dim(self) -> Literal[0]:
        """Dimension of Point = 0"""
        return 0

    def __init__(self, tag: int = -1, name: str = ""):
        """
        Constructor for GmshPoint class.

        Args:
            tag (int): Tag of the point.
            name (str, optional): Name of the point. Defaults to "".
        """
        if not isinstance(tag, (int, np.integer)):
            raise TypeError("Gmsh tag must be positive integer!")
        # make sure the point with given tag exists in gmsh:
        if (0, tag) not in gmsh.model.occ.getEntities(0):
            raise ValueError(f"Point with given {tag=} does not exist!")
        self._id = tag  # set tag
        # set name in gmsh if not empty
        self.name = name
        # NOTE: There is no need to call the constructor of the Point class here, because
        # all relevant properties are accessed dynamically via the gmsh API.

    def __eq__(self, other):
        if type(self) == type(other):
            if self.id == other.id:
                return True
        return False

    @classmethod
    def from_coordinates(
        cls,
        coords: Union[np.ndarray, list, tuple],
        meshLength: float = 1e-3,
        name: str = "",
    ) -> "GmshPoint":
        """
        Create a GmshPoint instance from given coordinates.
        This method initializes a GmshPoint object using the provided coordinates,
        mesh length, and optional name. It supports both 2D and 3D points.
        Args:
            coords (Union[np.ndarray, list, tuple]): The coordinates of the point.
                Must be a numpy array, list, or tuple. For 2D points, provide
                [x, y]. For 3D points, provide [x, y, z].
            meshLength (float, optional): The mesh size associated with the point.
                Must be a positive number. Defaults to 1e-3.
            name (str, optional): An optional name for the point. Defaults to an
                empty string.
        Returns:
            GmshPoint: An instance of the GmshPoint class.
        Raises:
            TypeError: If `meshLength` is not a number or if `coords` is not a
                numpy array, list, or tuple.
            ValueError: If `meshLength` is less than or equal to 0, or if the
                size of `coords` is not 2 or 3.
        """
        # init with coords
        if not isinstance(meshLength, numbers.Number):
            raise TypeError("meshLength must be a number!")
        if meshLength <= 0:
            raise ValueError("meshLength must be greater than 0!")
        # type cast coords to np.ndarray if necessary
        if not isinstance(coords, np.ndarray):
            if not isinstance(coords, (list, tuple)):
                raise TypeError("coords must be a numpy array, list or tuple!")
            coords = np.array(coords)
        if coords.size == 2:
            # 2D point
            point_tag = gmsh.model.occ.addPoint(coords[0], coords[1], 0.0, meshLength)
        elif coords.size == 3:
            # 3D point
            point_tag = gmsh.model.occ.addPoint(
                coords[0], coords[1], coords[2], meshLength
            )
        else:
            raise ValueError(f"Wrong GmshPoint coordinates {coords=}!")
        return cls(tag=point_tag, name=name)

    @property
    def meshLength(self) -> float:
        """Get mesh length of point.

        Returns:
            float: mesh length in meter
        """
        try:
            # try to get the mesh size
            return gmsh.model.mesh.getSizes([(0, self.id)])[0]
        except Exception as exce:
            if "does not exist" in str(exce):
                gmsh.model.occ.synchronize()
                return gmsh.model.mesh.getSizes([(0, self.id)])[0]
            raise exce

    @meshLength.setter
    def meshLength(self, meshLength: float):
        """Set mesh length of point.

        Args:
            meshLength (float): mesh length
        """
        # TODO: In a simple test script this worked for a OCC Point. But in the api
        # this operation seems to be only valid for a occ point until we call sync().
        # Otherwise sync() resets the mesh size to its initial value...
        if isinstance(meshLength, numbers.Number):
            try:
                gmsh.model.occ.mesh.setSize([(0, self.id)], meshLength)
            except Exception as exce:
                if "does not exist" in str(exce):
                    gmsh.model.occ.synchronize()
                    gmsh.model.occ.mesh.setSize([(0, self.id)], meshLength)
                raise exce
            # We need to call synchronize() to make sure the mesh size is set internally
            # in gmsh aswell so it can be used in the getter!
            gmsh.model.occ.synchronize()
        else:
            raise ValueError("meshLength must be a number!")

    @property
    def coordinate(self) -> Tuple[float, float, float]:
        """
        Getter for the coordinate property.

        Returns:
            Tuple[float, float, float]: Tuple containing the x, y, and z coordinates of
                the point.
        """
        try:
            coords = gmsh.model.get_value(0, self.id, [])
        except Exception as e:
            if "does not exist" in str(e):
                # if point does not exist, synchronize and try again
                gmsh.model.occ.synchronize()
                coords = gmsh.model.get_value(0, self.id, [])

        return (coords[0], coords[1], coords[2])

    @coordinate.setter
    def coordinate(self, coords: Tuple[float, float, float]):
        raise AttributeError(
            "You can't set coordinates of a GmshPoint! Use the translate method!"
        )

    @property
    def x(self) -> float:
        """
        Getter for the x coordinate.

        Returns:
            float: x coordinate of the point.
        """
        return self.coordinate[0]

    @x.setter
    def x(self, new_x: float):
        raise AttributeError("You can't set the coordinates of a GmshPoint!")

    @property
    def y(self) -> float:
        """
        Getter for the y coordinate.

        Returns:
            float: y coordinate of the point.
        """
        return self.coordinate[1]

    @y.setter
    def y(self, new_y: float):
        raise AttributeError("You can't set the coordinates of a GmshPoint!")

    @property
    def z(self) -> float:
        """
        Getter for the z coordinate.

        Returns:
            float: z coordinate of the point.
        """
        return self.coordinate[2]

    @z.setter
    def z(self, new_z: float):
        raise AttributeError("You can't set the coordinates of a GmshPoint!")

    def __str__(self) -> str:
        """
        Returns a string representation of the GmshPoint.

        Returns:
            str: String containing the tag and coordinates of the point.
        """
        return f"GmshPoint(tag={self.id}, coords=({self.x}, {self.y}, {self.z}))"

    def translate(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0):
        """Translate the point by the given displacements.

        Args:
            dx (float): Displacement in the x-direction. Defaults to 0.0.
            dy (float): Displacement in the y-direction. Defaults to 0.0.
            dz (float): Displacement in the z-direction. Defaults to 0.0.
        """
        gmsh.model.occ.translate([(0, self.id)], dx, dy, dz)

    def rotateZ(self, rotationPoint: "Point" = defaultCenterPoint, angle: float = 0.0):
        """Rotate the point around a rotation point and the Z-axis by a given angle.

        Args:
            rotationPoint (Point): Rotation point.
            angle (float): Rotation angle in radians.
        """
        x, y, z = rotationPoint.coordinate  # get rotation point coordinates
        # rotate point in gmsh
        gmsh.model.occ.rotate([(0, self.id)], x, y, z, 0, 0, 1, angle)

    def duplicate(self, name="") -> "GmshPoint":
        dimTags: list[DimTag] = gmsh.model.occ.copy([(0, self.id)])
        assert len(dimTags) == 1, "Error while duplicating point!"
        new_point = GmshPoint(tag=dimTags[0][1])
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                # if Point was not duplicated before
                new_point.name = parentName + "_dup"
            else:
                # otherwise set point name to P_"newPointID"
                new_point.name = parentName
        else:
            new_point.name = name
        return new_point

    def mirror(
        self,
        planePoint: "Point",
        planeVector1: "Line",
        planeVector2: "Line",
        name: str = None,
    ) -> "Point":
        """TODO"""
        raise NotImplementedError("mirror is not implemented for GmshPoint!")
        # gmsh.model.occ.mirror(...)


GmshPoint.rotateX = GmshGeometry.rotateX
GmshPoint.rotateY = GmshGeometry.rotateY
