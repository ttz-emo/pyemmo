import math

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Machine import Machine

from pyemmo.api import air
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.functions.plot import plot
from .createGeoDict import createGeoDict
from .getCoordinatesForPoint import getXforPoint, getYforPoint


def buildBandsRotor(
    machine: Machine,
    bandRadiusList: list,
    centerPoint: Point,
    rPointRotorCont: Point,
    lPointRotorCont: Point,
    rotorContourLineList: list,
) -> tuple[SurfaceAPI, SurfaceAPI, float]:
    """Builds the air gap segments at the rotor side.

    Args:
        bandRadiusList (list): List with the radii of the bands
        centerPoint (Point): Center point of machine
        lowestYPointRotor (Point):
        biggestYPointRotor (Point): _description_
        rotorSymAngle (float): _description_
        rotorContourLineList (list): _description_
        nbrRotorSeg (int): _description_
        angleRotor (float): _description_

    Returns:
        tuple[SurfaceAPI, SurfaceAPI, float]: _description_
    """
    nbrRotorSeg = machine.rotor.comp_periodicity_geo()[0]
    angleRotor = 2 * math.pi / nbrRotorSeg  # [rad]

    # -----------------
    # Rotor inner band:
    # -----------------
    # Points:
    mbMeshLen = 2 * bandRadiusList[1] * math.pi / 360
    pointM11 = Point(
        name="PointM11", x=bandRadiusList[0], y=0, z=0, meshLength=mbMeshLen
    )
    pointM12 = Point(
        name="PointM12",
        x=getXforPoint(bandRadiusList[0], angleRotor),
        y=getYforPoint(bandRadiusList[0], angleRotor),
        z=0,
        meshLength=mbMeshLen,
    )

    # Curves:
    rotorCircle1 = CircleArc(
        name="rotorBand1",
        startPoint=pointM11,
        endPoint=pointM12,
        centerPoint=centerPoint,
    )
    lowerLine1 = Line(
        name="lowerLine1", startPoint=rPointRotorCont, endPoint=pointM11
    )
    upperLine1 = Line(
        name="upperLine1", startPoint=lPointRotorCont, endPoint=pointM12
    )

    # Adding curves to list:
    rotorAirgap1Curves = rotorContourLineList
    rotorAirgap1Curves.append(rotorCircle1)
    rotorAirgap1Curves.append(lowerLine1)
    rotorAirgap1Curves.append(upperLine1)

    # Assginment of rotorBand1 as surface:
    Rotorluftspalt1 = SurfaceAPI(
        name="Rotorluftspalt 1",
        idExt="LuR1",
        curves=rotorAirgap1Curves,
        material=air,
        nbrSegments=nbrRotorSeg,
        angle=angleRotor,
        meshSize=1.0,
    )
    plot(rotorAirgap1Curves, linewidth=1, markersize=3, tag=True)
    # Rotorluftspalt1.plot()
    print("---")

    # -----------------
    # Rotor outer band:
    # -----------------
    # Points:
    PointM21 = Point(
        name="PointM21", x=bandRadiusList[1], y=0, z=0, meshLength=mbMeshLen
    )
    PointM22 = Point(
        name="PointM22",
        x=getXforPoint(bandRadiusList[1], angleRotor),
        y=getYforPoint(bandRadiusList[1], angleRotor),
        z=0,
        meshLength=mbMeshLen,
    )
    # Curves:
    rotorCircle2 = CircleArc(
        name="MB_CurveRotor",
        startPoint=PointM21,
        endPoint=PointM22,
        centerPoint=centerPoint,
    )
    lowerLine2 = Line(
        name="lowerLine2", startPoint=pointM11, endPoint=PointM21
    )
    upperLine2 = Line(
        name="upperLine2", startPoint=pointM12, endPoint=PointM22
    )

    # Adding curves to list:
    rotorAirgap2Curves = []
    rotorAirgap2Curves.append(rotorCircle1)
    rotorAirgap2Curves.append(rotorCircle2)
    rotorAirgap2Curves.append(lowerLine2)
    rotorAirgap2Curves.append(upperLine2)

    # Assginment of rotorBand2 as surface:
    Rotorluftspalt2 = SurfaceAPI(
        name="Rotorluftspalt 2",
        idExt="LuR2",
        curves=rotorAirgap2Curves,
        material=air,
        nbrSegments=nbrRotorSeg,
        angle=angleRotor,
        meshSize=1.0,
    )
    movingband_r = rotorCircle2.startPoint.radius

    # -----------------
    # RotorBandsCurves:
    # -----------------
    RotorluftspaltCurves = []
    RotorluftspaltCurves.append(rotorAirgap1Curves)
    RotorluftspaltCurves.append(rotorAirgap2Curves)
    plot(RotorluftspaltCurves, linewidth=1, markersize=3, tag=True)
    print("---")

    return (
        Rotorluftspalt1,
        Rotorluftspalt2,
        movingband_r,
    )


