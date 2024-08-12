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

# %%
import os
from os import mkdir, path

# from pyemmo.functions.importResults import plotAllDat
# from numpy import rad2deg, where
import math
from swat_em import datamodel

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.line import Line
from pyemmo.script.material.electricalSteel import Material, ElectricalSteel
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM
from pyemmo.script.script import Script
from pyemmo.functions.runOnelab import createCmdCommand
from pyemmo.definitions import ROOT_DIR

# %%

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
# ndFe35.setRemanence(0.01) # switch "off" remanence
air = Material()
air.loadMatFromDataBase("Material_new.db", "air")
copper = Material()
copper.loadMatFromDataBase("Material_new.db", "copper")

NBR_SLOTS = 36
NBR_POLES = 4
NBR_POLEPAIRS = NBR_POLES / 2
SPEED = 1000
F_EL = SPEED / 60 * NBR_POLEPAIRS
simuSPMSMDict = {
    "analysisParameter": {
        "freq": SPEED / 60,
        "symmetryFactor": 4,
        "nbrPolesTotal": NBR_POLES,
        "nbrSlotTotal": NBR_SLOTS,
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

# %% Maschine aus dem Baukasten parametrisieren
SPMSM = MachineSPMSM(simuSPMSMDict)
MAG_TYPE = 0  # 0: magnet01_surface, 1: magnet02_surface
if MAG_TYPE == 0:
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
    wSeg = 2 * rotor.laminationDict["r_R"] * math.pi
    rotor.addMagnetParameter(
        {
            "h_M": 7e-3,
            "angularWidth_i": math.pi / NBR_POLEPAIRS * 0.8,
            "angularWidth_a": math.pi / NBR_POLEPAIRS * 0.79,
            "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
            "magnetisationType": "radial",
            "material": ndFe35,
            "meshLength": 3e-3,
        }
    )
    # End:      Magnet Surface 01
elif MAG_TYPE == 1:
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
elif MAG_TYPE == 2:
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
L_AIRGAP = 3e-3
rotor.addAirGapParameter({"width": L_AIRGAP, "material": air})
rotor.createRotor()
rotor.plot()
# %%
winding = datamodel()
winding.genwdg(Q=NBR_SLOTS, P=NBR_POLES, m=3, layers=2, turns=23)
SLOT_TYPE = 0
if SLOT_TYPE == 0:
    stator = SPMSM.addStatorToMachine(
        "sheet01_standard", "slotForm_01", winding
    )
    stator.addLaminationParameter(
        {
            "r_S_i": 65e-3,
            "r_S_a": 92e-3,
            "meshLength": 3e-3,
            "material": steel_1010,
            "machineCentrePoint": PBohrung,
        }
    )
    wMin = 2 * stator.laminationDict["r_S_i"] * math.pi / NBR_SLOTS / 2
    wMax = 2 * stator.laminationDict["r_S_a"] * math.pi / NBR_SLOTS / 2
    hSt = stator.laminationDict["r_S_a"] - stator.laminationDict["r_S_i"]
    stator.addSlotParameter(
        {
            "w_SlotOP": 0.3 * wMin,
            "h_SlotOP": 0.05 * hSt,
            "w_Wedge": wMin,
            "h_Wedge": 0.1 * hSt,
            "h_Slot": 0.6 * hSt,
            "w_Slot": 0.7 * wMin,
            "material": copper,
            "meshLength": hSt / 10,
            "slot_OPAir": True,
        }
    )
# elif SLOT_TYPE == 1:
#     stator = SPMSM.addStatorToMachine("sheet01_standard", "slotForm_03", winding)
#     stator.addLaminationParameter(
#         {
#             "r_S_i": 65e-3,
#             "r_S_a": 100e-3,
#             "meshLength": 3e-3,
#             "material": steel_1010,
#             "machineCentrePoint": PBohrung,
#         }
#     )
#     stator.addSlotParameter(
#         {
#             "meshLength": 3e-3,
#             "w_SlotOP": 4e-3,
#             "h_SlotOP": 4e-3,
#             "h_Wedge": 5e-3,
#             "w_Wedge": 22e-3,
#             "h_Slot": 15e-3,
#             "r_Slot": 14e-3,
#             "slot_OPAir": True,
#             "material": copper,
#         }
#     )
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
stator.addAirGapParameter({"width": L_AIRGAP, "material": air})
stator.createStator()
SPMSM.stator.plot()
# %% Create Machine
SPMSM.createMachineDomains()
SPMSM.setFunctionMesh("linear", 8)
SPMSM.plot()
# SPMSM.createMachineDomains -> MachineAllType function
# %%
resDir = os.path.join(ROOT_DIR, r"Results\Baukasten")
modelDir = path.abspath(path.join(resDir, "Test_SPMSM"))
if not path.isdir(modelDir):
    mkdir(modelDir)

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

os.system(
    createCmdCommand(
        onelabFile=myScript.proFilePath,
        useGUI=True,
        paramDict={"Flag_ClearResults": 1},
    )
)
# plotAllDat(myScript.getResultsPath())
print("I am done!")


# %%
from pyemmo.functions.import_results import (
    get_result_files,
    read_timetable_dat,
)
from pyemmo.functions.import_results import (
    get_result_files,
    read_timetable_dat,
)
from SciDataTool import DataTime, Data1D

resPath = (
    myScript.resultsPath
)  # 'C:/Users/ganser/AppData/Local/Programs/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten'

resultsList: list[DataTime] = []
try:
    datFiles, posFiles = get_result_files(resPath)
    for datFile in datFiles:
        time, data = read_timetable_dat(os.path.join(resPath, datFile))
        _, datFileName = os.path.split(datFile)
        resQuantity, _ = os.path.splitext(datFileName)
        timeData = Data1D(
            values=time, symmetries=-1, name="time", symbol="t", unit="s"
        )
        valData = DataTime(axes=[timeData], values=data, name=resQuantity)
        resultsList.append(valData)
except FileNotFoundError:
    print("No results from GetDP...")
except Exception as exce:
    raise exce

# %%
from SciDataTool.Functions.Plot.plot_2D import plot_2D
import matplotlib.pyplot as plt

plt.plot(resultsList[00].values, resultsList[00].axes[0].values)
plt.show()
print("ENDE")
