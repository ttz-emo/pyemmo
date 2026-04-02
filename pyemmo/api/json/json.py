#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied
# Sciences Wuerzburg-Schweinfurt.
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
"""This is the main module of the json api to create a machine model in Onelab."""

# import debugpy
# debugpy.debug_this_thread()
from __future__ import annotations

# import re
import datetime
import json
import logging
import os
import subprocess
import timeit
from os import makedirs
from os.path import isdir, isfile, join
from pprint import pformat

import gmsh as gmsh_api
import numpy as np
from matplotlib import pyplot as plt

from ... import log_formatter
from ...functions import clean_name, core_loss, import_results, plot, run_onelab
from ...script.gmsh.utils import fix_missing_mesh_sizes
from ...script.machine import Machine
from ...script.material.electricalSteel import ElectricalSteel
from ...script.rotor import Rotor
from ...script.script import Script
from ...script.stator import Stator
from ..machine_segment_surface import MachineSegmentSurface
from . import ROTOR_AIRGAP_IDEXT, STATOR_AIRGAP_IDEXT, api_name_dict
from . import boundaryJSON as boundary
from . import default_info_dict, importJSON, modelJSON
from .create_airgaps import create_airgap_surfaces

# from swat_em import analyse
# from .. import calcPhaseangleStarvoltageCorr

# analyse.calc_phaseangle_starvoltage = calcPhaseangleStarvoltageCorr
pyemmoLogger = logging.getLogger("pyemmo")


