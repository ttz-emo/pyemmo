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
"""pyemmo Script module"""

# make all annotations strings, to avoid import errors in type checking case
from __future__ import annotations

# import warnings
import logging
import os
import re
import shutil
from math import isclose, pi
from os.path import abspath, join
from typing import TYPE_CHECKING

import gmsh
from numpy import mean, rad2deg, where
from pygetdp import Function as FunctionGetDP
from pygetdp import Group as GroupGetDP
from pygetdp import PostOperation
from pygetdp.postoperation import PostopItem

from ..definitions import DEFAULT_GEO_TOL, MAIN_DIR
from ..functions.clean_name import clean_name, is_valid_filename
from . import (
    DOMAIN_AIRGAP,
    DOMAIN_BAR,
    DOMAIN_CONDUCTING,
    DOMAIN_LAMINATION,
    DOMAIN_LINEAR,
    DOMAIN_NON_CONDUCTING,
    DOMAIN_NON_LINEAR,
    boundaryDomainDict,
    default_param_dict,
    rotorDomainDict,
    statorDomainDict,
    versionStr,
)
from .domain import Domain
from .geometry.line import Line
from .geometry.surface import Surface
from .material.electricalSteel import ElectricalSteel
from .physicals.magnet import Magnet
from .physicals.physicalElement import PhysicalElement
from .physicals.slot import Slot

if TYPE_CHECKING:
    from .geometry.circleArc import CircleArc
    from .geometry.point import Point
    from .geometry.spline import Spline
    from .machine import Machine
    from .material.material import Material
    from .rotor import Rotor
    from .stator import Stator


