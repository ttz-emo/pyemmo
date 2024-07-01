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
"""TODO: Module docstring"""

import os
import logging
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from pyleecan.Functions import load
from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR

from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo import rootLogger

from pyemmo.functions.runOnelab import (
    runCalcforCurrent,
    findGmsh,
    findGetDP,
    createCmdCommand,
    log_subprocess_output,
)
from datetime import datetime
from pyemmo.script.script import Script
from tests import GETDP_EXE, GMSH_EXE
from testUtils import make_test_cases

test_cases = {
    0: "Toyota_Prius",
}

test_params = {
    "api\\pyleecan": {
        "id": -10,
        "iq": 50,
        "rpm": 1000,
        "d_theta": 0.25,
        "test_data_folder": "tests\\data",
        "result_folder": "tests\\results",
        # "result_folder": "Results\\pyleecanAPI",
    }
}

test_type = "api\\pyleecan"


def pyleecanPrepTuple(test_cases, test_type):
    """
    Testing pyleecan API to generate GMSH and simulation files based on pyleecan machine json files.
    There are 4 test points included:
        - Check that simulation folders and subfolders are properly generated
        - Check that GMSH and GetDP files are properly generated
        - Check that simulation folders and files are generated
        - Check that content of result file match base comparison data

    """
    # test_type = "api\\pyleecan"
    # self.make_test_cases(test_type)
    # self.test_cases[test_type] = make_test_cases(test_type)
    # result_path = defaultdict(list)
    # simul_path = defaultdict(list)
    # simul_subfolder_path = defaultdict(list)
    rootLogger.setLevel(logging.DEBUG)
    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    header_flg = True
    param_tuples = list()

    # print("========TEST PYLEECAN API + SIMULATION FLOW START========")
    for test_id, test_case in test_cases[test_type][1:]:
        # curr_datetime, _ = updateConfig(test_type, test_id, test_case) #REDUNDANT since API level log already exists in each folder

        # preparing source and result folders
        source_path = os.path.join(
            ROOT_DIR,
            test_params[test_type]["test_data_folder"],
            f"{test_type}\\{test_case}.json",
        )

        # make sure source file exists -> REDUNDANT since test cases are created from test data folder content.
        # assert os.path.isfile(source_path) and messagePrinter("SUCCESS: Source file exist"), "ERROR: Source file does not exist"

        result_path = os.path.join(
            ROOT_DIR,
            test_params[test_type]["result_folder"],
            f"{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}",
        )
        if not os.path.isdir(result_path):
            os.makedirs(result_path)
        base_result_path = os.path.join(
            ROOT_DIR,
            test_params[test_type]["test_data_folder"],
            test_type,
            f"comparison_base\\{test_case}",
        )  # this can change to a different folder for base data

        if test_type == "api\\pyleecan":
            simul_path = os.path.join(result_path, f"res_{test_case}")
            simul_subfolder = f"id_{test_params[test_type]['id']}_iq_{test_params[test_type]['iq']}_n_{test_params[test_type]['rpm']}rpm"
            simul_subfolder_path = os.path.join(simul_path, simul_subfolder)
            base_simul_path = os.path.join(
                base_result_path, f"res_{test_case}"
            )  # This can also change for another base data folder
            base_simul_subfolder_path = os.path.join(
                base_simul_path, simul_subfolder
            )  # This can also change for another base data folder
            if header_flg:
                headers = "test_id, test_case, source_path, result_path, simul_path, simul_subfolder_path, base_result_path, base_simul_path, base_simul_subfolder_path"
                param_tuples = param_tuples + [headers]
                header_flg = False

            param_tuples = param_tuples + [
                (
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

        else:
            continue

    return param_tuples


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
    Params:
    - test_params: Containt parameter dict for running test
    - result_path: string path where result should be stored
    - test_data_path: string path where json data for testing can be found
    - test_data_path: string path where json data for testing can be found
    The following params are used in case running this alone e.g. for preparing base data:
    - test_type: type of test, default empty
    - test_id: test id, default empty
    - test_case: test case name, same as machine name, default empty
    - print_flag: default 0
    - debug_flag: default 0
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
        machine_file_path = os.path.join(
            ROOT_DIR,
            test_params["test_data_folder"],
            f"{test_type}\\{test_case}.json",
        )
    else:
        machine_file_path = test_data_path
    print(machine_file_path)
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
        if (
            pyleecan_machine.stator.winding.conductor.cond_mat.name
            == "Copper1"
        ):
            if (
                pyleecan_machine.stator.winding.conductor.cond_mat.name
                == "Copper1"
            ):
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
            f"{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}",
        )
        resFolder = os.path.join(
            ROOT_DIR,
            test_params["result_folder"],
            f"{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}",
        )
        if not os.path.isdir(resFolder):
            os.makedirs(resFolder)
    else:
        resFolder = result_path

    # Run simulation
    pyemmo_script: Script = pyleecanAPI.main(
        pyleecan_machine, model_dir=resFolder, use_gui=False
    )
    # geo_file = pyemmo_script.geoFilePath
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
        },
        "ResId": resid,
        "pro": pro_file,
        "res": sim_res_dir,
        # "exe": findGetDP(),
        # "exe": r"H:\onelab-Windows64\getdp.exe",
        "exe": GETDP_EXE,
        "gmsh": GMSH_EXE,
    }
    # runCalcforCurrent(param_dict)
    cmdCommand = createCmdCommand(
        pro_file,
        useGUI=False,
        gmshPath=param_dict["gmsh"],
        getdpPath=param_dict["exe"],
        paramDict=param_dict["getdp"],
    )

    logging.debug("cmd command is: %s", cmdCommand)
    logging.info("Running simulation for result-ID '%s'", resid)
    with Popen(cmdCommand, stdout=PIPE, stderr=STDOUT) as process:
        with process.stdout:
            log_subprocess_output(process.stdout)
        exitcode = process.wait()  # 0 means success
        if exitcode != 0:
            raise RuntimeError(
                f"Simulation for machine '{pyleecan_machine.name}' failed!"
            )

    return machine_file_path, resFolder


if __name__ == "__main__":
    # from integrationTest.apiTest import TestCases

    test_cases = make_test_cases("api\\pyleecan")
    print(type(test_cases[1]))
    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    result_path = os.path.join(
        ROOT_DIR, f"workingDirectory\\Vu\\for_testing\\{curr_datetime}"
    )
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    file = open(os.path.join(result_path, "base_data_creation_log"), "w")

    for tup in test_cases[1:]:
        # print(test_case, ": ",os.path.isfile(os.path.join(ROOT_DIR, test_params[test_type]["test_data_folder"], f"{test_type}\\{test_case}.json")))
        # print("\n")
        test_id, test_case = tup
        result_path_true = os.path.join(result_path, test_case)
        try:
            pyleecan_test_base(
                test_params[test_type],
                result_path=result_path_true,
                test_type=test_type,
                test_id=test_id,
                test_case=test_case,
            )
        except AttributeError:
            file.write(f"Attribute error in {test_case}\n")
            pass
        except RuntimeError:
            print(f"Runtime error in {test_case}\n")
            pass
        except ValueError:
            print(f"Value error in {test_case}\n")
            pass
        except FileNotFoundError:
            print(f"FileNotFoundError in {test_case}\n")
            pass
    file.close()
    # print(os.path.join(os.path.abspath('.'), "pytest.ini"))
