"""Test module for spmsm toolkit machine model"""
# %%
import os
from os import mkdir, path
import sys

# from pyemmo.functions.importResults import plotAllDat
# from numpy import rad2deg, where
from swat_em import datamodel
import math

try:
    from pyemmo.script.script import Script
except ImportError:
    try:
        rootname = path.abspath(path.join(path.dirname(__file__), ".."))
    except:
        rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\pyemmo"
        print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    from pyemmo.script.script import Script

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.line import Line
from pyemmo.script.material.electricalSteel import Material, ElectricalSteel
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM
from pyemmo.functions.runOnelab import createCmdCommand

# %%

PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = ElectricalSteel(
    sheetThickness=1e-3,
    lossParams=(0.0, 0.0, 0.0),
    referenceFrequency=0,
    referenceFluxDensity=0,
)
steel_1010.loadMatFromDataBase("Material_new.db", "steel_1010")
ndFe35 = Material()
ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")
# ndFe35.setRemanence(0.01) # switch "off" remanence
air = Material()
air.loadMatFromDataBase("Material_new.db", "air")
copper = Material()
copper.loadMatFromDataBase("Material_new.db", "copper")

nbrSlots = 12
nbrPoles = 8
nbrPolePairs = nbrPoles / 2
drehzahl = 1000
fel = drehzahl / 60 * nbrPolePairs
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
            "angularWidth_i": math.pi / 10,
            "angularWidth_a": math.pi / 12,
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
if SLOT_TYPE == 0:
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
elif SLOT_TYPE == 1:
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
            "h_Slot": 15e-3,
            "r_Slot": 14e-3,
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
SPMSM.plot()
# SPMSM.createMachineDomains -> MachineAllType function
# %%
resDir = r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\Baukasten"
modelDir = path.abspath(path.join(resDir, "Test_SPMSM"))
if not path.isdir(modelDir):
    mkdir(modelDir)

myScript = Script(
    name="Test_SPMSM_Baukasten",
    scriptPath=modelDir,
    simuParams={
        "init_rotor_pos": 0,
        "angle_increment": 2,
        "final_rotor_pos": 45,
        "Id_eff": 0,
        "Iq_eff": 0,
        "rot_speed": drehzahl,
        "park_angle_offset": None,  # calc angle from machine layout
        "analysis_type": 0,
        "magTemp": 20,
    },
    machine=SPMSM,
)
myScript.generateScript()

os.system(
    createCmdCommand(
        onelabFile=myScript.getProFilePath(),
        useGUI=True,
        paramDict={"Flag_ClearResults": 1},
    )
)
# plotAllDat(myScript.getResultsPath())
print("I am done!")


# %%
