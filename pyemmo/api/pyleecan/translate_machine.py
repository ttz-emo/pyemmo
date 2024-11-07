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
"""
Moving Band Builder Module

This module provides functions for building moving bands at the rotor and stator
side of an electric machine.

Functions:

    -   ``build_bands_rotor``: Builds the air gap segments at the rotor side.
    -   ``build_bands_stator``: Builds the air gap segments at the stator side.
    -   ``calcs_radii``: Calculates the magnet radii and the distance between
        rotor/magnet and stator inner radius.
    -   ``get_translated_machine``: Translates the geometry and creates rotor and
        stator contours.
"""

from __future__ import annotations

import logging
import math

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSCIM import MachineSCIM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line
from ...script.geometry.point import Point
from .. import air
from ..json import ROTOR_AIRGAP_IDEXT, STATOR_AIRGAP_IDEXT
from ..json.modelJSON import createSurfaceDict
from ..json.SurfaceJSON import SurfaceAPI
from . import PyleecanMachine
from .create_geo_dict import create_geo_dict
from .get_coords_for_point import get_x_for_point, get_y_for_point


def build_bands_rotor(
    machine: PyleecanMachine,
    band_radius_list: list,
    r_point_rotor_cont: Point,
    l_point_rotor_cont: Point,
    rotor_cont_line_list: list,
) -> tuple[SurfaceAPI, SurfaceAPI, float]:
    """
    Builds the air gap segments at the rotor side.

    Args:
        machine (PyleecanMachine): Pyleecan machine.
        band_radius_list (list): List with the radii of the bands.
        r_point_rotor_cont (Point): Rightmost point of rotor contour.
        l_point_rotor_cont (Point): Leftmost point of rotor contour.
        rotor_cont_line_list (list): List of rotor contour lines.

    Returns:
        tuple[SurfaceAPI, SurfaceAPI, float]: Tuple containing two air gap
        surfaces and the radius of the moving band.
    """
    nbr_rotor_seg = machine.rotor.comp_periodicity_geo()[0]
    angle_rotor = 2 * math.pi / nbr_rotor_seg  # [rad]
    center_point = Point(name="centerPointBand", x=0, y=0, z=0, meshLength=1e-3)

    # -----------------
    # Rotor inner band:
    # -----------------
    # Points:
    mb_mesh_len = 2 * band_radius_list[1] * math.pi / 360
    point_m11 = Point(
        name="PointM11",
        x=band_radius_list[0],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )
    point_m12 = Point(
        name="PointM12",
        x=get_x_for_point(band_radius_list[0], angle_rotor),
        y=get_y_for_point(band_radius_list[0], angle_rotor),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    rotor_circle1 = CircleArc(
        name="rotorBand1",
        startPoint=point_m11,
        endPoint=point_m12,
        centerPoint=center_point,
    )

    # Adding curves to list:
    rotor_air_gap1_curves = []
    rotor_air_gap1_curves.extend(rotor_cont_line_list)
    rotor_air_gap1_curves.append(rotor_circle1)
    rotor_air_gap1_curves.append(
        Line(
            name="lowerLine1",
            start_point=r_point_rotor_cont,
            end_point=point_m11,
        )
    )
    rotor_air_gap1_curves.append(
        Line(
            name="upperLine1",
            start_point=l_point_rotor_cont,
            end_point=point_m12,
        )
    )

    # Assginment of rotorBand1 as surface:
    # band closing the rotor contour and providing smooth interface for second airgap.
    rotor_air_gap1 = SurfaceAPI(
        name="rotor air - airgap 1",
        idExt="rotor air",
        curves=rotor_air_gap1_curves,
        material=air,
        nbrSegments=nbr_rotor_seg,
        angle=angle_rotor,
        meshSize=1.0,
    )
    assert rotor_air_gap1.idExt != ROTOR_AIRGAP_IDEXT

    # plot(rotor_air_gap1_curves, linewidth=1, markersize=3, tag=True)

    # ------------------------------------
    # Rotor outer band (Movingband Curve):
    # ------------------------------------
    # Points:
    point_m21 = Point(
        name="PointM21",
        x=band_radius_list[1],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )
    point_m22 = Point(
        name="PointM22",
        x=get_x_for_point(band_radius_list[1], angle_rotor),
        y=get_y_for_point(band_radius_list[1], angle_rotor),
        z=0,
        meshLength=mb_mesh_len,
    )
    rotor_mb_arcs = []
    if nbr_rotor_seg == 2:
        # TODO: Improve this. This is only a workaround for sym-factor = 2!
        # add third point to make arc < 180 deg!
        point_m23 = Point(
            name="PointM22",
            x=get_x_for_point(band_radius_list[1], angle_rotor / 2),
            y=get_y_for_point(band_radius_list[1], angle_rotor / 2),
            z=0,
            meshLength=mb_mesh_len,
        )
        rotor_mb_arcs.append(
            CircleArc(
                name="MB_CurveRotor_1",
                startPoint=point_m21,
                endPoint=point_m23,
                centerPoint=center_point,
            )
        )
        rotor_mb_arcs.append(
            CircleArc(
                name="MB_CurveRotor_2",
                startPoint=point_m23,
                endPoint=point_m22,
                centerPoint=center_point,
            )
        )
    else:
        rotor_mb_arcs.append(
            CircleArc(
                name="MB_CurveRotor",
                startPoint=point_m21,
                endPoint=point_m22,
                centerPoint=center_point,
            )
        )

    # Adding curves to list:
    rotor_air_gap2_curves = []
    rotor_air_gap2_curves.append(rotor_circle1)
    rotor_air_gap2_curves.extend(rotor_mb_arcs)
    rotor_air_gap2_curves.append(
        Line(name="lowerLine2", start_point=point_m11, end_point=point_m21)
    )
    rotor_air_gap2_curves.append(
        Line(name="upperLine2", start_point=point_m12, end_point=point_m22)
    )

    # Assginment of rotorBand2 as surface:
    rotor_air_gap2 = SurfaceAPI(
        name="rotor airgap 2",
        idExt=ROTOR_AIRGAP_IDEXT,
        curves=rotor_air_gap2_curves,
        material=air,
        nbrSegments=nbr_rotor_seg,
        angle=angle_rotor,
        meshSize=1.0,
    )
    mb_radius = band_radius_list[1]

    # # RotorBandsCurves only for plots:
    # rotor_air_cap_curves = []
    # rotor_air_cap_curves.append(rotor_air_gap1_curves)
    # rotor_air_cap_curves.append(rotor_air_gap2_curves)
    # plot(rotor_air_cap_curves, linewidth=1, markersize=3, tag=True)
    # print("---")

    return (
        rotor_air_gap1,
        rotor_air_gap2,
        mb_radius,
    )


def build_bands_stator(
    machine: PyleecanMachine,
    stator_cont_line_list: list,
    band_radius_list: list,
) -> tuple[SurfaceAPI, SurfaceAPI]:
    """
    Builds the air gap segments at the stator side.

    Args:
        machine (PyleecanMachine): Pyleecan machine.
        stator_cont_line_list (list): List of stator contour lines.
        band_radius_list (list): List with the radii of the bands.

    Returns:
        tuple[SurfaceAPI, SurfaceAPI]: Tuple containing two air gap surfaces at
        the stator side.
    """
    nbr_stator_seg = machine.stator.slot.Zs
    angle_stator = 2 * math.pi / nbr_stator_seg  # [rad]
    center_point = Point(name="centerPointBand", x=0, y=0, z=0, meshLength=1e-3)

    # ------------------
    # Stator outer band:
    # ------------------
    biggest_previous_y_stator = 0
    biggest_y_point_stator: Point | None = None
    lowest_y_point_stator: Point | None = None

    for curve in stator_cont_line_list:
        for point in curve.points:
            if point.coordinate[1] > biggest_previous_y_stator:
                biggest_previous_y_stator = point.coordinate[1]
                biggest_y_point_stator = point
            elif point.coordinate[1] == 0:
                lowest_y_point_stator = point

    # Points:
    mb_mesh_len = 2 * band_radius_list[2] * math.pi / 360

    point_m41 = Point(
        name="PointM41",
        x=band_radius_list[3],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )

    point_m42 = Point(
        name="PointM42",
        x=get_x_for_point(band_radius_list[3], angle_stator),
        y=get_y_for_point(band_radius_list[3], angle_stator),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    stator_circle4 = CircleArc(
        name="statorCircle4",
        startPoint=point_m41,
        endPoint=point_m42,
        centerPoint=center_point,
    )

    lower_line4 = Line(
        name="lowerLine4", start_point=lowest_y_point_stator, end_point=point_m41
    )

    upper_line4 = Line(
        name="upperLine4",
        start_point=biggest_y_point_stator,
        end_point=point_m42,
    )

    # Adding curves to list:
    curves_stlu1 = []
    curves_stlu1.extend(stator_cont_line_list)
    curves_stlu1.append(stator_circle4)
    curves_stlu1.append(lower_line4)
    curves_stlu1.append(upper_line4)

    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        from ...functions.plot import plot

        fig, ax = plot(curves_stlu1, linewidth=1, markersize=3, tag=True)
    # Assginment of statorAirGap1 as surface:
    stator_air_gap1 = SurfaceAPI(
        name="stator air - airgap 1",
        idExt="stator air",
        curves=curves_stlu1,
        material=air,
        nbrSegments=nbr_stator_seg,
        angle=angle_stator,
        meshSize=1.0,
    )
    assert stator_air_gap1.idExt != STATOR_AIRGAP_IDEXT
    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        stator_air_gap1.plot(fig=fig)

    # ------------------
    # Stator inner band:
    # ------------------
    # Points:
    point_m31 = Point(
        name="PointM31",
        x=band_radius_list[2],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )

    point_m32 = Point(
        name="PointM32",
        x=get_x_for_point(band_radius_list[2], angle_stator),
        y=get_y_for_point(band_radius_list[2], angle_stator),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    stator_circle3 = CircleArc(
        name="MB_CurveStator",
        startPoint=point_m31,
        endPoint=point_m32,
        centerPoint=center_point,
    )

    lower_line3 = Line(name="lowerLine3", start_point=point_m31, end_point=point_m41)

    upper_line3 = Line(name="upperLine3", start_point=point_m32, end_point=point_m42)

    # Adding curves to list 'curvesStLu2':
    curves_stlu2 = []
    curves_stlu2.append(stator_circle4)
    curves_stlu2.append(stator_circle3)
    curves_stlu2.append(lower_line3)
    curves_stlu2.append(upper_line3)

    # Assginment of statorBand3 as surface:
    stator_air_gap2 = SurfaceAPI(
        name="stator airgap 2",
        idExt=STATOR_AIRGAP_IDEXT,
        curves=curves_stlu2,
        material=air,
        nbrSegments=nbr_stator_seg,
        angle=angle_stator,
        meshSize=1.0,
    )
    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
        stator_air_gap2.plot(fig=fig)

    return stator_air_gap1, stator_air_gap2


def calcs_radii(
    machine: PyleecanMachine, is_internal_rotor: bool
) -> tuple[float, float]:
    """Calculation of the magnet-radii and of the distance between rotor/magnet
    and stator inner radius

    Args:
        machine (PyleecanMachine): Pyleecan machine.
        is_internal_rotor (bool): Indicates whether the rotor is internal or not.

    Returns:
        tuple[float, float]: Tuple containing the distance between rotor/magnet
        and stator inner radius, and the maximum radius.
    """

    rotor_rint = machine.rotor.Rint
    rotor_rext = machine.rotor.Rext
    stator_rint = machine.stator.Rint
    stator_rext = machine.stator.Rext

    if isinstance(machine, MachineSIPMSM):
        h0 = machine.rotor.slot.H0
        h1 = machine.rotor.slot.H1

        if is_internal_rotor:
            magnet_farthest_radius = rotor_rext + h1 - h0
            magnet_shortest_radius = rotor_rext - h0

            if rotor_rext > magnet_farthest_radius:
                diff_radius = stator_rint - rotor_rext
                max_radius = rotor_rext

            else:
                diff_radius = stator_rint - magnet_farthest_radius
                max_radius = magnet_farthest_radius

        else:
            magnet_farthest_radius = rotor_rint + h0
            magnet_shortest_radius = rotor_rint + h0 - h1

            if rotor_rint < magnet_shortest_radius:
                diff_radius = stator_rext - rotor_rint
                max_radius = rotor_rint

            else:
                diff_radius = stator_rext - magnet_shortest_radius
                max_radius = magnet_shortest_radius

    elif isinstance(machine, (MachineIPMSM, MachineSyRM, MachineSCIM)):
        if is_internal_rotor:
            max_radius = rotor_rext
            diff_radius = stator_rint - max_radius
        else:
            max_radius = rotor_rint
            diff_radius = stator_rext - max_radius
    else:
        raise ValueError("Wrong machine type!")  # TODO: Optimize error message
    return diff_radius, max_radius


def translate_machine(
    machine: PyleecanMachine,
) -> tuple[list[SurfaceAPI], list[SurfaceAPI], float, dict, dict]:
    """_summary_

    Args:
        machine (PyleecanMachine): Pyleecan Machine object.

    Raises:
        RuntimeError: If a surface ID is already present in the geometry
            dictionary.

    Returns:
        tuple[list, list[SurfaceAPI], float]: Tuple containing
            - Moving band radius.
            - Magnetization dict.
            - Geometry dict for PyEMMO JSON-api.
    """
    diff_radius, max_radius = calcs_radii(
        machine=machine, is_internal_rotor=machine.rotor.is_internal
    )
    # Translation of geometry and creation of rotor and stator contour:
    (
        geometry_list,
        rotor_cont_line_list,
        stator_cont_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    ) = create_geo_dict(
        machine,
        machine.rotor.is_internal,
    )
    # Calculation of the MovingBand radii:
    wp = diff_radius / 5
    band_radius_list = []

    for i in range(1, 5 + 1):
        band_radius_list.append(max_radius + wp * i)

    (
        rotor_air_gap1,
        rotor_air_gap2,
        movingband_r,
    ) = build_bands_rotor(
        machine=machine,
        band_radius_list=band_radius_list,
        r_point_rotor_cont=r_point_rotor_cont,
        l_point_rotor_cont=l_point_rotor_cont,
        rotor_cont_line_list=rotor_cont_line_list,
    )
    # add rotor airgaps to geo-list:
    geometry_list.extend([rotor_air_gap1, rotor_air_gap2])
    # add stator airgaps to geo-list:
    geometry_list.extend(
        build_bands_stator(
            machine=machine,
            stator_cont_line_list=stator_cont_line_list,
            band_radius_list=band_radius_list,
        )
    )

    # Try to reuse function from json api:
    geo_translation_dict = createSurfaceDict(geometry_list)

    return (
        movingband_r,
        magnetization_dict,
        geo_translation_dict,
    )
