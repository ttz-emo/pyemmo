import logging
from pyemmo.api.SurfaceJSON import SurfaceAPI


def getRotorSurfaces(
    geometryList: list[SurfaceAPI],
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
    rotorLamSurfList = []
    rotorMagSurfList = []

    for surf in geometryList:
        if surf.idExt == "Pol":
            rotorLamSurfList.append(surf)
            logging.debug("rotorLamSurf:")
            logging.debug(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag0":
            rotorMagSurfList.append(surf)
            logging.debug("rotorMagSurf:")
            logging.debug(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag1":
            rotorMagSurfList.append(surf)
            logging.debug("rotorMagSurf:")
            logging.debug(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag2":
            rotorMagSurfList.append(surf)
            logging.debug("rotorMagSurf:")
            logging.debug(f"gefunden: {surf.name}")

    return rotorLamSurfList, rotorMagSurfList


def getStatorSurfaces(
    geometryList: list[SurfaceAPI],
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
    statorLamSurfList = []
    statorWindSurfList = []

    for surf in geometryList:
        if surf.idExt == "StNut":
            statorLamSurfList.append(surf)
            logging.debug("statorLamSurf:")
            logging.debug(f"gefunden: {surf.name}")

    return statorLamSurfList
