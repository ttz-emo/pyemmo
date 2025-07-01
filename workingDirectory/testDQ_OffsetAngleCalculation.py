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
import subprocess
from cmath import pi
from genericpath import isdir
from os import mkdir, path

from numpy import gcd, rad2deg, where
from swat_em import analyse, datamodel

from pyemmo.definitions import RESULT_DIR
from pyemmo.functions.import_results import plot_all_dat
from pyemmo.functions.runOnelab import createCmdCommand
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM
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
# ndFe35.setRelPermeability(1000)
air = Material.load("air")
copper = Material.load("copper")

nbrSlots = 12
nutteilung = 2 * pi / nbrSlots
nbrPoles = 10
nbrPolePairs = nbrPoles / 2
drehzahl = 1000
fel = drehzahl / 60 * nbrPolePairs
simuSPMSMDict = {
    "analysisParameter": {
        "freq": drehzahl / 60,
        "symmetryFactor": gcd(nbrSlots, nbrPoles),
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
rotor.addLaminationParameter(
    {
        "r_We": 20e-3,
        "r_R": 55e-3,
        "meshLength": 3e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
polteilung = 2 * pi / nbrPoles
rotor.addMagnetParameter(
    {
        "h_M": 7e-3,
        "angularWidth_i": polteilung / 2 * 0.9,
        "angularWidth_a": polteilung / 2 * 0.8,
        "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
        "magnetisationType": "radial",
        "material": ndFe35,
        "meshLength": 3e-3,
    }
)
rotor.addAirGapParameter({"width": 3e-3, "material": air})
rotor.createRotor()
rotor.plot()
# %%
winding = datamodel()
winding.genwdg(Q=nbrSlots, P=nbrPoles, m=3, layers=2, turns=23)
stator = SPMSM.addStatorToMachine("sheet01_standard", "slotForm_01", winding)
rsi = 65e-3
rsa = 100e-3
stator.addLaminationParameter(
    {
        "r_S_i": rsi,
        "r_S_a": rsa,
        "meshLength": 3e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
rWedge = rsi + (4 + 7) * 1e-3
rSlot = rsi + (4 + 20) * 1e-3
rNutschlitz = rsi + 4e-3
hSlot = 20e-3
stator.addSlotParameter(
    {
        "w_SlotOP": nutteilung / 2 * rNutschlitz * 0.1,
        "h_SlotOP": hSlot * 0.08,
        "w_Wedge": nutteilung * rWedge * 0.5,
        "h_Wedge": hSlot * 0.15,
        "h_Slot": hSlot,
        "w_Slot": nutteilung / 2 * rSlot * 0.6,
        "material": copper,
        "meshLength": 3e-3,
        "slot_OPAir": True,
    }
)
stator.addAirGapParameter({"width": 3e-3, "material": air})
stator.createStator()
stator.plot()
# %% Create Machine
SPMSM.createMachineDomains()
SPMSM.setFunctionMesh("linear", 8)
SPMSM.plot()
# SPMSM.createMachineDomains -> MachineAllType function
# %% calc angle offset
dAxisAngle = polteilung / 2 * nbrPolePairs  # center angle of north pole -> d-Axis
print(f"d-Axis (rotor north pole) angle (elec): {rad2deg(dAxisAngle)}°")
nu, amp, angle = SPMSM.stator.winding.get_MMF_harmonics()
# Stator Winkel für I_U = 1 p.u., I_V = -1/2, I_W = -1/2
phiS = float(angle[where(nu == nbrPolePairs)])  # rad elec

print(f"Stator north pole angle (elec): {rad2deg(phiS)}°")
qAxisAngle = rad2deg(dAxisAngle) + 90  # deg elec
print(f"q-Axis angle (elec): {(qAxisAngle)}°")
dqOffset = rad2deg(nutteilung / 2 * nbrPolePairs) - rad2deg(phiS)  # deg elec
phi, MMK, theta = analyse.calc_MMK(
    Q=winding.get_num_slots(),
    m=3,
    S=winding.get_phases(),
    turns=winding.get_turns(),
    # actual angle of current system in deg
    angle=0,
    # angle=rad2deg(phiS) * nbrPolePairs,
)
durchflutungNut0 = theta[0]
print(f"Durchflutung in erster Nut: {durchflutungNut0}")
print(f"Offset angle for dq transformation: {(dqOffset)}°")
stator.winding.plot_MMK(filename=".\test_MMF.png", res=[800, 600], show=True)
# %%
modelDir = path.abspath(path.join(RESULT_DIR, "Test_SPMSM"))
if not isdir(modelDir):
    mkdir(modelDir)

myScript = Script(
    name="Test_SPMSM_Baukasten",
    scriptPath=modelDir,
    simuParams={
        "init_rotor_pos": 0,
        "angle_increment": 2,
        "final_rotor_pos": 45,
        "Id_eff": 0,
        "Iq_eff": 10,
        "rot_speed": drehzahl,
        "park_angle_offset": round(dqOffset, 3),
        "analysis_type": 0,
        "magTemp": 20,
    },
    machine=SPMSM,
)
myScript.generateScript()

subprocess.run(
    createCmdCommand(
        onelabFile=myScript.proFilePath,
        useGUI=True,
        paramDict={"Flag_ClearResults": 1},
    )
)
# fixed per Issue: [B605:start_process_with_a_shell] in workingDirectory\Vu\bandit_log\bandit_log_20240809_093824.log line 2596
# os.system(
#     createCmdCommand(
#         onelabFile=myScript.proFilePath,
#         useGUI=True,
#         paramDict={"Flag_ClearResults": 1},
#     )
# )
plot_all_dat(myScript.resultsPath)
# %%