class Script:
    """Eine Instanz der Klasse Script beinhaltet alle Informationen, die zum
    Erzeugen der .geo- und .pro-Skripte benötigt werden."""

    def __init__(
        self,
        name: str,
        scriptPath: str,
        simuParams: dict,
        machine: Machine | None = None,
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

        .. code-block:: python

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
        # Name des Skriptes
        if is_valid_filename(name):
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
            self._simulationParameters[key] = {
                **default_param_dict[key],
                **paramDict,
            }
        ### directory to save the model files
        self.scriptPath = scriptPath
        # directory to save simulation results
        self.resultsPath = (
            abspath(resultsPath).replace("\\", "/")
            if resultsPath
            else abspath(join(scriptPath, "res_" + self.name)).replace("\\", "/")
        )
        # point code (in gmsh syntax)
        self.pointCode: str = "\n// Points\n"
        # all points
        self.pointArray: list[Point] = []
        # line code (gmsh syntax)
        self.curveCode: str = "\n// Lines and Curves\n"
        # all generated lines
        self._curveList: list[Line | CircleArc | Spline] = []
        # all surfaces (gmsh syntax)
        self.areaCode: str = "\n// Surfaces\n"
        # all generated surfaces
        self.areaArray: list[Surface] = []

        self.colorCode: str = ""  # code for mesh colors

        # PhysicalElement code (gmsh syntax)
        self.physicalElementCode: str = "\n// Physical Elements\n"
        # all generatedPhysicals
        self.physicalElementArray: list[PhysicalElement] = []

        # Alle bereits erzeugten Materialien
        self.group = GroupGetDP()
        self._materialDict: dict[str, list[list[int]]] = {
            "material": [],
            "physicalElemID": [],
        }
        self.functionMaterial = FunctionGetDP()
        self.functionMagnetisation = FunctionGetDP()

        self._postOperation: PostOperation = PostOperation()
        # TODO: Add default Post Operation:
        # PostOperation{
        #     {
        #         Name get_local_fields_post_sim; NameOfPostProcessing MagStaDyn_a_2D;
        #         Operation {
        #             Print[ js, OnElementsOf DomainS, File StrCat[ResDir,"js",ExtGmsh]] ;
        #             Print[ b,  OnElementsOf Domain, File StrCat[ResDir,"b",ExtGmsh] ] ;
        #             Print[ bn,  OnElementsOf Domain, File StrCat[ResDir,"bn",ExtGmsh]] ;
        #             Print[ mu, OnElementsOf Domain, File StrCat[ResDir,"mu_r",ExtGmsh]] ;
        #             Print[ az, OnElementsOf Domain, File StrCat[ResDir,"az",ExtGmsh] ] ;
        #             // Echo[ Str["l=PostProcessing.NbViews-1;", "View[l].IntervalsType = 1;", "View[l].NbIso = 30;", "View[l].Light = 0;", "View[l].LineWidth = 2;"], File StrCat[ResDir,"tmp.geo"], LastTimeStepOnly] ;
        #             If (Flag_Cir_RotorCage)
        #             Print[
        #                 j, OnElementsOf Rotor_Bars, File StrCat[ResDir, "j_RotorBars", ExtGmsh]
        #             ];
        #             EndIf
        #     }
        #     }
        # }
        self.factory = factory  # gmsh geometry kernel

        # FOR DEBUGGING:
        self.nbrIdedentPoints: int = 0
        self.idedentPoints: list[Point] = []
        self.nbrIdedentLines: int = 0
        self.idedentLines: list[Line | CircleArc | Spline] = []

        # set flags to check if files have been created trough generateScript()
        self._pro_files_created = False
        self._geo_files_created = False

        # Save current gmsh model name, because if the model files shall be regenerated
        # but the model has changed due to post processing e.g., we need to reset the
        # model or raise an error
        self._gmsh_model: str = gmsh.model.getCurrent()  # get current model

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
    def scriptPath(self) -> str | os.PathLike:
        """Get the path, where the model files (.geo & .pro) should be stored

        Returns:
            str: path where the model files should be stored
        """
        return self._scriptPath

    @scriptPath.setter
    def scriptPath(self, newScriptPath: str | os.PathLike):
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
    def machine(self) -> Machine | None:
        """getter of machine object

        Returns:
            Union[Machine, None]: actual machine object in script or
                None if no machine was given
        """
        return self._machine

    @machine.setter
    def machine(self, newMachine: Machine):
        """Setter of machine attribute.
        You should not use setMachine because then basically everything would
        have to be recreated (Domains, Physicals, Geos,...) Rather generate new
        script...
        TODO: check this function and add test case.

        Args:
            machine (Machine): machine to create in script.
        """
        logger = logging.getLogger(__name__)
        logger.warning("Reset of machine in script '%s'!", self.name)
        # if isinstance(newMachine, Machine):
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
        """path to the folder where the simulation results are stored
        (simulation results folder)"""
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
    def materialDict(self) -> dict[str, list[list[int]]]:
        """Return the material dict of the script

        Returns:
            Dict[str, List]: material dictionary having the structure:
                .. code-block:: python

                    {
                        "material": [ListOfMaterials],
                        "physicalElemID":  [[physicalIDs],[physicalIDs],...]
                    }

                Every material in the material list has a list of physical
                element IDs in the physicalElemID-List(=List of lists)

        """
        return self._materialDict

    @property
    def curveList(self) -> list[Line | CircleArc | Spline]:
        """get the list of curves in the script

        Returns:
            List[Union[Line,CircleArc,Spline]]: list of curves that have been
                added to the script
        """
        return self._curveList

    @curveList.setter
    def curveList(self, new_curve_list: list[Line | CircleArc | Spline]) -> None:
        """set the curve list of the script.

        Args:
            curveList (List[Union[Line,CircleArc,Spline]]): list of line to be
                set in the script

        Raises:
            ValueError: if curve list was not type "list"
            ValueError: if one element of curve list is not a line of child of
                class line
        """
        if isinstance(new_curve_list, list):
            for curve in new_curve_list:
                # check if the element of curveList is neither type "Line" nor
                # child-class of Line
                # (e.g. CircleArc)
                # if type(curve) != Line or Line not in type(curve).__bases__:
                if not isinstance(curve, Line):
                    msg = f"Element {curve} of given curve list is not type Line!"
                    raise ValueError(msg)
            # if all elements new_curve_listist are valid lines -> set new line list
            self._curveList = new_curve_list
            # TODO: normally the point list has to be renewed by now...
            # But the function should not be used anyway by now.
        else:
            raise (
                ValueError(
                    f"Given curve list object was not a list, but type '{type(new_curve_list)}'!"
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
    def postOperationNames(self) -> list[str]:
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
    # -------------------------- START OF PRO FUNCTIONS -----------------------
    # -------------------------------------------------------------------------

    def _addMachineDomains(self):
        logger = logging.getLogger(__name__)
        domainList = self._createMachineDomains()
        for domain in domainList:
            logger.debug("Adding domain %s", domain.name)
            self._addDomain(domain)
        return domainList

    def _createMachineDomains(self) -> list[Domain]:
        """
        Create Domain objects from the output (Dict[domainName,
        List[PhysicalElements]]) of rotor and stator sortPhysicals() by linking
        them with the domain names for the magstatdyn file specified in
        ``rotorDomainDict`` and ``statorDomainDict`` (Dict[statorDomainName,
        magStatDynName])

        Args:
            machine (Machine): machine to get the physicals from
                (machine of script)

        Returns:
            List[Domain]: Domain list containing domains suitable for the
                magstatdyn.pro file. The order of that list is important since
                it dicides which points and lines are created first and which
                are sorted out!
        """
        domainList: list[Domain] = []
        statorPhysicalsDict = self.machine.stator.sortPhysicals()
        rotor = self.machine.rotor
        rotorPhysicalsDict = rotor.sortPhysicals()
        # create (boundary) domains existing in rotor AND stator (primary,
        # secondary lines) These domains MUST be created first, because meshing
        # constraints need to be applied on them and this is only possible if
        # the line IDs of these lines are not sorted out due to identical
        # lines. The domains will be created in the order they appeer in this
        # domain list!
        for statorDomain in statorPhysicalsDict.keys():
            if statorDomain in boundaryDomainDict:
                bndDomain = Domain(
                    boundaryDomainDict[statorDomain],
                    statorPhysicalsDict[statorDomain],
                )
                if statorDomain in rotorPhysicalsDict.keys():
                    # boundary also exists in rotor
                    bndDomain.addPhysicalElements(rotorPhysicalsDict[statorDomain])
                domainList.append(bndDomain)

        # create rotor domains
        # move domainC to domainCC
        rotorPhysicalsDict[DOMAIN_NON_CONDUCTING].extend(
            rotorPhysicalsDict[DOMAIN_CONDUCTING]
        )
        rotorPhysicalsDict[DOMAIN_CONDUCTING].clear()

        # create Domains
        domainList.extend(self._createDomains(rotorPhysicalsDict, rotorDomainDict))
        # Create single Bar regions
        if DOMAIN_BAR in rotorPhysicalsDict:
            rotorPhysicalsDict[DOMAIN_BAR].sort(key=Slot.get_circumferential_position)
            for i, region in enumerate(rotorPhysicalsDict[DOMAIN_BAR]):
                domainList.append(Domain(f"Rotor_Bar_{i+1}", region))
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
        # TODO: Decide which domains should be calculatd with eddy currents.
        #   -> UPDATE: Decition should be made in .pro file depening on params.
        statorPhysicalsDict[DOMAIN_NON_CONDUCTING].extend(
            statorPhysicalsDict[DOMAIN_CONDUCTING]
        )
        statorPhysicalsDict[DOMAIN_CONDUCTING].clear()

        # add stator domains to domain list
        domainList.extend(self._createDomains(statorPhysicalsDict, statorDomainDict))

        # create additional slot domains for excitations
        domainList.extend(self._createWindingDomains(statorPhysicalsDict).values())

        # append domains to identify linear and non-linear surfaces
        nonLinearDomainID = DOMAIN_NON_LINEAR
        nonLinearDomain = Domain(
            "DomainNL",
            rotorPhysicalsDict[nonLinearDomainID]
            + statorPhysicalsDict[nonLinearDomainID],
        )
        domainList.append(nonLinearDomain)

        linearDomainID = DOMAIN_LINEAR
        linearDomain = Domain(
            "DomainL",
            rotorPhysicalsDict[linearDomainID] + statorPhysicalsDict[linearDomainID],
        )
        domainList.append(linearDomain)

        # Create default domain for Movingband
        # This needs to be done here since we need to add it to the airgap
        # material domain. TODO: This could be handled by the pro-file for sure.
        try:
            airgap_mat = statorPhysicalsDict[DOMAIN_AIRGAP][0].material
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception as exce_1:
            try:
                airgap_mat = rotorPhysicalsDict[DOMAIN_AIRGAP][0].material
            except Exception as exce_2:
                raise exce_2 from exce_1
        domainList.append(
            Domain(
                name="MovingBand_PhysicalNb",
                physicalElements=PhysicalElement("", [], airgap_mat, phyID=0),
            )
        )

        # append domain for lamination
        lam_domain = Domain(
            "Domain_Lam",
            rotorPhysicalsDict[DOMAIN_LAMINATION]
            + statorPhysicalsDict[DOMAIN_LAMINATION],
        )
        domainList.append(lam_domain)

        return domainList

    def _createDomains(
        self,
        physicalsDict: dict[str, list[PhysicalElement]],
        domainDict: dict[str, str],
    ) -> list[Domain]:
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
        domainList: list[Domain] = []
        for domainName in physicalsDict.keys():
            if domainName in domainDict.keys():
                if physicalsDict[domainName]:  # if there are physicalElements
                    domainList.append(
                        Domain(domainDict[domainName], physicalsDict[domainName])
                    )
                else:
                    # FIXME: ADD MACHINE SIDE TO DOMAIN NAME
                    logger = logging.getLogger(__name__)
                    logger.debug(
                        "There were no physical elements in domain '%s'.",
                        domainName,
                    )
        return domainList

    def _createWindingDomains(
        self, domainDict: dict[str, list[PhysicalElement]]
    ) -> dict[str, Domain]:
        """
        This function creates the winding domains for a 3-phase stator:
        Domain names are: Stator_Ind{A,B,C}{p,n}
        """
        # create dict of slots
        slotDomainDict: dict[str, Domain] = {}
        # FIXME: use try-except statment instead of for loop!
        for domain, physicalsList in domainDict.items():
            # for i, (domain, physicalsList) in enumerate(domainDict.items()):
            if domain == "domainS":
                # TODO: This implies that all slots are in domainS
                for slot in physicalsList:
                    if slot.type == "Slot":
                        slot: Slot = slot
                        # FIXME: This assumes 3-Phase winding!
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
                            slotDomainDict[slotDomainName].addPhysicalElements([slot])
                    # else:
                    # FIXME: if physical element in domainS is not type Slot:
                    # should there be an Error or Warning?
                return slotDomainDict
        return None

    def addPostOperation(self, quantityName: str, name: str, **kwargs) -> None:
        r"""Add a new PostOperation (Print) statement

        Args:
            - quantityName (str): Name of the PostProcessing quantity (eg. a,
                az, b, bn, hn, b_tangent, b_radial, br, mu, j, js, jz, Vmag,
                I_n, ir, p_Lam, P_Lam, Inertia,...)

            - name (str, optional): Name of the PostOperation.

            - \*\*kwargs: kwargs are used to complete the Print statment, so eg.
                to print Br on the whole Domain the function call would look
                like:
                .. code-block:: python

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

        name = clean_name(name)
        if name in postOperationNames:
            # if that PostOperation allready exists, get the PostOperationItem
            # with that name
            poItem = userDefinedPO.items[postOperationNames.index(name)]
        else:
            # it that PostOperation is not existing, create it
            poItem = userDefinedPO.add(Name=name, NameOfPostProcessing="MagStaDyn_a_2D")
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
        # if physicalElement.geo_list:
        #     # if the geo list is not empty
        #     # remember there can be domains without geometrical elements,
        #     # like the "MovingBand_PhysicalNb" domain
        #     code = self._createPhysicalElementCode(physicalElement)
        #     self.physicalElementCode += code

        if physicalElement not in self.physicalElementArray:
            # add physical element to array
            self.physicalElementArray.append(physicalElement)
            # add material if existing
            if (
                physicalElement.material
            ):  # TODO: Verify if this is really needed because
                # physical element should allways have material
                self._addMaterial(physicalElement)
            # add magnetization if specified
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
            # check that the material has eighter bh curve or permeability
            if material.BH.size == 0 and not material.relPermeability:
                raise RuntimeError(
                    f"Material {material.name} has neither bh curve nor relative permability!"
                )
            matDict["physicalElemID"].append([physicalElement.id])
        else:
            # otherwise find the index of the existing material
            matIndex = matDict["material"].index(material)
            # and append the PhysicalElement to the List[PhysicalElement]
            matDict["physicalElemID"][matIndex].append(physicalElement.id)

    def _addMagnetisationRadial(self, magnet: Magnet):
        magDir = magnet.magDir
        matName = clean_name(magnet.material.name)
        self.functionMagnetisation.add(
            name="br",
            expression=f"{magDir}*br_{matName} * XYZ[]/Norm[XYZ[]]",
            region=f"Region[{magnet.id}]",
        )

    def _addMagnetisationParallel(self, physicalElement: Magnet):
        matName = clean_name(physicalElement.material.name)
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
        matName = clean_name(magnet.material.name)
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
        physicalElements: list[PhysicalElement] = domain.physicals
        physIDs: list[int] = []
        for physicalElement in physicalElements:
            self._addPhysicalElement(physicalElement)
            physIDs.append(physicalElement.id)
            # allPhysicalName.append(pE.getName())
        self.group.add(clean_name(domain.name), physIDs)

    def _printAllMaterial(self):
        """Generate the GetDP function code for all materials in the material dict"""
        self.functionMaterial.define(name=["br", "js"])
        self.functionMaterial.add_params({"mu0": "4.e-7 * Pi"})

        matDict = self.materialDict
        for i, mat in enumerate(matDict["material"]):
            mat: Material = mat
            # mat: Material = self._materialDict["material"][i]
            # convert list[int] to list[str]
            physElemIDstr: list[str] = []
            for physicalElementID in self.materialDict["physicalElemID"][i]:
                physElemIDstr.append(str(physicalElementID))
            # add group for material
            matName = clean_name(mat.name)
            # FIXME: Group Add fails if mat name exists twice
            # added workaround by adding _dup id
            try:
                self.group.add(id="group_" + matName, glist=physElemIDstr)
            except ValueError as val_err:
                if re.search(r"Identifier .* already in use.", val_err.args[0]):
                    logger = logging.getLogger(__name__)
                    if self._pro_files_created:
                        # materials allready been created. Skip material if allready
                        # existing...
                        logger.info(
                            "Material '%s' has allready been created in the pro-file. "
                            "Skip duplicate creation.",
                            matName,
                        )
                        continue
                    logger.warning(
                        "Material with name %s is defined multiple times, but with different "
                        "properties. Trying to add it again with different identifier...",
                        matName,
                    )
                    matName = matName + "_dup"
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
            if mat.linear:
                # add mue_r
                mueR = mat.relPermeability
                matFun.add_params({"muR_" + matName: (mueR if mueR else 0)})
                # add nu
                matFun.add_params({"nu_" + matName: f"1/(muR_{matName} * mu0)"})
                matFun.add("nu", "nu_" + matName, "group_" + matName)
            else:
                # if non linear
                bhArray = mat.BH
                bString = "{"
                hString = "{"
                for i, bhValue in enumerate(bhArray):
                    bString += str(bhValue[0]) + ","
                    hString += str(bhValue[1]) + ","
                    if ((i + 1) % 9 == 0) and ((i + 1) != bhArray.shape[0]):
                        # add newline after 10 values if its not the last value
                        bString += "\n"
                        hString += "\n"
                bString = bString[0 : len(bString) - 1] + "\n}"
                hString = hString[0 : len(hString) - 1] + "\n}"
                matFun.add_params({f"Mat_h_{matName}": hString})
                matFun.add_params({f"Mat_b_{matName}": bString})
                matFun.add_params({f"Mat_b2_{matName}": f"Mat_b_{matName}()^2"})
                matFun.add_params(
                    {f"Mat_nu_{matName}": f"Mat_h_{matName}()/Mat_b_{matName}()"}
                )
                matFun.add_params({f"Mat_nu_{matName}(0)": f"Mat_nu_{matName}(1)"})
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
                    f"2 * dnudb2_{matName}[$1#1] * " + matFun.SquDyadicProduct("#1"),
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
            + f"""Physical Line("DomainPlotMovingGeo",{plotID}) = {{rotorBndLines[], statorBndLines[]}};\n"""
            # f"Hide {{ Line{{ Line '*' }}; }} \n"
            # + f"Hide {{ Point{{ Point '*' }}; }} \n"
            # + f"Show{{ Line {{rotorBndLines[], statorBndLines[]}}; }} \n"
        )
        return geoCode

    def _createMeshCompoundCode(
        self, physList: list[PhysicalElement], regionName: str = ""
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
        logger = logging.getLogger(__name__)
        if physList:
            meshCompCode = ""
            for physical in physList:
                if physical.material == physList[0].material:
                    if physical.geoElementType is Surface:
                        if len(physical.geo_list) > 1:
                            for geoElem in physical.geo_list:
                                meshCompCode += str(geoElem.id) + ","
                        else:
                            logger.warning(
                                'Creation of "Compound Mesh" for domain "%s" failed, because "%s" has only one surface.',
                                regionName,
                                physical.name,
                            )
                            return ""
                    else:
                        logger.warning(
                            'Creation of "Compound Mesh" for domain "%s" failed, because "%s" is not a surface.',
                            regionName,
                            physical.name,
                        )
                        return ""
                else:
                    # domain/region has different materials -> no compound surface
                    # or is not geo type surface
                    logger.warning(
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
                meshCompCode += f"}}; // {regionName}\n"  # add closing and comment
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
            Mesh.AlgorithmSwitchOnFailure = 0; // Do not switch mesh algorithm
            //on failure, because this led to mesh errors in the past
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
                meshModCode += "// Add Periodic Mesh to model symmetry boundary-lines\n"
                primeLineIDs = ""
                primary_tags = []
                for line in primeLines:
                    primary_tags.append(line.id)
                    primeLineIDs += f"{line.id},"
                # set primary lines without last comma
                meshModCode += f"primaryLines = {{{primeLineIDs[0:-1]}}};\n"
                secondIDs = ""
                secondary_tags = []
                for line in secondaryLines:
                    secondary_tags.append(line.id)
                    secondIDs += f"{line.id},"
                # set primary lines without last comma
                meshModCode += f"secondaryLines = {{{secondIDs[0:-1]}}};\n"
                # The following assumes, that the prime lines are located on
                # the x-axis. Rotation from prime to secondary occure in math.
                # positive direction!

                # Skip setting of periodic meshing condition in gmsh model since
                # its not automatically exported to any gmsh output file.
                # phi = 2 * pi / symFactor
                # transformation_matrix = array(
                #     [
                #         [cos(phi), -sin(phi), 0, 0],
                #         [sin(phi), cos(phi), 0, 0],
                #         [0, 0, 1, 0],
                #         [0, 0, 0, 1],
                #     ]
                # )
                # gmsh.model.mesh.setPeriodic(
                #     1, secondary_tags, primary_tags, transformation_matrix.flatten()
                # )

                meshModCode += (
                    r"Periodic Curve{secondaryLines[]} = {primaryLines[]} "
                    r"Rotate {{0,0,1}, {0,0,0}, "
                    f"2*Pi/{symFactor}}};\n\n"
                )

        # 4. add mesh size setting for movingband lines
        movingbandPhysicals = rotor.movingBand  # get list of movingband physicals
        if movingbandPhysicals:
            # create line id string for mesh size setting
            mbLineIDs = ""
            for physicalMovingband in movingbandPhysicals:
                if (
                    physicalMovingband.type == "MovingBand"
                    and physicalMovingband.geoElementType == Line
                ):
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in physicalMovingband.geo_list:
                        # mbLine.setMeshLength()
                        # BUG, FIXME: Only add movingband line if the
                        # arc has realy been added to the script!
                        mbLineIDs += f"{mbLine.id},"  # add the line id
            # get approx. the min mesh length of the rotor movingband
            # (only checking first line of first movingband physical)
            _, p_tags = gmsh.model.getAdjacencies(
                1, movingbandPhysicals[0].geo_list[0].id
            )
            mbMeshSize = min(gmsh.model.mesh.getSizes([(0, tag) for tag in p_tags]))
            if mbLineIDs:
                rRotorMB = rotor.movingBandRadius
                nbrSeg0 = (2 * pi * rRotorMB / mbMeshSize) - (
                    2 * pi * rRotorMB / mbMeshSize
                ) % 10  # calc number of movingband segments by steps of 10
                max_nbr_segments = max(nbrSeg0, 1440)
                # create parameter code for movingband segment setting
                meshModCode += "// Add mesh size setting for Movingband lines\n"
                meshModCode += (
                    "DefineConstant[\n"
                    + (
                        f"\tNbrMbSegments = {{{nbrSeg0}, "
                        """Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],"""
                        f"Max {max_nbr_segments}, Min 180, Step 10, Help "
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
            mbLineIDs = ""  # reset string
            for physicalMovingband in stator.movingBand:
                if (
                    physicalMovingband.type == "MovingBand"
                    and physicalMovingband.geoElementType == Line
                ):
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in physicalMovingband.geo_list:
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
            meshModCode += (
                "Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)\n\n"
            )
        return meshModCode

    def writeGeo(self, UD_MeshCode: str = "") -> None:
        """writeGeo generates the .geo-File for the current script.

        Args:
            UD_MeshCode (str): User defined code to modify mesh settings. This
            will be printed *before* the internal mesh settings because
            otherwise Movingsband-Mesh could be overwritten. Must be conformal
            with the gmsh syntax!
        """
        logger = logging.getLogger(__name__)
        # add the code for the mesh settings and mesh modification
        meshSettingsCode = 'INPUT_MESH = "Input/04Mesh/";\n'
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
            "\tFlag_individualColoring = {0,"
            + 'Name StrCat[INPUT_MESH, "09Individual Mesh Coloring"], '
            + "Choices {0, 1}}\n];\n"
        )
        meshSettingsCode += "Mesh.MeshSizeFactor = gmsf;\n"
        # show mesh Lines without lighting
        meshSettingsCode += (
            "Mesh.SurfaceEdges = 1;\nMesh.Light = 0;\nMesh.SurfaceFaces = 1;\n"
        )
        meshSettingsCode += "Mesh.Algorithm = 6; // Frontal-Delaunay for 2D meshes\n"
        # TODO: This can be removed with a new GetDP version according to:
        # https://gitlab.onelab.info/gmsh/gmsh/-/issues/3194
        meshSettingsCode += "Mesh.MshFileVersion = 4.0; // Fix bug in mesh file creation for GetDP Version 3.6.0\n"
        meshSettingsCode += "\n"

        meshModCode = ""
        movingGeoCode = ""
        if self.machine:
            # TODO: Check that the geometry in PyEMMO is still up to date with gmsh.
            #       Probably the ID of surfaces changed due to boolean operations
            # add the code for mesh modifications
            meshModCode = self._createMeshModCode()
            # add the code for plotting the moving boundary in post processing
            movingGeoCode = self._createMovingGeoCode()

        # write out all the geometry and physicals code to .geo_unrolled file

        # NOTE: add default point in geo (internal gmsh) kernel to force geo_unrolled
        # output instead of .xao format (new in gmsh 4.14.0). See issue
        # https://gitlab.onelab.info/gmsh/gmsh/-/issues/3214 and comment
        # https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/src/geo/GModelIO_GEO.cpp?ref_type=heads#L1840
        # for more info

        # FIXME: This should trigger gmsh to export the geometry as real
        # geo_unrolled according to the above links, but doesn't work with
        # gmsh==4.14.0 ...
        # tmp_point_tag = gmsh.model.geo.addPoint(0, 0, 0, 1.0)
        # gmsh.model.geo.addPhysicalGroup(0, [tmp_point_tag], name="dummy point")

        geo_unrolled_path = self.geoFilePath + "_unrolled"
        gmsh.write(geo_unrolled_path)
        # read in the file content
        with open(geo_unrolled_path, "r+") as fd:
            geo_code = fd.readlines()
            # contents.insert(0, new_string)  # new_string should end in a newline
            fd.seek(0)  # readlines consumes the iterator, so we need to start over
            # fd.writelines(contents)  # No need to truncate as we are increasing
        os.remove(geo_unrolled_path)

        with open(self.geoFilePath, "w", encoding="utf-8") as geoScript:
            geoScript.write(versionStr)  # write the pyemmo version number
            # create Expert Mode Flag
            geoScript.write(
                """DefineConstant[\n Flag_ExpertMode = {1,"""
                + """Name '01View/Expert Mode', Choices {0, 1}}\n];\n\n"""
            )
            geoScript.write(meshSettingsCode)  # write code for mesh variables
            geoScript.writelines(geo_code)
            if self.colorCode:
                # TODO: Update to create color code from physical elements,
                # because the colors set by the gmsh api are not exported to
                # the geo_unrolled file.
                geoScript.write(
                    "\n// Color code\n"
                    + """If (!Flag_individualColoring)\n"""
                    + self.colorCode
                    + """EndIf\n"""
                )
            geoScript.write(UD_MeshCode)
            geoScript.write(meshModCode)
            # write code to only show physicals
            geoScript.write(
                "Hide {:}\nRecursive Show { Physical Surface{:}; }\n"
                "Recursive Show { Physical Curve{:}; }\n"
                "Geometry.PointSize = 3.0;\n\n"
            )
            geoScript.write(movingGeoCode)
        # set flag that geometry files have been created to true
        self._geo_files_created = True

        logger.debug(
            "I found %d identical points. There are %d points in the model.",
            self.nbrIdedentPoints,
            len(self.pointArray),
        )
        logger.debug(
            "I found %d identical lines. There are %d lines in the model.",
            self.nbrIdedentLines,
            len(self.curveList),
        )

    def _setParameters(self):
        """Set the machine parameters for the script to the
        ``Script.simParams`` attribute.
        """
        logger = logging.getLogger(__name__)
        machine = self.machine
        if not machine:
            raise RuntimeError("There was no machine specified. Add machine to script.")
        simuParamDict = self.simParams
        # 1. Set geometrical parameters via "machine.getSimParams()"
        #   SYMMETRY_FACTOR, L_AX_R, L_AX_S, NBR_POLE_PAIRS, NBR_TURNS_IN_FACE
        geometryParams = machine.getSimParams()
        # TODO: Improve check here...
        # assert len(geometryParams) == len(simuParamDict.GEO) # assert there
        # is the correct number of parameters

        # update machine parameters:
        simuParamDict["GEO"] = {**simuParamDict["GEO"], **geometryParams}

        # Create default parameters for rotor and stator airgap field post processing
        for side in ("rotor", "stator"):
            mside: Rotor | Stator = getattr(machine, side)
            for phys in mside._domainAirGap.physicals:
                airgap_radii = []
                for geo in phys.geo_list:
                    # calc mean radius
                    geo: Surface = geo
                    for p in geo.points:
                        if isclose(p.y, 0, abs_tol=DEFAULT_GEO_TOL):
                            airgap_radii.append(p.x)
                if not airgap_radii:
                    logger.warning(
                        "No points near x-axis found in %s airgap physical element '%s'. "
                        "Cannot calculate mean radius for airgap field post processing.",
                        side,
                        phys.name,
                    )
                    airgap_radii = [0.0]  # set to zero if no points found
                # set mean radius default value
                simuParamDict["GEO"][f"R_{side.upper()}_AIRGAP"] = mean(airgap_radii)

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
                    if not mat.linear:
                        flagCalcNL = 1
                        break  # if one BH curve is found, we can stop the loop
                    if isinstance(physicalElement, Magnet):
                        hasMagnets = True
        simuParamDict["SYM"]["FLAG_NL"] = flagCalcNL
        if not hasMagnets and simuParamDict["SYM"]["CALC_MAGNET_LOSSES"] == 1:
            # if there where no magnet physical elements, set flag to false
            # even if its set to true...
            logger.warning(
                "Unsetting the flag 'CALC_MAGNET_LOSSES', because"
                " no magnets where found in the machine."
            )
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
            if logger.level <= logging.DEBUG:
                if not os.path.exists(self.resultsPath):
                    os.mkdir(self.resultsPath)
                machine.stator.winding.save_to_file(
                    os.path.join(self.resultsPath, f"winding_{self.name}.wdg")
                )

            # Stator angle for I_U = 1 p.u., I_V = -1/2, I_W = -1/2 in rad elec
            try:
                # get index of fundamental MMF electrical order
                elec_order_index = where(mmfOrder == nbrPolePairs)
                system_offset = float(angle[elec_order_index[0][0]])
                logger.debug(
                    "Stator north pole angle (elec): %.4f°", rad2deg(system_offset)
                )
            except Exception as e:
                logger.warning(
                    "Cant find single fundamental MMF order in harmonics of SWAT-EM winding."
                    "Can't determine Park transformation offset angle.",
                    exc_info=e,
                )
                system_offset = None

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
            if system_offset is not None:
                magnetisations: list[str] = []
                for mag in machine.rotor._domainM.physicals:
                    mag: Magnet = mag
                    magnetisations.append(mag.magType == "tangential")
                if any(magnetisations):
                    logger.warning(
                        "Tangential magnetization detected! Dq-offset calculation is invalid"
                    )
                    dqOffset = 0
                else:
                    dqOffset = (
                        -rad2deg(slotPitch / 2 * nbrPolePairs)
                        + rad2deg(system_offset)
                        + 270
                    )
            else:
                dqOffset = 0
            simuParamDict["SYM"]["ParkAngOffset"] = dqOffset

    def _getParamCode(self, paramName: str, paramValue) -> str:
        """
        Get a line of parameter code:
        .. code-block:: python

            paramCode = f"{paramName} = {paramValue}
        """
        if isinstance(paramValue, (str)):
            paramCode = f'{paramName} = "{paramValue}";\n'  # add "" for string value
        else:  # isinstance(paramValue,(int, float)):
            paramCode = f"{paramName} = {paramValue};\n"
        return paramCode

    def _createParamCode(self) -> str:
        """Create the string code for the parameter file"""
        self._setParameters()  # set Parameters to write code
        paramDict = self.simParams
        paramCode: str = "// MACHINE SPECIFIC VALUES\n"
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
        logger = logging.getLogger(__name__)
        # Write the code
        #   1. write parameter file
        machineTempFile = abspath(join(MAIN_DIR, "script", "machine_template.pro"))
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
        machineFileCode = machineFileCode.replace("GROUP_CODE", self.group.code, 1)

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
        calcFileTempPath = join(MAIN_DIR, "script", calculationFileName).replace(
            "\\", "/"
        )
        # read the template file
        with open(calcFileTempPath, encoding="utf-8") as templateCalcFile:
            calcCode = versionStr + templateCalcFile.read()

        calcFilePath = join(self.scriptPath, calculationFileName).replace(
            "\\", "/"
        )  # filepath to the destination of the calculation file
        # write the magstadyn file to new destination
        with open(calcFilePath, "w", encoding="utf-8") as calcFile:
            calcFile.write(calcCode)

        ## COPY CIRCUIT FILE
        shutil.copy(
            join(MAIN_DIR, "script", "Circuit_SC_ASM.pro"),
            join(self.scriptPath, "Circuit_SC_ASM.pro"),
        )

        #  6.1 add the PostOperation command code before including the
        # magstatdyn-file
        postOperation = self.postOperation
        if postOperation.items:  # if there are Items in PostOperation
            # add the code for the compute command including the postoperations
            # TODO: Add option for "-bin" case (user setting)
            # TODO: adapt output verbosity based on internal verbosity

            computeCommandCode = (
                "DefineConstant[\n\t"
                """R_ = {"Analysis", Name "GetDP/1ResolutionChoices", Visible Flag_Debug || Flag_ExpertMode},\n\t"""
                """C_ = {"-solve -v 3 -v2 -pos", Name "GetDP/9ComputeCommand", Visible Flag_Debug || Flag_ExpertMode}\n\t"""
                """P_ = {\""""
                + ",".join(self.postOperationNames)
                + """", Name "GetDP/2PostOperationChoices", Visible Flag_Debug || Flag_ExpertMode}\n"""
                "];\n"
            )
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

        # If logging is set to debug, save the winding to a file
        if logger.getEffectiveLevel() <= logging.DEBUG:
            if not os.path.exists(self.scriptPath):
                os.mkdir(self.scriptPath)
            self.machine.stator.winding.save_to_file(
                os.path.join(self.scriptPath, f"winding_{self.name}.wdg")
            )
        self._pro_files_created = True

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
        logger = logging.getLogger(__name__)
        if self._gmsh_model != gmsh.model.getCurrent():
            logger.warning(
                "Gmsh model did change! Resetting to '%s' for script generation.",
                self._gmsh_model,
            )
            try:
                gmsh.model.setCurrent(self._gmsh_model)
            except Exception as e:  # pylint: disable=W0718
                logger.fatal(
                    "Could not reset gmsh model '%s'!", self._gmsh_model, exc_info=True
                )
                raise e
        if mode == 0:
            self.writeGeo(UD_MeshCode=UD_MeshCode)
            self.writePro()

        elif mode == 1:
            self.writeGeo(UD_MeshCode=UD_MeshCode)
        elif mode == 2:
            self.writePro()
