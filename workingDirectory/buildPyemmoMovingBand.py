import math
from workingDirectory.createGeoDict import createGeoDict
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.surface import Surface
from pyemmo.functions.plot import plot
from workingDirectory.getCoordinatesForPoint import getXforPoint, getYforPoint


def buildPyemmoMovingBand(machine):
    geometryList, rotorContourLineList, statorContourLineList = createGeoDict(
        machine=machine
    )
    """Build the MovingBand in the airgap.

    Returns:
        _type_: _description_
    """

    rotorRext = machine.rotor.Rext
    statorRint = machine.stator.Rint
    H0 = machine.rotor.slot.H0
    Hmag = machine.rotor.slot.Hmag
    magnetFarthestRadius = rotorRext + Hmag - H0

    # if isinstance(machine, MachineSCIM):
    rotorSym = machine.rotor.slot.Zs
    statorSym = machine.stator.slot.Zs
    rotorSymAngle = 2 * math.pi / rotorSym  # [rad]
    statorSymAngle = 2 * math.pi / statorSym  # [rad]

    # else:
    #     rotorSym = machine.get_pole_pair_number() * 2
    #     statorSym = machine.stator.slot.Zs
    #     rotorSymAngle = 2 * math.pi / rotorSym  # [rad]
    #     statorSymAngle = 2 * math.pi / statorSym  # [rad]

    # =========================================================================
    # Calculation of the distance between rotor/magnet and stator inner radius:
    # =========================================================================
    if rotorRext > magnetFarthestRadius:
        diffRadius = statorRint - rotorRext
        maxRadius = rotorRext
    else:
        diffRadius = statorRint - magnetFarthestRadius
        maxRadius = magnetFarthestRadius

    numberOfBands = 5
    Wp = diffRadius / numberOfBands
    bandRadiusList = []

    for i in range(1, numberOfBands + 1):
        bandRadiusList.append(maxRadius + Wp * i)

    print(f"bandRadiusList: {bandRadiusList}")
    print("---")

    biggestPreviousYRotor = 0
    for a, curve in enumerate(rotorContourLineList):
        for b, point in enumerate(curve.points):
            if point.coordinate[1] > biggestPreviousYRotor:
                biggestPreviousYRotor = point.coordinate[1]
                biggestYPointRotor = point
            elif point.coordinate[1] == 0:
                lowestYPointRotor = point

    centerPoint = Point(name="centerPointBand", x=0, y=0, z=0, meshLength=1)

    # ================
    # Bands for rotor:
    # ================
    # -----------
    # First Band:
    # -----------
    # Points:
    PointM11 = Point(name="PointM11", x=bandRadiusList[0], y=0, z=0, meshLength=1)
    PointM12 = Point(
        name="PointM12",
        x=getXforPoint(bandRadiusList[0], rotorSymAngle),
        y=getYforPoint(bandRadiusList[0], rotorSymAngle),
        z=0,
        meshLength=1,
    )

    # Curves:
    rotorCircle1 = CircleArc(
        name="rotorBand1",
        startPoint=PointM11,
        endPoint=PointM12,
        centerPoint=centerPoint,
    )
    lowerLine1 = Line(
        name="lowerLine1", startPoint=lowestYPointRotor, endPoint=PointM11
    )
    upperLine1 = Line(
        name="upperLine1", startPoint=biggestYPointRotor, endPoint=PointM12
    )

    # Adding curves to list:
    rotorBand1Curves = rotorContourLineList
    rotorBand1Curves.append(rotorCircle1)
    rotorBand1Curves.append(lowerLine1)
    rotorBand1Curves.append(upperLine1)

    # Assginment of rotorBand1 as surface:
    rotorBand1 = Surface(name="rotorBand1", curves=rotorBand1Curves)
    plot(rotorBand1Curves, linewidth=1, markersize=3, tag=True)
    rotorBand1.plot()
    print("---")

    # ------------
    # Second Band:
    # ------------
    # Points:
    PointM21 = Point(name="PointM21", x=bandRadiusList[1], y=0, z=0, meshLength=1)
    PointM22 = Point(
        name="PointM22",
        x=getXforPoint(bandRadiusList[1], rotorSymAngle),
        y=getYforPoint(bandRadiusList[1], rotorSymAngle),
        z=0,
        meshLength=1,
    )
    # Curves:
    rotorCircle2 = CircleArc(
        name="MB_CurveRotor",
        startPoint=PointM21,
        endPoint=PointM22,
        centerPoint=centerPoint,
    )
    lowerLine2 = Line(name="lowerLine2", startPoint=PointM11, endPoint=PointM21)
    upperLine2 = Line(name="upperLine2", startPoint=PointM12, endPoint=PointM22)

    # Adding curves to list:
    rotorBand2Curves = []
    rotorBand2Curves.append(rotorCircle1)
    rotorBand2Curves.append(rotorCircle2)
    rotorBand2Curves.append(lowerLine2)
    rotorBand2Curves.append(upperLine2)

    # Assginment of rotorBand2 as surface:
    rotorBand2 = Surface(name="rotorBand2", curves=rotorBand2Curves)

    # -----------------
    # RotorBandsCurves:
    # -----------------
    rotorBandsCurves = []
    rotorBandsCurves.append(rotorBand1Curves)
    rotorBandsCurves.append(rotorBand2Curves)
    plot(rotorBandsCurves, linewidth=1, markersize=3, tag=True)
    print("---")

    # =================
    # Bands for stator:
    # =================

    # ------------
    # Fourth Band:
    # ------------
    biggestPreviousYStator = 0
    for a, curve in enumerate(statorContourLineList):
        for b, point in enumerate(curve.points):
            if point.coordinate[1] > biggestPreviousYStator:
                biggestPreviousYStator = point.coordinate[1]
                biggestYPointStator = point
            elif point.coordinate[1] == 0:
                lowestYPointStator = point

    # Points:
    PointM41 = Point(name="PointM41", x=bandRadiusList[3], y=0, z=0, meshLength=1)
    PointM42 = Point(
        name="PointM42",
        x=getXforPoint(bandRadiusList[3], statorSymAngle),
        y=getYforPoint(bandRadiusList[3], statorSymAngle),
        z=0,
        meshLength=1,
    )

    # Curves:
    statorCircle4 = CircleArc(
        name="statorCircle4",
        startPoint=PointM41,
        endPoint=PointM42,
        centerPoint=centerPoint,
    )
    lowerLine4 = Line(
        name="lowerLine4", startPoint=lowestYPointStator, endPoint=PointM41
    )
    upperLine4 = Line(
        name="upperLine4", startPoint=biggestYPointStator, endPoint=PointM42
    )

    # Adding curves to list:
    statorBand4Curves = statorContourLineList
    statorBand4Curves.append(statorCircle4)
    statorBand4Curves.append(lowerLine4)
    statorBand4Curves.append(upperLine4)

    # Assginment of rotorBand4 as surface:
    statorBand4 = Surface(name="statorBand4", curves=statorBand4Curves)
    plot(statorBand4Curves, linewidth=1, markersize=3, tag=True)
    statorBand4.plot()
    print("---")

    # -----------
    # Third Band:
    # -----------
    # Points:
    PointM31 = Point(name="PointM31", x=bandRadiusList[2], y=0, z=0, meshLength=1)
    PointM32 = Point(
        name="PointM22",
        x=getXforPoint(bandRadiusList[2], statorSymAngle),
        y=getYforPoint(bandRadiusList[2], statorSymAngle),
        z=0,
        meshLength=1,
    )
    # Curves:
    statorCircle3 = CircleArc(
        name="MB_CurveStator",
        startPoint=PointM31,
        endPoint=PointM32,
        centerPoint=centerPoint,
    )
    lowerLine3 = Line(name="lowerLine3", startPoint=PointM31, endPoint=PointM41)
    upperLine3 = Line(name="upperLine3", startPoint=PointM32, endPoint=PointM42)

    # Adding curves to list:
    statorBand3Curves = []
    statorBand3Curves.append(statorCircle3)
    statorBand3Curves.append(statorCircle3)
    statorBand3Curves.append(lowerLine3)
    statorBand3Curves.append(upperLine3)

    # Assginment of statorBand3 as surface:
    statorBand3 = Surface(name="statorBand3", curves=statorBand3Curves)

    # ----------
    # All bands:
    # ----------
    allBands = []
    allBands.append(rotorBand1)
    allBands.append(rotorBand2)
    allBands.append(statorBand3)
    allBands.append(statorBand4)
    geometryList.extend(allBands)
    print("Plot allBands: ")
    plot(allBands)

    return allBands, geometryList
