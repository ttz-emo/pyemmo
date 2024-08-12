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
