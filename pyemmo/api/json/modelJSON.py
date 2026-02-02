#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
import math
from typing import Literal

import gmsh
import numpy as np
from numpy import pi, sign
from swat_em import datamodel

from ...functions.phase import phase2color
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
from ...script.gmsh.gmsh_arc import GmshArc
from ...script.gmsh.gmsh_line import GmshLine
from ...script.gmsh.gmsh_point import GmshPoint
from ...script.gmsh.gmsh_spline import GmshSpline
from ...script.material.material import Material
from ..machine_segment_surface import MachineSegmentSurface
from . import (
    ROTOR_AIRGAP_IDEXT,
    ROTOR_BAR_IDEXT,
    ROTOR_LAM_IDEXT,
    ROTOR_MAG_IDEXT,
    STATOR_AIRGAP_IDEXT,
    STATOR_LAM_IDEXT,
    STATOR_SLOT_IDEXT,
    importJSON,
)
from .get_coilspan import get_min_coilspan

# from .. import calc_phaseangle_starvoltageV2
# analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltageV2


def createLine(
    lineDict: dict[str, GmshLine],
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
        centerPoint = GmshPoint.from_coordinates(
            name=mpName,
            coords=coordsMP,
            meshLength=meshLen if meshLen else lineDict["MpMesh"],
        )
        line = GmshArc.from_points(
            name=lineName,
            start_point=startPoint,
            center_point=centerPoint,
            end_point=endPoint,
        )
    elif lineType == "Line":
        line = GmshLine.from_points(
            name=lineName, start_point=startPoint, end_point=endPoint
        )
    elif lineType == "Bezier":
        # in json api Bezier curves can only have one control point yet!
        cp_name = lineDict["MpName"]
        # import control point coordinates
        cp_coords = (
            lineDict["MpX"],
            lineDict["MpY"],
            lineDict["MpZ"],
        )
        # create control point of spline
        # NOTE: We don't need to specify a mesh length since the point will not be part
        # of the model
        controlPoint = GmshPoint.from_coordinates(
            coords=cp_coords,
            name=cp_name,
        )
        line = GmshSpline.from_points(
            points=[startPoint, controlPoint, endPoint],
            name=lineName,
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
) -> list[GmshLine | GmshArc]:
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
    lineList: list[GmshLine | GmshArc] = []
    pointList: list[GmshPoint] = []
    for lineID, lineDict in enumerate(lineDictList):  # for each line in lineDict
        # import line-point coordinates
        # start point
        coordsP1 = (lineDict["ApX"], lineDict["ApY"], lineDict["ApZ"])
        # end point
        coordsP2 = (lineDict["EpX"], lineDict["EpY"], lineDict["EpZ"])
        startPoint = GmshPoint.from_coordinates(
            name=lineDict["ApName"],
            coords=coordsP1,
            meshLength=meshLen if meshLen else lineDict["ApMesh"],
        )
        pointList.append(startPoint)
        endPoint = GmshPoint.from_coordinates(
            name=lineDict["EpName"],
            coords=coordsP2,
            meshLength=meshLen if meshLen else lineDict["EpMesh"],
        )
        line = createLine(lineDict, meshLen, startPoint, endPoint)
        lineList.append(line)
    return lineList


def createAPISurf(areaDict: dict) -> MachineSegmentSurface:
    """create a MachineSegmentSurface object from a area dict imported via json.

    Args:
        areaDict (dict): dict with area information.

    Returns:
        MachineSegmentSurface: Created surface object

    Keys in area dict are the following (see MachineSegmentSurface definition for more details):

    - Name
    - IdExt
    - Lines
    - Material
    - Quantity
    - Angle
    - Meshsize
    """
    logger = logging.getLogger(__name__)
    logger.debug(
        "Create MachineSegmentSurface for area %s with:\n\tID = %s\n\t"
        "Number of segments = %.1f\n\tMaterial = %s",
        areaDict["Name"],
        areaDict["IdExt"],
        areaDict["Quantity"],
        areaDict["Material"]["name"],
    )
    surf = MachineSegmentSurface.from_curve_loop(
        name=areaDict["Name"],
        part_id=areaDict["IdExt"],  # get short area name ("IdExt") as dict key
        curve_loop=getSurfaceLineList(
            lineDictList=areaDict["Lines"], meshLen=areaDict["Meshsize"]
        ),
        material=importJSON.create_material(areaDict["Material"]),
        nbr_segments=areaDict["Quantity"],
    )
    return surf


def importMachineGeometry(
    machineGeoList: list[dict | list[dict]],
) -> dict[str, MachineSegmentSurface]:
    """import one segment of the whole machine geometry from the geo.json file

    Args:
        machineGeoList (list[dict]): List of surface dictionaries with api geo info.
        TODO: describe surface dict structure!

    Returns:
        Dict[str, MachineSegmentSurface]: Segment Surface dict with short IDs (IdExt) as keys and
        MachineSegmentSurface objects as values
    """
    logger = logging.getLogger(__name__)
    segmentSurfDict: dict[str, MachineSegmentSurface] = {}
    for area in machineGeoList:
        if isinstance(area, dict):
            # normal surface; no subtraction
            logger.debug("Creating surface '%s' without tools", area["Name"])
            apiSurf = createAPISurf(area)
            segmentSurfDict[apiSurf.part_id] = apiSurf
        elif isinstance(area, list):
            logger.debug("Creating surface '%s' with tools", area[0]["Name"])
            logger.debug("Main surface is '%s'. Tool surfaces are:", area[0]["Name"])
            # pylint: disable=expression-not-assigned
            [logger.debug("%i: %s", i, tool["Name"]) for i, tool in enumerate(area[1:])]

            area: list[dict] = area
            # TODO: add multi layer subtraction here!
            main_surf = createAPISurf(area.pop(0))
            # # The tools can have a different symmtery than the main surface. To account
            # # for that, we need to determine number of segements of the main surface
            # # that need to be duplicated for the tools to be cut out:
            # sym_factor = main_surf.nbr_segments  # init sym factor
            # # calculate symmetry factor for all tools:
            # for nbr_segments in [tool_area["Quantity"] for tool_area in area]:
            #     sym_factor = np.gcd(sym_factor, nbr_segments)
            # # calc number of segments to fullfill symmetry:
            # nbr_main_segments = main_surf.nbr_segments / sym_factor
            # assert float(nbr_main_segments).is_integer()
            # new_quantity = sym_factor
            # # rotate and duplicate main surface and previous cut out tools:
            # for i in range(1, int(nbr_main_segments)):
            #     dup_main_surf = main_surf.rotate_duplicate(i)
            #     # fuse main surface:
            #     out_dim_tags, out_dim_tags_map = gmsh.model.occ.fuse(
            #         [(2, main_surf.id)], [(2, dup_main_surf.id)]
            #     )
            #     # update surface ids:
            #     main_surf.id = out_dim_tags[0][1]
            # # update nbr segements (angle updates automatically) of main surface
            # main_surf.nbr_segments = new_quantity

            if logger.getEffectiveLevel() <= logging.DEBUG - 1:
                logger.debug(
                    "Surface: '%s' before subtraction of tools.", main_surf.name
                )
                gmsh.model.occ.synchronize()
                gmsh.fltk.run()
            for surf in area:
                logger.debug("Creating tool surface '%s'", surf["Name"])
                tool_area = createAPISurf(surf)
                # for segment in range(0, int(tool_area.nbr_segments / sym_factor)):
                #     dup_tool_surf = tool_area.rotate_duplicate(segment)
                #     main_surf.cutOut(dup_tool_surf)

                logger.debug(
                    "Subtracting tool surface '%s' from main surface %s",
                    tool_area.name,
                    main_surf.name,
                )
                main_surf.cutOut(tool_area)
                if logger.getEffectiveLevel() <= logging.DEBUG - 1:
                    # show model after each tool cut out
                    logger.debug(
                        "Surface %s after subtraction of tool '%s'.",
                        main_surf.name,
                        tool_area.name,
                    )
                    gmsh.model.occ.synchronize()
                    gmsh.fltk.run()
                for tool in main_surf.tools:
                    if not isinstance(tool, MachineSegmentSurface):
                        raise RuntimeError(
                            f"Created tool surface {tool} is not type 'MachineSegmentSurface'"
                        )

            # # correct values for nbrSegments in tools (angle updates automatically):
            # for surf in main_surf.tools:
            #     surf.nbrSegments = new_quantity
            # # update curve of main surface
            # gmsh.model.occ.synchronize()
            # gmsh_main_surf = GmshSurface(tag=main_surf.id)
            # main_surf.curve = gmsh_main_surf.curve

            segmentSurfDict[main_surf.part_id] = main_surf
        else:
            msg = (
                "The type of an element in the area list imported from the"
                f"geometry file was neither dict or list."
                f"Type is '{type(area)}'. Value is {area}"
            )
            raise ValueError(msg)
    if logger.getEffectiveLevel() <= logging.DEBUG - 1:
        logger.debug("Display imported machine geometry in Gmsh...")
        gmsh.model.setVisibility(gmsh.model.getEntities(2), True, False)
        gmsh.model.occ.synchronize()
        gmsh.fltk.run()
    return segmentSurfDict


def createSurfaceDict(
    surfList: list[MachineSegmentSurface],
) -> dict[str, MachineSegmentSurface]:
    """creates a Dict of MachineSegmentSurface objects from a List of MachineSegmentSurface (see
    :func:`importMachineGeometry() <pyemmo.api.modelJSON.importMachineGeometry>`).
    The dict-keys are the surface IDs (short names/abbriviations of the surface
    name).

    Args:
        surfList: (List[MachineSegmentSurface]): List of surface dicts extended from the
            geometry json file

    Returns:
        Dict[str, MachineSegmentSurface]: Dict with surface ID as key

    Raises:
        ValueError: if surfList is not type list.
        ValueError: if a member of surfList is not type MachineSegmentSurface
    """
    if not isinstance(surfList, list):
        msg = (
            "The argument given for surface list was not list,"
            f"but {type(surfList)}. Should be a list!"
        )
        raise ValueError(msg)

    surfaceDict: dict[str, MachineSegmentSurface] = {}
    for surf in surfList:
        if not isinstance(surf, MachineSegmentSurface):
            msg = (
                "The object in the surface list was not type 'MachineSegmentSurface',"
                f" but '{type(surf)}'."
            )
            raise ValueError(msg)
        surfID = surf.part_id  # key is area ID
        surfaceDict[surfID] = surf
    return surfaceDict


def createMachineGeometryFromSegment(
    segmentSurfDict: dict[str, MachineSegmentSurface], symFactor: int
) -> dict[str, list[MachineSegmentSurface]]:
    """
    Generate (rotate and duplicate) all Surfaces of the machine from a segment
    (list of surfaces) and return them as surface-list

    Args:
        segmentSurfDict (Dict[str, MachineSegmentSurface]): Segment Surface dict with
            short IDs (IdExt) as keys and MachineSegmentSurface objects as values.
        SymFactor (int): Symmetry factor to calculate the number of segments
            that should be generated

    Returns:
        Dict[str, List[MachineSegmentSurface]]: Dict of all surfaces (including the
        ones from segmentSurfList, but with different Name and tool surfaces), with
        IdExt as keys and list of MachineSegmentSurface as values.

    Raises:
        ValueError: If number of segments on (2*Pi / symFactor) is not an
            integer.
    """
    logger = logging.getLogger(__name__)
    surf_dict: dict[str, list[MachineSegmentSurface]] = {}  # init surface dict
    # iterate through machine surface segments:
    for surf_id, surf in segmentSurfDict.items():
        nbrSegments = surf.nbr_segments / symFactor
        # make sure number of segments is an integer
        if not nbrSegments.is_integer():
            raise ValueError(
                f"Number of segments of surface '{surf_id}' must be even, but is: {nbrSegments}"
            )
        surf_dict[surf_id] = []  # init list to append surfaces
        # rotate and duplicte the original surface segment nbrSegments times
        if logger.getEffectiveLevel() <= logging.DEBUG:
            nbr_lines = len(gmsh.model.occ.get_entities(dim=1))
            nbr_surfs = len(gmsh.model.occ.get_entities(dim=2))
            logger.debug("nbr_lines = %i", nbr_lines)
            logger.debug("nbr_surfs = %i", nbr_surfs)

        logger.debug("Rotating and duplicating %s %i times", surf.name, nbrSegments)
        for segment_nbr in range(0, int(nbrSegments)):
            # rotate_duplicate also considers the tools automatically
            surf_dict[surf_id].append(surf.rotate_duplicate(segment_nbr))

            ### update surf dict with tool surfaces
            tools: list[MachineSegmentSurface] = surf_dict[surf_id][-1].tools
            for tool in tools:
                if tool.part_id in surf_dict:
                    surf_dict[tool.part_id].append(tool)
                else:
                    surf_dict[tool.part_id] = [tool]

    if logger.getEffectiveLevel() <= logging.DEBUG - 1:
        logger.debug(
            "Show final machine geometry after rotation and duplication of segments..."
        )
        gmsh.model.occ.synchronize()
        gmsh.fltk.run()
    return surf_dict


def createPhysicalSurfaces(
    part_id: str,
    surfList: list[MachineSegmentSurface],
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
        surf (MachineSegmentSurface): a surface of the machine geometry.
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
    logger = logging.getLogger(__name__)
    # determine if single point of surface is inside the Movingband radius,
    # because if one point is inside, all the others have to be too.
    # FIXME: This assumes all machine are inner rotor!
    machineSide = (
        "Rotor" if surfList[0].points[0].calcDist() <= rotorMBRadius else "Stator"
    )

    logger.debug("Physical %s is on %s", part_id, machineSide)

    if STATOR_SLOT_IDEXT in part_id:  # if is stator slot
        logger.debug("Creating %s...", part_id)
        slots: list[Slot] = list()
        for surf in surfList:
            slot = createSlot(
                surf=surf, material=surf.material, extendedInfo=extendedInfo
            )
            slots.append(slot)
        return slots, machineSide
    if ROTOR_MAG_IDEXT in part_id:  # if is magnet
        logger.debug("Creating %s...", part_id)

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
    if part_id in (ROTOR_AIRGAP_IDEXT, STATOR_AIRGAP_IDEXT):
        # if "1" in idExt:
        #     airArea = AirArea(
        #         name=idExt,
        #         geo_list=surfList,
        #         material=surfList[0].material,
        #     )
        #     return [airArea], machineSide
        logger.debug("Creating airgap %s...", part_id)
        airGap = AirGap(
            name=part_id,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [airGap], machineSide
    if ROTOR_BAR_IDEXT in part_id:  # For ASM-Cage
        logger.debug("Creating rotor bars...")
        bars = [Bar(surf.part_id, surf, surf.material) for surf in surfList]
        return bars, machineSide

    if ROTOR_LAM_IDEXT in part_id:
        logger.debug("Creating rotor lamination...")

        lam = RotorLamination(
            name=part_id,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [lam], machineSide
    if STATOR_LAM_IDEXT in part_id:
        logger.debug("Creating stator lamination...")
        lam = StatorLamination(
            name=part_id,
            geo_list=surfList,
            material=surfList[0].material,
        )
        return [lam], machineSide
    logger.debug("Creating physical element %s...", part_id)
    physElem = PhysicalElement(
        name=part_id, geo_list=surfList, material=surfList[0].material
    )
    physElem.setColor()  # set random color for all surfs
    return [physElem], machineSide


def createMagnet(surf: MachineSegmentSurface, mat: Material, extInfo: dict) -> Magnet:
    """create a Magnet (PhysicalElement) object.
        The magnet name will be the surface IdExt.
        The magnetization direction is determined by the segment number.
        Segment number 0 will lead to a "south pole" magnet (south pole facing
        towards the airgap)

    Args:
        surf (MachineSegmentSurface): magnet geometry
        material (Material): material of the magnet. Shoud have Br defined!
        extInfo (dict): dict with additional simulation information.
            E.g. Winding configuration, symmetry factor, rotational speed,...

    Returns:
        Magnet: The Magnet object generated from the above information.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Creating magnet from surface %s", surf.name)

    # identify magnetization direction
    # first segment (segmentNbr=0) must be north pole for dq-Offset calculation
    # FIXME: There can be multiple segments for one pole!
    magDir = 1 if (surf.segment_nbr + 1) % 2 else -1  # 1: north/outwards
    logger.debug(
        "Magnetization direction for magnet with segment number %i is %i",
        surf.segment_nbr,
        magDir,
    )

    # get magentization angle from magAngle dict by idExt
    logger.debug(
        "Getting magnetization angle for part_id %s from extended info", surf.part_id
    )
    magAngle = importJSON.get_mag_angle(extInfo)[surf.part_id]
    mag_vector_angle = (
        magAngle + math.radians(360 / surf.nbr_segments) * surf.segment_nbr
    )
    logger.debug(
        "Magnetization vector angle for magnet %s on segment %i is %.3f°",
        surf.part_id,
        surf.segment_nbr,
        np.rad2deg(mag_vector_angle),
    )

    return Magnet(
        name=surf.part_id,
        geoElements=[surf],
        material=mat,
        magDirection=magDir,
        magType=importJSON.get_mag_type(extInfo),
        magVectorAngle=mag_vector_angle,
    )


def getSlotInfo(slotSurfName: str) -> int:
    """Extract the slot side from the slot surface name.

    Args:
        slotSurfName (str): name of the slot surface. Must be
            "stator slot<slotSide>"

    Raises:
        ValueError: If the identifier "stator slot" is missing from the slot surface
            name.
        ValueError: If the stings for slot side and segment number extracted
            from the name are not pure decimal (are not only numbers).

    Returns:
        int: slot side
    """
    logger = logging.getLogger(__name__)
    logger.debug("Identifying slot side from slot name: %s", slotSurfName)
    if STATOR_SLOT_IDEXT in slotSurfName:
        # split up the surface name to get Slot side (0 odr 1)
        slotSide = slotSurfName.lstrip(STATOR_SLOT_IDEXT)
        # if both strings are numbers
        if slotSide:  # if slotSide not empty
            if slotSide.isdecimal():  # string is int
                logger.debug("Slot side is: %s", slotSide)
                slotSide = int(slotSide)
            else:
                raise ValueError(
                    f"Slot side was not decimal. Slot name: '{slotSurfName}'"
                )
        else:
            # Slot side is empty -> there is one layer side
            logger.debug("Slot side is empty. Assuming single layer winding.")
            slotSide = 0  # 0 to index first/only winding layer
        return slotSide
    raise ValueError(
        f'Slot identifier "stator slot" was not in surface name: {slotSurfName}'
    )


def getSlotPhase(
    windingLayout: list[list[int]], slot_number: int, slot_side: int
) -> tuple[Literal["p", "n"], Literal["u", "v", "w"]]:
    """Gets the name (u, v, w) of the Phase with it's direction (+, -)

    Args:
        windingLayout (list[list[int]]): Winding layout formatted for swat-em
            phases attribute (see `this <https://swat-em.readthedocs.io/en/latest/reference.html#swat_em.datamodel.datamodel.set_phases>`__
            SWAT-EM method for more details)
        slot_number (int): Slot number of the slot surface. The slot number is increasing
            in circumferential direction from 1 to total number of slots.
        slot_side (int): Slot side 0 = right side or slot bottom;
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
    logger = logging.getLogger(__name__)
    if slot_side == 1 and windingLayout[0][1] == []:
        # if slot side is 1 but second side of winding layout is empty:
        logger.warning(
            "Slot side of %i was given, but only one layer in winding layout!",
            slot_side,
        )
        logger.warning("Resetting slot side to 0!")
        slot_side = 0
    elif slot_side > 1:
        raise ValueError(
            "Index of slot side in slot identifier must be 0 or 1! "
            "More than two layers per slot is not supported. "
            f"Identifier of stator slot must be '{STATOR_SLOT_IDEXT}0' or '{STATOR_SLOT_IDEXT}1'"
        )

    logger.info(
        "Getting phase index of slot %i for layer %i from winding layout...",
        slot_number,
        slot_side,
    )

    # find phase index for current slot number and slot side
    if all(phaseList[1] == [] for phaseList in windingLayout):
        # if second slot side is empty, create winding layout separatly because np does
        # not allow array size missmatch
        logger.debug("Second layer in winding layout is empty.")
        windingLayout = np.array([phaseList[0] for phaseList in windingLayout])
        phase_index, slot_index = np.where(np.abs(windingLayout) == slot_number)
    else:
        logger.debug("Second layer in winding layout is not empty.")
        windingLayout = np.array(windingLayout)
        phase_index, slot_index = np.where(
            np.abs(windingLayout[:, slot_side, :]) == slot_number
        )
    if phase_index.size == 0:
        raise RuntimeError("Could not determine phase index by slot number.")
    assert (
        phase_index.size == 1
    ), f"Slot index found multiple times in winding layout of slot side {slot_side}"

    phase = chr(
        117 + phase_index[0]
    )  # convert unicode u=117 + index -> char [u,v,w,...]

    if sign(windingLayout[phase_index[0], slot_side, slot_index[0]]) == 1:
        cDir = "p"
    else:
        cDir = "n"

    logger.debug(
        "slot number: %i || slot side: %i || phase: %s || direction: %s",
        slot_number,
        slot_side,
        phase,
        cDir,
    )
    return cDir, phase


def createSlot(
    surf: MachineSegmentSurface, material: Material, extendedInfo: dict
) -> Slot:
    """create a Physical Element of type Slot.

    Args:
        surf (MachineSegmentSurface): Slot geometric surface. Surface IdExt must be
            formatted like "stator slot<slotSide>". E.g. The first
            slot side of the first segment must be named "stator slot0".
        material (Material): Slot Material.
        extendedInfo (dict): Additional model information dict, with winding
            configuration.

    Returns:
        Slot: Slot object generated from the above information.
    """
    logger = logging.getLogger(__name__)
    Qs = importJSON.get_nbr_of_slots(extendedInfo)
    slotSide = getSlotInfo(surf.part_id)
    if slotSide > 1:
        # for the special case where a single stator segment is not symmetrical and has
        # multiple e.g. to slots with two slot sides each
        logger.warning(
            "Slot side %i is greater 1! "
            "This assumes you have more than one slot per given stator segment. "
            "Resetting slot side index to %i. ",
            slotSide,
            slotSide % 2,
        )
        slotSide = slotSide % 2
    windingLayout = importJSON.get_winding_layout(extendedInfo)

    # calculate the slot number from the slot surface position:
    # the slot number is the angular position divided by the slot pitch
    # calculate angle of slot surface center to x-axis:
    slot_angle = surf.calcCOG().getAngleToX()
    slot_pitch = 2 * pi / Qs  # calculate slot pitch
    # NOTE: need to add half slot pitch because slot angle is the center of the slot
    slot_nbr = (slot_angle + slot_pitch / 2) / slot_pitch  # calculate slot number
    logger.debug(
        "Slot index = Angle of slot / Slot pitch = %.3f / %.3f = %.3f",
        np.rad2deg(slot_angle),
        np.rad2deg(slot_pitch),
        slot_nbr,
    )

    cDir, phase = getSlotPhase(windingLayout, round(slot_nbr, 0), slotSide)

    slot_name = f"{surf.part_id}_{phase.upper()}{cDir}{surf.segment_nbr}"
    logger.debug("Slot name is: %s", slot_name)

    # create slot without winding information, because winding is set by stator
    slot = Slot(name=slot_name, geo_list=[surf], material=material)

    logger.debug("Setting slot color to %s", phase2color(phase))
    surf.mesh_color = phase2color(phase)

    return slot


def createWinding(
    extendedInfo: dict, segmentSurfDict: dict[str, list[MachineSegmentSurface]] = {}
) -> datamodel:
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
    logger = logging.getLogger(__name__)
    logger.debug("Creating SWAT-EM winding object...")
    swatemWinding = datamodel()  # init swat-em winding object
    Qs = importJSON.get_nbr_of_slots(extendedInfo)
    z_pp = importJSON.get_nbr_of_pole_pairs(extendedInfo)
    nbr_turns = importJSON.get_nbr_of_turns(extendedInfo)
    # if no winding config is given (which means windLayout = "auto"), try to create winding object
    windLayout = importJSON.get_winding_layout(extendedInfo)
    if windLayout == "auto":
        logger.info("Creating auto generated winding with SWAT-EM...")
        if not segmentSurfDict:
            raise ValueError(
                "Can not create winding object without geometry information!"
            )
        logger.debug("Trying to find number of layers from geometry...")
        # get number of slots in minimal model
        stator_slotsides = [
            item for key, item in segmentSurfDict.items() if STATOR_SLOT_IDEXT in key
        ]
        if not stator_slotsides:
            raise RuntimeError(
                "Missing slots from geometry dict! "
                "Can not determine number of layers for winding!"
                f"Make sure slot identifier has '{STATOR_SLOT_IDEXT}' in it"
            )
        nbr_slotsides = len(stator_slotsides)
        logger.debug("Number of slot sides given = %d", nbr_slotsides)
        # assert all slots have the same number of segments:
        if not all(
            slots[0].nbr_segments == stator_slotsides[0][0].nbr_segments
            for slots in stator_slotsides
        ):
            logger.warning(
                "Different number of segments for stator slots! "
                "Check created winding configuration carefully!"
                "Using %d slot segments",
                stator_slotsides[0][0].nbr_segments,
            )
        segments = stator_slotsides[0][0].nbr_segments
        # number of sides per slot = total number of slot sides / number of slots
        nbr_layers = nbr_slotsides * segments / Qs
        logger.debug("Found number of layers from geometry = %.1f.", nbr_layers)

        # call genwdg to create automatic winding config
        swatemWinding.genwdg(Q=Qs, P=2 * z_pp, m=3, layers=nbr_layers, turns=nbr_turns)
        extendedInfo["winding"] = swatemWinding.get_phases()  # reset winding config
    else:
        # create winding from given swat-em winding layout
        # set machine data of swat-em object
        swatemWinding.set_machinedata(Q=Qs, p=z_pp, m=3)
        # Since windLayout was not "auto" it must be formatted in swat-em winding layout
        # format.
        if len(windLayout) != 3:
            # check number of phases.
            # NOTE: For now this fails because in Script._createWindingDomains() method
            # the number of phases for the GetDP model is assumed to be 3! This is a open
            # task.
            raise NotImplementedError("PyEMMO can't handle phase numbers != 3 for now!")
        swatemWinding.set_phases(
            S=windLayout,
            turns=nbr_turns,
            w=get_min_coilspan(windLayout, Qs),
        )
    # analyse winding to make sure its valid and all parameters are set:
    swatemWinding.analyse_wdg()
    # make sure that number of parallel paths does not exceed max. possible
    # paths of winding:
    if max(
        swatemWinding.get_parallel_connections()
    ) < importJSON.get_nbr_of_parallel_paths(extendedInfo):
        logger.warning(
            """The given number of parallel windings paths (%i) exceeds
            possible paths of the winding layout (%i)!""",
            importJSON.get_nbr_of_parallel_paths(extendedInfo),
            max(swatemWinding.get_parallel_connections()),
        )

    return swatemWinding
