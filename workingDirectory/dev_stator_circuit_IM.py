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
"""Create Model of IM from json test files and run simulation to compare with expected results"""
from __future__ import annotations

import logging
from os import makedirs
from os.path import isdir, isfile, join
from shutil import copytree, ignore_patterns, rmtree

import numpy as np
from matplotlib import pyplot as plt

from pyemmo.api.json.json import main
from pyemmo.functions.import_results import get_result_files, read_timetable_dat
from pyemmo.functions.runOnelab import runCalcforCurrent

# # disable messages of matplotlib
# logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
# logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

GETDP_EXE = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64_240901\getdp.exe"
GMSH_EXE = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64_240901\gmsh.exe"


class SimulationSetup:
    def __init__(self):
        self.setUpClass()

    @classmethod
    def setUpClass(cls):
        """
        Create model files depended on pro files
        """
        # copy model data and set actual model directory
        original_model_dir = join(r"D:\pyemmo\tests\data", "api", "json", "im")
        # folder to store temporary model data and simulation results
        cls.test_sim_dir = join(r"D:\pyemmo\Results", "TestCircuitSimulation")
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


# def tearDownClass(cls):
#     """
#     Vordefinierte teardown Funktion die einmalig am Ende der Testprozedur ausgeführt wird.
#     Nützlich für beispielsweise Löschen von in Test erzeugten Datein und Ordnern.
#     Konkret z.B. Löschen von abgespeicherten Geometrien
#     """
#     rmtree(cls.model_dir)
#     # remove any results folders that match the test res_id pattern
#     for folder in listdir(cls.test_sim_dir):
#         if fnmatch.fnmatch(folder, "test_*"):
#             rmtree(join(cls.test_sim_dir, folder))


def run_sim(resid: str, setup: SimulationSetup, clear_results: bool):
    # refernce data
    stator_resistance = 325.409e-3  # mOhm
    k_cu = 0.426479830954041  # fill factor winding
    # calc Rb[] = Factor_R_3DEffects * L_ax * k_cu * NbWires[]^2/SurfCoil[]/sigma[]
    # 140:  empirical correction factor to achive R_S given from expected results
    # 4:    Devide by symmetry factor to only give resistance in model
    k_endwinding = 2.787131 * 140 / 4  # end winding correction factor
    endring_resistance = 1.872971747498273e-06  # Ohm
    endring_inductance = 4.924650607446416e-09  # Henry

    # simulation parameters
    connection_type = "star"  # star connection via circuit
    U_input_pk = 153  # volt
    n = 1500  # rpm
    f_s = 52.478867971949249  # Hz
    f_r = f_s - n / 60 * 2  # 2.601763700396361 Hz
    s = f_r / f_s  # slip
    nbr_stator_periods = 24
    t_end = 24 / f_s  # seconds -> 3 stator period
    t_step = 1 / f_s / 16  #  steps per stator period
    nbr_time_steps = np.rint(t_end / t_step).astype(int) + 1
    initial_offset = 0  # degrees mech.

    # define simulation params
    param_dict = {
        "getdp": {
            "Flag_AnalysisType": 1,  # transient
            "Flag_NL": 1,  # 0: linear to speed up simulation
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
            "res": join(setup.test_sim_dir),  # result folder
            "ResId": resid,
            "Flag_ClearResults": clear_results,
            "Flag_PrintFields": 0,
            "Flag_Debug": 1,
            "exe": GETDP_EXE,
            "verbosity level": 3,
        },
        "gmsh": {"exe": GMSH_EXE},
        "pro": setup.script.proFilePath,
        # "res": self.script.resultsPath,
        # "hyst": 0, # loss coefficient
        # "eddy": 0, # loss coefficient
        # "exc": 0, # loss coefficient
    }
    results = runCalcforCurrent(param_dict)
    sim_res_folder = join(setup.test_sim_dir, resid)
    if ("R_A.dat") in get_result_files(sim_res_folder)[0]:
        _, resistance_A = read_timetable_dat(join(sim_res_folder, "R_A.dat"))
        results["resistance"] = {}
        results["resistance"]["A"] = resistance_A

    # check if voltages and other results are correct:
    time_ref = np.linspace(0, t_end, nbr_time_steps, endpoint=True)
    if param_dict["getdp"]["Flag_NL"]:
        f_relax = np.where(
            time_ref < (2 / f_s),
            0.5 * (1 - np.cos(np.pi * time_ref / (2 / f_s))),
            1,
        )
    else:
        f_relax = 1
    U_a_ref = (
        f_relax
        * U_input_pk
        * np.sin(2 * np.pi * f_s * time_ref + np.rad2deg(initial_offset))
    )
    U_a_sim = results["voltage"]["a"]

    fig, ax = plt.subplots(1, 2)
    ax[0].plot(results["time"], results["voltage"]["a"], ".-", label="U_{a,sim}")
    ax[0].plot(results["time"], results["voltage"]["b"], ".-", label="U_{b,sim}")
    ax[0].plot(results["time"], results["voltage"]["c"], ".-", label="U_{c,sim}")
    ax[0].set_title("Stator Voltage")
    ax[0].grid(True)
    ax[0].legend()
    ax[1].plot(results["time"], results["voltage"]["aw"], ".-", label="U_{i,a,sim}")
    ax[1].plot(results["time"], results["voltage"]["bw"], ".-", label="U_{i,b,sim}")
    ax[1].plot(results["time"], results["voltage"]["cw"], ".-", label="U_{i,c,sim}")
    ax[1].set_title("Stator Induced Voltage")
    ax[1].grid(True)
    ax[1].legend()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(time_ref, U_a_ref, "o-", label="U_{a,ref}")
    ax.plot(results["time"], U_a_sim, "x-", label="U_{a,sim}")
    ax.plot(results["time"], results["voltage"]["aw"], ".-", label="U_{i,w,a,sim}")
    ax.plot(
        results["time"][1:], results["inducedVoltage"]["a"], ".--", label="U_{i,a,sim}"
    )
    ax.set_title("Stator Voltage")
    ax.grid(True)
    ax.legend()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(U_a_ref.reshape(U_a_sim.shape) - U_a_sim, "x-")
    ax.grid(True)
    ax.set_title("Diviation in Stator Voltage")
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(results["current"]["a"], ".-", label="I_{a}")
    ax.plot(results["current"]["b"], ".-", label="I_{b}")
    ax.plot(results["current"]["c"], ".-", label="I_{c}")
    ax.grid(True)
    ax.set_title("Stator Current")
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(results["current"]["bars"], ".-")
    ax.grid(True)
    ax.set_title("Rotor Current")
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(results["time"], results["torque"], ".-")
    ax.grid(True)
    ax.set_title("Mean MST Torque of rotor and stator")
    fig.show()

    assert nbr_time_steps in U_a_sim.shape
    assert all(np.isclose(results["time"], time_ref, atol=t_step / 1e6))
    assert all(
        np.isclose(U_a_sim, U_a_ref.reshape(U_a_sim.shape), atol=U_input_pk / 1e6)
    )
    # TODO: make sure Ub = R_B * Ib + U_iB
    # NOTE: U_wB != U_iB
    #       U_wB = R_B * Ib + U_iB
    return results


sim_setup = SimulationSetup()
# results = run_sim("01", sim_setup, True)
