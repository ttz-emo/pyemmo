import math
from pyemmo.script.geometry.point import Point

def calcIPMSMRotorContour(geometryList: list, radius: float) -> tuple[list, Point, Point]:
    """Calculation of the rotor contour of an IPMSM machine.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        radius (float): Pyleecan machine

    Returns:
        tuple[list, Point, Point]: _description_
    """
    rotorContourLineList = []
    for surf in geometryList:
        if surf.idExt == "Pol":
            rotorLamSurf = surf
    for curve in rotorLamSurf.curve:
        if math.isclose(
            a=curve.startPoint.radius, b=radius, abs_tol=1e-6
        ) and math.isclose(a=curve.endPoint.radius, b=radius, abs_tol=1e-6):
            rotorContourLineList.append(curve)
    for point in rotorContourLineList[0].points:
        if math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6):
            lowestYPointRotor = point
        else:
            biggestYPointRotor = point
    return rotorContourLineList, lowestYPointRotor, biggestYPointRotor
