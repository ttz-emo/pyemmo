# %%
import os
import numpy as np

# =================
# Imports pyleecan:
# =================
from pyleecan.Functions.load import load
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq

from pyleecan.Classes.Machine import Machine
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


# Simulation Function
def generateSimulation(
    machine: Machine, Id: float = 0.0, Iq: float = 10.0, speed: float = 1000.0
) -> Simulation:
    """Create a Simulation object from a given machine

    Args:
        machine (Machine): Actual pyleecan machine

    Returns:
        Simulation: Pyleecan Simulation object
    """
    simu = Simu1(name="PyEMMO_Simulation", machine=machine)
    # simu.path_result = "path/to/folder" Path to the Result folder to use
    # (will contain FEMM files)
    p = simu.machine.stator.winding.p
    # qs = simu.machine.stator.winding.qs

    # Defining Simulation Input
    simu.input = InputCurrent()
    # Rotor speed [rpm]
    simu.input.OP = OPdq(Id_ref=Id, Iq_ref=Iq, N0=speed)

    # time discretization [s] -> one elec. period with # 32 timesteps
    time = np.linspace(start=0, stop=60 / speed / p, num=32, endpoint=True)
    simu.input.time = time

    # Angular discretization along the airgap circonference
    angularDisc = np.linspace(
        start=0, stop=2 * np.pi, num=2048, endpoint=False
    )
    simu.input.angle = angularDisc
    return simu


# %%
# ========================================
# Festlegung der zu berechnenden Maschine:
# ========================================
# machine = load(
# 	DATA_DIR, "Machine", "SPMSM_002.json"
#     )
machineFolder = os.path.join(ROOT_DIR, "workingDirectory/machineData")
resFolder = os.path.join(ROOT_DIR, r"Results\pyleecanAPI")
machineList = []
for i, file in enumerate(os.listdir(machineFolder)):
    if file.endswith(".json") and not "FEMM" in file:
        machineList.append(file)
        print(f"{machineList.index(file)}: " + file)

fileName = machineList[29]  # SELECT MACHINE HERE BY INDEX OR NAME
print("\nUsing machine: " + fileName)
machine = load(os.path.abspath(os.path.join(machineFolder, fileName)))
simulation = generateSimulation(machine, Id=0, Iq=10, speed=1000)
# =====================================
# Festlegung der Simulations-Parameter:
# =====================================
# %%
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
for surf in geometryList:
    if surf.idExt not in geoTranslationDict.keys():
        geoTranslationDict[surf.idExt] = surf
    else:
        raise RuntimeError(
            f"Surface ID '{surf.idExt}' allready in geometry dict!"
        )

geometryLineListFinish = []
for surf in geometryList:
    geometryLineListFinish.extend(surf.curve)

print("Plot ENDE:")
plot(geometryLineListFinish, linewidth=1, markersize=3, tag=True)
print("---")


paramDict = createParamDict(
    machine, simulation, movingband_r, magnetizationDict
)
main(
    geo=geoTranslationDict,
    extInfo=paramDict,
    model=os.path.join(resFolder, fileName.split(".")[0]),
    results=os.path.join(resFolder, fileName.split(".")[0], "res"),
)

# %%
