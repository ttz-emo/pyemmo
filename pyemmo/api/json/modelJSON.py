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
"""This module is about the model generation via json api"""

from __future__ import annotations

import logging
from math import radians
from typing import Literal

import gmsh
from numpy import pi, sign
from swat_em import datamodel

from ...script.geometry.airArea import AirArea
from ...script.geometry.airGap import AirGap
from ...script.geometry.bar import Bar
from ...script.geometry.circleArc import CircleArc, Line
from ...script.geometry.magnet import Magnet
from ...script.geometry.physicalElement import PhysicalElement
from ...script.geometry.rotorLamination import RotorLamination
from ...script.geometry.slot import Slot
from ...script.geometry.spline import Spline
from ...script.geometry.statorLamination import StatorLamination
from ...script.geometry.surface import Point
from ...script.material.material import Material
from .. import logger
from . import importJSON
from .get_coilspan import get_min_coilspan
from .SurfaceJSON import SurfaceAPI

# from .. import calc_phaseangle_starvoltageV2
# analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltageV2


def createLine(
    lineDict: dict,
    meshLen: float,
    startPoint: Point,
    endPoint: Point,
) -> Line | CircleArc | Spline:
    """This function creates a pyemmo line object from a given line dict. See
    :func:`getSurfaceLineList() <pyemmo.api.modelJSON.getSurfaceLineList>` for more infos
    about the line dict contents.
    Mesh length, start point, end point and potentially center point have been created before.

    Args:
        lineDict (Dict): Dict with all the line information.
        meshLen (float): Mesh Length of the surface, if given in the surface dict via json api.
        startPoint (Point): Start point of the line to create.
        endPoint (Point): End point of the line to create.

    Raises:
        ValueError: if "lineType" is neither "Arc", "Line" nor "Bezier"

    Returns:
        Line | CircleArc | Spline: newly created line
    """
    lineName = lineDict["LineName"]
    lineType = lineDict["Typ"]
    # if linetype is Arc
    if lineType == "Arc":
        # determine Centerpoint
        mpName = lineDict["MpName"]
        # import coordinates of Centerpoint for THIS arc
        coordsMP = (lineDict["MpX"], lineDict["MpY"], lineDict["MpZ"])
        centerPoint = Point(
            mpName,
            coordsMP[0],
            coordsMP[1],
            coordsMP[2],
            meshLen if meshLen else lineDict["MpMesh"],
        )
        line = CircleArc(lineName, startPoint, centerPoint, endPoint)
    elif lineType == "Line":
        line = Line(lineName, startPoint, endPoint)
    elif lineType == "Bezier":
        # in json api Bezier curves can only have one control point yet!
        controlPointName = lineDict["MpName"]
        # import control point coordinates
        controlPointCoords = (
            lineDict["MpX"],
            lineDict["MpY"],
            lineDict["MpZ"],
        )
        controlPoint = Point(
            controlPointName,
            controlPointCoords[0],
            controlPointCoords[1],
            controlPointCoords[2],
            meshLen if meshLen else lineDict["MpMesh"],
        )
        line = Spline(
            name=lineName,
            start_point=startPoint,
            end_point=endPoint,
            control_points=[controlPoint],
            spline_type=1,
        )
    # else invalid linetype
    else:
        raise ValueError(
            f"Linetype '{lineType}' of line '{lineName}' not found. (Should be 'Arc' or 'Line')"
        )
    return line


