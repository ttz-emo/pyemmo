"""This module is about the model generation via json api"""
import json
from math import ceil
from typing import Dict, List, Literal, Tuple, Union

from numpy import pi, sign
from swat_em import datamodel

from ..script.geometry.airArea import AirArea
from ..script.geometry.airGap import AirGap
from ..script.geometry.circleArc import CircleArc
from ..script.geometry.line import Line
from ..script.geometry.magnet import Magnet
from ..script.geometry.physicalElement import PhysicalElement
from ..script.geometry.point import Point
from ..script.geometry.rotorLamination import RotorLamination
from ..script.geometry.slot import Slot
from ..script.geometry.spline import Spline
from ..script.geometry.statorLamination import StatorLamination
from ..script.geometry.surface import Surface
from ..script.geometry.transformable import Transformable
from ..script.material.material import Material
from . import importJSON, globalCenterPoint
from .SurfaceJSON import SurfaceAPI

# from .. import calc_phaseangle_starvoltageV2
# analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltageV2


def createLine(
    lineDict: Dict,
    meshLen: float,
    startPoint: Point,
    endPoint: Point,
) -> Union[Line, CircleArc, Spline]:
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
        if "MP" in mpName:
            # the point is the global center point
            assert globalCenterPoint.getCoordinate() == (
                lineDict["MpX"],
                lineDict["MpY"],
                lineDict["MpZ"],
            ), f"In line {lineName} the given center point '{mpName}' coordinates where not (0,0,0)"
            centerPoint = globalCenterPoint
        else:  # Point is not CenterPoint (0,0,0)
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
        controlPointCoords = (lineDict["MpX"], lineDict["MpY"], lineDict["MpZ"])
        controlPoint = Point(
            controlPointName,
            controlPointCoords[0],
            controlPointCoords[1],
            controlPointCoords[2],
            meshLen if meshLen else lineDict["MpMesh"],
        )
        line = Spline(
            name=lineName,
            startPoint=startPoint,
            endPoint=endPoint,
            controlPoints=[controlPoint],
            SplineType=1,
        )
    # else invalid linetype
    else:
        raise ValueError(
            f"Linetype '{lineType}' of line '{lineName}' not found. (Should be 'Arc' or 'Line')"
        )
    return line


def getSurfaceLineList(
    lineDictList: List[Union[Dict[str, float], Dict[str, str]]], meshLen: float = None
) -> List[Line]:
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
            f"mesh size has wrong type: {type(meshLen)}. Should be float, int or None."
        )
    lineList: List[Line] = []
    pointList: List[Point] = []
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
            assert startPoint.getCoordinate() == coordsP1, (
                f"Start point ({startPoint.name}) of last line {lineDict['LineName']}"
                "is NOT endpoint of previous line. Check line loop!"
            )
            endPoint = pointList[0]
            assert endPoint.getCoordinate() == coordsP2, (
                f"End point ({endPoint.name}) of last line ('{lineDict['LineName']}')"
                "in line loop is NOT startpoint of first line. Check line loop!"
            )
        else:
            # ATTENTION: StartPoint of new line must be EndPoint of last line
            startPoint = pointList[-1]
            # make sure the coordinates are correct
            assert startPoint.getCoordinate() == coordsP1, (
                f"End point ({startPoint.name}) of last line in line loop is NOT"
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
            f"""Failed to generate API surface for '{areaDict["Name"]}' due to following error:"""
        ) from exce
    return surf


