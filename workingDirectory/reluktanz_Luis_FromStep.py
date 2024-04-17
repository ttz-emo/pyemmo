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
from os import path
from setPath import pathRes
from pyemmo.script.geometry.domain import Domain, PhysicalElement
from pyemmo.script.script import Script
import math
from stepToEMMO import getAdaptedPath, changeToEmmoObjects

# pathStepDir = r'C:\Users\koenig\Desktop\Maschine_Luis'
pathStepDir = path.abspath(path.join(path.dirname(__file__), "???"))


objPath = getAdaptedPath(pathStepDir)
pyemmoObj = changeToEmmoObjects(objPath, unit=1)

phy_phase_U_pos = PhysicalElement(
    "Phase_U_pos", pyemmoObj["sur_phase_U_pos"], None, 2100
)
phy_phase_U_neg = PhysicalElement(
    "Phase_U_neg", pyemmoObj["sur_phase_U_neg"], None, 2101
)
phy_phase_V_pos = PhysicalElement(
    "Phase_V_pos", pyemmoObj["sur_phase_V_pos"], None, 2102
)
phy_phase_V_neg = PhysicalElement(
    "Phase_V_neg", pyemmoObj["sur_phase_V_neg"], None, 2103
)
phy_phase_W_pos = PhysicalElement(
    "Phase_W_pos", pyemmoObj["sur_phase_W_pos"], None, 2104
)
phy_phase_W_neg = PhysicalElement(
    "Phase_W_neg", pyemmoObj["sur_phase_W_neg"], None, 2105
)
phy_StatorSheet = PhysicalElement(
    "StatorSheet", pyemmoObj["sur_StatorSheet"], None, 2001
)
phy_AirSlot = PhysicalElement("AirSlot", pyemmoObj["sur_AirSlot"], None, 2002)
phy_AirGapStator = PhysicalElement(
    "AirGapStator", pyemmoObj["sur_AirGapStator"], None, 2003
)
phy_RotorSheet = PhysicalElement(
    "RotorSheet", pyemmoObj["sur_RotorSheet"], None, 1001
)
phy_RotorSeg = PhysicalElement(
    "RotorSeg", pyemmoObj["sur_RotorSeg"], None, 1002
)
phy_RotorAir = PhysicalElement(
    "RotorAir", pyemmoObj["sur_RotorAir"], None, 1004
)
phy_AirGapRotor = PhysicalElement(
    "AirGapRotor", pyemmoObj["sur_AirGapRotor"], None, 1003
)

phy_outerLineLimit = PhysicalElement(
    "OuterLineLimit", pyemmoObj["curve_outerLineLimit"], None, 20001
)
phy_statorSlave = PhysicalElement(
    "StatorSlave", pyemmoObj["curve_statorSlave"], None, 20011
)
phy_statorMaster = PhysicalElement(
    "StatorMaster", pyemmoObj["curve_statorMaster"], None, 20012
)
phy_statorMB = PhysicalElement(
    "StatorMB", pyemmoObj["curve_statorMB"], None, 20020
)

phy_innerLineLimit = PhysicalElement(
    "InnerLineLimit", pyemmoObj["curve_innerLineLimit"], None, 10001
)
phy_rotorSlave = PhysicalElement(
    "RotorSlave", pyemmoObj["curve_rotorSlave"], None, 10011
)
phy_rotorMaster = PhysicalElement(
    "RotorMaster", pyemmoObj["curve_rotorMaster"], None, 10012
)
phy_rotorMB1 = PhysicalElement(
    "RotorMB1", pyemmoObj["curve_rotorMB1"], None, 10020
)
phy_rotorMB2 = PhysicalElement(
    "RotorMB2", pyemmoObj["curve_rotorMB2"], None, 10021
)

phy_contour = PhysicalElement(
    "Contour", pyemmoObj["curve_Contour"], None, 1111111
)


domainMaschine = Domain(
    "domainMaschine",
    [
        phy_phase_U_pos,
        phy_phase_U_neg,
        phy_phase_V_pos,
        phy_phase_V_neg,
        phy_phase_W_pos,
        phy_phase_W_neg,
        phy_StatorSheet,
        phy_AirSlot,
        phy_AirGapStator,
        phy_RotorSheet,
        phy_RotorSeg,
        phy_RotorAir,
        phy_AirGapRotor,
        phy_outerLineLimit,
        phy_statorSlave,
        phy_statorMaster,
        phy_statorMB,
        phy_innerLineLimit,
        phy_rotorSlave,
        phy_rotorMaster,
        phy_rotorMB1,
        phy_rotorMB2,
        phy_contour,
    ],
)
myScript = Script(name="Reluktanz", scriptPath=pathRes, simuParams={})
domainMaschine.addToScript(myScript)

# .geo-Datei erzeugen
myScript.generateScript()

print("done")
