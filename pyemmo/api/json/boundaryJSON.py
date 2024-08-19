#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""This module creates the boundary physical elements for models created via the json-api"""

from __future__ import annotations

from numpy import pi

# from matplotlib import pyplot as plt
# from ..functions.plot import plot
from ...script.geometry import physicalsDict
from ...script.geometry.limitLine import LimitLine
from ...script.geometry.line import Line
from ...script.geometry.movingBand import MovingBand
from ...script.geometry.physicalElement import PhysicalElement
from ...script.geometry.primaryLine import PrimaryLine
from ...script.geometry.slaveLine import SlaveLine
from ...script.geometry.transformable import Transformable
from ...script.material.material import Material
from .. import air
from .. import logger as apiLogger
from . import (
    InnerLimitLineDict,
    OuterLimitLineDict,
    RotorMBLineDict,
    StatorMBLineDict,
    globalCenterPoint,
)
from .modelJSON import rotateDuplicate
from .SurfaceJSON import SurfaceAPI


def getPrimaryLines(
    segmentSurfDict: dict[str, SurfaceAPI],
    rotorAirgapRadius: float,
    pinballRadius: float = 1e-6,
) -> tuple[list[Line], list[Line]]:
    """Extract the primary lines for the Link boundary condition.
        Since the geometry is allways constructed from the horizontal x-axis the lines must lie
        on that axis with a tolerance given by pinballRadius.

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt) as
            keys and SurfaceAPI objects as values
        RotorAirgapRadius (float): Radius of the outer rotor airgap line (rotor movingband line)
            to determine whether a line is on the rotor or stator side.
        pinballRadius (float, optional): Distance in m that a primary line point can differ from
            the x-axis. Defaults to 1e-6.

    Returns:
        Tuple[List[Line],List[Line]]: List of stator and rotor primary lines (StatorList,RotorList).
    """
    rotorMLList: list[Line] = []  # Rotor primarylines
    statorMLList: list[Line] = []  # Stator primarylines
    for area in segmentSurfDict.values():  # for every surface
        for line in area.curve:  # for each line
            # get the coordinates of the startpoint
            startPoint = line.startPoint.coordinate[:]
            # get the coords of the endpoint
            endPoint = line.endPoint.coordinate[:]
            # if the y-values are smaller than the maximal Distanz from y=0
            # (Pinball radius) which means they are on the x-axis AND their
            # x-coordinate is positive (positive side of x-axis) -> it's a
            # primary line
            if (
                abs(startPoint[1]) < pinballRadius
                and abs(endPoint[1]) < pinballRadius
                and (startPoint[0] > 0 and endPoint[0] > 0)
            ):
                # if x-values are smaller than airgap radius, line is on rotor
                # FIXME: this is only true for inner rotor machines
                if (
                    abs(startPoint[0]) <= rotorAirgapRadius
                    or abs(endPoint[0]) <= rotorAirgapRadius
                ):
                    # it is a rotor primary line
                    rotorMLList.append(line.duplicate())
                else:  # otherwise its on the stator side
                    # it is a stator primary line
                    statorMLList.append(line.duplicate())
    return statorMLList, rotorMLList


def createSecondaryLines(
    statorPrimaryLines: list[Line],
    rotorPrimaryLines: list[Line],
    symFactor: int,
) -> tuple[list[Line], list[Line]]:
    """duplicate the stator and rotor primary lines to get the secondary lines. For primary lines
    see function "getPrimaryLines".
    Lines are created by duplicating the primary lines and rotating them by 2*pi/symFactor.

    Args:
        statorPrimaryLines (List[Line]): List of primary lines on the stator side.
        rotorPrimaryLines (List[Line]): List of the primary lines on the rotor side.

    Returns:
        Tuple[List[Line], List[Line]]: List of stator and rotor secondary lines
        (StatorList, RotorList).
    """
    rotorSLList: list[Line] = list()  # Rotor slavelines
    statorSLList: list[Line] = list()  # Stator slavelines
    for primaryLine in statorPrimaryLines:
        slaveLine = primaryLine.duplicate()  # duplicate
        # and rotate primaryline to get slaveline
        slaveLine.rotateZ(angle=2 * pi / symFactor)
        statorSLList.append(slaveLine)
    for primaryLine in rotorPrimaryLines:
        slaveLine = primaryLine.duplicate()  # duplicate
        # and rotate primaryline to get slaveline
        slaveLine.rotateZ(angle=2 * pi / symFactor)
        rotorSLList.append(slaveLine)
    return statorSLList, rotorSLList


