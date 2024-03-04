"""pyemmo Script module"""

# make all annotations strings, to avoid import errors in type checking case
from __future__ import annotations
import os
import re

# import warnings
import logging
from math import pi
from os.path import abspath, join
from typing import TYPE_CHECKING, Dict, List, Literal, Tuple, Union
from numpy import rad2deg, where
from pygetdp import Function as FunctionGetDP
from pygetdp import Group as GroupGetDP
from pygetdp import PostOperation
from pygetdp.postoperation import PostopItem

from ..definitions import DEFAULT_GEO_TOL, MAIN_DIR
from ..functions.cleanName import cleanName, isValidFilename

# global domain dict to connect existing pyemmo Domains with domains for magstatdyn
from . import (
    boundaryDomainDict,
    default_param_dict,
    rotorDomainDict,
    statorDomainDict,
    versionStr,
)
from .geometry.domain import Domain
from .geometry.line import Line
from .geometry.magnet import Magnet
from .geometry.physicalElement import PhysicalElement
from .geometry.slot import Slot
from .geometry.surface import Surface
from .material.electricalSteel import ElectricalSteel

if TYPE_CHECKING:
    from .geometry.machineAllType import MachineAllType
    from .material.material import Material
    from .geometry.point import Point
    from .geometry.circleArc import CircleArc
    from .geometry.spline import Spline


