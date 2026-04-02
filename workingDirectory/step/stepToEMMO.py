#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

from os.path import join
from typing import TYPE_CHECKING

import pyemmo as emmo

from .stepToArea import getCurveFromStep, getSurfaceFromStep

if TYPE_CHECKING:
    from pyemmo.script.geometry.line import Line
    from pyemmo.script.geometry.surface import Surface


# Verknüpft Ordnerpfad von Stepdatei mit dem Dateienamen und ergänzt diese mit der Endung .step
def joinStepPath(pathDir, fileNames):
    pathFiles = list()
    for file in fileNames:
        pathFiles.append(join(pathDir, file + ".step"))
    return pathFiles


def getAdaptedPath(pathStepDir):
    surfaceSeg1 = [
        "Rotor_Seg1_1",
        "Rotor_Seg1_2",
        "Rotor_Seg1_3",
        "Rotor_Seg1_4",
        "Rotor_Seg1_5",
        "Rotor_Seg1_6",
    ]
    surfaceSeg2 = [
        "Rotor_Seg2_1",
        "Rotor_Seg2_2",
        "Rotor_Seg2_3",
        "Rotor_Seg2_4",
        "Rotor_Seg2_5",
        "Rotor_Seg2_6",
    ]
    surfaceSeg3 = [
        "Rotor_Seg3_1",
        "Rotor_Seg3_2",
        "Rotor_Seg3_3",
        "Rotor_Seg3_4",
        "Rotor_Seg3_5",
        "Rotor_Seg3_6",
    ]
    surfaceSeg4 = [
        "Rotor_Seg4_1",
        "Rotor_Seg4_2",
        "Rotor_Seg4_3",
        "Rotor_Seg4_4",
        "Rotor_Seg4_5",
        "Rotor_Seg4_6",
    ]

    surfaceSegAir1 = ["Rotor_Seg1_5", "Rotor_Seg1_7"]
    surfaceSegAir2 = ["Rotor_Seg2_5", "Rotor_Seg2_7"]
    surfaceSegAir3 = ["Rotor_Seg3_5", "Rotor_Seg3_7"]
    surfaceSegAir4 = ["Rotor_Seg4_5", "Rotor_Seg4_7"]

    surfaceRotorSheet = [
        "Rotor_Seg1_1",
        "Rotor_Seg1_2",
        "Rotor_Seg1_3",
        "Rotor_Seg2_1",
        "Rotor_Seg2_2",
        "Rotor_Seg2_3",
        "Rotor_Seg3_1",
        "Rotor_Seg3_2",
        "Rotor_Seg3_3",
        "Rotor_Seg4_1",
        "Rotor_Seg4_2",
        "Rotor_Seg4_3",
        "Rotor_ZwSeg1",
        "Rotor_ZwSeg2",
        "Rotor_ZwSeg3",
        "Rotor_ZwSeg4",
        "Rotor_ZwSeg5",
        "Rotor_Master",
        "Rotor_Slave",
        "Rotor_Welle",
    ]

    surfaceAirGapRotor = [
        "Rotor_MB",
        "Rotor_MB_links",
        "Rotor_MB_rechts",
        "Rotor_zwSeg1",
        "Rotor_zwSeg2",
        "Rotor_zwSeg3",
        "Rotor_zwSeg4",
        "Rotor_zwSeg5",
        "Rotor_Seg1_4",
        "Rotor_Seg1_6",
        "Rotor_Seg1_7",
        "Rotor_Seg2_4",
        "Rotor_Seg2_6",
        "Rotor_Seg2_7",
        "Rotor_Seg3_4",
        "Rotor_Seg3_6",
        "Rotor_Seg3_7",
        "Rotor_Seg4_4",
        "Rotor_Seg4_6",
        "Rotor_Seg4_7",
    ]

    surfaceAirGapStator = [
        "Stator_Bohrung01",
        "Stator_Bohrung03",
        "Stator_Bohrung05",
        "Stator_Bohrung07",
        "Stator_Bohrung09",
        "Stator_Bohrung11",
        "Stator_Bohrung13",
        "Stator_BohrungNut1",
        "Stator_BohrungNut2",
        "Stator_BohrungNut3",
        "Stator_BohrungNut4",
        "Stator_BohrungNut5",
        "Stator_BohrungNut6",
        "Stator_MB",
        "Stator_MB_links",
        "Stator_MB_rechts",
    ]

    surfaceAirSlot1 = [
        "Stator_BohrungNut1",
        "Stator_Nutschlitz1",
        "Stator_Nutschlitz1links",
        "Stator_Nutschlitz1rechts",
    ]
    surfaceAirSlot2 = [
        "Stator_BohrungNut2",
        "Stator_Nutschlitz2",
        "Stator_Nutschlitz2links",
        "Stator_Nutschlitz2rechts",
    ]
    surfaceAirSlot3 = [
        "Stator_BohrungNut3",
        "Stator_Nutschlitz3",
        "Stator_Nutschlitz3links",
        "Stator_Nutschlitz3rechts",
    ]
    surfaceAirSlot4 = [
        "Stator_BohrungNut4",
        "Stator_Nutschlitz4",
        "Stator_Nutschlitz4links",
        "Stator_Nutschlitz4rechts",
    ]
    surfaceAirSlot5 = [
        "Stator_BohrungNut5",
        "Stator_Nutschlitz5",
        "Stator_Nutschlitz5links",
        "Stator_Nutschlitz5rechts",
    ]
    surfaceAirSlot6 = [
        "Stator_BohrungNut6",
        "Stator_Nutschlitz6",
        "Stator_Nutschlitz6links",
        "Stator_Nutschlitz6rechts",
    ]

    surfaceSlot1 = [
        "Stator_Nutschlitz1",
        "Stator_Nut1_1",
        "Stator_Nut1_2",
        "Stator_Nut1_3",
        "Stator_Nut1_4",
        "Stator_Nut1_5",
    ]
    surfaceSlot2 = [
        "Stator_Nutschlitz2",
        "Stator_Nut2_1",
        "Stator_Nut2_2",
        "Stator_Nut2_3",
        "Stator_Nut2_4",
        "Stator_Nut2_5",
    ]
    surfaceSlot3 = [
        "Stator_Nutschlitz3",
        "Stator_Nut3_1",
        "Stator_Nut3_2",
        "Stator_Nut3_3",
        "Stator_Nut3_4",
        "Stator_Nut3_5",
    ]
    surfaceSlot4 = [
        "Stator_Nutschlitz4",
        "Stator_Nut4_1",
        "Stator_Nut4_2",
        "Stator_Nut4_3",
        "Stator_Nut4_4",
        "Stator_Nut4_5",
    ]
    surfaceSlot5 = [
        "Stator_Nutschlitz5",
        "Stator_Nut5_1",
        "Stator_Nut5_2",
        "Stator_Nut5_3",
        "Stator_Nut5_4",
        "Stator_Nut5_5",
    ]
    surfaceSlot6 = [
        "Stator_Nutschlitz6",
        "Stator_Nut6_1",
        "Stator_Nut6_2",
        "Stator_Nut6_3",
        "Stator_Nut6_4",
        "Stator_Nut6_5",
    ]

    surfaceStatorSheet = [
        "Stator_Bohrung01",
        "Stator_Bohrung03",
        "Stator_Bohrung05",
        "Stator_Bohrung07",
        "Stator_Bohrung09",
        "Stator_Bohrung11",
        "Stator_Bohrung13",
        "Stator_Nutschlitz1links",
        "Stator_Nutschlitz1rechts",
        "Stator_Nutschlitz2links",
        "Stator_Nutschlitz2rechts",
        "Stator_Nutschlitz3links",
        "Stator_Nutschlitz3rechts",
        "Stator_Nutschlitz4links",
        "Stator_Nutschlitz4rechts",
        "Stator_Nutschlitz5links",
        "Stator_Nutschlitz5rechts",
        "Stator_Nutschlitz6links",
        "Stator_Nutschlitz6rechts",
        "Stator_Nut1_1",
        "Stator_Nut1_2",
        "Stator_Nut1_3",
        "Stator_Nut1_4",
        "Stator_Nut1_5",
        "Stator_Nut2_1",
        "Stator_Nut2_2",
        "Stator_Nut2_3",
        "Stator_Nut2_4",
        "Stator_Nut2_5",
        "Stator_Nut3_1",
        "Stator_Nut3_2",
        "Stator_Nut3_3",
        "Stator_Nut3_4",
        "Stator_Nut3_5",
        "Stator_Nut4_1",
        "Stator_Nut4_2",
        "Stator_Nut4_3",
        "Stator_Nut4_4",
        "Stator_Nut4_5",
        "Stator_Nut5_1",
        "Stator_Nut5_2",
        "Stator_Nut5_3",
        "Stator_Nut5_4",
        "Stator_Nut5_5",
        "Stator_Nut6_1",
        "Stator_Nut6_2",
        "Stator_Nut6_3",
        "Stator_Nut6_4",
        "Stator_Nut6_5",
        "Stator_Master",
        "Stator_Slave",
        "Stator_Aussen",
    ]

    curveOuterLineLimit = ["Stator_Aussen"]
    curveSlaveLineStator = ["Stator_Slave", "Stator_MB_links"]
    curveMasterLineStator = ["Stator_Master", "Stator_MB_rechts"]
    curveMBStator = ["Stator_MB"]

    curveInnerLineLimit = ["Rotor_Welle"]
    curveSlaveLineRotor = ["Rotor_Slave", "Rotor_MB_links"]
    curveMasterLineRotor = ["Rotor_Master", "Rotor_MB_rechts"]
    curveMBRotor = ["Rotor_MB"]

    curveContour = [
        "Rotor_Seg1_1",
        "Rotor_Seg1_2",
        "Rotor_Seg1_3",
        "Rotor_Seg1_4",
        "Rotor_Seg1_5",
        "Rotor_Seg1_6",
        "Rotor_Seg2_1",
        "Rotor_Seg2_2",
        "Rotor_Seg2_3",
        "Rotor_Seg2_4",
        "Rotor_Seg2_5",
        "Rotor_Seg2_6",
        "Rotor_Seg3_1",
        "Rotor_Seg3_2",
        "Rotor_Seg3_3",
        "Rotor_Seg3_4",
        "Rotor_Seg3_5",
        "Rotor_Seg3_6",
        "Rotor_Seg4_1",
        "Rotor_Seg4_2",
        "Rotor_Seg4_3",
        "Rotor_Seg4_4",
        "Rotor_Seg4_5",
        "Rotor_Seg4_6",
        "Rotor_ZwSeg1",
        "Rotor_ZwSeg2",
        "Rotor_ZwSeg3",
        "Rotor_ZwSeg4",
        "Rotor_ZwSeg5",
        "Rotor_Master",
        "Rotor_Slave",
        "Rotor_Welle",
        "Stator_Bohrung01",
        "Stator_Bohrung03",
        "Stator_Bohrung05",
        "Stator_Bohrung07",
        "Stator_Bohrung09",
        "Stator_Bohrung11",
        "Stator_Bohrung13",
        "Stator_Nutschlitz1links",
        "Stator_Nutschlitz1rechts",
        "Stator_Nutschlitz2links",
        "Stator_Nutschlitz2rechts",
        "Stator_Nutschlitz3links",
        "Stator_Nutschlitz3rechts",
        "Stator_Nutschlitz4links",
        "Stator_Nutschlitz4rechts",
        "Stator_Nutschlitz5links",
        "Stator_Nutschlitz5rechts",
        "Stator_Nutschlitz6links",
        "Stator_Nutschlitz6rechts",
        "Stator_Nut1_1",
        "Stator_Nut1_2",
        "Stator_Nut1_3",
        "Stator_Nut1_4",
        "Stator_Nut1_5",
        "Stator_Nut2_1",
        "Stator_Nut2_2",
        "Stator_Nut2_3",
        "Stator_Nut2_4",
        "Stator_Nut2_5",
        "Stator_Nut3_1",
        "Stator_Nut3_2",
        "Stator_Nut3_3",
        "Stator_Nut3_4",
        "Stator_Nut3_5",
        "Stator_Nut4_1",
        "Stator_Nut4_2",
        "Stator_Nut4_3",
        "Stator_Nut4_4",
        "Stator_Nut4_5",
        "Stator_Nut5_1",
        "Stator_Nut5_2",
        "Stator_Nut5_3",
        "Stator_Nut5_4",
        "Stator_Nut5_5",
        "Stator_Nut6_1",
        "Stator_Nut6_2",
        "Stator_Nut6_3",
        "Stator_Nut6_4",
        "Stator_Nut6_5",
        "Stator_Master",
        "Stator_Slave",
        "Stator_Aussen",
        "Stator_Nutschlitz1",
        "Stator_Nutschlitz2",
        "Stator_Nutschlitz3",
        "Stator_Nutschlitz4",
        "Stator_Nutschlitz5",
        "Stator_Nutschlitz6",
    ]

    pathSurfaceSeg1 = joinStepPath(pathStepDir, surfaceSeg1)
    pathSurfaceSeg2 = joinStepPath(pathStepDir, surfaceSeg2)
    pathSurfaceSeg3 = joinStepPath(pathStepDir, surfaceSeg3)
    pathSurfaceSeg4 = joinStepPath(pathStepDir, surfaceSeg4)

    pathSurfaceSegAir1 = joinStepPath(pathStepDir, surfaceSegAir1)
    pathSurfaceSegAir2 = joinStepPath(pathStepDir, surfaceSegAir2)
    pathSurfaceSegAir3 = joinStepPath(pathStepDir, surfaceSegAir3)
    pathSurfaceSegAir4 = joinStepPath(pathStepDir, surfaceSegAir4)

    pathSurfaceRotorsheet = joinStepPath(pathStepDir, surfaceRotorSheet)

    pathSurfaceAirGapRotor = joinStepPath(pathStepDir, surfaceAirGapRotor)

    pathSurfaceAirGapStator = joinStepPath(pathStepDir, surfaceAirGapStator)

    pathSurfaceAirSlot1 = joinStepPath(pathStepDir, surfaceAirSlot1)
    pathSurfaceAirSlot2 = joinStepPath(pathStepDir, surfaceAirSlot2)
    pathSurfaceAirSlot3 = joinStepPath(pathStepDir, surfaceAirSlot3)
    pathSurfaceAirSlot4 = joinStepPath(pathStepDir, surfaceAirSlot4)
    pathSurfaceAirSlot5 = joinStepPath(pathStepDir, surfaceAirSlot5)
    pathSurfaceAirSlot6 = joinStepPath(pathStepDir, surfaceAirSlot6)

    pathSurfaceSlot1 = joinStepPath(pathStepDir, surfaceSlot1)
    pathSurfaceSlot2 = joinStepPath(pathStepDir, surfaceSlot2)
    pathSurfaceSlot3 = joinStepPath(pathStepDir, surfaceSlot3)
    pathSurfaceSlot4 = joinStepPath(pathStepDir, surfaceSlot4)
    pathSurfaceSlot5 = joinStepPath(pathStepDir, surfaceSlot5)
    pathSurfaceSlot6 = joinStepPath(pathStepDir, surfaceSlot6)

    pathSurfaceStatorSheet = joinStepPath(pathStepDir, surfaceStatorSheet)

    # Linien von Step nach pyemmo -> Grenzlinien
    pathOuterLineLimit = joinStepPath(pathStepDir, curveOuterLineLimit)
    pathSlaveLineStator = joinStepPath(pathStepDir, curveSlaveLineStator)
    pathMasterLineStator = joinStepPath(pathStepDir, curveMasterLineStator)
    pathMBStator = joinStepPath(pathStepDir, curveMBStator)

    pathInnerLineLimit = joinStepPath(pathStepDir, curveInnerLineLimit)
    pathSlaveLineRotor = joinStepPath(pathStepDir, curveSlaveLineRotor)
    pathMasterLineRotor = joinStepPath(pathStepDir, curveMasterLineRotor)
    pathMBRotor = joinStepPath(pathStepDir, curveMBRotor)

    pathContour = joinStepPath(pathStepDir, curveContour)

    pathList = [
        ["SurfaceSeg1", pathSurfaceSeg1],
        ["SurfaceSeg2", pathSurfaceSeg2],
        ["SurfaceSeg3", pathSurfaceSeg3],
        ["SurfaceSeg4", pathSurfaceSeg4],
        ["SurfaceSegAir1", pathSurfaceSegAir1],
        ["SurfaceSegAir2", pathSurfaceSegAir2],
        ["SurfaceSegAir3", pathSurfaceSegAir3],
        ["SurfaceSegAir4", pathSurfaceSegAir4],
        ["SurfaceRotorSheet", pathSurfaceRotorsheet],
        ["SurfaceAirGapRotor", pathSurfaceAirGapRotor],
        ["SurfaceAirGapStator", pathSurfaceAirGapStator],
        ["SurfaceAirSlot1", pathSurfaceAirSlot1],
        ["SurfaceAirSlot2", pathSurfaceAirSlot2],
        ["SurfaceAirSlot3", pathSurfaceAirSlot3],
        ["SurfaceAirSlot4", pathSurfaceAirSlot4],
        ["SurfaceAirSlot5", pathSurfaceAirSlot5],
        ["SurfaceAirSlot6", pathSurfaceAirSlot6],
        ["SurfaceSlot1", pathSurfaceSlot1],
        ["SurfaceSlot2", pathSurfaceSlot2],
        ["SurfaceSlot3", pathSurfaceSlot3],
        ["SurfaceSlot4", pathSurfaceSlot4],
        ["SurfaceSlot5", pathSurfaceSlot5],
        ["SurfaceSlot6", pathSurfaceSlot6],
        ["SurfaceStatorSheet", pathSurfaceStatorSheet],
        ["OuterLineLimit", pathOuterLineLimit],
        ["SlaveLineStator", pathSlaveLineStator],
        ["MasterLineStator", pathMasterLineStator],
        ["MBStator", pathMBStator],
        ["InnerLineLimit", pathInnerLineLimit],
        ["SlaveLineRotor", pathSlaveLineRotor],
        ["MasterLineRotor", pathMasterLineRotor],
        ["MBRotor", pathMBRotor],
        ["Contour", pathContour],
    ]

    return pathList