def findLine(lineName: str, lineIDList) -> bool:
    """
    findLine is a recursive function that checks if a list of IDs is in lineName.
    It returns true only if all IDs are valid.
    LineIDList can look like ["ID1",["ID21","ID22"],...], so lineName has to contain
    either "ID1" or "ID21" and "ID22".

    Args:
        lineName: line name to check.
        LineIDList: list of strings to check for in the line name.

    Returns:
        bool: True if a member of lineIDList (Point ID) was found in a line.
    """
    nbrLineIDs = 0
    for lineIDs in lineIDList:
        if isinstance(lineIDs, str):  # if the line ID is a string
            # just determine if the string is in the linename
            if lineIDs in lineName:
                nbrLineIDs += 1
        # if LineIDs is a list of lineIDs (type str) call function again
        elif isinstance(lineIDs, list):
            if findLine(lineName, lineIDs):
                return True
    if nbrLineIDs == len(lineIDList):
        return True
    return False


def findLines(
    segmentSurfDict: dict[str, SurfaceAPI],
    surfID: str,
    lineIDList: list[list[str] | str],
) -> tuple[list[Line], SurfaceAPI]:
    """
    findLines looks for a surface in segmentSurfDict by the SurfID and checks if this
    surface has lines containing the LindIDList IDs.
    (LineIDList can look like ["ID1",["ID21","ID22"],...], so linename has to contain
    either "ID1" or "ID21" and "ID22". See function "findLine" for more details)

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt)
            as keys and SurfaceAPI objects as values
        SurfID (str): ID of the surface to search for in the MachineSurfaceList
        LineIDList (List[Union[List[str],str]]): List of line IDs or List of LineIDs to
            search for in the surface line list ()

    Returns:
        Tuple[List[Line], SurfaceAPI] | Tuple[None, None]: List of identified lines and the
        surface where the lines where found. Both tuple members will be None if the surface
        was not in the surface list.

    Raises:
        UserWarning: If SurfID is not found in the MachineSurfList
        ValueError: If SurfID is found more than once in the surface list
    """
    areaOfSurfID = [area for area in segmentSurfDict.values() if (surfID == area.idExt)]
    if not areaOfSurfID:  # SurfID not in Surface Dict
        apiLogger.warning("Surface ID '%s' not found in machine surface list.", surfID)
        return None, None
    if len(areaOfSurfID) != 1:
        # there should only be one area in the list "areaOfSurfID"
        msg = f"Surface with ID '{surfID}' was found more than once in the list of machine surfaces"
        raise ValueError(msg)
    lineList: list[Line] = []
    for line in areaOfSurfID[0].curve:
        linename = line.name
        if findLine(linename, lineIDList):
            lineList.append(line)
    return lineList, areaOfSurfID[0]


def getBoundaryLines(
    segmentSurfDict: dict[str, SurfaceAPI],
    surfID: str,
    lineIDList: str | list[str],
    symFactor: int,
) -> list[Line] | None:
    """
    getBoundaryLines can be used to get specific boundary lines for a Onelab model out of the
    machine surfaces by identifying them through surface ID and a list of related line IDs

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt) as keys
            and SurfaceAPI objects as values
        surfID (str): Surface ID to search for in the machine surface list.
        lineIDList (str | List[str]): Line ID or list of line IDs to search for in the lineloop of
            the surface with "surfID".
        symFactor (int): symmetry factor for duplicating the found lines if necessary.

    Returns:
        List[Line] | None: List of found (and duplicated) boundary lines or None
        if no lines where found.

    """
    lineList, boundarySurface = findLines(segmentSurfDict, surfID, lineIDList)
    if lineList:  # if there are lines in linelist
        dupLines = []
        angle = boundarySurface.angle
        # number of segments in symmetry:
        nbrSegments = boundarySurface.NbrSegments / symFactor
        for line in lineList:
            for i in range(1, int(nbrSegments)):
                dupLines.append(rotateDuplicate(line, i * angle))
        return lineList + dupLines
    return None


