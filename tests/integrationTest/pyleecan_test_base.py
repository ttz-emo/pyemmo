#
# Copyright (c) 2018-2024 M. Schuler & Vu Nguyen, TTZ-EMO,
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
"""
This module runs the Pyleecan API simulation for selected machines, and create
a tuple of result directories for use in testing. It can be expanded to support
other types of tests. Running this module by itself will create base data for
comparison in the actual tests.
"""

# from __future__ import absolute_import


import logging
import os
import sys
from datetime import datetime
from subprocess import PIPE, Popen
from typing import List, Mapping, Tuple

import pytest
from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import createCmdCommand, log_subprocess_output
from pyemmo.script.script import Script

# logic to add local path to beginning of sys path
path_temp = []
for path in sys.path:
    if path == ROOT_DIR:
        path_temp.append(path)
        break
for path in sys.path:
    if path == ROOT_DIR:
        continue
    else:
        path_temp.append(path)
sys.path = path_temp

from .. import GETDP_EXE, GMSH_EXE
from . import LOGGER

# from .testUtils import make_test_cases


test_params = {
    "api\\pyleecan": {
        "id": -10,
        "iq": 50,
        "rpm": 1000,
        "d_theta": 0.25,
        "test_data_folder": "tests\\data",
        "result_folder": "tests\\results",
    }
}


def pyleecan_test_base(
    test_params: list,
    result_path: str = "",
    test_data_path: str = "",
    test_type: str = "",
    test_id: int = 0,
    test_case: str = "",
    print_flag: bool = 0,
    debug_flag: bool = 0,
):
    """
    Base test data prepper for Pyleecan API workflow test.
    When running this file as stand alone e.g. for preparing base data,
    result_path should be path to desired base data locations.
    The following params are used in case running this alone e.g. for preparing
    base data.

    Args:
        test_params (dict): Contains parameter for running test
        result_path (str): Path where result should be stored, default empty
            (so that timestamped folder can be generated)
        test_data_path (str): Path where json data for testing can be found
            Defaults to "", so that data path from test_params will be used.
        test_type (str): type of test, default empty
        test_id (int): test id, default 0
        test_case (str): test case name, same as machine name, default empty
        print_flag (int): default 0
        debug_flag (int): default 0
    """

    # disable messages of matplotlib
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    # logging.getLogger("matplotlib.colormaps").setLevel(logging.ERROR)
    # logging.getLogger("numpy").setLevel(logging.ERROR)
    logging.getLogger().setLevel(logging.DEBUG)

    # create machine
    if test_data_path == "":
        machine_file_path = os.path.join(
            ROOT_DIR,
            test_params["test_data_folder"],
            f"{test_type}\\{test_case}.json",
        )
    else:
        machine_file_path = test_data_path
    LOGGER.info("Path of actual machine file is %s", machine_file_path)
    # pylint: disable=locally-disabled, no-member
    pyleecan_machine: Machine = load.load(machine_file_path)

    CuMat = load.load(os.path.join(DATA_DIR, "Material", "Copper2.json"))
    try:
        if pyleecan_machine.rotor.winding.conductor.cond_mat.name == "Copper1":
            pyleecan_machine.rotor.winding.conductor.cond_mat = CuMat
    except AttributeError:
        pass
    except Exception as exce:
        raise exce
    try:
        if pyleecan_machine.stator.winding.conductor.cond_mat.name == "Copper1":
            pyleecan_machine.stator.winding.conductor.cond_mat = CuMat
    except AttributeError:
        pass
    except Exception as exce:
        raise exce

    # Create result folder
    if result_path == "":
        curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        resFolder = os.path.join(
            ROOT_DIR,
            test_params["result_folder"],
            test_type,
            curr_datetime,
            f"test_{test_id}\\{test_case}",
        )
        if not os.path.isdir(resFolder):
            os.makedirs(resFolder)
    else:
        resFolder = result_path

    # Run simulation
    LOGGER.info("Running Pyleecan API for machine: %s", test_case)
    pyemmo_script: Script = pyleecanAPI.main(
        pyleecan_machine, model_dir=resFolder, use_gui=False
    )
    # geo_file = pyemmo_script.geoFilePath # Seems to be redundant
    pro_file = pyemmo_script.proFilePath

    sim_res_dir = pyemmo_script.resultsPath
    if not os.path.isdir(sim_res_dir):
        os.makedirs(sim_res_dir)

    i_d = test_params["id"]
    i_q = test_params["iq"]
    n = test_params["rpm"]
    resid = f"id_{i_d}_iq_{i_q}_n_{n}rpm"
    param_dict = {
        "getdp": {
            "ID_RMS": i_d,
            "IQ_RMS": i_q,
            "RPM": n,
            "d_theta": test_params["d_theta"],
            "ResId": resid,
            "Flag_PrintFields": print_flag,
            "Flag_Debug": debug_flag,
            "verbosity level": 3,
        },
        "ResId": resid,
        "pro": pro_file,
        "res": sim_res_dir,
        # "exe": findGetDP(),
        # "exe": r"H:\onelab-Windows64\getdp.exe",
        "exe": GETDP_EXE,
        "gmsh": GMSH_EXE,
        # "exe": GETDP_EXE,
        # "gmsh": GMSH_EXE,
    }
    # runCalcforCurrent(param_dict)
    cmdCommand = createCmdCommand(
        pro_file,
        useGUI=False,
        gmshPath=param_dict["gmsh"],
        getdpPath=param_dict["exe"],
        paramDict=param_dict["getdp"],
    )

    LOGGER.debug("cmd command is: %s", cmdCommand)
    LOGGER.info("Running simulation for result-ID '%s'", resid)
    # with Popen(cmdCommand, stdout=PIPE, stderr=STDOUT) as process:
    with Popen(cmdCommand, stdout=PIPE, stderr=PIPE) as process:
        with process:
            error_message = log_subprocess_output(process.stdout, process.stderr)
        exitcode = process.wait()  # 0 means success
        if exitcode != 0:
            raise RuntimeError(
                "Simulation for machine '%s' failed due to:\n\t%s"
                % (pyleecan_machine.name, error_message)
            )
    return pyemmo_script