def createMachine(
    segmentSurfDict: dict[str, MachineSegmentSurface], extendedInfo: dict
) -> tuple[Machine, dict[str, list[MachineSegmentSurface]]]:
    """create a pyemmo Machine object from a list of surfaces forming one machine segment
    (imported from matlab).

    Args:
        segmentSurfDict (Dict[str, MachineSegmentSurface]): dict of surfaces forming one machine segment
            (on stator and rotor side). Segment width for rotor and stator can be different.
            Dict keys are IdExt of MachineSegmentSurface.
        extendedInfo (dict): Dict with additional information like pole pair number and axial
            length.

    Returns:
        Tuple[Machine, Dict[str, List[MachineSegmentSurface]]]: Resulting machine object and Machine
        surface dict with IdExt as keys and list of MachineSegmentSurface objects as items.
    """
    symFactor = importJSON.get_sym_factor(extendedInfo)
    rotorMovingBandRadius = importJSON.get_MB_radius(extendedInfo)

    logger = logging.getLogger(__name__)
    logger.debug("Calling modelJSON.createMachineGeometryFromSegment...")
    # create the remaining machine surfaces
    maschineSurfDict = modelJSON.createMachineGeometryFromSegment(
        segmentSurfDict, symFactor
    )
    logger.debug("Calling gmsh.model.occ.remove_all_duplicates()")
    gmsh_api.model.occ.remove_all_duplicates()
    # TODO: Test this for complex geometry
    # gmsh_api.logger.start()
    # try:
    #     gmsh_api.model.occ.remove_all_duplicates()
    # finally:
    #     log_catch = gmsh_api.logger.get()
    #     gmsh_api.logger.stop()
    # # update gmsh surface tags afer remove duplicates
    # # pattern = re.compile(r'Info: Cannot bind existing OpenCASCADE surface (\d+) to second tag (\d+)')
    # for line in log_catch:
    #     match = re.match(
    #         r"Info: Cannot bind existing OpenCASCADE surface (\d+) to second tag (\d+)",
    #         line,
    #     )
    #     if match:
    #         # Extract and convert the matched numbers
    #         new_tag, old_tag = map(int, match.groups())
    #         for _, surf_list in maschineSurfDict.items():
    #             for surf in surf_list:
    #                 if surf.id == old_tag:
    #                     surf._id = new_tag

    logger.debug("Calling gmsh.model.occ.synchronize()")
    gmsh_api.model.occ.synchronize()

    # call function create_airgap if any airgap surface is missing
    if (
        STATOR_AIRGAP_IDEXT not in maschineSurfDict
        or ROTOR_AIRGAP_IDEXT not in maschineSurfDict
    ):
        logger.debug(
            "Missing rotor or stator airgap from surface dict! "
            "Starting airgap creation"
        )
        create_airgap_surfaces(maschineSurfDict, rotorMovingBandRadius, symFactor)
    else:
        logger.debug(
            "Found rotor and stator airgap in surface dict! "
            "Not calling airgap creation."
        )

    # check mesh sizes after import! Due to issues with OCC it can happen that points
    # lose their mesh size and get mesh size = 0. In this case, search for the closest
    # point and set the mesh size to its mesh size.
    logger.info(
        "Fixing mesh size for points without mesh size by searching for closest point "
        "and resetting to its mesh size."
    )
    fix_missing_mesh_sizes()

    logger.info("Identifying boundary curves...")
    rotorPhysicals, statorPhysicals = boundary.get_boundaries(
        maschineSurfDict, symFactor, rotorMovingBandRadius
    )

    # create winding
    windingSWAT = modelJSON.createWinding(extendedInfo, maschineSurfDict)
    # Log winding layout for debugging *before* createSlot() is called.
    logger.debug("Winding: %s", windingSWAT)
    logger.debug("Winding layout: %s", windingSWAT.get_phases())

    # create physical elements from the surfaces
    logger.info("Creating physicals from geometry...")
    for idExt, surfList in maschineSurfDict.items():
        surfName = surfList[0].name
        if "GehInnen" in surfName and symFactor == 1:
            logger.warning(
                "Found surface %s with identifier 'GehInnen' and symmetry factor = 1."
                "Removing this tool-surface for correct housing creation",
                surfName,
            )
            # if the inner surface is air, overlapping the rotor, set the delete-flag to not create
            # the inner housing surface
            for surf in surfList:
                logger.warning("Removing surface %s with id %i", surf.name, surf.id)
                gmsh_api.model.removeEntities([(2, surf.id)])
        else:
            logger.debug("Creating physical element for %s", idExt)
            physSurfList, machineSide = modelJSON.createPhysicalSurfaces(
                part_id=idExt,
                surfList=surfList,
                rotorMBRadius=rotorMovingBandRadius,
                extendedInfo=extendedInfo,
            )
            if machineSide == "Stator":
                statorPhysicals.extend(physSurfList)
            elif machineSide == "Rotor":
                rotorPhysicals.extend(physSurfList)
            else:
                raise ValueError(
                    f"MachineSide was whether rotor or stator: {machineSide}",
                )
    if logger.getEffectiveLevel() <= logging.DEBUG - 1:
        gmsh_api.model.occ.synchronize()
        if extendedInfo["flag_openGUI"]:  # only open GUI if specified
            gmsh_api.model.setVisibility(gmsh_api.model.getEntities(), False)
            gmsh_api.model.setVisibility(gmsh_api.model.getEntities(2), True, True)
            gmsh_api.fltk.run()

    # create the rotor
    axLen = importJSON.get_axial_length(extendedInfo)
    logger.debug("Axial length of model is %.3f m", axLen["rotor"])

    logger.info("Creating rotor object...")
    rotorAPI = Rotor(
        name="rotor created via json api",
        physicals=rotorPhysicals,
        axLen=axLen["rotor"],
    )

    # create the stator
    logger.info("Creating stator object...")
    statorAPI = Stator(
        name="stator created via json api",
        nbr_slots=windingSWAT.get_num_slots(),
        physicals=statorPhysicals,
        axLen=axLen["stator"],
        winding=windingSWAT,
    )

    # create the machine object
    nbrPolePair = importJSON.get_nbr_of_pole_pairs(extendedInfo)
    modelName = importJSON.get_model_name(extendedInfo)

    logger.info("Creating Machine object for model %s...", modelName)
    machineSiemens = Machine(
        rotor=rotorAPI,
        stator=statorAPI,
        name=f"Machine from json interface ({modelName})",
        nbrPolePairs=nbrPolePair,
        symmetryFactor=symFactor,
    )
    # TODO: Add algorithm to remove all unused gmsh instances (aka ones that do not
    # belong to any Physical Line or Surface)
    return machineSiemens, maschineSurfDict


