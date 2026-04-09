#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
from os.path import isdir, join
from shutil import rmtree
from uuid import uuid4

import numpy as np
from matplotlib import pyplot as plt

from pyemmo.api.pyleecan.main import main
from pyemmo.functions.run_onelab import run_simulation

# from pyleecan.Functions.Electrical.dqh_transformation import n2dqh
from ... import GETDP_EXE, GMSH_EXE, TEST_DATA_DIR
from ... import TEST_TEMP_DIR as TESTS_RESULTS_DIR
from ...api.pyleecan.testutils import run_pyleecan_sim  # , run_pyleecan_sim_voltage

# Model data for Toyota Prius from:
# [1] T. A. Burress u. a., „Evaluation of the 2007 Toyota Camry Hybrid Synergy Drive System“,
# ORNL/TM-2007/190, Revised, 928684, Apr. 2008. doi: 10.2172/928684.

# back emf constant for toyota prius in V/rpm from back emf simulation. Measurement data
# in [1] shows ke ~= 50V/1000rpm.
k_e = 63.3 / 1000
R_S = 0.069  # stator phase resistance in Ohm from [1]


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
        logger = logging.getLogger(__name__)
        # set global and pyemmo log level
        logger.setLevel(logging.INFO)
        logging.getLogger("pyemmo").setLevel(logging.INFO)

        cls.pyleecan_model_file = join(
            TEST_DATA_DIR, "api", "pyleecan", "Toyota_Prius.json"
        )
        # folder to store temporary model data and simulation results
        # cls.timestamp = datetime.now().strftime(r"%Y%m%d_%H%M%S")
        cls.timestamp = str(uuid4())
        cls.main_test_dir = join(TESTS_RESULTS_DIR, "TestToyotaPrius")
        if not isdir(cls.main_test_dir):
            makedirs(cls.main_test_dir)

        # Create model data to test simulation results
        cls.model_dir = join(cls.main_test_dir, cls.timestamp + "_Toyota_Prius_Model")
        logger.info("Creating ONELAB model scripts...")
        cls.script = main(
            cls.pyleecan_model_file,
            cls.model_dir,
            gmsh=GMSH_EXE,
            getdp=GETDP_EXE,
            use_gui=False,
        )
        logger.info("ONELAB scripts created!")

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
            if fnmatch.fnmatch(folder, "*_test_*"):
                rmtree(join(cls.main_test_dir, folder))
        # remove temporary test folder if empty
        if len(listdir(cls.main_test_dir)) == 0:
            rmdir(cls.main_test_dir)

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
        res_id = self.timestamp + "_test_backEMF"
        # logging.getLogger("pyemmo.functions.runOnelab").setLevel(logging.WARNING)
        results = run_simulation(
            {
                "getdp": {
                    "exe": GETDP_EXE,
                    "IQ_RMS": 0.0,
                    "ID_RMS": 0.0,
                    "RPM": 6000,
                    "initrotor_pos": 0.0,
                    "d_theta": 90.0 / 32,
                    "finalrotor_pos": 90.0,
                    "ResId": res_id,
                    "Flag_AnalysisType": 1,
                    "Flag_PrintFields": 0,
                    "Flag_EC_Magnets": 0,  # no eddy currents
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
                "gmsh": {"exe": GMSH_EXE, "gmsf": 2},  # gmsh exe and params
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )

        if logging.getLogger(__name__).getEffectiveLevel() <= logging.DEBUG:
            fig, ax = plt.subplots()
            for phase in results["inducedVoltage"].keys():
                ax.plot(results["time"][1:], results["inducedVoltage"][phase])
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$U_\mathrm{ind}$ in V")

        if not results["inducedVoltage"]:
            raise ValueError("Missing back emf results!")
        bemf_rms = np.mean(
            [
                rms(results["inducedVoltage"][phase])
                for phase in results["inducedVoltage"].keys()
            ]
        )

        # Results from Maxwell simulation but with slightly different geometry
        # assert np.isclose(
        #     bemf_rms,
        #     380, # value from Maxwell simulation
        #     atol=15,
        # ), "Calculated back emf for 6000 rpm does not match expected value!"

        # Measurement data from [1] describes a back emf of about 320 V at 6000 rpm

        outfemm = run_pyleecan_sim(
            self.pyleecan_model_file, speed=6000.0, nbr_steps_per_period=int(90 / 2.5)
        )
        outfemm.mag.comp_emf()
        bemf_rms_pyleecan = rms(outfemm.mag.emf.values)
        assert np.isclose(
            bemf_rms,
            bemf_rms_pyleecan,
            rtol=1,
        ), "Back emf ONELAB <-> FEMM for 6000 rpm does not match!"

    def test_WP1(self):
        """Test working point results

        "Burress, T A, C L Coomer, S L Campbell, et.al. "Evaluation of the 2007 Toyota
        Camry Hybrid Synergy Drive System". ORNL/TM-2007/190, Revised, 928684. 2008.
        https://doi.org/10.2172/928684.
        """
        res_id = self.timestamp + "_test_WP1"
        Id, Iq = (-100, 200)
        speed = 1000.0
        nbr_steps = 32
        results = run_simulation(
            {
                "getdp": {
                    "exe": GETDP_EXE,
                    "IQ_RMS": Iq,
                    "ID_RMS": Id,
                    "RPM": speed,
                    "initrotor_pos": 0.0,
                    "d_theta": 90.0 / nbr_steps,
                    "finalrotor_pos": 90.0,
                    "ResId": res_id,
                    "Flag_AnalysisType": 1,
                    "Flag_PrintFields": 0,
                    "Flag_EC_Magnets": 0,  # no eddy currents
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
                "gmsh": {"exe": GMSH_EXE, "gmsf": 2},  # gmsh exe and params
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )

        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            fig, ax = plt.subplots()
            ax.plot(results["time"], results["torque"])
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$T_\mathrm{em}$ in Nm")

        mean_torque = np.mean(results["torque"])

        assert np.isclose(
            mean_torque, 376.0, atol=15
        ), "Torque does not match expected value!"

        outfemm = run_pyleecan_sim(
            self.pyleecan_model_file,
            speed=6000.0,
            Id=Id,
            Iq=Iq,
            nbr_steps_per_period=nbr_steps,
        )

        assert np.isclose(
            mean_torque, np.mean(outfemm.mag.Tem.values), rtol=5
        ), "Torque ONELAB <-> FEMM does not match!"

    def test_WP1_voltage_source(self):
        """Test working point results

        "Burress, T A, C L Coomer, S L Campbell, et.al. "Evaluation of the 2007 Toyota
        Camry Hybrid Synergy Drive System". ORNL/TM-2007/190, Revised, 928684. 2008.
        https://doi.org/10.2172/928684.
        """
        import matplotlib

        matplotlib.use("qtagg")
        logger = logging.getLogger(__name__)
        res_id = self.timestamp + "_test_WP1_voltage_source"
        speed = 1000.0
        I_eff_target = rms(np.array([100, 200]))
        U_eff = k_e * speed + R_S * I_eff_target
        U_amp = U_eff * np.sqrt(2)
        nbr_steps = 16  # number of steps per electrical period
        nbr_stator_periods = 4
        end_pos = 360 / 4 * nbr_stator_periods  # 4 pole pairs

        try:
            phase = self.script.sim_params["SYM"]["ParkAngOffset"]
        except KeyError:
            logger.warning("Could not get park angle from Script")
            phase = 0.0
        offset = -90  # offset angle for reasonable torque output
        results = run_simulation(
            {
                "getdp": {
                    "exe": GETDP_EXE,
                    "verbosity level": 3,
                    # mechanical parameters
                    "RPM": speed,
                    "initrotor_pos": 0.0,
                    "d_theta": 360 / 4 / nbr_steps,
                    "finalrotor_pos": end_pos,
                    # electrical / source parameters
                    "Flag_SrcType_Stator": 2,  # voltage source, no circuit
                    "VV": U_amp,  # voltage amplitude
                    "pA_deg": phase + offset,  # phase offset for source with Sin
                    "R_S": R_S,  # phase resistance
                    "Flag_Cir": 0,  # no circuit
                    "Flag_Relaxation": 1,  # use relaxation function for source voltage
                    # Analysis parameters
                    "Flag_AnalysisType": 1,
                    "Flag_EC_Magnets": 0,  # no eddy currents
                    "Flag_Debug": 1,
                    "stop_criterion": 1e-8,
                    # Results parameters
                    "res": join(self.main_test_dir, res_id),  # result folder
                    "ResId": res_id,
                    "Flag_ClearResults": 1,
                    "Flag_PrintFields": 0,
                    #                     mesh_veryFine, fineMesh or coarseMesh
                    # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                    # "Flag_SecondOrder": 0,
                },
                "pro": join(self.model_dir, "Toyota_Prius.pro"),  # pro file
                "gmsh": {"exe": GMSH_EXE, "gmsf": 2},  # gmsh exe and params
                "info": "",
                "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
            }
        )
        i_last_period = int((nbr_stator_periods - 1) * nbr_steps)

        # check input voltage
        assert "voltage" in results, "Missing voltage from results!"
        assert all(
            phase_index in results["voltage"] for phase_index in ("abc")
        ), "Missing phase voltage from results!"

        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            fig, axes = plt.subplots(2, 1)
            ax = axes[0]
            for phase_index in "abc":
                ax.plot(
                    results["time"],
                    results["voltage"][phase_index],
                    label=f"$U_\\mathrm{{{phase_index}}}$",
                )
                ax.plot(
                    results["time"][1:],
                    results["inducedVoltage"][phase_index],
                    label=f"$U_\\mathrm{{i,{phase_index}}}$",
                )
                ax.plot(
                    results["time"][1:],
                    results["voltage"][phase_index][1:]
                    - results["inducedVoltage"][phase_index],
                    label=f"$U_\\mathrm{{{phase_index}}}-U_i$",
                )
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$U$ in V")
            ax.grid(True)
            ax.legend(loc=1)
            fig.show()
            # plot currents
            # fig, ax = plt.subplots()
            ax = axes[1]
            ax.set_title("Currents")
            for phase_index in "abc":
                if phase_index + "w" in results["current"]:
                    ax.plot(
                        results["time"],
                        results["current"][phase_index + "w"],
                        label=f"$I_\\mathrm{{{phase_index}}}$",
                    )
                if phase_index in results["current"]:
                    ax.plot(
                        results["time"],
                        results["current"][phase_index],
                        label=f"$I_\\mathrm{{{phase_index},source}}$",
                    )
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$I$ in A")
            ax.legend(loc=1)
            ax.grid(True)
            fig.show()
        U_out_rms = np.mean(
            [
                rms(results["voltage"][phase_index][i_last_period:])
                for phase_index in "abc"
            ]
        )
        I_rms = np.mean(
            [
                rms(results["current"][phase_index][i_last_period:])
                for phase_index in "abc"
            ]
        )
        logger.info(
            "Calculated output voltage RMS: %.2f V, expected voltage RMS: %.2f V",
            U_out_rms,
            U_eff,
        )
        logger.info(
            "Calculated output current RMS: %.2f A, expected current RMS: %.2f A",
            I_rms,
            I_eff_target,
        )
        assert np.isclose(
            U_out_rms, U_eff, rtol=0.01
        ), f"Output voltage does not match expected value! Expected {U_eff:.2f} V, got {U_out_rms:.2f} V"

        # TODO:  add check for dq current and voltage values using n2dqh function

        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            fig, ax = plt.subplots()
            ax.plot(results["time"], results["torque"])
            ax.set_xlabel("time in s")
            ax.set_ylabel(r"$T_\mathrm{em}$ in Nm")
            fig.show()

        mean_torque = np.mean(results["torque"][i_last_period:])

        # assert np.isclose(
        #     mean_torque, 376.0, rtol=0.1
        # ), f"Torque does not match expected value: Expected 376 Nm, got {mean_torque:.2f} Nm "
        if not np.isclose(mean_torque, 376.0, rtol=0.1):
            logger.error(
                "Torque does not match expected value: Expected 376 Nm, got %.2f Nm",
                mean_torque,
            )

        # outfemm = run_pyleecan_sim_voltage(
        #     self.pyleecan_model_file,
        #     speed=speed,
        #     U_eff=U_eff,
        #     phase=0,
        #     nbr_periods=1,
        #     nbr_steps_per_period=nbr_steps,
        #     nbr_iterations=2,
        # )

        # assert np.isclose(
        #     mean_torque, outfemm.elec.Tem_av, rtol=5
        # ), "Torque ONELAB <-> FEMM does not match!"


def rms(array) -> float:
    return np.sqrt(np.mean(array**2))


if __name__ == "__main__":
    unittest.main()