def importMachineGeometry(geometryFile: str) -> Dict[str, SurfaceAPI]:
    """import one segment of the whole machine geometry from the geo.json file

    Args:
        geometryFile (str): File path to the json file containing the geometry information

    Returns:
        Dict[str, SurfaceAPI]: Segment Surface dict with short IDs (IdExt) as keys and
        SurfaceAPI objects as values
    """
    try:
        with open(geometryFile, encoding="utf-8") as jsonFile:
            machineGeoList = json.load(jsonFile)
    except FileNotFoundError as fnfe:
        raise fnfe
    except Exception as exept:
        raise exept
    else:
        # if no exceptions occured
        segmentSurfDict: Dict[str, SurfaceAPI] = dict()
        for area in machineGeoList:
            if isinstance(area, dict):
                # normal surface; no subtraction
                apiSurf: SurfaceAPI = createAPISurf(area)
                segmentSurfDict[apiSurf.getIdExt()] = apiSurf
            elif isinstance(area, list):
                mainSurf = createAPISurf(area.pop(0))
                for toolArea in area:
                    toolSurf = createAPISurf(toolArea)
                    mainSurf.cutOut(toolSurf)
                segmentSurfDict[mainSurf.getIdExt()] = mainSurf
            else:
                msg = (
                    "The type of an element in the area list imported from the"
                    f"geometry file ({geometryFile}) was neither dict or list."
                    f"Type is '{type(area)}'. Value is {area}"
                )
                raise ValueError(msg)
        return segmentSurfDict


