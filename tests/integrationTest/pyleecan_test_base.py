import os
import logging
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from pyleecan.Functions import load
from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR

from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.functions.runOnelab import (
    findGmsh,
    findGetDP,
    createCmdCommand,
    log_subprocess_output,
)


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
        "result_folder": "Results\\pyleecanAPI",
    }
}

test_type = "api\\pyleecan"


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
        if not os.path.isdir(resFolder):
            os.makedirs(resFolder)
    else:
        resFolder = result_path

    # Run simulation
    pyleecanAPI.main(pyleecan_machine, model_dir=resFolder, use_gui=False)
    geo_file = os.path.join(resFolder, pyleecan_machine.name + ".geo")
    pro_file = os.path.join(resFolder, pyleecan_machine.name + ".pro")

    sim_res_dir = os.path.join(resFolder, f"res_{pyleecan_machine.name}")
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
        "exe": findGetDP(),  # r"H:\onelab-Windows64\getdp.exe",  # FIXME: Remove hardcoded exe
        "gmsh": findGmsh(),
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
    from test_pytest import TestCases

    new_test = TestCases()

    test_cases = new_test.make_test_cases("api\\pyleecan")[test_type]

    result_path = os.path.join(ROOT_DIR, "workingDirectory\\Vu\\for_testing")
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    file = open(os.path.join(result_path, "base_data_creation_log"), "w")

    for test_id, test_case in test_cases.items():
        # print(test_case, ": ",os.path.isfile(os.path.join(ROOT_DIR, test_params[test_type]["test_data_folder"], f"{test_type}\\{test_case}.json")))
        # print("\n")
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
