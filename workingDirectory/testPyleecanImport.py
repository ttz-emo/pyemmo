# %%
import os
import logging
import json

import numpy as np

from pyleecan.Functions import load
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Machine import Machine as PyleecanMachine
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.definitions import DATA_DIR, USER_DIR

# from pyemmo.functions.plot import plot
# from pyemmo.api.json.json import main
from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan.get_translated_machine import get_translated_machine
from pyemmo.api.pyleecan.create_pyleecan_simulation import create_simulation
from pyemmo.api.pyleecan.create_param_dict import create_param_dict
from pyemmo.api.pyleecan.main import main

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.INFO)

# %%
# ==============================================
# Determination of the machine to be calculated:
# ==============================================
# machine folder pyemmo
machineFolder = os.path.join(ROOT_DIR, "workingDirectory/machineData")
# machine folder pyleecan:
# machineFolder = os.path.join(DATA_DIR, "Machine")
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
pylcn_machine_testfile = os.path.join(
    ROOT_DIR, r"Results\pyleecan_machine_test.json"
)
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
        print(f"{machineList.index(machineName)}: " + machineName)

# %%
# Use machines:
# 4 (IPMSM, (missing wedge))
# 17 (SIPMSM, SlotW22 + SlotM11) - full model
# 31 (SynRM, SlotW11 (missing wedge) + HoleM54) - 1/4 model
# 34 (Prius, SlotW11 + HoleM50)
fileName = machineList[34]  # SELECT MACHINE HERE BY INDEX OR NAME
# fileName = "SIPMSM_002.json"  # SELECT MACHINE HERE BY INDEX OR NAME
print("\nUsing machine: " + fileName)
pyleecan_machine: Machine = (
    load.load(  # pylint: disable=locally-disabled, no-member
        os.path.abspath(os.path.join(machineFolder, fileName))
    )
)
main(
    pyleecan_machine, model_dir=os.path.join(resFolder, pyleecan_machine.name)
)

# %%
