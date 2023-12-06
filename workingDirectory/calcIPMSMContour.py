import math
from typing import Union

from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.functions.plot import plot


def calcIPMSMRotorContour(
    rotorLamSurfList: list[SurfaceAPI],
    radius: float,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Calculation for the rotor contour of an IPMSM machine.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        radius (float): Pyleecan machine

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: _description_
    """

    rotorContourLineList = []

    # --------------------------------------------
    # Filtering the lines that lie at the air gap:
    # --------------------------------------------
    # rotor lamination:
    for curve in rotorLamSurfList[0].curve:
        if not (
            math.isclose(a=curve.startPoint.radius, b=radius, abs_tol=1e-6)
        ) and not math.isclose(
            a=curve.endPoint.radius, b=radius, abs_tol=1e-6
        ):
            rotorContourLineList.append(curve)
    print("---")
    print("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotorContourLineList, linewidth=1, markersize=3)
    print("---")

    for point in rotorContourLineList[0].points:
        if math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6):
            lowestYPointRotor = point
        else:
            biggestYPointRotor = point

    return rotorContourLineList, lowestYPointRotor, biggestYPointRotor
