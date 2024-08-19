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
"""Module for CircleArc Geometry"""
from math import atan2, cos, isclose, sin
from random import random
from typing import Literal, Tuple

from matplotlib import pyplot as plt
from matplotlib.patches import Arc
from numpy import pi, rad2deg

from ...definitions import DEFAULT_GEO_TOL
from .line import Line
from .point import Point
from ..geometry import defaultCenterPoint

import gmsh


class CircleArc(Line):
    """Eine Instanz der Unterklasse CircleArc ist ein Kreissegment, zwischen zwei Punkten
      (Objekte der Klasse Point) mit einem Mittelpunkt, im dreidimensionalen Raum.

    Beispiel:

    .. code::

        from pyemmo.script.geometry.point import Point
        from pyemmo.script.geometry.point import CircleArc
        C = Point('c', 0, 0, 0, 0.3)
        P1 = Point('p1', 1, 0, 0, 0.3)
        P2 = Point('p2', 0, 1, 0, 0.3)
        CA1 = CircleArc('ca1', P1, C, P2)

    """

    def __init__(
        self,
        name: str,
        startPoint: Point,
        centerPoint: Point,
        endPoint: Point,
        force: bool = False,
    ):
        """CircleArc

        Args:
            - name (str): Name of arc.
            - p1 (Point): Start point of arc.
            - c (Point): Center point of arc.
            - p2 (Point): End point of arc.
            - force (bool, optional): Flag to force generation of arc in script.
            Defaults to False.

        Raises:
            ValueError: If start and endpoint are equal.
        """
        try:
            super().__init__(name, startPoint, endPoint, force)
        except ValueError as exce:
            raise (
                ValueError(
                    "If you really want to draw a full circle"
                    " consider using 4 circle arcs."
                )
            ) from exce
        except Exception as exc:
            raise exc

        self.center: Point = centerPoint
        # make sure that start and end point have the same distance (radius)
        # to the center point:
        self.radius  # raises error if not

        ###Id des Kreisbogens.
        self.id = self._getNewID()
        ###Todesmerker wird nur gesetzt, wenn das Objekt im Skript erzeugt wurde
        # (Aufruf von addToScript())!
        self._todesmerker = False
        self._force = force

        self._id = gmsh.model.occ.addCircleArc(startPoint.id, centerPoint.id, endPoint.id)

        

    def __eq__(self, other: "CircleArc") -> bool:
        # check type:
        if isinstance(other, self.__class__):
            # check that all points are equal
            if self.arePointsEqual(other):
                if self.center.isEqual(other.center):
                    return True
            else:
                return False
        return False

    @property
    def center(self) -> Point:
        """Die Methode center gibt den Mittelpunkt der Kreiskurve zurück.

        Returns:
            Point: Center point of circle arc
        """
        return self._center

    @center.setter
    def center(self, newCenterPoint: Point) -> None:
        """setter of center point

        Args:
            newP (Point): New center point of CircleArc
        """
        self._center = newCenterPoint
        # FIXME: Make sure other points are changed too, !if position changes!

    @property
    def type(self) -> Literal["CircleArc"]:
        """getter of curve type

        Returns:
            str: Literal 'CircleArc'
        """
        return "CircleArc"

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """Mit translate() kann ein Kreisbogen linear verschoben werden. Die
        Inputvariablen dx, dy und dz beschreiben die Verschiebungsfaktoren in der
        x-, y- und z- Richtung.

        Args:
            dx (float): x translation [m]
            dy (float): y translation [m]
            dz (float): z translation [m]

        Beispiel:
          CA1 = ('ca1', P1, C, P2)\n
          CA1.translate(0, 1, 0)\n
        """
        if not self._todesmerker:
            # if line was not created in script
            self.startPoint.translate(dx, dy, dz)
            self.endPoint.translate(dx, dy, dz)
            self._center.translate(dx, dy, dz)

    def rotateX(self, rotationPoint: Point, angle: float):
        """Mit rotateX() wird ein Kreisbogen um einen Rotationspunkt
        (rotationPoint) und die X-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): rotation center point
            angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            CA1 = Line('ca1', P1, C, P2)\n
            CA1.rotateX(P0, pi)\n
        """
        if not self._todesmerker:
            self.startPoint.rotateX(rotationPoint, angle)
            self.endPoint.rotateX(rotationPoint, angle)
            self._center.rotateX(rotationPoint, angle)

    def rotateY(self, rotationPoint: Point, angle: float) -> None:
        """Mit rotateY() wird ein Kreisbogen um einen Rotationspunkt
        (rotationPoint) und die Y-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point): rotation center point
            - angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            CA1 = Line('ca1', P1, C, P2)\n
            CA1.rotateY(P0, pi)\n

        """
        if not self._todesmerker:
            self.startPoint.rotateY(rotationPoint, angle)
            self.endPoint.rotateY(rotationPoint, angle)
            self._center.rotateY(rotationPoint, angle)

    ##
    ###
    def rotateZ(self, rotationPoint=defaultCenterPoint, angle=0.0) -> None:
        """Mit rotateZ() wird ein Kreisbogen um einen Rotationspunkt
        (rotationPoint) und die Z-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (_type_, optional): Rotation Center Point.
            Defaults to Point("tmpCenterPoint", 0, 0, 0, 1).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:

            from math import pi
            CA1 = Line('ca1', P1, C, P2)
            CA1.rotateZ(P0, pi)
        """
        if not self._todesmerker:
            self.startPoint.rotateZ(rotationPoint, angle)
            self.endPoint.rotateZ(rotationPoint, angle)
            self._center.rotateZ(rotationPoint, angle)

    def duplicate(self, name="") -> "CircleArc":
        """Mit duplicate() wird einer Kreisbogen mit gleichen Eigenschaften zum
        Originalen erzeugt. Diese Kurve hat jedoch eine unterschiedliche ID.

        Args:
            name (str, optional): Name of duplicte. Defaults to "".

        Returns:
            CircleArc: Duplicate of CircleArc Object

        Beispiel:
            CA1 = Point('ca1', P1, C, P2)\n
            CA2 = CA1.duplicate()\n
        """
        startPoint = self.startPoint.duplicate()
        centerPoint = self._center.duplicate()
        endPoint = self.endPoint.duplicate()
        dupCircleArc = CircleArc(name, startPoint, centerPoint, endPoint)
        parentName = self.name
        if name == "":
            # TODO: Check the name generation so the name does not get too
            # long or something
            if "_dup" not in parentName:
                dupCircleArc.name = parentName + "_dup"
            else:
                dupCircleArc.name = parentName
        return dupCircleArc

    def mirror(
        self,
        planePoint: Point,
        planeVector1: Line,
        planeVector2: Line,
        name: str = "",
    ) -> "CircleArc":
        """Mit mirror() kann ein Kreisbogen an einer definierten Ebene gespiegelt
        werden. Bildpunkte werden hierbei generiert und eine Kurve zwischen den Punkten
        erzeugt. Die Spiegelebene wird durch einen Aufpunkt (planePoint) und 2 Vektoren
        (planeVector1 und planeVector2) beschrieben.

        Args:
            planePoint (Point): Aufpunkt der Ebene
            planeVector1 (Line): Erster Ebenenvektor.
            planeVector2 (Line): Zweiter Ebenenvektor.
            name (str, optional): Name der neuen Linie. Defaults to "".

        Returns:
            CircleArc: Mirrored CircleArc object

        Beispiel:

        .. code:: python

            P0 = Point('P0', 0, 0, 0, 1)
            Py = Point('Py', 0, 1, 0, 1)
            Pz = Point('Pz', 0, 0, 1, 1)
            yAxis = Line(P0, Py)
            zAxis = Line(P0, Pz)
            P1 = Point('P1', 1, 0, 0, 1)
            P2 = Point('P1', 0, 1, 0, 1)
            CA1 = CircleArc('ca1', P1, P0, P2)
            CA2 = CA1.mirror(P0, yAxis, zAxis)

        """
        startPoint = self.startPoint.mirror(
            planePoint, planeVector1, planeVector2
        )
        endPoint = self.endPoint.mirror(planePoint, planeVector1, planeVector2)
        centerPoint = self._center.mirror(
            planePoint, planeVector1, planeVector2
        )
        mirArc = CircleArc(self.name, endPoint, centerPoint, startPoint)
        if name == "":
            mirArc.name = "CA_" + str(abs(mirArc.id))
        else:
            mirArc.name = name
        return mirArc

    def getAnglesToX(self, inDeg=False) -> Tuple[float, float]:
        """calculate the angles to the horizontal axis of the center point (x-axis)
        in rad or deg.

        Args:
            - inDeg (bool, optional): Return the angle in degree.
            Defaults to False (-> radians).

        Returns:
            Tuple(float, float): angle of start and end point to the horizontal axis
        """
        startPoint = self.startPoint
        endPoint = self.endPoint
        centerPoint = self.center
        angleStart = startPoint.getAngleToX(
            flag_deg=inDeg, CenterPoint=centerPoint
        )
        angleEnd = endPoint.getAngleToX(
            flag_deg=inDeg, CenterPoint=centerPoint
        )
        return angleStart, angleEnd

    def getAngle(self, inDeg=False) -> float:
        """get the angle between the points of the circle arc.

        Args:
            inDeg (bool, optional): Return the angle in degree. Defaults to False
            (-> radians).

        Returns:
            float: angle between start and end point of the circle arc in [-180, 180].
            Value is negative if arc direction is clock wise.
        """
        thetaStart, thetaEnd = self.getAnglesToX()
        angleDiff = thetaEnd - thetaStart
        angle = atan2(sin(angleDiff), cos(angleDiff))
        if inDeg:
            return rad2deg(angle)
        else:
            return angle

    @property
    def radius(self) -> float:
        """Return the distance between the center point and the start point (P1) of the
        CircleArc (= radius)

        Returns:
            float: radius of the circle arc

        Raises:
            ValueError: if start and end point of the circle arc don't have the same
            distance to the center point
        """
        center = self.center
        startPoint = self.startPoint
        endPoint = self.endPoint
        if isclose(
            center.calcDist(startPoint.coordinate),
            center.calcDist(endPoint.coordinate),
            abs_tol=DEFAULT_GEO_TOL,
        ):
            radius = center.calcDist(startPoint.coordinate)
            return radius
        # pylint: disable=locally-disabled,  line-too-long
        raise (
            ValueError(
                f"Start and end point of circle arc '{self.name}' dont have the same distance to the center point:"
                f"Distance Pc-P1={center.calcDist(startPoint.coordinate)}; "
                f"Distance Pc-P2 = {center.calcDist(endPoint.coordinate)}."
            )
        )

    def plot(
        self,
        fig=None,
        marker=None,
        markersize=1,
        linewidth=0.5,
        color=[random() for i in range(3)],
        tag=False,
    ):
        """Circle Arc plot

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            marker (str, optional): Defaults to None.
            markersize (float, optional): Defaults to 1.
            linewidth (float): Defaults to 0.5.
            color (list, optional): Defaults to [random() for i in range(3)].
            tag (bool): Flag to print arc id and name like "C `L_ID` ("`L_Name`")"
            and point tags if marker is not None.
        """
        # pylint: disable=locally-disabled, too-many-locals, too-many-arguments
        centerPoint = self.center
        centerCoords = centerPoint.coordinate
        diameter = self.radius * 2
        thetaStart, thetaEnd = self.getAnglesToX(inDeg=False)
        angleDiff = thetaEnd - thetaStart
        if (
            atan2(sin(angleDiff), cos(angleDiff)) * 180 / pi
        ) > 0:  # if rotation direction from start to end angle is positiv
            theta1 = thetaStart
            theta2 = thetaEnd
        else:  # if the direction is negativ: switch points
            theta1 = thetaEnd
            theta2 = thetaStart
        arc = Arc(
            xy=(centerCoords[0], centerCoords[1]),
            width=diameter,
            height=diameter,
            angle=0,
            theta1=rad2deg(theta1),
            theta2=rad2deg(theta2),
            color=color,
            linewidth=linewidth,
        )
        if not fig:
            fig, axes = plt.subplots()
            axes.set_aspect("equal", adjustable="box")
            axes.autoscale()
            fig.set_dpi(300)
        else:
            axes = fig.axes[0]
        axes.add_patch(arc)
        if tag:
            # add tag to arc
            tagPoint = self.startPoint.duplicate()
            tagPoint.rotateZ(centerPoint, (theta2 - theta1) / 2)
            tagCo = tagPoint.coordinate
            axes.annotate(
                f"""C {self.id} ("{self.name}")""",
                (tagCo[0], tagCo[1]),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
        # if marker not None: Plot points
        if marker:
            centerPoint.plot(fig, marker, markersize, color=color, tag=tag)
            self.startPoint.plot(fig, marker, markersize, color=color, tag=tag)
            self.endPoint.plot(fig, marker, markersize, color=color, tag=tag)

    def combine(
        self, addLine: "CircleArc", touchPoint: Point = None
    ) -> "CircleArc":
        """combine two arcs and return them as new CircleArc

        Args:
            - addLine (CircleArc): line to combine with this line
            - dockingPoint (Point): Point where the lines touch each other. Defaults to
            None. Trying to identify the point if its not given.


        """
        if self == addLine:
            return self
        # pylint: disable=locally-disabled, unidiomatic-typecheck
        if not type(addLine) == type(
            self
        ):  # make sure the line types are equal
            raise TypeError(
                "Tried to combine lines, but the line types are different! "
                f"{type(self)} != {type(addLine)}"
            )
        # make sure center points are equal
        if not self.center.isEqual(addLine.center):
            raise ValueError(
                f"Tried to combine CircleArcs ({self.name} and "
                f"{addLine.name}) but the centerpoints are not matching!"
            )

        if not touchPoint:
            # find the point where the two lines are touching
            for point in self.points:
                for addP in addLine.points:
                    if point.isEqual(addP):
                        touchPoint: Point = point
                        break
        if touchPoint:
            # get the two points forming the new start and endpoint excluding the docking point
            newPoints = [
                point
                for point in self.points + addLine.points
                if not point.isEqual(touchPoint)
            ]
            if len(newPoints) == 2:  # make sure there are exactly 2 points
                # replace the combined line pattern in the old names if they contained
                lName = self.name.replace("combinedLine_", "")
                addName = addLine.name.replace("combinedLine_", "")
                return CircleArc(
                    name=f"combinedLine_{lName}_{addName}",
                    startPoint=newPoints[0],
                    centerPoint=self.center,
                    endPoint=newPoints[1],
                )
            raise (
                RuntimeError(
                    f"Combination of lines ({self.name} and "
                    f"{addLine.name}) failed. There were {len(newPoints)} "
                    "points to create a new line. There should be 2!"
                )
            )
        raise (
            RuntimeError(
                f"Combination of lines ({self.name} and {addLine.name}) "
                "failed. Could not find touchpoint."
            )
        )
