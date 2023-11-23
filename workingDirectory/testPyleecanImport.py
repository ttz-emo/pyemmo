import pyleecan
from os import path
from os.path import join
import sys
import json
import math
from numpy import pi
from typing import List
import swat_em as swatem

# ===============
# Imports pyemmo:
# ===============
try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.material.material import Material
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from Tests import save_plot_path
from pyemmo.functions.plot import plot
from workingDirectory.buildPyemmoMovingBand import buildPyemmoMovingBand
from pyemmo.api.json import main

# =================
# Imports pyleecan:
# =================
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind
import pyleecan.Classes.LamSquirrelCage
import pyleecan.Classes.Segment
import pyleecan.Classes.Arc1
import pyleecan.Classes.Arc2
import pyleecan.Classes.Arc3
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.Lamination import Lamination
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Methods.Simulation.MagElmer import (
    MagElmer_BP_dict,
)


# ===================
# Import of Machines:
# ===================
# Import IPMSM
IPMSM_motor = load(join(DATA_DIR, "Machine", "IPMSM_B.json"))
# Import SPMSM:
SPMSM_motor = load(join(DATA_DIR, "Machine", "SPMSM_002.json"))
# directory = "C:\Users\k49976\Desktop"
SPMSMMuster = load(join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster.json"))
SPMSMMuster2 = load(join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_2.json"))
SPMSMMuster2Shaft = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_2Shaft.json")
)
SPMSMMuster2ShaftSIMU = load(
    join(
        "C:\\Users\\k49976\\Desktop\\TEST_TRANSLATION\\2023_11_16-14h50min23s_FEMM_SPMSMPyleecanMuster_2Shaft",
        "FEMM_SPMSMPyleecanMuster_2Shaft.json",
    )
)
SPMSMMuster3Shaft = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_3Shaft.json")
)
SPMSMMuster4Shaft = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_4Shaft.json")
)
SPMSMMuster4ShaftSIMU = load(
    join(
        "C:\\Users\\k49976\\Desktop\\TEST_TRANSLATION\\2023_11_15-13h38min47s_FEMM_SPMSMPyleecanMuster_4Shaft",
        "FEMM_SPMSMPyleecanMuster_4Shaft.json",
    )
)
SPMSMMuster4Shaftinverted = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_4Shaft_inverted.json")
)
SPMSMMuster4ShaftinvertedSIMU = load(
    join(
        "C:\\Users\\k49976\\Desktop\\TEST_TRANSLATION\\2023_11_21-16h00min55s_FEMM_SPMSMPyleecanMuster_4Shaft_inverted",
        "FEMM_SPMSMPyleecanMuster_4Shaft_inverted.json",
    )
)
# Import ASM:
SCIM_motor = load(join(DATA_DIR, "Machine", "SCIM_L2EP_48s_2p.json"))

# ========================================
# Festlegung der zu berechnenden Maschine:
# ========================================
machine = SPMSMMuster4Shaftinverted

# =====================================
# Festlegung der Simulations-Parameter:
# =====================================
isInternalRotor: bool = False

rotorRext = machine.rotor.Rext
rotorRint = machine.rotor.Rint
statorRint = machine.stator.Rint
H0 = machine.rotor.slot.H0
Hmag = machine.rotor.slot.Hmag
if isInternalRotor:
    magnetFarthestRadius = rotorRext + Hmag - H0
    magnetShortestRadius = rotorRext - H0
else:
    magnetFarthestRadius = rotorRint + H0
    magnetShortestRadius = rotorRint + H0 - Hmag

# --------------------------
# isInternalRotor detection:
# --------------------------
isInternalRotor = bool(statorRint > rotorRext)

allBands, geometryList, movingband_r = buildPyemmoMovingBand(
    machine, rotorRext, statorRint, isInternalRotor,magnetFarthestRadius, magnetShortestRadius
)

geoTranslationDict = {}
for a, surfAPI in enumerate(geometryList):
    geoTranslationDict[surfAPI.idExt] = surfAPI

geometryLineListFinish = []
for a, surf in enumerate(geometryList):
    for b, line in enumerate(surf.curve):
        geometryLineListFinish.append(line)

print("Plot ENDE:")
plot(geometryLineListFinish, linewidth=1, markersize=3, tag=True)
print("---")


def translateWinding(machine: Machine):
    winding = swatem.datamodel()
    Q = machine.stator.slot.Zs
    P = machine.stator.winding.p * 2
    m = machine.stator.winding.qs
    layers = machine.stator.winding.Nlayer
    turns = machine.stator.winding.Ntcoil

    winding.genwdg(
        Q=Q,
        P=P,
        m=m,
        layers=layers,
        turns=turns,
    )
    windSwat = winding.get_phases()

    return windSwat


