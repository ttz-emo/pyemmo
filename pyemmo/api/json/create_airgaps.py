#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied
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
"""This module implements a function ``create_airgap_surfaces`` - if no airgaps (stator
or rotor) given with the segmented input for the :mod:`~pyemmo.api.json` API, create
them by extracting the inner/outer boundary of stator/rotor and the information about the
movingband radius given with the model information dict."""

from __future__ import annotations

import logging
import gmsh
import numpy as np

from ...definitions import DEFAULT_GEO_TOL
from ...script.gmsh.gmsh_arc import GmshArc
from ...script.gmsh.gmsh_line import GmshLine
from ...script.gmsh.gmsh_point import GmshPoint
from ...script.gmsh.gmsh_surface import GmshSurface
from ...script.gmsh.utils import (
    filter_lines_at_angle,
    get_dim_tags,
    get_max_radius,
    get_min_radius,
    get_global_center,
    create_disk,
)
from .. import air
from ..machine_segment_surface import MachineSegmentSurface
from . import ROTOR_AIRGAP_IDEXT, STATOR_AIRGAP_IDEXT
from . import boundaryJSON as boundary


def create_airgap_surfaces(
    surface_dict: dict[str, list[MachineSegmentSurface]],
    moving_band_radius: float,
    symmetry: int,
):
    """This function can be used to create the airgap surfaces for the current gmsh model.

    The algorithm follows these steps for the rotor and stator side:

        1. Get the interface contour towards the airgap

            1.1 Extract the boundary lines for the combination of all surfaces (total
            outer boundary).

            1.2 Filter out the lines on the symmetry axis.

            1.3 Find the point thats closed to the airgap on the x-axis (PyEMMO models
            allways start with the tooth on the x-axis) and its related curve.

            1.4 Find the remaining lines that connect to this line froming the interface.

        2. Check if the interface lines for a cylindric curve to determine wheter to
        create one or two airgap surfaces.

            If the interface is not purely cylindrical
            (but i.e. includes the slot opening) we create two airgap surfaces
            to improve GetDP torque calculation by the purely cylindrical band.

        3. Find the point which is closest to the airgap **out of all points** to
        determine the band height(s).

            .. note:: If there is no geometrical point object at the closest interface
                section, the airgap creation can fail!

        4. Create the band surface(s) by constructing the curve loop(s) and add it
        to the surface dictionary.

            .. note:: If the symmetry factor is 2, the created arc will be split up into
                two separate curves, because the gmsh geometry export fails for arcs > 180°.

    Args:
        surface_dict (dict[str, list[MachineSegmentSurface]]): Actual surface dict used
            to check for the airgaps and extracting the boundary lines of rotor and
            stator.
        moving_band_radius (float): Radius of the rotor side movingband interface used
            to determine if a surface is on the outer or inner side of the movingband
            and to calculate the airgap band heigt.
        symmetry (int): Symmetry factor of the current model.

    Raises:
        NotImplementedError: If the symmetry of the model is 1.
    """
    if STATOR_AIRGAP_IDEXT in surface_dict and ROTOR_AIRGAP_IDEXT in surface_dict:
        return
    rotor_dim_tags, stator_dim_tags = boundary.get_rotor_stator_dim_tags(
        surface_dict, moving_band_radius
    )
    if not STATOR_AIRGAP_IDEXT in surface_dict:
        # create stator airgap
        logging.info(
            "Starting stator airgap creation since no airgap was given by the input dict."
        )
        # filter boundary lines and remove boundaries on symmetry axis
        bound_lines = boundary.get_boundary_line_list(stator_dim_tags)
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility(gmsh.model.getEntities(), False)
            gmsh.model.setVisibility(get_dim_tags(bound_lines), True, False)
            gmsh.fltk.run()
        if symmetry > 1:
            # if symmetry remove boundary lines on sym-axis
            [
                bound_lines.remove(line)
                for line in filter_lines_at_angle(bound_lines, 0)
                + filter_lines_at_angle(bound_lines, 2 * np.pi / symmetry)
            ]
            if logging.getLogger().getEffectiveLevel() <= logging.DEBUG - 1:
                gmsh.model.setVisibility(gmsh.model.getEntities(), False)
                gmsh.model.setVisibility(get_dim_tags(bound_lines), True, False)
                # for curve in bound_lines:
                #     print(f"{curve}: {curve.id}")
                gmsh.fltk.run()

        # identify point on x-axis with minimal radius
        start_point = None
        start_curve = None
        for curve in bound_lines:
            for point in curve.points:
                if np.isclose(point.y, 0, atol=DEFAULT_GEO_TOL):
                    if start_point is None or start_point.x > point.x and point.x > 0:
                        # point.x > 0 for handling of symmetry of 2
                        start_point = point
                        start_curve = curve
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility([(0, start_point.id)], True)
            gmsh.option.setNumber("Geometry.PointNumbers", 1)
            gmsh.fltk.run()
            gmsh.option.setNumber("Geometry.PointNumbers", 0)  # point ids off

        # get all lines adjacent to the start point
        air_interface = [bound_lines.pop(bound_lines.index(start_curve))]
        while True:
            found_curve = False
            for i, curve in enumerate(bound_lines):
                if (
                    start_curve.start_point in curve.points
                    or start_curve.end_point in curve.points
                ):
                    air_interface.append(bound_lines.pop(i))
                    start_curve = curve  # reset start curve for next interation
                    found_curve = True
                    break  # restart for loop
            if not found_curve:
                break
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility(gmsh.model.getEntities(), False)
            gmsh.model.setVisibility(get_dim_tags(air_interface), True)
            gmsh.fltk.run()

        # check if airgap interface is smooth (only arcs with same radius) to determine
        # if 1 or 2 airgaps should be created
        nbr_airgaps = 1
        try:
            interface_radius = air_interface[0].radius
            for curve in air_interface[1:]:
                if not np.isclose(curve.radius, interface_radius):
                    nbr_airgaps = 2  # create two airgap surfaces
                    break
        except AttributeError:
            nbr_airgaps = 2  # curve is straigt -> 2
        if nbr_airgaps not in (1, 2):
            raise ValueError("Number of airgaps must be 1 or 2")

        # calculate airgap radii
        r_max = get_min_radius(stator_dim_tags)
        # divide distance of rotor moving band in 2 or 3 segments
        band_height = (r_max - moving_band_radius) / (nbr_airgaps + 1)
        if symmetry > 1:
            if nbr_airgaps == 2:
                # create air closing box
                airgap_curve_loop, air_interface, start_point = _create_band_contour(
                    start_point, air_interface, -band_height, symmetry
                )
                surface_dict["Stator Air"] = [
                    MachineSegmentSurface.from_curve_loop(
                        airgap_curve_loop,
                        symmetry,
                        "Stator Air",
                        material=air,
                        name="Stator Air (PyEMMO)",
                    )
                ]
            # create airgap
            airgap_curve_loop, _, _ = _create_band_contour(
                start_point, air_interface, -band_height, symmetry
            )
            surface_dict[STATOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface.from_curve_loop(
                    airgap_curve_loop,
                    symmetry,
                    STATOR_AIRGAP_IDEXT,
                    material=air,
                    name="Stator Airgap (PyEMMO)",
                )
            ]
        else:
            # if symmetry = 1 -> create a surface from the interface and subtract a circle
            if nbr_airgaps == 2:
                r_max = r_max - band_height  # reset for airgap creation
                air_area, air_interface = _create_band_surf(air_interface, r_max)
                surface_dict["Stator Air"] = [
                    MachineSegmentSurface(
                        tag=air_area.id,
                        nbr_segments=1,
                        part_id="Stator Air",
                        material=air,
                        name="Stator Air (PyEMMO)",
                    )
                ]
            airgap, _ = _create_band_surf(air_interface, r_max - band_height)
            surface_dict[STATOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface(
                    part_id=STATOR_AIRGAP_IDEXT,
                    nbr_segments=1,
                    tag=airgap.id,
                    material=air,
                    name="Stator Airgap (PyEMMO)",
                )
            ]
        # set airgap mesh size
        surface_dict[STATOR_AIRGAP_IDEXT][0].setMeshLength(band_height)
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG - 1:
            gmsh.model.occ.synchronize()
            gmsh.fltk.run()
    if not ROTOR_AIRGAP_IDEXT in surface_dict:
        # create rotor airgap
        logging.info(
            "Starting rotor airgap creation since no airgap was given by the input dict."
        )
        # filter boundary lines and remove boundaries on symmetry axis
        bound_lines = boundary.get_boundary_line_list(rotor_dim_tags)
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility(gmsh.model.getEntities(), False)
            gmsh.model.setVisibility(get_dim_tags(bound_lines), True, False)
            gmsh.fltk.run()
        if symmetry > 1:
            # if symmetry remove boundary lines on sym-axis
            [
                bound_lines.remove(line)
                for line in filter_lines_at_angle(bound_lines, 0)
                + filter_lines_at_angle(bound_lines, 2 * np.pi / symmetry)
            ]
            if logging.getLogger().getEffectiveLevel() <= logging.DEBUG - 1:
                gmsh.model.setVisibility(gmsh.model.getEntities(), False)
                gmsh.model.setVisibility(get_dim_tags(bound_lines), True, False)
                # for curve in bound_lines:
                #     print(f"{curve}: {curve.id}")
                gmsh.fltk.run()

        # identify point on x-axis with maximal radius
        start_point = None
        start_curve = None
        for curve in bound_lines:
            for point in curve.points:
                if np.isclose(point.y, 0, atol=DEFAULT_GEO_TOL):
                    if start_point is None or start_point.x < point.x:
                        start_point = point
                        start_curve = curve
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility([(0, start_point.id)], True)
            gmsh.option.setNumber("Geometry.PointNumbers", 1)
            gmsh.fltk.run()
            gmsh.option.setNumber("Geometry.PointNumbers", 0)  # show point off

        # get all lines adjacent to the start point
        air_interface = [bound_lines.pop(bound_lines.index(start_curve))]
        while True:
            found_curve = False
            for i, curve in enumerate(bound_lines):
                if (
                    start_curve.start_point in curve.points
                    or start_curve.end_point in curve.points
                ):
                    air_interface.append(bound_lines.pop(i))
                    start_curve = curve  # reset start curve for next interation
                    found_curve = True
                    break  # restart for loop
            if not found_curve:
                break
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            gmsh.model.setVisibility(gmsh.model.getEntities(), False)
            gmsh.model.setVisibility(get_dim_tags(air_interface), True)
            gmsh.fltk.run()

        # check if airgap interface is smooth (only arcs with same radius) to determine
        # if 1 or 2 airgaps should be created
        nbr_airgaps = 1
        try:
            interface_radius = air_interface[0].radius
            for curve in air_interface[1:]:
                if not np.isclose(curve.radius, interface_radius):
                    nbr_airgaps = 2  # create two airgap surfaces
                    break
        except AttributeError:
            nbr_airgaps = 2  # curve is straigt -> 2
        if nbr_airgaps not in (1, 2):
            raise ValueError("Number of airgaps must be 1 or 2")

        # calculate airgap radii
        r_max = get_max_radius(get_dim_tags(air_interface))
        # divide distance of rotor moving band in 2 or 3 segments
        band_height = (moving_band_radius - r_max) / nbr_airgaps
        if symmetry > 1:
            if nbr_airgaps == 2:
                # create air closing box
                airgap_curve_loop, air_interface, start_point = _create_band_contour(
                    start_point,
                    air_interface,
                    r_max - start_point.x + band_height,
                    symmetry,
                )
                surface_dict["Rotor Air"] = [
                    MachineSegmentSurface.from_curve_loop(
                        airgap_curve_loop,
                        symmetry,
                        "Rotor",
                        material=air,
                        name="Rotor Air (PyEMMO)",
                    )
                ]
            # create airgap
            airgap_curve_loop, _, _ = _create_band_contour(
                start_point, air_interface, band_height, symmetry
            )
            surface_dict[ROTOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface.from_curve_loop(
                    airgap_curve_loop,
                    symmetry,
                    ROTOR_AIRGAP_IDEXT,
                    material=air,
                    name="Rotor Airgap (PyEMMO)",
                )
            ]
        else:
            # if symmetry = 1 -> create a surface from the interface and subtract a circle
            if nbr_airgaps == 2:
                air_area, air_interface = _create_band_surf(
                    air_interface, r_max + band_height
                )
                r_max = r_max + band_height  # reset r_max for airgap
                surface_dict["Rotor Air"] = [
                    MachineSegmentSurface(
                        tag=air_area.id,
                        nbr_segments=1,
                        part_id="Rotor Air",
                        material=air,
                        name="Rotor Air (PyEMMO)",
                    )
                ]
            airgap, _ = _create_band_surf(air_interface, r_max + band_height)
            surface_dict[ROTOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface(
                    part_id=ROTOR_AIRGAP_IDEXT,
                    nbr_segments=1,
                    tag=airgap.id,
                    material=air,
                    name="Rotor Airgap (PyEMMO)",
                )
            ]
        surface_dict[ROTOR_AIRGAP_IDEXT][0].setMeshLength(band_height)
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG - 1:
            gmsh.model.occ.synchronize()
            gmsh.fltk.run()


