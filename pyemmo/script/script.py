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
""""""

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
    boundary_domain_dict,
    default_param_dict,
    rotor_domain_dict,
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
    from .machine import Machine
    from .material.material import Material
    from .rotor import Rotor
    from .stator import Stator


class Script:
    """
    Script class for generating GetDP simulation files from a PyEMMO machine model.
    This class manages the creation of .geo (geometry) and .pro (GetDP) files for
    electromagnetic finite element simulations. It handles:

    - Domain and material definitions
    - Mesh configuration and constraints
    - Post-processing operations
    - Simulation parameter management

    The Script class integrates with a :class:`~pyemmo.script.machine.Machine` object to automatically generate
    geometry-dependent parameters and domain definitions for both rotor and stator
    components.
    """

    def __init__(
        self,
        name: str,
        scriptPath: str,
        simuParams: dict,
        machine: Machine | None = None,
        resultsPath: str = "",
    ):
        """
        Args:
            name (str): script name
            scriptPath (str): path, where the geo and pro scripts should be
                saved
            simuParams (dict): Dictionary with different parameters to initialize the
                ONELAB paramters defined in the *machine_template.pro* file. See
                :data:`~pyemmo.script.default_param_dict` for or the example below for
                more details.
            machine (Machine): pyemmo machine object for domain definitions and geometic
                parameters. Defaults to None.
            resultsPath (str, optional): path, where the simulation results
                should be stored. Defaults to a folder in scriptPath with name
                "res_{scriptName}".


        Example simulation paramter dictionary:

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
        self.script_path = scriptPath
        # directory to save simulation results
        self.results_path = (
            abspath(resultsPath).replace("\\", "/")
            if resultsPath
            else abspath(join(scriptPath, "res_" + self.name)).replace("\\", "/")
        )

        self.color_code: str = ""  # code for mesh colors

        # list of phyiscal elements to make sure physicals and its properties are not
        # added twice.
        self._physicals: list[PhysicalElement] = []

        # group object to create the domains in the .pro file.
        # This contails the domain definitions of the individual phyiscals and
        # the material domains.
        self.group = GroupGetDP()
        self._materialDict: dict[str, list[list[int]]] = {
            "material": [],
            "physicalElemID": [],
        }
        self.function_material = FunctionGetDP()
        self.function_magnetization = FunctionGetDP()

        self._post_operation = PostOperation()

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

        # set flags to check if files have been created trough generateScript()
        self._pro_files_created = False
        self._geo_files_created = False

        # Save current gmsh model name, because if the model files shall be regenerated
        # but the model has changed due to post processing e.g., we need to reset the
        # model or raise an error
        self._gmsh_model: str = gmsh.model.getCurrent()  # get current model

        # add machine domains
        self._machine = machine  # do not set machine via setter function, because this
        # will reset the script object!
        if machine:
            self._add_machine_domains()
        # else
        #   machine is None...

    # -------------------------------------------------------------------------
    # ----------------- START OF GETTER AND SETTER FUNCTIONS ------------------
    # -------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Name of the script, used for file naming.

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
    def script_path(self) -> str | os.PathLike:
        """Get the path, where the model files (.geo & .pro) are stored.

        Returns:
            str: path where the model files should be stored.
        """
        return self._scriptPath

    @script_path.setter
    def script_path(self, newScriptPath: str | os.PathLike):
        """setter of Script Path

        Args:
            newScriptPath (os.PathLike): New path to folder where ONELAB files
                should be stored.
        """
        self._scriptPath = newScriptPath

    @property
    def pro_file_path(self) -> str:
        """Get the path to the resulting .pro file named "ScriptName.pro"

        Returns:
            str: path to the pro Script file
        """
        return join(self.script_path, self.name + ".pro")

    @property
    def geo_file_path(self) -> str:
        """Get the path to the resulting .geo file named "ScriptName.geo"

        Returns:
            str: path to the geo Script file
        """
        return join(self.script_path, self.name + ".geo")

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
            scriptPath=self.script_path,
            simuParams=self.sim_params,
            machine=newMachine,
            resultsPath=self.results_path,
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
    def results_path(self) -> str:
        """
        path to the folder where the simulation results are stored
        (simulation results folder)

        Retruns:
            str
        """
        return self._resPath

    @results_path.setter
    def results_path(self, resPath: str):
        """Setter of the attribute resPath"""
        self._resPath = resPath
        self._simulationParameters["SYM"]["PATH_RES"] = resPath

    @property
    def sim_params(self) -> dict:
        """Getter of the attribute simulationParameters"""
        return self._simulationParameters

    @property
    def material_dict(self) -> dict[str, list]:
        """Material dict of the current model.

        Returns:
            Dict[str, List]: dictionary with two elements. The first "material" is a
            list of :class:`~pyemmo.script.material.material.Material` objects. And
            the second "physicalElemID" is a list of lists with the gmsh physical surface
            ids.

        .. code-block:: python

            {
                "material": [ListOfMaterials],
                "physicalElemID":  [[physicalIDs],[physicalIDs],...]
            }

        Every material in the material list has a list of physical element IDs in the
        physicalElemID-List(=List of lists).

        """
        return self._materialDict

    @property
    def post_operation(self) -> PostOperation:
        """get the user defined PostOperations

        Returns:
            PostOperation
        """
        return self._post_operation

    @post_operation.setter
    def postOperations(self, postOperation: PostOperation) -> None:
        """set the user defined PostOperation

        Args:
            postOperation (PostOperation): PostOperation object
        """
        if isinstance(postOperation, PostOperation):
            self._post_operation = postOperation
            return None
        msg = (
            "Given object was not of type PostOperation: "
            + str(type(postOperation))
            + str(postOperation)
        )
        raise TypeError(msg)

    def get_post_operation_names(self) -> list[str]:
        """Get a list of GetDP PostOperation names defined in Script.

        Returns:
            List[str]: List of GetDP PostOperation Names
        """
        postOperation = self.post_operation
        return [POItem.Name for POItem in postOperation.items]

    # -------------------------------------------------------------------------
    # ------------------- END OF GETTER AND SETTER FUNCTIONS ------------------
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # -------------------------- START OF PRO FUNCTIONS -----------------------
    # -------------------------------------------------------------------------

    def _add_machine_domains(self):
        """Add the machine domains created by _create_machine_domains() to the script
        group and return the domain list."""
        logger = logging.getLogger(__name__)
        domain_list = self._create_machine_domains()
        for domain in domain_list:
            logger.debug("Adding domain %s", domain.name)
            self._add_domain(domain)
        return domain_list

    def _create_machine_domains(self) -> list[Domain]:
        """
        Create Domain objects from the output (Dict[domainName,
        List[PhysicalElements]]) of rotor and stator sortPhysicals() by linking
        them with the domain names for the magstatdyn file specified in
        ``rotorDomainDict`` and ``statorDomainDict`` (Dict[statorDomainName,
        magStatDynName])

        Returns:
            List[Domain]: Domain list containing domains suitable for the
                magstatdyn.pro file. The order of that list is important since
                it dicides which points and lines are created first and which
                are sorted out!
        """
        domain_list: list[Domain] = []
        stator_physicals = self.machine.stator.sortPhysicals()
        rotor = self.machine.rotor
        rotor_physicals = rotor.sortPhysicals()
        # create (boundary) domains existing in rotor AND stator (primary,
        # secondary lines) These domains MUST be created first, because meshing
        # constraints need to be applied on them and this is only possible if
        # the line IDs of these lines are not sorted out due to identical
        # lines. The domains will be created in the order they appeer in this
        # domain list!
        for domain_name in stator_physicals.keys():
            if domain_name in boundary_domain_dict:
                boundary_domain = Domain(
                    boundary_domain_dict[domain_name],
                    stator_physicals[domain_name],
                )
                if domain_name in rotor_physicals.keys():
                    # boundary also exists in rotor
                    boundary_domain.addPhysicalElements(rotor_physicals[domain_name])
                domain_list.append(boundary_domain)

        # create rotor domains
        # move domainC to domainCC because eddy currents are handled in GetDP
        rotor_physicals[DOMAIN_NON_CONDUCTING].extend(
            rotor_physicals[DOMAIN_CONDUCTING]
        )
        rotor_physicals[DOMAIN_CONDUCTING].clear()

        # create remaining domains
        domain_list.extend(self._create_domains(rotor_physicals, rotor_domain_dict))

        # Create single Bar regions
        if DOMAIN_BAR in rotor_physicals:
            # sort bars in circumferential direction to make sure their indices are in
            # the correct order for the use with the external squirrle cage circuit.
            rotor_physicals[DOMAIN_BAR].sort(key=Slot.get_circumferential_position)
            for i, region in enumerate(rotor_physicals[DOMAIN_BAR]):
                domain_list.append(Domain(f"Rotor_Bar_{i+1}", region))

        # add additional domains for every movinband part, to specify the
        # Link-boundary in magstatdyn
        for domain in domain_list:
            if domain.name == "Rotor_Bnd_MB":
                for i, mb_physical in enumerate(domain.physicals):
                    domain_list.insert(
                        3 + i,
                        Domain(
                            name=f"Rotor_Bnd_MB_{i+1}",
                            physicalElements=[mb_physical],
                        ),
                    )
                break

        # create stator domains
        # move domainC to domainCC
        # Decition where eddy currents shall be calculated should be made in .pro file
        # depening on parameters.
        stator_physicals[DOMAIN_NON_CONDUCTING].extend(
            stator_physicals[DOMAIN_CONDUCTING]
        )
        stator_physicals[DOMAIN_CONDUCTING].clear()

        # add stator domains to domain list
        domain_list.extend(self._create_domains(stator_physicals, statorDomainDict))

        # create additional slot domains for excitations
        domain_list.extend(self._create_winding_domains(stator_physicals).values())

        # append domains to identify linear and non-linear surfaces
        non_linear_domain = Domain(
            "DomainNL",
            rotor_physicals[DOMAIN_NON_LINEAR] + stator_physicals[DOMAIN_NON_LINEAR],
        )
        domain_list.append(non_linear_domain)

        linear_domain = Domain(
            "DomainL",
            rotor_physicals[DOMAIN_LINEAR] + stator_physicals[DOMAIN_LINEAR],
        )
        domain_list.append(linear_domain)

        # Create default domain for Movingband
        # This needs to be done here since we need to add it to the airgap
        # material domain.
        # TODO: This could be handled by the pro-file for sure.
        try:
            airgap_mat = stator_physicals[DOMAIN_AIRGAP][0].material
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception as exce_1:
            try:
                airgap_mat = rotor_physicals[DOMAIN_AIRGAP][0].material
            except Exception as exce_2:
                raise exce_2 from exce_1
        domain_list.append(
            Domain(
                name="MovingBand_PhysicalNb",
                physicalElements=PhysicalElement("", [], airgap_mat, phyID=0),
            )
        )

        # append domain for lamination
        lam_domain = Domain(
            "Domain_Lam",
            rotor_physicals[DOMAIN_LAMINATION] + stator_physicals[DOMAIN_LAMINATION],
        )
        domain_list.append(lam_domain)

        return domain_list

    def _create_domains(
        self,
        physicals: dict[str, list[PhysicalElement]],
        domain_name_dict: dict[str, str],
    ) -> list[Domain]:
        """
        Create a list of domains from the Rotor and Stator physicals dict with domain
        name as key and list of corresponding physical elements as value and a domain
        dict that associates the default domain names defined in :mod:`pyemmo.script`
        with the actual GetDP domain names.
        This ensures that the domain names in the machine_template.pro are independed
        of the PyEMMO definitions.

        Args:
            physicals (dict): Dict with domain name as key string and a
                list of physical elements containing to that domain
                ["Domain Name", List[PhysicalElements]].
            domain_name_dict (dict): Dict with domain name as key string and
                pro-script domain name as value.

                .. code:: python

                    {"Domain Name", "Pro-Script Name"}

        Returns:
            List[Domain]: List of domains with correct pro script names and
                physicals.

                .. code:: python

                    [Domain(name="Pro-Script Name", List[PhysicalElements]), ...]
        """
        domain_list: list[Domain] = []
        for domain_name in physicals.keys():
            if domain_name in domain_name_dict:
                if physicals[domain_name]:  # if there are physicalElements
                    domain_list.append(
                        Domain(domain_name_dict[domain_name], physicals[domain_name])
                    )
                else:
                    # FIXME: ADD MACHINE SIDE TO DOMAIN NAME
                    logger = logging.getLogger(__name__)
                    logger.debug(
                        "There were no physical elements in domain '%s'.",
                        domain_name,
                    )
        return domain_list

    def _create_winding_domains(
        self, domainDict: dict[str, list[PhysicalElement]]
    ) -> dict[str, Domain]:
        """
        This function creates the winding domains for a 3-phase stator:
        Domain names are: Stator_Ind{A,B,C}{p,n}
        """
        # create dict of slots
        slot_domains: dict[str, Domain] = {}
        # FIXME: use try-except statment instead of for loop!
        for domain, physicals in domainDict.items():
            # for i, (domain, physicalsList) in enumerate(domainDict.items()):
            if domain == "domainS":
                # TODO: This implies that all slots are in domainS
                for slot in physicals:
                    if slot.type == "Slot":
                        slot: Slot = slot
                        # FIXME: This assumes 3-Phase winding!
                        phase = slot.getPhase("ABC")
                        slot_domain_name = (
                            "Stator_Ind_"
                            + phase
                            + ("p" if slot.windDirection == 1 else "m")
                        )
                        if slot_domain_name not in slot_domains:
                            # add domain to slot dict
                            slot_domains[slot_domain_name] = Domain(
                                slot_domain_name, slot
                            )
                        else:
                            # add slot to existing domain
                            slot_domains[slot_domain_name].addPhysicalElements([slot])
                    # else:
                    # FIXME: if physical element in domainS is not type Slot:
                    # should there be an Error or Warning?
                return slot_domains
        return None

    def add_post_operation(self, quantityName: str, name: str, **kwargs) -> None:
        r"""Add a new PostOperation (Print) statement

        Args:

            quantityName (str): Name of the PostProcessing quantity (eg. a,
                az, b, bn, hn, b_tangent, b_radial, br, mu, j, js, jz, Vmag,
                I_n, ir, p_Lam, P_Lam, Inertia,...)
            name (str, optional): Name of the PostOperation.

        Additionally kwargs can be used to complete the Print statment, so eg.
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

        See https://getdp.info/doc/texinfo/getdp.html#Types-for-PostOperation
        for more PostOperation options.
        """
        po_names = self.get_post_operation_names()
        # search in the user defined PostOperation if there is a PO with that
        # name. Remember: our self._postOperation object of type
        # (PostOperation) has a list of PostOperations ("items") which can have
        # several "Operations" (eg. Prints, Echos,...) defined

        name = clean_name(name)
        if name in po_names:
            # if that PostOperation allready exists, get the PostOperationItem
            # with that name
            po_item = self.post_operation.items[po_names.index(name)]
        else:
            # it that PostOperation is not existing, create it
            po_item = self.post_operation.add(
                Name=name, NameOfPostProcessing="MagStaDyn_a_2D"
            )
        po_item: PostopItem = po_item
        po_item.add().add(quantity=quantityName, **kwargs)
        if "File" in kwargs:
            if "CAT_RESDIR" in kwargs["File"]:
                res_file: str = kwargs["File"]
                res_file_name = res_file.lstrip("CAT_RESDIR").lstrip("\\")
                po_item.item[-1].code = po_item.item[-1].code.replace(
                    f'"{kwargs["File"]}"', f'StrCat[ResDir,"{res_file_name}"]'
                )

    # -------------------------------------------------------------------------
    # -------------------------- END OF PRO FUNCTIONS -------------------------
    # -------------------------------------------------------------------------

    def _add_physical(self, physical_element: PhysicalElement) -> None:
        """Add a PhysicalElement to the Script.

        This calls:

            - :meth:`~pyemmo.script.script.Script._addMaterial`
              if material is not defined yet.
            - addMagnetization() (radial, parallel or tangential) if physical
              is a Magnet.

        Args:
            physical_element (PhysicalElement): Physical Element to add to Script.
        """
        if physical_element not in self._physicals:
            # add physical element to array
            self._physicals.append(physical_element)
            # add material if existing
            # TODO: Verify if this is really needed because physical element should
            # allways have material
            if physical_element.material:
                self._add_material(physical_element)
            # add magnetization if specified
            if isinstance(physical_element, Magnet):
                mag: Magnet = physical_element
                typeMag = mag.magType
                if typeMag == "radial":
                    self._addMagnetisationRadial(physical_element)
                elif typeMag == "parallel":
                    self._addMagnetisationParallel(physical_element)
                elif typeMag == "tangential":
                    self._addMagnetisationTangential(physical_element)
                else:
                    raise TypeError(
                        f"Wrong Magnetisation Type: '{typeMag}'."
                        + "Magnetisation Type must be 'radial', 'parallel' or "
                        + "'tangential'."
                    )

    def _add_material(self, physical_element: PhysicalElement) -> None:
        """
        Add the material of a physical element to the ``material_dict``.
        If the material allready exists in the material dict, its physical
        element ID is added to the physical element list of that material.

        Args:
            physical_element (PhysicalElement): Physical element (PE) which
                material should be added to the script. If the material of the
                PE is allready in the material dict of the script, the PE-ID is
                added to the material dict.

        Returns:
            None
        """
        # if the material is not in the material dict
        mat_dict = self.material_dict
        material = physical_element.material
        if material not in mat_dict["material"]:
            mat_dict["material"].append(material)
            # check that the material has eighter bh curve or permeability
            if material.BH.size == 0 and not material.relPermeability:
                raise RuntimeError(
                    f"Material {material.name} has neither bh curve nor relative permability!"
                )
            mat_dict["physicalElemID"].append([physical_element.id])
        else:
            # otherwise find the index of the existing material
            mat_index = mat_dict["material"].index(material)
            # and append the PhysicalElement to the List[PhysicalElement]
            mat_dict["physicalElemID"][mat_index].append(physical_element.id)

    def _addMagnetisationRadial(self, magnet: Magnet):
        magDir = magnet.magDir
        matName = clean_name(magnet.material.name)
        self.function_magnetization.add(
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
        self.function_magnetization.add(
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
        self.function_magnetization.add(
            "br",
            magFunction,
            f"Region[{magnet.id}]",
        )

    def _add_domain(self, domain: Domain):
        """Add a group with the domain name to the getdp-group section."""
        ids: list[int] = []
        for physical in domain.physicals:
            self._add_physical(physical)
            ids.append(physical.id)
            # allPhysicalName.append(pE.getName())
        self.group.add(clean_name(domain.name), ids)

    def _create_material_code(self):
        """Generate the GetDP function code for all materials in the material dict"""
        self.function_material.define(name=["br", "js"])
        self.function_material.add_params({"mu0": "4.e-7 * Pi"})

        for i, mat in enumerate(self.material_dict["material"]):
            mat: Material = mat
            # mat: Material = self._materialDict["material"][i]
            # convert list[int] to list[str]
            physElemIDstr: list[str] = []
            for physicalElementID in self.material_dict["physicalElemID"][i]:
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
            matFun = self.function_material
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

    def _create_moving_code(self) -> str:
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

    def _create_compound_code(
        self, physicals: list[PhysicalElement], name: str = ""
    ) -> str:
        """Generate the code for a compound mesh of several surfaces.
        The code looks like:

            .. code::

                Compound Surface{27,28,29,30,31}; // Stator airgap

        for the stator airgap surfaces (IDs 27 to 31)

        Args:
            physicals (List[PhysicalElement]): list of physical elements to
                combine. The IDs are extracted.
            name (str): region name for the comment

        Returns:
            str: Compound mesh code.
        """
        logger = logging.getLogger(__name__)
        if not physicals:
            return ""
        comp_code = ""
        for physical in physicals:
            if physical.material != physicals[0].material:
                # domain/region has different materials -> no compound surface
                # or is not geo type surface
                logger.warning(
                    (
                        "Creation of 'Compound Mesh' for domain '%s' failed, ",
                        name,
                    )
                    + ("because materials of '%s' and ", physicals[0].name)
                    + ("'%s' don't match.", physical.name)
                )
                return ""
            if physical.geoElementType is Surface:
                if len(physical.geo_list) > 1:
                    for geoElem in physical.geo_list:
                        comp_code += str(geoElem.id) + ","
                else:
                    logger.warning(
                        'Creation of "Compound Mesh" for domain "%s" failed, because '
                        '"%s" has only one surface.',
                        name,
                        physical.name,
                    )
                    return ""
            else:
                logger.warning(
                    'Creation of "Compound Mesh" for domain "%s" failed, because "%s" '
                    "is not a surface.",
                    name,
                    physical.name,
                )
                return ""

        # make sure there is code
        if comp_code:
            comp_code = "Compound Surface{" + comp_code[0:-1]  # erase last comma
            comp_code += f"}}; // {name}\n"  # add closing and comment
            return comp_code
        else:
            return ""

    def _create_mesh_code(self) -> str:
        """Create the code to individually modify the mesh size of the machine domains.

        This adds a bunch of code lines to the .geo file to modify the mesh. The main
        modification are:

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
        rotor_dict = rotor.sortPhysicals()

        stator = self.machine.stator
        stator_dict = stator.sortPhysicals()

        mesh_code = "\n// Mesh operations\n\n"
        # 1. add compound mesh for domain
        mesh_code += (
            "// Do not switch mesh algorithm on failure, "
            + "because this led to mesh errors in the past.\n"
            + "Mesh.AlgorithmSwitchOnFailure = 0;"
        )
        mesh_code += (
            "DefineConstant[Flag_CompoundMesh = {0, "
            + """Name StrCat[INPUT_MESH, "Compound Mesh"], Choices {0,1}, """
            + """Help "Use Compound Mesh to ignore lines between segments while meshing.","""
            + """Visible Flag_ExpertMode}];\n"""
        )
        mesh_code += """If (Flag_CompoundMesh)\n"""
        for region in ["domainLam", "airGap"]:
            # for region in ["domainLam"]:
            physicals = rotor_dict[region]
            if physicals:
                mesh_code += self._create_compound_code(physicals, ("rotor " + region))
            physicals = stator_dict[region]
            if physicals:
                mesh_code += self._create_compound_code(physicals, ("stator " + region))
        mesh_code += """EndIf // (Flag_CompoundMesh)\n\n"""

        # 2. add mesh size setting via factor
        # Allready done in json API. This would need a other grouping instead
        # of GetDP domains

        # 3. add periodic meshing constraint for primary and secondary lines
        sym_factor = self.machine.symmetryFactor
        if sym_factor > 1:
            prime_lines = self.machine.primaryLines
            secondary_lines = self.machine.getSecondaryLines()
            if prime_lines and secondary_lines:
                mesh_code += "// Add Periodic Mesh to model symmetry boundary-lines\n"
                primeLineIDs = ""
                primary_tags = []
                for line in prime_lines:
                    primary_tags.append(line.id)
                    primeLineIDs += f"{line.id},"
                # set primary lines without last comma
                mesh_code += f"primaryLines = {{{primeLineIDs[0:-1]}}};\n"
                secondIDs = ""
                secondary_tags = []
                for line in secondary_lines:
                    secondary_tags.append(line.id)
                    secondIDs += f"{line.id},"
                # set primary lines without last comma
                mesh_code += f"secondaryLines = {{{secondIDs[0:-1]}}};\n"
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

                mesh_code += (
                    r"Periodic Curve{secondaryLines[]} = {primaryLines[]} "
                    r"Rotate {{0,0,1}, {0,0,0}, "
                    f"2*Pi/{sym_factor}}};\n\n"
                )

        # 4. add mesh size setting for movingband lines
        if rotor.movingBand:
            # create line id string for mesh size setting
            mb_ids = ""
            for mb in rotor.movingBand:
                if mb.type == "MovingBand" and mb.geoElementType == Line:
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in mb.geo_list:
                        # mbLine.setMeshLength()
                        # BUG, FIXME: Only add movingband line if the
                        # arc has realy been added to the script!
                        mb_ids += f"{mbLine.id},"  # add the line id
            # get approx. the min mesh length of the rotor movingband
            # (only checking first line of first movingband physical)
            _, p_tags = gmsh.model.getAdjacencies(1, rotor.movingBand[0].geo_list[0].id)
            mb_meshsize = min(gmsh.model.mesh.getSizes([(0, tag) for tag in p_tags]))
            if mb_ids:
                r_rotor_mb = rotor.movingBandRadius
                nbr_seg0 = (2 * pi * r_rotor_mb / mb_meshsize) - (
                    2 * pi * r_rotor_mb / mb_meshsize
                ) % 10  # calc number of movingband segments by steps of 10
                max_nbr_segments = max(nbr_seg0, 1440)
                # create parameter code for movingband segment setting
                mesh_code += "// Add mesh size setting for Movingband lines\n"
                mesh_code += (
                    "DefineConstant[\n"
                    + (
                        f"\tNbrMbSegments = {{{nbr_seg0}, "
                        """Name StrCat[INPUT_MESH, "Number of Rotor Movingband Segments"],"""
                        f"Max {max_nbr_segments}, Min 180, Step 10, Help "
                        '"Set the number of mesh segments on the interface between rotor/stator'
                        "airgap and movingband. Value represents number of segments on whole "
                        'circle.", Visible Flag_ExpertMode},\n'
                    )
                    + f"\tr_MB_R = {r_rotor_mb}"  # rotor movingband radius as parameter
                    # + ",\n"
                    # + """\trotorMBMesh = {360, Name StrCat[INPUT_MESH, "Number of Roto
                    # Movingband Segments"], Min 180, Step 10, Help "Set the number of mesh
                    # segments on the interface between rotor airgap and movingband.",
                    # Visible Flag_ExpertMode}""" +
                    "\n];\n"
                )
                # create movingband line id list, because its cleaner
                mesh_code += f"MB_LinesR = {{{mb_ids[0:-1]}}};\n"
                # set the mesh size for all movingband points
                mesh_code += (
                    "MeshSize{ PointsOf{Line{MB_LinesR[]};}} = "
                    "2*Pi*r_MB_R/NbrMbSegments;\n\n"
                )
            # same thing for stator movingband with number of segments of
            # rotor movingband
            mb_ids = ""  # reset string
            for mb in stator.movingBand:
                if mb.type == "MovingBand" and mb.geoElementType == Line:
                    # if the mobingband object is type movingband and its
                    # geo-elements are lines
                    for mbLine in mb.geo_list:
                        # mbLine.setMeshLength()
                        mb_ids += f"{mbLine.id},"  # add the line id
            if mb_ids:
                r_stator_mb = stator.movingBandRadius
                # create movingband line id list, because its cleaner
                mesh_code += f"MB_LinesS = {{{mb_ids[0:-1]}}};\n"
                mesh_code += (
                    "MeshSize{ PointsOf{Line{MB_LinesS[]};}} = 2*Pi*"
                    + str(r_stator_mb)
                    + "/NbrMbSegments;\n\n"
                )  # set the mesh size for all movingband points
            mesh_code += (
                "Mesh.SurfaceFaces = 0; // don't show mesh faces (only edges)\n\n"
            )
        return mesh_code

    def write_geo(self, UD_MeshCode: str = "") -> None:
        """writeGeo generates the .geo-File for the current script.

        Args:
            UD_MeshCode (str): User defined code to modify mesh settings. This
                will be printed *before* the internal mesh settings because
                otherwise Movingband-Mesh could be overwritten. Must be conformal
                with the gmsh syntax!
        """
        logger = logging.getLogger(__name__)
        # add the code for the mesh settings and mesh modification
        init_mesh_code = 'INPUT_MESH = "Input/04Mesh/";\n'
        init_mesh_code += (
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
        init_mesh_code += (
            "\tFlag_individualColoring = {0,"
            + 'Name StrCat[INPUT_MESH, "09Individual Mesh Coloring"], '
            + "Choices {0, 1}}\n];\n"
        )
        init_mesh_code += "Mesh.MeshSizeFactor = gmsf;\n"
        # show mesh Lines without lighting
        init_mesh_code += (
            "Mesh.SurfaceEdges = 1;\nMesh.Light = 0;\nMesh.SurfaceFaces = 1;\n"
        )
        init_mesh_code += "Mesh.Algorithm = 6; // Frontal-Delaunay for 2D meshes\n"
        # TODO: This can be removed with a new GetDP version according to:
        # https://gitlab.onelab.info/gmsh/gmsh/-/issues/3194
        init_mesh_code += "Mesh.MshFileVersion = 4.0; // Fix bug in mesh file creation for GetDP Version 3.6.0\n"
        init_mesh_code += "\n"

        mesh_code = ""
        movingGeoCode = ""
        if self.machine:
            mesh_code = self._create_mesh_code()
            # add the code for plotting the moving boundary in post processing
            movingGeoCode = self._create_moving_code()

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

        geo_unrolled_path = self.geo_file_path + "_unrolled"
        gmsh.write(geo_unrolled_path)
        # read in the file content
        with open(geo_unrolled_path, "r+") as fd:
            geo_code = fd.readlines()
            # contents.insert(0, new_string)  # new_string should end in a newline
            fd.seek(0)  # readlines consumes the iterator, so we need to start over
            # fd.writelines(contents)  # No need to truncate as we are increasing
        os.remove(geo_unrolled_path)

        with open(self.geo_file_path, "w", encoding="utf-8") as geo_file:
            geo_file.write(versionStr)  # write the pyemmo version number
            # create Expert Mode Flag
            geo_file.write(
                """DefineConstant[\n Flag_ExpertMode = {1,"""
                + """Name '01View/Expert Mode', Choices {0, 1}}\n];\n\n"""
            )
            geo_file.write(init_mesh_code)  # write code for mesh variables
            geo_file.writelines(geo_code)
            if self.color_code:
                # TODO: Update to create color code from physical elements,
                # because the colors set by the gmsh api are not exported to
                # the geo_unrolled file.
                geo_file.write(
                    "\n// Color code\n"
                    + """If (!Flag_individualColoring)\n"""
                    + self.color_code
                    + """EndIf\n"""
                )
            geo_file.write(UD_MeshCode)
            geo_file.write(mesh_code)
            # write code to only show physicals
            geo_file.write(
                "Hide {:}\nRecursive Show { Physical Surface{:}; }\n"
                "Recursive Show { Physical Curve{:}; }\n"
                "Geometry.PointSize = 3.0;\n\n"
            )
            geo_file.write(movingGeoCode)
        # set flag that geometry files have been created to true
        self._geo_files_created = True

    def _setParameters(self):
        """
        Set the machine parameters for the script to the ``Script.simParams``attribute.
        """
        logger = logging.getLogger(__name__)
        machine = self.machine
        if not machine:
            raise RuntimeError("There was no machine specified. Add machine to script.")
        simu_param_dict = self.sim_params
        # 1. Set geometrical parameters via "machine.getSimParams()"
        #   SYMMETRY_FACTOR, L_AX_R, L_AX_S, NBR_POLE_PAIRS, NBR_TURNS_IN_FACE
        geo_params = machine.getSimParams()
        # TODO: Improve check here...
        # assert len(geometryParams) == len(simuParamDict.GEO) # assert there
        # is the correct number of parameters

        # update machine parameters:
        simu_param_dict["GEO"] = {**simu_param_dict["GEO"], **geo_params}

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
                simu_param_dict["GEO"][f"R_{side.upper()}_AIRGAP"] = mean(airgap_radii)

        # 2. Set simulation parameters
        #   INIT_ROTOR_POS  -> Allready set in __init__
        #   ANGLE_INCREMENT -> Allready set in __init__
        #   FINAL_ROTOR_POS -> Allready set in __init__
        #   SPEED_RPM       -> Allready set in __init__
        #   ParkAngOffset   -> Allready set in __init__
        #   FLAG_NL
        #   FLAG_CHANGE_ROT_DIR
        flag_CalcNL = 0
        has_magnets = False
        # flag_readonly = 0
        for domain in machine.domains:
            for physical in domain.physicals:
                if physical.geoElementType == Surface:
                    mat = physical.material
                    if not mat.linear:
                        flag_CalcNL = 1
                        break  # if one BH curve is found, we can stop the loop
                    if isinstance(physical, Magnet):
                        has_magnets = True
        simu_param_dict["SYM"]["FLAG_NL"] = flag_CalcNL
        if not has_magnets and simu_param_dict["SYM"]["CALC_MAGNET_LOSSES"] == 1:
            # if there where no magnet physical elements, set flag to false
            # even if its set to true...
            logger.warning(
                "Unsetting the flag 'CALC_MAGNET_LOSSES', because"
                " no magnets where found in the machine."
            )
            simu_param_dict["SYM"]["CALC_MAGNET_LOSSES"] = 0

        # machine.getStator().winding.plot_star('plot_star.png',None,False,True)
        if machine.stator.winding.get_windingfactor_el()[1][0, 0] < 0:
            # The fundamental windingfactor sign indicates the rotation
            # dirction of the field wave. If its negative, the field rotates
            # mathematically negative (CW) and the rotation dirction should be
            # inverted. The funamental winding factor allways refers to the
            # mechanical order which is equal to the number of pole pairs. (So
            # this is also true for non-fundamental winding configurations)
            simu_param_dict["SYM"]["FLAG_CHANGE_ROT_DIR"] = 1
        else:
            # Otherwise the rotation direction is ok.
            simu_param_dict["SYM"]["FLAG_CHANGE_ROT_DIR"] = 0

        # if the Park-transformation angle is not set manually, try to
        # calculate it
        if simu_param_dict["SYM"]["ParkAngOffset"] is None:
            nbr_pole_pairs = default_param_dict["GEO"]["NBR_POLE_PAIRS"]
            nbr_slots = default_param_dict["GEO"]["NBR_SLOTS"]
            slot_pitch = 2 * pi / nbr_slots
            mmf_order, _, angle = machine.stator.winding.get_MMF_harmonics()
            ## DEBUGGING:
            if logger.level <= logging.DEBUG:
                if not os.path.exists(self.results_path):
                    os.mkdir(self.results_path)
                machine.stator.winding.save_to_file(
                    os.path.join(self.results_path, f"winding_{self.name}.wdg")
                )

            # Stator angle for I_U = 1 p.u., I_V = -1/2, I_W = -1/2 in rad elec
            try:
                # get index of fundamental MMF electrical order
                elec_order_index = where(mmf_order == nbr_pole_pairs)
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
                    dq_offset = 0
                else:
                    dq_offset = (
                        -rad2deg(slot_pitch / 2 * nbr_pole_pairs)
                        + rad2deg(system_offset)
                        + 270
                    )
            else:
                dq_offset = 0
            simu_param_dict["SYM"]["ParkAngOffset"] = dq_offset

    def _getParamCode(self, param_name: str, param_value) -> str:
        """
        Get a line of parameter code:

        .. code-block:: python

            paramCode = f"{paramName} = {paramValue}
        """
        if isinstance(param_value, (str)):
            param_code = f'{param_name} = "{param_value}";\n'  # add "" for string value
        else:  # isinstance(paramValue,(int, float)):
            param_code = f"{param_name} = {param_value};\n"
        return param_code

    def _create_param_code(self) -> str:
        """Create the string code for the parameter file"""
        self._setParameters()  # set Parameters to write code
        param_code: str = "// MACHINE SPECIFIC VALUES\n"
        for paramName, paramValue in self.sim_params["GEO"].items():
            param_code += self._getParamCode(paramName, paramValue)
        param_code += "// SIMULATION SPECIFIC VALUES\n"
        for paramName, paramValue in self.sim_params["SYM"].items():
            param_code += self._getParamCode(paramName, paramValue)
        param_code += "// MATERIAL SPECIFIC VALUES\n"
        for paramName, paramValue in self.sim_params["MAT"].items():
            param_code += self._getParamCode(paramName, paramValue)
        return param_code

    def write_pro(self):
        """
        generate pro files.
        The main steps are:

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
        template_file = abspath(join(MAIN_DIR, "script", "machine_template.pro"))
        # script file name
        param_file_name = self.name + "_param.geo"
        param_file = abspath(join(self.script_path, param_file_name))

        # write file content to new file
        with open(param_file, "w", encoding="utf-8") as file:
            # also add versionStr to identify pyemmo version
            file.write(versionStr)
            # get the geometrical and simulation parameters:
            file.write(self._create_param_code())

        # 2. copy machine file
        with open(template_file, encoding="utf-8") as temp_file:
            machine_file_code = (
                versionStr + temp_file.read()
            )  # open and read machine template file

        # 3. append group code to machine file
        #   3.1 import parameter file
        # replace the place holder "PARAMETER_FILE" with the actual parameter
        # file name
        machine_file_code = machine_file_code.replace(
            "PARAMETER_FILE", '"' + param_file_name + '"', 1
        )
        #   3.2 add groups and material groups
        #       generate material code in _functionMaterial to account for
        #       material groups
        self._create_material_code()
        #       replace the place holder "GROUP_CODE" with actual group code
        machine_file_code = machine_file_code.replace("GROUP_CODE", self.group.code, 1)

        #  3.3 function code
        machine_file_code = machine_file_code.replace(
            "FUNCTION_CODE",
            self.function_material.code + self.function_magnetization.code,
            1,
        )

        # 4. copy the magstatdyn file
        # filename of the motor model template of getdp
        magstadyn_file_name = "machine_magstadyn_a.pro"
        # filepath to the template calculation file for motor models
        magstadyn_temp_file = join(MAIN_DIR, "script", magstadyn_file_name).replace(
            "\\", "/"
        )
        # read the template file
        with open(magstadyn_temp_file, encoding="utf-8") as calc_file:
            calcCode = versionStr + calc_file.read()
        # filepath to the destination of the calculation file
        magstadyn_dest_file = join(self.script_path, magstadyn_file_name).replace(
            "\\", "/"
        )
        # write the magstadyn file to new destination
        with open(magstadyn_dest_file, "w", encoding="utf-8") as magstadyn_file:
            magstadyn_file.write(calcCode)

        ## COPY CIRCUIT FILE
        shutil.copy(
            join(MAIN_DIR, "script", "Circuit_SC_ASM.pro"),
            join(self.script_path, "Circuit_SC_ASM.pro"),
        )

        #  6.1 add the PostOperation command code before including the
        # magstatdyn-file
        if self.post_operation.items:  # if there are Items in PostOperation
            # add the code for the compute command including the postoperations
            # TODO: Add option for "-bin" case (user setting)
            # TODO: adapt output verbosity based on internal verbosity

            compute_code = (
                "DefineConstant[\n\t"
                """R_ = {"Analysis", Name "GetDP/1ResolutionChoices", Visible Flag_Debug || Flag_ExpertMode},\n\t"""
                """C_ = {"-solve -v 3 -v2 -pos", Name "GetDP/9ComputeCommand", Visible Flag_Debug || Flag_ExpertMode}\n\t"""
                """P_ = {\""""
                + ",".join(self.get_post_operation_names())
                + """", Name "GetDP/2PostOperationChoices", Visible Flag_Debug || Flag_ExpertMode}\n"""
                "];\n"
            )
            machine_file_code += compute_code

        #   5. import magstatdyn file in machine file
        # # replace the placeholder in the machine script
        # machineFileCode = machineFileCode.replace(
        #     "DEFAULT_PRO_FILE", '"' + calculationFileName + '"', 1
        # )
        # had to replace placeholder method here to add the postoperation
        # command before
        machine_file_code += f'Include "{magstadyn_file_name}"\n'

        # 6.2 add the PostOperation code
        if self.post_operation.items:  # if there are Items in PostOperation
            machine_file_code += self.post_operation.code

        pro_file_path = join(self.script_path, self.name + ".pro")
        with open(pro_file_path, "w", encoding="utf-8") as proScript:
            proScript.write(machine_file_code)

        # If logging is set to debug, save the winding to a file
        if logger.getEffectiveLevel() <= logging.DEBUG:
            if not os.path.exists(self.script_path):
                os.mkdir(self.script_path)
            self.machine.stator.winding.save_to_file(
                os.path.join(self.script_path, f"winding_{self.name}.wdg")
            )
        self._pro_files_created = True

    def generate(self, mode: int = 0, UD_MeshCode: str = ""):
        """
        generate .geo- and .pro files

        Args:
            mode (int): Decide which scripts to generate

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
            self.write_geo(UD_MeshCode=UD_MeshCode)
            self.write_pro()

        elif mode == 1:
            self.write_geo(UD_MeshCode=UD_MeshCode)
        elif mode == 2:
            self.write_pro()
