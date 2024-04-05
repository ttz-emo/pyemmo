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
from ..json.SurfaceJSON import SurfaceAPI
from .. import logger


def get_rotor_surfs(
    geometry_list: list[SurfaceAPI],
) -> tuple[list[SurfaceAPI], list[SurfaceAPI]]:
    """Get the surfaces of the rotor.

    Args:
        geometryList (list[SurfaceAPI]): list with all surfaces of the machine in pyemmo format

    Returns:
        tuple[list[SurfaceAPI], list[SurfaceAPI]]: _description_
    """
    # =========================================
    # Zuweisung der Surfaces zu den Kategorien:
    # =========================================
    rotor_lam_surf_list = []
    rotor_mag_surf_list = []

    for surf in geometry_list:
        if surf.idExt in ("Pol", "Mag", "Mag0", "Mag1", "Mag2"):
            if surf.idExt == "Pol":
                rotor_lam_surf_list.append(surf)
                logger.debug("rotorLamSurf:")
            elif surf.idExt in ("Mag", "Mag0", "Mag1", "Mag2"):
                rotor_mag_surf_list.append(surf)
                logger.debug("rotorMagSurf:")

            logger.debug("gefunden: %s", {surf.name})

    return rotor_lam_surf_list, rotor_mag_surf_list


def get_stator_surfs(
    geometry_list: list[SurfaceAPI],
) -> list[SurfaceAPI]:
    """Get the surface of the stator lamination.

    Args:
        geometryList (list[SurfaceAPI]): list with all surfaces of the machine in pyemmo format

    Returns:
        list[SurfaceAPI]: _description_
    """
    # =========================================
    # Zuweisung der Surfaces zu den Kategorien:
    # =========================================
    stator_lam_surf_list = []
    # statorWindSurfList = []

    for surf in geometry_list:
        if surf.idExt == "StNut":
            stator_lam_surf_list.append(surf)
            logger.debug("statorLamSurf:")
            logger.debug("gefunden: %s", {surf.name})

    return stator_lam_surf_list
