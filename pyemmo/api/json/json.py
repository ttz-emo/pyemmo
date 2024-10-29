#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied
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

import datetime
import json
import logging
import os
import subprocess
from os import mkdir
from os.path import isdir, isfile, join

import gmsh

from ... import logFmt
from ...functions import calcIronLoss, import_results, runOnelab
from ...script.geometry.machineAllType import MachineAllType
from ...script.geometry.rotor import Rotor
from ...script.geometry.stator import Stator
from ...script.material import ElectricalSteel
from ...script.script import Script
from .. import logger
from . import apiNameDict
from . import boundaryJSON as boundary
from . import importJSON, modelJSON
from .SurfaceJSON import SurfaceAPI

gmsh.initialize()

# from swat_em import analyse
# from .. import calcPhaseangleStarvoltageCorr

# analyse.calc_phaseangle_starvoltage = calcPhaseangleStarvoltageCorr


def createMachine(
    segmentSurfDict: dict[str, SurfaceAPI], extendedInfo: dict
) -> tuple[MachineAllType, dict[str, list[SurfaceAPI]]]:
    """create a pyemmo Machine object from a list of surfaces forming one machine segment
    (imported from matlab).

    Args:
        segmentSurfDict (Dict[str, SurfaceAPI]): dict of surfaces forming one machine segment
            (on stator and rotor side). Segment width for rotor and stator can be different.
            Dict keys are IdExt of SurfaceAPI.
        extendedInfo (dict): Dict with additional information like pole pair number and axial
            length.

    Returns:
        Tuple[MachineAllType, Dict[str, List[SurfaceAPI]]]: Resulting machine object and Machine
        surface dict with IdExt as keys and list of SurfaceAPI objects as items.
    """
    symFactor = importJSON.getSymFactor(extendedInfo)
    rotorMovingBandRadius = importJSON.getMovingbandRadius(extendedInfo)
    # create the remaining machine surfaces
    maschineSurfDict = modelJSON.createMachineGeometryFromSegment(
        segmentSurfDict, symFactor
    )
    gmsh.model.occ.remove_all_duplicates()
    gmsh.model.occ.synchronize()

    rotorPhysicals, statorPhysicals = boundary.get_boundaries(
        maschineSurfDict, symFactor, rotorMovingBandRadius
    )

    # Log winding layout for debugging *before* createSlot() is called.
    logger.debug(f"Winding layout: {importJSON.getWindingList(extendedInfo)}")
    # create physical elements from the surfaces
    for idExt, surfList in maschineSurfDict.items():
        surfName = surfList[0].name
        if "GehInnen" in surfName and symFactor == 1:
            # if the inner surface is air, overlapping the rotor, set the delete-flag to not create
            # the inner housing surface
            for surf in surfList:
                surf.delete = (
                    True  # -> TODO: Make sure delete also removes the gmsh instance
                )
        else:
            logging.debug("Creating physical for %s", idExt)
            physSurfList, machineSide = modelJSON.createPhysicalSurfaces(
                idExt=idExt,
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
    if logging.getLogger().level <= logging.DEBUG:
        gmsh.model.occ.synchronize()
        # gmsh.fltk.run()
    # create the rotor
    axLen = importJSON.getAxialLength(extendedInfo)
    rotorAPI = Rotor(
        name="rotor created via json api",
        physicalElementList=rotorPhysicals,
        axLen=axLen["rotor"],
    )
    # create the stator
    # create winding
    windingSWAT = modelJSON.createWinding(extendedInfo)
    statorAPI = Stator(
        name="stator created via json api",
        nbrSlots=windingSWAT.get_num_slots(),
        physicalElements=statorPhysicals,
        axLen=axLen["stator"],
        winding=windingSWAT,
    )

    # create the machine object
    nbrPolePair = importJSON.getNbrPolePairs(extendedInfo)
    modelName = importJSON.getModelName(extendedInfo)
    machineSiemens = MachineAllType(
        rotor=rotorAPI,
        stator=statorAPI,
        name=f"Machine from json interface ({modelName})",
        nbrPolePairs=nbrPolePair,
        symmetryFactor=symFactor,
    )
    return machineSiemens, maschineSurfDict


def createMeshSizeGUICode(machineSurfDict: dict[str, list[SurfaceAPI]]):
    """
    Create the gmsh fomatted code to set the mesh size of the machine surfaces via the GUI.

    The names of the sufaces are defined in the `apiNameDict` (defined globally in
    pyemmo.api.init), which links the IdExt value of a SurfaceAPI object to a real name in the
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
        machineSurfDict (Dict[str, List[SurfaceAPI]]): dictionary with IdExt as keys.
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
    # First get all IDs containing idExt into idList (e.g. there could be "LplR" and "LplL"
    # for idExt = "Lpl")
    for idExt, apiSurfName in apiNameDict.items():
        surfID_List = []
        for surfID in machineSurfDict.keys():
            if idExt in surfID:
                surfID_List.append(surfID)
        # if there were ids containing idExt
        if surfID_List:
            # create a List of all surfaces with idExt in it -> surfList
            surfList: list[SurfaceAPI] = []
            for surfID in surfID_List:
                surfList.extend(machineSurfDict[surfID])
            # get the mesh size
            meshSize = surfList[0].meshSize
            # if meshsize in surfaceAPI was 0, get the mean mesh size of the points
            if not meshSize:
                meshSize = surfList[0].meanMeshLength
            meshSize = round(meshSize * 1e3, 3)
            try:
                # try to get the real name from the api name dict
                surfName = apiSurfName
            except KeyError:
                # if idExt not in api name dict, use surface name
                surfName = surfList[0].name()
            except Exception as exce:
                raise exce
            mscDefConst += (
                f"""\t\t{idExt}_msf = {{{meshSize},"""
                + f""" Name StrCat[INPUT_MESH, "05Mesh Size/{surfName} [mm]"],"""
                + f"""Min {meshSize/10}, Max {meshSize * 10}, Step 0.1,"""
                + "Visible Flag_SpecifyMeshSize},\n"
            )
            surfIds = [str(surf.id) for surf in surfList]
            # pylint: disable=locally-disabled,  line-too-long
            mscSetSize += f"\tMeshSize {{ PointsOf {{Surface{{ {','.join(surfIds)} }};}} }} = {idExt}_msf*mm;\n"
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
    machine = script.machine
    # 1. Airgap flux density
    rotorAirgapRadius = importJSON.getMovingbandRadius(extendedInfo)
    statorAirgapRadius = machine.stator.movingBand[0].radius
    for side, radius in {
        "rotor": rotorAirgapRadius,
        "stator": statorAirgapRadius,
    }.items():
        for quantity in ["b_radial", "b_tangent"]:
            sign = "-" if side == "rotor" else "+"
            resFilePath = join("CAT_RESDIR", quantity + "_airgap_" + side + ".pos")
            # resFilePath = abspath(
            #     join(script.getResultsPath(), quantity + "_airgap_" + side + ".pos")
            # )
            script.addPostOperation(
                quantityName=quantity,
                name="GetBOnRadius",
                OnGrid=(
                    f"{{({radius}*(1{sign}0.0001))*Cos[$A*Pi/180],"
                    f"({radius}*(1{sign}0.0001))*Sin[$A*Pi/180],0}}"
                    "{0:360/SymmetryFactor:0.5,0,0}"
                ),
                File=resFilePath,
                Name=f'"{quantity} (airgap {side})"',
            )

    # 2. Tooth Flux density
    if "r_z" in extendedInfo.keys():
        toothRadius = extendedInfo["r_z"]
        for quantity in ["b_radial", "b_tangent"]:
            script.addPostOperation(
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
        for quantity in ["b_radial", "b_tangent"]:
            script.addPostOperation(
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
    if importJSON.getFlagCalcIronLoss(extendedInfo):
        rotorIronPhysicalID = [
            str(phys.id) for phys in machine.rotor._domainLam.physicals
        ]
        statorIronPhysicalID = [
            str(phys.id) for phys in machine.stator._domainLam.physicals
        ]
        script.addPostOperation(
            "b",
            "GetBIron",
            OnElementsOf=f"Region[{{{','.join(rotorIronPhysicalID)}}}]",
            File=join("CAT_RESDIR", "b_rotor.pos"),
            Name='"b (rotor)"',
        )
        script.addPostOperation(
            "b",
            "GetBIron",
            OnElementsOf=f"Region[{{{','.join(statorIronPhysicalID)}}}]",
            File=join("CAT_RESDIR", "b_stator.pos"),
            Name='"b (stator)"',
        )

    # 5. PM Eddy current loss
    if machine._domainM.physicals:
        # if there are magnets
        allMagConducting = True
        for magnet in machine._domainM.physicals:
            if magnet.material.conductivity is None:
                allMagConducting = False
                logging.warning(
                    "Unable to calculate magnet losses, due to missing el. conductivity in %s.",
                    magnet.name,
                )
                break
        if allMagConducting:
            script.addPostOperation(
                "JouleLosses[Rotor_Magnets]",
                "GetMagnetLosses",
                OnGlobal="",
                Format="TimeTable",
                File=join("CAT_RESDIR", "Pv_eddy_Mag.dat"),
                # Name='"p (stator)"',
            )
            script.simParams["SYM"]["CALC_MAGNET_LOSSES"] = 1


# ======================================== START MAIN FUNCTION =====================================


def main(
    geo: str | dict,
    extInfo: str | dict,
    model: str | os.PathLike,
    gmsh: str | os.PathLike = "",
    getdp: str | os.PathLike = "",
    results: str | os.PathLike = "",
):
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
            :func:`createCmdCommand() <pyemmo.functions.runOnelab.createCmdCommand>`
            and start with :code:`subprocess.run`


    Args:
        geo (str or dict): File path to JSON formatted geometry file OR segment
            surface dict with IdExt as keys and SurfaceAPI objects as values.
        extInfo (str or dict): File path to JSON formatted extended information
            file or directly given info dict.
        model (str): Folder path where the resulting model files should be
            placed.
        gmsh (str, optional): Gmsh executable path. If nothing is provieded the
            executable will be searched.
        getdp (str, optional): GetDP executable path. Defaults to "".
        results (str, optional): Folder path to store the simulation results.
            Defaults to "modelDir/res_ModelName"
    """
    # create dir for model files if it doesnt exist
    if not isdir(model):
        mkdir(model)
    # Set logging path to model dir
    jsonLogFileHandler = logging.FileHandler(
        filename=os.path.join(model, "pyemmo_jsonAPI.log"),
        mode="w",
        encoding="utf-8",
    )
    jsonLogFileHandler.setLevel(logger.getEffectiveLevel())
    jsonLogFileHandler.setFormatter(logFmt)
    logger.addHandler(jsonLogFileHandler)
    logging.info(
        "PyEMMO API started on %s %s",
        datetime.date.today(),
        datetime.datetime.now().strftime("%H:%M:%S"),
    )

    # get geometry
    if isinstance(geo, str):
        if isfile(geo):
            # import the segment surface list from the json file
            try:
                with open(geo, encoding="utf-8") as jsonFile:
                    machineGeoList = json.load(jsonFile)
                    # create dict with surface api (segment) objects from the surface list
                    segmentSurfDict = modelJSON.importMachineGeometry(machineGeoList)
            except FileNotFoundError as fnfe:
                raise fnfe
            except Exception as exept:
                raise exept
        else:
            raise (FileNotFoundError(f"Given file path {geo} was not a file."))
    elif isinstance(geo, dict):
        segmentSurfDict = geo
    else:
        raise TypeError(
            f"Geometry file has to be type 'File' or 'dict', not {type(geo)}"
        )

    # addition information
    if isinstance(extInfo, str):
        if isfile(extInfo):
            # import the extended information
            extendedInfo = importJSON.importExtInfo(extInfo)
        else:
            raise (FileNotFoundError(f"Given file path {extInfo} was not a file."))
    elif isinstance(extInfo, dict):
        extendedInfo = extInfo
    else:
        raise TypeError(
            f"Model information file has to be type 'File' or 'dict', not {type(extInfo)}"
        )

    # generate the machine geometry
    machine, machineSurfDict = createMachine(segmentSurfDict, extendedInfo)

    # set function mesh
    if "useFunctionMesh" in extendedInfo.keys():
        if extendedInfo["useFunctionMesh"]:
            machine.setFunctionMesh()

    # get the simulation pareameters
    simulationParameters = importJSON.getSimuParams(extendedInfo=extendedInfo)
    logger.info("Generating the Script object in JSON API.")
    apiScript = Script(
        name=importJSON.getModelName(extendedInfo),
        scriptPath=model,
        simuParams=simulationParameters,
        machine=machine,
        resultsPath=results,
        # factory="OpenCascade",
    )
    addPostOperations(apiScript, extendedInfo)
    meshSizeSetCode = createMeshSizeGUICode(machineSurfDict)
    # generate geo and pro files:
    apiScript.generateScript(UD_MeshCode=meshSizeSetCode)

    if importJSON.getFlagOpenGui(extendedInfo) is True:
        _open_onelab(apiScript, extendedInfo, gmsh, getdp)

    logger.removeHandler(jsonLogFileHandler)
    jsonLogFileHandler.close()  # close log file handler!
    return apiScript


def _open_onelab(
    apiScript: Script, extendedInfo: dict, gmsh: str = "", getdp: str = ""
):
    """
    Private function to open ONELAB simulation in GUI and evaluate results
    """
    # check if gmsh was provided
    if not gmsh:
        # if gmsh was not provided, try to find it:
        logger.debug("Gmsh path not given. Trying to find Gmsh...")
        gmsh = runOnelab.findGmsh()
    else:
        # if gmsh was given by the user, check that its valid
        if not isfile(gmsh):
            raise FileNotFoundError(f"Provided gmsh executable was not found: {gmsh}")
    proFile = apiScript.proFilePath  # path to .pro file
    command = runOnelab.createCmdCommand(
        onelabFile=proFile,
        gmshPath=gmsh,
        getdpPath=getdp,
        useGUI=True,
    )
    logging.debug("CMD command is: '%s'", command)
    calcInfo = subprocess.run(
        command,
        capture_output=True,  # not importJSON.getFlagOpenGui(extendedInfo),
        text=True,
        check=False,
        shell=False,
    )
    # print(f"StdOut:\n{calcInfo.stdout}")
    if calcInfo.stderr:
        for textLine in calcInfo.stderr.split("\n"):
            if "error" in textLine.lower():
                logging.error(
                    "Onelab call issued the following error: \n\t%s",
                    textLine.replace("\n", "\n\t"),
                )
            else:
                if textLine:  # if textline is not empty
                    logging.warning(
                        "Onelab call issued the following warning: \n\t%s",
                        textLine.replace("\n", "\n\t"),
                    )
    # iron loss post processing:
    resPath = apiScript.resultsPath
    # check if resPath exists -> simulation has been run.
    if isdir(resPath):
        # check if the simulation that has been run is a single transient simulation:
        sim_is_transient = is_single_transient(resPath)
        if importJSON.getFlagCalcIronLoss(extendedInfo):
            if sim_is_transient:
                # if core loss flag and simulation is transient, calc core loss:
                _run_core_loss_calculation(resPath, apiScript)
            else:
                logger.warning(
                    "IRON LOSS CALCULATION: Iron loss calculation "
                    "cannot be done for static simulation!",
                )
        # Plot Results for Debugging
        if logger.getEffectiveLevel() <= 10:
            # if the folder for results exists
            import_results.plt.set_loglevel(
                level="info"
            )  # avoid matplotlib debug infos
            for file in os.listdir(resPath):
                filename, fileExt = os.path.splitext(file)
                if fileExt == ".dat":
                    import_results.plot_timetable_dat(
                        os.path.abspath(join(resPath, file)),
                        filename,
                        title=filename,
                        savefig=True,
                        showfig=False,
                        savePath=None,
                    )


def _run_core_loss_calculation(resPath, apiScript: Script):
    """Private function to run core loss calculation in case of GUI api run.

    Args:
        resPath (str): Path to the results directory.
        apiScript (Script): Script object.
    """
    machine = apiScript.machine
    simulationParameters = apiScript.simParams
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
        ironLossR, _ = calcIronLoss.main(
            brFilePath,
            loss_factor={
                "hyst": lossParams[0],
                "eddy": lossParams[1],
                "exc": lossParams[2],
            },
            sym_factor=machine.symmetryFactor,
            axial_length=machine.rotor.axialLength,
        )
        lossParams = statorMat.lossParams
        ironLossS, time = calcIronLoss.main(
            bsFilePath,
            loss_factor={
                "hyst": lossParams[0],
                "eddy": lossParams[1],
                "exc": lossParams[2],
            },
            sym_factor=machine.symmetryFactor,
            axial_length=machine.stator.axialLength,
        )
        calcIronLoss.write_simple(
            join(resPath, "Pv_hyst_R.dat"), time, ironLossR["hyst"]
        )
        calcIronLoss.write_simple(
            join(resPath, "Pv_hyst_S.dat"), time, ironLossS["hyst"]
        )
        calcIronLoss.write_simple(
            join(resPath, "Pv_eddy_R.dat"), time, ironLossR["eddy"]
        )
        calcIronLoss.write_simple(
            join(resPath, "Pv_eddy_S.dat"), time, ironLossS["eddy"]
        )
        calcIronLoss.write_simple(join(resPath, "Pv_exc_R.dat"), time, ironLossR["exc"])
        calcIronLoss.write_simple(join(resPath, "Pv_exc_S.dat"), time, ironLossS["exc"])
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
