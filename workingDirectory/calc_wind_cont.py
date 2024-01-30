import math
from typing import Union

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from pyemmo.functions.plot import plot
from .get_rotor_stator_surfs import get_stator_surfs


def calc_wind_contour(
    geometry_list: list,
    stator_rint: float,
    stator_rext: float,
) -> list[Union[Line, CircleArc]]:
    """Calculation for the contour of a slot with winding.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        statorRint (float): Inner radius of stator
        statorRext (float): Outer radius of stator

    Returns:
        list[Union[Line, CircleArc]]: list of the stator contour lines
    """
    stator_cont_line_list = []
    stator_lam_surf_list = get_stator_surfs(geometry_list=geometry_list)

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================

    # -----------------------------------------------------------
    # Aussortieren der Linien die nicht an der Oberfläche liegen:
    # -----------------------------------------------------------
    for curve in stator_lam_surf_list[0].curve:
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
            math.isclose(
                a=curve.endPoint.radius,
                b=stator_rext,
                abs_tol=1e-6,
            )
            is False
            and math.isclose(
                a=curve.startPoint.radius,
                b=stator_rext,
                abs_tol=1e-6,
            )
            is False
        ):
            stator_cont_line_list.append(curve)

    stator_line_point_list = []

    for curve in stator_cont_line_list:
        if (
            curve.startPoint.radius > stator_rint
            or curve.startPoint.radius > stator_rext
        ) and math.isclose(
            a=curve.startPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            stator_line_point_list.append(curve.startPoint)
        elif (
            curve.endPoint.radius > stator_rint
            or curve.endPoint.radius > stator_rext
        ) and math.isclose(
            a=curve.endPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            stator_line_point_list.append(curve.endPoint)

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
    
    stator_new_line = Line(
        name="test_line_contour",
        startPoint=stator_line_point_list[0],
        endPoint=stator_line_point_list[1],
    )
    
    stator_cont_line_list.append(stator_new_line)
    print("windContourLineList:")
    plot(stator_cont_line_list, linewidth=1, markersize=3, tag=True)
    print("---")
    return stator_cont_line_list
