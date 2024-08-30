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

from typing import Literal

# from matplotlib import pyplot as plt
# from ..functions.plot import plot
import gmsh
import numpy as np

from ...script.geometry import physicalsDict
from ...script.geometry.line import Line
from ...script.geometry.movingBand import MovingBand
from ...script.geometry.physicalElement import PhysicalElement
from ...script.geometry.primaryLine import PrimaryLine
from ...script.geometry.slaveLine import SlaveLine
from ...script.geometry.transformable import Transformable
from ...script.gmsh.gmsh_arc import CircleArc
from ...script.gmsh.gmsh_line import GmshLine
from ...script.gmsh.gmsh_point import GmshPoint
from ...script.material.material import Material
from .. import air
from .. import logger as apiLogger
from . import (
    RotorMBLineDict,
    StatorMBLineDict,
)
from .SurfaceJSON import SurfaceAPI


################################## MISC FUNCTIONS ######################################
def get_max_radius(dim_tags: list[tuple[Literal[0, 1, 2], int]]) -> float:
    """Get the maximal radius of a list of surface dim-tags.

    Args:
        surf_dim_tags (list[int]): List of surface dim tags, like ``(2, tag)``

    Returns:
        float: Maximal radius of bounding points.
    """
    max_radius = 0
    point_dim_tags = gmsh.model.get_boundary(dim_tags, recursive=True)
    for p_dim, p_tag in point_dim_tags:
        coords = gmsh.model.get_value(0, p_tag, [])
        radius = np.linalg.norm(coords)
        if radius > max_radius:
            max_radius = radius
    return max_radius


def get_min_radius(dim_tags: list[tuple[Literal[0, 1, 2], int]]) -> float:
    """Get the minimal radius of a list of surface dim-tags.

    Args:
        dim_tags (list[int]): List of dim tags, like ``(dim, tag)``

    Returns:
        float: Minimal radius of bounding points.
    """
    point_dim_tags = gmsh.model.get_boundary(dim_tags, recursive=True)
    min_radius = 1e18
    for p_dim, p_tag in point_dim_tags:
        assert p_dim == 0
        coords = gmsh.model.get_value(0, p_tag, [])
        radius = np.linalg.norm(coords)
        if radius < min_radius:
            min_radius = radius
    return min_radius


def filter_lines_on_radius(line_list: list[GmshLine], radius: float) -> list[GmshLine]:
    """Filter all lines from a list of lines that are TODO

    Args:
        line_list (list[Line]): List of (boundary) lines.
        radius (float): TODO.

    Returns:
        list[Line]: List of lines that are on the specified radius.
    """
    curved_lines = filter(lambda line: isinstance(line, CircleArc), line_list)
    lines_on_radius: list[Line] = []
    for line in curved_lines:
        # we need to check start and end point angle here because there could be a line
        # on the boundary that has the same vector-angle, but is no secondary line!
        if all(
            np.isclose(
                [
                    line.start_point.radius,
                    line.end_point.radius,
                ],
                [radius, radius],
                atol=1e-6,
            )
        ):
            lines_on_radius.append(line)
    return lines_on_radius


def filter_lines_at_angle(line_list: list[Line], angle: float) -> list[Line]:
    """Filter all lines from a list of lines that are on a specific ``angle`` to the
    x-axis in the xy-plane.

    Args:
        line_list (list[Line]): List of (boundary) lines.
        angle (float): Angle of axis in xy-plane to filter.

    Returns:
        list[Line]: List of lines that are on the specified axis.
    """
    straight_lines = filter(lambda line: type(line) in (Line, GmshLine), line_list)
    lines_at_angle: list[Line] = []
    for line in straight_lines:
        # we need to check start and end point angle here because there could be a line
        # on the boundary that has the same vector-angle, but is no secondary line!
        if np.isclose(
            [
                line.start_point.getAngleToX(),
                line.end_point.getAngleToX(),
            ],
            [angle, angle],
            atol=1e-6,
        ):
            lines_at_angle.append(line)
    return lines_at_angle


