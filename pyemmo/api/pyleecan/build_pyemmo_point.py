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
This module provides functions for translating points between different geometric libraries.

Functions:
    -   ``build_pyemmo_point``: Translates the coordinates of a point in pyleecan
        into a pyemmo point.

Classes:
    ``Point``: Represents a point in 3D space.

"""

from __future__ import annotations

from ...script.geometry.point import Point


def build_pyemmo_point(pyleecan_point: complex) -> Point:
    """Translates the coordinates of a point in pyleecan into a pyemmo point.

    Args:
        pyleecanPoint (complex): coordinates of the pyleecan point

    Returns:
        Point: pyemmoPoint: pyemmo point
    """
    coords = [pyleecan_point.real, pyleecan_point.imag]

    pyemmo_point = Point(
        name="point_pylc", x=coords[0], y=coords[1], z=0, meshLength=1e-3
    )

    return pyemmo_point
