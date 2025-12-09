#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

import logging

import gmsh
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

from ...definitions import DEFAULT_GEO_TOL
from ...functions.plot import plot
from ...script.geometry import physicalsDict
from ...script.geometry.circleArc import CircleArc
from ...script.geometry.limitLine import LimitLine
from ...script.geometry.line import Line
from ...script.geometry.movingBand import MovingBand
from ...script.geometry.physicalElement import PhysicalElement
from ...script.geometry.primaryLine import PrimaryLine
from ...script.geometry.slaveLine import SlaveLine
from ...script.geometry.transformable import Transformable
from ...script.gmsh import SurfDimTag
from ...script.gmsh.create_gmsh_curve import create_curve
from ...script.gmsh.gmsh_arc import GmshArc
from ...script.gmsh.gmsh_line import GmshLine
from ...script.gmsh.gmsh_point import GmshPoint
from ...script.gmsh.utils import (
    filter_curves_on_radius,
    filter_lines_at_angle,
    get_dim_tags,
    get_max_radius,
    get_min_radius,
)
from ...script.material.material import Material
from .. import air
from ..machine_segment_surface import MachineSegmentSurface
from . import STATOR_AIRGAP_IDEXT, globalCenterPoint


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
    segmentSurfDict: dict[str, MachineSegmentSurface],
    surfID: str,
    lineIDList: list[list[str] | str],
) -> tuple[list[Line], MachineSegmentSurface]:
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
        logger = logging.getLogger(__name__)
        logger.warning("Surface ID '%s' not found in machine surface list.", surfID)
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
    segmentSurfDict: dict[str, MachineSegmentSurface],
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
        dupLines: list[Line] = []
        angle = boundarySurface.angle
        # number of segments in symmetry:
        nbrSegments = boundarySurface.nbr_segments / symFactor
        for line in lineList:
            for i in range(1, int(nbrSegments)):
                dupLines.append(line.duplicate())
                dupLines[-1].rotateZ(angle=i * angle)
        return lineList + dupLines
    return None


############################## START MOVINGBAND CREATION ##############################


def createMBLines(
    movingBandLineDict: dict,
    segmentSurfDict: dict[str, MachineSegmentSurface],
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
    mb_lines_rotor: list[GmshArc], symFaktor: int, material=air
) -> list[MovingBand]:
    """
    createMBAux creates the outer Movingband lines of the rotor and add them to
    pyemmo-Movingband objects depended on symmetry.

    Args:
        mb_lines_rotor (List[Line]): Inner moving band lines to duplicate.
        symFaktor (int): Symmetry factor.
        material (Material): Moving band material. Defaults to ''Air''.

    Returns:
        List[MovingBand]: Auxilliary moving band list.
    """
    logger = logging.getLogger(__name__)

    mb_aux_list: list[MovingBand] = []
    sym_angle = 2 * np.pi / symFaktor
    # here order of for-loops had to be changed because for example for symFaktor=4
    # we need 3 auxiliary movingband (mb) objects, each containing the same number
    # of lines as the inner movingband
    nbr_mb_curves = len(mb_lines_rotor)
    mb_radius = mb_lines_rotor[0].radius
    mb_center_point = mb_lines_rotor[0].center

    logger.debug("Try to find boundary points of Rotor_MB_Line_1")
    p_on_x_axis = None
    p_on_sym_axis = None
    for curve in mb_lines_rotor:
        for p in curve.points:
            if np.isclose(p.getAngleToX(), 0, atol=DEFAULT_GEO_TOL):
                logger.debug("Found boundary point on x-axis: %s", p)
                p_on_x_axis = p
            elif np.isclose(p.getAngleToX(), sym_angle, atol=DEFAULT_GEO_TOL):
                logger.debug("Found boundary point on symmetry-axis: %s", p)
                p_on_sym_axis = p
        if p_on_x_axis is not None and p_on_sym_axis is not None:
            break

    logger.debug("Create outer movingband curves...")
    for i_band in range(1, symFaktor):  # for every symmetry part
        mb_lines_aux: list[GmshArc] = []  # re-init mb_lines_list

        # create curves individually since the duplicated instances cannot be
        # automatically removed by gmsh... This is only possible for instances of the
        # highest gemetrical order which is surfaces at this point!
        for i_curve in range(1, nbr_mb_curves + 1):
            p_end_angle = sym_angle * i_band + sym_angle / nbr_mb_curves * (i_curve)
            if i_band == 1 and i_curve == 1:
                # first curve of first band -> use interface point
                p_start = p_on_sym_axis
                p_end = GmshPoint.from_coordinates(
                    name=f"Movingband point {i_band+1}.{i_curve}",
                    coords=(
                        np.cos(p_end_angle) * mb_radius,
                        np.sin(p_end_angle) * mb_radius,
                    ),
                    meshLength=1,
                )
                # p_end = GmshPoint(p_end.id)
            elif i_band == symFaktor - 1 and i_curve == nbr_mb_curves:
                # final curve of last band -> use other interface point:

                if not mb_lines_aux:
                    # mb lines are empty -> there is only one MB curve per segment
                    p_start = mb_aux_list[-1].geo_list[-1].end_point
                else:
                    p_start = mb_lines_aux[-1].end_point  # start point is end point of
                    # last curve
                p_end = p_on_x_axis
            else:
                if not mb_lines_aux:
                    # mb lines are empty (e.g. second third mb curve when sym = 4)
                    # use last point of last curve in previous MovingBand object
                    p_start = mb_aux_list[-1].geo_list[-1].end_point
                else:
                    p_start = mb_lines_aux[-1].end_point
                p_end = GmshPoint.from_coordinates(
                    name=f"Movingband point {i_band+1}.{i_curve}",
                    coords=(
                        np.cos(p_end_angle) * mb_radius,
                        np.sin(p_end_angle) * mb_radius,
                    ),
                    meshLength=1,
                )
                # p_end = GmshPoint(p_end.id)
            logger.debug("Creating band arc %i for band %i", i_curve, i_band + 1)
            band_arc = GmshArc.from_points(
                name=f"rotor auxiliary movingband {i_band+1}.{i_curve}",
                start_point=p_start,
                center_point=mb_center_point,
                end_point=p_end,
            )
            mb_lines_aux.append(band_arc)
            # if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            #     plot(mb_lines_aux, fig=fig, tag=True)

        gmsh.model.occ.synchronize()  # need to sync before adding Physical
        logger.debug("Creating Movingband physical 'Rotor_Bnd_MB_%i'", i_band + 1)
        mb_aux_list.append(
            MovingBand(
                name=(physicalsDict["Rotor_MB_Line"] + f"_{str(i_band+1)}"),
                geo_list=mb_lines_aux.copy(),
                material=material,
                auxiliary=True,
            )
        )
    return mb_aux_list


