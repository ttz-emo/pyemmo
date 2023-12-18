import math
import copy
import logging
from typing import Union

from pyleecan.Classes.Machine import Machine

from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.functions.plot import plot


def calcSPMSMContGenerally(
    machine: Machine,
    rotorLamSurfList: list[SurfaceAPI],
    rotorMagSurfList: list[SurfaceAPI],
    radius: float,
    isInternalRotor: bool,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """General calculations for creating the rotor contour: \n
    * Filtering the lines that lie on the air gap
    * Detecting the outer points of the rotor contour facing the air gap

    Args:
        machine (Machine): Pyleecan machine
        rotorLamSurfList (list[SurfaceAPI]): List of the pyemmo-surfaces of the rotor
        radius (float): Internal Rotor -> ``rotorRint`` | External Rotor -> ``rotorRext``
        isInternalRotor (bool): Internal or external rotor

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
    logging.debug("---")
    logging.debug("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotorContourLineList, linewidth=1, markersize=3)
    logging.debug("---")

    # --------------------------------------------
    # Filtering the outermost points of the rotor:
    # --------------------------------------------
    rPointRotorCont = Point("rPointRotorCont", x=0, y=0, z=0, meshLength=0)
    lPointRotorCont = Point("lPointRotorCont", x=0, y=0, z=0, meshLength=0)
    rotorSegAngle = 360 / machine.rotor.comp_periodicity_geo()[0]

    if math.isclose(a=rotorSegAngle, b=0, abs_tol=1e-6):
        rotorSegAngle = 180

    if isInternalRotor:
        for curve in rotorContourLineList:
            for point in curve.points:
                anglePoint = (
                    math.atan2(point.coordinate[1], point.coordinate[0])
                    / math.pi
                    * 180
                )
                if math.isclose(a=anglePoint, b=0, abs_tol=1e-6):
                    anglePoint = 180
                if (
                    math.isclose(a=anglePoint, b=rotorSegAngle, abs_tol=1e-6)
                    and point.radius <= machine.rotor.Rext
                    and point.radius >= machine.rotor.Rint
                ):
                    lPointRotorCont = point
                if (
                    math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6)
                    and point.coordinate[0] > radius
                ):
                    rPointRotorCont = point

    else:
        smallestPreviousXRotor = machine.rotor.Rext
        for curve in rotorContourLineList:
            for point in curve.points:
                if point.coordinate[0] < smallestPreviousXRotor:
                    smallestPreviousXRotor = point.coordinate[0]
                    lPointRotorCont = point

                if (
                    math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6)
                    and point.coordinate[0] > radius
                ):
                    rPointRotorCont = point

    for magSurf in rotorMagSurfList:
        rotorContourLineList.extend(magSurf.curve)

    return (
        rotorContourLineList,
        rPointRotorCont,
        lPointRotorCont,
    )


def calcSPMSMRotorContour(
    machine: Machine,
    rotorLamSurfList: list,
    rotorMagSurfList: list,
    radius: float,
    isInternalRotor: bool,
) -> tuple[list, Point, Point]:
    """_summary_

    Args:
        machine (Machine): _description_
        rotorLamSurfList (list): _description_
        rotorMagSurfList (list): _description_
        radius (float): _description_
        isInternalRotor (bool): _description_

    Returns:
        tuple[list, list, Point]: _description_
    """

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================
    (
        rotorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
    ) = calcSPMSMContGenerally(
        machine=machine,
        rotorLamSurfList=rotorLamSurfList,
        rotorMagSurfList=rotorMagSurfList,
        radius=radius,
        isInternalRotor=isInternalRotor,
    )

    # ----------------------------------------------
    # Aussortieren von doppelten Linien/Kreisboegen:
    # ----------------------------------------------
    rotorContourLineListCopy = copy.copy(rotorContourLineList)
    for rotorLamCurve in rotorContourLineListCopy:
        for rotorMagSurf in rotorMagSurfList:
            # Rotor-Lamination Curves
            for rotorMagCurve in rotorMagSurf.curve:
                # Rotor-Magnet Curves
                if (
                    math.isclose(
                        a=rotorMagCurve.startPoint.coordinate[0],
                        b=rotorLamCurve.endPoint.coordinate[0],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotorMagCurve.endPoint.coordinate[1],
                        b=rotorLamCurve.startPoint.coordinate[1],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotorMagCurve.endPoint.coordinate[0],
                        b=rotorLamCurve.startPoint.coordinate[0],
                        abs_tol=1e-6,
                    )
                    and math.isclose(
                        a=rotorMagCurve.endPoint.coordinate[1],
                        b=rotorLamCurve.startPoint.coordinate[1],
                        abs_tol=1e-6,
                    )
                ):
                    logging.debug("gefiltert: %s", rotorLamCurve)
                    logging.debug("gefiltert: %s", rotorMagCurve)
                    rotorContourLineList.remove(rotorLamCurve)
                    rotorContourLineList.remove(rotorMagCurve)
                    # plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)

    logging.debug("Plot contourLineList ")
    plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)
    logging.debug("---")

    return rotorContourLineList, lowestYPointRotor, biggestYPointRotor
