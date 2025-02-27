#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied
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
"""Module for geometry element Point"""
import logging
from math import atan2, cos, degrees, sin
from typing import TYPE_CHECKING, Tuple, Union

import gmsh

gmsh.initialize()

import matplotlib.pyplot as plt
from numpy import array, array_equal, cross, pi, vdot
from numpy.linalg import norm

from ...definitions import DEFAULT_GEO_TOL, POINT_COLOR
from .transformable import Transformable

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from .line import Line


###
# Eine Instanz der Klasse Point ist ein Punkt im dreidimensionalen Raum.
#
#   Beispiel:
#
#       import pyemmo as pyd
#       P1 = pyd.Point(name = 'P1', x = 0.0, y = 1.0, z = 0.0, meshLength = 0.3)
###
class Point(Transformable):
    """
    Eine Instanz der Klasse Point ist ein Punkt im dreidimensionalen Raum.

    Beispiel:
        import pyemmo as pyd
        P1 = pyd.Point(name = 'P1', x = 0.0, y = 1.0, z = 0.0, meshLength = 0.3)
    """

    # Die statische Variable ID wird durch die Methode getNewID() hochgezählt.
    # Diese Variable wird für die automatische ID-Vergabe der Punkte verwendet!
    pointID = 0

    def __init__(
        self, name: str, x: float, y: float, z: float, meshLength: float, tag: int = -1
    ):
        """Konstruktor der Klasse Point.

        Args:
            name (str): Name of Point
            x (float): x-Coordinate
            y (float): y-Coordinate
            z (float): z-Coordinate
            meshLength (float): Mesh length of point in meter.
            tag (int, optional): ID of point. Defaults to unique point ID (internal
                class variable).
        """
        self.name = name
        self.coordinate = (x, y, z)
        self.meshLength = meshLength

        # set point id
        if tag == -1:
            self.id = self._getNewID()  # no id given
        else:
            self.id = tag  # id given

    # def __eq__(self, x) -> bool:
    #     """Overload the "==" operator to compare if points are equal in a given tolerance"""
    #     if x is None:
    #         return False
    #     tol=1e-7
    #     xP, yP, zP = self.getCoordinate()
    #     xTest, yTest, zTest = x.getCoordinate()
    #     diffX = abs(xTest - xP)
    #     diffY = abs(yTest - yP)
    #     diffZ = abs(zTest - zP)
    #     if diffX < tol and diffY < tol and diffZ < tol:
    #         return True
    #     else:
    #         return False

    # ------ attributes ------

    @classmethod
    def _getNewID(cls) -> int:
        """Wird ein Punkt erzeugt, bekommt er automatisch eine eindeutige ID zugewiesen.
        Mit getNewID() wird eine neue ID erzeugt.

        Returns:
            int: New unique ID for point.
        """
        Point.pointID = Point.pointID + 1
        return Point.pointID

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """get global point ID

        Returns:
            int: ID of point
        """
        return self._id

    @id.setter
    def id(self, newID: int) -> None:
        """setter of point ID

        Args:
            newID (int): New ID of point
        """
        if newID % 1 == 0:
            self._id = int(newID)
        raise ValueError("Point ID must be an integer!")

    @property
    def name(self) -> str:
        """Get name of point.

        Returns:
            str: name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name of point.

        Args:
            name (str): New Point name
        """
        if not isinstance(name, str):
            raise TypeError(f"Name must be string, not {type(name)}")
        self._name = name

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
    def coordinate(self) -> Tuple[float, float, float]:
        """Die Methode getCoordinate() gibt die x- y- und z-Koordinaten eines Punktes zurück.

        Returns:
            Tuple[float, float, float]: x,y and z-coordinates
        """
        return (self.x, self.y, self.z)

    @coordinate.setter
    def coordinate(self, coordinate: Tuple[float, float, float]):
        """Die Methode setCoordinate() setzt die x- y- und z-Koordinaten eines Punktes.

        Args:
            coordinate (Tuple[float, float, float]): New point coordinates.
        """
        if len(coordinate) != 3:
            raise ValueError("Number of point cooridinates must be 3!")
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = coordinate[2]

    @property
    def meshLength(self) -> float:
        """get mesh length of point

        Returns:
            float: mesh length
        """
        return self._meshLength

    @meshLength.setter
    def meshLength(self, meshLength: float):
        """Set mesh length of point.

        Args:
            meshLength (float): mesh length
        """
        if not isinstance(meshLength, (int, float)):
            raise ValueError(
                "Mesh length must be int or float. (Mesh length of Point in meter)"
            )
        self._meshLength = meshLength

    # ------ methods ------

    def isEqual(self, compPoint: "Point", tol=DEFAULT_GEO_TOL):
        """
        isEqual checks if another points coordinates are equal with a given tolerance
        (default < 1e-7)
        """
        originCoords = array(self.coordinate)
        compCoords = array(compPoint.coordinate)

        if norm(originCoords - compCoords) < tol:
            return True
        return False

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """Mit translate() kann ein Punkt linear verschoben werden. Die Inputvariablen dx, dy und dz
        beschreiben die Verschiebungsfaktoren in der x-, y- und z- Richtung.

        Args:
            dx (float): x offset
            dy (float): y offset
            dz (float): z offset
            flag_gmsh (bool): Flag to control if the operation should be run in gmsh
                aswell. Defaults to True.
        """
        self._x = self._x + dx
        self._y = self._y + dy
        self._z = self._z + dz

    def rotateZ(self, rotationPoint: "Point", angle: float):
        """Mit rotateZ() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die Z-Achse mit
        einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.
        """
        # durch Verschiebung Rotation im Ursprung!
        x, y, z = rotationPoint.coordinate
        self.translate(-x, -y, 0)
        oldx = self._x
        oldy = self._y
        self._x = cos(angle) * oldx - sin(angle) * oldy
        self._y = sin(angle) * oldx + cos(angle) * oldy
        self.translate(x, y, 0)

    def rotateX(self, rotationPoint: "Point", angle: float):
        """Mit rotateX() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die X-Achse mit
        einem definierten Winkel rotiert.

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

    def rotateY(self, rotationPoint: "Point", angle: float):
        """Mit rotateY() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die Y-Achse mit
        einem definierten Winkel rotiert.

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

    def duplicate(self, name="") -> "Point":
        """Mit duplicate() wird ein neuer Punkt mit gleichen Koordinaten erzeugt. Dieser Punkt hat
        jedoch eine unterschiedliche ID zum Originalpunkt.

        Args:
            name (str, optional): Name of new Point. Defaults to original point name + "_dup".

        Returns:
            Point: Duplicate of point.
        """
        x, y, z = self.coordinate
        meshLen = self.meshLength
        dupPoint = Point(name, x, y, z, meshLen)
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
        planePoint: "Point",
        planeVector1: "Line",
        planeVector2: "Line",
        name: str = None,
    ) -> "Point":
        """Mit mirror() kann ein Punkt an einer definierten Ebene gespiegelt werden. Ein Bildpunkt
        wird hierbei erzeugt. Die Spiegelebene wird durch einen Aufpunkt (planePoint) und 2 Vektoren
        (planeVector1 und planeVector2) beschrieben.

        Args:
            planePoint (Point)
            planeVector1 (Line)
            planeVector2 (Line)
            name (str, optional): Name of new mirrored point. Defaults to None.

        Returns:
            Point or None: Mirrored point or None if no mirror plane could be created (plane vetors
            parallel)

        Beispiel:
            P0 = Point('P0', 0, 0, 0, 1) \n
            Py = Point('Py', 0, 1, 0, 1) \n
            Pz = Point('Pz', 0, 0, 1, 1) \n
            yAxis = Line(P0, Py) \n
            zAxis = Line(P0, Pz) \n
            P1 = Point('P1', 1, 0, 0, 0.3) \n
            P2 = P1.mirror(P0, yAxis, zAxis) \n
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

        R_Point = Point(
            self.name, mirPoint[0], mirPoint[1], mirPoint[2], self._meshLength
        )
        if not name:
            R_Point.name = "P_" + str(abs(R_Point.id))
        else:
            R_Point.name = name

        return R_Point

    def addToScript(self, script: "Script") -> Union["Point", None]:
        """
        Mit addToScript wird der Punkt zum Skriptobjekt übergeben und in
        gmsh-Syntax übersetzt. Transformationen von Punkten sind nach dem Aufruf
        nicht mehr erlaubt, da die neuen Koordinaten der Punkte nicht mehr erfasst
        werden. Diese Methode sollte stets nur in Kombination mit generateScript
        (Klassenmethode von Script) verwendet werden.

            Input:
                script : Script
            Output:
                None

            Beispiel:
                myScript = Script(...)
                P1.addToScript(myScript)

            Returns:
                _type_: _description_
        """
        if self.isDrawn():
            logging.warn(f"Point '{self.name}' is allready in a script.")
            return None
        return script._addPoint(self)

    def getAngleToX(
        self,
        flag_deg=False,
        CenterPoint: Union[Tuple[float, float, float], "Point"] = (
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
            try:
                cCoords = CenterPoint.coordinate
            except AttributeError:
                ValueError("CenterPoint was not class Point or array of coordinates")
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
        """Mit calcDist() der Abstand zwischen dem Punkt (self) und den Koordinaten xyz
        zurückgegeben (Euklidische Norm).

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
        """get the radius to the center point (0,0,0)

        Returns:
            float: distance to center point (radius)
        """
        return self.calcDist()

    def plot(
        self,
        fig: "Figure" = None,
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
            tag (bool): Flag to print point id and name like "P `P_ID` ("`P_Name`")"
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
                f"""P {self.id} ("{self.name}")""",
                (coords[0], coords[1]),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
