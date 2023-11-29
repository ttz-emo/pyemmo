"""Example module for SPMSM toolkit machine model for Wike³ 2023"""
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

from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.surface import Surface
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

# Motor- und Simulationsparameter festlegen
nbrSlots = 12
nbrPoles = 8
drehzahl = 1000
simulationDict = {
    "analysisParameter": {
        "symmetryFactor": 4,
        "nbrPolesTotal": nbrPoles,
        "nbrSlotTotal": nbrSlots,
        "startPosition": 0,
    }
}

# %% Rotor aus dem Baukasten parametrisieren
from pyemmo.script.geometry.rotorLamination_Sheet01_Standard import RotorLamination_Sheet01_Standard
from pyemmo.script.geometry.magnet_Surface01 import Magnet_Surface01
from pyemmo.script.geometry.rotorSPMSM import RotorSPMSM

SPMSM = MachineSPMSM(simulationDict)
# -> Magnet Surface 01
rotor = SPMSM.addRotorToMachine("sheet01_standard", "magnet01_surface")

rotor.addLaminationParameter(
    {
        "r_We": 20e-3,  # Wellenradius
        "r_R": 56e-3,  # Rotor-Außenradius
        "meshLength": 3e-3,
        "material": steel_1010,
        "machineCentrePoint": PBohrung,
    }
)
rotor.addMagnetParameter(
    {
        "h_M": 5e-3,  # Magnethöhe
        "angularWidth_i": math.pi / 10,  # Winkel innen
        "angularWidth_a": math.pi / 12,  # Winkel außen
        "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
        "magnetisationType": "radial",
        "material": ndFe35,
        "meshLength": 3e-3,
    }
)

# Luftspalt Parameter
lAirgap = 3e-3
rotor.addAirGapParameter({"width": lAirgap, "material": air})
rotor.createRotor()
# rHole = 0.5e-3
# for physical in rotor._domainNL.physicals:
#     for surface in physical.geometricalElement:
#         cog = surface.calcCOG()
#         p1 = cog.duplicate()
#         p1.translate(-rHole,0,0)
#         p2 = cog.duplicate()
#         p2.translate(rHole,0,0)
#         arc1 = CircleArc("c1",p1,cog,p2)
#         arc2 = CircleArc("c2",p2, cog, p1)
#         circSurf = Surface("s1",[arc1,arc2])
#         surface.cutOut(circSurf)
rotor.plot(symFactor=4)
# %% Stator aus dem Baukasten parametrieren
winding = datamodel()  # SWAT-EM Wicklung
winding.genwdg(Q=nbrSlots, P=nbrPoles, m=3, layers=2, turns=23)

stator = SPMSM.addStatorToMachine("sheet01_standard", "slotForm_03", winding)
stator.addLaminationParameter(
    {
        "r_S_i": 64e-3,
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

# Luftspaltparameter für Stator
stator.addAirGapParameter({"width": lAirgap, "material": air})
stator.createStator()
stator.plot()
# %% Create Machine
SPMSM.createMachineDomains()  # Domänen für Simlation generieren
SPMSM.setFunctionMesh("linear", 8)  # Mesh über Funktion einstellen
SPMSM.plot()
# %% Simulationsmodell erzeugen
resDir = r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\Baukasten"
modelDir = path.abspath(path.join(resDir, "SPMSM_Wike"))
if not path.isdir(modelDir):
    mkdir(modelDir)

myScript = Script(
    name="Test_SPMSM_Baukasten_Wike3",
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
        "calcMagnetLosses": 1,
    },
    machine=SPMSM,
)
myScript.generateScript()  # ONELAB Dateien erzeugen

# Start Gmsh from command line
systemReturn = os.system(
    createCmdCommand(
        onelabFile=myScript.getProFilePath(),
        useGUI=True,
        paramDict={"Flag_ClearResults": 1},
    )
)
# plotAllDat(myScript.getResultsPath())
# %%
