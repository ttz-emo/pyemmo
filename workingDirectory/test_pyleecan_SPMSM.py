# %%
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied
# Sciences Wuerzburg-Schweinfurt.
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
"""This tutorial script shows how to use the pyemmo api to create a ONELAB
model of a pyleecan machine."""
from __future__ import annotations

import logging

# %%
import os

from pyleecan.definitions import USER_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import ROOT_DIR

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.INFO)

# %%
# Machine and results folder definition:

# We are using the standard prius machine from the tests folder for now...
# machine_file_path = os.path.join(
#     ROOT_DIR, r"tests\data\api\pyleecan\Toyota_Prius.json"
# )
DATA_DIR = USER_DIR
machine_file_list = [
    "Toyota_Prius.json",
    "SIPMSM_001.json",
    "Railway_Traction_noDucts.json",
]

machine_file_path = os.path.join(DATA_DIR, "Machine", machine_file_list[0])
# machine_file_path = r"D:\pyemmo\tests\data\api\pyleecan\03_synrm_muster_Bachelor.json"

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
CuMat = load.load(os.path.join(DATA_DIR, "Material", "Copper2.json"))
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
pyleecanAPI.main(pyleecan_machine, model_dir=model_folder)
# %%
#
geo_file = os.path.join(model_folder, pyleecan_machine.name + ".geo")
pro_file = os.path.join(model_folder, pyleecan_machine.name + ".pro")
# folder where simulation results will be stored
# sim_res_dir = os.path.join(model_folder, f"res_{pyleecan_machine.name}")

# # define simulation params
# i_d = -10
# i_q = 50
# n = 1000
# resid = f"id_{i_d}_iq_{i_q}_n_{n}rpm"
# param_dict = {
#     "getdp": {
#         "ID_RMS": i_d,  # d current in A
#         "IQ_RMS": i_q,  # q current in A
#         "RPM": n,  # speed in rpm
#         "d_theta": 0.25,
#         "ResId": resid,
#         "Flag_PrintFields": 0,
#         "Flag_Debug": 0,
#     "exe": findGetDP(),
#     },
#     "ResId": resid,
#     "pro": pro_file,
#     "res": sim_res_dir,
#     "gmsh": {"exe": findGmsh()},
#     # "hyst": 0, # loss coefficient
#     # "eddy": 0, # loss coefficient
#     # "exc": 0, # loss coefficient
# }
# runCalcforCurrent(param_dict)
