#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
from random import random
from typing import List, Literal

try:
    from .point import Point
    from .line import Line
except ImportError:
    from pyemmo.script.geometry.point import Point
    from pyemmo.script.geometry.line import Line

###
# Eine Instanz der Unterklasse Spilne ist ein Polynomzug, zwischen beliebig vielen Punkten (Objekte der Klasse Point) im dreidimensionalen Raum.
# Spline-Befehl aus Gmsh erzeugt einie Linie, die durch all gegebenen Punkte laufen.
#
#   Beispiel:
#
#       import pyemmo as pyd
#       P0 = pyd.Point('p0', 0, 0, 0, 0.3)
#       P1 = pyd.Point('p1', 1, 0, 0, 0.3)
#       P2 = pyd.Point('p2', 1, 1, 0, 0.3)
#       P3 = pyd.Point('p3', 0, 1, 0, 0.3)
#       SP1 = pyd.Spline('sp1', P0, P3, [P1, P2])
#
###


class Spline(Line):
    def __init__(
        self,
        name: str,
        startPoint: Point,
        endPoint: Point,
        controlPoints: List[Point],
        SplineType: Literal[0, 1, 2] = 0,
    ):
        """Konstruktor der Klasse Spline

        Args:
            name (str): Name of the Spline
            p1 (Point): Startpoint
            p2 (Point): Endpoint
            controlPoints (List[Point]): List of controll points
            SplineType (Literal[0, 1, 2], optional): There are 3 different types of Splines
             that can be generated with Gmsh. Defaults to 0 (Spline):

                0 : Catmull-Rom Spline (Build-in Kernel) or C2 BSpline (OpenCASCADE Kernel)
                1 : Bezierkurve
                2 : Basis-Spline

        """
        super().__init__(name=name, startPoint=startPoint, endPoint=endPoint)
        ###Zwischenpunkte vom Polynomzug in der richtigen durchzulaufenden Reihenfolge.
        self.controlPoints = controlPoints
        # 0: Catmull-Rom Spline, 1: Bezierkurve, 2: Basis-Spline
        self._splineType = SplineType

    @property
    def type(self) -> Literal["Spline"]:
        """Mit type wird ein Identifier der Klasse als String zurück gegeben.

        Returns:
            Literal["Spline"]: Class identifier
        """
        return "Spline"

    @property
    def splineType(self) -> Literal[0, 1, 2]:
        """get Spline type. There are 3 different types of Splines that can be generated with Gmsh:
                0 : Catmull-Rom Spline (Build-in Kernel) or C2 BSpline (OpenCASCADE Kernel)
                1 : Bezierkurve
                2 : Basis-Spline

        Returns:
            Literal[0,1,2]: Spline type
        """
        return self._splineType

    @property
    def controlPoints(self) -> List[Point]:
        """Get the controll point list of a Spline

        Returns:
            List[Point]: controll point list
        """
        return self._controlPoints

    @controlPoints.setter
    def controlPoints(self, newControlPointList: List[Point]):
        """Mit setControlPoints können neue Kontrollpunkte der Spline definiert werden.

        Args:
            newControlPointList (List[Point]): List of new controll points
        """
        self._controlPoints = newControlPointList

    def addControlPoint(self, newControllPoint: Point, position: int = None):
        """Mit addControlPoint() kann an einer definierten Postion ein weitere Kontrollpunkt in die Liste der Kontrollpunkte ergänzt werden.

        Args:
            newP (Point): New controll point
            position (int): Position in controll point list Defaults to None. If None, controll point is appended to the controll point list.
        """
        if isinstance(position, int):
            self.controlPoints.insert(position, newControllPoint)
        else:
            self.controlPoints.append(newControllPoint)

    def removeControlPoint(self, point: Point):
        """Mit removeControlPoint() kann ein definierter Punkt aus der Liste der Kontrollpunkte entfernt werden.

        Args:
            point (Point): Controll point that should be removed.
        """
        cpList = self.controlPoints
        if point in cpList:
            cpList.remove(point)
        else:
            raise (
                UserWarning(
                    f"Tried to remove Point '{point.name}' from controll points of Spline '{self.name}', but point was not found in controll point list."
                )
            )

    def getPoints(self) -> List["Point"]:
        points = []
        points.extend(super().points)
        points.extend(self.controlPoints)
        return points

    def translate(self, dx: float, dy: float, dz: float):
        """Mit translate() wird das Objekt linear verschoben. Die Inputvariablen dx, dy und dz beschreiben die Verschiebungsfaktoren in der x-, y- und z- Richtung.

        Args:
            dx (float): x offset
            dy (float): y offset
            dz (float): z offset
        """
        if self._todesmerker == True:
            return None
        else:
            self.startPoint.translate(dx, dy, dz)
            self.endPoint.translate(dx, dy, dz)
            for p in self.controlPoints:
                p.translate(dx, dy, dz)

    def rotateX(self, rotationPoint: Point, angle):
        """Mit rotateX() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die X-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.
        """
        if self._todesmerker == True:
            return None
        else:
            self.startPoint.rotateX(rotationPoint, angle)
            self.endPoint.rotateX(rotationPoint, angle)
            for p in self._controlPoints:
                p.rotateX(rotationPoint, angle)

    def rotateY(self, rotationPoint, angle):
        """Mit rotateY() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die Y-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.

        """
        if self._todesmerker == True:
            return None
        else:
            self.startPoint.rotateY(rotationPoint, angle)
            self.endPoint.rotateY(rotationPoint, angle)
            for p in self._controlPoints:
                p.rotateY(rotationPoint, angle)

    def rotateZ(self, rotationPoint, angle):
        """Mit rotateZ() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die Z-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle.
        """
        if self._todesmerker == True:
            return None
        else:
            self.startPoint.rotateZ(rotationPoint, angle)
            self.endPoint.rotateZ(rotationPoint, angle)
            for p in self._controlPoints:
                p.rotateZ(rotationPoint, angle)

    def duplicate(self, name="") -> "Spline":
        """Mit duplicate() wird eine Spline mit gleichen Eigenschaften zur Originalen erzeugt. Diese Spline hat jedoch eine unterschiedliche ID.
                Beispiel:
                SP1 = Spline('sp1', P1, P2, [P3, P4, P5])
                SP2 = SP1.duplicate()
        Args:
            name (str, optional): Name of new spline. Defaults to "".

        Returns:
            Spline: Duplicate of the current Spline
        """
        newP1 = self.startPoint.duplicate()
        newP2 = self.endPoint.duplicate()
        controlPoints: List[Point] = []
        for controllPoint in self.controlPoints:
            controlPoints.append(controllPoint.duplicate())

        dupSpline = Spline(
            name=self._name,
            startPoint=newP1,
            endPoint=newP2,
            controlPoints=controlPoints,
            SplineType=self.splineType,
        )
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                dupSpline.name = f"{parentName}_dup"
            else:
                dupSpline.name = parentName
        return dupSpline

    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        """Mit mirror() kann ein Punkt an einer definierten Ebene gespiegelt werden. Ein Bildpunkt wird hierbei erzeugt. Die Spiegelebene wird durch einen Aufpunkt (planePoint) und 2 Vektoren (planeVector1 und planeVector2) beschrieben.

        Args:
            planePoint (Point): _description_
            planeVector1 (Line): _description_
            planeVector2 (Line): _description_
            name (str, optional): Name of new mirrored point. Defaults to None.

        Returns:
            Point: mirrored point

        Beispiel:
            P0 = Point('P0', 0, 0, 0, 1) \n
            Py = Point('Py', 0, 1, 0, 1) \n
            Pz = Point('Pz', 0, 0, 1, 1) \n
            yAxis = Line(P0, Py) \n
            zAxis = Line(P0, Pz) \n
            P1 = Point('P1', 1, 0, 0, 0.3) \n
            P2 = P1.mirror(P0, yAxis, zAxis) \n
        """
        p1 = self.startPoint.mirror(planePoint, planeVector1, planeVector2)
        p2 = self.endPoint.mirror(planePoint, planeVector1, planeVector2)
        cp = []
        for p in self._controlPoints:
            pmirror = p.mirror(planePoint, planeVector1, planeVector2)
            cp.append(pmirror)

        cp.reverse()
        SP = Spline(self._name, p2, p1, cp)
        if name == "":
            SP.name = "SP_" + str(abs(SP.id))
        else:
            SP.name = name
        return SP

    # def plot(
    #     self,
    #     fig=None,
    #     linewidth=0.5,
    #     color=[random() for i in range(3)],
    #     marker=None,
    #     markersize=1,
    # ):
    #     controlPoints = self.getControlPoints()
    #     centerCoords = centerPoint.getCoordinate()

    #     if not fig:
    #         fig, ax = plt.subplots()
    #         ax.add_patch(arc)
    #         ax.set_aspect("equal", adjustable="box")
    #         ax.autoscale()
    #         fig.set_dpi(300)
    #     else:
    #         fig.axes[0].add_patch(arc)
    #     # if marker not None: Plot points
    #     if marker:
    #         centerPoint.plot(fig, marker, markersize, color=color)
    #         self.startPoint.plot(fig, marker, markersize, color=color)
    #         self.endPoint.plot(fig, marker, markersize, color=color)
