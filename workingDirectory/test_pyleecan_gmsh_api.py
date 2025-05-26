# %%
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
from os import makedirs
from os.path import isdir, join

import gmsh
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.Output import Output
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.definitions import DATA_DIR as PYLEECAN_DATA_DIR
from pyleecan.Functions import load
from pyleecan.Functions.GMSH.draw_GMSH import draw_GMSH
from pyleecan.Methods.Simulation.MagElmer import (
    MagElmer_BP_dict,
)

from pyemmo.definitions import ROOT_DIR

mesh_dict = {
    "Lamination_Rotor_Bore_Radius_Ext": 180,
    "surface_line_0": 5,
    "surface_line_1": 10,
    "surface_line_2": 5,
    "surface_line_3": 5,
    "surface_line_4": 10,
    "surface_line_5": 5,
    "Lamination_Stator_Bore_Radius_Int": 10,
    "Lamination_Stator_Yoke_Side_Right": 30,
    "Lamination_Stator_Yoke_Side_Left": 30,
    "int_airgap_arc": 120,
    "int_sb_arc": 120,
    "ext_airgap_arc": 120,
    "ext_sb_arc": 120,
    "airbox_line_1": 10,
    "airbox_line_2": 10,
    "airbox_arc": 20,
}

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.DEBUG)
# %%
# ==============================================
# Determination of the machine to be calculated:
# ==============================================
# machine folder pyemmo
# machineFolder = os.path.join(TEST_DIR, "data", "api", "pyleecan")
# machine folder pyleecan:
machineFolder = os.path.join(PYLEECAN_DATA_DIR, "Machine")
resFolder = os.path.join(ROOT_DIR, r"Results\Pyleecan_Gmsh_API")
if not os.path.isdir(resFolder):
    os.makedirs(resFolder)
machineList: list[Machine] = []
for i, filename in enumerate(os.listdir(machineFolder)):
    if filename.endswith(".json") and not "FEMM" in filename:
        machineList.append(filename)
        print(f"{machineList.index(filename)}: " + filename)

# # %%working machines
# # Load data with info about working machine names
# pylcn_machine_testfile = os.path.join(ROOT_DIR, r"Results\pyleecan_machine_test.json")
# if os.path.isfile(pylcn_machine_testfile):
#     # define filter function
#     def filter_success(keyVal):
#         """Filter function to search test for successfully translated machines"""
#         _, value = keyVal
#         if "success" in value:
#             return True

#     # load data from file
#     with open(pylcn_machine_testfile, encoding="utf-8") as infile:
#         pyleecan_machine_results_dict = json.load(infile)

#     # Filter original dict for working machiness
#     workingMachineDict = dict(
#         filter(filter_success, pyleecan_machine_results_dict.items())
#     )
#     # get list IDs and print them
#     print(f"Translateable machines from {machineFolder}")
#     for machineName in workingMachineDict.keys():
#         if machineName in machineList:
#             print(f"{machineList.index(machineName)}: " + machineName)

# %%
for i, machine_filename in enumerate(machineList[6:]):
    print(f"Current Machine {i}: {machine_filename}")
    machine: Machine = load.load(  # pylint: disable=locally-disabled, no-member
        os.path.abspath(os.path.join(machineFolder, machine_filename))
    )
    # Import the machine from a script
    save_path = join(resFolder, machine.name)
    if not isdir(save_path):
        makedirs(save_path)
    # fileName = "SIPMSM_002.json"  # SELECT MACHINE HERE BY INDEX OR NAME
    # # Workaround for wrong material
    # # pylint: disable=locally-disabled, no-member
    # CuMat = load.load(os.path.join(PYLEECAN_DATA_DIR, "Material", "Copper2.json"))
    # try:
    #     if pyleecan_machine.rotor.winding.conductor.cond_mat.name == "Copper1":
    #         pyleecan_machine.rotor.winding.conductor.cond_mat = CuMat
    # except AttributeError:
    #     pass
    # except Exception as exce:
    #     raise exce
    # try:
    #     if pyleecan_machine.stator.winding.conductor.cond_mat.name == "Copper1":
    #         pyleecan_machine.stator.winding.conductor.cond_mat = CuMat
    # except AttributeError:
    #     pass
    # except Exception as exce:
    #     raise exce

    # Try the pyleecan internal gmsh api
    try:
        # Create the Simulation
        mySimu = Simu1(name="test_gmsh", machine=machine)
        myResults = Output(simu=mySimu)
        sim, is_anti_periodic = machine.comp_periodicity_spatial()
        model_file_save_path = join(
            save_path, f"{machine.name}_noSlidingBand.geo_unrolled"
        )
        print(model_file_save_path)
        is_drawn = False
        gmsh_dict = draw_GMSH(
            output=myResults,
            sym=sim * 2 if is_anti_periodic else 1,
            boundary_prop=MagElmer_BP_dict,
            is_lam_only_S=False,
            is_lam_only_R=False,
            user_mesh_dict={},  # mesh_dict,
            is_sliding_band=True,
            is_airbox=True,
            path_save=model_file_save_path,
        )
        is_drawn = True
    except Exception as e:
        print(f"Error while drawing GMSH: {e}")
        continue

    if is_drawn:
        gmsh.initialize()
        if not gmsh.model.getCurrent():
            gmsh.open(model_file_save_path)
        gmsh.fltk.run()
        gmsh.finalize()

    # with open("test_gmsh_ipm.json", "w") as fw:
    #     json.dump(gmsh_dict, fw, indent=4)

# %%