def _create_band_contour(
    start_point: GmshPoint,
    interface: list[GmshLine, GmshArc],
    band_height: float,
    symmetry: int,
) -> tuple[list[GmshLine | GmshArc], list[GmshLine | GmshArc], GmshPoint]:
    """Refactored function to create band contour (curve loop) for symmetry != 1 to then
    create airgap surface in :func:`create_airgap_surfaces`

    Args:
        start_point (GmshPoint): Start point of interface in x-axis
        interface (list[GmshLine, GmshArc]): list of interface curves for the band.
        band_height (float): Requested band height. Must be negative if the the interface
            is outside and band should be created radially inwards.
        symmetry (int): Symmetry factor

    Raises:
        ValueError: If symmetry factor is < 2.
        RuntimeError: If final interface line found does not contain boundary point on
            symmetry axis (at angle 2*pi/sym).

    Returns:
        tuple[list[GmshLine|GmshArc], list[GmshLine|GmshArc], GmshPoint]: Curve loop
        to create airgap band surface, new interface line list and new start point of
        contour on x-axis.
    """
    center = get_global_center()  # get or create center point at (0,0)
    if symmetry <= 1:
        raise ValueError("Symmetry factor must be greater than 1!")
    sym_angle = 2 * np.pi / symmetry
    # create air closing box
    p1 = start_point
    # copy and move start point on x-axis by band height
    p2 = start_point.duplicate()
    p2.translate(dx=band_height)
    new_start_point = p2  # next interface start point
    # copy p2 and rotate result by symmetry angle
    p3 = p2.duplicate()
    p3.rotateZ(angle=sym_angle)
    # find end point from interface. Last element should be last curve!
    if np.isclose(interface[-1].end_point.getAngleToX(), sym_angle):
        p4 = interface[-1].end_point
    elif np.isclose(interface[-1].start_point.getAngleToX(), sym_angle):
        p4 = interface[-1].start_point
    else:
        raise RuntimeError(
            "Could not create airgap surface because none of the last "
            "interface curve points is on the symmetry axis."
        )
    airgap_curve_loop = interface
    airgap_curve_loop.append(GmshLine.from_points(p1, p2, "L_air_area_1"))
    if symmetry in (2, 3):
        # if symmetry is 2 or 3 -> create intermediate point to enforce arc export
        p_intermediate = p2.duplicate()
        p_intermediate.rotateZ(angle=sym_angle / 2)
        new_interface = [
            GmshArc.from_points(p2, center, p_intermediate, "C_air_area_2_1"),
            GmshArc.from_points(p_intermediate, center, p3, "C_air_area_2_2"),
        ]
    else:
        new_interface = [GmshArc.from_points(p2, center, p3, "C_air_area_2")]
    airgap_curve_loop.extend(new_interface)
    airgap_curve_loop.append(GmshLine.from_points(p3, p4, "L_air_area_3"))
    return airgap_curve_loop, new_interface, new_start_point


