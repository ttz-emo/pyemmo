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
"""Test module for spmsm toolkit machine model"""
from __future__ import annotations

# from numpy import rad2deg, where
import math

# %%
import os
import subprocess
from os import path

from swat_em import datamodel

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.import_results import plot_all_dat
from pyemmo.functions.run_onelab import createCmdCommand, findGetDP, findGmsh
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.line import Line
from pyemmo.script.material.electricalSteel import Material
from pyemmo.script.script import Script

# %%

PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = Material.load("steel_1010")
ndFe35 = Material.load("NdFe35")
# ndFe35.setRemanence(0.01) # switch "off" remanence
air = Material.load("air")
copper = Material.load("copper")

nbrSlots = 12
nbrPoles = 8
nbrPolePairs = nbrPoles / 2
drehzahl = 1000
fel = drehzahl / 60 * nbrPolePairs
simuSPMSMDict = {
    "analysisParameter": {
        # "freq": drehzahl / 60,
        "symmetryFactor": 4,
        "nbrPolesTotal": nbrPoles,
        "nbrSlotTotal": nbrSlots,
        # "timeMax": 1
        # / 67,  # Winkel/wr 2*math.pi / (2 * math.pi * 67) = 1/67 für ganzen mech. Winkel mit f = 67 Hz
        # "timeStep": 1
        # / (
        #     180 * 67 * 2
        # ),  # Ein Grad pro Step -> math.pi/180/(2*math.pi*67) = 1/(180*2*67)
        # "analysisType": "timedomain",  #'timedomain', #'static'
        "startPosition": 0,
    },
    # "output": {"b": True, "az": True, "js": True},
}

# %% Maschine aus dem Baukasten parametrisieren
SPMSM = MachineSPMSM(simuSPMSMDict)
magType = 0  # 0: magnet01_surface, 1: magnet02_surface
if magType == 0:
    # Magnet Surface 01
    rotor = SPMSM.addRotorToMachine("sheet01_standard", "magnet01_surface")
    rotor.addLaminationParameter(
        {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    rotor.addMagnetParameter(
        {
            "h_M": 7e-3,
            "angularWidth_i": math.pi / 5,
            "angularWidth_a": math.pi / 6,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "material": ndFe35,
            "meshLength": 3e-3,
        }
    )
    # End:      Magnet Surface 01
elif magType == 1:
    # Start:    Magnet Surface 02
    rotor = SPMSM.addRotorToMachine("sheet01_standard", "magnet02_surface")
    rotor.addLaminationParameter(
        {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    rotor.addMagnetParameter(
        {
            # "h_M": 7e-3,
            "h_M": 4e-3,
            # "w_Mag": 30e-3,
            "w_Mag": 20e-3,
            "r_Mag": 25e-3,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "material": ndFe35,
            "meshLength": 3e-3,
        }
    )
    # End:      Magnet Surface 02
elif magType == 2:
    # Start:    Magnet Surface 03 -> BUG!
    rotor = SPMSM.addRotorToMachine("sheet01_standard", "magnet03_surface")
    rotor.addLaminationParameter(
        {
            "r_We": 20e-3,
            "r_R": 55e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    rotor.addMagnetParameter(
        {
            "h_M": 7e-3,
            "w_Mag": 30e-3,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "material": ndFe35,
            "meshLength": 3e-3,
        }
    )
    # End:      Magnet Surface 03
else:
    raise ValueError("Wrong number for rotor type!")

# rotor.addLaminationParameter(
#     {
#         "r_We": 20e-3,
#         "r_R": 55e-3,
#         "meshLength": 3e-3,
#         "material": steel_1010,
#         "machineCentrePoint": PBohrung,
#     }
# )
lAirgap = 3e-3
rotor.addAirGapParameter({"width": lAirgap, "material": air})
rotor.createRotor()
rotor.plot()
# %%
winding = datamodel()
winding.genwdg(Q=nbrSlots, P=nbrPoles, m=3, layers=2, turns=23)
SLOT_TYPE = 1
if SLOT_TYPE == 0:  # trapezoidal slot
    stator = SPMSM.addStatorToMachine("sheet01_standard", "slotForm_01", winding)
    stator.addLaminationParameter(
        {
            "r_S_i": 65e-3,
            "r_S_a": 100e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    stator.addSlotParameter(
        {
            "w_SlotOP": 4e-3,
            "h_SlotOP": 4e-3,
            "w_Wedge": 20e-3,
            "h_Wedge": 7e-3,
            "h_Slot": 20e-3,
            "w_Slot": 14e-3,
            "material": copper,
            "meshLength": 3e-3,
            "slot_OPAir": True,
        }
    )
elif SLOT_TYPE == 1:  # round slot bottom
    stator = SPMSM.addStatorToMachine("sheet01_standard", "slotForm_03", winding)
    stator.addLaminationParameter(
        {
            "r_S_i": 65e-3,
            "r_S_a": 100e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    stator.addSlotParameter(
        {
            "meshLength": 3e-3,
            "w_SlotOP": 4e-3,
            "h_SlotOP": 4e-3,
            "h_Wedge": 5e-3,
            "w_Wedge": 22e-3,
            "h_Slot": 10e-3,
            "r_Slot": 13e-3,
            "slot_OPAir": True,
            "material": copper,
        }
    )
else:
    raise ValueError("Wrong number for slot type!")

# stator.addLaminationParameter(
#     {
#         "r_S_i": 65e-3,
#         "r_S_a": 100e-3,
#         "meshLength": 3e-3,
#         "material": steel_1010,
#         "machineCentrePoint": PBohrung,
#     }
# )
stator.addAirGapParameter({"width": lAirgap, "material": air})
stator.createStator()
stator.plot()
# %% Create Machine
SPMSM.createMachineDomains()
SPMSM.setFunctionMesh("linear", 8)
fig = SPMSM.plot()
# SPMSM.createMachineDomains -> MachineAllType function
# %%
resDir = os.path.join(ROOT_DIR, r"Results\Baukasten")
modelDir = path.abspath(path.join(resDir, "Test_SPMSM"))
if not path.isdir(modelDir):
    os.makedirs(modelDir)
else:
    # remove results folder
    pass

myScript = Script(
    name="Test_SPMSM_Baukasten",
    scriptPath=modelDir,
    simuParams={
        "SYM": {
            "INIT_ROTOR_POS": 0.0,
            "ANGLE_INCREMENT": 1,
            "FINAL_ROTOR_POS": 90.0,
            "Id_eff": 0,
            "Iq_eff": 0,
            "SPEED_RPM": 1000,
            "ParkAngOffset": None,  # optional
            "ANALYSIS_TYPE": 0,  # optional; 0: static, 1: transient
        },
    },
    machine=SPMSM,
)
myScript.generateScript()

cmd = createCmdCommand(
    onelabFile=myScript.proFilePath,
    gmshPath=findGmsh(),
    getdpPath=findGetDP(),
    useGUI=False,
    paramDict={"Flag_ClearResults": 1},
)
print(cmd)

# %%
subprocess.run(cmd, check=True)
plot_all_dat(myScript.resultsPath)
print("I am done!")


# %%
