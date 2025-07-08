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
import fnmatch
import unittest
from os import listdir, makedirs
from os.path import isdir, isfile, join
from shutil import copytree, ignore_patterns, rmtree

from pyemmo.functions.runOnelab import findGetDP, findGmsh, runCalcforCurrent
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
        original_model_dir = join(
            TEST_DATA_DIR, "api", "pyleecan", "comparison_base", "Toyota_Prius"
        )
        # folder to store temporary model data and simulation results
        cls.test_sim_dir = join(TESTS_RESULTS_DIR, "TestRunOnelab")
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

        res_id = "test_runOnelab"
        runCalcforCurrent(
            {
                "getdp": {
                    "IQ_RMS": 10.0,
                    "ID_RMS": 0.0,
                    "RPM": 1000,
                    "initrotor_pos": 0.0,
                    "d_theta": 5,
                    "finalrotor_pos": 15,
                    "ResId": res_id,
                    "Flag_AnalysisType": 1,
                    "Flag_PrintFields": 0,
                    "Flag_Debug": 1,
                    "Flag_ClearResults": 1,
                    "verbosity level": 3,
                    #                     mesh_veryFine, fineMesh or coarseMesh
                    # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                    # "Flag_SecondOrder": 0,
                    "stop_criterion": 1e-8,
                },
                "ResId": res_id,
                "pro": join(self.model_dir, "Toyota_Prius.pro"),
                "res": self.test_sim_dir,
                "exe": findGetDP(),
                "gmsh": findGmsh(),
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
