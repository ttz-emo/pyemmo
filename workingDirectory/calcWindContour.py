import math
from typing import Union

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from pyemmo.functions.plot import plot
from .getRotorStatorSurfaces import getStatorSurfaces


def calcWindContour(
    geometryList: list,
    statorRint: float,
    statorRext: float,
) -> list[Union[Line, CircleArc]]:
    """Calculation for the contour of a slot with winding.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        statorRint (float): Inner radius of stator
        statorRext (float): Outer radius of stator

    Returns:
        list[Union[Line, CircleArc]]: _description_
    """
    statorContourLineList = []
    statorLamSurfList = getStatorSurfaces(geometryList=geometryList)

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================

    # -----------------------------------------------------------
    # Aussortieren der Linien die nicht an der Oberfläche liegen:
    # -----------------------------------------------------------
    for curve in statorLamSurfList[0].curve:
        if (
            math.isclose(
                a=curve.startPoint.radius,
                b=statorRint,
                abs_tol=1e-6,
            )
            or math.isclose(
                a=curve.endPoint.radius,
                b=statorRint,
                abs_tol=1e-6,
            )
        ) and (
            math.isclose(
                a=curve.endPoint.radius,
                b=statorRext,
                abs_tol=1e-6,
            )
            is False
            and math.isclose(
                a=curve.startPoint.radius,
                b=statorRext,
                abs_tol=1e-6,
            )
            is False
        ):
            statorContourLineList.append(curve)

    statorLinePointList = []
    for curve in statorContourLineList:
        if (
            curve.startPoint.radius > statorRint or curve.startPoint.radius > statorRext
        ) and math.isclose(
            a=curve.startPoint.radius, b=statorRint, abs_tol=1e-6
        ) is False:
            statorLinePointList.append(curve.startPoint)
        elif (
            curve.endPoint.radius > statorRint or curve.endPoint.radius > statorRext
        ) and math.isclose(
            a=curve.endPoint.radius, b=statorRint, abs_tol=1e-6
        ) is False:
            statorLinePointList.append(curve.endPoint)

    centerPoint = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
    statorNewLine = CircleArc(
        name="windNewCircleArc",
        startPoint=statorLinePointList[0],
        endPoint=statorLinePointList[1],
        centerPoint=centerPoint,
    )
    statorContourLineList.append(statorNewLine)
    print("windContourLineList:")
    plot(statorContourLineList, linewidth=1, markersize=3, tag=True)
    print("---")
    return statorContourLineList
