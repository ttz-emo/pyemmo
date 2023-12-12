from os.path import join
import sys

# =================
# Imports pyleecan:
# =================
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM

# ===============
# Imports pyemmo:
# ===============
from pyemmo.functions.plot import plot
from pyemmo.api.json import main
from pyemmo.definitions import ROOT_DIR
from workingDirectory.buildPyemmoMovingBand import buildMovingBand
from workingDirectory.createParamDict import createParamDict


# ========================================
# Festlegung der zu berechnenden Maschine:
# ========================================
machine = load(
    join(ROOT_DIR, "workingDirectory\\machineData\\SPMSMPyleecanMuster_2Shaft_ZaW2.json")
)
simulation = load(
    join(ROOT_DIR, "workingDirectory\\machineData\\FEMM_SPMSMPyleecanMuster_2Shaft_ZaW2.json")
)

# =====================================
# Festlegung der Simulations-Parameter:
# =====================================

rotorRext = machine.rotor.Rext
rotorRint = machine.rotor.Rint
statorRint = machine.stator.Rint
statorRext = machine.stator.Rext


# --------------------------
# isInternalRotor detection:
# --------------------------
isInternalRotor = bool(statorRint > rotorRext)

if isinstance(machine, MachineSIPMSM):
    allBands, geometryList, movingband_r, magnetizationDict = buildMovingBand(
        machine=machine,
        rotorRint=rotorRint,
        rotorRext=rotorRext,
        statorRint=statorRint,
        statorRext=statorRext,
        isInternalRotor=isInternalRotor,
    )

elif isinstance(machine, MachineIPMSM):
    allBands, geometryList, movingband_r, magnetizationDict = buildMovingBand(
        machine=machine,
        rotorRint=rotorRint,
        rotorRext=rotorRext,
        statorRint=statorRint,
        statorRext=statorRext,
        isInternalRotor=isInternalRotor,
    )

geoTranslationDict = {}
for surfAPI in geometryList:
    geoTranslationDict[surfAPI.idExt] = surfAPI

geometryLineListFinish = []
for surf in geometryList:
    for line in surf.curve:
        geometryLineListFinish.append(line)

print("Plot ENDE:")
plot(geometryLineListFinish, linewidth=1, markersize=3, tag=True)
print("---")


paramDict = createParamDict(
    machine, simulation, movingband_r, magnetizationDict
)
main(
    geo=geoTranslationDict,
    extInfo=paramDict,
    model=join(ROOT_DIR, r"Results\pyleecanAPI\TEST_TRANSLATION"),
    gmsh="C:\\Software\\Onelab\\gmsh.exe",
)
