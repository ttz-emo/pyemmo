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
import unittest
from os import listdir, makedirs
from os.path import isdir, isfile, join
from shutil import copytree, ignore_patterns, rmtree
import logging
from matplotlib import pyplot as plt
import numpy as np
from pyemmo.functions.runOnelab import findGetDP, findGmsh, runCalcforCurrent
from ... import TEST_DATA_DIR, GMSH_EXE, GETDP_EXE
from ... import TEST_TEMP_DIR as TESTS_RESULTS_DIR
from pyemmo.api.pyleecan.main import main


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
        logging.getLogger(__name__).setLevel(logging.INFO)
        pyleecan_model_file = join(
            TEST_DATA_DIR, "api", "pyleecan", "Toyota_Prius.json"
        )
        # folder to store temporary model data and simulation results
        cls.main_test_dir = join(TESTS_RESULTS_DIR, "TestToyotaPrius")
        if not isdir(cls.main_test_dir):
            makedirs(cls.main_test_dir)

        # Create model data to test simulation results
        cls.model_dir = join(cls.main_test_dir, "Toyota_Prius_Model")
        cls.script = main(
            pyleecan_model_file,
            cls.model_dir,
            gmsh=GMSH_EXE,
            getdp=GETDP_EXE,
            use_gui=False,
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
        for folder in listdir(cls.main_test_dir):
            if fnmatch.fnmatch(folder, "test_*"):
                rmtree(join(cls.main_test_dir, folder))

    def setUp(self):
        """
        Predefined setup function of unit tests. The syntax "setUp" must be preserved.
        setUp is executed before each test method of the test class.
        """
        pass

    def tearDown(self):
        """
        Predefined teardown function of unit tests. The syntax "tearDown" must be
        preserved. tearDown is executed after each test method of the test class.
        """
        pass

    def test_BackEMF(self):
        """Test the back emf of the given model to match the expected resutls.
        Measurment data is taken from:

        "Burress, T A, C L Coomer, S L Campbell, et.al. "Evaluation of the 2007 Toyota
        Camry Hybrid Synergy Drive System". ORNL/TM-2007/190, Revised, 928684. 2008.
        https://doi.org/10.2172/928684.
        """
        res_id = "test_backEMF"
        results = runCalcforCurrent(
            {
                "getdp": {
                    "exe": GETDP_EXE,
                    "IQ_RMS": 0.0,
                    "ID_RMS": 0.0,
                    "RPM": 6000,
                    "initrotor_pos": 0.0,
                    "d_theta": 2.5,
                    "finalrotor_pos": 90.0,
                    "ResId": res_id,
                    "Flag_AnalysisType": 1,
                    "Flag_PrintFields": 0,
                    "Flag_Debug": 0,
                    "Flag_ClearResults": 1,
                    "verbosity level": 3,
                    #                     mesh_veryFine, fineMesh or coarseMesh
                    # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                    # "Flag_SecondOrder": 0,
                    "stop_criterion": 1e-7,
                    "res": join(self.main_test_dir, res_id),  # result folder
                },
                "pro": join(self.model_dir, "Toyota_Prius.pro"),  # pro file
                "gmsh": {"exe": GMSH_EXE},  # gmsh exe and params
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )

        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            fig, ax = plt.subplots()
            for phase in results["inducedVoltage"].keys():
                ax.plot(results["time"][1:], results["inducedVoltage"][phase])
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$U_\mathrm{ind}$ in V")

        assert np.isclose(
            np.mean([rms(results["inducedVoltage"][phase]) for phase in "abc"]),
            320,
            atol=15,
        ), "Calculated back emf for 6000 rpm does not match expected value!"


def rms(array) -> float:
    return np.sqrt(np.mean(array**2))


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
