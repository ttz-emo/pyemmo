import pyleecan
from os import path
from os.path import join
import sys
import json
import math
from numpy import pi
from typing import List

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
import pyleecan.Classes.Machine
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
SPMSMMuster3Shaft = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_3Shaft.json")
)
SPMSMMuster4Shaft = load(
    join("C:\\Users\\k49976\\Desktop", "SPMSMPyleecanMuster_4Shaft.json")
)
# Import ASM:
SCIM_motor = load(join(DATA_DIR, "Machine", "SCIM_L2EP_48s_2p.json"))


allBands, geometryList = buildPyemmoMovingBand(machine=SPMSMMuster4Shaft)

geometryLineListFinish=[]
for a, surf in enumerate(geometryList):
    for b, line in enumerate(surf.curve):
        geometryLineListFinish.append(line)
        
print("Plot ENDE:")
plot(geometryLineListFinish, linewidth=1, markersize=3, tag=True)
print("---")