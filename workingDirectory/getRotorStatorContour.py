import math
import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from workingDirectory.getRotorStatorSurfaces import getRotorSurfaces, getStatorSurfaces
from pyemmo.functions.plot import plot
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point


def getRotorContour(geometryList, machine):
    """Get a line list of the rotor-contour. ``rotorContourLineList``

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
    # -----------------------------------------------------------
    # Aussortieren der Linien die nicht an der Oberfläche liegen:
    # -----------------------------------------------------------
    # rotor lamination:
    for a, curve in enumerate(rotorLamSurfList[0].curve):
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
        for a, curve in enumerate(rotorContourLineList):
            if (
                math.isclose(a=curve.startPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
                and math.isclose(a=curve.endPoint.radius, b=rotorRext, abs_tol=1e-6)
                is False
            ):
                rotorSlotBottomLineList.append(curve)

        for a, magnet in enumerate(rotorMagSurfList):
            for b, curve in enumerate(magnet.curve):
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

        # ------------------------------------------------
        # Loeschen des Rotornutboden und Magnetboden:
        # ------------------------------------------------
        for a, curve in enumerate(rotorSlotBottomLineList):
            rotorContourLineList.remove(curve)
        # rotorContourLineList.remove(rotorSlotBottomLineList[0])

        # ---------------------------------------------------
        # createMagGrndCurve(): Erzeugung der 3 neuen Curves:
        # ---------------------------------------------------
        # Points:
        centerPointNewCircles = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1)
        startPointNewCircle1 = rotorSlotBottomLineList[0].startPoint
        endPointNewCircle1 = rotorSlotBottomLineList[1].endPoint
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
        for a, rotorLamSurfCurve in enumerate(rotorLamSurfList[0].curve):
            # Rotor-Lamination Curves
            for b, rotorMagSurf in enumerate(rotorMagSurfList):
                # Rotor-Magnets Surfaces (for multiple magnets)
                for c, rotorMagSurfCurve in enumerate(rotorMagSurf.curve):
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
    for a, curve in enumerate(statorLamSurfList[0].curve):
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
    for a, curve in enumerate(statorContourLineList):
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
