import sys
import os
from os.path import expanduser, isdir, isfile, join, normpath, splitext
from typing import Dict, Union, List
import logging
from shutil import which
import subprocess
from argparse import ArgumentParser
import numpy as np

from . import calcIronLoss
from .importResults import readTimeTableDat


def findGmsh(verbosity: bool = True) -> str:
    """Find gmsh executable on maschine"""
    gmshExe = findExe("gmsh", verbosity=verbosity)
    return gmshExe


def findGetDP(verbosity: bool = True) -> str:
    """Find getdp executable on maschine"""
    getdpExe = findExe("getdp", verbosity=verbosity)
    return getdpExe


def findExe(exeName: str, verbosity: bool = True) -> str:
    """Search the local machine for the executalble given in exeName.
    There are several searching stages and the function returns the exe path if one stage gives a result:
        1. search with "which" command
        2. search the python path
        3. search the "User/appdate/local/programs" path

    TODO:
        Search "C:/Program Files" path

    Args:
        exeName (str): name of the executable. E.g. "myExe.exe" or just "myExe"
        verbosity (bool): Print additional information to the command line if True. Defaults to True.

    Raises:
        SystemError: If not run on Windows
        FileNotFoundError: If the exe is not found.

    Returns:
        str: filepath to the executable
    """
    executableName, _ = splitext(exeName)
    # first opion: try to find gmsh with "which"
    exePath = which(executableName)
    if not exePath:
        if verbosity:
            logging.debug(
                "Could not find %s from command line. Trying to find it in python-path...",
                executableName,
            )
        # second option: try to find gmsh in python path. (Should work since gmsh module is installed!)
        for path in sys.path:
            if isdir(path):
                for fileList in os.listdir(path):
                    if fileList == f"{executableName}.exe":
                        exePath = join(path, fileList)
                        if verbosity:
                            logging.debug(
                                "Found %s in '%s'!", executableName, exePath
                            )
                        return exePath
        if not exePath:
            if verbosity:
                logging.debug(
                    "%s was not found in 'path' Variable. Trying to find it in user home directory. This can take some time!",
                    executableName,
                )
            # third option: try to find {executableName} in user/local/programs and subfolders. Takes time to iterate through all files
            if sys.platform.startswith("win32"):
                # is system windows; user-program-path:
                userProgDir = normpath(
                    join(expanduser("~"), "appdata", "local", "programs")
                )
                # try to find {executableName} in user programm path
                if isdir(userProgDir):
                    for root, _, files in os.walk(userProgDir):
                        if files == f"{executableName}.exe":
                            if verbosity:
                                logging.debug(
                                    "Found %s in '%s'! :)",
                                    executableName,
                                    root,
                                )
                            return join(root, f"{executableName}.exe")
                    # if exe was not found in home dir
                    if verbosity:
                        logging.debug(
                            "%s could not be found in home program folder '%s'",
                            executableName,
                            userProgDir,
                        )
                else:
                    if verbosity:
                        logging.debug("Can't find home directory.")
            else:
                raise SystemError(
                    f"sys.platform is {sys.platform}, not 'win32'.  Could not find home directory"
                )
            if not exePath:
                raise FileNotFoundError(
                    f"Can not find {executableName} on your system! Please install {executableName} or set PATH Variable."
                )
    else:
        if verbosity:
            logging.debug("Found %s in '%s'!", executableName, exePath)
        return exePath


def mergeAllGeoFiles(folderPath, gmshExe):
    # get all files in path:
    allFiles = os.listdir(folderPath)
    allCommands = list()
    allCommands.append(gmshExe)  # add gmsh exe as first command part
    for filename in allFiles:
        if ".geo" in filename:  # if its a geo file
            geoFilePath = join(folderPath, filename)
            allCommands.append(
                geoFilePath
            )  # append the total filename to allCommands
    subprocess.run(allCommands, shell=True)
    return None


