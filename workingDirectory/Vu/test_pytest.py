
import os
from pyleecan_test_base import pyleecan_test_base

import glob
from collections import defaultdict
from pyemmo.definitions import ROOT_DIR

from testUtils import updateConfig
from configparser import ConfigParser
from datetime import datetime

class TestCases:
    test_cases = defaultdict(dict)

    test_params = {
        'api\\pyleecan': {
            "id": -10,
            "iq": 50,
            "rpm": 1000,
            "d_theta": 0.25,
        }
    }
    def test_pyleecan(self):
        """
        Testing pyleecan API to generate GMSH and simulation files based on pyleecan machine json files.


        """
        test_type = "api\\pyleecan"
        self.make_test_cases(test_type)
        for test_id, test_case in self.test_cases[test_type].items():
            curr_datetime, log_dest = updateConfig(test_type, test_id, test_case)
            pyleecan_test_base(curr_datetime, test_type, test_id, test_case, self.test_params[test_type])

        for  test_id, test_case in self.test_cases[test_type].items():
            #Point 1: check if result folder exist
            result_path = f"Results\\pyleecanAPI\\{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}"
            assert os.path.isdir(result_path)

            #Point 2: check if GMSH base files are generated
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.geo"))) == 2
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.pro"))) == 3
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.db"))) == 1
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.msh"))) == 1
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.pre"))) == 1
            assert len(glob.glob(os.path.join(ROOT_DIR, result_path, "*.res"))) == 1
            

            #Point 3: check if simulation data is generated
            assert os.path.isdir(os.path.join(ROOT_DIR, result_path, f"res_{test_case}"))
            



    def make_test_cases(self, test_type: str) -> dict:
        test_files = glob.glob(os.path.join(ROOT_DIR, r"tests\data", test_type, "*.json"))
        print(test_files)
        test_names = list(map(lambda x: x.split(".")[0], map(lambda x: x.split("\\")[-1], test_files)))
        self.test_cases[test_type] = {}
        for id, name in enumerate(test_names):
             self.test_cases[test_type][id] = name
        
        return self.test_cases


    # def updateConfig(test_type: str, test_id: int, test_case: str):
    
    #     '''
    #     Function to update config file to generate proper test file name
    #     '''

    #     curr_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    #     parser = ConfigParser()
    #     parser.read('pytest.ini')
    #     parser.set('pytest', 'log_file', f"logs/{test_type}/test_{test_id}_{test_case}/{curr_datetime}.log")

    #     with open('pytest.ini', 'w') as config_file:
    #         parser.write(config_file)