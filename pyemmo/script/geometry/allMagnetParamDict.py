"""MagnetParameter Beschreibung"""
import math
from ..material.material import Material

ndFe35 = Material()
ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")
# Type magnet01_Surface
mag_Type01 = {
    "h_M": 7e-3,
    "angularWidth_i": math.pi / 10,
    "angularWidth_a": math.pi / 12,
    "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
    "magnetisationType": "radial",
    "material": ndFe35,
    "meshLength": 3e-3,
}

# Type magnet02_Surface
mag_Type02 = {
    "h_Mag": 7.5e-3,
    "w_Mag": 15e-3,
    "r_Mag": 18e-3,
    "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
    "magnetisationType": "radial",
    "material": ndFe35,
    "meshLength": 3e-3,
}

# Type magnet03_Surface
mag_Type03 = {
    "h_Mag": 7.5e-3,
    "w_Mag": 12e-3,
    "magnetisationDirection": [1, -1, 1, -1, 1, -1, 1, -1],
    "magnetisationType": "radial",
    "material": ndFe35,
    "meshLength": 3e-3,
}