def buildBandsStator(
    machine: Machine,
    statorContourLineList: list,
    bandRadiusList: list,
    centerPoint: Point,
) -> tuple[SurfaceAPI, SurfaceAPI]:
    """_summary_

    Args:
        statorContourLineList (list): _description_
        bandRadiusList (list): _description_
        statorSymAngle (float): _description_
        centerPoint (Point): _description_
        nbrStatorSeg (int): _description_
        angleStator (float): _description_

    Returns:
        tuple[SurfaceAPI, SurfaceAPI]: _description_
    """
    nbrStatorSeg = machine.stator.slot.Zs
    angleStator = 2 * math.pi / nbrStatorSeg  # [rad]
    
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
    mbMeshLen = 2 * bandRadiusList[2] * math.pi / 360
    PointM41 = Point(
        name="PointM41", x=bandRadiusList[3], y=0, z=0, meshLength=mbMeshLen
    )
    PointM42 = Point(
        name="PointM42",
        x=getXforPoint(bandRadiusList[3], angleStator),
        y=getYforPoint(bandRadiusList[3], angleStator),
        z=0,
        meshLength=mbMeshLen,
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
        material=air,
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
    PointM31 = Point(
        name="PointM31", x=bandRadiusList[2], y=0, z=0, meshLength=mbMeshLen
    )
    PointM32 = Point(
        name="PointM22",
        x=getXforPoint(bandRadiusList[2], angleStator),
        y=getYforPoint(bandRadiusList[2], angleStator),
        z=0,
        meshLength=mbMeshLen,
    )
    # Curves:
    statorCircle3 = CircleArc(
        name="MB_CurveStator",
        startPoint=PointM31,
        endPoint=PointM32,
        centerPoint=centerPoint,
    )
    lowerLine3 = Line(
        name="lowerLine3", startPoint=PointM31, endPoint=PointM41
    )
    upperLine3 = Line(
        name="upperLine3", startPoint=PointM32, endPoint=PointM42
    )

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
        material=air,
        nbrSegments=nbrStatorSeg,
        angle=angleStator,
        meshSize=1.0,
    )

    return Statorluftspalt1, Statorluftspalt2


def buildMovingBand(
    machine: Machine,
    isInternalRotor: bool,
) -> tuple[list, list[SurfaceAPI], float]:
    """_summary_

    Args:
        machine (Machine): _description_
        rotorRint (float): _description_
        rotorRext (float): _description_
        statorRint (float): _description_
        statorRext (float): _description_
        isInternalRotor (bool): _description_

    Returns:
        tuple[list, list[SurfaceAPI], float]: _description_
    """
    # =========================================================================
    # Calculation of the magnet-radii
    # &
    # Calculation of the distance between rotor/magnet and stator inner radius:
    # =========================================================================
    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext
    statorRint = machine.stator.Rint
    statorRext = machine.stator.Rext
    if isinstance(machine, MachineSIPMSM):
        H0 = machine.rotor.slot.H0
        H1 = machine.rotor.slot.H1

        if isInternalRotor:
            magnetFarthestRadius = rotorRext + H1 - H0
            magnetShortestRadius = rotorRext - H0
        else:
            magnetFarthestRadius = rotorRint + H0
            magnetShortestRadius = rotorRint + H0 - H1

        if isInternalRotor:
            if rotorRext > magnetFarthestRadius:
                diffRadius = statorRint - rotorRext
                maxRadius = rotorRext
            else:
                diffRadius = statorRint - magnetFarthestRadius
                maxRadius = magnetFarthestRadius
        else:
            statorRext = machine.stator.Rext
            rotorRint = machine.rotor.Rint
            if rotorRint < magnetShortestRadius:
                diffRadius = statorRext - rotorRint
                maxRadius = rotorRint
            else:
                diffRadius = statorRext - magnetShortestRadius
                maxRadius = magnetShortestRadius

    elif isinstance(machine, (MachineIPMSM, MachineSyRM)):
        if isInternalRotor:
            maxRadius = rotorRext
            diffRadius = statorRint - maxRadius
        else:
            maxRadius = rotorRint
            diffRadius = statorRext - maxRadius

    # =================================================================
    # Translation of geometry and creation of rotor and stator contour:
    # =================================================================
    (
        geometryList,
        rotorContourLineList,
        statorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
        magnetizationDict,
    ) = createGeoDict(
        machine,
        isInternalRotor,
    )

    # ====================================
    # Calculation of the MovingBand radii:
    # ====================================
    numberOfBands = 5
    Wp = diffRadius / numberOfBands
    bandRadiusList = []

    for i in range(1, numberOfBands + 1):
        bandRadiusList.append(maxRadius + Wp * i)

    print(f"bandRadiusList: {bandRadiusList}")
    print("---")

    centerPoint = Point(name="centerPointBand", x=0, y=0, z=0, meshLength=1e-3)

    (
        Rotorluftspalt1,
        Rotorluftspalt2,
        movingband_r,
    ) = buildBandsRotor(
        machine=machine,
        bandRadiusList=bandRadiusList,
        centerPoint=centerPoint,
        rPointRotorCont=lowestYPointRotor,
        lPointRotorCont=biggestYPointRotor,
        rotorContourLineList=rotorContourLineList,
    )
    (
        Statorluftspalt1,
        Statorluftspalt2,
    ) = buildBandsStator(
        machine=machine,
        statorContourLineList=statorContourLineList,
        bandRadiusList=bandRadiusList,
        centerPoint=centerPoint,
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

    return allBands, geometryList, movingband_r, magnetizationDict