def createMeshSizeGUICode(machineSurfDict: dict[str, list[MachineSegmentSurface]]):
    """
    Create the gmsh fomatted code to set the mesh size of the machine surfaces via the GUI.

    The names of the sufaces are defined in the `apiNameDict` (defined globally in
    pyemmo.api.init), which links the IdExt value of a MachineSegmentSurface object to a real name in the
    GUI. The order of the IdExt in that dict matters since it defines which mesh size the
    intersection points between two surfaces should get.

    For example: If the rotor airgap IdExt comes after the rotor lammination IdExt, the points at
    the intersection line will get the mesh size of the airgap.

    The order is:

    - Rotor:
        * Miscellaneous
        * Shaft
        * Sleeve
        * Hole pole gap
        * Magnet
        * Slot
        * Lamination
        * Airgap
    - Stator:
        * Miscellaneous
        * Housing
        * Slot
        * Slot opening
        * Lamination
        * Airgap

    If the surface has no surface mesh size, the mean mesh size of the points of that surface will
    be used.

    Args:
        machineSurfDict (Dict[str, List[MachineSegmentSurface]]): dictionary with IdExt as keys.
    """
    mscDefConst = (
        "\nDefineConstant[\n\tmm = 1e-3,\n"
        + """\tFlag_SpecifyMeshSize = {0, """
        + """Name StrCat[INPUT_MESH, "04User defined surface mesh sizes"],"""
        + "Choices {0, 1}}\n];\n"
        + "If(Flag_SpecifyMeshSize)\n"
        + "\tDefineConstant[\n"
    )
    mscSetSize = ""

    # Create a new surface dict with the arbitrary part_ids at the beginning and ending
    # with the predefined parts defined in api_name_dict.
    machine_dict_keys = list(machineSurfDict.keys())  # extract dict keys as list
    # create separate dict to handle indexed part_ids with single part_id
    surf_dict: dict[str, list[MachineSegmentSurface]] = {}
    # first handle the known part_ids
    for part_id in api_name_dict:
        if part_id in machine_dict_keys:
            # if part_id in machine_dict_keys as it is, add it to surf dict
            surf_dict[part_id] = machineSurfDict[part_id]
            machine_dict_keys.remove(part_id)
        elif any(part_id in key for key in machine_dict_keys):
            # collect all parts that have indices (eg. slots or magnets) separately
            # and combine them in single surface list.
            surf_dict[part_id] = []  # init surface list
            # use copy here for loop with `remove` call in loop. Otherwise elements in
            # loop are skipped!
            for key in machine_dict_keys.copy():
                # loop through remaining keys and search for current part_id.
                if part_id in key:
                    # if part_id is part of key (eg. 'stator slot' in 'stator slot1')
                    surf_dict[part_id].extend(machineSurfDict[key])
                    machine_dict_keys.remove(key)
    # insert remaining surface names at the beginning of the dict
    for key in machine_dict_keys:
        surf_dict = {key: machineSurfDict[key]} | surf_dict
    for i, (part_id, surf_list) in enumerate(surf_dict.items()):
        # create mesh code in correct order since surf_dict is ordered correctly.
        # get the mesh size
        mesh_size = np.mean([surf.meanMeshLength for surf in surf_list])
        # if mesh size in MachineSegmentSurface was 0, get the mean mesh size of the points
        if not mesh_size:
            mesh_size = surf_list[0].meanMeshLength
        mesh_size = round(mesh_size * 1e3, 3)  # convert to mm for easier use in UI
        # try to get the real name from the api_name_dict, otherwise use part_id itself
        surfName = api_name_dict.get(part_id, part_id)
        # create the mesh size parameter name
        param_name = clean_name.clean_name(part_id) + "_msf"
        mscDefConst += (
            f"""\t\t{param_name} = {{{mesh_size},"""
            + f""" Name StrCat[INPUT_MESH, "05Mesh Size/{i:02d}{surfName} [mm]"],"""
            + f"""Min {mesh_size/10}, Max {mesh_size * 10}, Step 0.1,"""
            + "Visible Flag_SpecifyMeshSize},\n"
        )
        surfIds = [str(surf.id) for surf in surf_list]
        mscSetSize += (
            f"\tMeshSize {{ PointsOf {{Surface{{ {','.join(surfIds)} }};}} }} = "
            f"{param_name}*mm;\n"
        )
    # At the end remove last comma and close bracket
    if mscDefConst[-2] == ",":
        mscDefConst = mscDefConst[0 : len(mscDefConst) - 2] + "\n\t];\n"
    # close if statement
    mscSetSize += "EndIf\n"
    return mscDefConst + mscSetSize