def createMBLines(
    movingBandLineDict: dict,
    segmentSurfDict: dict[str, SurfaceAPI],
    symFactor: int,
) -> list[Line]:
    """
    createMBLines finds the inner Movingband lines in the list of SurfaceAPI objects by the IDs
    in MBLineDict and generates the corresponding number of movingband lines for the given symmetry
    by duplicate and rotate.

    Args:
        MBLineDict (Dict[str, List[str]]): Dict identifying the surface IDs to search for as
            dict keys and a list of corresponding line IDs to search for as values.
            e.g.: {"StLu": ["LuA", "LuM"] }
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt)
            as keys and SurfaceAPI objects as values
        SymFactor (int): symmetry factor

    Returns:
        List(Line): Moving band lines
    """
    # mbLines = list()
    for surfaceID in movingBandLineDict.keys():
        mbLines = getBoundaryLines(
            segmentSurfDict=segmentSurfDict,
            surfID=surfaceID,
            lineIDList=movingBandLineDict[surfaceID],
            symFactor=symFactor,
        )
        if mbLines is not None:  # Break loop if boundary line was found
            break
    return mbLines


def createMBAux(
    symFaktor: int, rotorMovingBandInnerLines: list, material=air
) -> list[MovingBand]:
    """
    createMBAux creates the outer Movingband lines of the rotor and add them to
    pyemmo-Movingband objects depended on symmetry

    Args:
        symFaktor (int): Symmetry factor.
        rotorMovingBandInnerLines (List[Line]): Inner moving band lines to duplicate.
        material (Material): Moving band material. Defaults to ''Air''.

    Returns:
        List[MovingBand]: Auxilliary moving band list.
    """
    movingBandAuxList: list[MovingBand] = []
    mbAuxLines: list[Line] = []
    symAngle = 2 * pi / symFaktor
    # here order of for-loops had to be changed because for example for symFaktor=4
    # we need 3 auxiliary movingband (mb) objects, each containing the same number
    # of lines as the inner movingband
    for i in range(1, symFaktor):  # for every symmetry part
        for line in rotorMovingBandInnerLines:  # for every inner line
            mbAuxLine = rotateDuplicate(line, i * symAngle)
            mbAuxLines.append(mbAuxLine)
        # physical element name must be Rotor_Bnd_MB_2, ..._3, ...
        movingBandAuxList.append(
            MovingBand(
                name=(physicalsDict["Rotor_MB_Line"] + f"_{str(i+1)}"),
                # copy list because is cleared for next iteration:
                geometricalElement=mbAuxLines.copy(),
                material=material,
                auxiliary=True,
            )
        )
        # clear so the old lines are no longer in the list for the next moving band part
        mbAuxLines.clear()
    return movingBandAuxList


def createMB(
    segmentSurfDict: dict[str, SurfaceAPI],
    symFactor: int,
    material: Material = air,
) -> tuple[MovingBand, MovingBand, list[MovingBand] | None]:
    """
    createMB generates all pyemmo Movingband objects needed for a simulation.

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt)
            as keys and SurfaceAPI objects as values
        symFactor (int): symmetry factor
        material (Material): Movingband material. Defaults to "air".

    Returns:
        tuple:
        - MB_Stator (MovingBand): Stator movingband
        - MB_Rotor_inner (MovingBand): Inner part of the rotor moving band
        - MB_Rotor_Aux (List(MovingBand) or None): Outer (auxillary) part of the movingband
          or None if symFactor=1
    """
    mbLinesStator = createMBLines(StatorMBLineDict, segmentSurfDict, symFactor)
    if mbLinesStator is None:
        mssg = (
            "Could not find stator movingband lines."
            f"Make sure the geometry contains the surface(s): {StatorMBLineDict.keys()}"
            f"with lines {[mbPointNames for _, mbPointNames in StatorMBLineDict.items()]}"
        )
        raise RuntimeError(mssg)

    mbLinesRotor = createMBLines(RotorMBLineDict, segmentSurfDict, symFactor)
    if mbLinesRotor is None:
        mssg = (
            f"Could not find rotor movingband lines."
            f"Make sure the geometry contains the surface(s): {RotorMBLineDict.keys()} with lines"
            f"{[mbPointNames for _, mbPointNames in RotorMBLineDict.items()]}"
        )
        raise RuntimeError(mssg)

    movingBandStator: MovingBand = MovingBand(
        name="mbStator",
        geometricalElement=mbLinesStator,
        material=material,
        auxiliary=False,
    )
    movingBandRotorInner: MovingBand = MovingBand(
        name=physicalsDict["Rotor_MB_Line"] + "_1",
        geometricalElement=mbLinesRotor,
        material=material,
        auxiliary=False,
    )
    # Outer Movingband-lines
    if symFactor > 1:
        movingBandRotorAux = createMBAux(symFactor, mbLinesRotor, material)
    else:
        movingBandRotorAux = None
    return movingBandStator, movingBandRotorInner, movingBandRotorAux


