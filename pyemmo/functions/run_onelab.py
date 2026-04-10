#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
"""You can use the run_onelab module to run ONELAB from the command line.

.. code-block:: text

    usage: run_onelab.py [-h] [--gmsh GMSH] [--getdp GETDP] [--gui] file

    Open the given Onelab file with gmsh.

    positional arguments:
    file           path to the file that should be processed

    options:
    -h, --help     show this help message and exit
    --gmsh GMSH    path to the Gmsh executable
    --getdp GETDP  path to the GetDP executable
    --gui          flag to decide if the file should be opened in the gui or command line. Defaults to False if flag is not mentioned


Example
-------
To open the file `my_file.geo` in the gmsh GUI you can run:

.. code-block:: bash

    python -m pyemmo.functions.run_onelab my_file.geo --gmsh /path/to/gmsh --gui


"""
from __future__ import annotations

import json
import logging
import os
import platform
import subprocess
import sys
import time as time_module
import warnings
from argparse import ArgumentParser
from io import BufferedReader
from os.path import expanduser, isdir, isfile, join, normpath, splitext
from shutil import which
from subprocess import PIPE, STDOUT, Popen

import numpy as np

from . import RES_FILE_NAME, SETUP_FILE_NAME, core_loss, import_results


class NumpyEncoder(json.JSONEncoder):
    """Numpy Encoder class to read and write numpy arrays to json"""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def log_subprocess_output(pipe: BufferedReader, stderr: BufferedReader = None):
    """Function to redirect commandline output to Python logger.
    Took this from answer in https://stackoverflow.com/a/21978778
    """
    logger = logging.getLogger(__name__)
    err_msg = ""
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        logger.info(line.rstrip(b"\n").decode("UTF-8"))
    if stderr:
        for line in iter(stderr.readline, b""):
            line = line.rstrip(b"\n").decode("UTF-8")
            if "Error" in line:
                # err_msg += str(line)
                err_msg += "\t" + line.replace("\r\n", "") + "\n"
                logger.error("%s", line)
            elif "Warning" in str(line):
                logger.warning("%s", line)
            else:
                logger.info("%s", line)
    return err_msg


def find_gmsh(verbosity: bool = True) -> str:
    """Find gmsh executable on maschine"""
    gmshExe = find_exe("gmsh", verbosity=verbosity)
    return gmshExe


def findGmsh(verbosity: bool = True) -> str:
    """Old find gmsh executable on maschine

    :meta private:
    """
    warnings.warn("The 'findGmsh' function was renamed find_gmsh!", DeprecationWarning)
    # TODO: Remove in pyemmo 1.6
    return find_gmsh(verbosity)


def find_getdp(verbosity: bool = True) -> str:
    """Find getdp executable on maschine"""
    getdpExe = find_exe("getdp", verbosity=verbosity)
    return getdpExe


def findGetDP(verbosity: bool = True) -> str:
    """Old find GetDP executable on maschine

    :meta private:
    """
    warnings.warn("The 'findGetDP' function was renamed find_gmsh!", DeprecationWarning)
    # TODO: Remove in pyemmo 1.6
    return find_getdp(verbosity)


