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

from __future__ import annotations

# %%
import math
import os
import subprocess
import sys

from swat_em.datamodel import datamodel

try:
    from pyemmo.script.script import Script
except:
    try:
        rootname = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except:
        rootname = r"C:\Users\k49976\Desktop\repositoryGibLab\pyemmo"
        print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    from pyemmo.version import __version__

    print(__version__)
    from pyemmo.script.script import Script

from pyemmo.definitions import RESULT_DIR
from pyemmo.functions.runOnelab import createCmdCommand
from pyemmo.script.geometry.airArea import AirArea
from pyemmo.script.geometry.airGap import AirGap
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.limitLine import LimitLine
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.machineAllType import MachineAllType
from pyemmo.script.geometry.magnet import Magnet
from pyemmo.script.geometry.movingBand import MovingBand
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.primaryLine import PrimaryLine
from pyemmo.script.geometry.rotor import Rotor
from pyemmo.script.geometry.rotorLamination import RotorLamination
from pyemmo.script.geometry.slaveLine import SlaveLine
from pyemmo.script.geometry.slot import Slot
from pyemmo.script.geometry.stator import Stator
from pyemmo.script.geometry.statorLamination import StatorLamination
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.material.material import Material
from pyemmo.script.script import Script

#######################################################
#           Koordinatensystem aufbauen
P0 = Point("P0", 0, 0, 0, 1)
Px = Point("Px", 1, 0, 0, 1)
Py = Point("Py", 0, 1, 0, 1)
Pz = Point("Pz", 0, 0, 1, 1)

ex = Line("ex", P0, Px)
ey = Line("ey", P0, Py)
ez = Line("ez", P0, Pz)
####################################################

####################################################
#       Rotorparameter (ausgedacht!)
PBohrung = Point("mittelPunktBohrung", 0, 0, 0, 5e-3)

# Material aus Datenbank laden
steel_1010 = Material.load("steel_1010")
# steel_1010.load("M330_50AP_050Hz") # bug in material bh curve

ndFe35 = Material.load("NdFe35")
air = Material.load("air")
copper = Material.load("copper")

# parameters
nbrSlots = 12
nbrPoles = 8
symFactor = 4