def addPostOperations(script: Script, extendedInfo: dict) -> None:
    """adding user defined post operation to machine.pro file.
    Right now adding the PostOperation "GetBOnRadius" to get the B field (B_rad, B_tan) on
    different radii evaluated by OnGrid PO-type.

    Args:
        script (Script): Actual Script object to add PostOperation.
        extendedInfo (dict): Extended info dict to get the different radii.
    """
    logger = logging.getLogger(__name__)
    logger.debug(
        "Adding api specific post operation GetBOnRadius to get the B field "
        "(B_rad, B_tan) on different radii evaluated by OnGrid"
    )
    machine = script.machine
    # 1. Airgap flux density
    rotorAirgapRadius = machine.rotor.movingband_radius
    statorAirgapRadius = machine.stator.movingband[0].radius
    for side, radius in {
        "rotor": rotorAirgapRadius,
        "stator": statorAirgapRadius,
    }.items():
        logger.debug("Adding PO for %s airgap at raidus %.3f mm", side, radius * 1e3)
        for quantity in ["b_radial", "b_tangent"]:
            sign = "-" if side == "rotor" else "+"
            resFilePath = join("CAT_RESDIR", quantity + "_airgap_" + side + ".pos")
            # resFilePath = abspath(
            #     join(script.getResultsPath(), quantity + "_airgap_" + side + ".pos")
            # )
            script.add_post_operation(
                quantity_name=quantity,
                post_operation="GetBOnRadius",
                OnGrid=(
                    f"{{({radius}*(1{sign}0.0001))*Cos[$A*Pi/180],"
                    f"({radius}*(1{sign}0.0001))*Sin[$A*Pi/180],0}}"
                    "{0:360/SymmetryFactor:360/NbrMbSegments*GlobalMeshsizeFactor,0,0}"
                ),
                File=resFilePath,
                Name=f'"{quantity} (airgap {side})"',
            )

    # 2. Tooth Flux density
    if "r_z" in extendedInfo.keys():
        toothRadius = extendedInfo["r_z"]
        logger.debug("Adding PO for tooth at raidus %.3f mm", toothRadius)
        for quantity in ["b_radial", "b_tangent"]:
            script.add_post_operation(
                quantity,
                "GetBOnRadius",
                OnGrid=(
                    f"{{{toothRadius}*Cos[$A*Pi/180],"
                    f"{toothRadius}*Sin[$A*Pi/180],0}}"
                    "{0:360/SymmetryFactor:0.5,0,0}"
                ),
                File=join("CAT_RESDIR", quantity + "_tooth.pos"),
                Name=f'"{quantity} (Tooth)"',
            )

    # 3. Yoke Flux density
    if "r_j" in extendedInfo.keys():
        yokeRadius = extendedInfo["r_j"]
        logger.debug("Adding PO for yoke at raidus %.3f mm", yokeRadius)

        for quantity in ["b_radial", "b_tangent"]:
            script.add_post_operation(
                quantity,
                "GetBOnRadius",
                OnGrid=(
                    f"{{{yokeRadius}*Cos[$A*Pi/180],"
                    f"{yokeRadius}*Sin[$A*Pi/180],0}}"
                    "{0:360/SymmetryFactor:0.5,0,0}"
                ),
                File=join("CAT_RESDIR", quantity + "_yoke.pos"),
                Name=f'"{quantity} (Yoke)"',
            )

    ## 4. Add rotor and stator b-field export for iron loss calculation
    if importJSON.get_flag_core_loss_calc(extendedInfo):
        logger.debug("Adding post operation 'GetBIron' for core loss calculation...")

        rotorIronPhysicalID = [
            str(phys.id) for phys in machine.rotor._domainLam.physicals
        ]
        statorIronPhysicalID = [
            str(phys.id) for phys in machine.stator._domainLam.physicals
        ]
        script.add_post_operation(
            "b",
            "GetBIron",
            OnElementsOf=f"Region[{{{','.join(rotorIronPhysicalID)}}}]",
            File=join("CAT_RESDIR", "b_rotor.pos"),
            Name='"b (rotor)"',
        )
        script.add_post_operation(
            "b",
            "GetBIron",
            OnElementsOf=f"Region[{{{','.join(statorIronPhysicalID)}}}]",
            File=join("CAT_RESDIR", "b_stator.pos"),
            Name='"b (stator)"',
        )

    # 5. PM Eddy current loss
    if machine._domainM.physicals:
        logger.debug("Adding post operation 'GetMagnetLosses'...")
        # if there are magnets
        allMagConducting = True
        for magnet in machine._domainM.physicals:
            if magnet.material.conductivity is None:
                allMagConducting = False
                logger.warning(
                    "Unable to calculate magnet losses, due to missing el. conductivity "
                    "in %s. Skip magnet loss calculation!",
                    magnet.name,
                )
                break
        if allMagConducting:
            script.add_post_operation(
                "JouleLosses[Rotor_Magnets]",
                "GetMagnetLosses",
                OnGlobal="",
                Format="TimeTable",
                File=join("CAT_RESDIR", "Pv_eddy_Mag.dat"),
                # Name='"p (stator)"',
            )
            script.sim_params["SYM"]["CALC_MAGNET_LOSSES"] = 1


# ======================================== START MAIN FUNCTION =====================================


