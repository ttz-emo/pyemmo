"""Module: spmsm_rotor_contour_calculation"""

import math
import copy
from typing import Union

from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM

from ..json.SurfaceJSON import SurfaceAPI
from ...script.geometry.point import Point
from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from ...functions.plot import plot
from .. import logger


def general_calc_spmsm_cont(
    machine: MachineSIPMSM,
    rotor_lam_surf_list: list[SurfaceAPI],
    rotor_mag_surf_list: list[SurfaceAPI],
    radius: float,
    is_internal_rotor: bool,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """General calculations for creating the rotor contour: \n
    * Filtering the lines that lie on the air gap
    * Detecting the outer points of the rotor contour facing the air gap

    Args:
        machine (MachineSIPMSM): Pyleecan machine
        rotorLamSurfList (list[SurfaceAPI]): List of the pyemmo-surfaces of the rotor
        radius (float): if inner rotor ``rotor_rint``, if external rotor
            ``rotor_rext``
        is_internal_rotor (bool): Internal or external rotor

    Returns:
        Tuple[List[Union[Line, CircleArc]], Point, Point]: A tuple containing:
            - A list of contour lines for the SPMSM rotor.
            - The right point of the rotor contour.
            - The left point of the rotor contour.
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

    # logger.debug("---")
    # logger.debug("Plot Überprüfung des Löschens der Seitenlinien.")
    # plot(rotor_cont_line_list, linewidth=1, markersize=3)
    # logger.debug("---")

    # --------------------------------------------
    # Filtering the outermost points of the rotor:
    # --------------------------------------------
    # r_point_rotor_cont = Point("rPointRotorCont", x=0, y=0, z=0, meshLength=0)
    # l_point_rotor_cont = Point("lPointRotorCont", x=0, y=0, z=0, meshLength=0)
    rotor_seg_angle = 360 / machine.rotor.comp_periodicity_geo()[0]

    if math.isclose(a=rotor_seg_angle, b=0, abs_tol=1e-6):
        rotor_seg_angle = 180

    if is_internal_rotor:
        for curve in rotor_cont_line_list:
            for point in curve.points:
                angle_point = (
                    math.atan2(point.coordinate[1], point.coordinate[0])
                    / math.pi
                    * 180
                )
                if math.isclose(a=angle_point, b=0, abs_tol=1e-6):
                    angle_point = 180
                if (
                    math.isclose(
                        a=angle_point, b=rotor_seg_angle, abs_tol=1e-6
                    )
                    and (
                        (point.radius < machine.rotor.Rext)
                        or (
                            math.isclose(
                                point.radius, machine.rotor.Rext, abs_tol=1e-6
                            )
                        )
                    )
                    and (
                        point.radius > machine.rotor.Rint
                        or (
                            math.isclose(
                                point.radius, machine.rotor.Rint, abs_tol=1e-6
                            )
                        )
                    )
                ):
                    l_point_rotor_cont = point
                if (
                    math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6)
                    and point.coordinate[0] > radius
                ):
                    r_point_rotor_cont = point

    else:
        smallest_prev_x_rotor = machine.rotor.Rext
        for curve in rotor_cont_line_list:
            for point in curve.points:
                if point.coordinate[0] < smallest_prev_x_rotor:
                    smallest_prev_x_rotor = point.coordinate[0]
                    l_point_rotor_cont = point

                if (
                    math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6)
                    and point.coordinate[0] > radius
                ):
                    r_point_rotor_cont = point

    for mag_surf in rotor_mag_surf_list:
        rotor_cont_line_list.extend(mag_surf.curve)

    return (
        rotor_cont_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
    )


def calc_spmsm_rotor_cont(
    machine: MachineSIPMSM,
    rotor_lam_surf_list: list,
    rotor_mag_surf_list: list,
    radius: float,
    is_internal_rotor: bool,
) -> tuple[list, Point, Point]:
    """
    Calculates the contour lines for the surface permanent magnet synchronous machine (SPMSM) rotor.

    This function calculates the contour lines for the SPMSM rotor based on
    the provided machine, rotor lamination surface list, rotor magnet surface list,
    radius, and whether the rotor is internal or external.

    Args:
        machine (MachineSIPMSM): The PYLEECAN SPMSM machine.
        rotor_lam_surf_list (List[Surface]): A list of rotor lamination surfaces.
        rotor_mag_surf_list (List[Surface]): A list of rotor magnet surfaces.
        radius (float): The radius of the rotor.
        is_internal_rotor (bool): Whether the rotor is internal or external.

    Returns:
        tuple[List, Point, Point]: A tuple containing:
            - A list of contour lines for the SPMSM rotor.
            - The right point of the rotor contour.
            - The left point of the rotor contour.

    Notes:
        - The contour lines are calculated based on the provided machine, rotor lamination
          surface list, rotor magnet surface list, radius, and whether the rotor is internal or external.
        - Duplicate lines or circle arcs are filtered out based on the intersection points between
          rotor lamination and magnet surfaces.
        - The contour lines are plotted for visualization.
    """

    (
        rotor_cont_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
    ) = general_calc_spmsm_cont(
        machine=machine,
        rotor_lam_surf_list=rotor_lam_surf_list,
        rotor_mag_surf_list=rotor_mag_surf_list,
        radius=radius,
        is_internal_rotor=is_internal_rotor,
    )

    # ----------------------------------------------
    # Aussortieren von doppelten Linien/Kreisboegen:
    # ----------------------------------------------
    rotor_cont_line_list_copy = copy.copy(rotor_cont_line_list)
    for rotor_lam_curve in rotor_cont_line_list_copy:
        for rotor_mag_surf in rotor_mag_surf_list:
            # Rotor-Lamination Curves
            for rotor_mag_curve in rotor_mag_surf.curve:
                # Rotor-Magnet Curves
                if (
                    math.isclose(
                        a=rotor_mag_curve.startPoint.coordinate[0],
                        b=rotor_lam_curve.endPoint.coordinate[0],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotor_mag_curve.endPoint.coordinate[1],
                        b=rotor_lam_curve.startPoint.coordinate[1],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotor_mag_curve.endPoint.coordinate[0],
                        b=rotor_lam_curve.startPoint.coordinate[0],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotor_mag_curve.endPoint.coordinate[1],
                        b=rotor_lam_curve.startPoint.coordinate[1],
                        abs_tol=1e-6,
                    )
                ):
                    logger.debug("gefiltert: %s", rotor_lam_curve)
                    logger.debug("gefiltert: %s", rotor_mag_curve)
                    rotor_cont_line_list.remove(rotor_lam_curve)
                    rotor_cont_line_list.remove(rotor_mag_curve)
                    # plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)

    # logger.debug("Plot contourLineList ")
    # plot(rotor_cont_line_list, linewidth=1, markersize=3, tag=True)
    # logger.debug("---")

    return rotor_cont_line_list, r_point_rotor_cont, l_point_rotor_cont
