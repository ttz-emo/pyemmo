#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
Module: create_gmsh_surface

This module provides functions for translating surfaces from pyleecan format to
pyemmo format.

Functions:
    -   ``create_gmsh_surface``: Translates pyleecan surfaces into pyemmo surfaces.
"""

from __future__ import annotations

from pyleecan.Classes.SurfLine import SurfLine

from ...api.machine_segment_surface import MachineSegmentSurface
from ...script.gmsh.gmsh_line import GmshLine
from ...script.material import Material
from .create_gmsh_lines import create_gmsh_lines


def create_gmsh_surface(
    surface: SurfLine,
    nbr_segments: int,
    part_id: str,
    material: Material,
    name: str = "",
) -> MachineSegmentSurface:
    """
    Translates Pyleecan SurfLine surfaces into pyemmo GmshSurface objects.

    Args:
        surface (pyleecan.Classes.SurfLine.SurfLine): Pyleecan surface.

    Returns:
        GmshSurface: PyEMMO surface in Gmsh.
    """
    if not isinstance(surface, SurfLine):
        raise TypeError(f"Surface must be of type SurfLine, got {type(surface)}")
    # create line loop:
    curves: list[GmshLine] = create_gmsh_lines(surface.get_lines())
    # create gmsh surface
    # FIXME: The line list of a pyleecan surface does not have to be closed. This
    # happens for example in case of holes on the boundary of a surface. In this case,
    # the curve loop is open at the part where the hole intersects.
    pyemmo_surf = MachineSegmentSurface.from_curve_loop(
        curves, nbr_segments, part_id, material, name=name
    )
    return pyemmo_surf
