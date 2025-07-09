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

import math

from setPath import pathRes

import pyemmo as emmo

myScript = emmo.Script("pmsm", pathRes)

#       Rotorparameter (ausgedacht!)
PBohrung = emmo.Point("mittelPunktBohrung", 0, 0, 0, 5e-3)
modellR = 8
modellS = 12

# Material aus Datenbank laden
steel1010 = emmo.Material()
steel1010.loadMatFromDataBase("Material.db", "steel1010")
ndFe35 = emmo.Material()
ndFe35.loadMatFromDataBase("Material.db", "ndFe35")
air = emmo.Material()
air.loadMatFromDataBase("Material.db", "air")
copper = emmo.Material()
copper.loadMatFromDataBase("Material.db", "copper")

motorPMSM_struct = {
    "name": "PMSM_Model1",
    "maschinenMittelpunkt": PBohrung,
    "RotorBlech": {
        "geometrie": "RotorBlechschnitt1",
        "r_We": 20e-3,
        "r_R": 50e-3,
        "mesh": 5e-3,
        "BlechTeilmodell": 1 / (modellR * 2),
        "material": steel1010,
    },
    "Magnet": {
        "geometrie": "Magnet_Schale1",
        "h_M": 5e-3,
        "b_M_i": 25e-3,
        "b_M_a": 25e-3,
        "Gesamtpolzahl": modellR,
        "Pole im Modell": int(0.25 * modellR),
        "material": ndFe35,
        "mesh": 4e-3,
        "magnetisierung": [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
    },
    "Bohrung": None,
    "Kaefig": None,
    "Luftspalt": {"material": air, "mesh": 1e-3},
    "StatorBlech": {
        "geometrie": "StatorBlechschnitt1",
        "r_i": 57e-3,
        "r_a": 100e-3,
        "BlechTeilmodell": 1 / (modellS * 2),
        "material": steel1010,
        "mesh": 5e-3,
    },
    "StatorNut": {
        "geometrie": "NutEinzelZahn",
        "h_n": 20e-3,
        "h_zk": 7e-3,
        "h_ngs": 7e-3,
        "b_nng": 25e-3,
        "b_nzk": 15e-3,
        "Gesamtnuten": modellS,
        "Statornuten im Modell": int(0.25 * modellS),
        "material": copper,
        "mesh": 2e-3,
    },
    "StatorNutschlitz": {
        "b_s": 5e-3,
        "h_s": 3e-3,
        "material": air,
        "mesh": 1e-3,
    },
    "WicklungStator": {
        "phasen": 3,
        "stromAmplitute": 10,
        "windungszahl": 60,  # Wicklung in einer Nut!-> nicht halber Nut
        "Wicklungschema": [
            {"PhasenName": "U", "richtung": "+", "Phasenwinkel": 0},
            {"PhasenName": "U", "richtung": "-", "Phasenwinkel": 0},
            {
                "PhasenName": "W",
                "richtung": "+",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "W",
                "richtung": "-",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "+",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "-",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {"PhasenName": "U", "richtung": "+", "Phasenwinkel": 0},
            {"PhasenName": "U", "richtung": "-", "Phasenwinkel": 0},
            {
                "PhasenName": "W",
                "richtung": "+",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "W",
                "richtung": "-",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "+",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "-",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {"PhasenName": "U", "richtung": "+", "Phasenwinkel": 0},
            {"PhasenName": "U", "richtung": "-", "Phasenwinkel": 0},
            {
                "PhasenName": "W",
                "richtung": "+",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "W",
                "richtung": "-",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "+",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "-",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {"PhasenName": "U", "richtung": "+", "Phasenwinkel": 0},
            {"PhasenName": "U", "richtung": "-", "Phasenwinkel": 0},
            {
                "PhasenName": "W",
                "richtung": "+",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "W",
                "richtung": "-",
                "Phasenwinkel": 4 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "+",
                "Phasenwinkel": 2 * math.pi / 3,
            },
            {
                "PhasenName": "V",
                "richtung": "-",
                "Phasenwinkel": 2 * math.pi / 3,
            },
        ],
    },
    "Simulationsparameter": {
        "freq": 67,
        "wr": 67 * math.pi * 2,
        "timeMax": 1 / (67 * 2),  # Winkel/wr
        "timeStep": 1 / (180 * 67 * 2),
        "analysisType": "timedomain",  #'timedomain', #'static'
        "resultDir": "res",
    },
    "Feld": {"b": True, "az": True, "js": True},
}

pmsm = emmo.Machine(motorPMSM_struct)
pmsm.addToScript(myScript)

myScript.generateScript()

print("I am done!")
