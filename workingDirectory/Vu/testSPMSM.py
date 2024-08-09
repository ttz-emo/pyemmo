# from numpy import rad2deg, where
import os
import subprocess
from collections import defaultdict
from os import path
from os.path import abspath, dirname, join, normpath

from mat_refs import magnetTypes, slotTypes
from testSPMSM_base import SPMSM_test

from pyemmo.functions.import_results import plot_all_dat
from pyemmo.functions.runOnelab import createCmdCommand

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.line import Line
from pyemmo.script.material.electricalSteel import ElectricalSteel, Material
from pyemmo.script.script import Script

# from pyemmo.definitions import ROOT_DIR


"""Preparation of test data"""
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
magType = 0
slotType = 1

test_params = defaultdict(list)
test_params["PBohrung"] = PBohrung
test_params["mats"] = {
    "laminMat": steel_1010,
    "magMat": ndFe35,
    "wireMat": copper,
    "airMat": air,
}
test_params["slotCount"] = 12
test_params["poleCount"] = 8
test_params["revols"] = 1000
test_params["simuParams"] = {
    # "freq": drehzahl / 60,
    "symmetryFactor": 4,
    # "timeMax": 1
    # / 67,  # Winkel/wr 2*math.pi / (2 * math.pi * 67) = 1/67 für ganzen mech. Winkel mit f = 67 Hz
    # "timeStep": 1
    # / (
    #     180 * 67 * 2
    # ),  # Ein Grad pro Step -> math.pi/180/(2*math.pi*67) = 1/(180*2*67)
    # "analysisType": "timedomain",  #'timedomain', #'static'
    "startPosition": 0,
    # "output": {"b": True, "az": True, "js": True},
}
test_params["magnet"] = magnetTypes[magType]
test_params["magnet"]["laminationParams"]["machineCentrePoint"] = PBohrung
test_params["magnet"]["laminationParams"]["material"] = steel_1010
test_params["magnet"]["magnetParams"]["material"] = ndFe35


test_params["slot"] = slotTypes[slotType]
test_params["slot"]["laminationParams"]["machineCentrePoint"] = PBohrung
test_params["slot"]["laminationParams"]["material"] = steel_1010
test_params["slot"]["slotParams"]["material"] = copper

test_params["airGapWidth"] = 3e-3
test_params["windingParams"] = {"m": 3, "layers": 2, "turns": 23}

SPMSM, rotor, stator = SPMSM_test(test_params)

rotor.plot()
stator.plot()
SPMSM.plot()

ROOT_DIR = normpath(abspath(join(dirname(__file__), ".."))).replace("\\", "/")

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
    # gmshPath=r"C:\Software\onelab\gmsh.exe",
    # getdpPath=r"C:\Software\onelab\getdp.exe",
    useGUI=True,
    paramDict={"Flag_ClearResults": 1},
)
print(cmd)

# os.system(cmd) #fixed per Issue: [B605:start_process_with_a_shell] in workingDirectory\Vu\bandit_log\bandit_log_20240809_093824.log
subprocess.run(cmd)
plot_all_dat(myScript.resultsPath)
print("I am done!")