def createSurfaceDict(surfList: List[SurfaceAPI]) -> Dict[str, SurfaceAPI]:
    """creates a Dict of SurfaceAPI objects from a List of SurfaceAPI (see
    :func:`importMachineGeometry() <pyemmo.api.modelJSON.importMachineGeometry>`).
    The dict-keys are the surface IDs (short names/abbriviations of the surface name).

    Args:
        surfList: (List[SurfaceAPI]): List of surface dicts extended from the geometry json file

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

    surfaceDict: Dict[str, SurfaceAPI] = {}
    for surf in surfList:
        if not isinstance(surf, SurfaceAPI):
            msg = f"The object in the surface list was not type 'SurfaceAPI', but '{type(surf)}'."
            raise ValueError(msg)
        surfID = surf.getIdExt()  # key is area ID
        surfaceDict[surfID] = surf
    return surfaceDict


# def createNewPointName(orgPointName: str, addPointName: str) -> str:
#     orgNameParts = orgPointName.split("_")
#     newName = orgNameParts.pop(0)  # add first part without underscore
#     for orgPart in orgNameParts:
#         newName += f"_{orgPart}"
#     addNameParts = addPointName.split("_")
#     for addPart in addNameParts:
#         if isinstance(addPart, str):
#             if addPart not in orgPointName:
#                 newName += f"_{addPart}"
#     return newName


def rotateDuplicate(geoObj: Transformable, angle: float) -> Transformable:
    """
    Create a copy of the give geometrical entity and rotate it by :attr:`angle`

    Args:
        geoObj (Transformable): Geometrical entity (Point, Line or Surface object)
        angle (float): Rotation angle in rad.

    Returns:
        Transformable: Copied and rotated geo object.
    """
    if angle != 0:  # if the rotation angle is not zero
        duplicatedGeoObj: Transformable = geoObj.duplicate()  # duplicate obj
        duplicatedGeoObj.rotateZ(globalCenterPoint, angle)  # rotate obj
        # if type(GeoObj) == Surface:
        #     replaceIdenticalLines(GeoObj, DuplicatedGeoObj)
        return duplicatedGeoObj
    # if the angle is zero: give back duplicate of the old surface
    return geoObj.duplicate()


def createMachineGeometryFromSegment(
    segmentSurfDict: Dict[str, SurfaceAPI], symFactor: int
) -> Dict[str, List[SurfaceAPI]]:
    """
    Generate (rotate and duplicate) all Surfaces of the machine from a segment (list of surfaces)
    and return them as surface-list

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): Segment Surface dict with short IDs (IdExt) as keys
            and SurfaceAPI objects as values.
        SymFactor (int): Symmetry factor to calculate the number of segments that should be
            generated

    Returns:
        Dict[str, List[SurfaceAPI]]: Dict of all surfaces (including the given ones by
        segmentSurfList, but with different Name), with IdExt as keys and list of SurfaceAPI
        as values.

    Raises:
        ValueError: If number of segments on (2*Pi / symFactor) is not an integer.
    """
    surfDict: Dict[str, List[SurfaceAPI]] = {}  # init surface dict
    for (
        surfIdExt,
        surf,
    ) in segmentSurfDict.items():  # iterate through machine surface segments
        nbrSegments = surf.getNbrSegments() / symFactor
        # make sure number of segments is an integer
        if not nbrSegments.is_integer():
            mssg = f"Number of segments (Quantity/SymFactor) must be even, but is: {nbrSegments}"
            raise ValueError(mssg)
        surfDict[surfIdExt] = []  # init list to append surfaces
        # rotate and duplicte the original surface segment nbrSegments times,
        # considering cutted surfaces (tools)
        for segmentNbr in range(0, int(nbrSegments)):
            # rotate and duplicate parent surface
            dupSurf: SurfaceAPI = rotateDuplicate(
                geoObj=surf,
                angle=segmentNbr * surf.getAngle(),
            )
            # set IdExt to SurfaceID + SegmentNbr
            newIdExt = surfIdExt + "_" + str(segmentNbr)
            dupSurf.setIdExt(newIdExt)
            # for each surface that should be subtracted from the parent surface
            for tool in surf.getTools():
                tool: SurfaceAPI = tool
                toolIdExt = tool.getIdExt()
                if toolIdExt not in surfDict:
                    surfDict[toolIdExt] = []
                # Rotate and duplicate tool surface
                dupToolSurf: SurfaceAPI = rotateDuplicate(
                    geoObj=tool,
                    angle=segmentNbr * surf.getAngle(),
                )
                # set name to SurfaceID + Segment number
                newToolID = toolIdExt + "_" + str(segmentNbr)
                dupToolSurf.setIdExt(newToolID)
                # cut the duplicated surface from the duplicated parent surface
                dupSurf.cutOut(dupToolSurf)
                # add the tool surf to the surf dict (to create physical elements later)
                surfDict[toolIdExt].append(dupToolSurf)
            surfDict[surfIdExt].append(dupSurf)
    return surfDict


def createPhysicalSurfaces(
    idExt: str, surfList: List[SurfaceAPI], rotorMBRadius: float, extendedInfo: dict
) -> Tuple[List[PhysicalElement], Literal["Rotor", "Stator"]]:
    """create a PhysicalElement (PhysicalSurface) from the given surface and determine the machine
    side (rotor or stator). The type of PhysicalElement (Slot, Magnet, Airgap,...) is determined by
    the surfaces external ID (IdExt). The machine side is determined via the given rotor
    moving band radius.

    Args:
        IdExt (str): Short ID of surface list.
        surf (SurfaceAPI): a surface of the machine geometry.
        rotorMBRadius (float): radius of the moving band line of the rotor side.
        extendedInfo (dict): dict with additional simulation information.
            E.g. Winding configuration, symmetry factor, rotational speed,...

    Returns:
        Tuple[List[PhysicalElement], Literal["Rotor", "Stator"]]:

        - List[PhysicalElement]: generated List of PhysicalElements. E.g. in case of slots, there
          will be a physical element for every slot. In the case of the rotor lamination, there will
          only be one PhysicalElement.
        - Literal["Rotor", "Stator"]]: machine side to correctly assign the pE to the Rotor or
          Stator object.
    """
    # determine if single point of surface is inside the Movingband radius, because if one point is
    # inside, all the others have to be too:
    machineSide = (
        "Rotor"
        if surfList[0].getCurve()[0].startPoint.calcDist() <= rotorMBRadius
        else "Stator"
    )

    if "StCu" in idExt:  # if is stator slot
        slots: List[Slot] = list()
        for surf in surfList:
            slot = createSlot(
                surf=surf, material=surf.getMaterial(), extendedInfo=extendedInfo
            )
            slots.append(slot)
        return slots, machineSide
    if "Mag" in idExt:  # if is magnet
        magList = list()
        for surf in surfList:
            mag = createMagnet(
                surf=surf,
                material=surf.getMaterial(),
                magType=importJSON.getMagDir(extendedInfo),
            )  # create magnet object
            magList.append(mag)
        return magList, machineSide
    if "Lu" in idExt:
        if "1" in idExt:
            airArea = AirArea(
                name=idExt,
                geometricalElement=surfList,
                material=surfList[0].getMaterial(),
            )
            return [airArea], machineSide
        airGap = AirGap(
            name=idExt,
            geometricalElement=surfList,
            material=surfList[0].getMaterial(),
        )
        return [airGap], machineSide
    # elif "RoCu" in surfName: # For ASM-Cage
    #     print(surfName)
    #     pass
    # elif "Pol" in surfName or "RoNut" in surfName: # Rotor lamination
    #     pass
    if any(identifier in idExt for identifier in ("Pol", "RoNut")):
        lam = RotorLamination(
            name=idExt, geometricalElement=surfList, material=surfList[0].getMaterial()
        )
        return [lam], machineSide
    if "StNut" in idExt:
        lam = StatorLamination(
            name=idExt, geometricalElement=surfList, material=surfList[0].getMaterial()
        )
        return [lam], machineSide
    physElem = PhysicalElement(
        name=idExt, geometricalElement=surfList, material=surfList[0].getMaterial()
    )
    physElem.setColor()  # set random color for all surfs
    # FIXME: Is it really necessary to return a list here? Seems to allway be just a PE...
    return [physElem], machineSide


def createMagnet(surf: SurfaceAPI, material: Material, magType: str) -> Magnet:
    """create a Magnet (PhysicalElement) object.
        The magnet name will be the surface IdExt.
        The magnetization direction is determined by the segment number. Segment number 0 will lead
        to a "south pole" magnet (south pole facing towards the airgap)

    Args:
        surf (SurfaceAPI): magnet geometry
        material (Material): material of the magnet. Shoud have Br defined!
        magType (str): magnetization type. Options are:

            * "parallel"
            * "radial"
            * "tangential"

    Returns:
        Magnet: The Magnet object generated from the above information.
    """
    # get segment number
    segmentNbr = surf.getIdExt().split("_")[1]
    # identify magnetization direction:
    magDir = 1 if (int(segmentNbr) + 1) % 2 else -1
    return Magnet(
        name=surf.getIdExt(),
        geoElements=[surf],
        material=material,
        magDirection=magDir,
        magType=magType,
        magVectorAngle=getMagVec(surf),
    )


def getMagVec(magSurface: Surface) -> float:
    """
    Get the basic magnetisation vector angle (normally perpendicular to longer edge) from
    a magnet surface.

    The Surface must contain two Points with name "S1" (inner magnet center point) and "S2" (outer
    magnet center point) to determine the magnetisation vector.
    The vector angle is determined by transforming the coordinates of point S1 to the origin
    (same translation for S2) and calculating the angle of point S2 to the x-axis.

    Args:
        magSurface (Surface): magnet surface geometry

    Returns:
        float: magnetization vector angle in radians within [0, 2*Pi]

    Raises:
        NameError: if S1 or S2 are not found in surfaces points.
    """
    magnetPointList = magSurface.getPoints()
    for point in magnetPointList:
        # S1 is inner magnet point, S2 is outer
        if "S1" in point.name:
            pInner = point.duplicate()
        elif "S2" in point.name:
            pOuter = point.duplicate()
    try:
        innerPointCoords = pInner.getCoordinate()
        # translate the outer point like the inner point would be in the coordinate center
        # by appliing a translation with vector \vec{-pInner}. Now the angle between the x-axis
        # and the outer point is the magnetisation vector
        if pOuter.translate(
            -innerPointCoords[0], -innerPointCoords[1], -innerPointCoords[2]
        ):
            # TODO: getAngleToX takes the center point as argument -> Verify thats working!
            return pOuter.getAngleToX()
    except NameError as exc:
        raise NameError("Could not find Magnet Points") from exc
    except Exception as exc:
        raise exc


def phase2angle(phaseChar: Literal["u", "v", "w"]) -> float:
    """returns the angle of a specific phase name in "UVW"

    * U = 0
    * V = :math:`\\frac{2\pi}{3}`
    * W = :math:`-\\frac{2\pi}{3}`

    Args:
        PhaseChar (str): char object for the phase name (phase ID). Should be "u", "v" or "w"

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


