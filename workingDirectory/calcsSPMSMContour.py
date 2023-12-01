import math
import copy

from pyleecan.Classes.Machine import Machine

from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.point import Point
from pyemmo.functions.plot import plot


def calcSPMSMContGenerally(
    machine: Machine,
    rotorLamSurfList: list[SurfaceAPI],
    rotorMagSurfList: list[SurfaceAPI],
    radius: float,
    isInternalRotor: bool,
) -> tuple[list, list, Point, Point]:
    """General calculations for creating the rotor contour: \n
    * Filtering the lines that lie on the air gap
    * Detecting the outer points of the rotor contour facing the air gap

    Args:
        machine (Machine): Pyleecan machine
        rotorLamSurfList (list[SurfaceAPI]): List of the pyemmo-surfaces of the rotor
        radius (float): Internal Rotor -> ``rotorRint`` | External Rotor -> ``rotorRext``
        isInternalRotor (bool): Internal or external rotor

    Returns:
        _type_: _description_
    """
    rotorContourLineList = []
    # --------------------------------------------
    # Filtering the lines that lie at the air gap:
    # --------------------------------------------
    # rotor lamination:
    for curve in rotorLamSurfList[0].curve:
        if not (
            math.isclose(a=curve.startPoint.radius, b=radius, abs_tol=1e-6)
        ) and not math.isclose(a=curve.endPoint.radius, b=radius, abs_tol=1e-6):
            rotorContourLineList.append(curve)
    print("---")
    print("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotorContourLineList, linewidth=1, markersize=3)
    print("---")

    # --------------------------------------------
    # Filtering the outermost points of the rotor:
    # --------------------------------------------
    lowestYPointRotor = Point("lowestYPointRotor", x=0, y=0, z=0, meshLength=0)
    biggestYPointRotor = Point("biggestYPointRotor", x=0, y=0, z=0, meshLength=0)
    if isInternalRotor:
        biggestPreviousYRotor = 0
        for curve in rotorContourLineList:
            for point in curve.points:
                if point.coordinate[1] > biggestPreviousYRotor:
                    biggestPreviousYRotor = point.coordinate[1]
                    biggestYPointRotor = point
                    # return biggestYPointRotor
                elif point.coordinate[1] == 0:
                    lowestYPointRotor = point
                    # return lowestYPointRotor

    else:
        smallestPreviousXRotor = machine.rotor.Rext
        for curve in rotorContourLineList:
            for point in curve.points:
                if point.coordinate[0] < smallestPreviousXRotor:
                    smallestPreviousXRotor = point.coordinate[0]
                    biggestYPointRotor = point
                    # return biggestYPointRotor

                if math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6):
                    lowestYPointRotor = point

    rotorContourLineList.extend(rotorMagSurfList[0].curve)

    return (
        rotorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
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
        # Rotor-Lamination Curves
        for rotorMagCurve in rotorMagSurfList[0].curve:
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
                print(f"gefiltert: {rotorLamCurve}")
                print(f"gefiltert: {rotorMagCurve}")
                rotorContourLineList.remove(rotorLamCurve)
                rotorContourLineList.remove(rotorMagCurve)

    print("Plot contourLineList ")
    plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)
    print("---")

    return rotorContourLineList, lowestYPointRotor, biggestYPointRotor