def main(
    geo: str | dict[str, MachineSegmentSurface],
    extInfo: str | dict,
    model: str | os.PathLike,
    gmsh: str | os.PathLike = "",
    getdp: str | os.PathLike = "",
    results: str | os.PathLike = "",
) -> Script:
    """The main function reads the JSON files (if given) and creates the .geo
    and .pro scripts for a onelab simulation.

    Program sequence:
        1. Check that both json files are given and gmsh is installed. Import
            the geo segments and the additional machine information.
        2. Create a pyemmo Machine-object by rotating and duplicating the given
            surface segments with
            :func:`createMachine() <pyemmo.api.json.createMachine>`
        3. Create a pyemmo Script-object with the Machine and the simulation
            parameters.
        4. Add additional code for the API specific B-field PostOperation (on
            line evaluation) and the surface mesh size setting via the GUI.
        5. Create the .geo and .pro script files by calling
            :meth:`Script.generateScript() <pyemmo.script.script.Script.generateScript>`
        6. Create command line call for gmsh/getdp with
            :func:`~pyemmo.functions.run_onelab.create_command`
            and start with :code:`subprocess.run`


    Args:
        geo (str or dict): File path to JSON formatted geometry file OR segment
            surface dict with IdExt as keys and MachineSegmentSurface objects as values.
        extInfo (str or dict): File path to JSON formatted extended information
            file or directly given info dict. See
            :ref:`Model Properties <section-pyemmo.api.json-param>`
            section in doc for parameters description.
        model (str): Folder path where the resulting model files should be
            placed.
        gmsh (str, optional): Gmsh executable path. If nothing is provided the
            executable will be searched.
        getdp (str, optional): GetDP executable path. Defaults to "".
        results (str, optional): Folder path to store the simulation results.
            Defaults to "modelDir/res_ModelName"
    """
    module_logger = logging.getLogger(__name__)
    if module_logger.getEffectiveLevel() <= logging.DEBUG:
        t0 = timeit.default_timer()
    # create dir for model files if it doesn't exist
    makedirs(model, exist_ok=True)
    # Set logging path to model dir
    jsonLogFileHandler = logging.FileHandler(
        filename=os.path.join(model, "pyemmo_jsonAPI.log"),
        mode="w",  # create new file each time the api is run
        encoding="utf-8",
    )
    jsonLogFileHandler.setLevel(
        min(
            pyemmoLogger.getEffectiveLevel(),
            module_logger.getEffectiveLevel(),
            logging.INFO,
        )
    )
    jsonLogFileHandler.setFormatter(log_formatter)
    pyemmoLogger.addHandler(jsonLogFileHandler)
    module_logger.info(
        "PyEMMO API started on %s %s",
        datetime.date.today(),
        datetime.datetime.now().strftime("%H:%M:%S"),
    )

    # addition information
    if isinstance(extInfo, str):
        if isfile(extInfo):
            # import the extended information
            module_logger.debug("Loading model information from file %s", extInfo)
            extendedInfo = importJSON.load_info_dict(extInfo)
        else:
            raise (FileNotFoundError(f"Given file path {extInfo} was not a file."))
    elif isinstance(extInfo, dict):
        extendedInfo = extInfo
    else:
        raise TypeError(
            f"Model information file has to be type 'File' or 'dict', not {type(extInfo)}"
        )
    module_logger.debug(
        "Model and simulation parameters from info dict: %s",
        pformat(extendedInfo, indent=4),
    )
    # make sure extendedInfo contains all relevant infos by merging with default dict.
    # second dict is prioritized!
    extendedInfo = {**default_info_dict, **extendedInfo}
    # TODO: Update default simulation parameters if they are matching the default values

    # get geometry
    if isinstance(geo, str):
        if isfile(geo):
            # gmsh_api.logger.start()
            # supress output of log messages to console.
            # See https://gitlab.onelab.info/gmsh/gmsh/-/issues/1901
            # Use gmsh.logger.start(), gmsh.logger.get(), gmsh.logger.stop() to catch logs.
            module_logger.debug("Setting gmsh option General.Terminal to 0.")
            gmsh_api.option.setNumber("General.Terminal", 0)
            # add new gmsh model in case api is called multiple times:
            gmsh_api.model.add(extendedInfo["modelName"])
            # import the segment surface list from the json file:
            try:
                with open(geo, encoding="utf-8") as jsonFile:
                    module_logger.debug("Loading geometry data from file %s", geo)
                    machineGeoList = json.load(jsonFile)
                    # create dict with surface api (segment) objects from the surface list
                    segmentSurfDict = modelJSON.importMachineGeometry(machineGeoList)
            except FileNotFoundError as fnfe:
                raise fnfe
            except Exception as exept:
                raise exept
        else:
            raise FileNotFoundError(f"Given file path {geo} was not a file.")
    elif isinstance(geo, dict):
        module_logger.debug("Checking given surface types for 'MachineSegmentSurface'")
        # Make sure all given surfaces have the correct type:
        if not all(type(surf) == MachineSegmentSurface for surf in geo.values()):
            raise TypeError(
                "Invalid geometry dict provided! "
                "Make sure that the geometry values are of type MachineSegmentSurface!"
            )
        # TODO: I think this can be skipped now!
        module_logger.debug(
            "Assert that the given surfaces are created in the current gmsh model"
        )
        module_logger.debug("Current gmsh model is: %s", gmsh_api.model.getCurrent())
        gmsh_api.model.occ.synchronize()
        surf_dim_tags = gmsh_api.model.get_entities(2)
        surf_tags = [dim_tag[1] for dim_tag in surf_dim_tags]
        for surf in geo.values():
            if surf.id not in surf_tags:
                raise RuntimeError(
                    f"Segment surface {surf.name} with ID {surf.id} not in current gmsh model!"
                )
        segmentSurfDict = geo
    else:
        raise TypeError(
            f"Geometry file has to be type 'File' or 'dict', not {type(geo)}"
        )
    # check if the symmetry factor from the segment surf dict matches the externally
    # given symmetry factor in extendedInfo:
    _check_symmetry(segmentSurfDict, extendedInfo)

    if module_logger.getEffectiveLevel() <= logging.DEBUG:
        # update gmsh fltk GUI config
        gmsh_api.option.setNumber("Geometry.Surfaces", 1)  # show surface indications
        gmsh_api.option.setNumber("Geometry.Light", 0)  # deactivate 3D light

        t1 = timeit.default_timer()
        module_logger.debug("Time for loading geometry: %.2fs", t1 - t0)

    # add plot of given geometry
    if module_logger.getEffectiveLevel() <= logging.DEBUG - 1:
        # show boundary line plot
        fig, ax = plt.subplots()
        surfs = [elem for _, elem in segmentSurfDict.items()]
        # get colors from colormap 'rainbow'
        colors = plt.cm.get_cmap("rainbow")(np.linspace(0, 1, len(surfs)), 1)
        # plot each boundary with own color
        for surf, color in zip(surfs, colors):
            plot.plot([surf], fig=fig, tag=False, color=color)
            if surf.tools:
                for tool in surf.tools:
                    plot.plot([tool], fig=fig, tag=False, color=color)
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_xlabel("x Axis")
        ax.set_ylabel("y Axis")
        ax.set_title("Model Geometry Input")
        fig.show()

    # generate the machine geometry
    module_logger.info("Creating complete model from segmented input...")
    machine, machineSurfDict = createMachine(segmentSurfDict, extendedInfo)

    if module_logger.getEffectiveLevel() <= logging.DEBUG:
        t2 = timeit.default_timer()
        module_logger.info("Time for creating machine object: %.2fs", t2 - t1)

    # set function mesh
    if "useFunctionMesh" in extendedInfo.keys():
        if extendedInfo["useFunctionMesh"]:
            module_logger.info("Creating automatic, function based mesh sizes...")
            machine.set_function_mesh()

    # get the simulation pareameters
    simulationParameters = importJSON.get_simulation_params(extendedInfo)
    module_logger.info("Generating the Script object in JSON API...")
    apiScript = Script(
        name=importJSON.get_model_name(extendedInfo),
        scriptPath=model,
        simuParams=simulationParameters,
        machine=machine,
        resultsPath=results,
    )

    if module_logger.getEffectiveLevel() <= logging.DEBUG:
        t3 = timeit.default_timer()
        module_logger.debug("Time for creating script object: %.2fs", t3 - t2)

    addPostOperations(apiScript, extendedInfo)

    module_logger.debug("Creating gmsh code for user defined mesh size setting...")
    meshSizeSetCode = createMeshSizeGUICode(machineSurfDict)

    # generate geo and pro files:
    module_logger.info("Creating Gmsh and GetDP input files...")
    apiScript.generate(UD_MeshCode=meshSizeSetCode)

    if module_logger.getEffectiveLevel() <= logging.DEBUG:
        t4 = timeit.default_timer()
        module_logger.debug("Time for generating script files: %.2fs", t4 - t3)

    if importJSON.get_flag_open_gui(extendedInfo) is True:
        module_logger.debug("Open Gmsh GUI to show model")
        _open_onelab(apiScript, extendedInfo, gmsh)

    pyemmoLogger.removeHandler(jsonLogFileHandler)
    jsonLogFileHandler.close()  # close log file handler!
    return apiScript


