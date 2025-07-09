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
"""Module to test the core loss calculation functions"""

from __future__ import annotations

# %% imports
# import gmsh
import os
import time as clockTime

import numpy as np
from matplotlib import pyplot as plt

from pyemmo.definitions import TEST_DIR

# from pyemmo.definitions import ROOT_DIR
from pyemmo.functions import calcIronLoss, import_results

# import tkinter as tk
# from tkinter import filedialog


TIME_DOMAIN = True
FREQ_DOMAIN = False
loss_factors = {"hyst": 172.04, "eddy": 1.047, "exc": 0.0}
# resDir = r"C:\TEMP\res_Id=0_Iq=0_1000rpm"
RES_DIR = os.path.join(TEST_DIR, "data", "core_loss")
AX_LEN = 0.05
SYM = 4

# resDir = r"C:\Users\ganser\Documents\PyEMMO\Austausch Siemens\230321_DebugEis
# enverlusteReluktanz\Results\res__1PH8138_7xD0_Reluktanz_182Steps"
# lossParams = {"hyst": 165.9694, "eddy": 1.0529, "exc": 0.0}
# axLen = 0.31
# symFactor = 4

# %%
if FREQ_DOMAIN:
    lossesFreq = {}
    for side in ("rotor", "stator"):
        print(f"run freq. domain iron loss calculation for {side}")
        tstart = clockTime.time()
        lossesFreq[side], freqs = calcIronLoss.calc_freq_domain_core_loss(
            os.path.join(RES_DIR, f"b_{side}.pos"), loss_factors, SYM, AX_LEN
        )
        print(
            f"Freq. domain iron loss calculation for {side} took "
            + clockTime.strftime(
                "%H:%M:%S", clockTime.gmtime(clockTime.time() - tstart)
            )
        )


# print(
#     f"Hysteresis: {np.sum(lossesFreq['stator']['hyst']+lossesFreq['rotor']['hyst']) : .3f} W"
# )
# print(
#     f"Eddy Current: {np.sum(lossesFreq['stator']['eddy']+lossesFreq['rotor']['eddy']) : .3f} W"
# )
# print(
#     f"Excess: {np.sum(lossesFreq['stator']['exc']+lossesFreq['rotor']['exc']) : .3f} W"
# )
# %%
if TIME_DOMAIN:
    # run time domain iron loss calculation
    losses = {}
    for side in ["rotor", "stator"]:
        print(f"run time domain iron loss calculation for {side}")
        tstart = clockTime.time()
        losses[side], time = calcIronLoss.calc_time_domain_core_loss(
            os.path.join(RES_DIR, f"b_{side}.pos"), loss_factors, SYM, AX_LEN
        )
        print(
            f"Time domain iron loss calculation for {side} took "
            + clockTime.strftime(
                "%H:%M:%S", clockTime.gmtime(clockTime.time() - tstart)
            )
        )

# print(f"Hysteresis: {np.mean(losses['hyst']) : .3f} W")
# print(f"Eddy Current: {np.mean(losses['eddy']) : .3f} W")
# print(f"Excess: {np.mean(losses['exc']) : .3f} W")

# %%
# Print results
# pylint: disable=locally-disabled, line-too-long
if FREQ_DOMAIN:
    print("---------------------------------------------------------------------")
    print("Frequency domain results:")
    print(f"{'Rotor':>24} {'Stator':>11} {'Sum':>9}")
    print(
        f"{'Hysteresis:':<14} {np.sum(lossesFreq['rotor']['hyst']) : 8.3f} W {np.sum(lossesFreq['stator']['hyst']) : 9.3f} W {np.sum(lossesFreq['stator']['hyst']+lossesFreq['rotor']['hyst']) : 9.3f} W"
    )
    print(
        f"{'Eddy Current:':<14} {np.sum(lossesFreq['rotor']['eddy']) : 8.3f} W {np.sum(lossesFreq['stator']['eddy']) : 9.3f} W {np.sum(lossesFreq['stator']['eddy']+lossesFreq['rotor']['eddy']) : 9.3f} W"
    )
    print(
        f"{'Excess:':<14} {np.sum(lossesFreq['rotor']['exc']) : 8.3f} W {np.sum(lossesFreq['stator']['exc']) : 9.3f} W {np.sum(lossesFreq['stator']['exc']+lossesFreq['rotor']['exc']) : 9.3f} W"
    )
    print("---------------------------------------------------------------------")
if TIME_DOMAIN:
    print("Time domain results:")
    print(
        f"{'Hysteresis:':<14} {np.mean(losses['rotor']['hyst']) : 8.3f} W {np.mean(losses['stator']['hyst']) : 9.3f} W {np.mean(losses['stator']['hyst']+losses['rotor']['hyst']) : 9.3f} W"
    )
    print(
        f"{'Eddy Current:':<14} {np.mean(losses['rotor']['eddy']) : 8.3f} W {np.mean(losses['stator']['eddy']) : 9.3f} W {np.mean(losses['stator']['eddy']+losses['rotor']['eddy']) : 9.3f} W"
    )
    print(
        f"{'Excess:':<14} {np.mean(losses['rotor']['exc']) : 8.3f} W {np.mean(losses['stator']['exc']) : 9.3f} W {np.mean(losses['stator']['exc']+losses['rotor']['exc']) : 9.3f} W"
    )
    print("---------------------------------------------------------------------")

# %%
lossGetdpFile = os.path.join(RES_DIR, "Pec_Lam.dat")
if os.path.isfile(lossGetdpFile):
    time, eddyLossOnelab = import_results.read_timetable_dat(lossGetdpFile)
    print(
        "\nOnelab eddy current loss results:\n"
        f"{'Eddy Current:':<14} {np.mean(eddyLossOnelab) : 8.3f} W"
    )
else:
    eddyLossOnelab = None

# %%
# Do some plots...
if FREQ_DOMAIN:
    fig, ax = plt.subplots()
    WIDTH = 0.3
    orders = freqs / freqs[1]
    ax.bar(orders, lossesFreq["stator"]["eddy"], WIDTH, label="eddy current")
    ax.bar(orders + WIDTH, lossesFreq["stator"]["hyst"], WIDTH, label="hysteresis")
    plt.xticks(orders + WIDTH / 2, orders.astype(int))
    ax.set_xlim((0, 16))
    ax.set_xlabel("elec Order")
    ax.set_ylabel("Stator iron losses in W")
    ax.legend()

# %% plot eddy current losses
if TIME_DOMAIN:
    fig, ax = plt.subplots()
    # fig.suptitle("")
    ax.plot(
        time,
        losses["rotor"]["eddy"] + losses["stator"]["eddy"],
        label="time domain",
    )
    PvEddySum = np.sum(losses["rotor"]["eddy"] + losses["stator"]["eddy"])
    # ax.plot(
    #     [time[0], time[-1]],
    #     [PvEddySum, PvEddySum],
    #     label="freq. domain",
    # )
    if eddyLossOnelab:
        ax.plot(time[1:], eddyLossOnelab[1:], label="GetDP (direct)")
        ax.set_xlabel("time in s")
        ax.set_ylabel("Eddy current losses in W")
        ax.legend()
# %%
