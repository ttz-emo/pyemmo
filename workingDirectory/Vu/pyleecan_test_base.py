import os
import logging

from pyleecan.Functions import load
from pyleecan.Classes.Machine import Machine

from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan import main as pyleecanAPI

from pyemmo.functions.runOnelab import runCalcforCurrent, findGmsh, findGetDP
from datetime import datetime

test_cases = {
    1: "IPMSM_B",
}

test_params = {
    1: {
        "id": -10,
        "iq": 50,
        "rpm": 1000,
        "d_theta": 0.25,
    }
}


def pyleecan_test_base(test_params: list, 
                       result_path: str = "",
                       test_data_path: str = "", 
                       result_folder:str = "",
                       test_data_folder: str = "",
                       test_type: str = "",
                       test_id: int = 0,
                       test_case: str = "",
                       print_flag: bool = 0, debug_flag: bool = 0) :

    '''
    Base test data prepper for Pyleecan API workflow test.
    Params:
    - test_type: type of test
    - test_id: test id
    - test_case: test case name, same as machine name
    
    '''

    # disable messages of matplotlib
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    # logging.getLogger("matplotlib.colormaps").setLevel(logging.ERROR)
    # logging.getLogger("numpy").setLevel(logging.ERROR)
    logging.getLogger().setLevel(logging.DEBUG)


    #create machine
    if test_data_path == "":
        machine_file_path = os.path.join(ROOT_DIR, test_data_folder, f"{test_type}\\{test_case}.json")
    else:
        machine_file_path = test_data_path
    print(machine_file_path)
    pyleecan_machine: Machine = load.load(machine_file_path)

    #Create result folder
    if result_path == "":
        curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        resFolder = os.path.join(ROOT_DIR, result_folder, f"{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}")
        if not os.path.isdir(resFolder):
            os.makedirs(resFolder)
    else:
        resFolder = result_path

    #Run simulation
    pyleecanAPI.main(pyleecan_machine, model_dir = resFolder)
    geo_file = os.path.join(resFolder, pyleecan_machine.name + ".geo")
    pro_file = os.path.join(resFolder, pyleecan_machine.name + ".pro")

    sim_res_dir = os.path.join(resFolder, f"res_{pyleecan_machine.name}")
    if not os.path.isdir(sim_res_dir):
        os.makedirs(sim_res_dir)

    id = test_params["id"]
    iq = test_params["iq"]
    n = test_params["rpm"]
    resid = f"id_{id}_iq_{iq}_n_{n}rpm"
    param_dict = {
        "getdp": {
            "ID_RMS": id,
            "IQ_RMS": iq,
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
        "exe": r'H:\onelab-Windows64\getdp.exe',
        "gmsh": findGmsh(),
    }
    runCalcforCurrent(param_dict)

    return machine_file_path, resFolder

if __name__ == "__main__":
    # pyleecan_test_base(test_cases, test_params)
    print(os.path.join(os.path.abspath('.'), "pytest.ini"))