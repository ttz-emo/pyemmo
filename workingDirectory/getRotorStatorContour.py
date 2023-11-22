import math
import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from pyleecan.Classes.Machine import Machine

from workingDirectory.getRotorStatorSurfaces import getRotorSurfaces, getStatorSurfaces
from pyemmo.functions.plot import plot
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point


def calculationSurfacemagnetContour(
    machine, rotorLamSurfList, rotorMagSurfList, rotorRint, rotorRext, magnetRadius
):
    rotorContourLineList = []
    rotorSlotBottomLineList = []

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================
    # ------------------------------------------------------
    # Aussortieren der Linien die nicht am Luftspalt liegen:
    # ------------------------------------------------------
    # rotor lamination:
    for curve in rotorLamSurfList[0].curve:
        if (
            math.isclose(a=curve.startPoint.radius, b=rotorRint, abs_tol=1e-6) is False
            and math.isclose(a=curve.endPoint.radius, b=rotorRint, abs_tol=1e-6)
            is False
        ):
            rotorContourLineList.append(curve)

    print("---")
    print("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotorContourLineList, linewidth=1, markersize=3)
    print("---")

    if machine.rotor.slot.H0 != 0:
        # -----------------------------
        # Split von Linien/Kreisboegen:
        # -----------------------------
        # Heraussuchen des Bodens von Slot
        for curve in rotorContourLineList:
            if (
                math.isclose(a=curve.startPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
                and math.isclose(a=curve.endPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
            ):
                rotorSlotBottomLineList.append(curve)
        
        # Heraussuchen des Bodens von Magnet
        for magnet in rotorMagSurfList:
            for curve in magnet.curve:
                rotorContourLineList.append(curve)
                if (
                    math.isclose(
                        a=curve.startPoint.radius, b=magnetRadius, abs_tol=1e-6
                    )
                    is False
                    and math.isclose(
                        a=curve.endPoint.radius, b=magnetRadius, abs_tol=1e-6
                    )
                    is False
                ):
                    rotorSlotBottomLineList.append(curve)

        # ----------------------------------------------
        # Plots des Magnettaschenbodens und Magnetboden:
        # ----------------------------------------------
        print("Plot Rotornutboden und Magnetboden.")
        plot(rotorSlotBottomLineList, linewidth=1, markersize=3, tag=True)
        print("---")

        # -------------------------------------------
        # Loeschen des Rotornutboden und Magnetboden:
        # -------------------------------------------
        for curve in rotorSlotBottomLineList:
            rotorContourLineList.remove(curve)

        # ---------------------------------------------------
        # createMagGrndCurve(): Erzeugung der 3 neuen Curves:
        # ---------------------------------------------------
        # Points:
        centerPointNewCircles = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
        startPointNewCircle1 = rotorSlotBottomLineList[0].startPoint
        endPointNewCircle1 = rotorSlotBottomLineList[2].endPoint
        startPointNewCircle2 = rotorSlotBottomLineList[1].startPoint
        endPointNewCircle2 = rotorSlotBottomLineList[0].endPoint

        # Erstellung von zwei neuen Curves:
        newCurve1 = CircleArc(
            name="newCurve1",
            startPoint=startPointNewCircle1,
            centerPoint=centerPointNewCircles,
            endPoint=endPointNewCircle1,
        )
        newCurve2 = CircleArc(
            name="newCurve2",
            startPoint=startPointNewCircle2,
            centerPoint=centerPointNewCircles,
            endPoint=endPointNewCircle2,
        )

        rotorContourLineList.append(newCurve1)
        rotorContourLineList.append(newCurve2)

    # ----------------------------------------------
    # Aussortieren von doppelten Linien/Kreisboegen:
    # ----------------------------------------------
    else:
        for rotorLamSurfCurve in rotorLamSurfList[0].curve:
            # Rotor-Lamination Curves
            for rotorMagSurf in rotorMagSurfList:
                # Rotor-Magnets Surfaces (for multiple magnets)
                for rotorMagSurfCurve in rotorMagSurf.curve:
                    # Rotor-Magnet Curves
                    if (
                        rotorMagSurfCurve.startPoint.coordinate
                        == rotorLamSurfCurve.endPoint.coordinate
                        and rotorMagSurfCurve.endPoint.coordinate
                        == rotorLamSurfCurve.startPoint.coordinate
                    ):
                        print(f"gefiltert: {rotorLamSurfCurve}")
                        print(f"gefiltert: {rotorMagSurfCurve}")
                        rotorContourLineList.remove(rotorLamSurfCurve)
                        rotorContourLineList.remove(rotorMagSurfCurve)

    print("Plot contourLineList ")
    plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)
    print("---")

    return rotorContourLineList


def getSurfacemagnetContour(
    geometryList: list, machine: Machine, isInternal: bool = True
):
    """Get a list of curves of the contour of the rotor or stator with a surfacemagnet. ``rotorContourLineList``

    Args:
        geometryList (list): _description_
        machine (Machine): _description_
        isRotor (bool): _description_

    Returns:
        _type_: _description_
    """
    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext
    H0 = machine.rotor.slot.H0
    Hmag = machine.rotor.slot.Hmag

    rotorLamSurfList, rotorMagSurfList = getRotorSurfaces(geometryList=geometryList)

    if isInternal:  # Internal rotor
        magnetFarthestRadius = rotorRext + Hmag - H0
        rotorContourLineList = calculationSurfacemagnetContour(
            machine=machine,
            rotorLamSurfList=rotorLamSurfList,
            rotorMagSurfList=rotorMagSurfList,
            rotorRint=rotorRint,
            rotorRext=rotorRext,
            magnetRadius=magnetFarthestRadius,
        )

    else:
        magnetShortestRadius = rotorRext - Hmag + H0
        rotorContourLineList = calculationSurfacemagnetContour(
            machine=machine,
            rotorLamSurfList=rotorLamSurfList,
            rotorMagSurfList=rotorMagSurfList,
            rotorRint=rotorRext,
            rotorRext=rotorRint,
            magnetRadius=magnetShortestRadius,
        )

    return rotorContourLineList


def getRotorContour(geometryList, machine: Machine):
    """Get a list of curves of the . ``rotorContourLineList``

    Args:
        geometryList (_type_): _description_
        machine (_type_): _description_

    Returns:
        _type_: _description_
    """
    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext
    H0 = machine.rotor.slot.H0
    Hmag = machine.rotor.slot.Hmag
    magnetFarthestRadius = rotorRext + Hmag - H0

    rotorContourLineList = []
    rotorSlotBottomLineList = []
    rotorLamSurfList, rotorMagSurfList = getRotorSurfaces(geometryList=geometryList)

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================
    # ------------------------------------------------------
    # Aussortieren der Linien die nicht am Luftspalt liegen:
    # ------------------------------------------------------
    # rotor lamination:
    for curve in rotorLamSurfList[0].curve:
        if (
            math.isclose(a=curve.startPoint.radius, b=rotorRint, abs_tol=1e-6) is False
            and math.isclose(a=curve.endPoint.radius, b=rotorRint, abs_tol=1e-6)
            is False
        ):
            rotorContourLineList.append(curve)

    print("---")
    print("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotorContourLineList, linewidth=1, markersize=3)
    print("---")

    if machine.rotor.slot.H0 != 0:
        # -----------------------------
        # Split von Linien/Kreisboegen:
        # -----------------------------
        # Heraussuchen der Boeden von Magnet und Slot
        for curve in rotorContourLineList:
            if (
                math.isclose(a=curve.startPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
                and math.isclose(a=curve.endPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
            ):
                rotorSlotBottomLineList.append(curve)

        for magnet in rotorMagSurfList:
            for curve in magnet.curve:
                rotorContourLineList.append(curve)
                if (
                    math.isclose(
                        a=curve.startPoint.radius, b=magnetFarthestRadius, abs_tol=1e-6
                    )
                    is False
                    and math.isclose(
                        a=curve.endPoint.radius, b=magnetFarthestRadius, abs_tol=1e-6
                    )
                    is False
                ):
                    rotorSlotBottomLineList.append(curve)

        # ----------------------------------------------
        # Plots des Magnettaschenbodens und Magnetboden:
        # ----------------------------------------------

        print("Plot Rotornutboden und Magnetboden.")
        plot(rotorSlotBottomLineList, linewidth=1, markersize=3, tag=True)
        print("---")

        # -------------------------------------------
        # Loeschen des Rotornutboden und Magnetboden:
        # -------------------------------------------
        for curve in rotorSlotBottomLineList:
            rotorContourLineList.remove(curve)

        # ---------------------------------------------------
        # createMagGrndCurve(): Erzeugung der 3 neuen Curves:
        # ---------------------------------------------------
        # Points:
        centerPointNewCircles = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
        startPointNewCircle1 = rotorSlotBottomLineList[0].startPoint
        endPointNewCircle1 = rotorSlotBottomLineList[2].endPoint
        startPointNewCircle2 = rotorSlotBottomLineList[1].startPoint
        endPointNewCircle2 = rotorSlotBottomLineList[0].endPoint

        # Erstellung von zwei neuen Curves:
        newCurve1 = CircleArc(
            name="newCurve1",
            startPoint=startPointNewCircle1,
            centerPoint=centerPointNewCircles,
            endPoint=endPointNewCircle1,
        )
        newCurve2 = CircleArc(
            name="newCurve2",
            startPoint=startPointNewCircle2,
            centerPoint=centerPointNewCircles,
            endPoint=endPointNewCircle2,
        )

        rotorContourLineList.append(newCurve1)
        rotorContourLineList.append(newCurve2)

    # ----------------------------------------------
    # Aussortieren von doppelten Linien/Kreisboegen:
    # ----------------------------------------------
    else:
        for rotorLamSurfCurve in rotorLamSurfList[0].curve:
            # Rotor-Lamination Curves
            for rotorMagSurf in rotorMagSurfList:
                # Rotor-Magnets Surfaces (for multiple magnets)
                for rotorMagSurfCurve in rotorMagSurf.curve:
                    # Rotor-Magnet Curves
                    if (
                        rotorMagSurfCurve.startPoint.coordinate
                        == rotorLamSurfCurve.endPoint.coordinate
                        and rotorMagSurfCurve.endPoint.coordinate
                        == rotorLamSurfCurve.startPoint.coordinate
                    ):
                        print(f"gefiltert: {rotorLamSurfCurve}")
                        print(f"gefiltert: {rotorMagSurfCurve}")
                        rotorContourLineList.remove(rotorLamSurfCurve)
                        rotorContourLineList.remove(rotorMagSurfCurve)

    print("Plot contourLineList ")
    plot(rotorContourLineList, linewidth=1, markersize=3, tag=True)
    print("---")
    return rotorContourLineList


def getStatorContour(geometryList, machine):
    statorContourLineList = []
    statorLamSurfList = getStatorSurfaces(geometryList=geometryList)

    # =================================================
    # Erstellung der Rotor-Konturlinie fuer MovingBand:
    # =================================================

    # rotorLamSurfTestList = rotorLamSurfList.copy()
    # rotorMagSurfTestList = rotorMagSurfList.copy()

    # -----------------------------------------------------------
    # Aussortieren der Linien die nicht an der Oberfläche liegen:
    # -----------------------------------------------------------
    statorRint = machine.stator.Rint
    statorRext = machine.stator.Rext
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
            curve.startPoint.radius > statorRint
            and math.isclose(a=curve.startPoint.radius, b=statorRint, abs_tol=1e-6)
            is False
        ):
            statorLinePointList.append(curve.startPoint)
        elif (
            curve.endPoint.radius > statorRint
            and math.isclose(a=curve.endPoint.radius, b=statorRint, abs_tol=1e-6)
            is False
        ):
            statorLinePointList.append(curve.endPoint)

    centerPoint = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
    statorNewLine = CircleArc(
        name="statorNewCircleArc",
        startPoint=statorLinePointList[0],
        endPoint=statorLinePointList[1],
        centerPoint=centerPoint,
    )
    statorContourLineList.append(statorNewLine)
    print("statorContourLineList:")
    plot(statorContourLineList, linewidth=1, markersize=3, tag=True)
    print("---")
    return statorContourLineList