def getSurfaceLineList(
    lineDictList: list[dict[str, float] | dict[str, str]],
    meshLen: float = None,
) -> list[Line]:
    """
    This function takes a list of dicts with surface-line-information (lineloop structure)
    and generates a list of pyemmo :class:`Line <pyemmo.script.geometry.line.Line>` objects
    from that.

    If mesh length (meshLen) is given in meters, the mesh settings of the points itself will be
    overwritten.

    Args:
        lineDictList (List[Dict]): list of line dictionaries. Every value in the list is a dict
            of line parameters
        meshLen (float): mesh length parameter

    Returns:
        list(Line): Line list for given line loop structure.

    Raises:
        ValueError: If lineDictList if not a list
        ValueError: If lineDictList if not a list

    Line Parameters in lineloop struct are:

    - 'LineName'
    - 'Typ'
    - 'ApName'
    - 'ApX'
    - 'ApY'
    - 'ApZ'
    - 'ApMesh'
    - 'EpName'
    - 'EpX'
    - 'EpY'
    - 'EpZ'
    - 'EpMesh'
    - 'MpName'
    - 'MpX'
    - 'MpY'
    - 'MpZ'
    - 'MpMesh'

    .. - 'LineID'
    .. - 'Descript'
    .. - 'ApID'
    .. - 'ApDesc'
    .. - 'EpID'
    .. - 'EpDesc'
    .. - 'MpID'
    .. - 'MpDesc'
    """
    if not isinstance(lineDictList, list):
        raise ValueError(f"line dict list has wrong type: {type(lineDictList)}")
    if meshLen is not None and not isinstance(meshLen, (int, float)):
        raise ValueError(
            f"mesh size has wrong type: {type(meshLen)}. "
            "Should be float, int or None."
        )
    lineList: list[Line] = []
    pointList: list[Point] = []
    for lineID, lineDict in enumerate(lineDictList):  # for each line in lineDict
        # import line-point coordinates
        # start point
        coordsP1 = (lineDict["ApX"], lineDict["ApY"], lineDict["ApZ"])
        # end point
        coordsP2 = (lineDict["EpX"], lineDict["EpY"], lineDict["EpZ"])
        # Points
        if lineID == 0:
            startPoint = Point(
                lineDict["ApName"],
                coordsP1[0],
                coordsP1[1],
                coordsP1[2],
                meshLen if meshLen else lineDict["ApMesh"],
            )
            pointList.append(startPoint)
            endPoint = Point(
                lineDict["EpName"],
                coordsP2[0],
                coordsP2[1],
                coordsP2[2],
                meshLen if meshLen else lineDict["EpMesh"],
            )
            pointList.append(endPoint)
        elif lineID == len(lineDictList) - 1:
            # last line has allready two existing points. Start point is end point of last line.
            # End point is startpoint of first line.
            # endpoint of penultimate (vorletzte) line must be first point
            # of this line (==last line in curve loop)
            startPoint = pointList[-1]
            if not startPoint.coordinate == coordsP1:
                raise ValueError(
                    f"Start point ({startPoint.name}) of last line {lineDict['LineName']} "
                    "is NOT endpoint of previous line. Check line loop!"
                )
            endPoint = pointList[0]
            if not endPoint.coordinate == coordsP2:
                raise ValueError(
                    f"End point ({endPoint.name}) of last line ('{lineDict['LineName']}') "
                    "in line loop is NOT startpoint of first line. Check line loop!"
                )
        else:
            # ATTENTION: StartPoint of new line must be EndPoint of last line
            startPoint = pointList[-1]
            # make sure the coordinates are correct
            if not startPoint.coordinate == coordsP1:
                raise ValueError(
                    f"End point ({startPoint.name}) of last line in line loop is NOT "
                    f"startpoint of this line ('{lineDict['LineName']}'). Check line loop!"
                )
            endPoint = Point(
                lineDict["EpName"],
                coordsP2[0],
                coordsP2[1],
                coordsP2[2],
                meshLen if meshLen else lineDict["EpMesh"],
            )
            pointList.append(endPoint)
        line = createLine(lineDict, meshLen, startPoint, endPoint)
        lineList.append(line)
    return lineList


def createAPISurf(areaDict: dict) -> SurfaceAPI:
    """create a SurfaceAPI object from a area dict imported via json.

    Args:
        areaDict (dict): dict with area information.

    Returns:
        SurfaceAPI: Created surface object

    Keys in area dict are the following (see SurfaceAPI definition for more details):

    - Name
    - IdExt
    - Lines
    - Material
    - Quantity
    - Angle
    - Meshsize
    """
    try:
        surf = SurfaceAPI(
            name=areaDict["Name"],
            idExt=areaDict["IdExt"],  # get short area name ("IdExt") as dict key
            curves=getSurfaceLineList(
                lineDictList=areaDict["Lines"], meshLen=areaDict["Meshsize"]
            ),
            material=importJSON.createMaterial(areaDict["Material"]),
            nbrSegments=areaDict["Quantity"],
            angle=areaDict["Angel"],
            meshSize=areaDict["Meshsize"],
        )
    except Exception as exce:
        raise RuntimeError(
            f"""Failed to generate API surface for '{areaDict["Name"]}' """
            f"due to following error: {exce.args[0]}"
        ) from exce
    return surf


