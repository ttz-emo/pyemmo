# %%
import os
import sys
import numpy as np

from pyleecan.Functions.load import load
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
from pyemmo.functions.plot import plot
from pyemmo.api.json import main
from pyemmo.definitions import ROOT_DIR
from workingDirectory.buildPyemmoMovingBand import translate_machine_geo
from workingDirectory.createParamDict import createParamDict


# Simulation Function
def generateSimulation(
    machine: Machine,
    i_d: float = 0.0,
    i_q: float = 10.0,
    speed: float = 1000.0,
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
    simu.input.OP = OPdq(Id_ref=i_d, Iq_ref=i_q, N0=speed)

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
# ==============================================
# Determination of the machine to be calculated:
# ==============================================

machineFolder = os.path.join(ROOT_DIR, "workingDirectory/machineData")
resFolder = os.path.join(ROOT_DIR, r"Results\pyleecanAPI")
machineList = []
for i, file in enumerate(os.listdir(machineFolder)):
    if file.endswith(".json") and not "FEMM" in file:
        machineList.append(file)
        print(f"{machineList.index(file)}: " + file)
fileName = machineList[1]  # SELECT MACHINE HERE BY INDEX OR NAME
print("\nUsing machine: " + fileName)
machine: Machine = load(os.path.abspath(os.path.join(machineFolder, fileName)))
simulation = generateSimulation(machine, i_d=0, i_q=10, speed=1000)

# --------------------------
# isInternalRotor detection:
# --------------------------
isInternalRotor = machine.rotor.is_internal

if isinstance(machine, (MachineSIPMSM, MachineIPMSM, MachineSyRM)):
    (
        allBands,
        geometryList,
        movingband_r,
        magnetizationDict,
        geo_translation_dict,
    ) = translate_machine_geo(
        machine=machine,
        is_internal_rotor=isInternalRotor,
    )

else:
    raise ValueError("Machine type is not translatable!")


geometryLineListFinish = []
for surf in geometryList:
    geometryLineListFinish.extend(surf.curve)

print("Plot ENDE:")
# plot(geometryLineListFinish, linewidth=1, markersize=3, tag=True)
print("---")

paramDict = createParamDict(
    machine, simulation, movingband_r, magnetizationDict
)

main(
    geo=geo_translation_dict,
    extInfo=paramDict,
    model=os.path.join(resFolder, fileName.split(".")[0]),
    results=os.path.join(resFolder, fileName.split(".")[0], "res"),
)

# %%
