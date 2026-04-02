#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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

import os

import matplotlib.pyplot as plt
import numpy as np

# %%
# Imports
import pandas
import scipy.io as sio
from matplotlib import cm

# %% import ansys data
ansysResPath = r"H:\Workstation (Austausch)\EisenverlustberechnungVergleich\230223_EisenverlustkennfeldAnsys.csv"
ansysResults = pandas.read_csv(ansysResPath)
for key in ansysResults.keys():
    if "offset_deg" in key:
        phiDQ = ansysResults[key]  # angle for dq offset in deg
    elif "I [A]" in key:
        iAnsys = ansysResults[key]  # current amplitude (effective value) in A_eff
    elif "AvgCoreLoss" in key:
        coreLossAnsys = ansysResults[key]  # core loss results
    elif "AvgTorque" in key and not "AvgTorqueRipple" in key:
        torque = ansysResults[key]  # core loss results
nbrDesignPoints = len(phiDQ)
phi = np.deg2rad(phiDQ)
idq = np.array([iAnsys * -np.sin(phi), iAnsys * np.cos(phi)])

ansysResMat = os.path.join(
    os.path.dirname(ansysResPath),
    os.path.split(ansysResPath)[1].split(".")[0] + ".mat",
)
sio.savemat(
    ansysResMat,
    {
        "coreLossAnsys": coreLossAnsys.tolist(),
        "torqueAnsys": torque.tolist(),
        "phiDQ_Ansys": phiDQ.to_list(),
        "iAmpAnsys": iAnsys.to_list(),
    },
)
# %%
# Load onelab results
RES_DIR = (
    r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"
)
coreLossOnelab = np.load(os.path.join(RES_DIR, "ironLossData.npy"))
# coreLossOnelabMatFile = os.path.join(RES_DIR, "230301_ironLossDataOnelab.mat")
# sio.savemat(
#     coreLossOnelabMatFile,
#     {
#         "coreLossOnelab": coreLossOnelab.tolist(),
#         # "phiDQ_Onelab": phiDQ.to_list(),
#         # "iAmpOnelab": iAnsys.to_list(),
#     },
# )
# %%
# plot results
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=100)
phiMesh, iMesh = np.meshgrid(np.rad2deg(phi), iAnsys)
ax.scatter(np.rad2deg(phi), iAnsys, coreLossAnsys, color=cm.jet(0))
ax.scatter(np.rad2deg(phi), iAnsys, coreLossOnelab, color=cm.jet(100))
plt.show()

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=100)
# phiMesh, iMesh = np.meshgrid(np.rad2deg(phi), iAnsys)
# ax.scatter(
#     np.rad2deg(phi), iAnsys, (coreLossOnelab - coreLossAnsys) / coreLossAnsys * 100
# )
# plt.show()
