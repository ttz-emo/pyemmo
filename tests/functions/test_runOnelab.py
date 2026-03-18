#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
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
from __future__ import annotations

import fnmatch
import logging
import unittest
from os import listdir, makedirs, rmdir
from os.path import isdir, isfile, join
from shutil import copytree, ignore_patterns, rmtree
from uuid import uuid4

import pytest

from pyemmo.functions.run_onelab import (
    find_getdp,
    find_gmsh,
    findGmsh,
    run_simulation,
)
from tests import GETDP_EXE, TEST_DATA_DIR
from tests import TEST_TEMP_DIR as TESTS_RESULTS_DIR


class TestRunOnelab(unittest.TestCase):
    """
    Testing the module runOnelab
    Based on tutorial: https://youtu.be/6tNS--WetLI
    Author: Max Schuler
    """

    @classmethod
    def setUpClass(cls):
        """
        A predefined setup function that is executed once at the beginning of the test
        procedure. This is useful, for example, for time-consuming setup of elements
        that will not be changed.
        Specifically, for example, loading predefined, verified test geometry.
        """
        proc_id = uuid4()
        # copy model data and set actual model directory
        original_model_dir = join(TEST_DATA_DIR, "onelab", "Toyota_Prius")
        # folder to store temporary model data and simulation results
        cls.test_sim_dir = join(TESTS_RESULTS_DIR, "TestRunOnelab_" + str(proc_id))
        if not isdir(cls.test_sim_dir):
            makedirs(cls.test_sim_dir)
        # copy model data to test simulation results directory
        model_dir = join(cls.test_sim_dir, "Toyota_Prius")
        if not isdir(model_dir):
            cls.model_dir = copytree(
                original_model_dir,
                model_dir,
                ignore=ignore_patterns("res*", "*.msh", "*.db", "*.res", "*.pre"),
            )
        else:
            if isfile(join(model_dir, "Toyota_Prius.pro")):
                cls.model_dir = model_dir
            else:
                raise FileExistsError(
                    f"Model directory {model_dir} already exists but does not "
                    "contain the expected files (Toyota_Prius.pro)."
                )

    @classmethod
    def tearDownClass(cls):
        """
        A predefined teardown function that is executed once at the end of the test procedure.
        Useful, for example, for deleting files and folders created during testing.
        Specifically, for example, deleting saved geometries.
        """
        rmtree(cls.model_dir)
        # remove any results folders that match the test res_id pattern
        for folder in listdir(cls.test_sim_dir):
            if fnmatch.fnmatch(folder, "test_*"):
                rmtree(join(cls.test_sim_dir, folder))
        # remove temporary test folder if empty
        if len(listdir(cls.test_sim_dir)) == 0:
            rmdir(cls.test_sim_dir)

    def setUp(self):
        """
        Predefined setup function of unit tests. The syntax "setUp" must be preserved.
        setUp is executed before each test method of the test class.
        """

    def tearDown(self):
        """
        Predefined teardown function of unit tests. The syntax "tearDown" must be
        preserved. tearDown is executed after each test method of the test class.
        """
        pass

    def test_find_gmsh(self):
        """Test function find_gmsh"""
        gmsh_path = find_gmsh()
        # Verify
        logging.getLogger(__file__).info("Found Gmsh in %s", gmsh_path)
        assert gmsh_path.lower().endswith(".exe") or gmsh_path.lower().endswith(".bat")
        assert isfile(gmsh_path)

    def test_findGmsh(self):
        """Test old findGmsh notation for function find_gmsh."""
        with pytest.warns(DeprecationWarning):
            gmsh_path = findGmsh()
        # Verify
        logging.getLogger(__file__).info("Found Gmsh in %s", gmsh_path)
        assert gmsh_path.lower().endswith(".exe") or gmsh_path.lower().endswith(".bat")
        assert isfile(gmsh_path)

    def test_find_getdp(self):
        """Test the find_getdp function and make sure sure getdp can be found for test_run_simulation"""
        exe = find_getdp()
        # Verify
        # logger = logging.getLogger(__file__)
        logging.getLogger(__file__).info("Found GetDP in %s", exe)
        assert exe.lower().endswith(".exe")
        assert isfile(exe)

    def test_run_simulation(self):
        """Test the run_simulation function with default parameters for the Toyota Prius."""
        # make sure simulation folder starts with "test_" so the teardown function
        # removes it.
        res_id = "test_run_simulation_func"
        run_simulation(
            {
                "getdp": {
                    "exe": GETDP_EXE,
                    "IQ_RMS": 10.0,
                    "ID_RMS": 0.0,
                    "RPM": 1000,
                    "initrotor_pos": 0.0,
                    "d_theta": 5.0,
                    "finalrotor_pos": 10.0,
                    "ResId": res_id,
                    "Flag_AnalysisType": 1,
                    "Flag_PrintFields": 0,
                    "Flag_Debug": 0,
                    "Flag_ClearResults": 1,
                    "verbosity level": 3,
                    #                     mesh_veryFine, fineMesh or coarseMesh
                    # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                    # "Flag_SecondOrder": 0,
                    "stop_criterion": 1e-5,
                    "res": self.test_sim_dir,  # result folder
                },
                "pro": join(self.model_dir, "Toyota_Prius.pro"),  # pro file
                "gmsh": {"exe": findGmsh()},  # gmsh exe and params
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
