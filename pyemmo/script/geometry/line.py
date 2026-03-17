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
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from numpy.linalg import norm

from ...definitions import DEFAULT_GEO_TOL, LINE_COLOR, POINT_COLOR
from ..geometry import defaultCenterPoint
from .point import Point
from .transformable import Transformable

if TYPE_CHECKING:
    from matplotlib.figure import Figure


class Line(Transformable):
    """
    An instance of the class Line is a straight line between two points (objects of the
    class Point).

    Example:
        >>> from pyemmo.script.geometry.point import Point
        >>> from pyemmo.script.geometry.line import Line
        >>> P1 = pyd.Point('p1', 0, 0, 0)
        >>> P2 = pyd.Point('p2', 1, 0, 0)
        >>> L1 = pyd.Line('l1', P1, P2)
    """

    def __init__(
        self,
        name: str,
        start_point: Point,
        end_point: Point,
    ):
        """Init from start and end point

        Args:
            name (str): Name of the line
            start_point (Point): Start point.
            end_point (Point): End point.
        """
        if not start_point.isEqual(end_point):
            ###Startpunkt des Kreisbogens.
            self.start_point = start_point
            ###Endpunkt des Kreisbogens.
            self.end_point = end_point
        else:
            raise (
                ValueError(
                    f"The coordinates of start and end point of Line '{name}' are equal: "
                    f"{start_point.coordinate} - {end_point.coordinate}."
                )
            )
        ###Name der Linie.
        self.name = name

    def __eq__(self, other: Line) -> bool:
        # check type:
        if isinstance(other, self.__class__):
            # check that all points are equal
            return self.arePointsEqual(other)
        return False

    @property
    def start_point(self) -> Point:
        """Start point of line

        Returns:
            Point: Start points
        """
        return self._start_point

    @start_point.setter
    def start_point(self, new_start_point: Point) -> None:
        """setter of start point

        Args:
            new_start_point (Point)
        """
        if not isinstance(new_start_point, Point):
            raise TypeError(
                f"Given start point has wrong type {type(new_start_point)}!"
            )
        self._start_point = new_start_point

    @property
    def end_point(self) -> Point:
        """end point of curve

        Returns:
            Point: End point
        """
        return self._end_point

    @end_point.setter
    def end_point(self, new_end_point: Point) -> None:
        """setter of end point

        Args:
            new_end_point (Point)
        """
        if not isinstance(new_end_point, Point):
            raise TypeError(f"Given end point has wrong type ({type(new_end_point)})")
        self._end_point = new_end_point

    @property
    def points(self) -> tuple[Point, Point]:
        """get the start and end point of a line

        Returns:
            Tuple[Point, Point]: start and end point of the line
        """
        start_point = self.start_point
        end_point = self.end_point
        return (start_point, end_point)

    @property
    def middle_point(self) -> Point:
        """Get the center point between start and end point.

        Its not named 'center_point' because we have allready defined center_point in
        ``CircleArc``

        Returns:
            Point: Center point in the middle between start and end point.
        """
        return Point(
            name=f"Middle point of {self.name}",
            x=(self.start_point.coordinate[0] + self.end_point.coordinate[0]) / 2,
            y=(self.start_point.coordinate[1] + self.end_point.coordinate[1]) / 2,
            z=(self.start_point.coordinate[2] + self.end_point.coordinate[2]) / 2,
        )

    @property
    def vector(self) -> np.ndarray:
        """Get the vector between end and start point.

        Returns:
            np.ndarray: 3D-Vector (x,y,z)
        """
        return array(self.end_point.coordinate) - array(self.start_point.coordinate)

    @property
    def complex(self) -> complex:
        """Get the complex value of the (2D) line vector.

        Returns:
            complex: Complex vector of line vector.

        Raises:
            RuntimeError: If z-component of self.vector is not 0.
        """
        if self.vector[2] != 0:
            raise RuntimeError(
                "Can not return complex representation of vector with z-component!"
            )
        return complex(self.vector[0], self.vector[1])

    @property
    def length(self) -> float:
        """Get the length of the line

        Returns:
            float: Length of the line.
        """
        return self.getPointDist()

    def switchPoints(self) -> None:
        """switch start and end point of curve (revert direction)

        Returns:
            nothing
        """
        oldP1 = self.start_point
        oldP2 = self.end_point
        self.start_point = oldP2
        self.end_point = oldP1

    def translate(self, dx: float, dy: float, dz: float):
        """Translate line

        Args:
            dx, dy, dz (float): offset in meter
        """
        self.start_point.translate(dx, dy, dz, flag_gmsh=False)
        self.end_point.translate(dx, dy, dz, flag_gmsh=False)

    def rotateZ(self, rotationPoint=defaultCenterPoint, angle=0.0):
        """Rotation around the z-axis by ``angle`` in radians.
        The default rotation center point it the model origin
        (:obj:`~pyemmo.script.geometry.defaultCenterPoint`).

        Args:
            rotationPoint (Point, optional): Rotation center point.
                Defaults to :obj:`defaultCenterPoint` =
                Point("tmpCenterPoint", 0, 0, 0, 1).
            angle (float, optional): Rotation angle in rad. Defaults to 0.0.
        """
        if not isinstance(rotationPoint, Point):
            raise TypeError("Rotation point must be a Point object!")
        if not isinstance(angle, (int, float)):
            raise TypeError("Angle must be a number!")
        self.start_point.rotateZ(rotationPoint, angle)
        self.end_point.rotateZ(rotationPoint, angle)

    def rotateY(self, rotationPoint: Point, angle: float):
        """Rotation of the line around the y-axis.

        Args:
           rotationPoint (Point): rotation center point
           angle (float): rotation angle in rad
        """
        if not isinstance(rotationPoint, Point):
            raise TypeError("Rotation point must be a Point object!")
        if not isinstance(angle, (int, float)):
            raise TypeError("Angle must be a number!")
        self.start_point.rotateY(rotationPoint, angle)
        self.end_point.rotateY(rotationPoint, angle)

    def rotateX(self, rotationPoint: Point, angle: float):
        """Rotation around x-axis by angle in radians.

        Args:
           rotationPoint (Point): rotation center point
           angle (float): rotation angle in rad
        """
        if not isinstance(rotationPoint, Point):
            raise TypeError("Rotation point must be a Point object!")
        if not isinstance(angle, (int, float)):
            raise TypeError("Angle must be a number!")
        self.start_point.rotateX(rotationPoint, angle)
        self.end_point.rotateX(rotationPoint, angle)

    def duplicate(self, name=""):
        """Create a copy of the line

        Args:
            name (str, optional): Name of duplicte. Defaults to "".

        Returns:
            CircleArc: Duplicate of CircleArc object
        """
        newP1 = self.start_point.duplicate()
        newP2 = self.end_point.duplicate()
        dupLine = Line(name, newP1, newP2)
        # set new line name
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                dupLine.name = f"{parentName}_dup"
            else:
                dupLine.name = parentName
        return dupLine

    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        """Mirror a circle arc by a plane.

        Args:
            planePoint (Point): Start point of the plane
            planeVector1 (Line): First plane vector.
            planeVector2 (Line): Second plane vector.
            name (str, optional): New name of the arc. Defaults to "".

        Returns:
            CircleArc: Mirrored CircleArc object
        """
        p1 = self.start_point.mirror(planePoint, planeVector1, planeVector2)
        p2 = self.end_point.mirror(planePoint, planeVector1, planeVector2)
        mirLine = Line(self._name, p2, p1)
        if name == "":
            mirLine.name = f"mirrored line ({self.name})"
        else:
            mirLine.name = name
        return mirLine

    def getPointDist(self) -> float:
        """calculate the distance between start and end point"""
        start_point = array(self.start_point.coordinate)
        end_point = array(self.end_point.coordinate)
        return norm(start_point - end_point)

    def plot(
        self,
        fig: Figure = None,
        marker=None,
        markersize=1.0,
        linewidth=0.5,
        color=LINE_COLOR,
        tag=False,
    ):
        """Line plot

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            marker (str, optional): Defaults to None.
            markersize (float, optional): Defaults to 1.
            linewidth (float): Defaults to 0.5.
            color (list, optional): Defaults to [random() for i in range(3)].
            tag (bool): Flag to print line id and name like "L `L_ID` ("`L_Name`")"
                and point tags if `marker` is given.
        """
        start_point = self.start_point
        end_point = self.end_point
        startCoords = start_point.coordinate
        endCoords = end_point.coordinate
        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect("equal", adjustable="box")
            fig.set_dpi(300)
        else:
            ax = fig.axes[0]
        ax.plot(
            [startCoords[0], endCoords[0]],
            [startCoords[1], endCoords[1]],
            linewidth=linewidth,
            color=color,
        )
        if tag:
            # add tag to line
            ax.annotate(
                f"""L ("{self.name}")""",
                (
                    sum([startCoords[0], endCoords[0]]) / 2,
                    sum([startCoords[1], endCoords[1]]) / 2,
                ),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
        if marker is not None:
            # need to check color for str, because can also be list/np.ndarray
            if isinstance(color, str) and color == LINE_COLOR:
                # if color is default value
                p_color = POINT_COLOR
            else:
                p_color = color
            start_point.plot(
                fig=fig,
                marker=marker,
                markersize=markersize,
                color=p_color,
                tag=tag,
            )
            end_point.plot(
                fig=fig,
                marker=marker,
                markersize=markersize,
                color=p_color,
                tag=tag,
            )

    def arePointsEqual(self, compLine: Line, tol=DEFAULT_GEO_TOL) -> bool:
        """
        Checks if start and end point of two lines are identical.
        The result is regardless of the direction.
        """
        originP1 = array(self.start_point.coordinate)
        originP2 = array(self.end_point.coordinate)
        compP1 = array(compLine.start_point.coordinate)
        compP2 = array(compLine.end_point.coordinate)
        # FIXME: Does not respect the type of line yet!
        if norm(originP1 - compP1) < tol:
            # oP1 and cP1 are identical
            if norm(originP2 - compP2) < tol:
                # if oP1=cP1, oP2 must be cP2 to return True
                return True
            return False
        if norm(originP1 - compP2) < tol:
            # oP1 and cP2 are identical
            if norm(originP2 - compP1) < tol:
                # if oP1=cP2, oP2 must be cP1 to return True
                return True
        return False

    def combine(self, addLine: Line, touchPoint: Point | None = None) -> Line:
        """combine two lines and return them as new line

        Args:
            addLine (Line): line to combine with this line
            touchPoint (Point): Point where the lines touch each other. Defaults to None.
                Trying to identify the point if its not given.
        """
        # pylint: disable=locally-disabled, unidiomatic-typecheck
        if not type(addLine) == type(self):  # make sure the line types are equal
            raise (
                TypeError(
                    "Tried to combine lines, but the line types are different! "
                    f"{type(self)} != {type(addLine)}"
                )
            )
        # TODO: Remove touchpoint from arguments since its unnessecary in gmsh representation
        if not touchPoint:
            for p in self.points:
                for addP in addLine.points:
                    if p.isEqual(addP):
                        touchPoint: Point = p
                        break
        if not touchPoint:
            raise (
                RuntimeError(
                    f"Combination of lines ({self.name} and {addLine.name}) failed."
                    "Could not find touchpoint."
                )
            )

        if (np.angle(self.complex) != np.angle(addLine.complex)) and (
            np.angle(self.complex) != np.angle(-addLine.complex)
        ):
            # angle of vectors are not matching in any direction...
            raise RuntimeError("Lines do not have same direction.")

        # get the two points excluding the docking point
        newPoints = [
            point
            for point in self.points + addLine.points
            if not point.isEqual(touchPoint)
        ]
        if len(newPoints) != 2:
            raise (
                RuntimeError(
                    f"Combination of lines ({self.name} and {addLine.name}) failed."
                    f"{len(newPoints)} points to create a new line; should be 2!"
                )
            )
        # replace the combined line pattern in the old names if they contained
        lName = self.name.replace("combinedLine_", "")
        addName = addLine.name.replace("combinedLine_", "")
        combined_line = Line(
            f"combinedLine_{lName}_{addName}",
            start_point=newPoints[0],
            end_point=newPoints[1],
        )
        return combined_line

    def containsPoint(self, refPoint: Point, tol: float = DEFAULT_GEO_TOL) -> bool:
        """This function checks if start or end point coordinates are equal to the given
        reference point.

        Args:
            refPoint (Point): Reference point to check for.
            tol (float): Geometric tolerance for the comparison of the coordinates.

        Returns:
            bool: True if line contains point, False if not.
        """
        if not isinstance(refPoint, Point):
            raise ValueError(f"Given reference point has wrong type ({type(refPoint)})")
        if not isinstance(tol, (int, float)):
            raise ValueError("Given tolerance is not type int or float!")
        for p in self.points:
            if p.isEqual(refPoint, tol=tol):
                return True
        return False

    def angle_to_middle(self) -> float:
        """Return the angle of the middle point of the curve to the x-axis
        This can be used to sort lists of curve in circumferential direction.

        Returns:
            float: Angle of the line middle point to x axis.
        """
        return self.middle_point.getAngleToX()
