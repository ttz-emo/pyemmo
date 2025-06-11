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

import logging
import os

import numpy as np
from pyleecan.definitions import USER_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import runCalcforCurrent

# import subprocess


# from tests import TEST_DATA_DIR

GETDP_EXE = ""
GMSH_EXE = ""


def test_simulation_with_stator_circuit():
    # refernce data from Maxwell Simulation
    Br_magnets = 1.16  # Tesla
    l_axial = 84 * 1e-3  # milli meter
    R_ext_stator = 269.24 / 2 * 1e-3  # meter
    R_int_stator = 161.9 / 2 * 1e-3  # meter
    R_ext_rotor = 160.4 / 2 * 1e-3  # meter
    R_int_stator = 110.64 / 2 * 1e-3  # meter
    lamination_stacking_factor = 0.96
    # BH curve for rotor and stator core
    BH_curve = np.array(
        [
            [
                0,
                22.280000000000001,
                25.460000000000001,
                31.829999999999998,
                47.740000000000002,
                63.659999999999997,
                79.569999999999993,
                159.15000000000001,
                318.30000000000001,
                477.45999999999998,
                636.61000000000001,
                795.76999999999998,
                1591.5,
                3183,
                4774.6000000000004,
                6366.1000000000004,
                7957.6999999999998,
                15915,
                31830,
                111407,
                190984,
                350138,
                509252,
                560177.19999999995,
                1527756,
            ],
            [
                0,
                0.050000000000000003,
                0.10000000000000001,
                0.14999999999999999,
                0.35999999999999999,
                0.54000000000000004,
                0.65000000000000002,
                0.98999999999999999,
                1.2,
                1.28,
                1.3300000000000001,
                1.3600000000000001,
                1.4399999999999999,
                1.52,
                1.5800000000000001,
                1.6299999999999999,
                1.6699999999999999,
                1.8,
                1.8999999999999999,
                2.0,
                2.1000000000000001,
                2.2999999999999998,
                2.5,
                2.5639944940000001,
                3.7798898740000002,
            ],
        ]
    )
    N_coil = 9  # turns per coil
    R_strand = 500e-3  # Ohm

    # simulation parameters
    connection_type = "star"  # star connection via circuit
    V_in_pk = 100  # volt
    f = 50  # Hz
    n = 750  # rpm
    t_end = 0.06  # seconds -> 3 periods
    t_step = 0.005  # seconds
    initial_offset = -22.5  # degrees mech.

    # simulation results of last period (rough)
    I_out_rms = 82.4  # ampere
    I_out_pk2pk = 252  # ampere
    torque = 78.45  # newton meter

    ## CREATE MODEL FOR PRIUS MOTOR IN ONELAB

    # disable messages of matplotlib
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    logging.getLogger().setLevel(logging.INFO)

    machine_file_path = os.path.join(USER_DIR, "Machine", "Toyota_Prius.json")

    if not os.path.isfile(machine_file_path):  # make sure file exists
        raise FileNotFoundError(machine_file_path)

    # Default development results folder
    resFolder = os.path.join(ROOT_DIR, r"Results\pyleecanAPI")
    if not os.path.isdir(resFolder):
        os.makedirs(resFolder)  # create res dir if necessary

    # Load pyleecan machine object and call pyemmo-pyleecan-api
    # pylint: disable=locally-disabled, no-member
    pyleecan_machine = load.load(machine_file_path)  # load machine obj
    # %%
    # FIX: rotor bar material
    CuMat = load.load(os.path.join(USER_DIR, "Material", "Copper2.json"))
    pyleecan_machine.stator.winding.conductor.cond_mat = CuMat
    try:
        pyleecan_machine.rotor.winding.conductor.cond_mat = CuMat
    except AttributeError:
        pass
    except Exception as exce:
        raise exce

    # Call pyleecan api main function
    # This triggers the translation process via the pyemmo json api, creates the
    # model file for Gmsh and GetDP + opens the model in the Gmsh GUI.
    # This behaviour should be changed to e.g. return the model file path or the
    # whole pyemmo Script object so the user can open the GUI or run the simulation
    # directly...
    model_folder = os.path.join(resFolder, pyleecan_machine.name)
    pyemmo_script = pyleecanAPI.main(
        pyleecan_machine, model_dir=model_folder, use_gui=False
    )
    # %%

    # folder where simulation results will be stored
    sim_res_dir = os.path.join(model_folder, f"res_{pyleecan_machine.name}")

    # define simulation params
    i_d = -10
    i_q = 50
    n = 1000
    resid = f"id_{i_d}_iq_{i_q}_n_{n}rpm"
    param_dict = {
        "getdp": {
            "ID_RMS": i_d,  # d current in A
            "IQ_RMS": i_q,  # q current in A
            "RPM": n,  # speed in rpm
            "d_theta": 0.25,
            "ResId": resid,
            "Flag_PrintFields": 0,
            "Flag_Debug": 0,
        },
        "ResId": resid,
        "pro": pyemmo_script.proFilePath,
        "res": sim_res_dir,
        "exe": GETDP_EXE,
        "gmsh": GMSH_EXE,
        "verbosity level": 3,
        # "hyst": 0, # loss coefficient
        # "eddy": 0, # loss coefficient
        # "exc": 0, # loss coefficient
    }
    runCalcforCurrent(param_dict)