def createMB(
    rotor_bnd_lines: list[GmshLine],
    stator_bnd_lines: list[GmshLine],
    symFactor: int,
    material: Material = air,
) -> tuple[MovingBand, MovingBand, list[MovingBand] | None]:
    """
    createMB generates all PyEMMO Movingband objects needed for a simulation.

    Args:
        TODO

    Returns:
        tuple:
        - MB_Stator (MovingBand): Stator movingband
        - MB_Rotor_inner (MovingBand): Inner part of the rotor moving band
        - MB_Rotor_Aux (List(MovingBand) or None): Outer (auxillary) part of the movingband
          or None if symFactor=1
    """
    logger = logging.getLogger(__name__)

    # get dim tags list of stator boundary lines (GmshLine):
    bnd_line_dim_tags = [(1, line.id) for line in stator_bnd_lines]

    logger.debug(
        "Filter stator movingband lines from stator boundary curve list by minimal radius: %f",
        get_min_radius(bnd_line_dim_tags),
    )
    mb_lines_stator = filter_curves_on_radius(
        stator_bnd_lines, get_min_radius(bnd_line_dim_tags)
    )

    if not mb_lines_stator:
        raise RuntimeError("Could not find stator movingband lines")

    # Get rotor movingband lines:
    # get dim tags list of ROTOR boundary lines (GmshLine):
    bnd_line_dim_tags = [(1, line.id) for line in rotor_bnd_lines]

    # filter ROTOR movingband lines.
    logger.debug(
        "Filter rotor movingband lines from boundary curve list by maximal radius: %f",
        get_max_radius(bnd_line_dim_tags),
    )
    # Must be the most outer (max. radius) lines in the boundary list:
    mb_lines_rotor = filter_curves_on_radius(
        rotor_bnd_lines, get_max_radius(bnd_line_dim_tags)
    )

    if not mb_lines_rotor:
        raise RuntimeError("Could not find rotor movingband lines")

    logger.debug("Create Stator Movingband...")
    mb_stator: MovingBand = MovingBand(
        name="Stator Movingband",
        geo_list=mb_lines_stator,
        material=material,
        auxiliary=False,
    )

    logger.debug("Create INNER Rotor Movingband 'Rotor_Bnd_MB_1'...")
    mb_rotor_inner: MovingBand = MovingBand(
        name=physicalsDict["Rotor_MB_Line"] + "_1",
        geo_list=mb_lines_rotor,
        material=material,
        auxiliary=False,
    )
    # Outer Movingband-lines
    if symFactor > 1:
        logger.debug("Create OUTER Rotor Movingband...")
        mb_rotor_ax = createMBAux(mb_lines_rotor, symFactor, material)
    else:
        mb_rotor_ax = None

    # This was unnecessary since remove_all_duplicates() just removes instances
    # belonging to highest order instances (= surfaces in our case)...
    # gmsh.model.occ.remove_all_duplicates()  # call to remove duplicate points of moving band interfaces

    if logger.getEffectiveLevel() <= logging.DEBUG - 1:
        logger.debug("Show moving band in gmsh...")
        gmsh.model.setVisibility(gmsh.model.getEntities(), False)  # disable all
        gmsh.model.setVisibility(get_dim_tags([mb_stator, mb_rotor_inner]), True, False)
        if mb_rotor_ax:
            gmsh.model.setVisibility(get_dim_tags(mb_rotor_ax), True, False)
        gmsh.option.setNumber("Geometry.CurveLabels", 1)
        # Show comment of what is displayed:
        v = gmsh.view.add("comments")
        gmsh.view.addListDataString(
            v,
            list(globalCenterPoint.coordinate),
            ["Displaying Movingband Physical curves"],
        )

        gmsh.model.occ.synchronize()
        gmsh.fltk.run()

        # Reset gmsh layout
        gmsh.view.remove(v)  # remove view
        gmsh.option.setNumber("Geometry.CurveLabels", 0)  # reset curve labels
    return mb_stator, mb_rotor_inner, mb_rotor_ax


