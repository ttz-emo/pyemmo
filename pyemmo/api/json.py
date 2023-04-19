"""This is the main module of the json api to create a machine model in Onelab."""
# import debugpy
# debugpy.debug_this_thread()
import subprocess
import warnings
from argparse import ArgumentParser
from os import mkdir
from os.path import isdir, isfile, join
from typing import Dict, List, Tuple

from ..definitions import RESULT_DIR
from ..functions import runOnelab, calcIronLoss
from ..script.geometry.machineAllType import MachineAllType
from ..script.geometry.rotor import Rotor
from ..script.geometry.stator import Stator
from ..script.script import Script
from ..script.material import ElectricalSteel
from . import boundaryJSON, importJSON, modelJSON, apiNameDict
from .SurfaceJSON import SurfaceAPI

# from swat_em import analyse
# from .. import calcPhaseangleStarvoltageCorr

# analyse.calc_phaseangle_starvoltage = calcPhaseangleStarvoltageCorr


def createMachine(
    segmentSurfDict: Dict[str, SurfaceAPI], extendedInfo: dict
) -> Tuple[MachineAllType, Dict[str, List[SurfaceAPI]]]:
    """create a PyDraft Machine object from a list of surfaces forming one machine segment
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
    # create boundaries
    rotorMovingBandRadius = importJSON.getMovingbandRadius(extendedInfo)
    symFactor = importJSON.getSymFactor(extendedInfo)
    statorPhysicals, rotorPhysicals = boundaryJSON.createBoundaries(
        segmentSurfDict=segmentSurfDict,
        symFactor=symFactor,
        rotorMBRadius=rotorMovingBandRadius,
    )
    # create the remaining machine surfaces
    maschineSurfDict = modelJSON.createMachineGeometryFromSegment(
        segmentSurfDict, symFactor
    )
    # create physical elements from the surfaces
    for idExt, surfList in maschineSurfDict.items():
        surfName = surfList[0].name
        if "GehInnen" in surfName and symFactor == 1:
            # if the inner surface is air, overlapping the rotor, set the delete-flag to not create
            # the inner housing surface
            for surf in surfList:
                surf.delete = True
        else:
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
                ValueError(
                    f"MachineSide was whether rotor or stator: {machineSide}",
                )

    # create the rotor
    axLen = importJSON.getAxialLength(extendedInfo)
    rotorAPI = Rotor(
        name="rotor created via json api",
        physicalElementList=rotorPhysicals,
        axLen=axLen["rotor"],
    )
    # create the stator
    nbrSlotTotal = segmentSurfDict["StNut"].getNbrSegments()
    # create winding
    windingSwat = modelJSON.createWinding(extendedInfo)
    statorAPI = Stator(
        name="stator created via json api",
        nbrSlots=nbrSlotTotal,
        physicalElements=statorPhysicals,
        axLen=axLen["stator"],
        winding=windingSwat,
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


def createMeshSizeGUICode(machineSurfDict: Dict[str, List[SurfaceAPI]]):
    """
    Create the gmsh fomatted code to set the mesh size of the machine surfaces via the GUI.

    The names of the sufaces are defined in the `apiNameDict` (defined globally in
    pydraft.api.init), which links the IdExt value of a SurfaceAPI object to a real name in the
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
            surfList: List[SurfaceAPI] = []
            for surfID in surfID_List:
                surfList.extend(machineSurfDict[surfID])
            # get the mesh size
            meshSize = surfList[0].getMeshSize()
            # if meshsize in surfaceAPI was 0, get the mean mesh size of the points
            if not meshSize:
                meshSize = surfList[0].getMeanMeshLength()
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
    machine = script.getMachine()
    # 1. Airgap flux density
    rotorAirgapRadius = importJSON.getMovingbandRadius(extendedInfo)
    statorAirgapRadius = machine.getStator().getMovingBand()[0].radius
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

    ## Add rotor and stator b-field export for iron loss calculation
    if importJSON.getFlagCalcIronLoss(extendedInfo):
        rotorIronPhysicalID = [
            str(phys.id) for phys in machine.getRotor()._domainLam.physicals
        ]
        statorIronPhysicalID = [
            str(phys.id) for phys in machine.getStator()._domainLam.physicals
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


# ======================================== START MAIN FUNCTION =====================================


def main(
    geo: str,
    extInfo: str,
    model: str,
    gmsh: str = "",
    getdp: str = "",
    results: str = "",
):
    """The main function reads the JSON files and creates the .geo and .pro scripts for a onelab
    simulation.

    Program sequence:
        1. Check that both json files are given and gmsh is installed. Import the geo segments and
           the additional machine information.
        2. Create a PyDraft Machine-object by rotating and duplicating the given surface segments
           with :func:`createMachine() <pydraft.api.json.createMachine>`
        3. Create a PyDraft Script-object with the Machine and the simulation parameters.
        4. Add additional code for the API specific B-field PostOperation (on line evaluation) and
           the surface mesh size setting via the GUI.
        5. Create the .geo and .pro script files by calling :meth:`Script.generateScript()
           <pydraft.script.script.Script.generateScript>`
        6. Create command line call for gmsh/getdp with :func:`createCmdCommand()
           <pydraft.functions.runOnelab.createCmdCommand>` and start with :code:`subprocess.run`


    Args:
        geo (str): File path to JSON formatted geometry file.
        extInfo (str): File path to JSON formatted extended information file.
        model (str): Folder path where the resulting model files should be placed.
        gmsh (str, optional): Gmsh executable path. If nothing is provieded the
            executable will be searched.
        getdp (str, optional): GetDP executable path. Defaults to "".
        results (str, optional): Folder path to store the simulation results.
            Defaults to "modelDir/res_ModelName"
    """
    print("running main() of json-api.")
    # check if gmsh was provided
    if not gmsh:
        # if gmsh was not provided, try to find it:
        gmsh = runOnelab.findGmsh()
    else:
        # if gmsh was given by the user, check that its valid
        if not isfile(gmsh):
            raise FileNotFoundError(f"Provided gmsh executable was not found: {gmsh}")

    # get geometry
    if isfile(geo):
        # import the segment machine geometry
        segmentSurfDict = modelJSON.importMachineGeometry(geo)
    # else:
    #     # print()
    #     msg = (
    #         f"Given json file(s) did not exist! Check '{args.geo}' or '{args.extInfo}'."
    #     )
    #     raise FileNotFoundError(msg)
    elif isinstance(geo, dict):
        segmentSurfDict = geo
    else:
        raise TypeError()

    # addition information
    if isfile(extInfo):
        # import the extended information
        extendedInfo = importJSON.importExtInfo(extInfo)
    elif isinstance(extInfo, dict):
        extendedInfo = extInfo
    else:
        raise TypeError()

    # generate the machine geometry
    machine, machineSurfDict = createMachine(segmentSurfDict, extendedInfo)
    # create dir for model files if it doesnt exist
    if not isdir(model):
        mkdir(model)
    # get the simulation pareameters
    simulationParameters = importJSON.getSimuParams(extendedInfo=extendedInfo)
    # generate the script
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
    apiScript.generateScript(UD_MeshCode=meshSizeSetCode)
    # run(
    #     [args.gmsh, abspath(join(args.mod, testScript.getName() + ".geo")), "-2"],
    #     shell=True,
    # )
    # run(
    #     args.getdp
    #     + " "
    #     + abspath(join(args.mod, testScript.getName() + ".pro"))
    #     + " -solve Analysis -v1",
    #     shell=True,
    # )
    proFile = apiScript.getProFilePath()  # path to .pro file
    command = runOnelab.createCmdCommand(
        onelabFile=proFile,
        gmshPath=gmsh,
        getdpPath=getdp,
        useGUI=importJSON.getFlagOpenGui(extendedInfo),
    )
    # print(f"cmd command is:\n{command}")
    calcInfo = subprocess.run(command, capture_output=True, text=True, check=False)
    print(f"StdOut:\n{calcInfo.stdout}")
    print(f"StdErr:\n{calcInfo.stderr}")

    # iron loss post processing:
    resPath = apiScript.getResultsPath()
    # check if resPath exists -> simulation has been run.
    if (
        importJSON.getFlagCalcIronLoss(extendedInfo)
        and isdir(resPath)
        and simulationParameters["analysis_type"] == 1  # transient simulation
    ):
        # FIXME: Implement better check for simulation status
        brFilePath = join(resPath, "b_rotor.pos")
        bsFilePath = join(resPath, "b_stator.pos")
        nbrPolePairs = machine.getNbrPolePairs()
        calcAngle = (
            simulationParameters["final_rotor_pos"]
            - simulationParameters["init_rotor_pos"]
        )
        if 360 / nbrPolePairs > calcAngle:
            # make sure at least one electrical period has been simulated
            # pylint: disable=locally-disabled,  line-too-long
            warnings.warn(
                f"IRON LOSS CALCULATION: Simulated rotation ({calcAngle}°) might be smaller than one electrical period! Iron loss calculation is only valid if at least one electrical period is simulated."
            )
        rotorMat = machine.getRotor()._domainLam.physicals[0].getMaterial()
        statorMat = machine.getStator()._domainLam.physicals[0].getMaterial()
        if (
            isfile(brFilePath)
            and isfile(bsFilePath)
            and isinstance(rotorMat, ElectricalSteel)
            and isinstance(statorMat, ElectricalSteel)
        ):
            lossParams = rotorMat.lossParams
            calcIronLoss.adaptIronLossParams(lossParams, rotorMat)
            ironLossR, _ = calcIronLoss.main(
                brFilePath,
                lossFactor={
                    "hyst": lossParams[0],
                    "eddy": lossParams[1],
                    "exc": lossParams[2],
                },
                symFactor=importJSON.getSymFactor(extendedInfo),
                axialLength=importJSON.getAxialLength(extendedInfo)["rotor"],
            )
            lossParams = statorMat.lossParams
            calcIronLoss.adaptIronLossParams(lossParams, statorMat)
            ironLossS, time = calcIronLoss.main(
                bsFilePath,
                lossFactor={
                    "hyst": lossParams[0],
                    "eddy": lossParams[1],
                    "exc": lossParams[2],
                },
                symFactor=importJSON.getSymFactor(extendedInfo),
                axialLength=importJSON.getAxialLength(extendedInfo)["stator"],
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_hyst_R.dat"), time, ironLossR["hyst"]
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_hyst_S.dat"), time, ironLossS["hyst"]
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_eddy_R.dat"), time, ironLossR["eddy"]
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_eddy_S.dat"), time, ironLossS["eddy"]
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_exc_R.dat"), time, ironLossR["exc"]
            )
            calcIronLoss.writeSimple(
                join(resPath, "Pv_exc_S.dat"), time, ironLossS["exc"]
            )
        else:
            warnings.warn(
                "IRON LOSS CALCULATION: B field results file 'b_rotor.pos' or 'b_stator.pos' not found in "
                + resPath
            )
            # raise (
            #     FileNotFoundError(
            #         "IRON LOSS CALCULATION: B field results file 'b_rotor.pos' or 'b_stator.pos' not found in "
            #         + resPath
            #     )
            # )

    ###########################################################################################
    ################ Plot Results for Debugging ##################
    # resPath = apiScript.getResultsPath()
    # if isdir(resPath):
    #     # if the folder for results exists
    #     for file in listdir(resPath):
    #         filename, fileExt = splitext(file)
    #         if fileExt == ".dat":
    #             importResults.plotTimeTableDat(
    #                 abspath(join(resPath, file)),
    #                 filename,
    #                 title=filename,
    #                 savefig=True,
    #                 showfig=False,
    #                 savePath=None,
    #             )
    ###########################################################################################


if __name__ == "__main__":
    # 1. Check that all argvs are valid!
    parser = ArgumentParser(
        description="Process Motor-JSON files to generate a Onelab Simulation."
    )
    parser.add_argument(
        "geo",
        help="path to the JSON geometry file ('geometry.json')",
        type=str,
    )
    parser.add_argument(
        "extInfo",
        help="path to the extended info JSON file ('extendedInfo.json')",
        type=str,
    )
    parser.add_argument(
        "--gmsh",
        help="path to the Gmsh executable",
        type=str,
        default="",
    )
    parser.add_argument(
        "--getdp", help="path to the GetDP executable", type=str, default=""
    )
    parser.add_argument(
        "--mod",
        help="path where the model files should be stored",
        type=str,
        default=RESULT_DIR,
    )
    parser.add_argument(
        "--res",
        help="path where the simulation results should be stored",
        type=str,
        default="",
    )

    args = parser.parse_args()
    main(
        geo=args.geo,
        extInfo=args.extInfo,
        gmsh=args.gmsh,
        getdp=args.getdp,
        model=args.mod,
        results=args.res,
    )