def getSlotInfo(slotSurfName: str) -> Tuple[int, int]:
    """Extract the slot side and the segement number from the slot surface name.

    Args:
        slotSurfName (str): name of the slot surface. Must be "StCu<slotSide>_<segmentNumber>"

    Raises:
        ValueError: If the identifier "StCu" is missing from the slot surface name.
        ValueError: If the stings for slot side and segment number extracted from the name are not
            pure decimal (are not only numbers).
        ValueError: If the values for slot side and segment number are not int.

    Returns:
        Tuple[int, int]:

        - slot side (0 or 1)
        - segment number as integer.
    """
    if "StCu" in slotSurfName:
        # split up the surface name to get Slot side (0 odr 1) and segmentNbr (n)
        [slotSide, segmentNbr] = slotSurfName.lstrip("StCu").split("_")
        # if both stings are numbers
        if slotSide.isdecimal() and segmentNbr.isdecimal():
            if float(slotSide).is_integer() and float(segmentNbr).is_integer():
                return int(slotSide), int(segmentNbr)  # return the int value
            msg = f"slotSide ({slotSide}) and/or segmentNbr ({segmentNbr}) are not integers!"
            raise ValueError(msg)
        msg = (
            f"Could not determine Slot infomations"
            f"slotSide ({slotSide}) and/or segmentNbr ({segmentNbr}) are not decimal!"
        )
        raise ValueError(msg)
    msg = f'Slot identifier "StCu" was not in Surfacename: {slotSurfName}'
    raise ValueError(msg)


