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
"""Module: rotor_contour_calculation"""

import math
from typing import Union

from ..json.SurfaceJSON import SurfaceAPI
from ...script.geometry.point import Point
from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from ...functions.plot import plot


def calc_even_rotor_cont(
    rotor_lam_surf_list: list[SurfaceAPI],
    radius: float,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """
    Calculates the contour lines for the even rotor contour.

    This function calculates the contour lines for an even rotor contour based on
    the provided rotor lamination surface list and radius.

    Args:
        rotor_lam_surf_list (list[SurfaceAPI]): A list of rotor lamination surfaces.
        radius (float): The radius of the rotor.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: A tuple containing:
            - A list of contour lines for the even rotor.
            - The right point of the rotor contour.
            - The left point of the rotor contour.

    Notes:
        - The contour lines are calculated based on the provided rotor lamination
          surface list and radius.
        - The contour lines are plotted for visualization.
    """

    rotor_cont_line_list = []

    # --------------------------------------------
    # Filtering the lines that lie at the air gap:
    # --------------------------------------------
    # rotor lamination:
    for curve in rotor_lam_surf_list[0].curve:
        if not (
            math.isclose(a=curve.startPoint.radius, b=radius, abs_tol=1e-6)
        ) and not math.isclose(
            a=curve.endPoint.radius, b=radius, abs_tol=1e-6
        ):
            rotor_cont_line_list.append(curve)
    # print("---")
    # print("Plot Überprüfung des Löschens der Seitenlinien.")
    # plot(rotor_cont_line_list, linewidth=1, markersize=3)
    # print("---")

    for point in rotor_cont_line_list[0].points:
        if math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6):
            r_point_rotor_cont = point
        else:
            l_point_rotor_cont = point

    return rotor_cont_line_list, r_point_rotor_cont, l_point_rotor_cont