def changeToEmmoObjects(objStepPath, unit=1) -> dict[str, list[Surface | Line]]:
    mesh_big = 2e-3 * unit
    mesh_middle = 5e-4 * unit
    mesh_small = 2e-4 * unit
    sur_phase_U_pos = []
    sur_phase_U_neg = []
    sur_phase_V_pos = []
    sur_phase_V_neg = []
    sur_phase_W_pos = []
    sur_phase_W_neg = []
    sur_StatorSheet = []
    sur_AirSlot = []
    sur_AirGapStator = []
    sur_RotorSheet = []
    sur_RotorSeg = []
    sur_RotorAir = []
    sur_AirGapRotor = []

    curve_outerLineLimit = []
    curve_statorSlave = []
    curve_statorMaster = []
    curve_statorMB = []
    curve_innerLineLimit = []
    curve_rotorSlave = []
    curve_rotorMaster = []
    curve_rotorMB1 = []
    curve_rotorMB2 = []
    curve_Contour = []

    for p in objStepPath:
        if "SurfaceAirSlot" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_middle, unit, p[0])
            sur_AirSlot.append(sur)
        elif "SurfaceAirGap" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_small, unit, p[0])
            if "Rotor" in p[0]:
                sur_AirGapRotor.append(sur)
            else:
                sur_AirGapStator.append(sur)
        elif "SurfaceRotorSheet" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_RotorSheet.append(sur)
        elif "SurfaceStatorSheet" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_StatorSheet.append(sur)
        elif "SurfaceSlot1" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_U_pos.append(sur)
        elif "SurfaceSlot2" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_U_neg.append(sur)
        elif "SurfaceSlot3" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_V_pos.append(sur)
        elif "SurfaceSlot4" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_V_neg.append(sur)
        elif "SurfaceSlot5" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_W_pos.append(sur)
        elif "SurfaceSlot6" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            sur_phase_W_neg.append(sur)
        elif "SurfaceSeg" in p[0]:
            sur = getSurfaceFromStep(p[1], mesh_big, unit, p[0])
            if "Air" in p[0]:
                sur_RotorAir.append(sur)
            else:
                sur_RotorSeg.append(sur)
        elif "OuterLineLimit" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_outerLineLimit = l
        elif "SlaveLineStator" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_statorSlave = l
        elif "MasterLineStator" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_statorMaster = l
        elif "MBStator" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_statorMB = l
        elif "InnerLineLimit" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_innerLineLimit = l
        elif "SlaveLineRotor" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_rotorSlave = l
        elif "MasterLineRotor" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_rotorMaster = l
        elif "MBRotor" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_rotorMB1 = l
            MB2 = emmo.CircleArc("", l[0].getP2(), l[0].getC(), l[0].getP1(), True)
            MB2.setName("Curve_" + str(MB2.getID()))
            curve_rotorMB2.append(MB2)
        elif "Contour" in p[0]:
            l = getCurveFromStep(p[1], mesh_big, unit)
            curve_Contour = l

    objectDict = {
        "sur_phase_U_pos": sur_phase_U_pos,
        "sur_phase_U_neg": sur_phase_U_neg,
        "sur_phase_V_pos": sur_phase_V_pos,
        "sur_phase_V_neg": sur_phase_V_neg,
        "sur_phase_W_pos": sur_phase_W_pos,
        "sur_phase_W_neg": sur_phase_W_neg,
        "sur_StatorSheet": sur_StatorSheet,
        "sur_AirSlot": sur_AirSlot,
        "sur_AirGapStator": sur_AirGapStator,
        "sur_RotorSheet": sur_RotorSheet,
        "sur_RotorSeg": sur_RotorSeg,
        "sur_RotorAir": sur_RotorAir,
        "sur_AirGapRotor": sur_AirGapRotor,
        "curve_outerLineLimit": curve_outerLineLimit,
        "curve_statorSlave": curve_statorSlave,
        "curve_statorMaster": curve_statorMaster,
        "curve_statorMB": curve_statorMB,
        "curve_innerLineLimit": curve_innerLineLimit,
        "curve_rotorSlave": curve_rotorSlave,
        "curve_rotorMaster": curve_rotorMaster,
        "curve_rotorMB1": curve_rotorMB1,
        "curve_rotorMB2": curve_rotorMB2,
        "curve_Contour": curve_Contour,
    }
    return objectDict