def createCmdCommand(
    onelabFile: str,
    useGUI: bool,
    gmshPath: Union[str ,os.PathLike] = "",
    getdpPath: Union[str ,os.PathLike] = "",
    logFileName: Union[str ,os.PathLike] = "",
    paramDict: Dict[str, Union[str, int, float]] = None,
    postOperations: List[str] = None,
) -> str:
    """Create a cmd command to open a .geo or .pro file with the gmsh gui or
    run gmsh and getdp from the command line.

    Args:
        onelabFile (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui (independed if its a geo or pro file).
        gmshPath (str): Path to the gmsh executable. By defaults the gmsh exe is searched.
        getdpPath (str, optional): path to a getdp executable. Path will only be used if gui is not used. Defaults to "".
        paramDict (Dict[str, Union[str, int, float]], optional): Dict with parameters to set in the simulation. Defaults to None.

            E.g. to set the onelab parameter "IQ_RMS" for the quadrature rms current to 10A the dict would look like:

            .. code:: python

                {
                    "IQ_RMS": 10,
                }

        postOperations (List[str], optional): List containing the PostOperation names that should be performed after the solving stage.
            ! PostOperations will only be executed if a getdp executable is given !

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    if not gmshPath:
        gmshPath = findGmsh()
    # check if the onelab file is valid:
    if isfile(onelabFile):
        (filePath, ext) = splitext(onelabFile)
        # first part of the cmd command: open the geo or pro-file
        command = (
            f'{gmshPath} "{onelabFile}"'  # the command is: 'gmsh "FILE.xxx"'
        )
        if ext.lower() == ".geo":
            # if its a geo file
            if not useGUI:
                # run onelab server in command line if gui is False
                #   this does the meshing and database generation
                command += " -run"  # the command is: "gmsh FILE.geo -run"
                if logFileName:
                    command += f" -log {logFileName} "
            # else:
            #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
        elif ext.lower() == ".pro":
            if not useGUI:
                if getdpPath:
                    # if command line and getdp specified

                    # # TODO: Check if mesh file exists -> if not, create command to generate .msh file
                    # if not isfile(filePath+'.msh')

                    command = f"{gmshPath} {filePath}.geo -run "  # set the gmsh file extension to mesh and && for new command
                    if logFileName:
                        command += f" -log {logFileName} "
                    command += "&& "
                    command += f"{getdpPath} {onelabFile} -solve Analysis"  # run the simulation with specific getdp exe
                    # the command is: "gmsh FILE.geo -run && getdp FILE.pro -solve Analysis"
                    # add post operations
                    if postOperations:
                        command += " -pos "
                        for postOp in postOperations:
                            if isinstance(postOp, str):
                                command += postOp + " "
                            else:
                                raise (
                                    ValueError(
                                        f"Given Post Operation name was not a string: {type(postOp)}, {postOp}"
                                    )
                                )
                else:
                    # only command line specified
                    command += " -run"  # just run "gmsh FILE.pro -run", which auto-selects a getdp installation
            # else:
            # if gui was specified, just leave the command as it is: "gmsh FILE.pro" to open gui
        else:
            raise (
                ValueError(
                    f"File '{onelabFile}' has wrong file extension (not '.geo' or '.pro') or is missing file extension: {ext}"
                )
            )
        if paramDict:
            # if the paramDict is not empty or None
            if not isinstance(paramDict, dict):
                raise TypeError(
                    f"Parameter dict was not a dict, but type '{type(paramDict)}.'"
                )
            else:
                for paramName, paramValue in paramDict.items():
                    if isinstance(paramValue, str):
                        command += f" -setstring {paramName} {paramValue}"
                    elif isinstance(paramValue, (float, int)):
                        command += f" -setnumber {paramName} {paramValue}"
                    else:
                        raise (
                            TypeError(
                                f"Parameter value was not string, float or int! -> {type(paramValue)}"
                            )
                        )
    else:
        raise FileNotFoundError(
            f"Provided Onelab file was not found: {onelabFile}"
        )
    return command


def createGMSHCommand(
    gmshFile: str,
    useGUI: bool,
    gmshPath: str = "",
    logFileName: str = "",
) -> str:
    """Create a cmd command to open a GMSH .geo file with the GUI or
    generate the mesh by running gmsh from the command line.

    Args:
        onelabFile (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui (independed if its a geo or pro file).
        gmshPath (str): Path to the gmsh executable. By defaults the gmsh exe is searched.

            E.g. to set the onelab parameter "IQ_RMS" for the quadrature rms current to 10A the dict would look like:

            .. code:: python

                {
                    "IQ_RMS": 10,
                }

        postOperations (List[str], optional): List containing the PostOperation names that should be performed after the solving stage.
            ! PostOperations will only be executed if a getdp executable is given !

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    if not gmshPath:
        gmshPath = findGmsh()
    # check if the onelab file is valid:
    if isfile(gmshFile):
        (filePath, ext) = splitext(gmshFile)
        # first part of the cmd command: open the geo or pro-file
        command = (
            f'{gmshPath} "{gmshFile}"'  # the command is: 'gmsh "FILE.xxx"'
        )
        if ext.lower() == ".geo":
            # if its a geo file
            if not useGUI:
                # run onelab server in command line if gui is False
                #   this does the meshing and database generation
                command += " -run"  # the command is: "gmsh FILE.geo -run"
                if logFileName:
                    command += f" -log {logFileName} "
            # else:
            #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
        elif ext.lower() == ".pro":
            if not useGUI:
                # only command line specified
                command += " -run"  # just run "gmsh FILE.pro -run", which auto-selects a getdp installation
            # else:
            # if gui was specified, just leave the command as it is: "gmsh FILE.pro" to open gui
        else:
            raise (
                ValueError(
                    f"File '{gmshFile}' has wrong file extension (not '.geo' or '.pro') or is missing file extension: {ext}"
                )
            )
    else:
        raise FileNotFoundError(
            f"Provided Onelab file was not found: {gmshFile}"
        )
    return command


def runCalcforCurrent(param: dict):

    RES_DIR = param["res"]
    if not os.path.isdir(RES_DIR):
        raise RuntimeError(f"Result directory does not exist: {RES_DIR}")
    # adding additional results path because its initally set in the parameter geo file.
    # But if the files are moved the results folder might not exist any more!
    param["getdp"]["ResPath"] = RES_DIR
    pro_file = param["pro"]
    simulation_res_dir = os.path.join(RES_DIR, param["ResId"])
    if not os.path.isdir(simulation_res_dir):
        # only run if results dir for this simulation not exists
        # determine if core loss can be calculated
        post_operations = None
        if "hyst" in param and "eddy" in param:
            post_operations = ["GetBIron"]  # calc core loss

        cmdCommand = createCmdCommand(
            pro_file,
            useGUI=False,
            gmshPath=param["gmsh"],
            getdpPath=param["exe"],
            paramDict=param["getdp"],
            postOperations=post_operations,
        )

        logging.debug("cmd command is: %s", cmdCommand)
        logging.info("Running simulation for result-ID '%s'", param["ResId"])

        subprocess.run(
            cmdCommand,
            check=True,  # raise Python-error on error execution error
            capture_output=False,
            stdout=subprocess.DEVNULL,
        )
    else:
        # Simulation with this resId has allready been done!
        # raise RuntimeError(
        #     f"Result directory {simulation_res_dir} allready exists!"
        # )
        logging.warning(
            "Result directory %s allready exists!", simulation_res_dir
        )
    ##########################################################################
    # EVALUATE RESULTS
    ##########################################################################
    logging.info("Import results for result-ID '%s'", param["ResId"])
    results_dict = {}
    # try to import getdp parameters from param dict
    # TODO: Add start and stop angle, angle and time step, ...
    # OTHER OPTION: Just add input param dict to result dict...
    for key, getdp_param in {
        "id": "ID_RMS",
        "iq": "IQ_RMS",
        "speed": "RPM",
    }.items():
        try:
            results_dict[key] = param["getdp"][getdp_param]
        except KeyError:
            pass
        except Exception as exce:
            raise exce
    # 1. Phase currents
    results_dict["current"] = {}
    for index in "abc":
        res_file = os.path.join(simulation_res_dir, f"I{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            results_dict["time"], results_dict["current"][index] = (
                readTimeTableDat(res_file)
            )
        else:
            # Error because we need to import time here!
            raise FileNotFoundError(
                f"Could not find result file for phase current I{index}"
            )

    # 2. Torque Results
    results_dict["torque"] = {}
    results_dict["torque_vw"] = {}
    for side in ["rotor", "stator"]:
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque"][side] = readTimeTableDat(res_file)
        # Virtual Work results
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}_vw.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque_vw"][side] = readTimeTableDat(res_file)

    # 3. Flux results
    results_dict["flux"] = {}
    for index in "abcdq0":
        res_file = os.path.join(simulation_res_dir, f"Flux_{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            time, results_dict["flux"][index] = readTimeTableDat(res_file)

    # 4. Induced voltage
    results_dict["inducedVoltage"] = {}
    for index in "ABC":
        res_file = os.path.join(
            simulation_res_dir, f"InducedVoltage{index}.dat"
        )
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["inducedVoltage"][index] = readTimeTableDat(
                res_file
            )

    # 5. Rotor position
    res_file = os.path.join(simulation_res_dir, "RotorPos_deg.dat")
    if os.path.isfile(res_file):
        # get first char in machine side to index rotor and stator results
        _, results_dict["rotorPos"] = readTimeTableDat(res_file)

    # 6. Core loss
    # Check if file hystLoss_rotor.dat allready exists -> loss allready calculated
    core_loss_dict = {}
    if not os.path.exists(
        os.path.join(simulation_res_dir, "hystLoss_rotor.dat")
    ):
        if post_operations is not None:
            # calculate core loss
            totalLoss = 0
            for _, side in enumerate(["rotor", "stator"]):
                bFilePath = os.path.join(simulation_res_dir, f"b_{side}.pos")
                lossDict, time = calcIronLoss.main(
                    bFilePath,
                    loss_factor={
                        "hyst": param["hyst"],
                        "eddy": param["eddy"],
                        "exc": param["exc"],
                    },
                    sym_factor=param["sym"],
                    axial_length=param["axLen"],
                )
                totalLoss += sum(lossDict.values())
                # print(f"Iron losses for {paramDict['ResId']} on {side} are: {lossDict}")

                # save to file:
                for loss_type, loss_data in lossDict.items():
                    core_loss_res_file = os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                    calcIronLoss.write_simple(
                        core_loss_res_file, time, loss_data
                    )
                    # with open(ironLossResFile, mode="w+", encoding="utf-8") as file:
                    #     lossDataJSON = json.dumps(ironLossDictList, indent=3)
                    #     file.write(lossDataJSON)
                core_loss_dict[side] = lossDict
    else:
        logging.warning(
            "Iron losses for %s have allready been calculated.\nImporting values...",
            param["ResId"],
        )
        for side in ["rotor", "stator"]:
            core_loss_dict[side] = {}
            for loss_type in ("hyst", "eddy", "exc"):
                time, core_loss_dict[side][loss_type] = readTimeTableDat(
                    os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                )
    if core_loss_dict:
        results_dict["coreLoss"] = core_loss_dict
        # pylint: disable=locally-disabled, logging-not-lazy, logging-fstring-interpolation, line-too-long
        logging.debug("Iron loss for '" + param["ResId"] + "'")
        logging.debug(f"{'Rotor':>24} {'Stator':>11} {'Gesamt':>11}")
        logging.debug(
            f"{'Hysteresis:':<14} {np.mean(core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['stator']['hyst']+core_loss_dict['rotor']['hyst']) : 9.3f} W"
        )
        logging.debug(
            f"{'Eddy Current:':<14} {np.mean(core_loss_dict['rotor']['eddy']) : 8.3f} W {np.mean(core_loss_dict['stator']['eddy']) : 9.3f} W {np.mean(core_loss_dict['stator']['eddy']+core_loss_dict['rotor']['eddy']) : 9.3f} W"
        )
        logging.debug(
            f"{'Excess:':<14} {np.mean(core_loss_dict['rotor']['exc']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']) : 9.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['rotor']['exc']) : 9.3f} W"
        )
        logging.debug(
            "---------------------------------------------------------------------"
        )
        logging.debug(
            f"{'Summe:':<14} {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']+core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W"
        )
    return results_dict



def runCalcforCurrent(param: dict):

    RES_DIR = param["res"]
    if not os.path.isdir(RES_DIR):
        raise RuntimeError(f"Result directory does not exist: {RES_DIR}")
    # adding additional results path because its initally set in the parameter geo file.
    # But if the files are moved the results folder might not exist any more!
    param["getdp"]["ResPath"] = RES_DIR
    pro_file = param["pro"]
    simulation_res_dir = os.path.join(RES_DIR, param["ResId"])
    if not os.path.isdir(simulation_res_dir):
        # only run if results dir for this simulation not exists
        # determine if core loss can be calculated
        post_operations = None
        if "hyst" in param and "eddy" in param:
            post_operations = ["GetBIron"]  # calc core loss

        cmdCommand = createCmdCommand(
            pro_file,
            useGUI=False,
            gmshPath=param["gmsh"],
            getdpPath=param["exe"],
            paramDict=param["getdp"],
            postOperations=post_operations,
        )

        logging.debug("cmd command is: %s", cmdCommand)
        logging.info("Running simulation for result-ID '%s'", param["ResId"])

        subprocess.run(
            cmdCommand,
            check=True,  # raise Python-error on error execution error
            capture_output=False,
            stdout=subprocess.DEVNULL,
        )
    else:
        # Simulation with this resId has allready been done!
        # raise RuntimeError(
        #     f"Result directory {simulation_res_dir} allready exists!"
        # )
        logging.warning(
            "Result directory %s allready exists!", simulation_res_dir
        )
    ##########################################################################
    # EVALUATE RESULTS
    ##########################################################################
    logging.info("Import results for result-ID '%s'", param["ResId"])
    results_dict = {}
    # try to import getdp parameters from param dict
    # TODO: Add start and stop angle, angle and time step, ...
    # OTHER OPTION: Just add input param dict to result dict...
    for key, getdp_param in {
        "id": "ID_RMS",
        "iq": "IQ_RMS",
        "speed": "RPM",
    }.items():
        try:
            results_dict[key] = param["getdp"][getdp_param]
        except KeyError:
            pass
        except Exception as exce:
            raise exce
    # 1. Phase currents
    results_dict["current"] = {}
    for index in "abc":
        res_file = os.path.join(simulation_res_dir, f"I{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            results_dict["time"], results_dict["current"][index] = (
                readTimeTableDat(res_file)
            )
        else:
            # Error because we need to import time here!
            raise FileNotFoundError(
                f"Could not find result file for phase current I{index}"
            )

    # 2. Torque Results
    results_dict["torque"] = {}
    results_dict["torque_vw"] = {}
    for side in ["rotor", "stator"]:
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque"][side] = readTimeTableDat(res_file)
        # Virtual Work results
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}_vw.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque_vw"][side] = readTimeTableDat(res_file)

    # 3. Flux results
    results_dict["flux"] = {}
    for index in "abcdq0":
        res_file = os.path.join(simulation_res_dir, f"Flux_{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            time, results_dict["flux"][index] = readTimeTableDat(res_file)

    # 4. Induced voltage
    results_dict["inducedVoltage"] = {}
    for index in "ABC":
        res_file = os.path.join(
            simulation_res_dir, f"InducedVoltage{index}.dat"
        )
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["inducedVoltage"][index] = readTimeTableDat(
                res_file
            )

    # 5. Rotor position
    res_file = os.path.join(simulation_res_dir, "RotorPos_deg.dat")
    if os.path.isfile(res_file):
        # get first char in machine side to index rotor and stator results
        _, results_dict["rotorPos"] = readTimeTableDat(res_file)

    # 6. Core loss
    # Check if file hystLoss_rotor.dat allready exists -> loss allready calculated
    core_loss_dict = {}
    if not os.path.exists(
        os.path.join(simulation_res_dir, "hystLoss_rotor.dat")
    ):
        if post_operations is not None:
            # calculate core loss
            totalLoss = 0
            for _, side in enumerate(["rotor", "stator"]):
                bFilePath = os.path.join(simulation_res_dir, f"b_{side}.pos")
                lossDict, time = calcIronLoss.main(
                    bFilePath,
                    loss_factor={
                        "hyst": param["hyst"],
                        "eddy": param["eddy"],
                        "exc": param["exc"],
                    },
                    sym_factor=param["sym"],
                    axial_length=param["axLen"],
                )
                totalLoss += sum(lossDict.values())
                # print(f"Iron losses for {paramDict['ResId']} on {side} are: {lossDict}")

                # save to file:
                for loss_type, loss_data in lossDict.items():
                    core_loss_res_file = os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                    calcIronLoss.write_simple(
                        core_loss_res_file, time, loss_data
                    )
                    # with open(ironLossResFile, mode="w+", encoding="utf-8") as file:
                    #     lossDataJSON = json.dumps(ironLossDictList, indent=3)
                    #     file.write(lossDataJSON)
                core_loss_dict[side] = lossDict
    else:
        logging.warning(
            "Iron losses for %s have allready been calculated.\nImporting values...",
            param["ResId"],
        )
        for side in ["rotor", "stator"]:
            core_loss_dict[side] = {}
            for loss_type in ("hyst", "eddy", "exc"):
                time, core_loss_dict[side][loss_type] = readTimeTableDat(
                    os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                )
    if core_loss_dict:
        results_dict["coreLoss"] = core_loss_dict
        # pylint: disable=locally-disabled, logging-not-lazy, logging-fstring-interpolation, line-too-long
        logging.debug("Iron loss for '" + param["ResId"] + "'")
        logging.debug(f"{'Rotor':>24} {'Stator':>11} {'Gesamt':>11}")
        logging.debug(
            f"{'Hysteresis:':<14} {np.mean(core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['stator']['hyst']+core_loss_dict['rotor']['hyst']) : 9.3f} W"
        )
        logging.debug(
            f"{'Eddy Current:':<14} {np.mean(core_loss_dict['rotor']['eddy']) : 8.3f} W {np.mean(core_loss_dict['stator']['eddy']) : 9.3f} W {np.mean(core_loss_dict['stator']['eddy']+core_loss_dict['rotor']['eddy']) : 9.3f} W"
        )
        logging.debug(
            f"{'Excess:':<14} {np.mean(core_loss_dict['rotor']['exc']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']) : 9.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['rotor']['exc']) : 9.3f} W"
        )
        logging.debug(
            "---------------------------------------------------------------------"
        )
        logging.debug(
            f"{'Summe:':<14} {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']+core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W"
        )
    return results_dict


def main() -> None:
    # print("running main() of runOnelab.")
    # 1. Check that all argvs are valid!
    parser = ArgumentParser(
        description="Open the given Onelab file with gmsh."
    )

    parser.add_argument(
        "onelabFile",
        help="path to the file that should be processed",
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
        "--gui",
        help="flag to decide if the file should be opened in the gui or command line. Defaults to False if flag is not mentioned",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()
    # check if gmsh was provided
    if not args.gmsh:
        # if not provided find gmsh
        args.gmsh = findGmsh()
    else:
        # if provided check if its a correct file
        if not isfile(args.gmsh):
            raise (
                FileNotFoundError(
                    f"Provided gmsh executable was not found: {args.gmsh}"
                )
            )

    command = createCmdCommand(
        args.onelabFile,
        useGUI=args.gui,
        gmshPath=args.gmsh,
        getdpPath=args.getdp,
    )
    subprocess.run(command, check=False)


if __name__ == "__main__":
    main()
