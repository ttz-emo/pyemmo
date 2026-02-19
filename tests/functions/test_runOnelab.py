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
from json import load
from os import listdir, makedirs
from os.path import isdir, isfile, join, normpath
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree

from pyemmo.functions import run_onelab
from pyemmo.functions.run_onelab import (
    SETUP_FILE_NAME,
    findGetDP,
    findGmsh,
    runCalcforCurrent,
)
from tests import TEST_DATA_DIR
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
        Vordefinierte Setup Funktion die einmalig am Anfang der Testprozedur ausgeführt wird.
        Nützlich für beispielsweise zeitintensives Setup von Dingen die nicht verändert werden.
        Konkret z.B. Laden von vordefinierter, verifizierter Testgeometrie
        """
        # copy model data and set actual model directory
        original_model_dir = normpath(join(TEST_DATA_DIR, "onelab", "Toyota_Prius"))
        # folder to store temporary model data and simulation results
        cls.test_sim_dir = normpath(join(TESTS_RESULTS_DIR, "TestRunOnelab"))
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
        cls.pro_file = join(cls.model_dir, "Toyota_Prius.pro")
        cls.geo_file = join(cls.model_dir, "Toyota_Prius.geo")
        # add default setup dict to use in runCalcForCurrent
        cls.default_param_dict = {
            "getdp": {
                "exe": findGetDP(),
                "IQ_RMS": 10.0,
                "ID_RMS": 0.0,
                "RPM": 1000,
                "initrotor_pos": 0.0,
                "d_theta": 5.0,
                "finalrotor_pos": 10.0,
                "ResId": "",
                "Flag_AnalysisType": 0,
                "Flag_PrintFields": 0,
                "Flag_Debug": 0,
                "Flag_ClearResults": 1,
                "verbosity level": 3,
                #                     mesh_veryFine, fineMesh or coarseMesh
                # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                # "Flag_SecondOrder": 0,
                "stop_criterion": 1e-5,
                "res": cls.test_sim_dir,  # result folder
            },
            "pro": join(cls.model_dir, "Toyota_Prius.pro"),  # pro file
            "gmsh": {"exe": findGmsh()},  # gmsh exe and params
            "info": "",
            "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
        }

    @classmethod
    def tearDownClass(cls):
        """
        Vordefinierte teardown Funktion die einmalig am Ende der Testprozedur ausgeführt wird.
        Nützlich für beispielsweise Löschen von in Test erzeugten Datein und Ordnern.
        Konkret z.B. Löschen von abgespeicherten Geometrien
        """
        rmtree(cls.model_dir)
        # remove any results folders that match the test res_id pattern
        for folder in listdir(cls.test_sim_dir):
            if fnmatch.fnmatch(folder, "test_*"):
                rmtree(join(cls.test_sim_dir, folder))

    def setUp(self):
        """
        Vordefinierte Setup Funktion von Unittest
        Die Schreibweise "setUp" muss beachtet werden.
        Setup wird vor jeder Testmethode der Klasse TestRotorIPMSM ausgeführt
        """

    def tearDown(self):
        """
        Vordefinierte Reset Funktion von Unittest
        Die Schreibweise "tearDown" muss beachtet werden!
        teardown wird nach jeder Testmethode der Klasse TestRotorIPMSM ausgeführt
        """
        pass

    def test_findGmsh(self):
        # Setup

        # Run
        GmshExe = findGmsh()
        # Verify
        ...

    def test_run_ONELAB(self):
        """Test the run_calc_for_current function"""

        res_id = "test_runOnelab"
        input_param_dict = self.default_param_dict
        input_param_dict["getdp"]["ResId"] = res_id
        # input_param_dict["getdp"]["Flag_AnalysisType"] = 1  # transient

        # run simulation
        sim_res_dict = runCalcforCurrent(input_param_dict)
        # results are stored in [getdp][res] + [getdp][resId]
        res_dir = join(self.test_sim_dir, res_id)
        # make sure results folder exists
        if not isdir(res_dir):
            raise FileNotFoundError(
                f"Simulation results folder '{self.test_sim_dir} + {res_id}' does not exist!"
            )
        # make sure setup_file was created
        setup_file_path = join(res_dir, SETUP_FILE_NAME)
        if SETUP_FILE_NAME not in listdir(res_dir):
            raise FileNotFoundError(
                f"Missing simulation setup json file '{SETUP_FILE_NAME}'."
            )
        # make sure setup file contains all input parameters
        with open(setup_file_path, encoding="UTF-8") as setup_file:
            setup_dict = load(setup_file)
        for key, val in input_param_dict.items():
            assert key in setup_dict, f"Key '{key}' is missing from dict: {setup_dict}"
            if not setup_dict[key] == val:
                raise ValueError(
                    f"Value of key '{key}' between input dict and exported json setup "
                    f"file does not match:\n{setup_dict[key]} != {val}"
                )
        # make sure log file was created and is not empty
        if not any(file.endswith(".log") for file in listdir(res_dir)):
            raise FileNotFoundError(
                f"Missing simulation log file from {res_dir}!\n"
                f"Files in that directory:\n{listdir(res_dir)}"
            )
        else:
            log_files = [path for path in Path(res_dir).glob("*.log")]
            if len(log_files) == 0:
                raise RuntimeError("Found log file with listdir but missing from path!")
            assert len(log_files) == 1, "More than one log file in results folder!"
            log_file_path = log_files[0]
            with open(log_file_path, encoding="UTF-8") as log_file:
                log = log_file.read()
            assert log, "Log of simulation was empty!"

    def test_run_sim_detached(self):
        """Test that runCalcForCurrent function also works with ``detach_process=True``"""
        logger = logging.getLogger(__file__)
        res_id = "test_simulation_detached"
        res_dir = Path(self.test_sim_dir, res_id)
        logger.info(f"Running simulation '{res_id}' with detached subprocess")
        res_dict = runCalcforCurrent(
            param={
                "getdp": {
                    "exe": "getdp",
                    "res": str(self.test_sim_dir),
                    "ResId": res_id,
                    "Flag_AnalysisType": 0,
                    "Flag_ClearResults": 0,
                    "Flag_NL": 0,  # linear fast
                },
                "gmsh": {"exe": "gmsh"},
                "pro": str(self.pro_file),
            },
            detach_process=True,
        )
        # make sure process id was saved
        assert isfile(Path(res_dir, run_onelab.PID_FILE))


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
