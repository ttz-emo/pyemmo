"""Import of pi"""
from numpy import pi


def getMagnetizationDict(
    magnetizationDict: dict, idExt: str, anglePointRef: float, magnetizationType: int
) -> dict:
    """Get the magnetization dict with the magnet and the magnetization angle.

    Args:
        magnetizationDict (dict): Dict with magnet corresponding magnetization angle
        idExt (str): IdExt of the surface
        anglePointRef (float): Angle of the pointRef
        magnetizationType (int): 0: radial | 1: parallel | 3: tangential

    Returns:
        dict: magnetizationDict with magnet and corresponding magnetization angle
    """
    if magnetizationType in (0, 1):  # radial & parallel
        magnetizationAngle = anglePointRef

    elif magnetizationType == 3:  # tangential
        magnetizationAngle = anglePointRef - 90 / pi

    magnetizationDict[idExt] = magnetizationAngle

    return magnetizationDict
