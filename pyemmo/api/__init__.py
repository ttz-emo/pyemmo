"""init module of json api"""
import logging
from ..script.material.material import Material
from ..script.geometry import defaultCenterPoint
from .. import logFmt, rootLogger

logger = rootLogger # test to get script.py log in local model log file
# logger = logging.getLogger("pydraft.api.json")  # init module logger
ch = logging.StreamHandler()
ch.setFormatter(logFmt)
logger.addHandler(ch)

try:
    air = Material()
    air.loadMatFromDataBase("Material_new.db", "air")
    air.setName("Air")
    air.setDensity(1.2041)
except FileNotFoundError:
    air = Material(
        name="Air",
        conductivity=None,
        relPermeability=1,
        remanence=None,
        density=1.204,
        thermalConductivity=0.0261,
        thermalCapacity=1.005,
    )

globalCenterPoint = defaultCenterPoint
# Movingband line Identification dicts
RotorMBLineDict = {
    "LuR2": [["LuA2", "LuM2"], ["LuAa", "LuBa"]],
    "RoLu2": ["LuA2", "LuM2"],
    "LuR": ["LuAa", "LuBa"],
}
StatorMBLineDict = {
    "StLu2": ["LuA2", "LuM2"],
    "StLu": ["LuA", "LuM"],
}

# Outer limit lines
OuterLimitLineDict = {
    "Geh": [  # first case: no inner shaft radius; second case: with radius
        ["G1", "G3"],  # first case: zylindrical housing
        [
            ["G1", "G2a"],  # second case: quadratic or "kreuzprofil" with rounding
            ["G2a", "G2e"],
            ["G2e", "G3"],
            ["G2", "G1"],  # without rounding
            ["G2", "G3"],
        ],
    ],
    "StNut": ["SZ", "SN"],  # if there is no housing, use stator iron outer line
}

# Inner limit lines
InnerLimitLineDict = {
    "Wel": [
        # ["W2", "MP"], # first case: no inner shaft radius -> no limit line!
        ["W4", "W3"],  # second case: with radius -> inner limit line
    ],
    "Hul": ["H3", "H4"],
    "Pol": [["RMi", "RI"], ["RndI", "RndM"]],  # first case:IPM; second case:APM
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