def pyleecanPrepTuple(
    test_cases: Mapping[str, List[Tuple[str, str, bool]]], test_type: str
):
    """
    This function generates test paramemters for Pyleecan API testing.
    It basically generate test data folders and return the list of folders as
    a tuple for use in test cases.

    Args:
        test_cases (dict[list[tuple]]): list of test case names
        test_type (str): type of test performed
    Returns:
        list[tuple]: list of test data tuples with headers as first element.
        Headers (str) are:
        - test_id
        - test_case
        - source_path
        - result_path
        - simul_path
        - simul_subfolder_path
        - base_result_path
        - base_simul_path
        - base_simul_subfolder_path

    """
    # rootLogger.setLevel(logging.DEBUG)
    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    header_flg = True
    param_tuples = []
    result_path_all = os.path.join(
        ROOT_DIR,
        test_params[test_type]["result_folder"],
        test_type,
        curr_datetime,
    )
    if not os.path.isdir(result_path_all):
        os.makedirs(result_path_all)
    log_file = open(os.path.join(result_path_all, f"simulation.log"), "w+")
    log_file.write(f"Pyleecan API simulation log on {curr_datetime}\n")

    for test_id, test_case, machine_works in test_cases[test_type][1:]:
        # curr_datetime, _ = updateConfig(test_type, test_id, test_case) #REDUNDANT since API level log already exists in each folder

        # preparing source and result folders
        source_path = os.path.join(
            ROOT_DIR,
            test_params[test_type]["test_data_folder"],
            test_type,
            f"{test_case}.json",
        )

        # make sure source file exists -> REDUNDANT since test cases are created from test data folder content.
        # assert os.path.isfile(source_path) and messagePrinter("SUCCESS: Source file exist"), "ERROR: Source file does not exist"

        result_path = os.path.join(
            result_path_all,
            f"test_{test_id}_{test_case}",
        )
        if not os.path.isdir(result_path):
            os.makedirs(result_path)

        # this can change to a different folder for base data:
        base_result_path = os.path.join(
            ROOT_DIR,
            test_params[test_type]["test_data_folder"],
            test_type,
            "comparison_base",
            test_case,
        )
        if test_type == "api\\pyleecan" and machine_works:
            try:
                pyemmo_script: Script = pyleecan_test_base(
                    test_params[test_type],
                    result_path=result_path,
                    test_data_path=source_path,
                    test_case=test_case,
                    test_id=test_id,
                )
                log_file.write(f"Simulation successful for {test_case}.json\n")

            except RuntimeError as err:
                LOGGER.warning(f"{err.__str__()}, cannot start tests for {test_case}")
                log_file.write(
                    f"{err.__str__()}, cannot start tests for {test_case}.json\n"
                )

            except Exception as exce:
                LOGGER.warning(
                    f"test for {test_case} failed. exce.args[0]: " + exce.args[0]
                )
                log_file.write(
                    f"test for {test_case} failed. exce.args[0]: " + exce.args[0] + "\n"
                )
            # simul_path = pyemmo_script.resultsPath
            simul_path = [
                os.path.join(result_path, dir)
                for dir in os.listdir(result_path)
                if os.path.isdir(os.path.join(result_path, dir)) and "res_" in dir
            ][0]
            # simul_folder = simul_path.split("/")[-1]
            simul_folder = simul_path.split("\\")[-1]
            simul_subfolder = (
                f"id_{test_params[test_type]['id']}_"
                + f"iq_{test_params[test_type]['iq']}_"
                + f"n_{test_params[test_type]['rpm']}rpm"
            )
            simul_subfolder_path = os.path.join(simul_path, simul_subfolder)
            base_simul_path = os.path.join(
                base_result_path, simul_folder
            )  # This can also change for another base data folder
            base_simul_subfolder_path = os.path.join(
                base_simul_path, simul_subfolder
            )  # This can also change for another base data folder
            if header_flg:
                headers = "test_id, test_case, source_path, result_path, simul_path, simul_subfolder_path, base_result_path, base_simul_path, base_simul_subfolder_path"
                param_tuples = param_tuples + [headers]
                header_flg = False

            param_tuples = param_tuples + [
                pytest.param(
                    test_id,
                    test_case,
                    source_path,
                    result_path,
                    simul_path,
                    simul_subfolder_path,
                    base_result_path,
                    base_simul_path,
                    base_simul_subfolder_path,
                )
            ]
        elif not machine_works:
            if header_flg:
                headers = "test_id, test_case, source_path, result_path, simul_path, simul_subfolder_path, base_result_path, base_simul_path, base_simul_subfolder_path"
                param_tuples = param_tuples + [headers]
                header_flg = False
            param_tuples = param_tuples + [
                pytest.param(
                    test_id,
                    test_case,
                    source_path,
                    result_path,
                    "",
                    "",
                    "",
                    "",
                    "",
                    marks=pytest.mark.xfail(),
                )
            ]
        else:
            continue

    log_file.close()

    return param_tuples


