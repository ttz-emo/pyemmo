import os
from pyleecan_test_base import pyleecan_test_base

import glob
from collections import defaultdict
from pyemmo.definitions import ROOT_DIR
from pyemmo import rootLogger
from pyemmo.functions.import_results import read_timetable_dat
import logging
from datetime import datetime
import unittest
from pytest_check import check

from testUtils import (
    updateConfig,
    count_files,
    messagePrinter,
    fileParser,
    fileFilter,
    make_test_cases,
)


class TestCases(unittest.TestCase):
    """
    Class containing test cases for Pyleecan API
    Prerequisites
    - Pytest should be installed
    - Pytest-progress should be installed (pip install pytest-progress)
    - test data should be available locally

    Test content:
    1. Test Pyleecan API to create Pyleecan machine and generate simulations in Onelab
    """

    test_cases = defaultdict(dict)

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

    def test_pyleecan(self):
        """
        Testing pyleecan API to generate GMSH and simulation files based on pyleecan machine json files.
        There are 4 test points included:
            - Check that simulation folders and subfolders are properly generated
            - Check that GMSH and GetDP files are properly generated
            - Check that simulation folders and files are generated
            - Check that content of result file match base comparison data

        """
        test_type = "api\\pyleecan"
        # self.make_test_cases(test_type)
        self.test_cases[test_type] = make_test_cases(test_type)
        result_path = defaultdict(list)
        simul_path = defaultdict(list)
        simul_subfolder_path = defaultdict(list)
        rootLogger.setLevel(logging.DEBUG)

        print("========TEST PYLEECAN API + SIMULATION FLOW START========")
        for test_id, test_case in self.test_cases[test_type].items():
            # curr_datetime, _ = updateConfig(test_type, test_id, test_case) #REDUNDANT since API level log already exists in each folder
            curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

            # preparing source and result folders
            source_path = os.path.join(
                ROOT_DIR,
                self.test_params[test_type]["test_data_folder"],
                f"{test_type}\\{test_case}.json",
            )

            # make sure source file exists -> REDUNDANT since test cases are created from test data folder content.
            # assert os.path.isfile(source_path) and messagePrinter("SUCCESS: Source file exist"), "ERROR: Source file does not exist"

            result_path[test_id] = os.path.join(
                ROOT_DIR,
                self.test_params[test_type]["result_folder"],
                f"{test_type}\\test_{test_id}\\{test_case}\\{curr_datetime}",
            )
            if not os.path.isdir(result_path[test_id]):
                os.makedirs(result_path[test_id])

            simul_path[test_id] = os.path.join(
                result_path[test_id], f"res_{test_case}"
            )
            simul_subfolder = f"id_{self.test_params[test_type]['id']}_iq_{self.test_params[test_type]['iq']}_n_{self.test_params[test_type]['rpm']}rpm"
            simul_subfolder_path[test_id] = os.path.join(
                simul_path[test_id], simul_subfolder
            )

            pyleecan_test_base(
                self.test_params[test_type],
                result_path=result_path[test_id],
                test_data_path=source_path,
            )

        # _, _ = updateConfig()

        for test_id, test_case in self.test_cases[test_type].items():

            # Preparation of base comparison paths
            base_result_path = os.path.join(
                ROOT_DIR,
                self.test_params[test_type]["test_data_folder"],
                test_type,
                f"comparison_base\\{test_case}",
            )  # this can change to a different folder for base data
            base_simul_path = os.path.join(
                base_result_path, f"res_{test_case}"
            )  # This can also change for another base data folder
            base_simul_subfolder_path = os.path.join(
                base_simul_path, simul_subfolder
            )  # This can also change for another base data folder

            # Point 1: Check that simulation result folders are properly generated
            print(f"TEST CASE {test_id}: {test_case}")
            print(
                "Test point 1: Check that simulation result folders are properly generated:"
            )
            with check("check simulation folder existence"):
                assert os.path.isdir(simul_path[test_id]) and messagePrinter(
                    "SUCCESS: Simulation result folder exist"
                ), "ERROR: Simulation result folder does not exist"
            with check("check simulation subfolder existence"):
                assert os.path.isdir(
                    simul_subfolder_path[test_id]
                ) and messagePrinter(
                    "SUCCESS: Simulation result subfolder exists!"
                ), "ERROR: Simulation result subfolder does not exist"

            with check("check base result folder existence"):
                assert os.path.isdir(base_result_path) and messagePrinter(
                    "SUCCESS: Base result subfolder exists!"
                ), "ERROR: Base result subfolder does not exist"
            with check("check base simulation folder existence"):
                assert os.path.isdir(base_simul_path) and messagePrinter(
                    "SUCCESS: Base simulation folder exists!"
                ), "ERROR: Base simulation folder does not exist"

            with check("check base simulation subfolder existence"):
                assert os.path.isdir(
                    base_simul_subfolder_path
                ) and messagePrinter(
                    "SUCCESS: Base simulation subfolder exists!"
                ), "ERROR: Base simulation subfolder does not exist"
            print()

            if (
                os.path.isdir(base_result_path)
                and os.path.isdir(base_simul_path)
                and os.path.isdir(base_simul_subfolder_path)
            ):

                # Point 2: check if GMSH base files are generated
                print("Test point 2: check if GMSH base files are generated")
                self.check_file_counts(base_result_path, result_path[test_id])
                print()

                # Point 3: check if simulation data is generated
                print("Test point 3: check if simulation data is generated")
                self.check_file_counts(base_simul_path, simul_path[test_id])
                self.check_file_counts(
                    base_simul_subfolder_path, simul_subfolder_path[test_id]
                )
                print()

                # # Point 4: Check content of files - Takes to long, need another method.
                # print("Test point 4: check content of simulation files")
                # # target_file_types = ["geo", "pro", "msh","pre", "pos"]
                # target_file_types = ["msh", "pre", "pos"]
                # # 4.1 In main test folder
                # self.check_content(base_result_path, result_path[test_id], target_file_types)

                # #4.2 In simulation folder
                # self.check_content(base_simul_path, simul_path[test_id], target_file_types)

                # #4.3 In simulation subfolder
                # self.check_content(base_simul_subfolder_path, simul_subfolder_path[test_id], target_file_types)
                # print()

                # Point 5: check dat files value:
                print("Test point 5: check values in dat files")
                dat_targets = glob.glob(
                    os.path.join(simul_subfolder_path[test_id], "*.dat")
                )
                dat_bases = glob.glob(
                    os.path.join(base_simul_subfolder_path, "*.dat")
                )
                for target_file, base_file in zip(dat_targets, dat_bases):
                    target_dat = read_timetable_dat(target_file)
                    base_dat = read_timetable_dat(base_file)
                    with check:
                        assert target_dat == base_dat and messagePrinter(
                            f"SUCCESS: {target_file} check ok"
                        ), f"ERROR: mismatch found between base and target dat in {target_file}!"

                print("\n")
            else:
                print("No base file for comparison")
                continue

        print("========TEST PYLEECAN API + SIMULATION DONE========")

    def check_file_counts(self, base_folder: str, folder_to_count: str):
        """
        Compare count of files per type between base data and result data
        """
        base_count = count_files(base_folder)
        for file_type, count in base_count.items():
            if file_type != "dir":
                result_count = len(
                    glob.glob(
                        os.path.join(
                            ROOT_DIR, folder_to_count, f"*.{file_type}"
                        )
                    )
                )
                with check:
                    assert result_count == count and messagePrinter(
                        f"SUCCESS: .{file_type} count matches"
                    ), f"ERROR: .{file_type} count mismatch!\nBase: {count}\nResult: {result_count}"

    def check_content(self, base_path, target_path, target_types):
        """
        Line by line comparison of base data vs. result data
        """
        base_result_files = fileFilter(
            glob.glob(os.path.join(base_path, "*.*")), target_types
        )
        result_files = fileFilter(
            glob.glob(os.path.join(target_path, "*.*")), target_types
        )

        for base_file, result_file in zip(base_result_files, result_files):
            base_content = fileParser(base_file)
            result_content = fileParser(result_file)
            l = 0
            for line_base, line_result in zip(base_content, result_content):
                assert (
                    line_base == line_result
                ), f"ERROR: mismatch found between base and result of {result_file}!\nBase: {line_base}\nResult: {line_result}"
                l += 1
            assert l == len(base_content) and messagePrinter(
                f"SUCCESS: {result_file} content check ok"
            ), f"{result_file} content check failed."


if __name__ == "__main__":
    new_test = TestCases()
    new_test.test_pyleecan()
