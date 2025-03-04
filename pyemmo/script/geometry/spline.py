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
from typing import List, Literal, Union

import matplotlib.pyplot as plt
import numpy as np
from splines import Bernstein, CatmullRom, Natural

from ...definitions import LINE_COLOR, POINT_COLOR
from . import defaultCenterPoint
from .line import Line
from .point import Point

NBR_INTERPOLATION_POINTS = 100


class Spline(Line):
    """Class Spline Child of class line"""

    def __init__(
        self,
        name: str,
        start_point: Point,
        end_point: Point,
        control_points: List[Point],
        spline_type: Literal[0, 1, 2] = 0,
    ):
        """Konstruktor der Klasse Spline

        Args:
            name (str): Name of the Spline
            p1 (Point): start_point
            p2 (Point): end_point
            control_points (List[Point]): List of controll points
            spline_type (Literal[0, 1, 2], optional): There are 3 different types of Splines
             that can be generated with Gmsh. Defaults to 0 (Spline):

                0 : Catmull-Rom Spline (Build-in Kernel) or C2 BSpline (OpenCASCADE Kernel)
                1 : Bezierkurve
                2 : Basis-Spline

        """
        super().__init__(name=name, start_point=start_point, end_point=end_point)
        ###Zwischenpunkte vom Polynomzug in der richtigen durchzulaufenden Reihenfolge.
        self.control_points = control_points
        # 0: Catmull-Rom Spline, 1: Bezierkurve, 2: Basis-Spline
        self._spline_type = spline_type

    @property
    def spline_type(self) -> Literal[0, 1, 2]:
        """get Spline type.
        There are 3 different types of Splines that can be generated with Gmsh:

            0 : Catmull-Rom Spline (Build-in Kernel) or C2 BSpline (OpenCASCADE Kernel)
            1 : Bezierkurve
            2 : Basis-Spline

        Returns:

            Literal[0,1,2]: Spline type
        """
        return self._spline_type

    @property
    def control_points(self) -> List[Point]:
        """Get the controll point list of a Spline

        Returns:
            List[Point]: controll point list
        """
        return self._control_points

    @control_points.setter
    def control_points(self, new_control_points: List[Point]):
        """Mit setControlPoints können neue Kontrollpunkte der Spline definiert werden.

        Args:
            newControlPointList (List[Point]): List of new controll points
        """
        self._control_points = new_control_points

    def addControlPoint(
        self, new_control_point: Point, position: Union[int, None] = None
    ):
        """Mit addControlPoint() kann an einer definierten Postion ein weitere
        Kontrollpunkt in die Liste der Kontrollpunkte ergänzt werden.

        Args:
            new_control_point (Point): New controll point
            position (int): Position in controll point list Defaults to None. If None,
                controll point is appended to the controll point list.
        """
        if isinstance(position, int):
            self.control_points.insert(position, new_control_point)
        else:
            self.control_points.append(new_control_point)

    def removeControlPoint(self, point: Point):
        """Mit removeControlPoint() kann ein definierter Punkt aus der Liste der
        Kontrollpunkte entfernt werden.

        Args:
            point (Point): Controll point that should be removed.
        """
        cpList = self.control_points
        if point in cpList:
            cpList.remove(point)
        else:
            raise (
                ValueError(
                    f"Tried to remove Point '{point.name}' from controll points of "
                    f"Spline '{self.name}', but point was not found in controll point list."
                )
            )

    @property
    def points(self) -> list[Point]:
        """get the start and end point of a line

        Returns:
            list[Point]: List of all points, starting with start point, then control
            points and ends with end point.
        """
        points = [self.start_point]
        points.extend(self.control_points)
        points.append(self.end_point)
        return points

    def translate(self, dx: float, dy: float, dz: float):
        """Mit translate() wird das Objekt linear verschoben. Die Inputvariablen dx, dy
        und dz beschreiben die Verschiebungsfaktoren in der x-, y- und z- Richtung.

        Args:
            dx (float): x offset
            dy (float): y offset
            dz (float): z offset
        """
        self.start_point.translate(dx, dy, dz)
        self.end_point.translate(dx, dy, dz)
        for p in self.control_points:
            p.translate(dx, dy, dz)

    def rotateX(self, rotationPoint: Point, angle):
        """Mit rotateX() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die
        X-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.
        """
        self.start_point.rotateX(rotationPoint, angle)
        self.end_point.rotateX(rotationPoint, angle)
        for p in self._control_points:
            p.rotateX(rotationPoint, angle)

    def rotateY(self, rotationPoint, angle):
        """Mit rotateY() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die
        Y-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle in radians.

        """
        self.start_point.rotateY(rotationPoint, angle)
        self.end_point.rotateY(rotationPoint, angle)
        for p in self._control_points:
            p.rotateY(rotationPoint, angle)

    def rotateZ(self, rotationPoint: Point = defaultCenterPoint, angle: float = 0.0):
        """Mit rotateZ() wird ein Punkt um einen Rotationspunkt (rotationPoint) und die
        Z-Achse mit einem definierten Winkel rotiert.

        Args:
            rotationPoint (Point): Centerpoint of rotation.
            angle (float): Rotational angle.
        """
        self.start_point.rotateZ(rotationPoint, angle)
        self.end_point.rotateZ(rotationPoint, angle)
        for p in self._control_points:
            p.rotateZ(rotationPoint, angle)

    def duplicate(self, name="") -> "Spline":
        """Mit duplicate() wird eine Spline mit gleichen Eigenschaften zur Originalen
        erzeugt. Diese Spline hat jedoch eine unterschiedliche ID.
                Beispiel:
                    SP1 = Spline('sp1', P1, P2, [P3, P4, P5])
                    SP2 = SP1.duplicate()

        Args:
            name (str, optional): Name of new spline. Defaults to \"\".

        Returns:
            Spline: Duplicate of the current Spline

        """
        newP1 = self.start_point.duplicate()
        newP2 = self.end_point.duplicate()
        control_points: List[Point] = []
        for controllPoint in self.control_points:
            control_points.append(controllPoint.duplicate())

        dupSpline = Spline(
            name=self._name,
            start_point=newP1,
            end_point=newP2,
            control_points=control_points,
            spline_type=self.spline_type,
        )
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                dupSpline.name = f"{parentName}_dup"
            else:
                dupSpline.name = parentName
        return dupSpline

    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        """Mit mirror() kann ein Punkt an einer definierten Ebene gespiegelt werden. Ein
        Bildpunkt wird hierbei erzeugt. Die Spiegelebene wird durch einen Aufpunkt
        (planePoint) und 2 Vektoren (planeVector1 und planeVector2) beschrieben.

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
        p1 = self.start_point.mirror(planePoint, planeVector1, planeVector2)
        p2 = self.end_point.mirror(planePoint, planeVector1, planeVector2)
        cp = []
        for p in self._control_points:
            pmirror = p.mirror(planePoint, planeVector1, planeVector2)
            cp.append(pmirror)

        cp.reverse()
        SP = Spline(self._name, p2, p1, cp)
        if name == "":
            SP.name = f"mirrored spline {self.name}"
        else:
            SP.name = name
        return SP

    def plot(
        self,
        fig=None,
        linewidth: float = 0.5,
        color=LINE_COLOR,
        marker=None,
        markersize: float = 1,
        tag: bool = False,
    ):
        """TODO

        Depended on the spline type the correct spline type in the ``splines``
        module will be selected:

        +-------+-----------------------------------+------------------------+
        | Index | Gmsh Spline-Type                  | splines-module class   |
        +=======+===================================+========================+
        | 0     | Catmull-Rom Spline or C2 BSpline  | CatmullRom             |
        +-------+-----------------------------------+------------------------+
        | 1     | Bezierkurve                       | Bernstein              |
        +-------+-----------------------------------+------------------------+
        | 2     | Basis-Spline                      | Natural                |
        +-------+-----------------------------------+------------------------+

        Args:
            fig (_type_, optional): _description_. Defaults to None.
            linewidth (float, optional): _description_. Defaults to 0.5.
            color (_type_, optional): _description_. Defaults to LINE_COLOR.
            marker (_type_, optional): _description_. Defaults to None.
            markersize (int, optional): _description_. Defaults to 1.
        """
        all_points = self.points
        xy_list = []
        for p in all_points:
            xy_list.append((p.coordinate[0], p.coordinate[1]))
        if self.spline_type == 0:
            spline = CatmullRom(xy_list)
        elif self.spline_type == 1:
            spline = Bernstein([xy_list])
        else:
            spline = Natural(xy_list)
        times = np.linspace(spline.grid[0], spline.grid[-1], 100)
        # shape (2,100) -> (xy, index)
        xy_point_list = spline.evaluate(times).T
        if not fig:
            fig, ax = plt.subplots()
            ax.set_aspect("equal", adjustable="box")
            ax.autoscale()
            fig.set_dpi(300)
        else:
            ax = fig.axes[0]
        ax.plot(
            *xy_point_list,
            linewidth=linewidth,
            color=color,
            label=self.name,
        )
        if tag:
            # add tag to line
            ax.annotate(
                f"""Spline ("{self.name}")""",
                spline.evaluate(0.5),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
        # if marker not None: Plot points
        if marker:
            for p in all_points:
                p.plot(
                    fig,
                    marker,
                    markersize,
                    color=color if color != LINE_COLOR else POINT_COLOR,
                    tag=tag,
                )