def createRotorPMSM():
    airGapAll = 37e-3 - 33.3e-3 - 2.9e-3
    # Erzeugung der Punkte
    mRotor = Point("mRotor", 0, 0, 0, 0.1)
    mPolshape = Point("mPolshape", 33.3e-3 - 15e-3, 0, 0, 0.005)
    mPolshape.rotateZ(mRotor, math.pi / 8)
    mMag = Point("mMag", (33.3e-3 - 15e-3) + 2.9e-3, 0, 0, 0.005)
    mMag.rotateZ(mRotor, math.pi / 8)
    dR1 = Point("dR1", 28e-3 / 2, 0, 0, 0.002)
    dR2 = dR1.duplicate()
    dR2.rotateZ(mRotor, math.pi / 8)
    dR3 = Point("dR3", 30.38e-3, 0, 0, 0.001)
    dR4 = Point("dR4", 0.030377315912837346, 0.0004038290872121964, 0.0, 0.002)
    dR5 = Point("dR5", 33.3e-3, 0, 0, 0.001)
    dR5.rotateZ(mRotor, math.pi / 8)
    dM2 = Point("dM2", 33.3e-3 + 2.9e-3, 0, 0, 0.0003)
    dM2.rotateZ(mRotor, math.pi / 8)
    dM3 = Point("dM3", 0.030378517125591847, 0.0004062815449140659, 0.0, 0.002)
    dM1 = Point("dM1", 0.03305776776987458, 0.0015160634987728214, 0.0, 0.0002)

    ddB1 = Point("ddB1", 33.3e-3 + 2.9e-3 + 2 * airGapAll / 4, 0, 0, 0.0003)
    ddB2 = ddB1.duplicate()
    ddB2.rotateZ(mRotor, math.pi / 8)
    ddCR1 = Point("ddCR1", 33.3e-3 + 2.9e-3 + airGapAll / 4, 0, 0, 0.0003)
    ddCR2 = ddCR1.duplicate()
    ddCR2.rotateZ(mRotor, math.pi / 8)

    # Erzeugung der Linien
    dLR1 = CircleArc("dLR1", dR1, mRotor, dR2)
    dLR2 = Line("dLR2", dR1, dR3)
    dLR3 = CircleArc("dLR3", dR3, mRotor, dR4)
    dLR4 = CircleArc("dLR4", dR4, mPolshape, dM3)
    dLR5 = Line("dLR5", dR2, dR5)
    dLR6 = CircleArc("dLR6", dM3, mPolshape, dR5)
    dLRM1 = Line("dLRM1", dM1, dM3)
    dLRM2 = Line("dLRM2", dR5, dM2)
    dLRM3 = CircleArc("dLRM3", dM2, mMag, dM1)

    dLdB1 = CircleArc("dLdB1", ddB1, mRotor, ddB2)
    dLdB2 = Line("dLdB2", ddB2, ddCR2)
    dLdB3 = Line("dLdB3", ddCR1, ddB1)
    dLdC1 = CircleArc("dLdC1", ddCR1, mRotor, ddCR2)
    dLdC2 = Line("dLdC2", ddCR2, dM2)
    dLdC3 = Line("dLdC3", ddCR1, dR3)

    # Erzeugung der Flächen
    s_RotorBlech_01 = Surface("s_RotorBlech", [dLR1, dLR5, dLR6, dLR4, dLR3, dLR2])
    s_Magnet_01 = Surface("s_Magnet", [dLR6, dLRM2, dLRM3, dLRM1])
    s_Container_01 = Surface(
        "s_Container", [dLdC1, dLdC2, dLRM3, dLRM1, dLR4, dLR3, dLdC3]
    )
    s_Luftspalt_01 = Surface("s_Luftspalt", [dLdC1, dLdB2, dLdB1, dLdB3])

    s_RotorBlech = [s_RotorBlech_01]
    s_Magnet = [s_Magnet_01]
    s_Container = [s_Container_01]
    s_Luftspalt = [s_Luftspalt_01]
    mbR_all = [dLdB1]
    innerLimit = [dLR1]

    hP1 = dR2.duplicate()
    hL = Line("hL", PBohrung, hP1)  # Hilfslinie für mirror-Befehl

    # Duplizieren und Rotieren der Segmente für Teilmodell
    for i in range(0, 3):
        s_Rot = s_RotorBlech[len(s_RotorBlech) - 1].mirror(PBohrung, ez, hL)
        s_RotorBlech.append(s_Rot)
        s_Mag = s_Magnet[len(s_Magnet) - 1].mirror(PBohrung, ez, hL)
        s_Magnet.append(s_Mag)
        s_Con = s_Container[len(s_Container) - 1].mirror(PBohrung, ez, hL)
        s_Container.append(s_Con)
        s_Luft = s_Luftspalt[len(s_Luftspalt) - 1].mirror(PBohrung, ez, hL)
        s_Luftspalt.append(s_Luft)
        hL.rotateZ(PBohrung, math.pi / 8)

        mbR = mbR_all[len(mbR_all) - 1].duplicate()
        mbR.rotateZ(mRotor, math.pi / 8)
        mbR_all.append(mbR)

        iL = innerLimit[len(innerLimit) - 1].duplicate()
        iL.rotateZ(mRotor, math.pi / 8)
        innerLimit.append(iL)

    # Movingband Linien und Definition
    mbRotorAux = []
    for i2 in range(1, 4):
        mbR_allAux = []
        for mb in mbR_all:
            mbAux = mb.duplicate()
            mbAux.rotateZ(mRotor, i2 * math.pi / 2)
            mbR_allAux.append(mbAux)
        # outer part of the moving band
        mbR_Aux = MovingBand("", mbR_allAux, air, auxiliary=True)
        mbR_Aux.name = "mbRotor_" + str(mbR_Aux.id)
        mbRotorAux.append(mbR_Aux)

    # Definition der PhysicalElements
    rotorBlech = RotorLamination(
        name="rotorBlech", geo_list=s_RotorBlech, material=steel_1010
    )
    magnet1 = Magnet(
        name="magnet_Nord",
        geoElements=s_Magnet[0:2],
        material=ndFe35,
        magDirection=1,
        magType="radial",
        magVectorAngle=0.0,
    )
    magnet2 = Magnet(
        "magnet_Sued", s_Magnet[2:4], ndFe35, -1, "radial", magVectorAngle=0.0
    )
    luft = AirArea(name="luft", geo_list=s_Container, material=air)
    luftspalt = AirGap("luftspalt", s_Luftspalt, air)
    masterR = PrimaryLine("masterR", [dLR2, dLdB3, dLdC3])
    # Prime-Linien duplizieren und Rotieren
    slave_R = [dLR2.duplicate(), dLdB3.duplicate(), dLdC3.duplicate()]
    for sR in slave_R:
        sR.rotateZ(mRotor, math.pi / 2)
    slaveR = SlaveLine("slaveR", slave_R)

    mbRotor = MovingBand(name="mbRotor", geo_list=mbR_all, material=air)
    phy_innerLimit = LimitLine("innerLimitRotor", innerLimit)

    return Rotor(
        physicalElementList=[
            rotorBlech,
            magnet1,
            magnet2,
            luft,
            luftspalt,
            masterR,
            slaveR,
            mbRotor,
            phy_innerLimit,
        ]
        + mbRotorAux,
        name="StatorPMSM_free",
        axLen=0.1,
    )