def createSlot(surf: SurfaceAPI, material: Material, extendedInfo: dict) -> Slot:
    """create a Physical Element of type Slot.

    Args:
        surf (SurfaceAPI): Slot geometric surface. Surface IdExt must be formatted like
            "StCu<slotSide>_<segmentNumber>". E.g. The first slot side of the first
            segment must be named "StCu0_0".
        material (Material): Slot Material.
        extendedInfo (dict): Additional model information dict, with winding configuration.

    Returns:
        Slot: Slot object generated from the above information.
    """
    slotSide, segmentNbr = getSlotInfo(surf.getIdExt())
    windList = importJSON.getWindingList(extendedInfo)
    # modulo operation to repeat the winding sequence
    windIndex = (2 * segmentNbr + slotSide % 2) % (len(windList))  # + 1)
    cDir = windList[windIndex][0]  # Current direction ('+' or '-')
    phase = windList[windIndex][1]  # Phase ID (U,V,W)
    slotName = surf.getIdExt() + "_" + phase.upper() + ("p" if cDir == "+" else "n")
    slot = Slot(
        name=slotName, geometricalElement=[surf], material=material
    )  # create slot without winding information, because winding is set by stator
    surf.setMeshColor(phase2color(phase))
    return slot


def createWinding(extendedInfo: dict) -> datamodel:
    """Create a `swat_em <https://swat-em.readthedocs.io/en/latest/#>`__ :class:`datamodel`
    object for the stator winding by the information given in the extended info dict.

    Args:
        extendedInfo (dict): dict with extended machine and simulation information.

    Returns:
        datamodel: swat_em.datamodel object of winding.
    """
    winding = datamodel()
    nbrSlots = importJSON.getNbrSlots(extendedInfo)
    nbrPolePairs = importJSON.getNbrPolePairs(extendedInfo)
    winding.set_machinedata(Q=nbrSlots, p=nbrPolePairs, m=3)
    # get winding layout from json file
    windList = importJSON.getWindingList(extendedInfo)
    symFactor = importJSON.getSymFactor(extendedInfo)
    # format winding layout for swat_em
    windLayout = genWindLayoutSwatEM(
        windList, nbrSlots, bool((2 * nbrPolePairs / symFactor) % 2)
    )
    # print(windLayout)
    winding.set_phases(S=windLayout, turns=(importJSON.getNbrOfTurns(extendedInfo)))
    winding.analyse_wdg()  # analyse winding to make sure its valid and all parameters are set
    return winding


