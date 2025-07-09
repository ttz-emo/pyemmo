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

# %%
from os import path

import gmsh
import numpy as np
from matplotlib import pyplot as plt
from numpy.linalg import norm

from pyemmo.functions.import_results import importPos

POS_FILE_PATH = r"C:\Users\ganser\AppData\Local\Programs\pyemmo\workingDirectory\testPosImport\brad.pos"
# filepathRotor = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\workingDirectory\testPosImport\res\brad.pos"
filepath = [POS_FILE_PATH]
# with open(filepath) as posFile:
#     header = posFile.readline()
#     for line in posFile.readline():
# rawData = posFile.read()

# %% New method
angles = []
values = []
gmsh.initialize()
for sim, path in enumerate(filepath):
    gmsh.merge(path)
    tags = gmsh.view.get_tags()
    dataType, numElem, data = gmsh.view.getListData(tags[-1])
    print(dataType)
    print(numElem)
    radius = norm(data[0][0:3])
    print(f"Radius is {radius*1e3}mm.")
    angles.append(np.empty((numElem[0], 1)))
    values.append(np.empty((numElem[0], 1)))
    # FIXME: reshaping into 4 components fails for multiple time steps
    for i, (x, y, z, value) in enumerate(data[0].reshape(numElem[0], 4)):
        angles[sim][i] = np.rad2deg(math.acos(x / radius))
        values[sim][i] = value
gmsh.finalize()
# %%

fig, ax = plt.subplots()
for i, angle in enumerate(angles):
    ax.plot(angle, values[i])

# mean_values = empty((numElem[0],1))
# for i in range(0,numElem[0]):
#     mean_values[i] = mean([values[0][i],values[1][i]])
# ax.plot(angle, mean_values)

ax.set(xlabel="Angle in °", ylabel="Airgap flux density in T")
plt.legend(["stator side", "rotor side", "mean"])
plt.show()
# %%
# Try with new importPos function
DATA_FILE_PATH = POS_FILE_PATH
try:
    time, data = importPos(DATA_FILE_PATH)
except OSError:
    print("Failed for file ", DATA_FILE_PATH)

DATA_FILE_PATH = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\workingDirectory\testPosImport\bradMultiTimeSteps.pos"
try:
    time, data = importPos(DATA_FILE_PATH)
except OSError:
    print("Failed for file ", DATA_FILE_PATH)
else:
    fig, ax = plt.subplots()
    ax.plot(time, np.mean(norm(data, axis=2), axis=1))
    fig.show()
# %%
