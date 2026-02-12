#
# Copyright (c) 2018-2024 S. König, L. Reiniger, M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

###Noch nicht in die Doku. Funktioniert zunächst eingeschränkt für einzelne Linien wie beim Luis.
# def loadFromStep(self, stepFiles, unit, meshLength):
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.surface import Surface


def trimStepData(textLineFromFile):
    startId = "TRIMMED_CURVE"
    endId = "PRODUCT_RELATED_PRODUCT_CATEGORY"
    for i1 in range(len(textLineFromFile)):
        idFind = textLineFromFile[i1].find(startId)
        if idFind == -1:
            pass
        else:
            textLineFromFile = textLineFromFile[i1 : len(textLineFromFile)]
            break
    for i2 in range(len(textLineFromFile)):
        idFind2 = textLineFromFile[i2].find(endId)
        if idFind2 == -1:
            pass
        else:
            textLineFromFile = textLineFromFile[0:i2]
            break
    return textLineFromFile


def determineCurveType(textLineFromFile):
    idCurve = 0
    for code in textLineFromFile:
        if code.find("LINE") == -1 and code.find("CIRCLE") == -1:
            pass
        elif code.find("LINE") != -1:
            idCurve = "line"
            break
        elif code.find("CIRCLE") != -1:
            idCurve = "circleArc"
            break
    return idCurve


def getRawCoordinate(textLineFromFile, idCurve):
    if idCurve == "circleArc":
        # Mittelpunkt extrahieren
        rawCoordCentre = ""
        circleTag = "AXIS2_PLACEMENT_3D"
        for i1 in range(len(textLineFromFile)):
            idFind = textLineFromFile[i1].find(circleTag)
            if idFind == -1:
                pass
            else:
                textLineFromFile = textLineFromFile[i1 : len(textLineFromFile)]
                break

        centrePointTag = "CARTESIAN_POINT"
        for i1 in range(len(textLineFromFile)):
            idFind = textLineFromFile[i1].find(centrePointTag)
            if idFind == -1:
                pass
            else:
                rawCoordCentre = textLineFromFile[i1]
                break

        coordTag1 = "CARTESIAN_POINT('',("
        idFind = rawCoordCentre.find(coordTag1)
        if idFind == -1:
            pass
        else:
            rawCoordCentre = rawCoordCentre[
                idFind + len(coordTag1) : len(rawCoordCentre)
            ]

        coordTag2 = "));"
        idFind = rawCoordCentre.find(coordTag2)
        if idFind == -1:
            pass
        else:
            rawCoordCentre = rawCoordCentre[0:idFind]

    # Anfangs- und Endpunkte bestimmen
    rawCoordP1 = ""
    rawCoordP2 = ""
    lineTag = "DIRECTION('',"
    for i1 in range(len(textLineFromFile)):
        idFind = textLineFromFile[i1].find(lineTag)
        if idFind == -1:
            pass
        else:
            textLineFromFile = textLineFromFile[i1 : len(textLineFromFile)]
            break

    coordTag1 = "CARTESIAN_POINT('',("
    for i1 in range(len(textLineFromFile)):
        idFind = textLineFromFile[i1].find(coordTag1)
        if idFind == -1:
            pass
        else:
            rawCoordP1 = textLineFromFile[i1]
            idFind2 = rawCoordP1.find(coordTag1)
            rawCoordP1 = rawCoordP1[idFind2 + len(coordTag1) : len(rawCoordP1)]

            rawCoordP2 = textLineFromFile[i1 + 1]
            idFind3 = rawCoordP2.find(coordTag1)
            rawCoordP2 = rawCoordP2[idFind3 + len(coordTag1) : len(rawCoordP2)]
            break

    coordTag2 = "));"
    idFind = rawCoordP1.find(coordTag2)
    if idFind == -1:
        pass
    else:
        rawCoordP1 = rawCoordP1[0:idFind]

    idFind4 = rawCoordP2.find(coordTag2)
    if idFind4 == -1:
        pass
    else:
        rawCoordP2 = rawCoordP2[0:idFind4]

    if idCurve == "circleArc":
        return [rawCoordP1, rawCoordP2, rawCoordCentre]
    elif idCurve == "line":
        return [rawCoordP1, rawCoordP2]


def createCurve(rawCoord, typeCurve, meshLength, unit):
    if typeCurve == "circleArc":
        coord = rawCoordToFloatCoord(rawCoord[2])
        pC = Point(
            "", coord[0] * unit, coord[1] * unit, coord[2] * unit
        )  # , meshLength)
        pC.name = "point_"  # + str(pC.id)
    coord = rawCoordToFloatCoord(rawCoord[0])
    p1 = Point("", coord[0] * unit, coord[1] * unit, coord[2] * unit)  # , meshLength)
    p1.name = "point_"  # + str(p1.id)
    coord = rawCoordToFloatCoord(rawCoord[1])
    p2 = Point("", coord[0] * unit, coord[1] * unit, coord[2] * unit)  # , meshLength)
    p2.name = "point_"  # + str(p2.id)

    if typeCurve == "circleArc":
        curve1 = CircleArc("", p1, pC, p2)
        curve1.name = "curve_"  # + str(curve1.id)
    else:
        curve1 = Line("", p1, p2)
        curve1.name = "curve_"  # + str(curve1.id)
    return curve1


def rawCoordToFloatCoord(rawCoord):
    x = float(rawCoord[0 : rawCoord.find(",")])
    rawCoord = rawCoord[rawCoord.find(",") + 1 : len(rawCoord)]
    y = float(rawCoord[0 : rawCoord.find(",")])
    rawCoord = rawCoord[rawCoord.find(",") + 1 : len(rawCoord)]
    z = float(rawCoord)
    return [x, y, z]


def getSurfaceFromStep(allPathArea, meshLength, unit, name):
    allCurve = []
    for path in allPathArea:
        stepData = open(path)
        textLineFromFile = stepData.readlines()
        trimData = trimStepData(textLineFromFile)
        typeCurve = determineCurveType(trimData)
        rawCoord = getRawCoordinate(trimData, typeCurve)
        curve = createCurve(rawCoord, typeCurve, meshLength, unit)
        allCurve.append(curve)

    surface1 = Surface(name, allCurve)
    return surface1


def getCurveFromStep(allPathCurve, meshLength, unit):
    allCurve = []
    for path in allPathCurve:
        stepData = open(path)
        textLineFromFile = stepData.readlines()
        trimData = trimStepData(textLineFromFile)
        typeCurve = determineCurveType(trimData)
        rawCoord = getRawCoordinate(trimData, typeCurve)
        curve = createCurve(rawCoord, typeCurve, meshLength, unit)
        allCurve.append(curve)
    return allCurve
