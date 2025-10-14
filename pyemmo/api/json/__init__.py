#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
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
"""init module of json api"""

from __future__ import annotations

from ...script.geometry import defaultCenterPoint

# TODO: Clean up unused definitions here!

globalCenterPoint = defaultCenterPoint
# Movingband line Identification dicts
RotorMBLineDict = {
    "LuR2": [
        ["MB_CurveRotor"],
        ["LuA2", "LuM2"],
        ["LuAa", "LuBa"],
    ],  # double airgap
    "RoLu2": ["LuA2", "LuM2"],  # double airgap
    "RoLu": ["LuA", "LuM"],  # single airgap
    "LuR": ["LuAa", "LuBa"],  # single airgap
}
StatorMBLineDict = {
    "StLu2": [["MB_CurveStator"], ["LuA2", "LuM2"]],
    "StLu": ["LuA", "LuM"],
}

# Outer limit lines
OuterLimitLineDict = {
    "Geh": [  # first case: no inner shaft radius; second case: with radius
        ["OuterLimit"],
        ["G1", "G3"],  # first case: zylindrical housing
        [
            [
                "G1",
                "G2a",
            ],  # second case: quadratic or "kreuzprofil" with rounding
            ["G2a", "G2e"],
            ["G2e", "G3"],
            ["G2", "G1"],  # without rounding
            ["G2", "G3"],
        ],
    ],
    # if there is no housing, use stator iron outer line
    "StNut": [
        ["OuterLimit"],
        ["InnerLimit"],
        ["SZ", "SN"],
    ],
}

# Inner limit lines
InnerLimitLineDict = {
    "Wel": [
        ["InnerLimit"],
        # ["W2", "MP"], # first case: no inner shaft radius -> no limit line!
        ["W4", "W3"],  # second case: with radius -> inner limit line
    ],
    "Hul": ["H3", "H4"],
    "Pol": [
        ["InnerLimit"],
        ["OuterLimit"],
        ["RMi", "RI"],  # first case:IPM
        ["RndI", "RndM"],  # second case:APM
    ],
    "RoNut": ["SZ", "SN"],
}

# Predefine IdExt of special surface api objects for identification
ROTOR_MAG_IDEXT = "magnet"
ROTOR_BAR_IDEXT = "rotor bar"
ROTOR_LAM_IDEXT = "rotor lamination"
ROTOR_AIRGAP_IDEXT = "rotor airgap"
STATOR_SLOT_IDEXT = "stator slot"
STATOR_LAM_IDEXT = "stator lamination"
STATOR_AIRGAP_IDEXT = "stator airgap"

# order defines user defined mesh setting order.
apiNameDict = {
    # rotor
    "shaft": "Shaft",
    "hole": "Holes",
    ROTOR_MAG_IDEXT: "Magnet",
    ROTOR_BAR_IDEXT: "Rotor Slot",
    ROTOR_LAM_IDEXT: "Rotor Lamination",
    ROTOR_AIRGAP_IDEXT: "Rotor Airgap",  # case 3 airgap segments
    "rotor air": "Rotor Air",
    # stator
    "housing": "Housing",
    STATOR_SLOT_IDEXT: "Stator Slot",
    STATOR_LAM_IDEXT: "Stator Lamination",
    STATOR_AIRGAP_IDEXT: "Stator Airgap",  # case 3 airgap segments
    "stator air": "Stator Air",  # case 5 airgap segments
}
