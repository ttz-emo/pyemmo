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
import os
from os import path
import math
import subprocess
from swat_em import datamodel
from pyemmo.script.script import Script
from pyemmo.script.geometry.point import Point
from pyemmo.script.material import ElectricalSteel, Material
from pyemmo.script.geometry.machineIPMSM import MachineIPMSM
from pyemmo.functions import runOnelab
from pyemmo.definitions import ROOT_DIR

####################################################
#       Rotorparameter (ausgedacht!)
PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = ElectricalSteel(
    sheetThickness=1e-3,
    lossParams=None,
    referenceFrequency=0,
    referenceFluxDensity=0,
    density=1,
)
steel_1010.loadMatFromDataBase("Material_new.db", "steel_1010")
ndFe35 = Material()
ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")
air = Material()
air.loadMatFromDataBase("Material_new.db", "air")
copper = Material()
copper.loadMatFromDataBase("Material_new.db", "copper")
# %% Simulationsparameter
DEG2RAD = math.pi / 180
nbrSlots = 12
nbrPoles = 8
axialLength = 0.1
simuIPMSMDict = {
    "analysisParameter": {
        "freq": 67,
        "symmetryFactor": math.gcd(
            nbrPoles, nbrSlots
        ),  # aus PMSM Struct raus -> kann auch mit Zahlen besetzt werden
        "nbrPolesTotal": nbrPoles,
        "nbrSlotTotal": nbrSlots,
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
rotor1 = pmsm1.addRotorToMachine(
    "sheet01_standard", "magnet_Slot01", axLen=axialLength
)
rotor1.addLaminationParameter(
    {
        "r_We": 7e-3,
        "r_R": 33e-3 / 2,
        "meshLength": 1.5e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
rotor1.addMagnetParameter(
    {
        "h_Mag": 7e-3,
        "w_Mag": 4e-3,
        "d_Slot": 1e-3,
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
rotor1.plot(symFactor=4)
# %% Statordefinition
winding = datamodel()
winding.genwdg(Q=nbrSlots, P=nbrPoles, m=3, layers=2, turns=12)
stator1 = pmsm1.addStatorToMachine(
    "sheet01_standard", "slotForm_01", axLen=axialLength, winding=winding
)
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
stator1.plot()
# %%
pmsm1.setFunctionMesh(
    functionType="quad", meshGainFactor=2, basisMeshsize=0.5e-3
)
pmsm1.createMachineDomains()

modelDir = path.abspath(
    path.join(ROOT_DIR, "Results", "Baukasten", "Test_IPMSM")
)
if not path.isdir(modelDir):
    os.makedirs(modelDir)

testIPMSM_Script = Script(
    name="Test_IPMSM",
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
    machine=pmsm1,
)
testIPMSM_Script.addPostOperation(
    quantityName="b",
    name="User Defined PostOperation",
    OnGrid="{(r_AG)*Sin[$A*Pi/180],(r_AG)*Cos[$A*Pi/180],0}{0:360/SymmetryFactor,0,0}",
    # OnGrid="{(r_AG)*Sin[Pi/nbSlots-$A*Pi/180],(r_AG)*Cos[Pi/nbSlots-$A*Pi/180],0}{0:360/SymmetryFactor,0,0}",
    File=path.abspath(
        path.join(testIPMSM_Script.resultsPath, "b_OnRadius.pos")
    ),
)
import time

startTime = time.time()
testIPMSM_Script.generateScript()
stopTime = time.time()
print("I am done!")
print(f"\n Generation of script took {stopTime-startTime} seconds.")

# %%
proFilePath = path.join(
    testIPMSM_Script.scriptPath, testIPMSM_Script.name + ".pro"
)
command = runOnelab.createCmdCommand(
    onelabFile=path.abspath(proFilePath),
    gmshPath=runOnelab.findGmsh(),
    useGUI=True,
)
subprocess.run(command, check=False)
# %%
# from pyemmo.functions import importResults
# importResults.plotAllDat(testIPMSM_Script.getResultsPath())

# %%
