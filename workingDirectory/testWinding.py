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

from __future__ import annotations

import math
import subprocess
from genericpath import isdir

# %%
from os import mkdir, path

from pyemmo.definitions import RESULT_DIR
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM
from pyemmo.script.geometry.point import Point
from pyemmo.script.material.electricalSteel import Material
from pyemmo.script.script import Script

# %%

PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = Material.load("steel_1010")
ndFe35 = Material.load("NdFe35")
# ndFe35.setRemanence(0.01)
air = Material.load("air")
copper = Material.load("copper")

nbrSlots = 12
nbrPoles = 8
drehzahl = 1000
fel = drehzahl / 60 * nbrPoles / 2
simuSPMSMDict = {
    "analysisParameter": {
        "freq": drehzahl / 60,
        "symmetryFactor": 4,
        "nbrPolesTotal": nbrPoles,
        "nbrSlotTotal": nbrSlots,
        "timeMax": 1
        / 67,  # Winkel/wr 2*math.pi / (2 * math.pi * 67) = 1/67 für ganzen mech. Winkel mit f = 67 Hz
        "timeStep": 1
        / (
            180 * 67 * 2
        ),  # Ein Grad pro Step -> math.pi/180/(2*math.pi*67) = 1/(180*2*67)
        "analysisType": "timedomain",  #'timedomain', #'static'
        "startPosition": 0,
    },
    "output": {"b": True, "az": True, "js": True},
}

# Maschine aus dem Baukasten parametrisieren
SPMSM = MachineSPMSM(simuSPMSMDict)
rotor = SPMSM.addRotorToMachine("sheet01_standard", "magnet01_surface")
rR_Blech = 55e-3
rotor.addLaminationParameter(
    {
        "r_We": 20e-3,
        "r_R": rR_Blech,
        "meshLength": 3e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
h_mag = 7e-3
rotor.addMagnetParameter(
    {
        "h_M": h_mag,
        "angularWidth_i": math.pi / 10,
        "angularWidth_a": math.pi / 12,
        "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
        "magnetisationType": "radial",
        "material": ndFe35,
        "meshLength": 3e-3,
    }
)
rR = rR_Blech + h_mag
l_airgap = 1e-3
rotor.addAirGapParameter({"width": l_airgap, "material": air})
rotor.createRotor()
rotor.plot()
# %%
from swat_em import datamodel

# generate winding and add to stator
myWinding = datamodel()
myWinding.genwdg(Q=nbrSlots, P=int(nbrPoles / 2), m=3, layers=2, turns=30)
stator = SPMSM.addStatorToMachine(
    laminationType="sheet01_standard",
    slotType="slotForm_01",
    winding=myWinding,
)
stator.addLaminationParameter(
    {
        "r_S_i": rR + l_airgap,
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
stator.addAirGapParameter({"width": 1e-3, "material": air})
stator.createStator()
stator.plot()
# %% Create Machine
SPMSM.createMachineDomains()
SPMSM.plot()
# SPMSM.createMachineDomains -> MachineAllType function
# %%
modelDir = path.abspath(path.join(RESULT_DIR, "Test_WindingDef"))
if not isdir(modelDir):
    mkdir(modelDir)

myScript = Script(
    name="Test_SPMSM_Baukasten",
    scriptPath=modelDir,
    simuParams={
        "SYM": {
            "init_rotor_pos": 0,
            "angle_increment": 5,
            "final_rotor_pos": 90,
            "Id_eff": 0,
            "Iq_eff": 10,
            "rot_speed": drehzahl,
            "park_angle_offset": 360 / nbrSlots,
            "analysis_type": 1,
            "magTemp": 20,
        }
    },
    machine=SPMSM,
)
myScript.generateScript()


# %%
from pyemmo.functions.runOnelab import createCmdCommand

subprocess.run(
    createCmdCommand(
        onelabFile=myScript.proFilePath,
        useGUI=True,
        paramDict={"Flag_ClearResults": 1},
    ),
    check=True,
)

# plotAllDat(myScript.getResultsPath())
print("I am done!")


# %%
