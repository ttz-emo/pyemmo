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
Rotor and Stator Surfaces Module

This module provides functions to extract rotor and stator surfaces from the
geometry of an electric machine.

Functions:
    -   ``get_rotor_surfs``: Extracts rotor surfaces from the machine geometry.
    -   ``get_stator_surfs``: Extracts stator surfaces from the machine geometry.
"""

from __future__ import annotations

import re

from .. import logger
from ..json import ROTOR_LAM_IDEXT, ROTOR_MAG_IDEXT
from ..json.SurfaceJSON import SurfaceAPI


def get_rotor_surfs(
    geometry_list: list[SurfaceAPI],
) -> tuple[list[SurfaceAPI], list[SurfaceAPI]]:
    """
    Get the surfaces of the rotor.

    Args:
        geometry_list (list[SurfaceAPI]): List with all surfaces of the machine
            in PyEMMO format (= SurfaceAPI).

    Returns:
        tuple[list[SurfaceAPI], list[SurfaceAPI]]: Tuple containing lists of
        rotor lamination surfaces and rotor magnet surfaces.
    """
    # Assignment of surfaces to categories
    rotor_lam_surf_list = []
    rotor_mag_surf_list = []

    for surf in geometry_list:
        # FIXME:
        pattern = rf"\b({ROTOR_LAM_IDEXT}|{ROTOR_MAG_IDEXT}|{ROTOR_MAG_IDEXT}\d+)\b"
        re.findall(pattern, surf.idExt)
        if re.findall(pattern, surf.idExt):
            if surf.idExt == ROTOR_LAM_IDEXT:
                rotor_lam_surf_list.append(surf)
                logger.debug("rotorLamSurf:")
            elif ROTOR_MAG_IDEXT in surf.idExt:
                rotor_mag_surf_list.append(surf)
                logger.debug("rotorMagSurf:")
            else:
                raise RuntimeError()
            logger.debug("found: %s", {surf.name})

    return rotor_lam_surf_list, rotor_mag_surf_list


def get_stator_surfs(
    geometry_list: list[SurfaceAPI],
) -> list[SurfaceAPI]:
    """
    Get the surface of the stator lamination.

    Args:
        geometry_list (list[SurfaceAPI]): List with all surfaces of the machine
            in PyEMMO format.

    Returns:
        list[SurfaceAPI]: List of stator lamination surfaces.
    """
    # Assignment of surfaces to categories
    stator_lam_surf_list = []
    # statorWindSurfList = []

    for surf in geometry_list:
        if surf.idExt == "StNut":
            stator_lam_surf_list.append(surf)
            logger.debug("statorLamSurf:")
            logger.debug("found: %s", {surf.name})

    return stator_lam_surf_list