def importMachineGeometry(machineGeoList: list[dict]) -> dict[str, SurfaceAPI]:
    """import one segment of the whole machine geometry from the geo.json file

    Args:
        machineGeoList (list[dict]): List of surface dictionaries with api geo info.
        TODO: describe surface dict structure!

    Returns:
        Dict[str, SurfaceAPI]: Segment Surface dict with short IDs (IdExt) as keys and
        SurfaceAPI objects as values
    """
    segmentSurfDict: dict[str, SurfaceAPI] = {}
    for area in machineGeoList:
        if isinstance(area, dict):
            # normal surface; no subtraction
            apiSurf: SurfaceAPI = createAPISurf(area)
            segmentSurfDict[apiSurf.idExt] = apiSurf
        elif isinstance(area, list):
            # TODO: add multi layer subtraction here!
            mainSurf = createAPISurf(area.pop(0))
            for toolArea in area:
                toolSurf = createAPISurf(toolArea)
                mainSurf.cutOut(toolSurf)
            segmentSurfDict[mainSurf.idExt] = mainSurf
        else:
            msg = (
                "The type of an element in the area list imported from the"
                f"geometry file was neither dict or list."
                f"Type is '{type(area)}'. Value is {area}"
            )
            raise ValueError(msg)
    return segmentSurfDict


def createSurfaceDict(surfList: list[SurfaceAPI]) -> dict[str, SurfaceAPI]:
    """creates a Dict of SurfaceAPI objects from a List of SurfaceAPI (see
    :func:`importMachineGeometry() <pyemmo.api.modelJSON.importMachineGeometry>`).
    The dict-keys are the surface IDs (short names/abbriviations of the surface
    name).

    Args:
        surfList: (List[SurfaceAPI]): List of surface dicts extended from the
            geometry json file

    Returns:
        Dict[str, SurfaceAPI]: Dict with surface ID as key

    Raises:
        ValueError: if surfList is not type list.
        ValueError: if a member of surfList is not type SurfaceAPI
    """
    if not isinstance(surfList, list):
        msg = (
            "The argument given for surface list was not list,"
            f"but {type(surfList)}. Should be a list!"
        )
        raise ValueError(msg)

    surfaceDict: dict[str, SurfaceAPI] = {}
    for surf in surfList:
        if not isinstance(surf, SurfaceAPI):
            msg = (
                "The object in the surface list was not type 'SurfaceAPI',"
                f" but '{type(surf)}'."
            )
            raise ValueError(msg)
        surfID = surf.idExt  # key is area ID
        surfaceDict[surfID] = surf
    return surfaceDict


def createMachineGeometryFromSegment(
    segmentSurfDict: dict[str, SurfaceAPI], symFactor: int
) -> dict[str, list[SurfaceAPI]]:
    """
    Generate (rotate and duplicate) all Surfaces of the machine from a segment
    (list of surfaces) and return them as surface-list

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with
            short IDs (IdExt) as keys and SurfaceAPI objects as values.
        SymFactor (int): Symmetry factor to calculate the number of segments
            that should be generated

    Returns:
        Dict[str, List[SurfaceAPI]]: Dict of all surfaces (including the
        ones from segmentSurfList, but with different Name and tool surfaces), with
        IdExt as keys and list of SurfaceAPI as values.

    Raises:
        ValueError: If number of segments on (2*Pi / symFactor) is not an
            integer.
    """
    surf_dict: dict[str, list[SurfaceAPI]] = {}  # init surface dict
    # iterate through machine surface segments:
    for surf_id, surf in segmentSurfDict.items():
        nbrSegments = surf.NbrSegments / symFactor
        # make sure number of segments is an integer
        if not nbrSegments.is_integer():
            raise ValueError(f"Number of segments must be even, but is: {nbrSegments}")
        surf_dict[surf_id] = []  # init list to append surfaces
        # rotate and duplicte the original surface segment nbrSegments times
        if logging.getLogger().level <= logging.DEBUG:
            gmsh.model.occ.synchronize()
            nbr_lines = len(gmsh.model.get_entities(dim=1))
            nbr_surfs = len(gmsh.model.get_entities(dim=2))
            logging.debug(f"{nbr_lines = :3}")
            logging.debug(f"{nbr_surfs = :3}")
            # gmsh.fltk.run()
        logging.debug("Rotating and duplicating %s %i times", surf.name, nbrSegments)
        for segment_nbr in range(0, int(nbrSegments)):
            # rotate_duplicate also considers the tools automatically
            surf_dict[surf_id].append(surf.rotateDuplicate(segment_nbr))

            ### update surf dict with tool surfaces
            tools = surf_dict[surf_id][-1].tools
            while tools:
                new_tools = []  # init new tools
                for tool in tools:
                    if tool.idExt in surf_dict:
                        surf_dict[tool.idExt].append(tool)
                    else:
                        surf_dict[tool.idExt] = [tool]
                    # add tool tools to new tools if not empty
                    new_tools.extend(tool.tools)  # extent tools
                tools = new_tools
    # TODO: Add airgap creation if no airgap in given geometry
    if logging.getLogger().level <= logging.DEBUG:
        gmsh.model.occ.synchronize()
        # gmsh.fltk.run()
    return surf_dict


