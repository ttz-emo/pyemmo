
import os
from pyleecan_test_base import pyleecan_test_base

import glob
from collections import defaultdict
from pyemmo.definitions import ROOT_DIR

import configparser
from datetime import datetime

# Overwrite log_file filename in pytest.ini with datetime
def update_py_test_ini():
    curr_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    test_config = configparser.ConfigParser()
    test_config.read('pytest.ini')
    # Update the string at log_file to with latest datetime
    test_config.set('pytest', 'log_file', 'logs/pytest-{}-logs.log'.format(curr_datetime))

    with open('pytest.ini', 'w') as configfile:
        test_config.write(configfile)


class TestCases:
    test_cases = defaultdict(dict)

    test_params = {
        'api\pyleecan': {
            "id": -10,
            "iq": 50,
            "rpm": 1000,
            "d_theta": 0.25,
        }
    }
    def test_pyleecan(self):
        test_type = "api\pyleecan"
        self.make_test_cases(test_type)
        pyleecan_test_base(self.test_cases[test_type], self.test_params[test_type])

        for k, v in self.test_cases[test_type].items():
            assert len(glob.glob(os.path.join(ROOT_DIR, f"Results\pyleecanAPI\\test_{k}\\{v}\\*.geo"))) == 2

    def test_dummy(self):
        assert 1 + 1 == 3 

    def make_test_cases(self, test_type: str) -> dict:
        test_files = glob.glob(os.path.join(ROOT_DIR, r"tests\data", test_type, "*.json"))
        test_names = list(map(lambda x: x.split(".")[0], map(lambda x: x.split("\\")[-1], test_files)))
        self.test_cases[test_type] = {}
        for id, name in enumerate(test_names):
             self.test_cases[test_type][id] = name
        
        return self.test_cases
