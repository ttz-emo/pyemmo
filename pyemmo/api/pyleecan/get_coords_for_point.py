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
import math


def get_x_for_point(radius: float, angle: float) -> float:
    """Get the x-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: ``x``: x-coordinate of point
    """
    x = radius * math.cos(angle)
    return x


def get_y_for_point(radius: float, angle: float) -> float:
    """Get the y-coordinate of the Point.

    Args:
        radius (float): radius of band
        angle (float): angle of rotor segment

    Returns:
        float: ``y``: y-coordinate of point
    """
    y = radius * math.sin(angle)
    return y