def createStatorPMSM():
    airGapAll = 37e-3 - 33.3e-3 - 2.9e-3
    mStator = Point("mStator", 0, 0, 0, 0.0001)
    dS1 = Point("dS1", 37e-3, 0, 0, 0.0001)
    dS3_0 = dS1.duplicate()
    dS3_0.translate(0.35e-3, 0, 0)
    win = math.atan(3e-3 / (2 * 37e-3))
    dS2 = dS1.duplicate()
    dS2.rotateZ(mStator, win)
    dS3 = dS3_0.duplicate()
    dS3.rotateZ(mStator, win)
    dS4 = Point("dS4", 37e-3 + 1.6e-3, 11.3865e-3 / 2, 0, 0.003)
    dS5 = Point("dS5", 37e-3 + 14.566e-3, 18.335e-3 / 2, 0, 0.003)
    dS6 = Point("dS6", 37e-3 + 14.566e-3 + 2.976e-3, 0, 0, 0.003)

    dS7 = Point(
        "dS7",
        37e-3 * math.cos(math.pi / 12),
        37e-3 * math.sin(math.pi / 12),
        0,
        0.0003,
    )
    dS8 = Point(
        "dS8",
        60.9e-3 * math.cos(math.pi / 12),
        60.9e-3 * math.sin(math.pi / 12),
        0,
        0.003,
    )
    dS9 = Point("dS9", 60.9e-3, 0, 0, 0.003)

    ################################################################
    #               Band Punkte erzeugen
    ################################################################
    rContainer_Stator = 37e-3 - 0.25 * airGapAll
    ddC1 = Point("ddC1", rContainer_Stator, 0, 0, 0.0001)
    ddC2 = ddC1.duplicate()
    ddC2.rotateZ(mStator, math.pi / 12)

    ################################################################
    #               Linien erzeugen
    ################################################################
    dLS2 = Line("dLS2", dS2, dS3)
    dLS3 = Line("dLS3", dS3, dS4)
    dLS4 = Line("dLS4", dS4, dS5)
    dLS5 = Line("dLS5", dS5, dS6)
    dLS6 = Line("dLS6", dS6, dS3_0)
    dLS7 = Line("dLS7", dS6, dS9)
    dLS8 = CircleArc("dLS8", dS9, mStator, dS8)
    dLS9 = Line("dLS9", dS8, dS7)
    dLS10 = CircleArc("dLS10", dS7, mStator, dS2)

    dLNS1 = CircleArc("dLNS1", dS1, mStator, dS2)
    dLNS2 = CircleArc("dLNS2", dS3, mStator, dS3_0)
    dLNS3 = Line("dLNS3", dS3_0, dS1)

    ################################################################
    #               Band Linien erzeugen
    ################################################################
    dLdCS1 = CircleArc("dLdCS1", ddC1, mStator, ddC2)
    dLdCSS1 = Line("dLdCSS1", dS1, ddC1)
    dLdCSS2 = Line("dLdCSS2", dS7, ddC2)

    ################################################################
    #               Fläche erzeugen
    ################################################################

    mbS_all = [dLdCS1]
    masterLine = [dLS6, dLS7, dLNS3, dLdCSS1]
    slaveLine = []
    for mL in masterLine:
        sL = mL.duplicate()
        sL.rotateZ(mStator, math.pi / 2)
        slaveLine.append(sL)
    outerLine = [dLS8]

    s_statorblech01 = Surface(
        "statorblech_01", [dLS2, dLS3, dLS4, dLS5, dLS7, dLS8, dLS9, dLS10]
    )
    s_Nutschlitz01 = Surface("nutschlitz_01", [dLS2, dLNS2, dLNS3, dLNS1])
    s_Nut01 = Surface("nut_01", [dLNS2, dLS6, dLS5, dLS4, dLS3])
    s_Luftspalt01 = Surface("Luftspalt_01", [dLNS1, dLS10, dLdCSS2, dLdCS1, dLdCSS1])

    s_Statorblech = [s_statorblech01]
    s_Nutschlitz = [s_Nutschlitz01]
    s_Nut = [s_Nut01]
    s_Luftspalt = [s_Luftspalt01]

    hP1 = dS8.duplicate()
    hL = Line("hL", PBohrung, hP1)
    hL2 = hL.duplicate()

    for i in range(0, 5):
        s_Stat = s_Statorblech[len(s_Statorblech) - 1].mirror(PBohrung, ez, hL)
        s_Statorblech.append(s_Stat)
        s_N = s_Nut[len(s_Nut) - 1].mirror(PBohrung, ez, hL)
        s_Nut.append(s_N)
        s_Ns = s_Nutschlitz[len(s_Nutschlitz) - 1].mirror(PBohrung, ez, hL)
        s_Nutschlitz.append(s_Ns)
        s_Luft = s_Luftspalt[len(s_Luftspalt) - 1].mirror(PBohrung, ez, hL)
        s_Luftspalt.append(s_Luft)
        oL = outerLine[len(outerLine) - 1].duplicate()
        oL.rotateZ(mStator, math.pi / 12)
        outerLine.append(oL)
        hL.rotateZ(PBohrung, math.pi / 12)

    for i3 in range(0, 5):
        mbS = mbS_all[len(mbS_all) - 1].mirror(PBohrung, ez, hL2)
        mbS_all.append(mbS)
        hL2.rotateZ(PBohrung, math.pi / 12)

    phy_StatorBlech = StatorLamination("StatorBlech", s_Statorblech, steel_1010)
    phy_Nutschlitz = AirArea("Nutschlitz", s_Nutschlitz, air)
    allSlot: list[Slot] = []
    for i2 in range(0, len(s_Nut)):
        allSlot.append(Slot(name="", geo_list=[s_Nut[i2]], material=copper))
        allSlot[len(allSlot) - 1].name = "slot_" + str(allSlot[len(allSlot) - 1].id)
        # allSlot[len(allSlot) - 1].addExcitation(windingInstruction[i2])
    phy_airGap = AirGap("luftspalt_stator", s_Luftspalt, air)

    phy_mb = MovingBand("mbStator", mbS_all, air)
    phy_master = PrimaryLine("masterS", masterLine)
    phy_slave = SlaveLine("slaveS", slaveLine)
    phy_outerLimit = LimitLine("outerLimitStator", outerLine)

    # create SWAT-EM winding obj.
    winding = datamodel()
    winding.genwdg(Q=nbrSlots, P=nbrPoles, m=3, layers=2, turns=12)

    return Stator(
        nbrSlots=nbrSlots,
        physicalElements=[
            phy_StatorBlech,
            phy_Nutschlitz,
            phy_airGap,
            phy_mb,
            phy_master,
            phy_slave,
            phy_outerLimit,
        ]
        + allSlot,
        name="StatorPMSM_free",
        axLen=0.1,
        winding=winding,
    )


# %%
# create machine

rotor = createRotorPMSM()
stator = createStatorPMSM()

rotor.plot()
stator.plot()
machine = MachineAllType(
    name="PMSM_free",
    nbrPolePairs=nbrPoles / 2,
    symmetryFactor=symFactor,
    rotor=rotor,
    stator=stator,
)
machine.plot()

# %%
# create script
scriptPath = os.path.join(RESULT_DIR, "testFreeGeoDef")
if not os.path.isdir(scriptPath):
    os.mkdir(scriptPath)
pmsmScript = Script(
    name="test_pmsm_freeDefined",
    scriptPath=scriptPath,
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
    machine=machine,
)
pmsmScript.generateScript()
# %%
# subprocess.run(createCmdCommand(pmsmScript.getGeoFilePath(), True), check=False)
subprocess.run(createCmdCommand(pmsmScript.proFilePath, True), check=False)
