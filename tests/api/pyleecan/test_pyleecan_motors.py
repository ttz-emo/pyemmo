"""This module loads all the available pyleecan machines and trys to run the pyemmo api"""

# %%
import os
from typing import Union
import json

from pyleecan.definitions import DATA_DIR
from pyleecan.Functions import load

# from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineAsync import MachineAsync
from pyleecan.Classes.MachineSync import MachineSync

from pyemmo.definitions import ROOT_DIR
from pyemmo.api.pyleecan.get_translated_machine import get_translated_machine

MACHINE_FILE_DIR = os.path.join(DATA_DIR, "Machine")
machine_test_dict = {}
nbrTranslatedMaschines = 0
for machineFile in os.listdir(MACHINE_FILE_DIR):
    machinePath = os.path.join(MACHINE_FILE_DIR, machineFile)
    try:
        # pylint: disable=locally-disabled, no-member
        machine: Union[MachineAsync, MachineSync] = load.load(machinePath)
    except Exception as exce:
        machine_test_dict[machineFile] = (
            f"Could not load machine. Error: {exce}"
        )
    else:
        try:
            (
                movingband_r,
                magnetization_dict,
                geo_translation_dict,
            ) = get_translated_machine(machine)
        except Exception as exce:
            machine_test_dict[machineFile] = (
                f"Machine could not be translated. Error: {exce}"
            )
        else:
            machine_test_dict[machineFile] = "Machine successfully translated!"
            nbrTranslatedMaschines += 1
nbrMachinesTotal = len(os.listdir(MACHINE_FILE_DIR))
nbrFails = nbrMachinesTotal - nbrTranslatedMaschines
machine_test_dict["FINAL_RESULT"] = f"{nbrMachinesTotal} machines, {nbrTranslatedMaschines} tranlated, {nbrFails} failed"
print(machine_test_dict["FINAL_RESULT"])
# Write results to "Results" folder because its not tracked by Git.
with open(
    os.path.join(ROOT_DIR, "Results", "pyleecan_machine_test.json"),
    "w",
    encoding="utf-8",
) as jFile:
    # results = json.dumps(machine_test_dict)
    json.dump(machine_test_dict, jFile, indent=4)