def _create_band_surf(
    interface: list[GmshLine], r_circ: float
) -> tuple[GmshSurface, list[GmshLine]]:
    """Special refactored function like :func:`_create_band_contour` but for symmetry=1.
    This function creates a circle surface using :func:`create_disk` at :attr:`r_circ` and
    a second surface from the given :attr:`interface` curve loop. Then it creates the airgap
    surface by subtracting the circle from the interface surface or the other way around
    depending on if the interface is radially below or above r_circ.

    Args:
        interface (list[GmshLine]): Interface curve loop. For sym=1 this list forms a
            closed boundary.
        r_circ (float): Radius of outer/inner band interface.

    Returns:
        tuple[GmshSurface, list[GmshLine]]: Created airgap surface and new outer/inner
        interface line list.
    """
    interface_surface = GmshSurface.from_curve_loop(
        curve_loop=interface, name="interface surface"
    )
    new_interface = create_disk(r_circ)
    circle = GmshSurface.from_curve_loop(new_interface, "air circle")
    if interface[0].start_point.radius > r_circ:
        # interface is outer so disk is tool
        interface_surface.cutOut(circle, keepTool=False)  # cut out circle and
        return interface_surface, new_interface
    # interface is inner so disk is air surface
    circle.cutOut(interface_surface, False)
    return circle, new_interface
