#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
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
""""""
from __future__ import annotations

from math import atan2, cos, isclose, sin

from matplotlib import pyplot as plt
from matplotlib.patches import Arc
from numpy import pi, rad2deg

from ...definitions import DEFAULT_GEO_TOL, LINE_COLOR, POINT_COLOR
from ..geometry import defaultCenterPoint
from .line import Line
from .point import Point


class CircleArc(Line):
    """CircleArc is a circle arc segement between two points around a center point.

    Example:

        >>> from pyemmo.script.geometry.point import Point
        >>> from pyemmo.script.geometry.point import CircleArc
        >>> C = Point('center', 0, 0, 0)
        >>> P1 = Point('start point', 1, 0, 0)
        >>> P2 = Point('end point', 0, 1, 0)
        >>> CA1 = CircleArc('arc name', P1, C, P2)

    """

    def __init__(
        self,
        name: str,
        startPoint: Point,
        centerPoint: Point,
        endPoint: Point,
    ):
        """Initialize from start, end and center point.

        Args:
            - name (str): Name of arc.
            - p1 (Point): Start point of arc.
            - c (Point): Center point of arc.
            - p2 (Point): End point of arc.

        Raises:
            ValueError: If start and endpoint are equal.
        """
        # Name der Linie.
        self.name = name
        if not startPoint.isEqual(endPoint):
            self.start_point = startPoint
            self.end_point = endPoint
        else:
            raise ValueError(
                "If you really want to draw a full circle  consider using 4 circle arcs."
            )
        self.center: Point = centerPoint
        # make sure that start and end point have the same distance (radius)
        # to the center point:
        _ = self.radius  # raises error if not

    def __eq__(self, other: CircleArc) -> bool:
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
        """Returns the center point of the arc.

        Returns:
            Point: Center point of circle arc
        """
        return self._center

    @center.setter
    def center(self, newCenterPoint: Point) -> None:
        """Set new center point

        Args:
            newP (Point): New center point of CircleArc
        """
        if not isinstance(newCenterPoint, Point):
            raise TypeError(
                f"Center point of CircleArc '{self.name}' must be a Point object, "
                f"but is {type(newCenterPoint)}"
            )
        self._center = newCenterPoint
        # FIXME: Make sure other points are changed too, !if position changes!

    @property
    def length(self) -> float:
        """Get the length of the line

        Returns:
            float: Length of the line.
        """
        r = self.radius
        theta = self.getAngle()
        # circumference = 2*pi*r where the part of the circle is theta/(2*pi)
        # => 2*pi*r*theta/(2*pi) = r*theta
        return abs(r * theta)

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """Linear translation of the arc by dx, dy and dz.

        Args:
            dx (float): x translation [m]
            dy (float): y translation [m]
            dz (float): z translation [m]

        Example:

            >>> CA1 = ('ca1', P1, C, P2)
            >>> CA1.translate(0, 1, 0)
        """
        self.start_point.translate(dx, dy, dz)
        self.end_point.translate(dx, dy, dz)
        self._center.translate(dx, dy, dz)

    def rotateX(self, rotationPoint: Point, angle: float):
        """Rotation around x-axis by angle in radians.

        Args:
            rotationPoint (Point): rotation center point
            angle (float): rotation angle in rad

        Example:

            >>> from math import pi
            >>> CA1 = Line('ca1', P1, C, P2)
            >>> CA1.rotateX(P0, pi)
        """
        self.start_point.rotateX(rotationPoint, angle)
        self.end_point.rotateX(rotationPoint, angle)
        self._center.rotateX(rotationPoint, angle)

    def rotateY(self, rotationPoint: Point, angle: float) -> None:
        """Rotation of the arc around the y-axis.

        Args:
            rotationPoint (Point): rotation center point
            angle (float): rotation angle in rad

        Example:

            >>> from math import pi\n
            >>> CA1 = Line('ca1', P1, C, P2)\n
            >>> CA1.rotateY(P0, pi)\n

        """
        self.start_point.rotateY(rotationPoint, angle)
        self.end_point.rotateY(rotationPoint, angle)
        self._center.rotateY(rotationPoint, angle)

    def rotateZ(self, rotationPoint=defaultCenterPoint, angle=0.0) -> None:
        """Rotation around the z-axis by ``angle`` in radians.
        The default rotation center point it the model origin
        (:obj:`~pyemmo.script.geometry.defaultCenterPoint`).

        Args:
            rotationPoint (_type_, optional): Rotation Center Point.
                Defaults to Point("tmpCenterPoint", 0, 0, 0, 1).
            angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Example:

            >>> from math import pi
            >>> CA1 = Line('ca1', P1, C, P2)
            >>> CA1.rotateZ(P0, pi)
        """
        self.start_point.rotateZ(rotationPoint, angle)
        self.end_point.rotateZ(rotationPoint, angle)
        self._center.rotateZ(rotationPoint, angle)

    def duplicate(self, name="") -> CircleArc:
        """Create a copy of the circle arc.

        Args:
            name (str, optional): Name of duplicte. Defaults to "{arc name}_dup".

        Returns:
            CircleArc: Duplicate of CircleArc Object

        Example:

            >>> CA1 = Point('ca1', P1, C, P2)
            >>> CA2 = CA1.duplicate()
        """
        startPoint = self.start_point.duplicate()
        centerPoint = self._center.duplicate()
        endPoint = self.end_point.duplicate()
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
    ) -> CircleArc:
        """Mirror a circle arc by a plane.

        Args:
            planePoint (Point): Start point of the plane
            planeVector1 (Line): First plane vector.
            planeVector2 (Line): Second plane vector.
            name (str, optional): New name of the arc. Defaults to "".

        Returns:
            CircleArc: Mirrored CircleArc object

        Example:

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
        startPoint = self.start_point.mirror(planePoint, planeVector1, planeVector2)
        endPoint = self.end_point.mirror(planePoint, planeVector1, planeVector2)
        centerPoint = self._center.mirror(planePoint, planeVector1, planeVector2)
        mirArc = CircleArc(self.name, endPoint, centerPoint, startPoint)
        if name == "":
            mirArc.name = f"mirrored CircleArc {self.name}"
        else:
            mirArc.name = name
        return mirArc

    def getAnglesToX(self, inDeg=False) -> tuple[float, float]:
        """calculate the angles to the horizontal axis of the center point (x-axis)
        in rad or deg.

        Args:
            inDeg (bool, optional): Return the angle in degree.
                Defaults to False (-> radians).

        Returns:
            Tuple(float, float): angle of start and end point to the horizontal axis
        """
        startPoint = self.start_point
        endPoint = self.end_point
        centerPoint = self.center
        angleStart = startPoint.getAngleToX(flag_deg=inDeg, CenterPoint=centerPoint)
        angleEnd = endPoint.getAngleToX(flag_deg=inDeg, CenterPoint=centerPoint)
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
        return angle

    @property
    def radius(self) -> float:
        """Return the distance between the center point and the start/end point of the
        CircleArc (= radius).

        Returns:
            float: radius of the circle arc

        Raises:
            ValueError: if start and end point of the circle arc don't have the same
            distance to the center point
        """
        center = self.center
        startPoint = self.start_point
        endPoint = self.end_point
        if isclose(
            center.calcDist(startPoint.coordinate),
            center.calcDist(endPoint.coordinate),
            abs_tol=DEFAULT_GEO_TOL,
        ):
            radius = center.calcDist(startPoint.coordinate)
            return radius
        raise (
            ValueError(
                f"Start and end point of circle arc '{self.name}' "
                "dont have the same distance to the center point:"
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
        color=LINE_COLOR,
        tag=False,
    ):
        """Plot the circle arc

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            marker (str, optional): Defaults to None.
            markersize (float, optional): Defaults to 1.
            linewidth (float): Defaults to 0.5.
            color (list, optional): Defaults to [random() for i in range(3)].
            tag (bool): Flag to print name like "C ("`L_Name`")"
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
            tagPoint = self.start_point.duplicate()
            tagPoint.rotateZ(centerPoint, (thetaEnd - thetaStart) / 2)
            tagCo = tagPoint.coordinate
            axes.annotate(
                f"""CA ("{self.name}")""",
                (tagCo[0], tagCo[1]),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
        # if marker not None: Plot points
        if marker:
            # need to check color for str, because can also be list/np.ndarray
            if isinstance(color, str) and color == LINE_COLOR:
                # if color is default value
                p_color = POINT_COLOR
            else:
                p_color = color
            centerPoint.plot(
                fig,
                marker,
                markersize,
                color=p_color,
                tag=tag,
            )
            self.start_point.plot(
                fig,
                marker,
                markersize,
                color=p_color,
                tag=tag,
            )
            self.end_point.plot(
                fig,
                marker,
                markersize,
                color=p_color,
                tag=tag,
            )

    def combine(self, addLine: CircleArc, touchPoint: Point = None) -> CircleArc:
        """combine two arcs and return them as new CircleArc

        Args:
            addLine (CircleArc): line to combine with this line
            touchPoint (Point): Point where the lines touch each other. Defaults to
                None. Trying to identify the point if its not given.
        """
        if self == addLine:
            return self
        # pylint: disable=locally-disabled, unidiomatic-typecheck
        if not type(addLine) == type(self):  # make sure the line types are equal
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
