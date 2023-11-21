import math

from pyleecan.Classes.MachineIPMSM import MachineIPMSM

from pyemmo.script.material.material import Material
from workingDirectory.createGeoDict import createGeoDict
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.functions.plot import plot
from workingDirectory.getCoordinatesForPoint import getXforPoint, getYforPoint


def buildPyemmoMovingBand(
    machine, rotorRext, statorRint, magnetFarthestRadius, magnetShortestRadius
):
    """Build the MovingBand in the airgap.

    Returns:
        _type_: _description_
    """

    if isinstance(machine, MachineIPMSM):
        rotorSym = machine.get_pole_pair_number()
        statorSym = machine.stator.slot.Zs
        rotorSymAngle = 2 * math.pi / rotorSym  # [rad]
        statorSymAngle = 2 * math.pi / statorSym  # [rad]

    else:
        rotorSym = machine.rotor.slot.Zs
        statorSym = machine.stator.slot.Zs
        rotorSymAngle = 2 * math.pi / rotorSym  # [rad]
        statorSymAngle = 2 * math.pi / statorSym  # [rad]

    geometryList, rotorContourLineList, statorContourLineList = createGeoDict(
        machine, rotorSym, statorSym, magnetFarthestRadius, magnetShortestRadius
    )
    materialAir = Material(name="Air",conductivity=0,relPermeability=1.0000004,remanence=None,tempCoefRem=None,BH=None,density=None,thermalConductivity=None,thermalCapacity=None)
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
    for curve in rotorContourLineList:
        for point in curve.points:
            if point.coordinate[1] > biggestPreviousYRotor:
                biggestPreviousYRotor = point.coordinate[1]
                biggestYPointRotor = point
            elif point.coordinate[1] == 0:
                lowestYPointRotor = point

    centerPoint = Point(name="centerPointBand", x=0, y=0, z=0, meshLength=1)
    nbrStatorSeg = machine.stator.slot.Zs
    angleStator = 2 * math.pi / nbrStatorSeg
    nbrRotorSeg = machine.rotor.slot.Zs
    angleRotor = 2 * math.pi / nbrRotorSeg
    
    # ================
    # Bands for rotor:
    # ================
    # -----------------
    # Rotor inner band:
    # -----------------
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
    Rotorluftspalt1Curves = rotorContourLineList
    Rotorluftspalt1Curves.append(rotorCircle1)
    Rotorluftspalt1Curves.append(lowerLine1)
    Rotorluftspalt1Curves.append(upperLine1)

    # Assginment of rotorBand1 as surface:
    Rotorluftspalt1 = SurfaceAPI(
        name="Rotorluftspalt 1",
        idExt="LuR1",
        curves=Rotorluftspalt1Curves,
        material=materialAir,
        nbrSegments=nbrRotorSeg,
        angle=angleRotor,
        meshSize=1.0,
    )
    plot(Rotorluftspalt1Curves, linewidth=1, markersize=3, tag=True)
    Rotorluftspalt1.plot()
    print("---")

    # -----------------
    # Rotor outer band:
    # -----------------
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
    Rotorluftspalt2Curves = []
    Rotorluftspalt2Curves.append(rotorCircle1)
    Rotorluftspalt2Curves.append(rotorCircle2)
    Rotorluftspalt2Curves.append(lowerLine2)
    Rotorluftspalt2Curves.append(upperLine2)

    # Assginment of rotorBand2 as surface:
    Rotorluftspalt2 = SurfaceAPI(
        name="Rotorluftspalt 2",
        idExt="LuR2",
        curves=Rotorluftspalt2Curves,
        material=materialAir,
        nbrSegments=nbrRotorSeg,
        angle=angleRotor,
        meshSize=1.0,
    )
    movingband_r = rotorCircle2.startPoint.radius

    # -----------------
    # RotorBandsCurves:
    # -----------------
    RotorluftspaltCurves = []
    RotorluftspaltCurves.append(Rotorluftspalt1Curves)
    RotorluftspaltCurves.append(Rotorluftspalt2Curves)
    plot(RotorluftspaltCurves, linewidth=1, markersize=3, tag=True)
    print("---")


    # =================
    # Bands for stator:
    # =================
    # ------------------
    # Stator outer band:
    # ------------------
    biggestPreviousYStator = 0
    for curve in statorContourLineList:
        for point in curve.points:
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
    stlu1curves = statorContourLineList
    stlu1curves.append(statorCircle4)
    stlu1curves.append(lowerLine4)
    stlu1curves.append(upperLine4)

    # Assginment of Statorluftspalt2 as surface:
    Statorluftspalt1 = SurfaceAPI(
        name="Statorluftspalt 1",
        idExt="StLu1",
        curves=stlu1curves,
        material=materialAir,
        nbrSegments=nbrStatorSeg,
        angle=angleStator,
        meshSize=1.0,
    )

    plot(stlu1curves, linewidth=1, markersize=3, tag=True)
    Statorluftspalt1.plot()
    print("---")

    # ------------------
    # Stator inner band:
    # ------------------
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
    StLu2curves = []
    StLu2curves.append(statorCircle4)
    StLu2curves.append(statorCircle3)
    StLu2curves.append(lowerLine3)
    StLu2curves.append(upperLine3)

    # Assginment of statorBand3 as surface:
    Statorluftspalt2 = SurfaceAPI(
        name="Statorluftspalt 2",
        idExt="StLu2",
        curves=StLu2curves,
        material= materialAir,
        nbrSegments=nbrStatorSeg,
        angle=angleStator,
        meshSize=1.0,
    )

    # ----------
    # All bands:
    # ----------
    allBands = []
    allBands.append(Rotorluftspalt1)
    allBands.append(Rotorluftspalt2)
    allBands.append(Statorluftspalt1)
    allBands.append(Statorluftspalt2)
    geometryList.extend(allBands)
    print("Plot allBands: ")
    plot(allBands)

    return allBands, geometryList, movingband_r
