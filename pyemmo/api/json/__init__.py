"""init module of json api"""
import logging
from ...script.material.material import Material
from ...script.geometry import defaultCenterPoint


globalCenterPoint = defaultCenterPoint
# Movingband line Identification dicts
RotorMBLineDict = {
    "LuR2": [["MB_CurveRotor"], ["LuA2", "LuM2"], ["LuAa", "LuBa"]], # double airgap
    "RoLu2": ["LuA2", "LuM2"], # double airgap
    "RoLu": ["LuA", "LuM"], # single airgap
    "LuR": ["LuAa", "LuBa"], # single airgap
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
            ["G1", "G2a"],  # second case: quadratic or "kreuzprofil" with rounding
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

# order defines user defined mesh setting order.
apiNameDict = {
    # rotor
    "Wel": "Welle",
    "Hul": "Huelse",
    "Lpl": "Loch (Polluecke)",
    "Mag": "Magnet",
    "RoCu": "Rotor-Nut",
    "RoNuS": "Rotor-Nutschlitz",
    "RoNuL": "Rotor-Nutschlitzluft",
    "Pol": "Rotorblech",
    "RoNut": "Rotorblech",
    "LuR": "Rotorluftspalt",  # case 3 airgap segments
    "LuR1": "Rotorluftspalt 1",
    "RoLu1": "Rotorluftspalt 1",
    "LuR2": "Rotorluftspalt 2",
    "RoLu2": "Rotorluftspalt 2",
    # stator
    "Geh": "Gehaeuse",
    "StCu": "Stator-Nut",
    "StNuS": "Stator-Nutschlitz",
    "StNuL": "Stator-Nutschlitzluft",
    "StNut": "Statorblech",
    "StLu": "Statorluftspalt",  # case 3 airgap segments
    "StLu1": "Statorluftspalt 1",  # case 5 airgap segments
    "StLu2": "Statorluftspalt 2",
}