def getLimitLines(
    limitLineDict: dict[str, list[str]],
    machineSurfList: list[SurfaceAPI],
    symFactor: int,
) -> list[Line] | None:
    """
    getLimitLines identifies the inner or outer boundary lines from the machine surfaces by the
    line-IDs in LimitLineDict and duplicates them if needed.

    Args:
        limitLineDict (Dict[str, List[str]]): Is a predefined dict with surface IDs as keys and
            List of line IDs as values. The order of the surface IDs matters since the function
            directly returns the found lines! So the dict must be defined most outer to the most
            inner limit line. E.g. for the inner limit lines the limit lines dict would look like

                TODO: Create example for inner limit line dict

        machineSurfList (List[SurfaceAPI]): List of all surfaces that should be searched
        symFactor (int): symmetry factor for duplication.

    Returns:
        Union[List[Line], None]: List of limit lines if they could be identified by the surface and
        line IDs in the limitLineDict or None if no limit lines where found.
    """
    for surfaceID in limitLineDict.keys():
        limitLineList = getBoundaryLines(
            segmentSurfDict=machineSurfList,
            surfID=surfaceID,
            lineIDList=limitLineDict[surfaceID],
            symFactor=symFactor,
        )
        if limitLineList is not None:  # Break loop if boundary line was found
            return limitLineList
    # if no limit line was found:
    return None