def createPhysicalSurfaces(
    idExt: str,
    surfList: list[SurfaceAPI],
    rotorMBRadius: float,
    extendedInfo: dict,
) -> tuple[list[PhysicalElement], Literal["Rotor", "Stator"]]:
    """create a PhysicalElement (PhysicalSurface) from the given surface and
    determine the machine side (rotor or stator). The type of PhysicalElement
    (Slot, Magnet, Airgap,...) is determined by the surfaces external ID
    (IdExt). The machine side is determined via the given rotor moving band
    radius.

    Args:
        IdExt (str): Short ID of surface list.
        surf (SurfaceAPI): a surface of the machine geometry.
        rotorMBRadius (float): radius of the moving band line of the rotor side.
        extendedInfo (dict): dict with additional simulation information.
            E.g. Winding configuration, symmetry factor, rotational speed,...

    Returns:
        Tuple[List[PhysicalElement], Literal["Rotor", "Stator"]]:

        - List[PhysicalElement]: generated List of PhysicalElements. E.g. in
          case of slots, there will be a physical element for every slot. In
          the case of the rotor lamination, there will only be one
          PhysicalElement.
        - Literal["Rotor", "Stator"]]: machine side to correctly assign the pE
          to the Rotor or Stator object.
    """
    # determine if single point of surface is inside the Movingband radius,
    # because if one point is inside, all the others have to be too.
    # FIXME: This assumes all machine are inner rotor!
    machineSide = (
        "Rotor"
        if surfList[0].curve[0].start_point.calcDist() <= rotorMBRadius
        else "Stator"
    )

    if "StCu" in idExt:  # if is stator slot
        slots: list[Slot] = list()
        for surf in surfList:
            slot = createSlot(
                surf=surf, material=surf.material, extendedInfo=extendedInfo
            )
            slots.append(slot)
        return slots, machineSide
    if "Mag" in idExt:  # if is magnet
        magList = list()
        for surf in surfList:
            # create magnet object
            mag = createMagnet(
                surf=surf,
                mat=surf.material,
                extInfo=extendedInfo,
            )
            magList.append(mag)
        return magList, machineSide
    if "Lu" in idExt:
        if "1" in idExt:
            airArea = AirArea(
                name=idExt,
                geo_list=surfList,
                material=surfList[0].material,
            )
            return [airArea], machineSide
        airGap = AirGap(
            name=idExt,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [airGap], machineSide
    if idExt == "RoCu":  # For ASM-Cage
        bars = [Bar(surf.idExt, surf, surf.material) for surf in surfList]
        return bars, machineSide

    if any(identifier in idExt for identifier in ("Pol", "RoNut")):
        lam = RotorLamination(
            name=idExt,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [lam], machineSide
    if "StNut" in idExt:
        lam = StatorLamination(
            name=idExt,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [lam], machineSide
    physElem = PhysicalElement(
        name=idExt, geo_list=surfList, material=surfList[0].material
    )
    physElem.setColor()  # set random color for all surfs
    return [physElem], machineSide


def createMagnet(surf: SurfaceAPI, mat: Material, extInfo: dict) -> Magnet:
    """create a Magnet (PhysicalElement) object.
        The magnet name will be the surface IdExt.
        The magnetization direction is determined by the segment number.
        Segment number 0 will lead to a "south pole" magnet (south pole facing
        towards the airgap)

    Args:
        surf (SurfaceAPI): magnet geometry
        material (Material): material of the magnet. Shoud have Br defined!
        extInfo (dict): dict with additional simulation information.
            E.g. Winding configuration, symmetry factor, rotational speed,...

    Returns:
        Magnet: The Magnet object generated from the above information.
    """

    # identify magnetization direction
    # first segment (segmentNbr=0) must be north pole for dq-Offset calculation
    magDir = 1 if (surf.segment_nbr + 1) % 2 else -1  # 1: north/outwards
    # get magentization angle from magAngle dict by idExt
    magAngle = importJSON.getMagAngle(extInfo)[surf.idExt]
    return Magnet(
        name=surf.idExt,
        geoElements=[surf],
        material=mat,
        magDirection=magDir,
        magType=importJSON.getMagDir(extInfo),
        magVectorAngle=magAngle + radians(360 / surf.NbrSegments) * surf.segment_nbr,
    )


def phase2angle(phaseChar: Literal["u", "v", "w"]) -> float:
    """returns the angle of a specific phase name in "UVW"

    * U = 0
    * V = :math:`\\frac{2\\pi}{3}`
    * W = :math:`-\\frac{2\\pi}{3}`

    Args:
        PhaseChar (str): char object for the phase name (phase ID).
            Should be "u", "v" or "w".

    Raises:
        ValueError: PhaseChar should only by U,V or W
        ValueError: PhaseChar should only habe length=1

    Returns:
        Angle (float): phase angle
    """
    # Case uvw
    if len(phaseChar) == 1:  # if string PhaseChar is only one char
        if phaseChar.lower() == "u":
            return 0
        if phaseChar.lower() == "v":
            return 2 * pi / 3
        if phaseChar.lower() == "w":
            return -2 * pi / 3
        raise ValueError(
            f'Phase ID "{phaseChar}" is not uvw! Can not determine phase angle!'
        )
    raise ValueError(f'Phase ID "{phaseChar}"is not a single character!', phaseChar)


def phase2color(
    phaseChar: Literal["u", "v", "w"]
) -> Literal["IndianRed", "Yellow", "Aquamarine"]:
    """Get gmsh mesh color name for a phase-character. See `gmsh colors
    <https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_11_0/src/common/Colors.h>`_
    for all available colors.

    Args:
        PhaseChar (Literal["u","v","w"]): Character defining the phase [u,v or w].

    Raises:
        ValueError: if the phase character is different from u,v or w.
        ValueError: if the length of the PhaseChar string is geater 1.

    Returns:
        Literal["IndianRed", "Yellow", "Aquamarine"]:

        - u = "IndianRed"
        - v = "Yellow"
        - w = "Aquamarine"
    """
    # Case uvw
    if len(phaseChar) == 1:  # if string PhaseChar is only one char
        if phaseChar.lower() == "u":
            return "Magenta"
        if phaseChar.lower() == "v":
            return "Yellow4"
        if phaseChar.lower() == "w":
            return "Cyan"
        raise ValueError(
            f'Phase ID "{phaseChar}" is not uvw! Can not determine phase angle!'
        )

    raise ValueError(f'Phase ID "{phaseChar}"is not a single character!', phaseChar)


def getSlotInfo(slotSurfName: str) -> int:
    """Extract the slot side from the slot surface name.

    Args:
        slotSurfName (str): name of the slot surface. Must be
            "StCu<slotSide>"

    Raises:
        ValueError: If the identifier "StCu" is missing from the slot surface
            name.
        ValueError: If the stings for slot side and segment number extracted
            from the name are not pure decimal (are not only numbers).

    Returns:
        int: slot side
    """
    if "StCu" in slotSurfName:
        # split up the surface name to get Slot side (0 odr 1)
        slotSide = slotSurfName.lstrip("StCu")
        # if both strings are numbers
        if slotSide:  # if slotSide not empty
            if slotSide.isdecimal():  # string is int
                slotSide = int(slotSide)
            else:
                raise ValueError(
                    f"Slot side was not decimal. Slot name: '{slotSurfName}'"
                )
        else:
            # Slot side is empty -> there is one layer side
            slotSide = 0  # 0 to index first/only winding layer
        return slotSide
    raise ValueError(f'Slot identifier "StCu" was not in surface name: {slotSurfName}')


def getSlotPhase(
    windingLayout: list[list[int]], segmentNbr: int, slotSide: int
) -> tuple[Literal["p", "n"], Literal["u", "v", "w"]]:
    """Gets the name (u, v, w) of the Phase with it's direction (+, -)

    Args:
        windingLayout (list[list[int]]): Winding layout formatted for swat-em
            phases attribute (see `this <https://swat-em.readthedocs.io/en/latest/reference.html#swat_em.datamodel.datamodel.set_phases>`__
            SWAT-EM method for more details)
        segmentNbr (int): Circumferderal model segment number starting with 0
            on the x-axis (first segment). Number increasing in math. positive
            direction.
        slotSide (int): Slot side 0 = right side or  slot bottom;
            1 = left side or slot opening. (Slot side can also be 2 or 3 but
            is merged into 0 and 1 by modulo operation. This is usefull when
            you have multiple slot side (>2) per lamination segment.)

    Returns:
        Literal['p','n']: Winding direction

            -   'p' = positiv = +z-direction
            -   'n' = negative = -z-direction

        Literal["u", "v", "w"]: Phase indicator

    Raises:
        ValueError: If phase index in windingLayout is not 0, 1 or 2.
        RuntimeError: If windingLayout is empty.

    """
    for phaseIndex, phaseList in enumerate(windingLayout):
        # for slotSideList in phaseList:
        for slotNumber in phaseList[slotSide % 2]:  # TODO: Test if multiple
            # layer winding is working.
            if abs(slotNumber) == segmentNbr + 1:
                if phaseIndex == 0:
                    phase = "u"
                elif phaseIndex == 1:
                    phase = "v"
                elif phaseIndex == 2:
                    phase = "w"
                else:
                    raise ValueError("PhaseIndex not 0, 1 or 2.")

                if sign(slotNumber) == 1:
                    cDir = "p"
                else:
                    cDir = "n"
                logger.debug(
                    "segment number: %i || slot side: %i || phase: %s || direction: %s",
                    segmentNbr,
                    slotSide,
                    phase,
                    cDir,
                )
                return cDir, phase
    raise RuntimeError("Could not determine phase index by slot number.")


def createSlot(surf: SurfaceAPI, material: Material, extendedInfo: dict) -> Slot:
    """create a Physical Element of type Slot.

    Args:
        surf (SurfaceAPI): Slot geometric surface. Surface IdExt must be
            formatted like "StCu<slotSide>_<segmentNumber>". E.g. The first
            slot side of the first segment must be named "StCu0_0".
        material (Material): Slot Material.
        extendedInfo (dict): Additional model information dict, with winding
            configuration.

    Returns:
        Slot: Slot object generated from the above information.
    """

    slotSide = getSlotInfo(surf.idExt)
    windingLayout = importJSON.getWindingList(extendedInfo)
    # slotSide is set 0 or 1 where the naming of slotSide is 1 or 2
    cDir, phase = getSlotPhase(windingLayout, surf.segment_nbr, slotSide)
    slotName = f"{surf.idExt}_{phase.upper()}{cDir}{surf.segment_nbr}"
    # create slot without winding information, because winding is set by stator
    slot = Slot(name=slotName, geo_list=[surf], material=material)
    surf.setMeshColor(phase2color(phase))
    return slot


def createWinding(extendedInfo: dict) -> datamodel:
    """Create a
    `swat_em <https://swat-em.readthedocs.io/en/latest/#>`__ :class:`datamodel`
    object for the stator winding by the information given in the extended
    info dict.

    Args:
        extendedInfo (dict): dict with extended machine and simulation
            information.

    Returns:
        datamodel: swat_em.datamodel object of winding.
    """
    swatemWinding = datamodel()
    nbrSlots = importJSON.getNbrSlots(extendedInfo)
    nbrPolePairs = importJSON.getNbrPolePairs(extendedInfo)
    swatemWinding.set_machinedata(Q=nbrSlots, p=nbrPolePairs, m=3)
    # get winding layout from json file
    # windList = importJSON.getWindingList(extendedInfo)
    # symFactor = importJSON.getSymFactor(extendedInfo)
    # format winding layout for swat_em
    windLayout = importJSON.getWindingList(extendedInfo)

    swatemWinding.set_phases(
        S=windLayout,
        turns=(importJSON.getNbrOfTurns(extendedInfo)),
        w=get_min_coilspan(windLayout, nbrSlots),
    )
    swatemWinding.analyse_wdg()  # analyse winding to make sure its valid and
    # all parameters are set
    # make sure that number of parallel paths does not exceed max. possible
    # paths of winding:
    if max(swatemWinding.get_parallel_connections()) < importJSON.getNbrParalellPaths(
        extendedInfo
    ):
        logger.warning(
            """The given number of parallel windings paths (%i) exceeds
            possible paths of the winding layout (%i)!""",
            importJSON.getNbrParalellPaths(extendedInfo),
            max(swatemWinding.get_parallel_connections()),
        )

    return swatemWinding
