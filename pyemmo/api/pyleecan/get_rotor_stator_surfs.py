"""
Rotor and Stator Surfaces Module

This module provides functions to extract rotor and stator surfaces from the geometry of an electric machine.

Functions:
- get_rotor_surfs: Extracts rotor surfaces from the machine geometry.
- get_stator_surfs: Extracts stator surfaces from the machine geometry.

Classes:
None

"""

from ..json.SurfaceJSON import SurfaceAPI
from .. import logger


def get_rotor_surfs(
    geometry_list: list[SurfaceAPI],
) -> tuple[list[SurfaceAPI], list[SurfaceAPI]]:
    """
    Get the surfaces of the rotor.

    Args:
        geometry_list (list[SurfaceAPI]): List with all surfaces of the machine in pyemmo format.

    Returns:
        tuple[list[SurfaceAPI], list[SurfaceAPI]]: Tuple containing lists of rotor lamination surfaces and rotor magnet surfaces.
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
    """
    Get the surface of the stator lamination.

    Args:
        geometry_list (list[SurfaceAPI]): List with all surfaces of the machine in pyemmo format.

    Returns:
        list[SurfaceAPI]: List of stator lamination surfaces.
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
