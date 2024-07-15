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
import math
from typing import Union

from ...functions.plot import plot
from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line

# from ...script.geometry.point import Point
# from ...script.geometry import defaultCenterPoint
from ..json.SurfaceJSON import SurfaceAPI
from .get_rotor_stator_surfs import get_stator_surfs


def calc_wind_contour(
    geometry_list: list[SurfaceAPI],
    stator_rint: float,
    stator_rext: float,
) -> list[Union[Line, CircleArc]]:
    """Calculation for the contour of a slot with winding.

        TODO: Filterung der Konturlinien anpassen. Wicklungskontur(en) von der
        Innenkontur der Statorblechs abziehen. Die Interface-Linie zwischen Nutschlitz
        und Wicklung ist diejenige Linie, die nicht in der Wicklungs- UND Statorkontur
        vorkommt.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        statorRint (float): Inner radius of stator
        statorRext (float): Outer radius of stator

    Returns:
        list[Union[Line, CircleArc]]: list of the stator contour lines
    """
    stator_cont_line_list: list[Union[Line, CircleArc]] = []
    stator_lam_surf_list = get_stator_surfs(geometry_list=geometry_list)

    # -----------------------------------------------------------
    # Fügt Linien die an der Oberfläche liegen hinzu:
    # -----------------------------------------------------------
    for curve in stator_lam_surf_list[0].curve:
        # if one point is on rInt (airgap) and none of the curve points
        # is on rExt (outer radius)
        if (
            math.isclose(
                a=curve.startPoint.radius,
                b=stator_rint,
                abs_tol=1e-6,
            )
            or math.isclose(
                a=curve.endPoint.radius,
                b=stator_rint,
                abs_tol=1e-6,
            )
        ) and (
            not math.isclose(
                a=curve.endPoint.radius,
                b=stator_rext,
                abs_tol=1e-6,
            )
            and not math.isclose(
                a=curve.startPoint.radius,
                b=stator_rext,
                abs_tol=1e-6,
            )
        ):
            stator_cont_line_list.append(curve)

    # extract the points on the interface between slot opening and winding surface
    slot_op_points = []  # list for interface points

    for curve in stator_cont_line_list:
        # TODO: Describe what this if-case is doing.
        if (curve.startPoint.radius > stator_rint or curve.startPoint.radius > stator_rext) and math.isclose(
            a=curve.startPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            slot_op_points.append(curve.startPoint)
        elif (curve.endPoint.radius > stator_rint or curve.endPoint.radius > stator_rext) and math.isclose(
            a=curve.endPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            slot_op_points.append(curve.endPoint)

    # ------------------------
    # For translating SlotW22:
    # ------------------------
    # center_point = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
    # stator_new_line = CircleArc(
    #     name="windNewCircleArc",
    #     startPoint=stator_line_point_list[0],
    #     endPoint=stator_line_point_list[1],
    #     centerPoint=center_point,
    # )
    if len(slot_op_points) != 2:
        raise RuntimeError("Could not find exactly two points at the interface of slot and slot opening")

    # determine slot opening line type: Line or CircleArc
    slot_surfs: list[SurfaceAPI] = []
    for surf in geometry_list:
        if "StCu" in surf.idExt:
            slot_surfs.append(surf)

    slot_op_curve = slot_surfs[0].curve[0]
    for slot_surf in slot_surfs:
        # FIXME: This assumes that it is an inner rotor
        # just find the most inner curve of all slot surfs
        for curve in slot_surf.curve:
            if curve.middlePoint.radius < slot_op_curve.middlePoint.radius:
                slot_op_curve = curve

    # we need to check for exact type here!F
    if type(slot_op_curve) == Line:
        stator_slot_opening_line = Line(
            name="interface line slot opening - slot",
            startPoint=slot_op_points[0],
            endPoint=slot_op_points[1],
        )
    elif type(slot_op_curve) == CircleArc:
        stator_slot_opening_line = CircleArc(
            name="interface line slot opening - slot",
            startPoint=slot_op_points[0],
            endPoint=slot_op_points[1],
            centerPoint=slot_op_curve.center,
        )
    else:
        raise RuntimeError("Could not determine slot opening curve type.")

    stator_cont_line_list.append(stator_slot_opening_line)
    print("windContourLineList:")
    plot(stator_cont_line_list, linewidth=1, markersize=3, tag=True)
    print("---")
    return stator_cont_line_list