def genWindLayoutSwatEM(
    windingList: List[str], nbrSlots: int, onePole=False
) -> List[List[int]]:
    """generate winding layout for `swat_em <https://swat-em.readthedocs.io/en/latest/#>`__
    winding object (:class:`datamodel`)

    FIXME: the number of slot sides per slot is assumed to be 2 allways.

    Args:
        windingList (List[str]): Motor model winding layout (with symmetry) from json model info
            file, formatted as list of strings. For every slot, the sign of winding direction and the
            phase id (u,v or w) should be given. This should look something like:

            .. code ::

                "winding": ["+u","+u","-v","-v","+w","+w"]
    
        Qs (int): Total number of stator slots
        onePole (bool, optional): Flag if winding layout is only given for one pole, so the winding
            direction has to be reversed every time. Defaults to False.

    Returns:
        List[List[int]]: Winding layout formatted for swat-em phases attribute (see
        `this <https://swat-em.readthedocs.io/en/latest/reference.html#swat_em.datamodel.datamodel.set_phases>`__
        SWAT-EM method for more details)
    """
    # windType = "integer" if windingList[0::2]==windingList[1::2] else "fractional"
    # winding type is not of intrest because there will allways be 2 slot sides in one slot,
    # even if its a interger winding

    # FIXME: "number of slot sides" should be considered, instead of setting it to two by default
    nbrSlotsInList = len(windingList) / 2
    # number of times to repeat the winding sequence to get the values for all slots:
    nbrRepeat = nbrSlots / nbrSlotsInList
    if (
        nbrRepeat.is_integer() and nbrSlotsInList.is_integer()
    ):  # set them to int because swat_em-layout and range function only take int
        nbrRepeat = int(nbrRepeat)
        nbrSlotsInList = int(nbrSlotsInList)
    # if windType == "fractional":
    # winding layout with slot numbers like:
    # [Phase1[[upper slot side],[lower slot side]],Phase2[[...],[...]],Phase3[[...],[...]]]
    windLayout = [[[], []], [[], []], [[], []]]
    for segment in range(nbrRepeat):
        offset = segment * nbrSlotsInList  # slot number offset for repetition
        if onePole:
            # if there is only one pole in the model, then reverse winding direction for second
            # pole segment
            signChange = -1 if segment % 2 else 1
        else:
            signChange = 1
        for slotID, phaseID in enumerate(windingList):
            phaseID = phaseID.replace("u", "1")
            phaseID = phaseID.replace("v", "2")
            phaseID = phaseID.replace("w", "3")
            phaseNum = abs(int(phaseID)) - 1  # 0,1 or 2 for m=3 winding
            # actual slot number from 0...nbrSlots(=Qs)
            slotNum = int(ceil((slotID + 1) / 2) + offset)
            slotSide = (slotID) % 2  # 0 or 1 for left or right/upper or lower slot side
            # +1 or -1 direction of winding turns
            windDir = signChange * int(sign(int(phaseID)))
            windLayout[phaseNum][slotSide].append(windDir * slotNum)
    # elif windType == "integer":
    #     windLayout = [[],[],[]]
    #     for segment in range(nbrRepeat):
    #         offset = segment*nbrSlotsInList
    #         if onePole:
    #             signChange = (-1 if segment%2 else 1)
    #         for slotID, phaseID in enumerate(windingList):
    #             if slotID%2==0:
    #                 phaseID = phaseID.replace("u","1")
    #                 phaseID = phaseID.replace("v","2")
    #                 phaseID = phaseID.replace("w","3")
    #                 phaseNum = abs(int(phaseID))-1
    #                 slotNum = int(ceil((slotID+1)/2)+offset)
    #                 windDir = signChange*sign(int(phaseID))
    #                 windLayout[phaseNum].append(windDir*slotNum)
    # else:
    #     raise(ValueError("Winding type is not 'integer' or 'factional'"))
    return windLayout


# ==================================================================================================
# ======================================= END MODEL GENERATION =====================================
# ==================================================================================================