def find_exe(exe_name: str, verbosity: bool = True) -> str:
    """Search the local machine for the executalble given in exeName.
    There are several searching stages and the function returns the exe path if
    one stage gives a result:

        1. search with "which" command
        2. search the python path
        3. search the "User/appdate/local/programs" path

    TODO:

        Search "C:/Program Files" path

    Args:
        exe_name (str): name of the executable. E.g. "myExe.exe" or just "myExe"
        verbosity (bool): Print additional information to the command line if
            True. Defaults to True.

    Raises:
        SystemError: If not run on Windows and program not found using which and path.
        FileNotFoundError: If the exe is not found.

    Returns:
        str: filepath to the executable
    """
    logger = logging.getLogger(__name__)
    exe_name, _ = splitext(exe_name)
    # first opion: try to find gmsh with "which"
    exe_path = which(exe_name)
    if exe_path:
        logger.debug("Found %s in '%s'!", exe_name, exe_path)
        return exe_path
    logger.debug(
        "Could not find %s from command line. Trying to find it in python-path...",
        exe_name,
    )
    # second option: try to find gmsh in python path. (Should work since gmsh python
    # module is installed!)
    for path in sys.path:
        if isdir(path):
            for file in os.listdir(path):
                if file == f"{exe_name}.exe":
                    exe_path = join(path, file)
                    logger.debug("Found %s in '%s'!", exe_name, exe_path)
                    return exe_path

    logger.debug(
        "%s was not found in 'path' Variable. Trying to find it in user home directory."
        "This can take some time!",
        exe_name,
    )
    # third option: try to find {executableName} in user/local/programs
    # and subfolders. Takes time to iterate through all files
    if platform.system() == "Windows":
        # is system windows; user-program-path:
        user_dir = normpath(join(expanduser("~"), "appdata", "local", "programs"))
        # try to find {executableName} in user programm path
        if isdir(user_dir):
            for root, _, files in os.walk(user_dir):
                if files == f"{exe_name}.exe":
                    logger.debug("Found %s in '%s'! :)", exe_name, root)
                    return join(root, f"{exe_name}.exe")
            # if exe was not found in home dir
            logger.debug(
                "%s could not be found in home program folder '%s'", exe_name, user_dir
            )
        else:
            logger.debug(
                "Windows user programs directory '%s' does not exist...", user_dir
            )
    elif platform.system() == "Linux":
        # is system windows; user-program-path:
        user_dir = normpath(join(expanduser("~"), ""))
        # try to find {executableName} in user programm path
        if isdir(user_dir):
            for root, _, files in os.walk(user_dir):
                if files == f"{exe_name}.exe":
                    logger.debug("Found %s in '%s'! :)", exe_name, root)
                    return join(root, f"{exe_name}.exe")
            # if exe was not found in home dir
            logger.debug(
                "%s could not be found in home program folder '%s'", exe_name, user_dir
            )
        else:
            logger.debug("Windows home directory '%s' does not exist...", user_dir)
    else:
        raise SystemError(
            f"Platform is {platform.system()}, not 'Windows' or 'Linux'. "
            "Could not find home directory."
        )
    if not exe_path:
        raise FileNotFoundError(
            f"Can not find {exe_name} on your system! "
            f"Give the path to the executable manually or install {exe_name} and set "
            "your systems PATH variable."
        )


def findExe(exeName: str, verbosity: bool = True) -> str:
    """Old function def to find exe on maschine

    :meta private:
    """
    warnings.warn("The 'findExe' function was renamed find_exe!", DeprecationWarning)
    # TODO: Remove in pyemmo 1.6
    return find_exe(exeName, verbosity)


