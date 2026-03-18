#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied
# Sciences Wuerzburg-Schweinfurt.
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
""""""
from __future__ import annotations

from math import atan2, cos, degrees, sin
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from numpy import array, array_equal, cross, pi, vdot
from numpy.linalg import norm

from ...definitions import DEFAULT_GEO_TOL, POINT_COLOR
from .transformable import Transformable

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from .line import Line


class Point(Transformable):
    """
    Simple point with cartesian coordinates.

    Example:

        >>> from pyemmo.script.geometry.point import Point
        >>> P1 = Point(name = 'P1', x = 0.0, y = 1.0, z = 0.0)
    """

    def __init__(self, name: str, x: float, y: float, z: float):
        """Init point with name and coordinates.

        Args:
            name (str): Name of Point
            x (float): x-Coordinate
            y (float): y-Coordinate
            z (float): z-Coordinate
        """
        self.name = name
        self.coordinate = (x, y, z)

    def __eq__(self, comp_point: Point) -> bool:
        """Overload the "==" operator to compare if points are equal in a given
        tolerance"""
        if not isinstance(comp_point, Point):
            raise ValueError(
                "Point can only be compared with another Point! "
                f"But got: {type(comp_point)=}"
            )
        if not self.isEqual(comp_point):
            # checks coordinates within tolerance
            return False
        if self.name != comp_point.name:
            return False
        return True

    def __str__(self) -> str:
        msg = f"Point '{self.name}' with coorinates {self.coordinate}"
        return msg

    @property
    def x(self) -> float:
        """
        Getter for the x coordinate.

        Returns:
            float: x coordinate of the point.
        """
        return self._x

    @x.setter
    def x(self, new_x: float):
        """
        Setter for the x coordinate.

        Args:
            new_x (float): New x coordinate value to set.
        """
        if not isinstance(new_x, (int, float)):
            raise ValueError("Point coordinate values must be int or float!")
        self._x = new_x

    @property
    def y(self) -> float:
        """
        Getter for the y coordinate.

        Returns:
            float: y coordinate of the point.
        """
        return self._y

    @y.setter
    def y(self, new_y: float):
        """
        Setter for the y coordinate.

        Args:
            new_y (float): New y coordinate value to set.
        """
        if not isinstance(new_y, (int, float)):
            raise ValueError("Point coordinate values must be int or float!")
        self._y = new_y

    @property
    def z(self) -> float:
        """
        Getter for the z coordinate.

        Returns:
            float: z coordinate of the point.
        """
        return self._z

    @z.setter
    def z(self, new_z: float):
        """
        Setter for the z coordinate.

        Args:
            new_z (float): New z coordinate value to set.
        """
        if not isinstance(new_z, (int, float)):
            raise ValueError("Point coordinate values must be int or float!")
        self._z = new_z

    @property
    def coordinate(self) -> tuple[float, float, float]:
        """Returns the coordinates of the point as tuple.

        Returns:
            Tuple[float, float, float]: x,y and z-coordinates
        """
        return (self.x, self.y, self.z)

    @coordinate.setter
    def coordinate(self, coordinate: tuple[float, float, float]):
        """Setter of coordinates by tuple.

        Args:
            coordinate (Tuple[float, float, float]): New point coordinates.
        """
        if len(coordinate) != 3:
            raise ValueError("Number of point cooridinates must be 3!")
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = coordinate[2]

    # ------ methods ------

    def isEqual(self, comp_point: Point, tol=DEFAULT_GEO_TOL):
        """
        isEqual checks if another points coordinates are equal with a given tolerance
        (default < 1e-7)
        """
        return all(np.isclose(self.coordinate, comp_point.coordinate, atol=tol))

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """Linear translation of the point by dx, dy and dz.

        Args:
            dx (float): x offset
            dy (float): y offset
            dz (float): z offset
        """
        self._x = self._x + dx
        self._y = self._y + dy
        self._z = self._z + dz

    def rotateZ(self, rotationPoint: Point, angle: float):
        """rotate a point around a rotation point and the Z-axis by angle.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.
        """
        # durch Verschiebung Rotation im Ursprung!
        x, y, _ = rotationPoint.coordinate
        self.translate(-x, -y, 0)
        oldx = self._x
        oldy = self._y
        self._x = cos(angle) * oldx - sin(angle) * oldy
        self._y = sin(angle) * oldx + cos(angle) * oldy
        self.translate(x, y, 0)

    def rotateX(self, rotationPoint: Point, angle: float):
        """Rotation around x-axis by angle in radians.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.
        """
        # durch Verschiebung Rotation im Ursprung!
        rotPointCoords = rotationPoint.coordinate
        self.translate(-rotPointCoords[0], -rotPointCoords[1], -rotPointCoords[2])
        oldy = self._y
        oldz = self._z
        self._y = cos(angle) * oldy - sin(angle) * oldz
        self._z = sin(angle) * oldy + cos(angle) * oldz
        self.translate(rotPointCoords[0], rotPointCoords[1], rotPointCoords[2])

    def rotateY(self, rotationPoint: Point, angle: float):
        """Rotation around y-axis by angle in radians

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.

        """
        # durch Verschiebung Rotation im Ursprung!
        rotPointCoords = rotationPoint.coordinate
        self.translate(-rotPointCoords[0], -rotPointCoords[1], -rotPointCoords[2])
        oldx = self._x
        oldz = self._z
        self._x = cos(angle) * oldx + sin(angle) * oldz
        self._z = -sin(angle) * oldx + cos(angle) * oldz
        self.translate(rotPointCoords[0], rotPointCoords[1], rotPointCoords[2])

    def duplicate(self, name="") -> Point:
        """Create a copy of the point.

        Args:
            name (str, optional): Name of new Point. Defaults to original point name +
                "_dup".

        Returns:
            Point: Duplicate of point.
        """
        x, y, z = self.coordinate
        dupPoint = Point(name, x, y, z)
        if not name:
            parentName = self.name
            if "_dup" not in parentName:
                # if Point was not duplicated before
                dupPoint.name = parentName + "_dup"
            else:
                # otherwise set point name to P_"newPointID"
                dupPoint.name = parentName
        return dupPoint

    def mirror(
        self,
        planePoint: Point,
        planeVector1: Line,
        planeVector2: Line,
        name: str = None,
    ) -> Point:
        """Mirror a circle arc by a plane.

        Args:
            planePoint (Point): Start point of the plane
            planeVector1 (Line): First plane vector.
            planeVector2 (Line): Second plane vector.
            name (str, optional): New name of the arc. Defaults to "".

        Returns:
            Point or None: Mirrored point or None if no mirror plane could be created
            (plane vetors parallel)

        Example:

            >>> P0 = Point('P0', 0, 0, 0)
            >>> Py = Point('Py', 0, 1, 0)
            >>> Pz = Point('Pz', 0, 0, 1)
            >>> yAxis = Line(P0, Py)
            >>> zAxis = Line(P0, Pz)
            >>> P1 = Point('P1', 1, 0, 0)
            >>> P2 = P1.mirror(P0, yAxis, zAxis)
        """
        # 1. Normalenvektor der Ebene E bestimmen (Ebene aus den beiden Inputvektoren und Aufpunkt)
        # 2. Ebenengleichung in Koordinatenform aufstellen: ax1 + bx2 = c
        # 3. Eine Normale h, die durch die Ebene und den Punkt P geht aufstellen
        # 4. Schnittpunkt S von E und H betimmen
        # 5. Einen Vektor zwischen P und S aufstellen
        # 6. Spiegelpunkt bestimmen -> S + PS

        # 1) Normal vector on plane given by V1 and V2
        pV1startPoint = array(planeVector1.start_point.coordinate)
        pV1endPoint = array(planeVector1.end_point.coordinate)
        pV2startPoint = array(planeVector2.start_point.coordinate)
        pV2endPoint = array(planeVector2.end_point.coordinate)
        normalVec = cross(pV1endPoint - pV1startPoint, pV2endPoint - pV2startPoint)

        if array_equal(normalVec, [0, 0, 0]):
            # Plane_Vector1 parallel zu Plane_Vector2
            print("Error: Ebene nicht vorhanden!")
            return None

        # 2) equation for plane
        # nE[0] * x1 + nE[1] * x2 + nE[2] * x3 =
        # = Plane_Point.x * nE[0] + Plane_Point.y * nE[1] + Plane_Point.z * nE[2]
        # determine the right side of equation:

        Constant = vdot(planePoint.coordinate, normalVec)

        # 3) normal vector on plane through point to mirror
        # h = (Point.x + lambda * nE[0])
        #     (Point.y + lambda * nE[1])
        #     (Point.z + lambda * nE[2])

        # 4) projection of point on plane -> intersectionPoint
        selfVec = array(self.coordinate)
        lambda1 = (Constant - (vdot(normalVec, selfVec))) / (norm(pow(normalVec, 2), 1))
        # determine intersection by putting lambda in equation of h
        intersectionPoint = selfVec + lambda1 * normalVec

        # 5) Vector from point to intersection point on plane
        vecPtoS = intersectionPoint - selfVec

        # 6) Mirror point is intersection plus that vector
        mirPoint = intersectionPoint + vecPtoS

        R_Point = Point(self.name, mirPoint[0], mirPoint[1], mirPoint[2])
        if not name:
            R_Point.name = f"mirrored point {self.name}"
        else:
            R_Point.name = name

        return R_Point

    def getAngleToX(
        self,
        flag_deg=False,
        CenterPoint: tuple[float, float, float] | Point = (
            0.0,
            0.0,
            0.0,
        ),
    ) -> float:
        """get the angle of a point to the horizontal axis of its center point

        Args:
            flag_deg (bool, optional): return the angle in degrees. Defaults to False.
            CenterPoint (Tuple or Point, optional): Center point of the rotational axis.
                Defaults to (0,0,0).

        Returns:
            float: angle to the horizontal axis of the center point (in 'radians' if
                flag_deg is not True)
        """
        if isinstance(CenterPoint, tuple):
            if len(CenterPoint) == 3:
                cCoords = CenterPoint
            else:
                raise ValueError(
                    "CenterPoint must be a tuple with 3 coordinates or class Point!"
                )
        else:
            try:
                cCoords = CenterPoint.coordinate
            except AttributeError as exce:
                raise ValueError(
                    "CenterPoint was not class Point or array of coordinates!"
                ) from exce
            except Exception as exce:
                raise exce
        x, y, _ = self.coordinate
        x = x - cCoords[0]
        y = y - cCoords[1]
        # dupPoint = self.duplicate()
        # # translate the point so that the rotation center is at origin
        # if dupPoint.translate(-cCoords[0], -cCoords[1], -cCoords[2]):
        #     x, y, _ = dupPoint.coordinate
        # else:
        #     raise AttributeError("Translation failed")
        angle = atan2(y, x)
        # fix bug when angle is close to 0 but numerically not.
        if abs(angle) < DEFAULT_GEO_TOL:
            angle = 0.0
        if flag_deg:
            angle = degrees(angle)
            # conversion from -180~180 to 0~360
            return angle if angle >= 0 else angle + 360
        # conversion from -pi~pi to 0~2*pi
        return angle if angle >= 0 else angle + 2 * pi

    def calcDist(self, xyz=(0, 0, 0)) -> float:
        """calculate the distance between the point and the coordinates xyz by the
        Euclidean norm.

        Args:
            xyz (tuple, optional): Coordinates of distance to calculate. Defaults to
            origin (0, 0, 0).

        Returns:
            float: distance in meter.
        """
        StartPoint = array(self.coordinate)
        EndPoint = array(xyz)
        return norm(StartPoint - EndPoint)

    @property
    def radius(self) -> float:
        """get the radius (equals to the distance to the center point)

        Returns:
            float: distance to center point (radius)
        """
        return self.calcDist()

    def plot(
        self,
        fig: Figure = None,
        marker="o",
        markersize=1.0,
        color=POINT_COLOR,
        tag=False,
    ):
        """Point plot

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            marker (str, optional): Defaults to "o".
            markersize (float, optional): Defaults to 1.0.
            color (list, optional): Defaults to DEFAULT_POINT_COLOR.
            tag (bool): Flag to print point id and name like "P ("`P_Name`")"
        """
        coords = self.coordinate
        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect("equal", adjustable="box")
            fig.set_dpi(300)
        else:
            ax = fig.axes[0]
        ax.plot(
            coords[0],
            coords[1],
            marker=marker,
            markersize=markersize,
            color=color,
        )
        if tag:
            ax.annotate(
                f"""P ("{self.name}")""",
                (coords[0], coords[1]),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