def createBoundaries(
    segmentSurfDict: dict[str, SurfaceAPI],
    symFactor: int,
    rotorMBRadius: float,
) -> tuple[list[PhysicalElement], list[PhysicalElement]]:
    """finds or creates all essential boundary lines and adds them to corresponding
    PhysicalElements (LimitLine, MovingBand, PrimaryLine, SecondaryLine,...).

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt)
            as keys and SurfaceAPI objects as values
        symFactor (int): Symmetry factor
        rotorMBRadius (float): Rotor movingband radius to differ between rotor and
            stator boundaries.

    Returns:
        Tuple[List[PhysicalElement], List[PhysicalElement]]: List of stator and
        rotor boundary lines (statorBoundaries, rotorBoundaries)

    Raises:
        AttributeError: If no surface for the outer limit lines could be found.
        AttributeError: If no surface for the inner limit lines could be found.
    """
    # Create lists for Stator and Rotor boundaries
    rotorPhysicals: list[PhysicalElement] = []
    statorPhysicals: list[PhysicalElement] = []

    # 1: primary-Slave
    if symFactor > 1:
        [primaryLinesStator, primarylinesRotor] = getPrimaryLines(
            segmentSurfDict=segmentSurfDict, rotorAirgapRadius=rotorMBRadius
        )
        [slaveLinesStator, slavelinesRotor] = createSecondaryLines(
            statorPrimaryLines=primaryLinesStator,
            rotorPrimaryLines=primarylinesRotor,
            symFactor=symFactor,
        )
        # primarylines
        rotorPhysicals.append(PrimaryLine("primaryLineR", primarylinesRotor))
        statorPhysicals.append(PrimaryLine("primaryLineS", primaryLinesStator))
        # Slavelines
        rotorPhysicals.append(SlaveLine("slaveLineR", slavelinesRotor))
        statorPhysicals.append(SlaveLine("slaveLineS", slaveLinesStator))

    # 2: Movingband
    ## Handling Airgap material for Movingband
    # machineSurfDict = createSurfaceDict(segmentSurfDict)
    try:
        if "StLu" in segmentSurfDict.keys():
            movingBandMaterial: Material = segmentSurfDict["StLu"].material
        elif "StLu1" in segmentSurfDict.keys():
            movingBandMaterial: Material = segmentSurfDict["StLu1"].material
        else:
            movingBandMaterial: Material = segmentSurfDict["StLu2"].material
    except KeyError:
        apiLogger.warning(
            """Stator-Airgap Surface-ID was not "StLu","StLu1" or "StLu2". """
            "Can't determine Airgap material! Using air instead."
        )
        movingBandMaterial = air
    except Exception as exept:
        raise exept
    [
        movingBandStator,
        movingBandRotorInner,
        movingBandRotorAuxList,
    ] = createMB(
        segmentSurfDict=segmentSurfDict,
        symFactor=symFactor,
        material=movingBandMaterial,
    )

    rotorPhysicals.append(movingBandRotorInner)  # rotor side of inner Movingband
    if movingBandRotorAuxList:  # MB_Rotor_a is not None if sym>1
        for movingBandAux in movingBandRotorAuxList:
            rotorPhysicals.append(movingBandAux)  # outer movingband if sym>1
    statorPhysicals.append(movingBandStator)  # stator side of inner movingband

    # 3: Outer-Limit
    outerLimitLines = getLimitLines(
        limitLineDict=OuterLimitLineDict,
        machineSurfList=segmentSurfDict,
        symFactor=symFactor,
    )
    if outerLimitLines is not None:
        statorPhysicals.append(LimitLine("outerLimit", outerLimitLines))
    else:
        msg = (
            "Could not find outer limit lines for boundary. "
            f"Make sure at least one of the surfaces {OuterLimitLineDict.keys()} exist!"
        )
        raise AttributeError(msg)
    # 4: Inner-Limit
    innerLimitLines = getLimitLines(
        limitLineDict=InnerLimitLineDict,
        machineSurfList=segmentSurfDict,
        symFactor=symFactor,
    )
    if innerLimitLines is not None:
        rotorPhysicals.append(LimitLine("innerLimit", innerLimitLines))
    else:
        # checkout if most inner surface has center point
        noInnerLimit = False
        # Extract valid inner limit keys from innerLimitLineDict:
        innerLimitSurfaceKeys = []
        for key in InnerLimitLineDict:
            if key in segmentSurfDict:
                innerLimitSurfaceKeys.append(key)
        # check if any of those surfaces contains the center point:
        for innerLimitIdExt in innerLimitSurfaceKeys:
            for point in segmentSurfDict[innerLimitIdExt].allPoints:
                if point.isEqual(globalCenterPoint):
                    noInnerLimit = True  # no inner limit line
                    break  # break inner point loop
            if noInnerLimit is True:
                # if the center point was found, break the outer loop too.
                break
        if not noInnerLimit:
            msg = (
                "Could not find inner limit lines for boundary. "
                "And most inner Surface ('Wel') did not contain center point. "
                f'Make sure at least one of the surfaces "{InnerLimitLineDict.keys()}" exist!'
            )
            raise AttributeError(msg)
    # # Plot
    # TODO: Add verbosity and plot this when debugging.
    # fig, ax = plt.subplots()
    # plot(primarylinesRotor + primaryLinesStator, fig=fig, color="b")
    # plot(slavelinesRotor + slaveLinesStator, fig=fig, color="r")
    # plot(movingBandStator.geometricalElement, fig=fig)
    # plot(movingBandRotorInner.geometricalElement, fig=fig)
    # plot(geoElemList(movingBandRotorAuxList), fig=fig, color=[0.4940, 0.1840, 0.5560])
    # plot((innerLimitLines), fig=fig, color=[0.4660, 0.6740, 0.1880])
    # plot((outerLimitLines), fig=fig, color=[0.4660, 0.6740, 0.1880])
    # ax.set_aspect("equal")
    # ax.xaxis.set_ticklabels([])
    # ax.yaxis.set_ticklabels([])
    # ax.grid(True)
    # fig.show()

    return statorPhysicals, rotorPhysicals


def geoElemList(physElemList: list[PhysicalElement]) -> list[Transformable]:
    """Create a list of geometrical elements (type Transformable) from a list of PhysicalElements"""
    geoList = []
    if isinstance(physElemList, list):
        for phys in physElemList:
            geoList.extend(phys.geometricalElement)
        return geoList
    if isinstance(physElemList, PhysicalElement):
        return physElemList
    raise ValueError(physElemList)


# ===================================== END BOUNDARY FUNCTIONS ====================================