def _check_symmetry(
    segmentSurfDict: dict[str, MachineSegmentSurface], extendedInfo: dict
) -> bool:
    """Private function to check if the symmetry factor given in the extendedInfo is
    valid.

    Args:
        segmentSurfDict (dict[str, MachineSegmentSurface]): Dictionary with segment
            surfaces as values and their part ids as keys.
        extendedInfo (dict): Extended information dict with the symmetry factor.

    Raises:
        ValueError: If the symmetry factor is not compatible with the minimal symmetry
            of the machine.

    :meta private:
    """
    logger = logging.getLogger(__name__)
    logger.debug("Checking symmetry for given model...")
    # Check if the symmetry factor given from extendedInfo is valid:
    requested_sym = importJSON.get_sym_factor(extendedInfo)
    logger.debug("Given symmetry factor from extended info dict is %.1f", requested_sym)
    # get number of segments of the first surface to init symmetry check
    highest_sym = list(segmentSurfDict.values())[0].nbr_segments
    # get maximal symmetry for all segment surface:
    for seg_surf in segmentSurfDict.values():
        highest_sym = np.gcd(highest_sym, seg_surf.nbr_segments)
    logger.debug("Highest symmetry factor from current surfaces is %.1f", highest_sym)
    # symFactor must be a multiple of the highest symmetry (sym)
    if (highest_sym / requested_sym) % 1 != 0:
        raise ValueError(
            f"Given symmetry factor {requested_sym} is not compatible with the minimal symmetry {highest_sym}."
        )


