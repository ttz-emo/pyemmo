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
This module provides the function ``create_gmsh_surface`` which translates pyleecan
surfaces into pyemmo :class:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface`.
"""

from __future__ import annotations

from pyleecan.Classes.SurfLine import SurfLine

from ...api.machine_segment_surface import MachineSegmentSurface
from ...script.gmsh.gmsh_line import GmshLine
from ...script.material.material import Material
from .create_gmsh_lines import create_gmsh_lines
from .label2part_id import label2part_id


def create_gmsh_surface(
    surface: SurfLine,
    nbr_segments: int,
    material: Material,
    name: str = "",
) -> MachineSegmentSurface:
    """
    Translates Pyleecan SurfLine surfaces into pyemmo MachineSegmentSurface objects.

    Args:
        surface (pyleecan.Classes.SurfLine.SurfLine): Pyleecan surface.
        nbr_segments (int): Number of segments for the surface.
        material (Material): Material for the surface.
        name str: Optional name for the surface. Defaults to "".

    Returns:
        MachineSegmentSurface: PyEMMO machine segment surface in Gmsh.
    """
    if not hasattr(surface, "get_lines"):
        raise TypeError(
            f"Surface must have method 'get_lines', Surface type is: {type(surface)}"
        )
    assert hasattr(surface, "label") and isinstance(
        surface.label, str
    ), "Surface must have attribute 'label'"
    # create line loop:
    curves: list[GmshLine] = create_gmsh_lines(surface.get_lines())
    # create gmsh surface
    # FIXME: The line list of a pyleecan surface does not have to be closed. This
    # happens for example in case of holes on the boundary of a surface. In this case,
    # the curve loop is open at the part where the hole intersects.
    pyemmo_surf = MachineSegmentSurface.from_curve_loop(
        curves, nbr_segments, label2part_id(surface.label), material, name=name
    )
    return pyemmo_surf