# pylint: disable=locally-disabled, dangerous-default-value
def create_command(
    file: str,
    useGUI: bool,
    gmsh_path: str | os.PathLike = "",
    getdp_path: str | os.PathLike = "",
    log_file: str | os.PathLike = "",
    params: dict[str, str | int | float] = {},
    postops: list[str] = [],
) -> str:
    """Create a command line command to open a .geo or .pro file with the gmsh gui or
    run gmsh and getdp from the command line.

    Args:
        file (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui
            (independed if its a geo or pro file).
        gmsh_path (str): Path to the gmsh executable. By defaults the gmsh exe
            is searched.
        getdp_path (str, optional): path to a getdp executable. Path will only
            be used if gui is not used. Defaults to "".
        log_file (str, optional): Provide a log file name if the simulation
            procedure should be saved to a file. Defaults to "".
        params (Dict[str, Union[str, int, float]], optional): Dict with parameters
            to set in the simulation. Defaults to None. You can use the value "verbosity
            level" to change verbosity in GetDP from 0 to 99.

                E.g. to set the onelab parameter "IQ_RMS" for the quadrature
                rms current to 10A the dict would look like:

                .. code:: python

                    {
                        "IQ_RMS": 10,
                    }

        postops (List[str], optional): List containing the PostOperation
            names that should be performed after the solving stage.
            PostOperations will only be executed if a getdp executable is
            given!

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    gmsh_params = {}  # init gmsh parameter dict
    if "getdp" in params:
        # if param dict has "getdp" sub-dict
        getdp_params = params["getdp"].copy()
        if "gmsh" in params:
            #  if param dict has "gmsh" sub-dict
            gmsh_params = params["gmsh"].copy()
    else:
        # otherwise the paramDict is empty or only contains getdp parameters
        getdp_params = params.copy()

    # check if the onelab file is valid:
    if not isfile(file):
        raise FileNotFoundError(f"Provided Onelab file was not found: {file}")
    (filePath, ext) = splitext(file)
    # first part of the cmd command: open the geo or pro-file
    if not gmsh_path:
        gmsh_path = find_gmsh()
    gmsh_command = f'{gmsh_path} "{file}"'  # the command is: 'gmsh "FILE.xxx"'
    if ext.lower() == ".geo":
        # if its a geo file
        if not useGUI:
            # run onelab server in command line if gui is False. This does the meshing
            # and database generation.
            # TODO: Add general gmsh paramter to mesh generation call via gmsh parameter
            # dict
            gmsh_command += " -run"  # the command is: "gmsh FILE.geo -run"
            if log_file:
                gmsh_command += f" -log {log_file} "
        # else:
        #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
    elif ext.lower() == ".pro":
        getdp_command = ""
        if not useGUI:
            if getdp_path:
                # if command line and getdp specified
                # run the simulation with specific getdp exe
                getdp_command += f"""{getdp_path} "{file}" -solve Analysis"""
                # the command is: "getdp FILE.pro -solve Analysis"
                if "msh" in getdp_params:
                    if getdp_params["msh"] and not isfile(getdp_params["msh"]):
                        raise FileNotFoundError(
                            f"""Given msh file was not found: {getdp_params["msh"]}"""
                        )
                    # make sure file exists -> skip meshing
                    getdp_command += f" -msh {getdp_params['msh']}"
                    gmsh_command = ""  # reset gmsh command
                    # allways remove "msh" field for getdp param setting later
                    getdp_params.pop("msh")
                else:
                    # no "msh" key -> create mesh command
                    # TODO: Add gmsh paramter to mesh generation call
                    gmsh_command = f"""{gmsh_path} "{filePath}.geo" -run"""
                    # TODO: Check if the following should be used or not.
                    # if os.path.isfile(getdpPath):
                    #     # it getdp executable is given and exists, set internal solver
                    #     gmsh_command += (
                    #         f'-setstring Solver.Executable0 "{getdpPath}" '
                    #     )
                    #     gmsh_command += '-setstring Solver.Name0 "GetDP" '
                # # If log file name is given, add file logging flag:
                # if logFileName:
                #     gmsh_command += f" -log {logFileName} "
                # add post operations
                if postops:
                    getdp_command += " -pos "
                    # Using set() because it removes string duplicates automatically
                    for postOp in set(postops):
                        if not isinstance(postOp, str):
                            raise (
                                ValueError(
                                    "Given Post Operation name was not a string: "
                                    f"{type(postOp)}, {postOp}"
                                )
                            )
                        getdp_command += postOp + " "
            else:
                # only command line specified
                gmsh_command += " -run"  # just run "gmsh FILE.pro -run",
                # which auto-selects a getdp installation
        # else:
        # if gui was specified, just leave the command as it is:
        #   "gmsh FILE.pro" to open gui
    else:
        raise (
            ValueError(
                f"File '{file}' has wrong file extension (not '.geo'"
                " or '.pro') or is missing file extension: {ext}"
            )
        )
    if gmsh_params and gmsh_command != "":
        # if the paramDict is not empty or None
        if not isinstance(gmsh_params, dict):
            raise TypeError(
                f"Gmsh parameter dict was not a dict, but type '{type(gmsh_params)}.'"
            )
        # add verbosity if given
        if "verbosity level" in gmsh_params:
            if gmsh_command:
                gmsh_command += f" -v {gmsh_params.pop('verbosity level')}"
        for paramName, paramValue in gmsh_params.items():
            if paramName == "exe":
                continue  # skip exe
            if isinstance(paramValue, str):
                gmsh_command += f" -setstring {paramName} {paramValue}"
            elif isinstance(paramValue, bool):
                # convert bool to int!
                gmsh_command += f" -setnumber {paramName} {int(paramValue)}"
            elif isinstance(paramValue, (float, int)):
                gmsh_command += f" -setnumber {paramName} {paramValue}"
            else:
                raise (
                    TypeError(
                        "Parameter value was not string, float or "
                        f"int! -> {type(paramValue)}"
                    )
                )
    if getdp_params and getdp_command != "":
        # if the paramDict is not empty or None
        if not isinstance(getdp_params, dict):
            raise TypeError(
                f"Parameter dict was not a dict, but type '{type(getdp_params)}.'"
            )
        # add verbosity if given
        if "verbosity level" in getdp_params:
            getdp_command += f" -v {getdp_params.pop('verbosity level')}"
        for paramName, paramValue in getdp_params.items():
            if paramName == "exe":
                continue  # skip exe
            if isinstance(paramValue, str):
                getdp_command += f" -setstring {paramName} {paramValue}"
            elif isinstance(paramValue, bool):
                # convert bool to int!
                getdp_command += f" -setnumber {paramName} {int(paramValue)}"
            elif isinstance(paramValue, (float, int)):
                getdp_command += f" -setnumber {paramName} {paramValue}"
            else:
                raise (
                    TypeError(
                        "Parameter value was not string, float or "
                        f"int! -> {type(paramValue)}"
                    )
                )

    if gmsh_command and getdp_command:
        return gmsh_command + " && " + getdp_command
    if gmsh_command:
        return gmsh_command
    return getdp_command


def createCmdCommand(*args, **kwargs) -> str:
    """
    :meta private:
    """
    warnings.warn(
        "The 'createCmdCommand' function was renamed create_command!",
        DeprecationWarning,
    )
    # TODO: Remove in pyemmo 1.6
    return create_command(*args, **kwargs)


def create_gmsh_command(
    file: str,
    useGUI: bool,
    gmsh_path: str = "",
    log_file: str = "",
) -> str:
    """Create a cmd command to open a GMSH .geo file with the GUI or
    generate the mesh by running gmsh from the command line.

    Args:
        file (str): Path to the .geo or .pro file.
        useGUI (bool): If True command will open the file in the gmsh gui
            (independed if its a geo or pro file).
        gmsh_path (str): Path to the gmsh executable. By defaults the gmsh exe
            is searched.

            E.g. to set the onelab parameter "IQ_RMS" for the quadrature rms
            current to 10A the dict would look like:

            .. code:: python

                {
                    "IQ_RMS": 10,
                }
        log_file (str): Log file path to log gmsh output.

    Returns:
        str: string of the executable command-line command

    Raises:
        ValueError: If the file extension of onelabFile is not .geo or .pro.
        TypeError: If paramDict is not type dict.
        TypeError: If the parameter value is not str, float or int.
        FileNotFoundError: If onelabFile does not exist or is not a file.
    """
    if not gmsh_path:
        gmsh_path = find_gmsh()
    # check if the onelab file is valid:
    if not isfile(file):
        raise FileNotFoundError(f"Provided Onelab file was not found: {file}")
    (_, ext) = splitext(file)
    # first part of the cmd command: open the geo or pro-file
    command = f'{gmsh_path} "{file}"'  # the command is: 'gmsh "FILE.xxx"'
    if ext.lower() == ".geo":
        # if its a geo file
        if not useGUI:
            # run onelab server in command line if gui is False
            #   this does the meshing and database generation
            command += " -run"  # the command is: "gmsh FILE.geo -run"
            if log_file:
                command += f" -log {log_file} "
        # else:
        #   just leave the command as it is: "gmsh FILE.geo" to open gmsh GUI
    elif ext.lower() == ".pro":
        if not useGUI:
            # only command line specified
            command += " -run"  # just run "gmsh FILE.pro -run", which
            # auto-selects a getdp installation
        # else:
        # if gui was specified, just leave the command as it is:
        #   "gmsh FILE.pro" to open gui
    else:
        raise (
            ValueError(
                f"File '{file}' has wrong file extension (not '.geo' "
                f"or '.pro') or is missing file extension: {ext}"
            )
        )
    return command


def createGMSHCommand(*args, **kwargs) -> str:
    """
    :meta private:
    """
    warnings.warn(
        "The 'createGMSHCommand' function was renamed create_gmsh_command!",
        DeprecationWarning,
    )
    # TODO: Remove in pyemmo 1.6
    return create_gmsh_command(*args, **kwargs)


def run_simulation(param: dict) -> dict:
    """Function to run a getdp calculation based on parameter from param dict

    Args:
        param (dict): Parameter dict that looks like

    TODO: Show which parameter are not-optional and give hints for setting machine model
    parameters

    .. code-block:: python

        {
            "getdp": {
                "exe": findGetDP(), ##
                "ResId": res_id, ##
                "verbosity level": 3, #
                "res": self.test_sim_dir, ##

                "IQ_RMS": 10.0,
                "ID_RMS": 0.0,
                "RPM": 1000,
                "initrotor_pos": 0.0,
                "d_theta": 5,
                "finalrotor_pos": 15,
                "Flag_AnalysisType": 1,
                "Flag_PrintFields": 0,
                "Flag_Debug": 1,
                "Flag_ClearResults": 1,
                "stop_criterion": 1e-7,
            },
            "gmsh": {"exe": findGmsh()}, # gmsh exe and params ##
            "pro": join(self.model_dir, "Toyota_Prius.pro"), # pro file ##
            "info": "", #
            "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post" #
            "hyst": 102, # in combination with 'GetBIron' PostOp entry #
            "eddy": 1.5, #
            "datetime": time.ctime(), #
        }

    Returns:
        dict: Simulation results dict created from ``pyemmo.functions.import_results.main``
    """
    logger = logging.getLogger(__name__)
    # adding additional results path to GetDP parameters (only then GetDP knows where to
    # put the results) because its initally set in the parameter geo
    # file. But if the files are moved the results folder might not exist any more!
    RES_DIR = param["getdp"]["res"]
    if not os.path.isdir(RES_DIR):
        if os.path.isdir(os.path.dirname(RES_DIR)):
            logger.info("Creating results directory: %s", RES_DIR)
            os.mkdir(RES_DIR)
        else:
            raise RuntimeError(
                "Result directory does not exist and can not be created: " + RES_DIR
            )
    pro_file = param["pro"]
    # simulation_res_dir is the actual res folder joined from the global RES_DIR and
    # ResId (which is the folder name).
    simulation_res_dir = os.path.join(RES_DIR, param["getdp"]["ResId"])
    if "Flag_ClearResults" in param["getdp"] and os.path.isdir(simulation_res_dir):
        if param["getdp"]["Flag_ClearResults"]:
            logger.warning(
                "Removing previous results from folder: %s",
                simulation_res_dir,
            )
            for res_file in os.listdir(simulation_res_dir):
                os.remove(os.path.join(simulation_res_dir, res_file))
            os.rmdir(simulation_res_dir)

    post_operations = param["PostOp"] if "PostOp" in param else []

    if not os.path.isdir(simulation_res_dir):
        os.mkdir(simulation_res_dir)
        # only run if results dir for this simulation not exists
        # determine if core loss can be calculated
        if "hyst" in param and "eddy" in param and "GetBIron" not in post_operations:
            post_operations.append("GetBIron")  # calc core loss
        if "datetime" not in param:
            param["datetime"] = time_module.ctime()

        # save simulation setup to file
        setup_file_path = join(simulation_res_dir, SETUP_FILE_NAME)
        with open(setup_file_path, "x", encoding="utf-8") as setup_file:
            json.dump(param, setup_file)

        cmdCommand = create_command(
            pro_file,
            useGUI=False,
            gmsh_path=param["gmsh"]["exe"],
            getdp_path=param["getdp"]["exe"],
            params=param,
            postops=post_operations,
        )

        logger.debug("cmd command is: %s", cmdCommand)
        logger.info("Running simulation for result-ID '%s'", param["getdp"]["ResId"])

        ## TRY TO LOG OUTPUT OF FUNCTION CALL:
        # TODO: Add log file option and stream simulation to log file
        sim_log_file_handler = logging.FileHandler(
            os.path.join(simulation_res_dir, param["getdp"]["ResId"] + ".log"),
            encoding="utf-8",
        )
        logger.addHandler(sim_log_file_handler)
        process = Popen(
            cmdCommand,
            stdout=PIPE,
            stderr=STDOUT,
            # text=True,
        )
        with process.stdout:
            log_subprocess_output(process.stdout)
        exitcode = process.wait()  # 0 means success
        logger.info("Subprocess returned exit code %i", exitcode)
        logger.removeHandler(sim_log_file_handler)
        sim_log_file_handler.close()

    else:
        # Simulation with this resId has allready been done!
        logger.warning(
            "Result directory %s allready exists! Importing results...",
            simulation_res_dir,
        )

    # Calculate core loss
    # Check if file hystLoss_rotor.dat allready exists -> loss allready calculated
    # core_loss_dict = {}
    if not os.path.exists(os.path.join(simulation_res_dir, "hystLoss_rotor.dat")):
        if "GetBIron" in post_operations:
            # if B in core region was extracted -> calculate core loss
            totalLoss = 0
            for _, side in enumerate(["rotor", "stator"]):
                bFilePath = os.path.join(simulation_res_dir, f"b_{side}.pos")
                lossDict, time = core_loss.main(
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
                # save to file:
                for loss_type, loss_data in lossDict.items():
                    core_loss_res_file = os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                    core_loss.write_simple(core_loss_res_file, time, loss_data)
                    # with open(ironLossResFile, mode="w+", encoding="utf-8") as file:
                    #     lossDataJSON = json.dumps(ironLossDictList, indent=3)
                    #     file.write(lossDataJSON)
                # core_loss_dict[side] = lossDict
    # import default results:
    results_dict = import_results.main(param)

    try:  # to save results to json
        res_file_path = join(simulation_res_dir, RES_FILE_NAME)
        with open(res_file_path, "x", encoding="utf-8") as res_file:
            json.dump(results_dict, res_file, cls=NumpyEncoder, indent=4)
    except Exception as e:
        logger.warning("Could not save results to json file!", exc_info=e)

    return results_dict


def runCalcforCurrent(*args, **kwargs) -> str:
    """
    :meta private:
    """
    warnings.warn(
        "The 'runCalcforCurrent' function was renamed run_simulation!",
        DeprecationWarning,
    )
    # TODO: Remove in pyemmo 1.6
    return run_simulation(*args, **kwargs)


def main(
    file: str, use_gui: bool, gmsh="", getdp="", params={}
) -> subprocess.CompletedProcess:
    """Main function to open Gmsh GUI or run simulation.

    This uses :func:`create_command` to create a command call for gmsh or getdp and
    then starts a subprocess using that command.

    Args:
        file (str): GetDP or Gmsh input file.
        use_gui (_type_): Flag to open Gmsh GUI.
        gmsh (str, optional): Path to gmsh executable. If not given, try to find gmsh.
        getdp (str, optional): Path to GetDP executable. If not given, try to find getdp.
        params (dict, optional): Parameter dictionary for :func:`create_command`.
            Defaults to {}.

    Returns:
        subprocess.CompletedProcess: subprocess.CompletedProcess object.
    """
    command = create_command(
        file,
        useGUI=use_gui,
        gmsh_path=gmsh,
        getdp_path=getdp,
        params=params,
    )
    comp_process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        # shell=True # fixing bandit subprocess issue -> shell = False
    )
    return comp_process


if __name__ == "__main__":
    # print("running main() of run_onelab.")
    # 1. Check that all argvs are valid!
    parser = ArgumentParser(description="Open the given Onelab file with gmsh.")

    parser.add_argument(
        "file",
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
        help="flag to decide if the file should be opened in the gui or command line. "
        "Defaults to False if flag is not mentioned",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()
    # check if gmsh was provided
    if not args.gmsh:
        # if not provided find gmsh
        args.gmsh = find_gmsh()
    else:
        # if provided check if its a correct file
        if not isfile(args.gmsh):
            raise (
                FileNotFoundError(
                    f"Provided gmsh executable was not found: {args.gmsh}"
                )
            )
    main(args.onelabFile, args.gui, args.gmsh, args.getdp)
