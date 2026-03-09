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
"""Module to transform coordinates between systems:

- Cartesian XYZ
- Polar RPhiZ
- RadTanZ
"""
from __future__ import annotations

import math as m

import numpy as np


def cart2pol(x, y) -> tuple[float, float]:
    """Cartesian XY to Polar R - Phi

    Args:
        x (float): x-coordinate of cartesian point
        y (float): y-coordinate of cartesian point

    Returns:
        tuple[float, float]: R and Phi of polar equivalent
    """
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho, phi):
    """Polar rPhi to cartesian XY

    Args:
        rho (number): Radius of polar coordinate in meter
        phi (number): Angle of polar coordinate in rad

    Returns:
        tuple[float, float]: XY coordinates.
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def cart2sph(x, y, z=0.0) -> tuple[float, float, float]:
    """Transform cartesian coordinates to spherical.

    Args:
        x (float): x-coordinate of cartesian point
        y (float): y-coordinate of cartesian point
        z (float, optional): z-coordinate of cartesian point. Defaults to 0.0

    Returns:
        tuple[float, float, float]: Radius, elevation angle :math:`\\theta` and azimuthal angle :math:`\\phi`
    """
    XsqPlusYsq = x**2 + y**2
    r = m.sqrt(XsqPlusYsq + z**2)  # r
    elev = m.atan2(z, m.sqrt(XsqPlusYsq))  # theta
    az = m.atan2(y, x)  # phi
    return r, elev, az


def cart2sphA(points: np.ndarray) -> np.ndarray:
    """cartesian to spherical coordinates for array of points x,y,z.
    This uses function :func:`cart2sph`

    Args:
        points (np.ndarray): input array of cartesian points with coords x,y,z.

    Returns:
        np.ndarray: Array of spherical points.
    """
    return np.array([cart2sph(x, y, z) for x, y, z in points])
