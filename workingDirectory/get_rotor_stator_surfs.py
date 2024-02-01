import logging
from pyemmo.api.SurfaceJSON import SurfaceAPI


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
        if surf.idExt in ("Pol","Mag", "Mag0", "Mag1", "Mag2"):
            if surf.idExt == "Pol":
                rotor_lam_surf_list.append(surf)
                logging.debug("rotorLamSurf:")
            elif surf.idExt in ("Mag","Mag0", "Mag1", "Mag2"):
                rotor_mag_surf_list.append(surf)
                logging.debug("rotorMagSurf:")

            logging.debug("gefunden: %s", {surf.name})

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
            logging.debug("statorLamSurf:")
            logging.debug("gefunden: %s", {surf.name})

    return stator_lam_surf_list
