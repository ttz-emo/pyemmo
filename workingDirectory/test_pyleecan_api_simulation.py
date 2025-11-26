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
"""Test script for pyleecan api with subsequent simulation"""
# %%
from __future__ import annotations

import logging
import os
import time

import numpy as np
from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR as PYLEECAN_DATA_DIR
from pyleecan.definitions import USER_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import findGetDP, runCalcforCurrent

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.DEBUG)

# %%
# ==============================================
# Determination of the machine to be calculated:
# ==============================================
# machine folder pyemmo
# machineFolder = os.path.join(TEST_DIR, "data", "api", "pyleecan")
# machine folder pyleecan:
machineFolder = os.path.join(PYLEECAN_DATA_DIR, "Machine")
resFolder = os.path.join(ROOT_DIR, r"Results\pyleecanAPI")
if not os.path.isdir(resFolder):
    os.makedirs(resFolder)
machineList = []
for i, filename in enumerate(os.listdir(machineFolder)):
    if filename.endswith(".json") and not "FEMM" in filename:
        machineList.append(filename)
        print(f"{machineList.index(filename)}: " + filename)
# %%
# Use machines:
# 4 (IPMSM, (missing wedge))
# 17 (SIPMSM, SlotW22 + SlotM11) - full model
# 31 (SynRM, SlotW11 (missing wedge) + HoleM54) - 1/4 model
# 34 (Prius, SlotW11 + HoleM50)

# SELECT MACHINE HERE BY INDEX OR NAME
# fileName = machineList[33]
fileName = "LSRPM_001.json"
# fileName = "Toyota_Prius_6phases.json"

print("\nUsing machine: " + fileName)
pyleecan_machine: Machine = (
    load.load(  # pylint: disable=locally-disabled, no-member # type: ignore
        os.path.abspath(os.path.join(machineFolder, fileName))
        # os.path.abspath(os.path.join(USER_DIR, "Machine", "Toyota_Prius_complex.json"))
    )
)
# %%
# Run PyEMMO Pyleecan api
pyemmo_script = pyleecanAPI.main(
    pyleecan_machine,
    model_dir=os.path.join(resFolder, pyleecan_machine.name),  # type: ignore
    use_gui=True,
)
# %%
# Run Simulation over one elec period


# Simulation parameters
n = 1500
id = -10
iq = 50
resId = "test_simulation"  # result identifier and result folder name

# create param dict for simulation
param_dict = {
    # model .pro file path
    "pro": pyemmo_script.proFilePath,
    # Gmsh Parameters
    "gmsh": {
        "exe": r"",
        "gmsf": 2,
        "verbosity level": 2,
    },
    # GetDP Parameters
    "getdp": {
        "exe": findGetDP(),  # GetDP executable, you can use the function findGetDP
        # which tries to find the exe on you PC.
        # change gmsh and getdp verbosity level (0-99)
        # 0 - fatal, 1 - error, 2 - warning, 3 - info, 5 - debug, 99 - extended debug
        "verbosity level": 3,
        "Flag_Debug": 0,  # epxort debug infos and results from GetDP
        ## Analysis Parameters
        "Flag_AnalysisType": 0,  # 0 - static, 1 - transient
        "Flag_SrcType_Stator": 1,  # 1 - current source, 2 - voltage source (not finally implemented)
        "initrotor_pos": 0.0,  # initial rotor position in °
        "d_theta": 1,  # angular step size in °
        "finalrotor_pos": 45,  # final rotor position in °
        # "RPM": n, # rotational speed
        "Flag_EC_Magnets": 0,  # control magnet eddy current calculation
        #
        ## Result settings
        "res": pyemmo_script.resultsPath,  # main results folder
        "ResId": resId,  # current simulation result folder ID
        "Flag_PrintFields": 0,  # control field result output (.pos files, only last timestep)
        "Flag_ClearResults": 1,  # remove results if existing, otherwise existing results will be imported
        #
        ## Excitation parameters
        "ID_RMS": id / np.sqrt(2),
        "IQ_RMS": iq / np.sqrt(2),
    },
    # "log": f"{resId}.log",  # optional: log file name
    "info": "",  # optional: info string to save with simulation config
    "datetime": time.ctime(),  # optional: current time
    "PostOp": [],  # PostOperations to execute after simulation.
    # Standard Option is: GetBOnRadius
}
# run simulation:
results = runCalcforCurrent(param_dict)
