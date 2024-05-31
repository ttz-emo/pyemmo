import os
import logging

from pyleecan.Functions import load
from pyleecan.Classes.Machine import Machine

from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan import main as pyleecanAPI

from pyemmo.functions.runOnelab import runCalcforCurrent, findGmsh, findGetDP

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


def pyleecan_test_base(test_cases: dict, test_params: list, print_flag: bool = 0, debug_flag: bool = 0) :

    # disable messages of matplotlib
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    logging.getLogger().setLevel(logging.INFO)

    for k, v in test_cases.items():
        machine_file_path = os.path.join(
            ROOT_DIR, f"tests\data\\api\pyleecan\{v}.json"
        )
        assert os.path.isfile(machine_file_path)  # make sure file exists

        pyleecan_machine: Machine = load.load(machine_file_path)
        resFolder = os.path.join(ROOT_DIR, f"Results\pyleecanAPI\\test_{k}\\{pyleecan_machine.name}")
        if not os.path.isdir(resFolder):
            os.makedirs(resFolder)
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
        # runCalcforCurrent(param_dict)

if __name__ == "__main__":
    # pyleecan_test_base(test_cases, test_params)
    import sys
    for p in sys.path:
        print(p)