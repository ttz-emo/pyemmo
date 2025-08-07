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
from os import listdir, makedirs
from os.path import isdir, isfile, join
from shutil import copytree, ignore_patterns, rmtree

import numpy as np
from matplotlib import pyplot as plt

from pyemmo.api.json.json import main
from pyemmo.functions.runOnelab import runCalcforCurrent
from tests import GETDP_EXE, GMSH_EXE, TEST_DATA_DIR
from tests import TEST_TEMP_DIR as TESTS_RESULTS_DIR

# # disable messages of matplotlib
# logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
# logging.getLogger().setLevel(logging.INFO)


class TestCircuitSimulation(unittest.TestCase):
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
        original_model_dir = join(TEST_DATA_DIR, "api", "json", "im")
        # folder to store temporary model data and simulation results
        cls.test_sim_dir = join(TESTS_RESULTS_DIR, "TestCircuitSimulation")
        if not isdir(cls.test_sim_dir):
            makedirs(cls.test_sim_dir)
        # copy model data to test simulation results directory
        model_dir = join(cls.test_sim_dir, "induction_machine")
        if isdir(model_dir):
            # remove old data before creating new model
            rmtree(model_dir)
        cls.model_dir = copytree(
            original_model_dir,
            model_dir,
            ignore=ignore_patterns("res*", "*.msh", "*.db", "*.res", "*.pre"),
        )
        # create model
        model_json_file = join(cls.model_dir, "im.json")
        info_json_file = join(cls.model_dir, "simu_info.json")
        cls.script = main(model_json_file, info_json_file, cls.model_dir)
        if not isfile(cls.script.proFilePath):
            raise FileExistsError(
                f"Model directory {model_dir} already exists but does not "
                f"contain the expected files ({cls.script.proFilePath})."
            )
        logging.getLogger().setLevel(logging.DEBUG)

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

    def test_simulation_with_stator_circuit(self):
        # refernce data
        stator_resistance = 325.409e-3  # mOhm
        k_cu = 0.426479830954041  # fill factor winding
        # calc Rb[] = Factor_R_3DEffects*L_ax * k_cu * NbWires[]^2/SurfCoil[]/sigma[]
        k_endwinding = 1  # end winding correction factor
        endring_resistance = 1.872971747498273e-06  # Ohm
        endring_inductance = 4.924650607446416e-09  # Henry

        # simulation parameters
        connection_type = "star"  # star connection via circuit
        U_input_pk = 153  # volt
        n = 1500  # rpm
        f_s = 52.478867971949249  # Hz
        f_r = f_s - n / 60 * 2  # 2.601763700396361 Hz
        s = f_r / f_s  # slip
        t_end = 2 / f_s  # seconds -> 3 stator period
        t_step = 1 / f_s / 30  # 30 steps per stator period
        nbr_time_steps = np.rint(t_end / t_step).astype(int) + 1
        initial_offset = 0  # degrees mech.

        # define simulation params
        resid = "star_connection"
        param_dict = {
            "getdp": {
                "Flag_AnalysisType": 1,  # transient
                "Flag_NL": 0,  # linear to speed up simulation
                # machine parameters
                "FillFactor_Winding": k_cu,
                "Factor_R_3DEffects": k_endwinding,
                # analysis parameters
                "initrotor_pos": initial_offset,  # initial rotor position in degrees
                "RPM": n,  # speed in rpm
                "d_theta": n / 60 * 360 * t_step,
                "finalrotor_pos": initial_offset + n / 60 * 360 * t_end,
                # excitation parameters
                "Flag_SrcType_Stator": 2,  # voltage source
                "freq_rotor": f_r,
                "VV": U_input_pk,  # amplitude of voltage
                "R_wire": 1e-12,  # connection resistance (None)
                "CircuitConnection": 0,  # 0: star, 1:delta
                "pA_deg": initial_offset,
                "R_endring_segment": endring_resistance,
                "L_endring_segment": endring_inductance,
                # results parameter
                "res": join(self.test_sim_dir, "res"),  # result folder
                "ResId": resid,
                "Flag_ClearResults": True,
                "Flag_PrintFields": 0,
                "Flag_Debug": 0,
                "exe": GETDP_EXE,
                "verbosity level": 5,
            },
            "gmsh": {"exe": GMSH_EXE},
            "pro": self.script.proFilePath,
            # "res": self.script.resultsPath,
            # "hyst": 0, # loss coefficient
            # "eddy": 0, # loss coefficient
            # "exc": 0, # loss coefficient
        }
        results = runCalcforCurrent(param_dict)

        # check if voltages and other results are correct:
        time_ref = np.linspace(0, t_end, nbr_time_steps, endpoint=True)
        U_a_ref = U_input_pk * np.sin(
            2 * np.pi * f_s * time_ref + np.rad2deg(initial_offset)
        )
        U_a_sim = results["voltage"]["a"]

        fig, ax = plt.subplots()
        ax.plot(time_ref, U_a_ref, "o-")
        ax.plot(results["time"], U_a_sim, "x-")
        ax.grid(True)
        fig.show()

        fig, ax = plt.subplots()
        ax.plot(U_a_ref.reshape(U_a_sim.shape) - U_a_sim, "x-")
        ax.grid(True)
        fig.show()

        assert nbr_time_steps in U_a_sim.shape
        assert all(np.isclose(results["time"], time_ref, atol=t_step / 100))
        assert all(
            np.isclose(U_a_sim, U_a_ref.reshape(U_a_sim.shape), atol=U_input_pk / 100)
        )


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