def _open_onelab(apiScript: Script, extendedInfo: dict, gmsh: str = ""):
    """
    Private function to open ONELAB simulation in GUI and evaluate results

    :meta private:
    """
    logger = logging.getLogger(__name__)
    # check if gmsh was provided
    if not gmsh:
        # if gmsh was not provided, try to find it:
        logger.debug("Gmsh path not given. Trying to find Gmsh...")
        gmsh = run_onelab.find_gmsh()
    else:
        # if gmsh was given by the user, check that its valid
        if not isfile(gmsh):
            raise FileNotFoundError(f"Provided gmsh executable was not found: {gmsh}")
    command = run_onelab.create_command(
        file=apiScript.pro_file_path,
        gmsh_path=gmsh,
        useGUI=True,
    )
    logger.debug("Command for subprocess to start Gmsh is: '%s'", command)
    calcInfo = subprocess.run(command, capture_output=True, text=True, check=False)
    if calcInfo.stderr:
        for textLine in calcInfo.stderr.split("\n"):
            if "error" in textLine.lower():
                logger.error(
                    "Onelab call issued the following error: \n\t%s",
                    textLine.replace("\n", "\n\t"),
                )
            else:
                if textLine:  # if textline is not empty
                    logger.warning(
                        "Onelab call issued the following warning: \n\t%s",
                        textLine.replace("\n", "\n\t"),
                    )
    # Some other options to open the model in the Gmsh GUI without starting a subprocess
    # this works, but system is not recommended due to shell injection risk!
    # system("gmsh.exe " + apiScript.pro_file_path)

    # This also works, but runs in a client process through a socket. Only works
    # if ONELAB is downloaded from onelab.info and onelab.py file is available on
    # the system!
    # oc = onelab.client()
    # oc.run("gmsh", "gmsh", apiScript.pro_file_path)
    # oc.finalize()

    # You can start the simulation through the gmsh.onelab interface, but opening
    # the model (geo+pro) in the GUI did not work for me. If there is no mesh file,
    # the "Run" action results in an error. There must be some trick in the setup
    # when opening a pro file directly throught the GUI since the meshing is done
    # automatically then...
    # gmsh_api.onelab.run(
    #     "",
    #     f"gmsh.exe {apiScript.pro_file_path} -merge {apiScript.geo_file_path}",
    # )

    # core loss post processing:
    res_path = apiScript.results_path
    # check if resPath exists -> simulation has been run.
    if isdir(res_path):
        logger.debug("Found results path %s -> Simulation has been run.", res_path)
        # FIXME: This only works if "res_id" was not set in the GUI (no sub-res-folder).
        # check if the simulation that has been run is a single transient simulation:
        sim_is_transient = is_single_transient(res_path)
        if importJSON.get_flag_core_loss_calc(extendedInfo):
            if sim_is_transient:
                logger.info(
                    "Simulation found in results path was single transient simulation."
                    "Trying to run core loss calculation"
                )
                # if core loss flag and simulation is transient, calc core loss:
                _run_core_loss_calculation(res_path, apiScript)
            else:
                logger.warning(
                    "Iron loss calculation cannot be done for static or multi transient "
                    "simulation!"
                )
        # Plot Results for Debugging
        if logger.getEffectiveLevel() <= logging.DEBUG - 1:
            logger.info("Plotting all results for debugging!")
            # if the folder for results exists

            # avoid matplotlib debug infos
            import_results.plt.set_loglevel(level="info")

            for file in os.listdir(res_path):
                filename, fileExt = os.path.splitext(file)
                if fileExt == ".dat":
                    try:
                        import_results.plot_timetable_dat(
                            file_path=os.path.abspath(join(res_path, file)),
                            data_label=filename,
                            title=filename,
                            savefig=True,
                            showfig=False,
                            savepath=None,
                        )
                    except Exception as e:
                        logger.warning(
                            "Unable to plot file %s due to error: %s",
                            file,
                            e,
                        )


