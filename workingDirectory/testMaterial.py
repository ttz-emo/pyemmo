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
import numpy as np
from matplotlib import pyplot as plt
from pyemmo.script.material.material import Material
from copy import copy, deepcopy

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.material.electricalSteel import ElectricalSteel

air = Material(
    name="Air",
    conductivity=None,
    relPermeability=1,
    remanence=None,
    density=1.225,
    thermalConductivity=0.0262,
    thermalCapacity=1.005,
    BH=None,
)
air.print()


b = [
    0.0,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0,
    1.1,
    1.15,
    1.2,
    1.25,
    1.3,
    1.35,
    1.4,
    1.45,
    1.5,
    1.55,
    1.6,
    1.65,
    1.7,
    1.75,
    1.8,
    1.85,
    1.9,
    2.0,
    2.1,
    2.2,
    2.3,
]
h = [
    0.0,
    70.0,
    95.0,
    120.0,
    140.0,
    160.0,
    180.0,
    220.0,
    250.0,
    280.0,
    330.0,
    360.0,
    400.0,
    450.0,
    530.0,
    640.0,
    760.0,
    930.0,
    1220.0,
    2100.0,
    3200.0,
    4400.0,
    5700.0,
    7400.0,
    9500.0,
    12000.0,
    15000.0,
    23840.0,
    37100.0,
    63625.0,
    143202.0,
]
bh = np.array([b, h])
steel = ElectricalSteel(
    name="steel_1010",
    conductivity=5e6,
    relPermeability=None,
    BH=bh.transpose(),
    sheetThickness=0.5e-3,
    lossParams=None,
    referenceFrequency=0,
    referenceFluxDensity=0,
)

plt.plot(h, b, ".-")

# %%
# Check comparison
air_copy = deepcopy(air)
assert air_copy == air  # make sure test is ok.
# make fail test
air_copy.relPermeability = 10
try:
    assert air_copy == air  # this should fail now.
    raise RuntimeError("Error: This Assertion should fail!")
except AssertionError:
    print("Assertion failed as expected.")
except Exception as exce:
    raise exce

# %%
# Check comparison steel
steel_copy = deepcopy(steel)
assert steel_copy == steel  # make sure test is ok.
# make fail test
steel_copy.BH[1, 1] = 80  # vorher 70
try:
    assert steel_copy == steel  # this should fail now.
    raise RuntimeError("Error: This Assertion should fail!")
except AssertionError:
    print("Assertion failed as expected.")
except Exception as exce:
    raise exce