################################ END MISC FUNCTIONS ####################################


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
        dupLines: list[Line] = []
        angle = boundarySurface.angle
        # number of segments in symmetry:
        nbrSegments = boundarySurface.NbrSegments / symFactor
        for line in lineList:
            for i in range(1, int(nbrSegments)):
                dupLines.append(line.duplicate())
                dupLines[-1].rotateZ(angle=i * angle)
        return lineList + dupLines
    return None


############################## START MOVINGBAND CREATION ##############################


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


def createMBAux(mb_lines_rotor: list, symFaktor: int, material=air) -> list[MovingBand]:
    """
    createMBAux creates the outer Movingband lines of the rotor and add them to
    pyemmo-Movingband objects depended on symmetry

    Args:
        mb_lines_rotor (List[Line]): Inner moving band lines to duplicate.
        symFaktor (int): Symmetry factor.
        material (Material): Moving band material. Defaults to ''Air''.

    Returns:
        List[MovingBand]: Auxilliary moving band list.
    """
    mb_aux_list: list[MovingBand] = []
    sym_angle = 2 * np.pi / symFaktor
    # here order of for-loops had to be changed because for example for symFaktor=4
    # we need 3 auxiliary movingband (mb) objects, each containing the same number
    # of lines as the inner movingband
    for i in range(1, symFaktor):  # for every symmetry part
        mb_lines_aux: list[Line] = []  # re-init mb_lines_list
        # get dim tags of existing (inner) Movingband lines
        mb_line_dim_tags = [(1, line.tag) for line in mb_lines_rotor]
        # copy in gmsh (easier)
        new_dim_tags = gmsh.model.occ.copy(mb_line_dim_tags)
        # create GmshLine objects, rotate them and add them to line list:
        for dim, tag in new_dim_tags:
            assert dim == 1  # should be line
            mb_line = GmshLine(tag)
            mb_line.rotateZ(angle=i * sym_angle)
            mb_lines_aux.append(mb_line)
        mb_aux_list.append(
            MovingBand(
                name=(physicalsDict["Rotor_MB_Line"] + f"_{str(i+1)}"),
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
    # get dim tags list of stator boundary lines (GmshLine):
    bnd_line_dim_tags = [(1, line.tag) for line in stator_bnd_lines]
    # filter stator movingband lines:
    mb_lines_stator = filter_lines_on_radius(
        stator_bnd_lines, get_min_radius(bnd_line_dim_tags)
    )
    if not mb_lines_stator:
        raise RuntimeError(
            "Could not find stator movingband lines. Make sure the geometry contains"
            f" the surface(s): {StatorMBLineDict.keys()} with lines "
            f"{[mbPointNames for _, mbPointNames in StatorMBLineDict.items()]}"
        )
    # Get rotor movingband lines:
    # get dim tags list of ROTOR boundary lines (GmshLine):
    bnd_line_dim_tags = [(1, line.tag) for line in rotor_bnd_lines]
    # filter ROTOR movingband lines.
    # Must be the most outer (max. radius) lines in the boundary list:
    mb_lines_rotor = filter_lines_on_radius(
        rotor_bnd_lines, get_max_radius(bnd_line_dim_tags)
    )
    if not mb_lines_rotor:
        raise RuntimeError(
            "Could not find rotor movingband lines. Make sure the geometry contains"
            f" the surface(s): {RotorMBLineDict.keys()} with lines "
            f"{[mbPointNames for _, mbPointNames in RotorMBLineDict.items()]}"
        )

    mb_stator: MovingBand = MovingBand(
        name="Stator Movingband",
        geo_list=mb_lines_stator,
        material=material,
        auxiliary=False,
    )
    mb_rotor_inner: MovingBand = MovingBand(
        name=physicalsDict["Rotor_MB_Line"] + "_1",
        geo_list=mb_lines_rotor,
        material=material,
        auxiliary=False,
    )
    # Outer Movingband-lines
    if symFactor > 1:
        mb_rotor_ax = createMBAux(mb_lines_rotor, symFactor, material)
    else:
        mb_rotor_ax = None
    return mb_stator, mb_rotor_inner, mb_rotor_ax


############################### END MOVINGBAND CREATION ###############################


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


def get_rotor_stator_dim_tags(
    surf_dict: dict[str, list[SurfaceAPI]], rotor_mb_radius: float
) -> tuple[list[tuple[Literal[2], int]], list[tuple[Literal[2], int]]]:
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
        tuple[list[tuple[Literal[2], int]], list[tuple[Literal[2], int]]]: Two lists of tuples:
            - Rotor gmsh surface tags.
            - Stator gmsh surface tags.

    Example:

    .. python:

        surf_dict = ... # SurfaceAPI dict
        rotor_mb_radius = 0.6
        rotor_tags, stator_tags = get_rotor_stator_dim_tags(surf_dict, rotor_mb_radius)
    """
    stator_dim_tags: list[tuple[Literal[2], int]] = []
    rotor_dim_tags: list[tuple[Literal[2], int]] = []
    for _, surflist in surf_dict.items():
        dim_tags = [(2, surf.id) for surf in surflist]
        if surflist[0].points[0].radius > rotor_mb_radius:
            stator_dim_tags.extend(dim_tags)
        else:
            rotor_dim_tags.extend(dim_tags)
    return rotor_dim_tags, stator_dim_tags


def get_boundary_line_list(
    surf_dim_tags: list[tuple[Literal[2], int]]
) -> list[GmshLine]:
    """
    Retrieves and constructs a list of boundary lines (Type ``GmshLine`` for a given set
    of surface dimension tags.

    This function uses Gmsh to find the combined boundary lines of the specified
    surfaces. Each boundary line is represented as a `GmshLine` object, which includes
    the line's tag and the start and end points as `GmshPoint` objects.

    Args:
        surf_dim_tags (list[tuple[Literal[2], int]]): A list of tuples where each tuple
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
    # create a boundary line dict:
    bnd_line_list: list[GmshLine] = []
    for dim, l_tag in boundary_dim_tags:
        assert dim == 1
        # line_type = gmsh.model.get_type(1, l_tag)  # get curve type: 'Line' or 'Circle'
        point_tags = gmsh.model.get_boundary(dimTags=[(1, l_tag)])
        bnd_line_list.append(
            GmshLine(
                l_tag,
                GmshPoint(
                    point_tags[0][1], gmsh.model.get_value(0, point_tags[0][1], [])
                ),
                GmshPoint(
                    point_tags[1][1], gmsh.model.get_value(0, point_tags[1][1], [])
                ),
            )
        )
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
    primary_lines: list[GmshLine] = filter_lines_at_angle(bnd_line_list, 0.0)
    if not primary_lines:
        raise RuntimeError("Could not determine primary lines.")
    # remove used lines
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
    secondary_lines: list[GmshLine] = filter_lines_at_angle(
        bnd_line_list, angle=2 * np.pi / sym_factor
    )
    if not secondary_lines:
        raise RuntimeError("Could not determine secondary lines.")
    # remove used lines
    for gmsh_line in secondary_lines:
        bnd_line_list.remove(gmsh_line)
    return secondary_lines


def get_boundaries(
    surf_dict: dict[str, list[SurfaceAPI]], symFactor: int, rotor_mb_radius: float
) -> tuple[list[PhysicalElement], list[PhysicalElement]]:
    """TODO"""
    # Create lists for Stator and Rotor boundaries
    rotor_boundary: list[PhysicalElement] = []
    stator_boundary: list[PhysicalElement] = []

    # get dim_tag_list of rotor and stator surfaces:
    rotor_dim_tags, stator_dim_tags = get_rotor_stator_dim_tags(
        surf_dict, rotor_mb_radius
    )
    # get boundary dim tags for rotor:
    rotor_bnd_line_list = get_boundary_line_list(rotor_dim_tags)
    stator_bnd_line_list = get_boundary_line_list(stator_dim_tags)

    # 1. Get primary and secondary lines
    if symFactor > 1:
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
    ## Handling Airgap material for Movingband
    # machineSurfDict = createSurfaceDict(segmentSurfDict)
    try:
        if "StLu" in surf_dict.keys():
            movingBandMaterial: Material = surf_dict["StLu"][0].material
        elif "StLu1" in surf_dict.keys():
            movingBandMaterial: Material = surf_dict["StLu1"][0].material
        else:
            movingBandMaterial: Material = surf_dict["StLu2"][0].material
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

    # # 3: Outer-Limit
    # outerLimitLines = getLimitLines(
    #     limitLineDict=OuterLimitLineDict,
    #     machineSurfList=segmentSurfDict,
    #     symFactor=symFactor,
    # )
    # if outerLimitLines is not None:
    #     stator_boundary.append(LimitLine("outerLimit", outerLimitLines))
    # else:
    #     msg = (
    #         "Could not find outer limit lines for boundary. "
    #         f"Make sure at least one of the surfaces {OuterLimitLineDict.keys()} exist!"
    #     )
    #     raise AttributeError(msg)
    # # 4: Inner-Limit
    # innerLimitLines = getLimitLines(
    #     limitLineDict=InnerLimitLineDict,
    #     machineSurfList=segmentSurfDict,
    #     symFactor=symFactor,
    # )
    # if innerLimitLines is not None:
    #     rotor_boundary.append(LimitLine("innerLimit", innerLimitLines))
    # else:
    #     # checkout if most inner surface has center point
    #     noInnerLimit = False
    #     # Extract valid inner limit keys from innerLimitLineDict:
    #     innerLimitSurfaceKeys = []
    #     for key in InnerLimitLineDict:
    #         if key in segmentSurfDict:
    #             innerLimitSurfaceKeys.append(key)
    #     # check if any of those surfaces contains the center point:
    #     for innerLimitIdExt in innerLimitSurfaceKeys:
    #         for point in segmentSurfDict[innerLimitIdExt].allPoints:
    #             if point.isEqual(globalCenterPoint):
    #                 noInnerLimit = True  # no inner limit line
    #                 break  # break inner point loop
    #         if noInnerLimit is True:
    #             # if the center point was found, break the outer loop too.
    #             break
    #     if not noInnerLimit:
    #         msg = (
    #             "Could not find inner limit lines for boundary. "
    #             "And most inner Surface ('Wel') did not contain center point. "
    #             f'Make sure at least one of the surfaces "{InnerLimitLineDict.keys()}" exist!'
    #         )
    #         raise AttributeError(msg)
    # # # Plot
    # # TODO: Add verbosity and plot this when debugging.
    # # fig, ax = plt.subplots()
    # # plot(primarylinesRotor + primaryLinesStator, fig=fig, color="b")
    # # plot(slavelinesRotor + slaveLinesStator, fig=fig, color="r")
    # # plot(movingBandStator.geo_list, fig=fig)
    # # plot(movingBandRotorInner.geo_list, fig=fig)
    # # plot(geoElemList(movingBandRotorAuxList), fig=fig, color=[0.4940, 0.1840, 0.5560])
    # # plot((innerLimitLines), fig=fig, color=[0.4660, 0.6740, 0.1880])
    # # plot((outerLimitLines), fig=fig, color=[0.4660, 0.6740, 0.1880])
    # # ax.set_aspect("equal")
    # # ax.xaxis.set_ticklabels([])
    # # ax.yaxis.set_ticklabels([])
    # # ax.grid(True)
    # # fig.show()

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