class Script(object):
    """Eine Instanz der Klasse Script beinhaltet alle Informationen, die zum
    Erzeugen der .geo- und .pro-Skripte benötigt werden."""

    def __init__(
        self,
        name: str,
        scriptPath: str,
        simuParams: dict,
        machine: MachineAllType = None,
        resultsPath: str = "",
        factory: str = "Build-in",
    ):
        """
        Args:
            name (str): script name
            scriptPath (str): path, where the geo and pro scripts should be
                saved
            simuParams (dict): Dictionary with different simulation parameters

                - "INIT_ROTOR_POS" - initial rotor position mech °
                - "ANGLE_INCREMENT" - angular step size in mech °
                - "FINAL_ROTOR_POS" - final rotor position mech °
                - "Id_eff" - d-axis current in A
                - "Iq_eff" - q-axis current in A
                - "SPEED_RPM" - rotational speed in rpm

                optional:

                - "ParkAngOffset" - offset angle for park-transformation in
                    elec °
                - "NBR_PARALLEL_PATHS" - number of parallel winding paths
                - "CALC_MAGNET_LOSSES" - flag to calculate eddy current losses
                    in PMs
                - "ANALYSIS_TYPE"

                    - 0: static (default)
                    - 1: transient

            machine (Machine): pyemmo machine object for geometry and geometic
                parameters. Defaults to None.
            resultsPath (str, optional): path, where the simulation results
                should be stored. Defaults to a folder in scriptPath with name
                "res_{scriptName}".
            factory (str, optional): Geometry kernel for the geo file.
                Possible inputs are:

                - "Build-in" (default)
                - "OpenCASCADE"


        DEFAULT SimuParam Dict:

        .. code:: python
            {
                "SYM": {
                    "INIT_ROTOR_POS": 0.0,
                    "ANGLE_INCREMENT": 0.5,
                    "FINAL_ROTOR_POS": 90.0,
                    "Id_eff": 0,
                    "Iq_eff": 1,
                    "SPEED_RPM": 1000,
                    "ParkAngOffset": None,  # optional
                    "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient
                },
                "MAT": {
                    "TEMP_MAG": 20,
                }
            }
        """
        ###Name des Skriptes
        if isValidFilename(name):
            self.name = name
        else:
            raise ValueError(
                "Script name has invalid format! Make sure the Script name"
                + f"can be used as a filename! ('{name}')"
            )
        # set default simulation parameters
        self._simulationParameters = default_param_dict
        # update simulation parameters with user parameters
        for key, paramDict in simuParams.items():
            self._simulationParameters[key] = (
                default_param_dict[key] | paramDict
            )
        ### directory to save the model files
        self.scriptPath = scriptPath
        ### directory to save simulation results
        self.resultsPath = (
            abspath(resultsPath).replace("\\", "/")
            if resultsPath
            else abspath(join(scriptPath, "res_" + self.name)).replace(
                "\\", "/"
            )
        )
        ###Punkte in Gmsh-Syntax
        self.pointCode: str = "\n// Points\n"
        ###Alle erzeugten Punkte
        self.pointArray: List[Point] = []
        ###Alle Linien in Gmsh-Syntax
        self.curveCode: str = "\n// Lines and Curves\n"
        ###Alle erzeugten Linien
        self._curveList: List[Union[Line, CircleArc, Spline]] = []
        ###Alle Flächen in Gmsh-Syntax
        self.areaCode: str = "\n// Surfaces\n"
        ###Alle erzeugten Flächen
        self.areaArray: List[Surface] = []

        self.colorCode: str = ""  # code for mesh colors

        ###Alle erzeugenten Physicals in Gmsh-Syntax
        self.physicalElementCode: str = "\n// Physical Elements\n"
        ###Alle erzeugten Physicals
        self.physicalElementArray: List[PhysicalElement] = []

        ###Alle bereits erzeugten Materialien
        self.group = GroupGetDP()
        self._materialDict: Dict[str, List[List[int]]] = {
            "material": [],
            "physicalElemID": [],
        }
        self.functionMaterial = FunctionGetDP()
        self.functionMagnetisation = FunctionGetDP()

        self._postOperation: PostOperation = PostOperation()

        self.factory = factory  # gmsh geometry kernel

        ### FOR DEBUGGING ###
        self.nbrIdedentPoints: int = 0
        self.idedentPoints: List[Point] = []
        self.nbrIdedentLines: int = 0
        self.idedentLines: List[Union[Line, CircleArc, Spline]] = []
        ### END FOR DEBUGGING ###

        # add machine domains
        self._machine = machine  # do not set machine via setter function!
        if machine:
            self._addMachineDomains()
        # else
        #   machine is None...

    # -------------------------------------------------------------------------
    # ----------------- START OF GETTER AND SETTER FUNCTIONS ------------------
    # -------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """getter of Script name

        Returns:
            str: script name
        """
        return self._name

    @name.setter
    def name(self, newName: str):
        """setter of Script name

        Args:
            newName (str): new script name.
        """
        self._name = newName

    @property
    def scriptPath(self) -> str:
        """Get the path, where the model files (.geo & .pro) should be stored

        Returns:
            str: path where the model files should be stored
        """
        return self._scriptPath

    @scriptPath.setter
    def scriptPath(self, newScriptPath: os.PathLike):
        """setter of Script Path

        Args:
            newScriptPath (os.PathLike): New path to folder where ONELAB files
                should be stored.
        """
        self._scriptPath = newScriptPath

    @property
    def proFilePath(self) -> str:
        """Get the path to the resulting pro file named "ScriptName.pro"

        Returns:
            str: path to the pro Script file
        """
        return join(self.scriptPath, self.name + ".pro")

    @property
    def geoFilePath(self) -> str:
        """Get the path to the resulting geo file named "ScriptName.geo"

        Returns:
            str: path to the geo Script file
        """
        return join(self.scriptPath, self.name + ".geo")

    @property
    def machine(self) -> Union[MachineAllType, None]:
        """getter of machine object

        Returns:
            Union[MachineAllType, None]: actual machine object in script or
                None if no machine was given
        """
        return self._machine

    @machine.setter
    def machine(self, newMachine: MachineAllType):
        """Setter of machine attribute.
        You should not use setMachine because then basically everything would
        have to be recreated (Domains, Physicals, Geos,...) Rather generate new
        script...
        TODO: check this function and add test case.

        Args:
            machine (MachineAllType): machine to create in script.
        """
        logging.warning("Reset of machine in script '%s'!", self.name)
        # if isinstance(newMachine, MachineAllType):
        # self._machine = newMachine
        self.__init__(
            self.name,
            scriptPath=self.scriptPath,
            simuParams=self.simParams,
            machine=newMachine,
            resultsPath=self.resultsPath,
            factory=self.factory,
        )
        # else:
        # msg = f"Given parameter machine was not type machine, but '{type(newMachine)}'"
        # raise TypeError(msg)
        # reset attributes
        # self._resetGeometry()
        # self.group = GroupGetDP()  # reset group (= domains)
        # reset material attributes:
        # self.materialDict: Dict[str, List[List[int]]] = {
        #     "material": [],
        #     "physicalElemID": [],
        # }
        # self.functionMaterial = FunctionGetDP()
        # self.functionMagnetisation = FunctionGetDP()

        # # create new machine geometry
        # self._addMachineDomains()

    @property
    def resultsPath(self) -> str:
        """Getter of the attribute resPath
        (path where the simulation results are stored)"""
        return self._resPath

    @resultsPath.setter
    def resultsPath(self, resPath: str):
        """Setter of the attribute resPath"""
        self._resPath = resPath
        self._simulationParameters["SYM"]["PATH_RES"] = resPath

    @property
    def simParams(self) -> dict:
        """Getter of the attribute simulationParameters"""
        return self._simulationParameters

    @property
    def factory(self) -> str:
        """Getter of the attribute factory"""
        return self._factory

    @factory.setter
    def factory(self, factory: str):
        """Setter of the attribute factory"""
        if re.search(r"open[\s\-]?cascade", factory.lower()):
            self._factory = "OpenCASCADE"
        else:
            self._factory = "Build-in"
        # raise(ValueError(f"Given factory '{factory}' was not recognized!"))

    @property
    def materialDict(self) -> Dict[str, List[List[int]]]:
        """Retrun the material dict of the script

        Returns:
            Dict[str, List]: material dictionary having the structure:
                {
                    "material": [ListOfMaterials],
                    "physicalElemID":  [[physicalIDs],[physicalIDs],...]
                }
                Every material in the material list has a list of physical
                element IDs in the physicalElemID-List(=List of lists)
        """
        return self._materialDict

    @property
    def curveList(self) -> List[Union[Line, CircleArc, Spline]]:
        """get the list of curves in the script

        Returns:
            List[Union[Line,CircleArc,Spline]]: list of curves that have been
                added to the script
        """
        return self._curveList

    def _setCurveList(
        self, curveList: List[Union[Line, CircleArc, Spline]]
    ) -> None:
        """set the curve list of the script.

        Args:
            curveList (List[Union[Line,CircleArc,Spline]]): list of line to be
                set in the script

        Raises:
            ValueError: if curve list was not type "list"
            ValueError: if one element of curve list is not a line of child of
                class line
        """
        if isinstance(curveList, list):
            for curve in curveList:
                # check if the element of curveList is neither type "Line" nor
                # child-class of Line
                # (e.g. CircleArc)
                # if type(curve) != Line or Line not in type(curve).__bases__:
                if not isinstance(curve, Line):
                    msg = f"Element {curve} of given curve list is not type Line!"
                    raise ValueError(msg)
            # if all elements in curveList are valid lines -> set new line list
            self._curveList = curveList
            # TODO: normally the point list has to be renewed by now...
            # But the function should not be used anyway by now.
        else:
            raise (
                ValueError(
                    f"Given curve list object was not a list, but type '{type(curveList)}'!"
                )
            )

    @property
    def postOperation(self) -> PostOperation:
        """get the user defined PostOperations

        Returns:
            PostOperation
        """
        return self._postOperation

    @postOperation.setter
    def postOperations(self, postOperation: PostOperation) -> None:
        """set the user defined PostOperation

        Args:
            postOperation (PostOperation): PostOperation object
        """
        if isinstance(postOperation, PostOperation):
            self._postOperation = postOperation
            return None
        msg = (
            "Given object was not of type PostOperation: "
            + str(type(postOperation))
            + str(postOperation)
        )
        raise TypeError(msg)

    @property
    def postOperationNames(self) -> List[str]:
        """Get a list of GetDP PostOperation names defined in Script.

        Returns:
            List[str]: List of GetDP PostOperation Names
        """
        postOperation = self.postOperation
        return [POItem.Name for POItem in postOperation.items]

    # -------------------------------------------------------------------------
    # ------------------- END OF GETTER AND SETTER FUNCTIONS ------------------
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # -------------------------- START OF GEO FUNCTIONS -----------------------
    # -------------------------------------------------------------------------

    def _addPoint(self, point: Point) -> Union[Point, None]:
        """
        Adding Point to Script Object.

        The function returns the identical point if one was found otherwise
        None.
        """
        if not point.isDrawn():
            identicalPoint = self._testPoint(point)
            # Wenn return None -> kein identischer Punkt in der Liste gefunden
            if not identicalPoint:
                # add point to pointArray
                self.pointArray.append(point)
                point._todesmerker = True
                return None  # -> Punkt wird mit _printPoint() regulär erzeugt
            # return identicalPoint -> identischer Punkt gefunden
            self.nbrIdedentPoints += 1
            self.idedentPoints.append(point)
            return identicalPoint
        # point was allready drawn
        logging.debug(
            f"Point '%s' has allready been added to the script.", point.name
        )
        return None

    def _testPoint(
        self, testPoint: Point, tol: float = DEFAULT_GEO_TOL
    ) -> Union[Point, None]:
        """
        Tests if the coordinates of a given point match with those of a point
        allready existing in the point list of the script inside a given
        tolerance (tol). The function returns the identical point (from the
        point list) if one was found, otherwise None.

        Args:
            point (Point): Point to test against the point list
            tol (float): Tolerance radius (im meter) to check if
                points are equal

        Returns:
            Point or None: Identical point from the point list if one was found
        """
        for point in self.pointArray:
            if testPoint.isEqual(point, tol=tol):
                # Stop program at this stage and return identical point
                if point.meshLength > testPoint.meshLength:
                    point.meshLength = testPoint.meshLength
                return point
        return None

    def _testLine(self, line2Test: Line) -> Union[Line, None]:
        """checks if start or end point of the given curve of type Line are
        allready existing in the point list of the script and if the given line
        is identical with an existing line in the line list of the script. If
        start or end point are allready existing, they are replaced by the
        existing points.
        FIXME: If only a part of curve is overlapping an existing curve, its
        not recognized by the function!!!

        Args:
            line2Test (Line): New line that should be added to the script.

        Returns:
            Line | None: Identical Line if an existing Line was found,
                otherwise None.
        """
        curveList = self.curveList
        existingLines: List[Line] = []
        # getting all existing lines from _curveList
        for savedCurve in curveList:
            if savedCurve.type == "Line":
                existingLines.append(savedCurve)
        # getting points of tested line
        testPointDict = {"p1": line2Test.startPoint, "p2": line2Test.endPoint}
        # compare all points to the two test points
        for existingLine in existingLines:
            compareP = {
                "p1": existingLine.startPoint,
                "p2": existingLine.endPoint,
            }
            #!!! Testing for absolute identical points (name, id, ...)
            if (
                testPointDict["p1"] == compareP["p1"]
                or testPointDict["p1"] == compareP["p2"]
            ) and (
                testPointDict["p2"] == compareP["p1"]
                or testPointDict["p2"] == compareP["p2"]
            ):
                # Return identical Line, if one was found, exept for if the
                # line is forced:
                if line2Test.force:
                    # append the line even if it allready exists due to "force"
                    return None
                # return the in script existing curve
                ### For debugging ###
                self.nbrIdedentLines += 1
                # print(
                #     f"Found similar Line '{testArray[i].name}'"
                #     + f"to tested line '{curvename}' in testCurve"
                # )
                self.idedentLines.append(line2Test)
                ######
                return existingLine
        # If no identical line was found, return None to add the line to the
        # curve list.
        return None

    def _testCircleArc(self, curve: CircleArc) -> Union[CircleArc, None]:
        """checks if start point, end point and center point of the given curve
        of type CircleArc are equal to the points of an existing circle arc in
        the curve list of the script.
        FIXME: If only a part of curve is overlapping an existing curve, its
        not recognized by the function!!!

        Args:
            curve (CircleArc): New arc that should be added to the script

        Returns:
            CircleArc | None: Identical arc if an existing CircleArc was found,
                otherwise None
        """
        curveList = self.curveList
        existingArcs: List[CircleArc] = list()
        for savedCurve in curveList:
            if savedCurve.type == "CircleArc":
                existingArcs.append(savedCurve)
        testPointDict = {
            "p1": curve.startPoint,
            "p2": curve.endPoint,
            "c": curve.center,
        }
        for arc in existingArcs:
            comparePointDict = {
                "p1": arc.startPoint,
                "p2": arc.endPoint,
                "c": arc.center,
            }
            if (
                (
                    testPointDict["p1"] == comparePointDict["p1"]
                    or testPointDict["p1"] == comparePointDict["p2"]
                )
                and (
                    testPointDict["p2"] == comparePointDict["p1"]
                    or testPointDict["p2"] == comparePointDict["p2"]
                )
                and (testPointDict["c"] == comparePointDict["c"])
            ):
                if curve.force:
                    # if flag 'force' is set add the curve anyway
                    return None
                ### For debugging ###
                self.nbrIdedentLines += 1
                # print(
                #     f"Found similar CircleArc '{testArray[i].name}'"
                #     + f" to tested line {curve.name}' in testCurve"
                # )
                self.idedentLines.append(curve)
                ######
                # return identical CircleArc
                return arc
        # no identical curve found
        # return None to add Curve to global curve list
        return None

    def _testSpline(self, curve: Spline) -> Union[Spline, None]:
        """checks if start point, end point and control point list of the given
        curve of type Spline are equal to the points of an existing spline in
        the curve list of the script.
        FIXME: If only a part of curve is overlapping an existing curve, its
        not recognized by the function!!!

        Args:
            curve (Spline): New arc that should be added to the script

        Returns:
            Spline | None: Identical arc if an existing Spline was found,
                otherwise None
        """
        curveList = self.curveList
        existingSplines: List[Spline] = []
        for savedCurve in curveList:
            if savedCurve.type == "Spline":
                existingSplines.append(savedCurve)

        testPointDict = {
            "p1": curve.startPoint,
            "p2": curve.endPoint,
            "controlP": curve.controlPoints,
        }

        for spline in existingSplines:
            comparePointDict = {
                "p1": spline.startPoint,
                "p2": spline.endPoint,
                "controlP": spline.controlPoints,
            }
            if len(testPointDict["controlP"]) == len(
                comparePointDict["controlP"]
            ):
                # only continue if control point list length is equal
                if (
                    (
                        testPointDict["p1"] == comparePointDict["p1"]
                        or testPointDict["p1"] == comparePointDict["p2"]
                    )
                    and (
                        testPointDict["p2"] == comparePointDict["p1"]
                        or testPointDict["p2"] == comparePointDict["p2"]
                    )
                    and (
                        testPointDict["controlP"]
                        == comparePointDict["controlP"]
                    )
                ):
                    # if all start, end point and control point list are
                    # matching -> return identical spline
                    return spline
        # if no equal spline was found, return None to add it
        return None

    def testCurve(self, curve: Union[Line, CircleArc, Spline]):
        """
        checks if start or end point of the given line "curve" are allready
        existing in the point list of the script and if the given line "curve"
        is identical with an existing line in the line list of the script.
        If start or end point are allready existing, they are replaced by the
        existing points. If only a part of curve is overlapping an existing
        curve, its not recognized by the function.

        Args:
            curve (Line|CircleArc|Spline):  line to check start point, end
                point and the line itself on existance in the script.

        Returns:
            Line|CircleArc|Spline or None: Existing identical line, if one was
                found, or None.
        """
        # test line
        curveType = curve.type
        if curveType == "Line":
            testResult = self._testLine(curve)
        elif curveType == "CircleArc":
            testResult = self._testCircleArc(curve)
        elif curveType == "Spline":
            testResult = self._testSpline(curve)
        else:
            msg = f"Curve type of {curve} is unknown."
            raise TypeError(msg)
        return testResult

    def _addCurve(
        self, curve: Union[Line, CircleArc, Spline]
    ) -> Union[None, Line]:
        """
        The function _addCurve checks if the points of the Line/Curve or the
        curve itself allready exist in the Script point- and curve list. If not
        it adds the point and line code to the script. The function returns
        None if no identical curve was found and the given curve has been
        added. The functions returns the Line if an identical Line allready
        exists.

        Args:
            curve: Line

        Returns:
            Line or None: Identical line, if one was found, so it can be
                replaced in the surfaces curveloop. If no duplicate was found
                the function returns None.
        """
        # Punkte prüfen und erzeugen
        startPoint = curve.startPoint
        endPoint = curve.endPoint
        # Try to add the points
        addP1 = self._addPoint(startPoint)
        addP2 = self._addPoint(endPoint)

        # If one or both points are allready existing: set them in curve
        if addP1:
            curve.startPoint = addP1
        if addP2:
            curve.endPoint = addP2
        if curve.type == "CircleArc":
            centerPoint = curve.center
            addC = self._addPoint(centerPoint)
            if addC is not None:
                curve.center = addC
        elif curve.type == "Spline":
            controlPointList = curve.controlPoints.copy()
            for controlPoint in controlPointList:
                newP = self._addPoint(controlPoint)
                if newP is not None:
                    curve.removeControlPoint(controlPoint)
                    curve.addControlPoint(
                        newP, controlPointList.index(controlPoint)
                    )

        identicalCurve = self.testCurve(curve)
        if identicalCurve is None:
            # add the curve to the global curve list
            self.curveList.append(curve)
        # Wenn identicalCurve = None -> no identical curve found in list
        if not identicalCurve:
            # create the geometrical curve Code
            curveName = cleanName(curve.name)
            curveID = curve.id
            curveType = curve.type
            startPointID = curve.startPoint.id
            endPointID = curve.endPoint.id
            if curveType == "Line":
                code = (
                    f"{curveName} = {curveID};"
                    f"Line({curveName}) = {{{startPointID}, {endPointID}}}; \n"
                )
            elif curveType == "CircleArc":
                curve: CircleArc = curve
                centerPointID = curve.center.id
                code = (
                    f"{curveName} = {curveID};"
                    f"Circle({curveName}) = {{{startPointID}, {centerPointID}, {endPointID}}}; \n"
                )
                ###
                # # test add Transfinite curve mesh
                # angle = abs(curve.getAngle(flag_deg=True))
                # radius = curve.getRadius()
                # arcLen = 2*pi*radius*(angle/180)
                # nbrMeshPoints = round(arcLen*1e3) # 1mm distance
                # code += f"Transfinite Curve {{{curve.id}}} = {nbrMeshPoints};"
                ###
            elif curveType == "Spline":
                if curve.splineType == 0:
                    splineType = "Spline"
                elif curve.splineType == 1:
                    splineType = "Bezier"
                elif curve.splineType == 2:
                    splineType = "BSpline"

                code = (
                    f"{curveName} = {curveID}; \n"
                    f"{splineType}({curveName}) = {{{startPointID}, "
                )
                controlPoints = curve.controlPoints
                for controlPoint in controlPoints:
                    code += f"{controlPoint.id}, "
                code += f"{endPointID}}};\n"

            self.curveCode += code
            curve._todesmerker = True
            return None
        return identicalCurve

    def _addLineCode(self, surface: Surface) -> None:
        """Add the Code for the lines of a Surface to the Script"""
        lines: List[Line] = surface.curve
        # Alle Kurven erzeugen und Testen
        for line in lines:
            testLine = self._addCurve(line)
            # if a similar line was found replace it
            if testLine is not None:
                surface.replaceCurve(line, testLine)

    def _checkLoop(
        self, surface: Surface
    ) -> Tuple[List[Line], List[Literal[-1, 1]]]:
        """
        Reorder the lines of a close curve loop (surface) to generate a valid
        Gmsh curve loop.

        Args:
            surface (Surface): Surface to get line loop to sort.

        Returns:
            (List[Line], List[Literal[-1, 1]]): New reorder curve loop and
                direction list with 1 if line should appear in defined
                direction (from P1 to P2) or -1 if direction should be inverted
                (from P2 to P1)
        """
        oldLoop: List[Line] = surface.curve.copy()
        direction: List[int] = []
        direction.append(
            1
        )  # append 1 for first line, cause it sets the direction
        newLoop: List[Line] = []
        # add first line to newLoop, because it doesnt need to be checked
        newLoop.append(oldLoop.pop(0))
        nbrLines = len(oldLoop)  # get the remaining number of lines
        # for every line thats left:
        for outerCounter in range(nbrLines):
            # Check which line in oldLoop appends to the last line in newLoop
            # if that line was found get direction, append it to newLoop and
            # remove it from oldLoop
            for curveIndex, curve in enumerate(oldLoop):
                if direction[-1] == 1:
                    if curve.startPoint.isEqual(newLoop[-1].endPoint):
                        direction.append(1)
                        newLoop.append(oldLoop.pop(curveIndex))
                        break
                    if curve.endPoint.isEqual(newLoop[-1].endPoint):
                        direction.append(-1)
                        newLoop.append(oldLoop.pop(curveIndex))
                        break
                else:
                    if curve.startPoint.isEqual(newLoop[-1].startPoint):
                        direction.append(1)
                        newLoop.append(oldLoop.pop(curveIndex))
                        break
                    if curve.endPoint.isEqual(newLoop[-1].startPoint):
                        direction.append(-1)
                        newLoop.append(oldLoop.pop(curveIndex))
                        break
        return newLoop, direction

    def _addLoopCode(self, surface: Surface) -> str:
        """Create the curve loop code for the gmsh input file.

        The IDs of the curve objects (lines) forming a closed loop must be in
        the correct order so the end point of the first line is the start point
        of the second line and so on. See
        :func:`_checkLoop <pyemmo.script.script.Script._checkLoop>` function
        for more information.

        The gmsh-code for a curve loop looks like:

        .. code::

            Curve Loop(Surface_ID) = {Line_ID1, Line_ID2, -Line_ID3, Line_ID4};

        Where :code:`Surface_ID` and :code:`Line_ID` are integers refering to
        a surface and line instance.

        Args:
            surface (Surface): Surface to generate the curve loop code from

        Returns:
            str: Curve loop code in correct gmsh format
        """
        # TODO: add flag to not check the loop if lines are allready in order:
        lineList, directionList = self._checkLoop(surface)
        # Add CurveLoop code
        code = f"Curve Loop({surface.id}) = {{"
        # for every line in the Loop
        for lineIndex, line in enumerate(lineList):
            # add line index with sign for direction
            code += str(directionList[lineIndex] * line.id) + ","
        # print last element without ","
        code = code.rstrip(",")
        code += "};\n"
        return code

    def _addSurface(self, surface: Surface) -> None:
        """Create curve-, curve loop- and surface code for gmsh.

        The resulting code is stored in the internal :code:`Script` variables:

        - curve code -> :code:`Script.curveCode` (see :func:`addCurve
          <pyemmo.script.script.Script._addCurve>`)
        - curve loop code -> :code:`Script.areaCode` (see :func:`_addLoopCode
          <pyemmo.script.script.Script._addLoopCode>`)
        - surface code -> :code:`Script.areaCode`

        Args:
            surface (Surface): Surface to add to Script.
        """
        if surface not in self.areaArray:
            self._addLineCode(surface)
            code: str = "\n"
            toolIDCode: str = (
                ", "  # string for tool surfaces that should be subtracted
            )
            for toolSurf in surface.tools:  # if _cut list is not empty
                toolSurfName = cleanName(toolSurf.name)
                toolSurfID = toolSurf.id
                # if toolSurf not in self._areaArray:
                if not toolSurf.isDrawn():  # if the surface is not in script
                    self._addLineCode(toolSurf)
                    code += self._addLoopCode(toolSurf)
                    # if the tool-surface should be kept; add it as surface
                    # delete only makes sence for cutting surface
                    if not toolSurf.delete:
                        # adding Surface name for better identification
                        code += f"Surf_{toolSurfName} = {{{toolSurfID}}};\n"
                        # add Surface Code
                        code += f"Plane Surface(Surf_{toolSurfName}) = {{{toolSurfID}}};\n"
                        self.areaArray.append(toolSurf)
                    # code = code + "};\n"
                # add the surface ID to the lineloop-cut-id-list
                toolIDCode += str(toolSurfID) + ", "

            # Add CurveLoop code for parent surface
            code += self._addLoopCode(surface)
            surfName = cleanName(surface.name)
            surfID = surface.id
            ## Add surface code:
            # Generate name for ID; adding Surface name for better
            # identification
            code += f"Surf_{surfName} = {{{surfID}}};\n"
            # add Surface Code:
            # Plane Surface(Surf_SURFNAME) = {LOOPID, CUT_ID1, CUT_ID2,...};\n
            code += (
                f"Plane Surface(Surf_{surfName}) = {{{surfID}"
                + toolIDCode[
                    :-2
                ]  # ignore last two characters because they are ", "
                + "};\n"
            )

            self.areaCode += code
            self.areaArray.append(surface)

            cCode = ""
            if surface.getMeshColor():
                cCode = f"Color {surface.getMeshColor()} {{Surface {{{surfID}}}; }}\n"
            for toolSurf in surface.tools:
                if toolSurf.getMeshColor():
                    cCode += (
                        f"Color {toolSurf.getMeshColor()} "
                        f"{{Surface {{{toolSurf.id}}}; }}\n"
                    )
            self.colorCode += cCode

    def _resetGeometry(self) -> None:
        """Reset all geometry attributes of the script (point, line and surface
        lists; code strings; physical elements)"""
        # reset all lists and code strings
        # points
        self.pointCode: str = ""
        for point in self.pointArray:
            point._todesmerker = False
        self.pointArray: List[Point] = []

        # lines
        self.curveCode: str = ""
        for curve in self.curveList:
            curve._todesmerker = False
        self._setCurveList([])

        # surfaces
        self.areaCode: str = ""
        for area in self.areaArray:
            area._todesmerker = False
        self.areaArray: List[Surface] = []

        # physical surfaces
        self.physicalElementCode: str = ""
        self.physicalElementArray: List[PhysicalElement] = []

        # reset colors
        self.colorCode: str = "\n"  # code for mesh colors

    # -------------------------------------------------------------------------
    # -------------------------- END OF GEO FUNCTIONS -------------------------
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # -------------------------- START OF PRO FUNCTIONS -----------------------
    # -------------------------------------------------------------------------

    def _addMachineDomains(self):
        domainList = self._createMachineDomains(self.machine)
        for domain in domainList:
            self._addDomain(domain)
        return domainList

    def _createMachineDomains(self, machine: MachineAllType) -> List[Domain]:
        """
        Create Domain objects from the output (Dict[domainName,
        List[PhysicalElements]]) of rotor and stator sortPhysicals() by linking
        them with the domain names for the magstatdyn file specified in
        rotorDomainDict and statorDomainDict (Dict[statorDomainName,
        magStatDynName])

        Args:
            machine (MachineAllType): machine to get the physicals from
                (machine of script)

        Returns:
            List[Domain]: Domain list containing domains suitable for the
                magstatdyn.pro file. The order of that list is important since
                it dicides which points and lines are created first and which
                are sorted out!
        """
        domainList: List[Domain] = list()
        stator = machine.stator
        statorPhysicalsDict = stator.sortPhysicals()
        rotor = machine.rotor
        rotorPhysicalsDict = rotor.sortPhysicals()
        # create (boundary) domains existing in rotor AND stator (primary,
        # secondary lines) These domains MUST be created first, because meshing
        # constraints need to be applied on them and this is only possible if
        # the line IDs of these lines are not sorted out due to identical
        # lines.The domains will be created in the order they appeer in this
        # domain list!
        for statorDomain in statorPhysicalsDict.keys():
            if statorDomain in boundaryDomainDict:
                bndDomain = Domain(
                    boundaryDomainDict[statorDomain],
                    statorPhysicalsDict[statorDomain],
                )
                if statorDomain in rotorPhysicalsDict.keys():
                    # boundary also exists in rotor
                    bndDomain.addPhysicalElements(
                        rotorPhysicalsDict[statorDomain]
                    )
                domainList.append(bndDomain)

        # create rotor domains
        # move domainC to domainCC
        rotorPhysicalsDict["domainCC"].extend(rotorPhysicalsDict["domainC"])
        rotorPhysicalsDict["domainC"].clear()
        # create Domains
        domainList.extend(
            self._createDomains(rotorPhysicalsDict, rotorDomainDict)
        )
        # add additional domains for every movinband part, to specify the
        # Link-boundary in magstatdyn
        for domain in domainList:
            if domain.name == "Rotor_Bnd_MB":
                for i, mbPhysical in enumerate(domain.physicals):
                    domainList.insert(
                        3 + i,
                        Domain(
                            name=f"Rotor_Bnd_MB_{i+1}",
                            physicalElements=[mbPhysical],
                        ),
                    )
                break

        # create stator domains
        # move domainC to domainCC
        # TODO: Decide which domains should be calculatd with eddy currents
        statorPhysicalsDict["domainCC"].extend(statorPhysicalsDict["domainC"])
        statorPhysicalsDict["domainC"].clear()

        # add stator domains to domain list
        domainList.extend(
            self._createDomains(statorPhysicalsDict, statorDomainDict)
        )

        # create additional slot domains for excitations
        domainList.extend(
            self._createWindingDomains(statorPhysicalsDict).values()
        )

        # append domains to identify linear and non-linear surfaces
        nonLinearDomainID = "domainNL"
        nonLinearDomain = Domain(
            "DomainNL",
            rotorPhysicalsDict[nonLinearDomainID]
            + statorPhysicalsDict[nonLinearDomainID],
        )
        domainList.append(nonLinearDomain)

        linearDomainID = "domainL"
        linearDomain = Domain(
            "DomainL",
            rotorPhysicalsDict[linearDomainID]
            + statorPhysicalsDict[linearDomainID],
        )
        domainList.append(linearDomain)

        # append dummy domain for movingband
        try:
            airgapMaterial = statorPhysicalsDict["airGap"][0].material
        except Exception as firstExcept:
            try:
                airgapMaterial = rotorPhysicalsDict["airGap"][0].material
            except Exception as secondExcept:
                raise secondExcept from firstExcept

        domainList.append(
            Domain(
                name="MovingBand_PhysicalNb",
                physicalElements=PhysicalElement(
                    name="",
                    geometricalElement=[],
                    material=airgapMaterial,
                    phyID=0,
                ),
            )
        )

        # append domain for lamination
        laminationDomainID = "domainLam"
        laminationDomain = Domain(
            "Domain_Lam",
            rotorPhysicalsDict[laminationDomainID]
            + statorPhysicalsDict[laminationDomainID],
        )
        domainList.append(laminationDomain)

        return domainList

    def _createDomains(
        self,
        physicalsDict: Dict[str, List[PhysicalElement]],
        domainDict: Dict[str, str],
    ) -> List[Domain]:
        """
        Create a list of domains

        Args:
            physicalsDict (dict): Dict with domain name as key string and a
                list of physical elements containing to that domain
                ["Domain Name", List[PhysicalElements]].
            domainDict (dict): Dict with domain name as key string and
                pro-script domain name as value.

                .. code:: python

                    {"Domain Name", "Pro-Script Name"}

        Returns:
            List[Domain]: List of domains with correct pro script names and
                physicals.

                .. code:: python

                    [Domain(name="Pro-Script Name", List[PhysicalElements])]
        """
        domainList: List[Domain] = list()
        for domainName in physicalsDict.keys():
            if domainName in domainDict.keys():
                if physicalsDict[domainName]:  # if there are physicalElements
                    domainList.append(
                        Domain(
                            domainDict[domainName], physicalsDict[domainName]
                        )
                    )
                else:
                    # FIXME: ADD MACHINE SIDE TO DOMAIN NAME
                    logging.debug(
                        "There were no physical elements in domain '%s'.",
                        domainName,
                    )
        return domainList

    def _createWindingDomains(
        self, domainDict: Dict[str, List[PhysicalElement]]
    ) -> Dict[str, Domain]:
        """
        This function creates the winding domains for a 3-phase stator:
        Domain names are: Stator_Ind{A,B,C}{p,n}
        """
        # create dict of slots
        slotDomainDict: Dict[str, Domain] = {}
        # FIXME: use try-except statment instead of for loop!
        for domain, physicalsList in domainDict.items():
            # for i, (domain, physicalsList) in enumerate(domainDict.items()):
            if domain == "domainS":
                # TODO: This implies that all slots are in domainS
                for slot in physicalsList:
                    if slot.type == "Slot":
                        slot: Slot = slot
                        phaseName = slot.getPhase("ABC")
                        slotDomainName = (
                            "Stator_Ind_"
                            + phaseName
                            + ("p" if slot.windDirection == 1 else "m")
                        )
                        if slotDomainName not in slotDomainDict:
                            # add domain to slot dict
                            slotDomainDict[slotDomainName] = Domain(
                                slotDomainName, slot
                            )
                        else:
                            # add slot to existing domain
                            slotDomainDict[slotDomainName].addPhysicalElements(
                                [slot]
                            )
                    # else:
                    # FIXME: if physical element in domainS is not type Slot:
                    # should there be an Error or Warning?
                return slotDomainDict
        return None

    def addPostOperation(self, quantityName: str, name: str, **kwargs) -> None:
        """Add a new PostOperation (Print) statement

        Args:
            - quantityName (str): Name of the PostProcessing quantity (eg. a,
                az, b, bn, hn, b_tangent, b_radial, br, mu, j, js, jz, Vmag,
                I_n, ir, p_Lam, P_Lam, Inertia,...)
            - name (str, optional): Name of the PostOperation.

            - **kwargs: kwargs are used to complete the Print statment, so eg.
                to print Br on the whole Domain the function call would look
                like:
                    myScript.addPostOperation("b_radial", "User Defined
                    PostOperation", OnElementsOf="Domain",
                    File="Path/To/resFile.pos", LastTimeStepOnly="",)

            A special case is if you want to save something to the
            parameterized folder "ResDir" (Onelab parameter). In this case you
            have to specify the following "File" kwarg:
                '..., File = "CAT_RESDIR/YourResFileName.pos" ...'
            That way the File kwarg is replaced by:
                '.., File = StrCat[ResDir,"YourResFileName.pos"] ...'

            See
            https://getdp.info/doc/texinfo/getdp.html#Types-for-PostOperation
            for more PostOperation options
        """
        userDefinedPO = self.postOperation
        postOperationNames = self.postOperationNames
        # search in the user defined PostOperation if there is a PO with that
        # name. Remember: our self._postOperation object of type
        # (PostOperation) has a list of PostOperations ("items") which can have
        # several "Operations" (eg. Prints, Echos,...) defined

        name = cleanName(name)
        if name in postOperationNames:
            # if that PostOperation allready exists, get the PostOperationItem
            # with that name
            poItem = userDefinedPO.items[postOperationNames.index(name)]
        else:
            # it that PostOperation is not existing, create it
            poItem = userDefinedPO.add(
                Name=name, NameOfPostProcessing="MagStaDyn_a_2D"
            )
        poItem: PostopItem = poItem
        poItem.add().add(quantity=quantityName, **kwargs)
        if "File" in kwargs:
            if "CAT_RESDIR" in kwargs["File"]:
                resfileStr: str = kwargs["File"]
                resfileName = resfileStr.lstrip("CAT_RESDIR").lstrip("\\")
                poItem.item[-1].code = poItem.item[-1].code.replace(
                    f'"{kwargs["File"]}"', f'StrCat[ResDir,"{resfileName}"]'
                )

    # -------------------------------------------------------------------------
    # -------------------------- END OF PRO FUNCTIONS -------------------------
    # -------------------------------------------------------------------------
    def _createPhysicalElementCode(
        self, physicalElement: PhysicalElement
    ) -> str:
        """Create the code for a physical element (= domain for simulation) in
        the .geo file. E.g. for a Physical Surface the code would look like:

        .. code:: text

            Physical Surface("PHYSICAL_NAME", PHSICAL_ID) =
                {GEO_ID1,GEO_ID2,...};

        Args:
            physicalElement (PhysicalElement): Physical element to generate
                code from.

        Returns:
            str: Gmsh style physical element code.
        """
        if physicalElement not in self.physicalElementArray:
            code = f"// {physicalElement.name}\n"
            # raises error if not Surface or Line
            geoElmType = physicalElement.geoElementType
            if geoElmType == Surface:
                elementType = "Surface"
            elif geoElmType == Line:
                elementType = "Curve"
            code += (
                "Physical "
                + elementType
                + f'("{physicalElement.name}", {physicalElement.id}) = {{'
            )
            for geo in physicalElement.geometricalElement:
                if elementType == "Surface":
                    self._addSurface(geo)
                    code += f"{geo.id},"
                else:  # its a line
                    lineOrNone = self._addCurve(geo)
                    if lineOrNone:
                        # result of addCurve was an identical line;
                        # add the id of that line
                        code += f"{lineOrNone.id},"
                    else:
                        # add the id of the new line (= geo)
                        code += f"{geo.id},"
                geo._todesmerker = True
            # replace the last unnecessary "," with "};\n"
            code = code.rstrip(",") + "};\n"
            return code
        return ""

    def _addPhysicalElement(self, physicalElement: PhysicalElement) -> None:
        """Add a PhysicalElement to the Script.

        This calls:

            - :func:`addSurface() <pyemmo.script.script.Script.addSurface>` and
                 :func:`addCurve() <pyemmo.script.script.Script._addCurve>`
            - :func:`addMaterial() <pyemmo.script.script.Script._addMaterial>`
                if Material is not defined yet
            - addMagnetization() (radial, parallel or tangential) if Physical
                is a Magnet

        Args:
            physicalElement (PhysicalElement): Physical Element to add to
                Script.

        """
        if physicalElement.geometricalElement:
            # if the geo list is not empty
            # remember there can be domains without geometrical elements,
            # like the "MovingBand_PhysicalNb" domain
            code = self._createPhysicalElementCode(physicalElement)
            self.physicalElementCode += code

        if physicalElement not in self.physicalElementArray:
            # add physical element to array
            self.physicalElementArray.append(physicalElement)
            # add material if existing
            if physicalElement.material:
                self._addMaterial(physicalElement)
            # add magnetization if specified
            # FIXME: BUG Attribute errors inside addMag... functions are not
            # catched!

            if isinstance(physicalElement, Magnet):
                mag: Magnet = physicalElement
                typeMag = mag.magType
                if typeMag == "radial":
                    self._addMagnetisationRadial(physicalElement)
                elif typeMag == "parallel":
                    self._addMagnetisationParallel(physicalElement)
                elif typeMag == "tangential":
                    self._addMagnetisationTangential(physicalElement)
                else:
                    raise TypeError(
                        f"Wrong Magnetisation Type: '{typeMag}'."
                        + "Magnetisation Type must be 'radial', 'parallel' or "
                        + "'tangential'."
                    )

            # try:
            #     typeMag = physicalElement.magnetisationType
            #     if typeMag == "radial":
            #         self._addMagnetisationRadial(physicalElement)
            #     elif typeMag == "parallel":
            #         self._addMagnetisationParallel(physicalElement)
            #     elif typeMag == "tangential":
            #         self._addMagnetisationTangential(physicalElement)
            #     else:
            #         pass
            # except AttributeError:
            #     pass

    def _addMaterial(self, physicalElement: PhysicalElement) -> None:
        """
        Add the material of a physical element to the material_dict.
        If the material allready exists in the material dict, its physical
        element ID is added to the physical element list of that material.

        Args:
            physicalElement (PhysicalElement): Physical element (PE) which
                material should be added to the script. If the material of the
                PE is allready in the material dict of the script, the PE-ID is
                added to the material dict.

        Returns:
            None
        """
        # if the material is not in the material dict
        matDict = self.materialDict
        material = physicalElement.material
        if material not in matDict["material"]:
            matDict["material"].append(material)
            matDict["physicalElemID"].append([physicalElement.id])
        else:
            # otherwise find the index of the existing material
            matIndex = matDict["material"].index(material)
            # and append the PhysicalElement to the List[PhysicalElement]
            matDict["physicalElemID"][matIndex].append(physicalElement.id)

    def _addMagnetisationRadial(self, magnet: Magnet):
        magDir = magnet.magDir
        matName = cleanName(magnet.material.name)
        self.functionMagnetisation.add(
            name="br",
            expression=f"{magDir}*br_{matName} * XYZ[]/Norm[XYZ[]]",
            region=f"Region[{magnet.id}]",
        )

    def _addMagnetisationParallel(self, physicalElement: Magnet):
        matName = cleanName(physicalElement.material.name)
        magAngle = physicalElement.magAngle
        magDir = physicalElement.magDir
        magFunction = (
            f"{magDir}*br_{matName} * Vector["
            f"Cos[{magAngle} + RotorPosition[]], "
            f"Sin[{magAngle} + RotorPosition[]], 0]"
        )
        self.functionMagnetisation.add(
            "br",
            magFunction,
            f"Region[{physicalElement.id}]",
        )

    def _addMagnetisationTangential(self, magnet: Magnet):
        magAngle = magnet.magAngle
        magDir = magnet.magDir
        matName = cleanName(magnet.material.name)
        magFunction = (
            f"{magDir}*br_{matName} * Vector["
            f"-Sin[{magAngle} + RotorPosition[]], "
            f"Cos[{magAngle} + RotorPosition[]], 0] "
        )
        self.functionMagnetisation.add(
            "br",
            magFunction,
            f"Region[{magnet.id}]",
        )

    def _addDomain(self, domain: Domain):
        """_addDomain adds a group with the domain name to the script-class
        getdp-group "_group" """
        physicalElements: List[PhysicalElement] = domain.physicals
        physIDs: List[int] = []
        for physicalElement in physicalElements:
            self._addPhysicalElement(physicalElement)
            physIDs.append(physicalElement.id)
            # allPhysicalName.append(pE.getName())
        self.group.add(cleanName(domain.name), physIDs)

    def _printAllMaterial(self):
        """Generate the GetDP function code for all materials in the material
        dict"""
        self.functionMaterial.define(name=["br", "js"])
        self.functionMaterial.add_params({"mu0": "4.e-7 * Pi"})

        matDict = self.materialDict
        for i, mat in enumerate(matDict["material"]):
            mat: Material = mat
            # mat: Material = self._materialDict["material"][i]
            # convert list[int] to list[str]
            physElemIDstr: List[str] = []
            for physicalElementID in self.materialDict["physicalElemID"][i]:
                physElemIDstr.append(str(physicalElementID))
            # add group for material
            matName = cleanName(mat.name)
            self.group.add(id="group_" + matName, glist=physElemIDstr)
            matFun = self.functionMaterial

            matFun.add_comment(f"New Material: {matName}\n", True)
            # add electrical conductivity
            conductivity = mat.conductivity
            matFun.add_params(
                {f"sigma_{matName}": (conductivity if conductivity else 0)}
            )
            matFun.add("sigma", "sigma_" + matName, "group_" + matName)

            # Wenn linear True, nonlinear False
            if mat.isLinear():
                # add mue_r
                mueR = mat.relPermeability
                matFun.add_params({"muR_" + matName: (mueR if mueR else 0)})
                # add nu
                matFun.add_params(
                    {"nu_" + matName: f"1/(muR_{matName} * mu0)"}
                )
                matFun.add("nu", "nu_" + matName, "group_" + matName)
            else:
                # if non linear
                bhArray = mat.BH
                bString = "{"
                hString = "{"
                for bhValue in bhArray:
                    bString += str(bhValue[0]) + ","
                    hString += str(bhValue[1]) + ","
                bString = bString[0 : len(bString) - 1] + "}"
                hString = hString[0 : len(hString) - 1] + "}"
                matFun.add_params({f"Mat_h_{matName}": hString})
                matFun.add_params({f"Mat_b_{matName}": bString})
                matFun.add_params(
                    {f"Mat_b2_{matName}": f"Mat_b_{matName}()^2"}
                )
                matFun.add_params(
                    {
                        f"Mat_nu_{matName}": f"Mat_h_{matName}()/Mat_b_{matName}()"
                    }
                )
                matFun.add_params(
                    {f"Mat_nu_{matName}(0)": f"Mat_nu_{matName}(1)"}
                )
                matFun.add_params(
                    {
                        f"Mat_nu_b2_{matName}": f"ListAlt[Mat_b2_{matName}(),"
                        + f" Mat_nu_{matName}()]"
                    }
                )
                matFun.add(
                    f"nu_{matName}",
                    matFun.InterpolationLinear(
                        matFun.SquNorm("$1"), f"Mat_nu_b2_{matName}()"
                    ),
                )
                matFun.add(
                    f"dnudb2_{matName}",
                    matFun.dInterpolationLinear(
                        matFun.SquNorm("$1"), f"Mat_nu_b2_{matName}()"
                    ),
                )
                matFun.add(f"h_{matName}", f"nu_{matName}[$1] * $1")
                matFun.add(
                    f"dhdb_{matName}",
                    matFun.TensorDiag(1, 1, 1)
                    + f" * nu_{matName}[$1#1] + 2 * dnudb2_{matName}[#1] * "
                    + matFun.SquDyadicProduct("#1"),
                )
                matFun.add(
                    f"dhdb_NL_{matName}",
                    f"2 * dnudb2_{matName}[$1#1] * "
                    + matFun.SquDyadicProduct("#1"),
                )
                matFun.add("nu", f"nu_{matName}[$1]", f"group_{matName}")
                matFun.add(
                    "dhdb_NL",
                    f"dhdb_NL_{matName}[$1]",
                    f"group_{matName}",
                )
            # add remanence
            if mat.remanence:
                if mat.tempCoefRem:
                    # br = br_20 * (1 + tempCoef * (tempMag-20))
                    br20 = mat.remanence
                    tempCoef = mat.tempCoefRem
                    matFun.add_params(
                        {
                            ("br_" + matName): (
                                f"{br20} * (1 + ({tempCoef} * (tempMag - 20)))",
                                "Reference temperatur is 20°C",
                            )
                        }
                    )
                    matFun.add_raw_code(
                        (
                            f'Printf("Remanence flux density of magnet material {matName} '
                            f'at temperature %.1f °C is %.5f T",tempMag, {"br_" + matName});\n'
                        ),
                        newline=False,
                    )
                else:
                    matFun.add_params({"br_" + matName: mat.remanence})
            # add sheet thickness
            if isinstance(mat, ElectricalSteel):
                matFun.add_params(
                    {
                        f"d_Lam_{matName}": (
                            mat.sheetThickness,
                            f"lamination thickness of {matName}",
                        )
                    }
                )
                matFun.add("d_Lam", f"d_Lam_{matName}", f"group_{matName}")

            if mat.density:
                matFun.add_params(
                    {
                        f"density_{matName}": (
                            mat.density,
                            f"density of {matName}",
                        )
                    }
                )
                matFun.add("density", f"density_{matName}", f"group_{matName}")

    def _createPointCode(self) -> None:
        """creates all the point code (as text) and stores it in the privat
        variable _pointCode.

        Here a function had to be outsourced instead of printing the points
        directly on generation, because otherwise the smallest mesh size of a
        point could not be recognized
        """
        for point in self.pointArray:
            pName = cleanName(point.name)
            pID = point.id
            coord = point.coordinate
            pMeshSize = point.meshLength
            pCode = (
                f"{pName} = {pID}; "
                f"Point({pID}) = {{{coord[0]}, {coord[1]}, {coord[2]}, {pMeshSize}*gmsf}};\n"
            )
            self.pointCode += pCode

    def _createMovingGeoCode(self) -> str:
        """Create the code for plotting the moving geometry in the gmsh GUI.
        This code should be added at the end of the geo file to extract the
        boundary lines and plot them in the post processing.
        The code will look like:

        .. code:: c

            rotorBndLines[] = Boundary{ Physical Surface{ 14,15,16,17,18,19,20 }; };
            rotorBndLines[] += CombinedBoundary{ Physical Surface{ 13 }; };
            rotorBndLines[] += CombinedBoundary{ Physical Surface{ 23 }; };
            statorBndLines[] = Boundary{ Physical Surface{ 3,5,6,11,26,2... }; };
            Physical Line(1) = {rotorBndLines[], statorBndLines[]};


        Returns:
            str: Code for the moving geometry.


        """
        # rotorPhysicalsList = self.getMachine().getRotor().getPhysicalElements()
        # # rotorIdList: List[int] = list()
        # rotorIdStr = ""
        # for rotorPhys in rotorPhysicalsList:
        #     if rotorPhys.getGeoElementType() == Surface:
        #         rotorIdStr += str(rotorPhys.id) + ","
        # rotorIdStr = rotorIdStr[0:-1]  # erase last comma

        # 1. Non-contacting surfaces (at segment boundary)
        rotorPhysDict = self.machine.rotor.sortPhysicals()
        rotorIdStr = ""
        geoCode = "// Create boundary lines for moving rotor contour plot\n"
        for domainName in ["domainS", "domainM"]:  # only surface domains
            for rotorPhys in rotorPhysDict[domainName]:
                if rotorPhys.geoElementType == Surface:
                    rotorIdStr += str(rotorPhys.id) + ","
        if rotorIdStr:
            rotorIdStr = rotorIdStr[0:-1]
            geoCode += f"rotorBndLines[] = Boundary{{ Physical Surface{{ {rotorIdStr} }}; }};\n"
        # 2. surfaces with contact between segments
        for domainName in ["domainLam", "airGap"]:  # only surface domains
            rotorIdStr = ""
            for rotorPhys in rotorPhysDict[domainName]:
                if rotorPhys.geoElementType == Surface:
                    rotorIdStr += str(rotorPhys.id) + ","
            if rotorIdStr:
                rotorIdStr = rotorIdStr[0:-1]
                geoCode += (
                    f"rotorBndLines[] += CombinedBoundary{{ "
                    f"Physical Surface{{ {rotorIdStr} }}; }};\n"
                )

        statorPhysList = self.machine.stator.physicalElements
        statorIdStr = ""
        for statorPhys in statorPhysList:
            statorIdStr += str(statorPhys.id) + ","
        statorIdStr = statorIdStr[0:-1]

        linesToPlot = PhysicalElement("BoundaryLines", [], material=None)
        plotID = linesToPlot.id
        self.group.add("DomainPlotMovingGeo", [plotID])
        geoCode += (
            f"statorBndLines[] = Boundary{{ Physical Surface{{ {statorIdStr} }}; }};\n"
            + f"""Physical Line("DomainPlotMovingGeo",{plotID}) = {{rotorBndLines[], statorBndLines[]}}; \n"""
            # f"Hide {{ Line{{ Line '*' }}; }} \n"
            # + f"Hide {{ Point{{ Point '*' }}; }} \n"
            # + f"Show{{ Line {{rotorBndLines[], statorBndLines[]}}; }} \n"
        )
        return geoCode

    def _createMeshCompoundCode(
        self, physList: List[PhysicalElement], regionName: str = ""
    ) -> str:
        """Generate the code for a compound mesh of several surfaces.
        The code looks like:

            .. code::

                Compound Surface{27,28,29,30,31}; // Stator airgap

        for the stator airgap surfaces (IDs 27 to 31)

        Args:
            physList (List[PhysicalElement]): list of physical elements to
                combine. The IDs are extracted.
            regionName (str): region name for the comment

        Returns:
            str: Compound mesh code.
        """
        if physList:
            meshCompCode = str()
            for physical in physList:
                if physical.material == physList[0].material:
                    if physical.geoElementType is Surface:
                        if len(physical.geometricalElement) > 1:
                            for geoElem in physical.geometricalElement:
                                meshCompCode += str(geoElem.id) + ","
                        else:
                            logging.warning(
                                'Creation of "Compound Mesh" for domain "%s" failed, because "%s" has only one surface.',
                                regionName,
                                physical.name,
                            )
                            return ""
                    else:
                        logging.warning(
                            'Creation of "Compound Mesh" for domain "%s" failed, because "%s" is not a surface.',
                            regionName,
                            physical.name,
                        )
                        return ""
                else:
                    # domain/region has different materials -> no compound surface
                    # or is not geo type surface
                    logging.warning(
                        (
                            "Creation of 'Compound Mesh' for domain '%s' failed, ",
                            regionName,
                        )
                        + ("because materials of '%s' and ", physList[0].name)
                        + ("'%s' don't match.", physical.name)
                    )
                    return ""

            # make sure there is code
            if meshCompCode:
                meshCompCode = (
                    "Compound Surface{" + meshCompCode[0:-1]
                )  # erase last comma
                meshCompCode += (
                    f"}}; // {regionName}\n"  # add closing and comment
                )
                return meshCompCode
            else:
                return ""
        else:
            # if there are no pEs in that region -> no compound surface
            return ""

    def _createMeshModCode(self) -> str:
        """Create the code to individually modify the mesh size of the machine
        domains.

        This adds a bunch of code lines to the .geo file to modify the mesh.
        The main modification are:

        1. Compound Mesh: If "Compound Mesh" is set to 1, gmsh tries to mesh
            the airgap and lamination surfaces of rotor and stator as combined
            surfaces.
        2. Periodic Mesh constraint for primary and secondary lines.
        3. Mesh size setting for movingband lines via number of movingband
            segments factor.

        Returns:
            str: Gmsh code to modify the mesh properties.

        The final code in the geo file will look something like:

        .. code:: c

            // Mesh operations
            Mesh.AlgorithmSwitchOnFailure = 0; // Do not switch mesh algorithm on failure, because this led to mesh errors in the past
            DefineConstant[
                Flag_CompoundMesh = {
                    0, Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1},
                    Help "Use Compound Mesh to ignore lines between segments while meshing.",
                    Visible Flag_ExpertMode}
            ];

            If (Flag_CompoundMesh)
                Compound Surface{280,281,282,283,284,285,286,287,288}; // stator airGap
            EndIf // (Flag_CompoundMesh)

            // Add Periodic Mesh to model symmetry boundary-lines
            primaryLines = {2771,2772,2773,2774,2775,2776,2777,2778,2779,2780};
            secondaryLines = {2785,2786,2787,2788,2789,2790,2781,2782,2783,2784};
            Periodic Curve{secondaryLines[]} = {primaryLines[]} Rotate {{0,0,1}, {0,0,0}, 2*Pi/4};

            // Add mesh size setting for Movingband lines
            DefineConstant[
                NbrMbSegments = {
                    390.0,
                    Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],
                    Max 1440, Min 180, Step 10,
                    Help "Set the number of mesh segments on the interface between rotor/statorairgap
                    and movingband. Value represents number of segments on whole circle.",
                    Visible Flag_ExpertMode},
                r_MB_R = 0.03228066299098263
            ];

            MB_LinesR = {2673,2675,2824,2826,2828,2830,2832,2834};
            MeshSize{ PointsOf{Line{MB_LinesR[]};}} = 2*Pi*r_MB_R/NbrMbSegments;

            MB_LinesS = {2765,2767,2792,2794,2796,2798,2800,2802,2804,2806,2808,2810};
            MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*0.03268/NbrMbSegments;

            Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)

        """
        rotor = self.machine.rotor
        rotorDict = rotor.sortPhysicals()

        stator = self.machine.stator
        statorDict = stator.sortPhysicals()

        meshModCode = "\n// Mesh operations\n\n"
        # 1. add compound mesh for domain
        meshModCode += (
            "// Do not switch mesh algorithm on failure, "
            + "because this led to mesh errors in the past.\n"
            + "Mesh.AlgorithmSwitchOnFailure = 0;"
        )
        meshModCode += (
            "DefineConstant[Flag_CompoundMesh = {0, "
            + """Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, """
            + """Help "Use Compound Mesh to ignore lines between segments while meshing.","""
            + """Visible Flag_ExpertMode}];\n"""
        )
        meshModCode += """If (Flag_CompoundMesh)\n"""
        for region in ["domainLam", "airGap"]:
            # for region in ["domainLam"]:
            physicalsList = rotorDict[region]
            if physicalsList:
                meshModCode += self._createMeshCompoundCode(
                    physicalsList, ("rotor " + region)
                )
            physicalsList = statorDict[region]
            if physicalsList:
                meshModCode += self._createMeshCompoundCode(
                    physicalsList, ("stator " + region)
                )
        meshModCode += """EndIf // (Flag_CompoundMesh)\n\n"""

        # 2. add mesh size setting via factor
        # Allready done in json API. This would need a other grouping instead
        # of GetDP domains

        # 3. add periodic meshing constraint for primary and secondary lines
        symFactor = self.machine.symmetryFactor
        if symFactor > 1:
            primeLines = self.machine.primaryLines
            secondaryLines = self.machine.getSecondaryLines()
            if primeLines and secondaryLines:
                meshModCode += (
                    "// Add Periodic Mesh to model symmetry boundary-lines\n"
                )
                primeLineIDs = str()
                for line in primeLines:
                    primeLineIDs += f"{line.id},"
                # set primary lines without last comma
                meshModCode += f"primaryLines = {{{primeLineIDs[0:-1]}}};\n"
                secondIDs = str()
                for line in secondaryLines:
                    secondIDs += f"{line.id},"
                # set primary lines without last comma
                meshModCode += f"secondaryLines = {{{secondIDs[0:-1]}}};\n"
                # The following assumes, that the prime lines are located on
                # the x-axis. Rotation from prime to secondary occure in math.
                # positive direction!
                meshModCode += (
                    r"Periodic Curve{secondaryLines[]} = {primaryLines[]} "
                    r"Rotate {{0,0,1}, {0,0,0}, "
                    f"2*Pi/{symFactor}}};\n\n"
                )

        # 4. add mesh size setting for movingband lines
        movingbandPhysicals = (
            rotor.movingBand
        )  # get list of movingband physicals
        if movingbandPhysicals:
            # create line id string for mesh size setting
            mbLineIDs = str()
            for physicalMovingband in movingbandPhysicals:
                if (
                    physicalMovingband.type == "MovingBand"
                    and physicalMovingband.geoElementType == Line
                ):
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in physicalMovingband.geometricalElement:
                        # mbLine.setMeshLength()
                        # BUG, FIXME: Only add movingband line if the
                        # arc has realy been added to the script!
                        mbLineIDs += f"{mbLine.id},"  # add the line id
            # get approx. the min mesh length of the rotor movingband
            # (only checking first line of first movingband physical)
            mbMeshSize = (
                movingbandPhysicals[0].geometricalElement[0].getMinMeshLength()
            )
            if mbLineIDs:
                rRotorMB = rotor.movingBandRadius
                nbrSeg0 = (2 * pi * rRotorMB / mbMeshSize) - (
                    2 * pi * rRotorMB / mbMeshSize
                ) % 10  # calc number of movingband segments by steps of 10
                # create parameter code for movingband segment setting
                meshModCode += (
                    "// Add mesh size setting for Movingband lines\n"
                )
                meshModCode += (
                    "DefineConstant[\n"
                    + (
                        f"\tNbrMbSegments = {{{nbrSeg0}, "
                        """Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],"""
                        "Max 1440, Min 180, Step 10, Help "
                        '"Set the number of mesh segments on the interface between rotor/stator'
                        "airgap and movingband. Value represents number of segments on whole "
                        'circle.", Visible Flag_ExpertMode},\n'
                    )
                    + f"\tr_MB_R = {rRotorMB}"  # rotor movingband radius as parameter
                    # + ",\n"
                    # + """\trotorMBMesh = {360, Name StrCat[INPUT_MESH, "Number of Roto
                    # Movingband Segments"], Min 180, Step 10, Help "Set the number of mesh
                    # segments on the interface between rotor airgap and movingband.",
                    # Visible Flag_ExpertMode}""" +
                    "\n];\n"
                )
                # create movingband line id list, because its cleaner
                meshModCode += f"MB_LinesR = {{{mbLineIDs[0:-1]}}};\n"
                # set the mesh size for all movingband points
                meshModCode += (
                    "MeshSize{ PointsOf{Line{MB_LinesR[]};}} = "
                    "2*Pi*r_MB_R/NbrMbSegments;\n\n"
                )
            # same thing for stator movingband with number of segments of
            # rotor movingband
            mbLineIDs = str()  # reset string
            for physicalMovingband in stator.movingBand:
                if (
                    physicalMovingband.type == "MovingBand"
                    and physicalMovingband.geoElementType == Line
                ):
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in physicalMovingband.geometricalElement:
                        # mbLine.setMeshLength()
                        mbLineIDs += f"{mbLine.id},"  # add the line id
            if mbLineIDs:
                rStatorMB = stator.movingBandRadius
                # create movingband line id list, because its cleaner
                meshModCode += f"MB_LinesS = {{{mbLineIDs[0:-1]}}};\n"
                meshModCode += (
                    "MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*"
                    + str(rStatorMB)
                    + "/NbrMbSegments;\n\n"
                )  # set the mesh size for all movingband points
            meshModCode += "Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)\n\n"
        return meshModCode

    def writeGeo(self, UD_MeshCode: str = "") -> None:
        """writeGeo generates the .geo-File for the current script.

        Args:
            UD_MeshCode (str): User defined code to modify mesh settings. This
            will be printed *before* the internal mesh settings because
            otherwise Movingsband-Mesh could be overwritten. Must be conformal
            with the gmsh syntax!
        """
        geoFilePath = os.path.join(self.scriptPath, self.name + ".geo")
        # add all the geo Code
        self._createPointCode()
        # add the code for the mesh settings and mesh modification
        meshSettingsCode = 'INPUT_MESH = "Input/03Mesh/";\n'
        meshSettingsCode += (
            "DefineConstant[\n"
            + "\tgmsf = {1, "
            + 'Name StrCat[INPUT_MESH, "00Mesh size factor"], '
            # + "Visible Flag_ExpertMode, "
            + (
                'Help "Global mesh size factor to modify the mesh size of all points. '
                'Is multiplied with the given mesh size."'
            )
            + "},\n"
        )
        meshSettingsCode += (
            "\nFlag_individualColoring = {0,"
            + 'Name StrCat[INPUT_MESH, "09Individual Mesh Coloring"], '
            + "Choices {0, 1}}\n];\n"
        )
        # show mesh Lines without lighting
        meshSettingsCode += (
            "Mesh.SurfaceEdges = 1;\nMesh.Light = 0;\nMesh.SurfaceFaces = 1;\n"
        )
        meshSettingsCode += (
            "Mesh.Algorithm = 6; // Frontal-Delaunay for 2D meshes\n\n"
        )
        meshModCode = ""
        movingGeoCode = ""
        if self.machine:
            # add the code for mesh modifications
            meshModCode = self._createMeshModCode()
            # add the code for plotting the moving boundary in post processing
            movingGeoCode = self._createMovingGeoCode()

        with open(geoFilePath, "w", encoding="utf-8") as geoScript:
            geoScript.write(versionStr) # write the pyemmo version number 
            # set the geometry kernel
            if self.factory == "OpenCASCADE":
                geoScript.write('SetFactory("OpenCASCADE");\n')
            # create Expert Mode Flag 
            geoScript.write(
                """DefineConstant[\n Flag_ExpertMode = {1,"""
                + """Name '01View/Expert Mode', Choices {0, 1}}\n];\n\n"""
            )
            geoScript.write(meshSettingsCode) # write code for mesh variables
            geoScript.write(self.pointCode)
            geoScript.write(self.curveCode)
            geoScript.write(self.areaCode)
            geoScript.write(
                "\n// Color code\n"
                + """If (!Flag_individualColoring)\n"""
                + self.colorCode
                + """EndIf\n"""
            )
            # geoScript.write(self._colorCode)
            geoScript.write(self.physicalElementCode)
            geoScript.write(UD_MeshCode)
            geoScript.write(meshModCode)
            geoScript.write(movingGeoCode)

        logging.debug(
            "I found %d identical points. There are %d points in the model.",
            self.nbrIdedentPoints,
            len(self.pointArray),
        )
        logging.debug(
            "I found %d identical lines. There are %d lines in the model.",
            self.nbrIdedentLines,
            len(self.curveList),
        )

    def _setParameters(self):
        """Set the machine parameters for the script to the
        ``Script.simParams`` attribute.
        """
        machine = self.machine
        if not machine:
            raise RuntimeError(
                "There was no machine specified. Add machine to script."
            )
        simuParamDict = self.simParams
        # 1. Set geometrical parameters via "machine.getSimParams()"
        #   SYMMETRY_FACTOR, L_AX_R, L_AX_S, NBR_POLE_PAIRS, NBR_TURNS_IN_FACE
        geometryParams = machine.getSimParams()
        # TODO: Improve check here...
        # assert len(geometryParams) == len(simuParamDict.GEO) # assert there
        # is the correct number of parameters

        # update machine parameters:
        simuParamDict["GEO"] = simuParamDict["GEO"] | geometryParams

        # 2. Set simulation parameters
        #   INIT_ROTOR_POS  -> Allready set in __init__
        #   ANGLE_INCREMENT -> Allready set in __init__
        #   FINAL_ROTOR_POS -> Allready set in __init__
        #   SPEED_RPM       -> Allready set in __init__
        #   ParkAngOffset   -> Allready set in __init__
        #   FLAG_NL
        #   FLAG_CHANGE_ROT_DIR
        flagCalcNL = 0
        hasMagnets = False
        # flag_readonly = 0
        for domain in machine.domains:
            for physicalElement in domain.physicals:
                if physicalElement.geoElementType == Surface:
                    mat = physicalElement.material
                    if not mat.isLinear():
                        flagCalcNL = 1
                        break  # if one BH curve is found, we can stop the loop
                    if isinstance(physicalElement, Magnet):
                        hasMagnets = True
        simuParamDict["SYM"]["FLAG_NL"] = flagCalcNL
        if not hasMagnets:
            # if there where no magnet physical elements, set flag to false
            # even if its set to true...
            logging.warning("Unsetting the flag 'CALC_MAGNET_LOSSES', because"
                            " no magnets where found in the machine.")
            simuParamDict["SYM"]["CALC_MAGNET_LOSSES"] = 0

        # machine.getStator().winding.plot_star('plot_star.png',None,False,True)
        if machine.stator.winding.get_windingfactor_el()[1][0, 0] < 0:
            # The fundamental windingfactor sign indicates the rotation
            # dirction of the field wave. If its negative, the field rotates
            # mathematically negative (CW) and the rotation dirction should be
            # inverted. The funamental winding factor allways refers to the
            # mechanical order which is equal to the number of pole pairs. (So
            # this is also true for non-fundamental winding configurations)
            simuParamDict["SYM"]["FLAG_CHANGE_ROT_DIR"] = 1
        else:
            # Otherwise the rotation direction is ok.
            simuParamDict["SYM"]["FLAG_CHANGE_ROT_DIR"] = 0

        # if the Park-transformation angle is not set manually, try to
        # calculate it
        if simuParamDict["SYM"]["ParkAngOffset"] is None:
            nbrPolePairs = default_param_dict["GEO"]["NBR_POLE_PAIRS"]
            nbrSlots = default_param_dict["GEO"]["NBR_SLOTS"]
            slotPitch = 2 * pi / nbrSlots
            mmfOrder, _, angle = machine.stator.winding.get_MMF_harmonics()
            ## DEBUGGING:
            if logging.root.level == logging.DEBUG:
                if not os.path.exists(self.resultsPath):
                    os.mkdir(self.resultsPath)
                machine.stator.winding.save_to_file(
                    os.path.join(self.resultsPath, f"winding_{self.name}.wdg")
                )
                machine.stator.winding.plot_MMK(
                    filename=os.path.join(
                        self.resultsPath, f".\{self.name}_MMF.png"
                    ),
                )

            # Stator angle for I_U = 1 p.u., I_V = -1/2, I_W = -1/2 in rad elec
            systemOffset = float(angle[where(mmfOrder == nbrPolePairs)])
            logging.debug(
                "Stator north pole angle (elec): %.1f°", rad2deg(systemOffset)
            )

            # dq-offset (electrical) is:
            #   current system offset (CSO) angle - half slot pitch
            # because CSO is calculated from center of first slot, but geometry
            # starts with center of tooth.
            # + 270° elec (= -90°) for change of park matrix (to classical park
            #  matrix, where d-axis is aligned with the u-axis; before q-axis
            # was aligned with u-axis).
            # FIXME: This assumes, that the positiv d-axis is at the center of
            # the first pole pitch. This only is true if first pole (CCW) is a
            # north pole! And the magnetization is kind of radial. Does't work
            # for tangential or hallbach magnetization...
            magnetisations: List[str] = []
            for mag in machine.rotor._domainM.physicals:
                mag: Magnet = mag
                magnetisations.append(mag.magType == "tangential")
            if any(magnetisations):
                logging.warning(
                    "Tangential magnetization detected! Dq-offset calculation is invalid"
                )
                dqOffset = 0
            else:
                dqOffset = (
                    -rad2deg(slotPitch / 2 * nbrPolePairs)
                    + rad2deg(systemOffset)
                    + 270
                )
            simuParamDict["SYM"]["ParkAngOffset"] = dqOffset

    def _getParamCode(self, paramName: str, paramValue) -> str:
        """Get a line of parameter code:
        "paramCode = f"{paramName} = {paramValue};\n" """
        if isinstance(paramValue, (str)):
            paramCode = (
                f'{paramName} = "{paramValue}";\n'  # add "" for string value
            )
        else:  # isinstance(paramValue,(int, float)):
            paramCode = f"{paramName} = {paramValue};\n"
        return paramCode

    def _createParamCode(self) -> str:
        """Create the string code for the parameter file"""
        self._setParameters()  # set Parameters to write code
        paramDict = self.simParams
        paramCode: str = "// MACHINE SPECIFIC VALUES \n"
        for paramName, paramValue in paramDict["GEO"].items():
            paramCode += self._getParamCode(paramName, paramValue)
        paramCode += "// SIMULATION SPECIFIC VALUES\n"
        for paramName, paramValue in paramDict["SYM"].items():
            paramCode += self._getParamCode(paramName, paramValue)
        paramCode += "// MATERIAL SPECIFIC VALUES\n"
        for paramName, paramValue in paramDict["MAT"].items():
            paramCode += self._getParamCode(paramName, paramValue)
        return paramCode

    def writePro(self):
        """
        generate pro files.
        new schema:

            1. write parameter file
            2. copy template machine file
            3. append code to machine file
                - import parameter file in machine file
                - add groups and material groups
                - function code (material functions)
            4. import magstatdyn file in machine file

        """
        # Write the code
        #   1. write parameter file
        machineTempFile = abspath(
            join(MAIN_DIR, "script", "machine_template.pro")
        )
        # script file name
        paramFileName = self.name + "_param.geo"
        paramFilePath = abspath(join(self.scriptPath, paramFileName))

        # get the geometrical and simulation parameters:
        paramFileCode = self._createParamCode()

        # write file content to new file
        with open(paramFilePath, "w", encoding="utf-8") as file:
            # also add versionStr to identify pyemmo version
            file.write(versionStr)
            file.write(paramFileCode)

        # 2. copy machine file
        with open(machineTempFile, encoding="utf-8") as templateFile:
            machineFileCode = (
                versionStr + templateFile.read()
            )  # open and read machine template file

        # 3. append group code to machine file
        #   3.1 import parameter file
        # replace the place holder "PARAMETER_FILE" with the actual parameter
        # file name
        machineFileCode = machineFileCode.replace(
            "PARAMETER_FILE", '"' + paramFileName + '"', 1
        )
        #   3.2 add groups and material groups
        #       generate material code in _functionMaterial to account for
        #       material groups
        self._printAllMaterial()
        #       replace the place holder "GROUP_CODE" with actual group code
        machineFileCode = machineFileCode.replace(
            "GROUP_CODE", self.group.code, 1
        )

        #  3.3 function code
        machineFileCode = machineFileCode.replace(
            "FUNCTION_CODE",
            self.functionMaterial.code + self.functionMagnetisation.code,
            1,
        )

        # 4. copy the magstatdyn file
        # filename of the motor model template of getdp
        calculationFileName = "machine_magstadyn_a.pro"
        # filepath to the template calculation file for motor models
        calcFileTempPath = join(
            MAIN_DIR, "script", calculationFileName
        ).replace("\\", "/")
        # read the template file
        with open(calcFileTempPath, encoding="utf-8") as templateCalcFile:
            calcCode = versionStr + templateCalcFile.read()

        calcFilePath = join(self.scriptPath, calculationFileName).replace(
            "\\", "/"
        )  # filepath to the destination of the calculation file
        # write the magstadyn file to new destination
        with open(calcFilePath, "w", encoding="utf-8") as calcFile:
            calcFile.write(calcCode)

        #  6.1 add the PostOperation command code before including the
        # magstatdyn-file
        postOperation = self.postOperation
        if postOperation.items:  # if there are Items in PostOperation
            # add the code for the compute command including the postoperations
            # TODO: Add option for "-bin" case (user setting)

            computeCommandCode = """DefineConstant[\n\tC_ = {"-solve Analysis -v 99 -v2 -pos"""  # -bin
            for postOpName in self.postOperationNames:
                computeCommandCode += " " + postOpName
            computeCommandCode += """ ", Name "GetDP/9ComputeCommand", Visible Flag_Debug}\n];\n"""

            machineFileCode += computeCommandCode

        #   5. import magstatdyn file in machine file
        # # replace the placeholder in the machine script
        # machineFileCode = machineFileCode.replace(
        #     "DEFAULT_PRO_FILE", '"' + calculationFileName + '"', 1
        # )
        # had to replace placeholder method here to add the postoperation
        # command before
        machineFileCode += f'Include "{calculationFileName}"\n'

        # 6.2 add the PostOperation code
        if postOperation.items:  # if there are Items in PostOperation
            machineFileCode += self.postOperation.code

        proFilePath = join(self.scriptPath, self.name + ".pro")
        with open(proFilePath, "w", encoding="utf-8") as proScript:
            proScript.write(machineFileCode)

    def generateScript(self, mode: int = 0, UD_MeshCode: str = ""):
        """
        generate .geo- and .pro files

        Args:
            mode (int): Decide which scripts to generate:

                        - 0: .geo- und .pro-files (default)
                        - 1: only .geo-files
                        - 2: only .pro-files

            UD_MeshCode (str): User defined mesh code. Must be conformal with
                the gmsh syntax.
        """
        if mode == 0:
            self.writeGeo(UD_MeshCode=UD_MeshCode)
            self.writePro()

        elif mode == 1:
            self.writeGeo(UD_MeshCode=UD_MeshCode)
        elif mode == 2:
            self.writePro()