############################### END MOVINGBAND CREATION ###############################


def getLimitLines(
    limitLineDict: dict[str, list[str]],
    machineSurfList: list[MachineSegmentSurface],
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


def get_rotor_stator_dim_tags(
    surf_dict: dict[str, list[MachineSegmentSurface]], rotor_mb_radius: float
) -> tuple[list[SurfDimTag], list[SurfDimTag]]:
    """
    Classifies Gmsh surfaces into rotor and stator based on their radius.

    This function sorts surfaces into rotor or stator categories by comparing their
    radius to the specified movingband (=airgap) radius.
    Surfaces with a radius greater than the boundary are categorized as stator;
    others are categorized as rotor.

    Args:
        surf_dict (dict[str, list[SurfaceAPI]]): Dictionary of surface lists.
        rotor_mb_radius (float): Radius used to distinguish between rotor and stator
            surfaces.

    Returns:
        tuple[list[SurfDimTag], list[SurfDimTag]]: Two lists of tuples:
            - Rotor gmsh surface tags.
            - Stator gmsh surface tags.

    Example:

    .. python:

        surf_dict = ... # SurfaceAPI dict
        rotor_mb_radius = 0.6
        rotor_tags, stator_tags = get_rotor_stator_dim_tags(surf_dict, rotor_mb_radius)
    """
    stator_dim_tags: list[SurfDimTag] = []
    rotor_dim_tags: list[SurfDimTag] = []
    for _, surflist in surf_dict.items():
        dim_tags = [(2, surf.id) for surf in surflist]
        if surflist[0].points[0].radius > rotor_mb_radius:
            stator_dim_tags.extend(dim_tags)
        else:
            rotor_dim_tags.extend(dim_tags)
    return rotor_dim_tags, stator_dim_tags


def get_boundary_line_list(surf_dim_tags: list[SurfDimTag]) -> list[GmshLine]:
    """
    Retrieves and constructs a list of boundary lines (Type ``GmshLine`` for a given set
    of surface dimension tags.

    This function uses Gmsh to find the combined boundary lines of the specified
    surfaces. Each boundary line is represented as a `GmshLine` object, which includes
    the line's tag and the start and end points as `GmshPoint` objects.

    Args:
        surf_dim_tags (list[SurfDimTag]): A list of tuples where each tuple
            represents a surface in Gmsh, consisting of the dimension (2 for surfaces)
            and the surface tag.

    Returns:
        list[GmshLine]: A list of `GmshLine` objects representing the boundary lines of
        the provided surfaces.

    Raises:
        AssertionError: If a dimension other than 1 (for lines) is encountered in the
            boundary retrieval process.

    Example:

    .. python:

        surf_dim_tags = [(2, 1)]  # Example surface tag
        boundary_lines = get_boundary_line_dict(surf_dim_tags)
        for line in boundary_lines:
            print(line)
    """
    boundary_dim_tags = gmsh.model.get_boundary(surf_dim_tags)
    # create a boundary line list:
    bnd_line_list = [create_curve(abs(l_tag)) for _, l_tag in boundary_dim_tags]
    return bnd_line_list


def get_primary_lines(bnd_line_list: list[GmshLine]) -> list[GmshLine]:
    """Get a list of primary lines from the list of boundary lines by filtering the
    lines that are on the x-axis (at angle 0.0°).
    The primary lines are removed from the list of boundary lines since the cannot be
    any other boundary.

    Args:
        bnd_line_list (list[GmshLine]): List of boundary lines.

    Raises:
        RuntimeError: If no primary lines could be found.

    Returns:
        list[GmshLine]: List of primary lines.
    """
    logger = logging.getLogger(__name__)

    logger.debug("Identifying primary lines on axis with angle 0°")
    primary_lines: list[GmshLine] = filter_lines_at_angle(bnd_line_list, 0.0)

    if not primary_lines:
        raise RuntimeError("Could not determine primary lines.")

    # remove used lines
    logger.debug("Removing found primary lines from remaining boundary")
    for gmsh_line in primary_lines:
        bnd_line_list.remove(gmsh_line)
    return primary_lines


def get_secondary_lines(
    bnd_line_list: list[GmshLine], sym_factor: int
) -> list[GmshLine]:
    """Get the secondary lines from a list of boundary lines by checking if they are on
    the axis given by: angle = 2 * pi / symmetry
    Function removes the identified lines from the list of boundary lines, since they
    cannot be any other boundary anymore!

    Args:
        bnd_line_list (list[GmshLine]): List of boundary lines.
        sym_factor (int): Symmetry factor.

    Raises:
        RuntimeError: If no secondary lines could be found.

    Returns:
        list[GmshLine]: List of secondary lines.
    """
    logger = logging.getLogger(__name__)

    logger.debug("Identifying primary lines on axis with angle %.1f", 360 / sym_factor)
    secondary_lines: list[GmshLine] = filter_lines_at_angle(
        bnd_line_list, angle=2 * np.pi / sym_factor
    )

    if not secondary_lines:
        raise RuntimeError("Could not determine secondary lines.")

    # remove used lines
    logger.debug("Removing found secondary lines from remaining boundary")
    for gmsh_line in secondary_lines:
        bnd_line_list.remove(gmsh_line)
    return secondary_lines


def get_boundaries(
    surf_dict: dict[str, list[MachineSegmentSurface]],
    symFactor: int,
    rotor_mb_radius: float,
) -> tuple[list[PhysicalElement], list[PhysicalElement]]:
    """TODO"""
    logger = logging.getLogger(__name__)

    is_inner_rotor = True  # FIXME: Adapt for outer rotor

    # Create lists for Stator and Rotor boundaries
    rotor_boundary: list[PhysicalElement] = []
    stator_boundary: list[PhysicalElement] = []

    # get dim_tag_list of rotor and stator surfaces:
    logger.debug(
        "Distinguish between rotor and stator surfaces by movingband raidus %.3f mm",
        rotor_mb_radius,
    )
    rotor_dim_tags, stator_dim_tags = get_rotor_stator_dim_tags(
        surf_dict, rotor_mb_radius
    )
    # get boundary dim tags for rotor:
    rotor_bnd_line_list = get_boundary_line_list(rotor_dim_tags)
    stator_bnd_line_list = get_boundary_line_list(stator_dim_tags)

    # 1. Get primary and secondary lines
    if symFactor > 1:
        logger.info("Identifying primary and secondary boundary lines on symmetry axes")
        rotor_boundary.append(
            PrimaryLine("Primary Line Rotor", get_primary_lines(rotor_bnd_line_list))
        )
        rotor_boundary.append(
            SlaveLine(
                "Secondary Line Rotor",
                get_secondary_lines(rotor_bnd_line_list, symFactor),
            )
        )
        stator_boundary.append(
            PrimaryLine("Primary Line Stator", get_primary_lines(stator_bnd_line_list))
        )
        stator_boundary.append(
            SlaveLine(
                "Secondary Line Stator",
                get_secondary_lines(stator_bnd_line_list, symFactor),
            )
        )
    # 2: Movingband
    logger.info("Creating Movingband boundary...")
    ## Handling Airgap material for Movingband
    logger.debug("Try to find moving band material from stator airgap.")
    try:
        movingBandMaterial: Material = surf_dict[STATOR_AIRGAP_IDEXT][0].material
    except KeyError:
        logger.warning(
            "Stator-Airgap Surface-ID was not '%s'. Can't determine Airgap material! "
            "Using air instead.",
            STATOR_AIRGAP_IDEXT,
            exc_info=True,
        )
        movingBandMaterial = air
    except Exception as exept:
        raise exept
    [
        movingBandStator,
        movingBandRotorInner,
        movingBandRotorAuxList,
    ] = createMB(
        rotor_bnd_lines=rotor_bnd_line_list,
        stator_bnd_lines=stator_bnd_line_list,
        symFactor=symFactor,
        material=movingBandMaterial,
    )

    rotor_boundary.append(movingBandRotorInner)  # rotor side of inner Movingband
    if movingBandRotorAuxList:  # MB_Rotor_a is not None if sym>1
        for movingBandAux in movingBandRotorAuxList:
            rotor_boundary.append(movingBandAux)  # outer movingband if sym>1
    stator_boundary.append(movingBandStator)  # stator side of inner movingband

    # remove movingband lines from remaining boundary -> only limit left
    for stator_mb_curve in movingBandStator.geo_list:
        stator_bnd_line_list.remove(stator_mb_curve)
    for rotor_mb_curve in movingBandRotorInner.geo_list:
        rotor_bnd_line_list.remove(rotor_mb_curve)

    # 3: Outer-Limit
    logger.info("Identifying outer limit curves...")
    if is_inner_rotor:
        # if rotor inside -> stator = outer limit
        if len(stator_bnd_line_list) != 0:
            logger.debug("Setting outer limit to remaining stator boundary curves!")
            stator_boundary.append(LimitLine("outerLimit", stator_bnd_line_list))

            logger.debug("Inner limit are remaining rotor boundary curves!")
            inner_limit_lines = rotor_bnd_line_list
        else:
            raise RuntimeError("Could not identify outer limit lines for boundary...")
    else:
        # outer rotor -> rotor = outer limit
        if len(rotor_bnd_line_list) != 0:
            # TODO: Test that this actually works!
            logger.debug("Setting outer limit to remaining rotor boundary curves!")
            rotor_boundary.append(LimitLine("outerLimit", rotor_bnd_line_list))

            logger.debug("Inner limit are remaining stator boundary curves!")
            inner_limit_lines = stator_bnd_line_list
        else:
            raise RuntimeError("Could not identify outer limit lines for boundary...")

    # 4: Inner-Limit
    if len(inner_limit_lines) != 0:
        # remaining lines of rotor or stator are inner limit lines
        rotor_boundary.append(LimitLine("innerLimit", inner_limit_lines))
    else:
        # No inner limit lines left, which means the center point is the inner limit.
        if symFactor > 1:
            logger.debug(
                "No remaining inner limit lines. "
                "Check primary and secondary boundary contain the center point..."
            )
            # To make sure: checkout if primary/secondary lines contain the center point
            found_center = False
            rotor_primary: PrimaryLine = rotor_boundary[0]
            assert (
                type(rotor_primary) == PrimaryLine
                and "rotor" in rotor_primary.name.lower()
            )
            for line in rotor_primary.geo_list:
                line: Line | CircleArc = line
                for point in line.points:
                    if point.isEqual(globalCenterPoint):
                        found_center = True
                        break  # break inner point loop
                if found_center:
                    # if the center point was found, break the outer loop too
                    logger.debug("Primary contains center point.")
                    break
            if not found_center:
                raise RuntimeError(
                    "Cound not identify inner limit lines AND "
                    "primary lines did not contain center point!"
                )
    if logger.getEffectiveLevel() <= logging.DEBUG - 1:
        # show boundary line plot
        fig, ax = plt.subplots()
        # get colors from colormap 'rainbow'
        colors = plt.cm.get_cmap("rainbow")(
            np.linspace(0, 1, len(rotor_boundary + stator_boundary)),1
        )
        # plot each boundary with own color
        for boundary, color in zip(rotor_boundary + stator_boundary, colors):
            plot([boundary], fig=fig, tag=True, color=color)
        
        ax.set_aspect("equal")
        ax.grid(True)
        ax.title("Model Boundary Curves")
        fig.show()

    return rotor_boundary, stator_boundary


def geoElemList(
    physElemList: list[PhysicalElement] | PhysicalElement,
) -> list[Transformable]:
    """Create a list of geometrical elements (type Transformable) from a list of PhysicalElements"""
    geoList = []
    if isinstance(physElemList, list):
        for phys in physElemList:
            geoList.extend(phys.geo_list)
        return geoList
    if isinstance(physElemList, PhysicalElement):
        return physElemList
    raise ValueError(physElemList)


# ===================================== END BOUNDARY FUNCTIONS ====================================
