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
"""detect_inner_outer_limit Module

This module provides a function to detect and label the most inner and outer
curves of the machine geometry.

Functions:
    -   detect_inner_outer_limit: Detects and labels the most inner and outer
        curves of the machine geometry.
"""

from __future__ import annotations

import math

from ..json.SurfaceJSON import SurfaceAPI


def detect_inner_outer_limit(
    geometry_list: list[SurfaceAPI],
    inner_radius: float,
    outer_radius: float,
    has_shaft: bool,
) -> list[SurfaceAPI]:
    """Detects and labels the most inner and outer curves of the machine geometry.

    Overwrites the name of the curve to "InnerLimit" if it is the most inner curve,
    and to "OuterLimit" if it is the most outer curve.

    Attention when making the function call:\n
    If the machine has an **outer rotor**:\n
    ``inner_radius``: ``rotorRint`` or ``statorRint``\n
    ``outer_radius``: ``statorRext`` or ``rotorRext``\n

    Combinations that work:

        - ``rotorRint`` and ``statorRext``
        - ``statorRint`` and ``rotorRext``

    Args:
        geometry_list (list[SurfaceAPI]): List of the machine surfaces.
        inner_radius (float): Inner radius of the machine.
        outer_radius (float): Outer radius of the machine.
        has_shaft (bool): Indicates whether the machine has a shaft or not.

    Returns:
        list[SurfaceAPI]: Updated geometry list with curves labeled as
        "InnerLimit" or "OuterLimit".
    """
    for surf in geometry_list:
        for curve in surf.curve:
            if has_shaft:
                if math.isclose(
                    a=curve.startPoint.radius, b=inner_radius, abs_tol=1e-6
                ) and math.isclose(
                    a=curve.endPoint.radius, b=inner_radius, abs_tol=1e-6
                ):
                    curve.name = "InnerLimit"
            if math.isclose(
                a=curve.startPoint.radius, b=outer_radius, abs_tol=1e-6
            ) and math.isclose(a=curve.endPoint.radius, b=outer_radius, abs_tol=1e-6):
                curve.name = "OuterLimit"

    return geometry_list
