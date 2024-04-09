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

# %%
from numpy import sign
from os import path
import sys

try:
    from pyemmo.script.script import Script
except:
    try:
        rootname = path.abspath(path.join(path.dirname(__file__), ".."))
    except:
        rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
        print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

    from pyemmo.script.script import Script

from pyemmo.script.geometry.point import Point
from pyemmo.script.material.material import Material
from pyemmo.script.geometry.machineIPMSM import MachineIPMSM
from pyemmo.functions import runOnelab
import math
import subprocess

####################################################
#       Rotorparameter (ausgedacht!)
PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = Material()
steel_1010.loadMatFromDataBase("Material_new.db", "steel_1010")
steel_1010.setSheetThickness(
    1e-3
)  # add sheet parameter because its not in database yet
ndFe35 = Material()
ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")
air = Material()
air.loadMatFromDataBase("Material_new.db", "air")
copper = Material()
copper.loadMatFromDataBase("Material_new.db", "copper")
# %% Simulationsparameter
DEG2RAD = math.pi / 180
simuIPMSMDict = {
    "analysisParameter": {
        "freq": 67,
        "symmetryFactor": 4,  # aus PMSM Struct raus -> kann auch mit Zahlen besetzt werden
        "nbrPolesTotal": 8,
        "nbrSlotTotal": 12,
        "timeMax": (
            1 / 67 / 4 / 3
        ),  # Winkel/wr* 2*math.pi / (2 * math.pi * 67) = 1/67 für ganzen mech. Winkel mit f = 67 Hz ; /4 für viertel
        # Ein Grad pro Step -> math.pi/180/(2*math.pi*67) = 1/(180*2*67); *4 für viertel
        "timeStep": (180 * 67 * 2) ** -1,
        "analysisType": "timedomain",  #'timedomain', #'static'
        "startPosition": 0,
    },
    "output": {"b": True, "az": True, "js": True},
}
# %%
# Maschine aus dem Baukasten parametrisieren
pmsm1 = MachineIPMSM(simuIPMSMDict)
## ROTOR ##
rotor1 = pmsm1.addRotorToMachine("sheet01_standard", "magnet_Slot01")
rotor1.addLaminationParameter(
    {
        "r_We": 2e-3,
        "r_R": 33e-3 / 2,
        "meshLength": 1.5e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
rotor1.addMagnetParameter(
    {
        "h_Mag": 9e-3,
        "w_Mag": 4e-3,
        "d_Slot": 0.8e-3,
        "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
        "magnetisationType": "tangential",
        "material": ndFe35,
        "meshLength": 1e-3,
    }
)
r_Stator_i = 17e-3
rotor1.addAirGapParameter(
    {"width": r_Stator_i - rotor1._laminationDict["r_R"], "material": air}
)
rotor1.createRotor()
# %% Statordefinition
stator1 = pmsm1.addStatorToMachine("sheet01_standard", "slotForm_01")
stator1.addLaminationParameter(
    {
        "r_S_i": r_Stator_i,
        "r_S_a": 29e-3,
        "meshLength": 1e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
stator1.addSlotParameter(
    {
        "w_SlotOP": 1.2e-3,
        "h_SlotOP": 1e-3,
        "w_Wedge": 6e-3,
        "h_Wedge": 1e-3,
        "h_Slot": 8e-3,
        "w_Slot": 5e-3,
        "material": copper,
        "meshLength": 2e-3,
        "slot_OPAir": True,
    }
)
stator1.addAirGapParameter({"width": 1e-3, "material": air})
stator1.createStator()
# %%
# Für jede SlotSEITE! (deswegen immer 6 für Einzelzahnwicklung)
allSlot = stator1.getAllSlot()
nbrSlots = simuIPMSMDict["analysisParameter"]["nbrSlotTotal"]
slotsPerPole = (
    nbrSlots / simuIPMSMDict["analysisParameter"]["nbrPolesTotal"] * 2
)
N_wind = 12
I_rms = 1
angleOffset = -90 * DEG2RAD
freq = simuIPMSMDict["analysisParameter"]["freq"]

winding = [-1, +2, -2, +3, -3, +1]
for slotPos, slot in enumerate(allSlot):
    num = winding[slotPos % nbrSlots]
    # check if slot is U, V or W
    if num in (+1, -1):
        phase = "U"
        phaseAngle = -2 * math.pi / 3  # Phase U
        currentDir = sign(num)
    elif num in (+2, -2):
        phase = "V"
        phaseAngle = 2 * math.pi / 3  # Phase V
        currentDir = sign(num)
    elif num in (+3, -3):
        phase = "W"
        phaseAngle = 0  # Phase W
        currentDir = sign(num)
    else:
        raise (RuntimeError(f"phase not recognized"))
    print(f"Slot {int(slotPos)} with ID {slot.getID()}: {currentDir} {phase}")

    # set current dict
    ExcitationDict = {
        "currentAmplitude": I_rms,
        "nbrTurnsInFace": N_wind,  # weil Slots geteilt sind
        "currentDirection": currentDir,
        "phaseAngle": phaseAngle + angleOffset,
        "frequency": freq * nbrSlots / 2,  # Drehfrequenz * Polpaarzahl
    }
    slot.addExcitation(windingDict=ExcitationDict)

# %%
pmsm1.createMachineDomains()

# myScript = Script("Test_IPMSM", abspath(join(RESULT_DIR,"TestIPMSM")))
testIPMSM_Script = Script(
    name="Test_IPMSM",
    scriptPath=r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\Software_V2\Results\TestIPMSM",
    simuParams={
        "init_rotor_pos": 0,
        "angle_increment": 1,
        "final_rotor_pos": 90,
        "Id_eff": 0,
        "Iq_eff": 0,
        "rot_speed": 1000,
        "park_angle_offset": 0,
        "analysis_type": 0,
    },
    machine=pmsm1,
)
testIPMSM_Script.generateScript()
print("I am done!")
# %%
# append onelab path to find getdp:
sys.path.append(
    r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904"
)
proFilePath = path.join(
    testIPMSM_Script.getScriptPath(), testIPMSM_Script.getName() + ".pro"
)
command = runOnelab.createCmdCommand(
    onelabFile=path.abspath(proFilePath),
    gmshPath=runOnelab.findGmsh(),
    useGUI=True,
)
subprocess.run(command)
# %%
# from pyemmo.functions import importResults
# importResults.plotAllDat(testIPMSM_Script.getResultsPath())

# %% calculate iq vector
for iq in range(0, 11, 2):
    command = runOnelab.createCmdCommand(
        onelabFile=path.abspath(proFilePath),
        gmshPath=runOnelab.findGmsh(),
        getdpPath=runOnelab.findGetDP(),
        useGUI=False,
        paramDict={
            "IQ_RMS": iq,
            "ResId": rf"\IQ={iq}",
        },
    )
    print("System Command is:")
    print(command)
    subprocess.run(command)

# %%