def write_error_to_log(log_file, test_case, error_class):
    if hasattr(error_class, "message"):
        log_file.write(
            f"{type(error_class).__name__} in {test_case}: {error_class.message}\n"
        )
    else:
        log_file.write(f"{type(error_class).__name__} in {test_case}\n")


if __name__ == "__main__":
    # ONLY RUN THIS BY ITSELF IF YOU WANT TO CREATE BASE DATA
    import shutil
    from distutils.dir_util import copy_tree

    test_type = "api\\pyleecan"
    test_cases = [
        ("test_id", "test_case"),
        (0, "IPMSM_B"),
        (1, "SPMSM_002"),
        (2, "SPMSM_003"),
        (3, "Toyota_Prius"),
    ]
    # test_cases = make_test_cases(test_type)
    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ROOT_DIR, f"workingDirectory\\Vu\\for_testing\\{curr_datetime}"
    result_path = os.path.join(
        ROOT_DIR,
        test_params[test_type]["test_data_folder"],
        test_type,
        "comparison_base",
    )
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    # Backup existing data
    backup_path = os.path.join(result_path, "backup")

    log_file_path = os.path.join(result_path, "base_data_creation.log")
    if not os.path.isfile(log_file_path):
        log_file = open(log_file_path, "w")
    else:
        log_file = open(log_file_path, "a")
        log_file.write("\n")

    log_file.write(f"Base data creation on {curr_datetime}\n")

    for tup in test_cases[1:]:
        test_id, test_case = tup
        result_path_true = os.path.join(result_path, test_case)
        backup_path_true = os.path.join(backup_path, test_case)

        # copy existing base as new backup, and cleanup base result folder
        if os.path.isdir(result_path_true):
            # remove existing backup
            if os.path.isdir(backup_path_true):
                shutil.rmtree(backup_path_true)
                os.makedirs(backup_path_true)
            else:
                os.makedirs(backup_path_true)
            copy_tree(result_path_true, backup_path_true)
            shutil.rmtree(result_path_true)

        # create base data
        try:
            pyleecan_test_base(
                test_params[test_type],
                result_path=result_path_true,
                test_type=test_type,
                test_id=test_id,
                test_case=test_case,
            )
            log_file.write(f"Successfully created base data for {test_case}\n")
        except Exception as exce:
            log_file.write(f"{type(exce).__name__} in {test_case}: {exce.__str__()}\n")
    log_file.close()
