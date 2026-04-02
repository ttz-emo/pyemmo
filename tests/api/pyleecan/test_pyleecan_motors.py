#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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

import os
from os.path import join

import pytest
from pyleecan.Classes.LamSlotMulti import LamSlotMulti
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineWRSM import MachineWRSM
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions import load

from pyemmo.api.pyleecan.main import main

# from pyemmo.functions.runOnelab import main as run_onelab
from ... import TEST_TEMP_DIR

# from pyleecan.Classes.MachineLSPM


MODEL_RES_DIR = join(TEST_TEMP_DIR, "pyleecanAPI")
MACHINE_FILE_DIR = join(DATA_DIR, "Machine")
machine_file_list = os.listdir(MACHINE_FILE_DIR)
nbr_machines = len(machine_file_list)


@pytest.mark.parametrize("machineFile", machine_file_list)
def test_translate_machine(machineFile: str):
    """This function runs the pyemmmo pyleecan api for all available pyleecan machine
    from pyleecan.definitions.DATA_DIR."""
    machinePath = join(MACHINE_FILE_DIR, machineFile)
    # pylint: disable=locally-disabled, no-member
    machine: Machine = load.load(machinePath)
    machine_model_dir = join(MODEL_RES_DIR, machine.name)

    if not machine.rotor.is_internal:
        # internal rotor raises not implemented error
        pytest.skip("Machine has external rotor.")
    if isinstance(machine, MachineWRSM):
        pytest.skip("Machine is instance Wound Rotor Synchronous Machine")
    if machine.stator.winding.qs != 3:
        pytest.skip(f"Stator winding has {machine.stator.winding.qs} phases")
    if any(isinstance(lam, LamSlotMulti) for lam in machine.get_lam_list()):
        pytest.skip("Can not translate lamination of type LamSlotMulti.")
    if "LSPM_001.json" == machineFile:
        pytest.xfail(
            "Bug in LSPM_001.json: Rotor Squirrle Cage winding pole pair number does "
            "not match stator winding pole pair number"
        )
    if "SCIM_010.json" == machineFile:
        pytest.xfail(
            "Bug in SCIM_010.json: Material 'UserAluminium' missing magnetic properties"
        )
    if "Stellantis_IPMSM_test_doubleV.json" == machineFile:
        pytest.xfail(
            "Bug in Stellantis_IPMSM_test_doubleV.json: Material 'Magnet1' has invalid "
            "BH Curve."
        )
    if "TESLA_S.json" == machineFile:
        pytest.xfail(
            "Bug in TESLA_S.json: Bug in rotor slot parametrization leads to overlaping "
            "surfaces!"
        )

    main(machine, machine_model_dir, use_gui=False)

    # stderr = run_onelab(
    #     onelabFile=join(machine_model_dir, machine.name + ".pro"),
    #     use_gui=False,
    #     paramDict={
    #         # "freq_rotor": f_r,
    #         "I_eff": 10,
    #         "IQ_RMS": 10,
    #         # "RPM": float(n),
    #         # "initrotor_pos": 0.0,
    #         # "nbrStatorPeriods": nbr_stator_periods,
    #         # "nbrStepsPerPeriod": nbr_steps_per_period,
    #         # "d_theta": winkelschritt,
    #         # "ResId": resId,
    #         "Flag_AnalysisType": 0,
    #         # "Flag_PrintFields": 0,
    #         # "Flag_Debug": 1,
    #         "Flag_ClearResults": 1,
    #         # "verbosity level": 3,
    #         # # "AxialLength_R": 1,
    #         # # "AxialLength_S": 1,
    #         # "NbrParallelPaths": 1,
    #         # "R_endring_segment": 16e-7
    #         # / 2,  # Initial value: 16e-7,
    #         # "L_endring_segment": 2e-9 / 2,
    #         # "Flag_Cir_RotorCage": 1,
    #         # "Flag_Dynamic_RotorBarResistance": 0,
    #         # "Flag_Calculate_VW": 1,
    #         # #                           fineMesh or coarseMesh
    #         # "msh": os.path.join(MODEL_DIR, "fineMesh.msh"),
    #         # # "Flag_SecondOrder": 0,
    #         # "stop_criterion": 1e-8,
    #     },
    # )
    # if stderr:
    #     stderr = str(stderr)
    #     for textLine in stderr.split(r"\n"):
    #         if "error" in textLine.lower():
    #             logging.error(
    #                 "Onelab call issued the following error: \n\t%s",
    #                 textLine.replace("\n", "\n\t"),
    #             )
    #             raise RuntimeError(
    #                 "Simulation exited with error: %s",
    #                 textLine.replace("\n", "\n\t"),
    #             )
    #         if textLine:  # if textline is not empty
    #             logging.warning(
    #                 "Onelab call issued the following warning: \n\t%s",
    #                 textLine.replace("\n", "\n\t"),
    #             )
