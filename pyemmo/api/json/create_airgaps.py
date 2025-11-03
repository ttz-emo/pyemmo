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
"""Module for function ``create_airgap_surfaces`` - if no airgaps given with the
segmented input, create it by extracting the inner/outer boundary of stator/rotor."""

from __future__ import annotations

import gmsh
import numpy as np

from ...definitions import DEFAULT_GEO_TOL
from ...script.gmsh.gmsh_arc import GmshArc
from ...script.gmsh.gmsh_line import GmshLine
from ...script.gmsh.gmsh_point import GmshPoint
from ...script.gmsh.utils import (
    filter_lines_at_angle,
    get_dim_tags,
    get_max_radius,
    get_min_radius,
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
    if STATOR_AIRGAP_IDEXT in surface_dict and ROTOR_AIRGAP_IDEXT in surface_dict:
        return
    rotor_dim_tags, stator_dim_tags = boundary.get_rotor_stator_dim_tags(
        surface_dict, moving_band_radius
    )
    if not STATOR_AIRGAP_IDEXT in surface_dict:
        # create stator airgap
        # filter boundary lines and remove boundaries on symmetry axis
        bound_lines = boundary.get_boundary_line_list(stator_dim_tags)
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
        gmsh.model.setVisibility([(0, start_point.id)], True)
        gmsh.option.setNumber("Geometry.PointNumbers", 1)
        gmsh.fltk.run()

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

        # calculate airgap radii
        r_max = get_min_radius(stator_dim_tags)
        # divide distance of rotor moving band in 2 or 3 segments
        band_height = (r_max - moving_band_radius) / (nbr_airgaps + 1)
        if symmetry > 1:
            if nbr_airgaps not in (1, 2):
                raise ValueError("Number of airgaps must be 1 or 2")
            sym_angle = 2 * np.pi / symmetry
            center = GmshPoint.from_coordinates((0, 0), name="CenterPoint")
            if nbr_airgaps == 2:
                # create air closing box
                p1 = start_point
                # copy and move start point on x-axis by band height
                p2 = start_point.duplicate()
                p2.translate(dx=-band_height)
                # copy p2 and rotate result by symmetry angle
                p3 = p2.duplicate()
                p3.rotateZ(angle=sym_angle)
                # find end point from interface. Last element should be last curve!
                if np.isclose(air_interface[-1].end_point.getAngleToX(), sym_angle):
                    p4 = air_interface[-1].end_point
                elif np.isclose(air_interface[-1].start_point.getAngleToX(), sym_angle):
                    p4 = air_interface[-1].start_point
                else:
                    raise RuntimeError(
                        "Could not create airgap surface because none of the last "
                        "interface curve points is on the symmetry axis."
                    )
                l1 = GmshLine.from_points(p1, p2, "L_air_area_1")
                l2 = GmshArc.from_points(p2, center, p3, "C_air_area_2")
                l3 = GmshLine.from_points(p3, p4, "L_air_area_3")
                airgap_curve_loop = [l1, l2, l3]
                airgap_curve_loop.extend(air_interface)
                surface_dict["Stator Air"] = [
                    MachineSegmentSurface.from_curve_loop(
                        airgap_curve_loop,
                        symmetry,
                        "Stator Air",
                        material=air,
                        name="Stator Air (PyEMMO)",
                    )
                ]
                gmsh.model.occ.synchronize()
                gmsh.fltk.run()
                # set startpoint and interface curve for final airgap
                start_point = p2
                air_interface = [l2]
            # create airgap
            p1 = start_point
            # copy and move start point on x-axis by band height
            p2 = start_point.duplicate()
            p2.translate(dx=-band_height)
            # copy p2 and rotate result by symmetry angle
            p3 = p2.duplicate()
            p3.rotateZ(angle=sym_angle)
            # find end point from interface. Last element should be last curve!
            if np.isclose(air_interface[-1].end_point.getAngleToX(), sym_angle):
                p4 = air_interface[-1].end_point
            elif np.isclose(air_interface[-1].start_point.getAngleToX(), sym_angle):
                p4 = air_interface[-1].start_point
            else:
                raise RuntimeError(
                    "Could not create airgap surface because none of the last "
                    "interface curve points is on the symmetry axis."
                )
            l1 = GmshLine.from_points(p1, p2, "L_airgap_1")
            l2 = GmshArc.from_points(p2, center, p3, "C_airgap_2")
            l3 = GmshLine.from_points(p3, p4, "L_airgap_3")
            airgap_curve_loop = [l1, l2, l3]
            airgap_curve_loop.extend(air_interface)
            surface_dict[STATOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface.from_curve_loop(
                    airgap_curve_loop,
                    symmetry,
                    STATOR_AIRGAP_IDEXT,
                    material=air,
                    name="Stator Airgap (PyEMMO)",
                )
            ]
            surface_dict[STATOR_AIRGAP_IDEXT][0].setMeshLength(band_height)
        else:
            raise NotImplementedError(
                "Cannot create airgap surfaces for symmetry = 1 yet."
            )
    if not ROTOR_AIRGAP_IDEXT in surface_dict:
        # create rotor airgap
        # filter boundary lines and remove boundaries on symmetry axis
        bound_lines = boundary.get_boundary_line_list(rotor_dim_tags)
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
        gmsh.model.setVisibility([(0, start_point.id)], True)
        gmsh.option.setNumber("Geometry.PointNumbers", 1)
        gmsh.fltk.run()

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

        # calculate airgap radii
        r_max = get_max_radius(get_dim_tags(air_interface))
        # divide distance of rotor moving band in 2 or 3 segments
        band_height = (moving_band_radius - r_max) / nbr_airgaps
        if symmetry > 1:
            if nbr_airgaps not in (1, 2):
                raise ValueError("Number of airgaps must be 1 or 2")
            sym_angle = 2 * np.pi / symmetry
            center = GmshPoint.from_coordinates((0, 0), name="CenterPoint")
            if nbr_airgaps == 2:
                # create air closing box
                p1 = start_point
                # copy and move start point on x-axis by band height
                p2 = start_point.duplicate()
                p2.translate(dx=band_height)
                # copy p2 and rotate result by symmetry angle
                p3 = p2.duplicate()
                p3.rotateZ(angle=sym_angle)
                # find end point from interface. Last element should be last curve!
                if np.isclose(air_interface[-1].end_point.getAngleToX(), sym_angle):
                    p4 = air_interface[-1].end_point
                elif np.isclose(air_interface[-1].start_point.getAngleToX(), sym_angle):
                    p4 = air_interface[-1].start_point
                else:
                    raise RuntimeError(
                        "Could not create airgap surface because none of the last "
                        "interface curve points is on the symmetry axis."
                    )
                l1 = GmshLine.from_points(p1, p2, "L_air_area_1")
                l2 = GmshArc.from_points(p2, center, p3, "C_air_area_2")
                l3 = GmshLine.from_points(p3, p4, "L_air_area_3")
                airgap_curve_loop = [l1, l2, l3]
                airgap_curve_loop.extend(air_interface)
                surface_dict["Rotor Air"] = [
                    MachineSegmentSurface.from_curve_loop(
                        airgap_curve_loop,
                        symmetry,
                        "Rotor",
                        material=air,
                        name="Rotor Air (PyEMMO)",
                    )
                ]
                gmsh.model.occ.synchronize()
                gmsh.fltk.run()
                # set startpoint and interface curve for final airgap
                start_point = p2
                air_interface = [l2]
            # create airgap
            p1 = start_point
            # copy and move start point on x-axis by band height
            p2 = start_point.duplicate()
            p2.translate(dx=band_height)
            # copy p2 and rotate result by symmetry angle
            p3 = p2.duplicate()
            p3.rotateZ(angle=sym_angle)
            # find end point from interface. Last element should be last curve!
            if np.isclose(air_interface[-1].end_point.getAngleToX(), sym_angle):
                p4 = air_interface[-1].end_point
            elif np.isclose(air_interface[-1].start_point.getAngleToX(), sym_angle):
                p4 = air_interface[-1].start_point
            else:
                raise RuntimeError(
                    "Could not create airgap surface because none of the last "
                    "interface curve points is on the symmetry axis."
                )
            l1 = GmshLine.from_points(p1, p2, "L_airgap_1")
            l2 = GmshArc.from_points(p2, center, p3, "C_airgap_2")
            l3 = GmshLine.from_points(p3, p4, "L_airgap_3")
            airgap_curve_loop = [l1, l2, l3]
            airgap_curve_loop.extend(air_interface)
            surface_dict[ROTOR_AIRGAP_IDEXT] = [
                MachineSegmentSurface.from_curve_loop(
                    airgap_curve_loop,
                    symmetry,
                    ROTOR_AIRGAP_IDEXT,
                    material=air,
                    name="Rotor Airgap (PyEMMO)",
                )
            ]
            surface_dict[ROTOR_AIRGAP_IDEXT][0].setMeshLength(band_height)
