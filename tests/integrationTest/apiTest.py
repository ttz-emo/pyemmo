import os
from pyleecan_test_base import pyleecan_test_base, pyleecanPrepTuple

import glob
from collections import defaultdict
from pyemmo.definitions import ROOT_DIR
from pyemmo import rootLogger
from pyemmo.functions.import_results import read_timetable_dat
import logging
from datetime import datetime
import unittest
from pytest_check import check
import pytest

from testUtils import (
    updateConfig,
    count_files,
    messagePrinter,
    fileParser,
    fileFilter,
    make_test_cases,
)

api_test_type = "api\\pyleecan"
test_cases = {}
test_cases[api_test_type] = make_test_cases(api_test_type)

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


@pytest.mark.parametrize(
    "test_tuple", pyleecanPrepTuple(test_cases, api_test_type)[1:]
)
class TestCasesIntegration:
    """
    Class containing test cases for Pyleecan API
    Prerequisites
    - Pytest should be installed
    - Pytest-progress should be installed (pip install pytest-progress)
    - test data should be available locally

    Test content:
    1. Test Pyleecan API to create Pyleecan machine and generate simulations in Onelab
    """

    def test_api_simul_folder_exist(self, test_tuple):
        (
            test_id,
            test_case,
            source_path,
            result_path,
            simul_path,
            simul_subfolder_path,
            _,
            _,
            _,
        ) = test_tuple
        pyleecan_test_base(
            test_params[api_test_type],
            result_path=result_path,
            test_data_path=source_path,
        )
        print(f"TEST CASE {test_id}: {test_case}")
        print(
            "Test point 1: Check that simulation result folders are properly generated:"
        )
        with check("check simulation folder existence"):
            assert os.path.isdir(simul_path) and messagePrinter(
                "SUCCESS: Simulation result folder exist"
            ), "ERROR: Simulation result folder does not exist"
        with check("check simulation subfolder existence"):
            assert os.path.isdir(simul_subfolder_path) and messagePrinter(
                "SUCCESS: Simulation result subfolder exists!"
            ), "ERROR: Simulation result subfolder does not exist"
        print()

    def test_gmsh_base_files(self, test_tuple):
        test_id, test_case, _, result_path, _, _, base_result_path, _, _ = (
            test_tuple
        )
        print(f"TEST CASE {test_id}: {test_case}")
        print("Test point 2: check if GMSH base files are generated")
        self.check_file_counts(base_result_path, result_path)
        print()

    def test_simul_data_gen(self, test_tuple):
        (
            test_id,
            test_case,
            _,
            _,
            simul_path,
            simul_subfolder_path,
            _,
            base_simul_path,
            base_simul_subfolder_path,
        ) = test_tuple
        print(f"TEST CASE {test_id}: {test_case}")
        print("Test point 3: check if simulation data is generated")
        self.check_file_counts(base_simul_path, simul_path)
        self.check_file_counts(base_simul_subfolder_path, simul_subfolder_path)
        print()

    def test_dat_file_vals(self, test_tuple):

        (
            test_id,
            test_case,
            _,
            _,
            _,
            simul_subfolder_path,
            _,
            _,
            base_simul_subfolder_path,
        ) = test_tuple
        print(f"TEST CASE {test_id}: {test_case}")
        print("Test point 5: check values in dat files")
        dat_targets = glob.glob(os.path.join(simul_subfolder_path, "*.dat"))
        dat_bases = glob.glob(os.path.join(base_simul_subfolder_path, "*.dat"))
        for target_file, base_file in zip(dat_targets, dat_bases):
            target_dat = read_timetable_dat(target_file)
            base_dat = read_timetable_dat(base_file)
            with check:
                assert target_dat == base_dat and messagePrinter(
                    f"SUCCESS: {target_file} check ok"
                ), f"ERROR: mismatch found between base and target dat in {target_file}!"

        print("\n")

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
    api_test_tuple = pyleecanPrepTuple(test_cases, api_test_type)
    headers = api_test_tuple[0].split(",")
    for h, f in zip(headers, api_test_tuple[1]):
        print(h, ":", f)
    new_test = TestCasesIntegration()
    new_test.test_api_simul_folder_exist(api_test_tuple[1])
