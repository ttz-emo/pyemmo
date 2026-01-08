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
Author: Vu Nguyen

Description:
This module contains all integration tests for Pyleecan API, as part PyEMMO.
Test types are divided by classes, which contains individual test methods.
Since tests are written to be picked up by pytest, pytest should be used to
execute this module.

syntax: pytest <path_to_module>

"""

from __future__ import annotations

import glob
import logging
import os
import shutil

import pytest
from pytest_check import check  # to allow multiple failures per test

from pyemmo.definitions import ROOT_DIR, TEST_DIR
from pyemmo.functions.import_results import read_timetable_dat

from . import LOGGER
from .pyleecan_test_base import curr_datetime, pyleecanPrepTuple, test_params
from .testUtils import (
    check_folder_type,
    count_files,
    fileFilter,
    fileParser,
    messagePrinter,
)

# Vars for using in tests
test_types = ["api\\pyleecan"]
test_cases = {}
log_dir = os.path.join(TEST_DIR, "Results", test_types[0])
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
fileHandler = logging.FileHandler(
    filename=os.path.join(log_dir, f"test_result_{curr_datetime}.log"),
    mode="w",
    encoding="utf-8",
)
LOGGER.addHandler(fileHandler)

## Auto generate test cases from machine files in tests\data\api\pyleecan dir:
# for t in test_types:
#     test_cases[t] = make_test_cases(t, fixed_test_flg=True)

# Fix test cases for acutal machines to be testes from data folder:
test_cases["api\\pyleecan"] = [
    ("test_id", "test_case", "test_run_flag"),
    (0, "IPMSM_B", False),  # TODO: mark as failing instead of skipping!
    (1, "SPMSM_002", True),
    (2, "SPMSM_003", True),
    (3, "Toyota_Prius", True),
]


# Fixture for cleaning up test data
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """
    fixture for cleaning up data after tests.
    """
    from . import LOGGER

    def finisher():
        LOGGER.info("Doing teardown...")
        for t in test_types:
            test_result_dir = os.path.join(ROOT_DIR, test_params[t]["result_folder"], t)
            timestamped_result_dirs = [
                os.path.join(test_result_dir, dir)
                for dir in os.listdir(test_result_dir)
                if os.path.isdir(os.path.join(test_result_dir, dir))
            ]
            log_files = [
                os.path.join(test_result_dir, fn)
                for fn in os.listdir(test_result_dir)
                if ".log" in fn
            ]
            no_to_keep = 2  # decide how many test results should be kept
            no_to_remove_dir = 0
            no_to_remove_fn = 0
            while no_to_remove_dir < len(timestamped_result_dirs) - no_to_keep:
                shutil.rmtree(timestamped_result_dirs[no_to_remove_dir])
                no_to_remove_dir += 1
            while no_to_remove_fn < len(log_files) - no_to_keep:
                os.remove(log_files[no_to_remove_fn])
                no_to_remove_fn += 1

    request.addfinalizer(finisher)


# Integration test class
@pytest.mark.skip(
    reason="This old integration test setup is too complicated! New PyleecanAPI "
    "integration test in subfolder 'Toyota_Prius'. Additionally all pyleecan default "
    "motor files are tested in the pyleecan api tests."
)
@pytest.mark.parametrize(
    # "test_tuple",
    (
        "test_id",
        "test_case",
        "source_path",
        "result_path",
        "simul_path",
        "simul_subfolder_path",
        "base_result_path",
        "base_simul_path",
        "base_simul_subfolder_path",
    ),
    pyleecanPrepTuple(test_cases, test_types[0])[1:],
    scope="session",
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
        2. Check that GMSH and getDP files are generated
        3. Check that simulation files are generated
        4. Check dat files content are the same as base comparison

    How to run:

        - Use pytest <integration_test_folder> on command line
        - Use pytest <path_to_this_file> on command line

    .. note::

        The integration tests is currently limited to 4 machine models: ISPMS_B, SPMSM_002, SPMSM_003, Toyota_Prius.
        Machines whose simulation fails will have their tests skipped.
    """

    @pytest.mark.dependency(name="simul_folder_exist")
    def test_api_simul_folder_exist(
        self,
        test_id,
        test_case,
        source_path,
        result_path,
        simul_path,
        simul_subfolder_path,
        base_result_path,
        base_simul_path,
        base_simul_subfolder_path,
    ):
        """
        Check if simulation result folders were generated (meaning simulation was successful)
        All folders that exists in base data should also be in generated data.
        Test will fail if a folder does not exist.
        """
        # ) = test_tuple
        if result_path == "":
            LOGGER.info(f"TEST CASE {test_id}: {test_case}: SKIPPED")
        else:
            LOGGER.info(f"TEST CASE {test_id}: {test_case}:")
            LOGGER.info(
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

    @pytest.mark.dependency(name="simul_data_gen", depends=["simul_folder_exist"])
    def test_gmsh_base_files(
        self,
        # test_tuple
        test_id,
        test_case,
        source_path,
        result_path,
        simul_path,
        simul_subfolder_path,
        base_result_path,
        base_simul_path,
        base_simul_subfolder_path,
    ):
        """
        This test checks if the correct gmsh and getdp files have been generated correctly.
        This will be skipped if test_api_simul_folder_exist fails.
        """
        # (test_id, test_case, _, result_path, _, _, base_result_path, _, _) = (
        #     test_tuple
        # )

        LOGGER.info(f"TEST CASE {test_id}: {test_case}")
        LOGGER.info("Test point 2: check if GMSH base files are generated")
        self.check_file_counts(base_result_path, result_path)

    @pytest.mark.dependency(name="simul_data_gen", depends=["simul_folder_exist"])
    def test_simul_data_gen(
        self,
        # test_tuple
        test_id,
        test_case,
        source_path,
        result_path,
        simul_path,
        simul_subfolder_path,
        base_result_path,
        base_simul_path,
        base_simul_subfolder_path,
    ):
        """
        This test checks that the simulation result files have been generated correctly.
        If test_api_simul_folder_exist fails, this will be skipped.
        """
        # (
        #     test_id,
        #     test_case,
        #     _,
        #     _,
        #     simul_path,
        #     simul_subfolder_path,
        #     _,
        #     base_simul_path,
        #     base_simul_subfolder_path,
        # ) = test_tuple
        LOGGER.info(f"TEST CASE {test_id}: {test_case}")
        LOGGER.info("Test point 3: check if simulation data is generated")
        self.check_file_counts(base_simul_path, simul_path)
        self.check_file_counts(base_simul_subfolder_path, simul_subfolder_path)

    @pytest.mark.dependency(depends=["simul_folder_exist", "simul_data_gen"])
    def test_dat_file_vals(
        self,
        # test_tuple
        test_id,
        test_case,
        source_path,
        result_path,
        simul_path,
        simul_subfolder_path,
        base_result_path,
        base_simul_path,
        base_simul_subfolder_path,
    ):
        """
        Compares data in generated .dat files with base data.
        Runs for a test case only if test_simul_data_gen succeeded for that test case.
        Output comparison for all test cases to dat_check.log file within the test folder.
        Test will fail in case absolute difference (for values < 1e-6) or relative difference (for values >= 1e-6) is larger than 0.01.

        """
        # (
        #     test_id,
        #     test_case,
        #     _,
        #     _,
        #     _,
        #     simul_subfolder_path,
        #     _,
        #     _,
        #     base_simul_subfolder_path,
        # ) = test_tuple
        LOGGER.info(f"TEST CASE {test_id}: {test_case}")
        LOGGER.info("Test point 4: check values in dat files")
        # with check("check base simulation subfolder existence"):
        #     assert os.path.isdir(base_simul_subfolder_path) and messagePrinter(
        #         "Base simulation result subfolder exists, continuing tests..."
        #     ), "ERROR: Base simulation result subfolder does not exist, nothing to compare"
        if not os.path.isdir(base_simul_subfolder_path):
            LOGGER.info(
                f"Base simulation result subfolder for {test_case} does not exist, nothing to compare"
            )
        else:
            dat_targets = glob.glob(os.path.join(simul_subfolder_path, "*.dat"))
            dat_bases = glob.glob(os.path.join(base_simul_subfolder_path, "*.dat"))
            with open(
                os.path.join(
                    TEST_DIR, "results", test_types[0], f"{curr_datetime}/dat_check.log"
                ),
                "a",
            ) as f:  # write dat file check to file
                f.write(f"{test_id}_{test_case} result: \n")
                for target_file, base_file in zip(dat_targets, dat_bases):
                    # target_time, target_dat = read_timetable_dat(target_file)
                    # time_base, base_dat = read_timetable_dat(base_file)
                    target_dat = read_timetable_dat(target_file)
                    base_dat = read_timetable_dat(base_file)
                    check_flag = True
                    with check:
                        _, filename = os.path.split(target_file)
                        for i in range(len(base_dat[0])):
                            diff = abs(target_dat[1][i] - base_dat[1][i])
                            rel_diff = diff / abs(base_dat[1][i])
                            f.write(
                                f"{filename} | "
                                f"Base data: {base_dat}; Target data:{target_dat} | "
                                f"Difference - abs.:{diff} - rel.:{rel_diff}\n"
                            )
                            if (
                                abs(target_dat[1][i]) < 1e-6
                                and abs(base_dat[1][i]) < 1e-6
                            ):
                                # compare abs. difference
                                if diff >= 0.01:
                                    LOGGER.error(
                                        f"ERROR: Mismatch for file {filename}; "
                                        f"Base data: {base_dat}; Target data:{target_dat}; "
                                        f"Difference - abs.:{diff}"
                                    )
                                    check_flag = False

                                assert diff < 0.01, (
                                    f"Mismatch for file {filename}; "
                                    f"Base data: {base_dat}; Target data:{target_dat}; "
                                    f"Difference - abs.:{diff}"
                                )
                            else:
                                # compare relative difference
                                # rel_diff = diff / abs(base_dat[1][i])
                                if rel_diff >= 0.01:
                                    LOGGER.error(
                                        f"ERROR: Mismatch for file {filename}; "
                                        f"Base data: {base_dat}; Target data:{target_dat}; "
                                        f"Difference - abs.:{diff} - rel.:{rel_diff}"
                                    )
                                    check_flag = False
                                assert rel_diff < 0.01, (
                                    f"Mismatch for file {filename}; "
                                    f"Base data: {base_dat}; Target data:{target_dat}; "
                                    f"Difference - abs.:{diff} - rel.:{rel_diff}"
                                )
                            # if base_dat[1][i] >= 0.01:
                            #     check_flag = False

                        assert check_flag and messagePrinter(
                            f"SUCCESS: all data in {target_file} ok."
                        ), f"ERROR: mismatch detected between base ({base_file}) and target ({target_file})."
                f.write("\n")

    def check_file_counts(
        self,
        base_folder: str,
        folder_to_count: str,
        check_from_base: bool = True,
    ):
        """
        Helper function to compare count of files per type between base data and result data
        """
        base_count_fixed = {
            "result": {
                "pro": 3,
                "log": 1,
                "db": 1,
                "geo": 2,
                "msh": 1,
                "pre": 1,
                "res": 1,
            },
            "simul": {"wdg": 1},
            "simul_sub": {"pos": 10, "dat": 14},
        }
        if check_from_base:
            base_count = count_files(base_folder)
        else:
            base_count = base_count_fixed[check_folder_type(folder_to_count)]
        exclusion_list = ["dir", "png"]
        for file_type, count in base_count.items():
            if file_type not in exclusion_list:
                result_count = len(
                    glob.glob(os.path.join(ROOT_DIR, folder_to_count, f"*.{file_type}"))
                )
                with check:
                    assert result_count == count and messagePrinter(
                        f"SUCCESS: .{file_type} count matches"
                    ), f"ERROR: .{file_type} count mismatch! Base: {count}; Result: {result_count}"

    def check_content(self, base_path, target_path, target_types):
        """
        Line by line comparison of base data vs. result data
        Deprecated.
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
    api_test_tuple = pyleecanPrepTuple(test_cases, test_types[0])
    headers = api_test_tuple[0].split(",")
    for header, f in zip(headers, api_test_tuple[1]):
        LOGGER.info(header, ":", f)
    # new_test = TestCasesIntegration()
    # new_test.test_api_simul_folder_exist(api_test_tuple[1])
