#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

# %%

import json
import logging
import os

from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import ROOT_DIR

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.INFO)

# %%
# ==============================================
# Determination of the machine to be calculated:
# ==============================================
# machine folder pyemmo
# machineFolder = os.path.join(ROOT_DIR, r"tests\data\api\pyleecan")
# machine folder pyleecan:
machineFolder = os.path.join(DATA_DIR, "Machine")

resFolder = os.path.join(ROOT_DIR, r"Results\pyleecanAPI")
if not os.path.isdir(resFolder):
    os.makedirs(resFolder)
machineList = []
for i, filename in enumerate(os.listdir(machineFolder)):
    if filename.endswith(".json") and not "FEMM" in filename:
        machineList.append(filename)
        print(f"{machineList.index(filename)}: " + filename)
# %%working machines
# Load data with info about working machine names
pylcn_machine_testfile = os.path.join(ROOT_DIR, r"Results\pyleecan_machine_test.json")
if os.path.isfile(pylcn_machine_testfile):
    # define filter function
    def filter_success(keyVal):
        """Filter function to search test for successfully translated machines"""
        _, value = keyVal
        if "success" in value:
            return True

    # load data from file
    with open(pylcn_machine_testfile, encoding="utf-8") as infile:
        pyleecan_machine_results_dict = json.load(infile)

    # Filter original dict for working machiness
    workingMachineDict = dict(
        filter(filter_success, pyleecan_machine_results_dict.items())
    )
    # get list IDs and print them
    for machineName in workingMachineDict.keys():
        if machineName in machineList:
            print(f"{machineList.index(machineName)}: " + machineName)

# %%
# Use machines:
# 4 (IPMSM, (missing wedge))
# 17 (SIPMSM, SlotW22 + SlotM11) - full model
# 31 (SynRM, SlotW11 (missing wedge) + HoleM54) - 1/4 model
# 34 (Prius, SlotW11 + HoleM50)
fileName = machineList[33]  # SELECT MACHINE HERE BY INDEX OR NAME
# fileName = "SIPMSM_002.json"  # SELECT MACHINE HERE BY INDEX OR NAME
print("\nUsing machine: " + fileName)
pyleecan_machine: Machine = load.load(  # pylint: disable=locally-disabled, no-member
    os.path.abspath(os.path.join(machineFolder, fileName))
)
# Workaround for wrong material
CuMat = load.load(os.path.join(DATA_DIR, "Material", "Copper2.json"))
try:
    if pyleecan_machine.rotor.winding.conductor.cond_mat.name == "Copper1":
        pyleecan_machine.rotor.winding.conductor.cond_mat = CuMat
except AttributeError:
    pass
except Exception as exce:
    raise exce
try:
    if pyleecan_machine.stator.winding.conductor.cond_mat.name == "Copper1":
        pyleecan_machine.stator.winding.conductor.cond_mat = CuMat
except AttributeError:
    pass
except Exception as exce:
    raise exce
pyleecanAPI.main(
    pyleecan_machine, model_dir=os.path.join(resFolder, pyleecan_machine.name)
)

# %%