def _run_core_loss_calculation(resPath, apiScript: Script):
    """Private function to run core loss calculation in case of GUI api run.

    Args:
        resPath (str): Path to the results directory.
        apiScript (Script): Script object.

    :meta private:
    """
    logger = logging.getLogger(__name__)
    machine = apiScript.machine
    simulationParameters = apiScript.sim_params
    # FIXME: Implement better check for simulation status
    brFilePath = join(resPath, "b_rotor.pos")
    bsFilePath = join(resPath, "b_stator.pos")
    nbrPolePairs = machine.nbrPolePairs
    calcAngle = (
        simulationParameters["SYM"]["FINAL_ROTOR_POS"]
        - simulationParameters["SYM"]["INIT_ROTOR_POS"]
    )
    if 360 / nbrPolePairs > calcAngle:
        # make sure at least one electrical period has been simulated
        # pylint: disable=locally-disabled,  line-too-long
        logger.warning(
            "IRON LOSS CALCULATION: Simulated rotation (%.3f°) might be "
            "smaller than one electrical period! Iron loss calculation is "
            "only valid if at least one electrical period is simulated.",
            calcAngle,
        )
    rotorMat = machine.rotor._domainLam.physicals[0].material
    statorMat = machine.stator._domainLam.physicals[0].material
    if (
        isfile(brFilePath)
        and isfile(bsFilePath)
        and isinstance(rotorMat, ElectricalSteel)
        and isinstance(statorMat, ElectricalSteel)
    ):
        # FIXME: Material properties should be given valid
        lossParams = rotorMat.lossParams
        ironLossR, _ = core_loss.main(
            brFilePath,
            loss_factor={
                "hyst": lossParams[0],
                "eddy": lossParams[1],
                "exc": lossParams[2],
            },
            sym_factor=machine.symmetry_factor,
            axial_length=machine.rotor.axial_length,
        )
        lossParams = statorMat.lossParams
        ironLossS, time = core_loss.main(
            bsFilePath,
            loss_factor={
                "hyst": lossParams[0],
                "eddy": lossParams[1],
                "exc": lossParams[2],
            },
            sym_factor=machine.symmetry_factor,
            axial_length=machine.stator.axial_length,
        )
        core_loss.write_simple(join(resPath, "Pv_hyst_R.dat"), time, ironLossR["hyst"])
        core_loss.write_simple(join(resPath, "Pv_hyst_S.dat"), time, ironLossS["hyst"])
        core_loss.write_simple(join(resPath, "Pv_eddy_R.dat"), time, ironLossR["eddy"])
        core_loss.write_simple(join(resPath, "Pv_eddy_S.dat"), time, ironLossS["eddy"])
        core_loss.write_simple(join(resPath, "Pv_exc_R.dat"), time, ironLossR["exc"])
        core_loss.write_simple(join(resPath, "Pv_exc_S.dat"), time, ironLossS["exc"])
    else:
        logger.warning(
            "IRON LOSS CALCULATION: field file 'b_rotor.pos' or 'b_stator.pos'"
            " not found in '%s'",
            resPath,
        )


def is_single_transient(res_dir: str) -> bool:
    """Function to determine if the results inside the results folder are from
    a single transient simulation (nbr_sims = 1 && nbr_timesteps > 1).

    Args:
        res_dir (str): Path to results folder

    Returns:
        bool: True if nbr_sims = 1 && nbr_timesteps > 1 otherwise False.

    :meta private:
    """
    # This function checks a results folder for .dat results files and
    # determines if the results are transient
    # get all dat results from results folder
    dat_file_list, _ = import_results.get_result_files(res_dir)
    # if there are results
    if dat_file_list:
        # for dat_file in dat_file_list:
        # get time and data values of first file
        time, data = import_results.read_timetable_dat(join(res_dir, dat_file_list[0]))
        if time.size > 1:
            # get number of simulations in that file
            nbrSim, _, _ = import_results.split_data(time, data)
            if nbrSim == 1:
                # timesteps > 1 and number of simulation = 1
                return True
    # otherwise false
    return False
