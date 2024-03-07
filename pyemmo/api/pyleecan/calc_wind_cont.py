"""Module: wind_contour_calculation"""

import math
from typing import Union

from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc

# from ...script.geometry.point import Point
# from ...script.geometry import defaultCenterPoint
from ..json.SurfaceJSON import SurfaceAPI
from ...functions.plot import plot
from .get_rotor_stator_surfs import get_stator_surfs


def calc_wind_contour(
    geometry_list: list[SurfaceAPI],
    stator_rint: float,
    stator_rext: float,
) -> list[Union[Line, CircleArc]]:
    """Calculation for the contour of a slot with winding.

    Args:
        geometry_list (list): A list of geometry elements.
        stator_rint (float): The inner radius of the stator.
        stator_rext (float): The outer radius of the stator.

    Returns:
        list[Union[Line, CircleArc]]: A list of wind contour lines for the stator.

    Notes:
        - The wind contour lines are calculated based on the provided geometry list
          and stator inner and outer radii.
        - The wind contour lines are plotted for visualization.
    # """
    # TODO: Filterung der Konturlinien anpassen. Wicklungskontur(en) von der
    # Innenkontur der Statorblechs abziehen. Die Interface-Linie zwischen
    # Nutschlitz und Wicklung ist diejenige Linie, die nicht in der Wicklungs-
    # UND Statorkontur vorkommt.
    
    stator_cont_line_list: list[Union[Line, CircleArc]] = []
    stator_lam_surf_list = get_stator_surfs(geometry_list=geometry_list)

    # Creation of the rotor contour line for MovingBand:

    # Filtering out the lines that do not lie on the surface facing the air gap:
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
        if (
            curve.startPoint.radius > stator_rint
            or curve.startPoint.radius > stator_rext
        ) and math.isclose(
            a=curve.startPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            slot_op_points.append(curve.startPoint)
        elif (
            curve.endPoint.radius > stator_rint
            or curve.endPoint.radius > stator_rext
        ) and math.isclose(
            a=curve.endPoint.radius, b=stator_rint, abs_tol=1e-6
        ) is False:
            slot_op_points.append(curve.endPoint)

    # For translating SlotW22:
    # center_point = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
    # stator_new_line = CircleArc(
    #     name="windNewCircleArc",
    #     startPoint=stator_line_point_list[0],
    #     endPoint=stator_line_point_list[1],
    #     centerPoint=center_point,
    # )
    assert (
        len(slot_op_points) == 2
    ), "Could not find exactly two points at the interface of slot and slot opening"

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
