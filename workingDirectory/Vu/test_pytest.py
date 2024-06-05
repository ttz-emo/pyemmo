
import os
from pyleecan_test_base import pyleecan_test_base

import glob
from collections import defaultdict
from pyemmo.definitions import ROOT_DIR

from testUtils import updateConfig, count_files

class TestCases:
    test_cases = defaultdict(dict)

    test_params = {
        'api\\pyleecan': {
            "id": -10,
            "iq": 50,
            "rpm": 1000,
            "d_theta": 0.25,
            "test_data_folder": "tests\\data",
            "result_folder": "Results\\pyleecanAPI"
        }
    }
    def test_pyleecan(self):
        """
        Testing pyleecan API to generate GMSH and simulation files based on pyleecan machine json files.


        """
        test_type = "api\\pyleecan"
        self.make_test_cases(test_type)
        result_path = defaultdict(list)
        simul_path = defaultdict(list)
        simul_subfolder_path = defaultdict(list)
        

        for test_id, test_case in self.test_cases[test_type].items():
            curr_datetime, log_dest = updateConfig(test_type, test_id, test_case)


            #preparing source and result folders
            source_path = os.path.join(ROOT_DIR, self.test_params[test_type]["test_data_folder"], f"{test_type}\\{test_case}.json")

            assert os.path.isfile(source_path)  # make sure source file exists

            result_path[test_id] = os.path.join(ROOT_DIR, self.test_params[test_type]["result_folder"], f"{test_type}\\{curr_datetime}\\test_{test_id}\\{test_case}")
            if not os.path.isdir(result_path[test_id]):
                os.makedirs(result_path[test_id])

            simul_path[test_id] = os.path.join(result_path[test_id], f"res_{test_case}")
            simul_subfolder = f"id_{self.test_params[test_type]['id']}_iq_{self.test_params[test_type]['iq']}_n_{self.test_params[test_type]['rpm']}rpm"
            simul_subfolder_path[test_id] = os.path.join(simul_path[test_id], simul_subfolder)

            pyleecan_test_base(self.test_params[test_type], result_path=result_path[test_id], test_data_path=source_path)

        for  test_id, test_case in self.test_cases[test_type].items():
            #Point 1: check if result folder exist
            base_result_path = os.path.join(ROOT_DIR, self.test_params[test_type]["test_data_folder"], test_type, f"comparison_base\\{test_case}") #this can change to a different folder for base data

            
            #Point 2: check if GMSH base files are generated
            base_result_file_count = count_files(base_result_path)
            self.check_file_counts(base_result_file_count, result_path[test_id])

            
            #Point 3: check if simulation data is generated
            base_simul_path = os.path.join(base_result_path, f"res_{test_case}") #This can also change for another base data folder
            base_simul_subfolder_path = os.path.join(base_simul_path, simul_subfolder) #This can also change for another base data folder

            assert os.path.isdir(simul_path[test_id])
            assert os.path.isdir(simul_subfolder_path[test_id])

            base_simul_file_count = count_files(base_simul_path)
            base_simul_subfolder_file_count = count_files(base_simul_subfolder_path)

            self.check_file_counts(base_simul_file_count, simul_path[test_id])
            self.check_file_counts(base_simul_subfolder_file_count, simul_subfolder_path[test_id])


            #Point 4: Check content of file







    def make_test_cases(self, test_type: str) -> dict:
        test_files = glob.glob(os.path.join(ROOT_DIR, r"tests\data", test_type, "*.json"))
        print(test_files)
        test_names = list(map(lambda x: x.split(".")[0], map(lambda x: x.split("\\")[-1], test_files)))
        self.test_cases[test_type] = {}
        for id, name in enumerate(test_names):
             self.test_cases[test_type][id] = name
        
        return self.test_cases

    def check_file_counts(self, base_count: dict, folder_to_count: str):
        for file_type, count in base_count.items():
                if file_type != "dir":
                    assert len(glob.glob(os.path.join(ROOT_DIR, folder_to_count, f"*.{file_type}"))) == count
