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
"""This module loads all the available pyleecan machines and trys to run the pyemmo api"""

from __future__ import annotations

import json
import logging

# %%
import os
import traceback
from os.path import join

from pyleecan.Classes.Machine import Machine
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan.main import main
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import main as run_onelab

logging.getLogger().setLevel(logging.INFO)


MODEL_RES_DIR = join(ROOT_DIR, "Results", "pyleecanAPI")
MACHINE_FILE_DIR = join(DATA_DIR, "Machine")
machine_test_dict = {}
nbrTranslatedMaschines = 0
nbr_simulated_machines = 0
machine_file_list = os.listdir(MACHINE_FILE_DIR)
nbr_machines = len(machine_file_list)

# pylint: disable=locally-disabled, no-member
CuMat = load.load(os.path.join(DATA_DIR, "Material", "Copper2.json"))

for num, machineFile in enumerate(os.listdir(MACHINE_FILE_DIR)):
    print(f"Machine {num}/{nbr_machines} - {num/nbr_machines*100:.1f}% - {machineFile}")
    machinePath = join(MACHINE_FILE_DIR, machineFile)
    try:
        # pylint: disable=locally-disabled, no-member
        machine: Machine = load.load(machinePath)
        try:
            if "Copper1" in machine.stator.winding.conductor.cond_mat.name:
                machine.stator.winding.conductor.cond_mat = CuMat
            if "Copper1" in machine.rotor.winding.conductor.cond_mat.name:
                machine.rotor.winding.conductor.cond_mat = CuMat
        except AttributeError:
            pass
        except Exception as exce:
            raise exce
    except Exception as exce:
        machine_test_dict[machineFile] = f"Could not load machine. Error: {exce}"
    else:
        try:
            if not machine.rotor.is_internal:
                raise NotImplementedError("Outer rotor machine")
            machine_model_dir = join(MODEL_RES_DIR, machine.name)
            main(machine, machine_model_dir, use_gui=False)
        except Exception as exce:
            tb_str = "".join(traceback.format_tb(exce.__traceback__))
            machine_test_dict[machineFile] = (
                f"TRANSLATION FAILED! Error: {exce}\nDetail:\n{tb_str}"
            )
        else:
            try:
                stderr = run_onelab(
                    onelabFile=join(machine_model_dir, machine.name + ".pro"),
                    use_gui=False,
                    paramDict={
                        # "freq_rotor": f_r,
                        "I_eff": 10,
                        "IQ_RMS": 10,
                        # "RPM": float(n),
                        # "initrotor_pos": 0.0,
                        # "nbrStatorPeriods": nbr_stator_periods,
                        # "nbrStepsPerPeriod": nbr_steps_per_period,
                        # "d_theta": winkelschritt,
                        # "ResId": resId,
                        "Flag_AnalysisType": 0,
                        # "Flag_PrintFields": 0,
                        # "Flag_Debug": 1,
                        "Flag_ClearResults": 1,
                        # "verbosity level": 3,
                        # # "AxialLength_R": 1,
                        # # "AxialLength_S": 1,
                        # "NbrParallelPaths": 1,
                        # "R_endring_segment": 16e-7
                        # / 2,  # Initial value: 16e-7,
                        # "L_endring_segment": 2e-9 / 2,
                        # "Flag_Cir_RotorCage": 1,
                        # "Flag_Dynamic_RotorBarResistance": 0,
                        # "Flag_Calculate_VW": 1,
                        # #                           fineMesh or coarseMesh
                        # "msh": os.path.join(MODEL_DIR, "fineMesh.msh"),
                        # # "Flag_SecondOrder": 0,
                        # "stop_criterion": 1e-8,
                    },
                )
                if stderr:
                    stderr = str(stderr)
                    for textLine in stderr.split(r"\n"):
                        if "error" in textLine.lower():
                            logging.error(
                                "Onelab call issued the following error: \n\t%s",
                                textLine.replace("\n", "\n\t"),
                            )
                            raise RuntimeError(
                                "Simulation exited with error: %s",
                                textLine.replace("\n", "\n\t"),
                            )
                        if textLine:  # if textline is not empty
                            logging.warning(
                                "Onelab call issued the following warning: \n\t%s",
                                textLine.replace("\n", "\n\t"),
                            )
            except Exception as exce:
                tb_str = "".join(traceback.format_tb(exce.__traceback__))
                machine_test_dict[machineFile] = (
                    f"SIMULATION FAILED! Error: {exce}\nDetail:\n{tb_str}"
                )
            else:
                machine_test_dict[machineFile] = (
                    "SUCCESS: Machine successfully translated + simulated!"
                )
                nbr_simulated_machines += 1
            nbrTranslatedMaschines += 1
nbrFails = nbr_machines - nbrTranslatedMaschines
machine_test_dict["FINAL_RESULT"] = (
    f"{nbr_machines} machines, {nbrTranslatedMaschines} translated, "
    f"{nbrFails} failed, {nbr_simulated_machines=}",
)
print(json.dumps(machine_test_dict, sort_keys=True, indent=4))  # print results
print(machine_test_dict["FINAL_RESULT"])
# Write results to "Results" folder because its not tracked by Git.
with open(
    join(ROOT_DIR, "Results", "pyleecan_machine_test.json"),
    "w",
    encoding="utf-8",
) as jFile:
    # results = json.dumps(machine_test_dict)
    json.dump(machine_test_dict, jFile, indent=4)
