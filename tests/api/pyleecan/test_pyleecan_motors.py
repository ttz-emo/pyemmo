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
#
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
from pyemmo.api.pyleecan.translate_machine import translate_machine

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
                all_bands,
                geometry_list,
                movingband_r,
                magnetization_dict,
                geo_translation_dict,
            ) = translate_machine(machine)
        except Exception as exce:
            machine_test_dict[machineFile] = (
                f"Machine could not be translated. Error: {exce}"
            )
        else:
            machine_test_dict[machineFile] = "Machine successfully translated!"
            nbrTranslatedMaschines += 1
nbrMachinesTotal = len(os.listdir(MACHINE_FILE_DIR))
nbrFails = nbrMachinesTotal - nbrTranslatedMaschines
machine_test_dict["FINAL_RESULT"] = (
    f"{nbrMachinesTotal} machines, {nbrTranslatedMaschines} tranlated, {nbrFails} failed"
)
print(machine_test_dict["FINAL_RESULT"])
# Write results to "Results" folder because its not tracked by Git.
with open(
    os.path.join(ROOT_DIR, "Results", "pyleecan_machine_test.json"),
    "w",
    encoding="utf-8",
) as jFile:
    # results = json.dumps(machine_test_dict)
    json.dump(machine_test_dict, jFile, indent=4)