def createParamDict(machine: Machine, pyleecanSimulation: Simulation) -> dict[str, any]:
    """
    This function builds a dictionary for communication between pyleecan and pyemmo.

    The following part of the function tests if 'Id_ref' and 'Iq_ref' are having values
    and if so their values will directly be set in the dictionary under 'Id' and 'Iq'.
    If only 'I0_Phi0' has a set value but 'Id_ref' and 'Iq_ref' don't 'Id' and 'Iq' will be
    calculated.

    """

    op = pyleecanSimulation.input.OP

    if isinstance(op, OPdq):
        Id = op.Id_ref
        Iq = op.Iq_ref

    else:
        Id = 0
        Iq = 0
        print('!! Warning: No Values set for "Id_ref" and "Iq_ref" -> Id = Iq = 0 !!')

    # --------------------------------------------------------------------------------------
    # The following part of the function tests if rotor or stator have magnets and if so
    # if there are more than one magnet build in.
    # If there are magnets, the type of the magnetization will be safed in 'pyemmoMagType'.
    # 'pyemmoMagType': [0] : parallel
    #                  [1] : radial
    #                  [2] : Hallbach (!! not implemented in pyemmo !!)
    #                  [3] : tangential
    # If there are no magnets in rotor and stator, 'pyemmoMagType' will be set to 'None'.
    # --------------------------------------------------------------------------------------

    lamWithMag: Lamination = None

    if pyleecanSimulation.machine.rotor.has_magnet():  # Test, if rotor has magnet(s)
        lamWithMag = pyleecanSimulation.machine.rotor

    elif (
        pyleecanSimulation.machine.stator.has_magnet()
    ):  # Test, if stator has magnet(s)
        lamWithMag = pyleecanSimulation.machine.stator

    else:  # If rotor doesn't have magnets, pyemmoMagType = None
        pyemmoMagType = None

    if lamWithMag:
        if isinstance(
            lamWithMag, LamHole
        ):  # Test, if lamWithMag has Holes where the magnet(s) sit(s) in
            if isinstance(
                lamWithMag.hole, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmoMagType = lamWithMag.hole[0].magnet_0.type_magnetization

            else:  # If lamWithMag has only one magnet
                pyemmoMagType = lamWithMag.hole.magnet_0.type_magnetization

        elif isinstance(
            lamWithMag, LamSlotMag
        ):  # Test, if lamWithMag has Slots where the magnet(s) sit(s) in
            if isinstance(
                lamWithMag.slot, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmoMagType = lamWithMag.slot[0].magnet_0.type_magnetization

            else:  # If rotor has only one magnet
                pyemmoMagType = lamWithMag.magnet.type_magnetization

        else:
            # Error
            raise RuntimeError(
                f'Lamination of type "{str(type(lamWithMag))}" is not type LamHole or LamSlotMag.'
            )
    if pyemmoMagType == 0:
        pyemmoMagType = "radial"
    elif pyemmoMagType == 1:
        pyemmoMagType = "parallel"
    elif pyemmoMagType == 3:
        pyemmoMagType = "tangential"

    # ----------------------------------------------------------------------------------------------------------------
    symFactor = machine.comp_periodicity_spatial()
    if symFactor[1]:
        symFactor = symFactor[0] * 2
    else:
        symFactor = symFactor[0]

    translationParameterDict = {
        "winding": translateWinding(machine),  # winding layout for given geometry
        "wickSWAT": translateWinding(machine),
        "NpP": machine.stator.winding.Npcp,  # number of parallel paths per winding phase
        "Ntps": machine.stator.winding.Ntcoil,
        "z_pp": machine.stator.winding.p,  # number of pole pairs
        "Qs": machine.stator.slot.Zs,  # number of stator slots
        "movingband_r": movingband_r,  # moving band radius in meters
        "axLen_S": machine.stator.L1,  # axial length of stator
        "axLen_R": machine.rotor.L1,  # axial length of rotor
        "symFactor": symFactor,  # symmetry factor for model (STANDARD = 1) has to be defined
        "startPos": 0,  # start rotor position in ° (STANDARD = 0°)
        "endPos": pyleecanSimulation.input.Na_tot * 360,  # end rotor position in °
        "nbrSteps": pyleecanSimulation.input.Nt_tot,  # number of time steps for simulation
        "rot_freq": pyleecanSimulation.input.OP.N0 / 60,  # rotational frequency in Hz
        "parkAngleOffset": None,  # park transformation offset angle in elec. ° (STANDARD = None)
        "analysisType": 1,  # 0=static; 1=transient (STANDARD = 1)
        "tempMag": 20,  # magnet temperature °C (STANDARD = 20°C)
        "r_z": 0.7,  # tooth radius in meterm (STANDARD = None)
        "r_j": 0.9,  # yoke radius in meter (STANDARD = None)
        "id": Id,  # d-axis current in A
        "iq": Iq,  # q-axis current in A
        "modelName": machine.name,  # name of the model files
        "magDirection": pyemmoMagType,  # magnetization Type/ type of permament magnets(“parallel”, “radial” or “tangential”)
        "flag_openGUI": True,  # open Gmsh GUI after model generation (STANDARD = True)
        "calcIronLoss": False,
    }

    with open("translationDict.json", "w") as json_file:
        json.dump(translationParameterDict, json_file, indent=4)

    return translationParameterDict


paramDict = createParamDict(machine, SPMSMMuster4ShaftinvertedSIMU)
main(
    geo=geoTranslationDict,
    extInfo=paramDict,
    model="TEST_TRANSLATION",
    gmsh="C:\\Software\\Onelab\\gmsh.exe",
)
