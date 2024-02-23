# %% imports
import gmsh
import sys, os
import numpy as np
import time as clockTime
from matplotlib import pyplot as plt

# import tkinter as tk
# from tkinter import filedialog

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions import calcIronLoss
from pyemmo.functions import importResults

timedomain = True
freqdomain = False
lossParams = {"hyst": 172.04, "eddy": 1.047, "exc": 0.0}
# resDir = r"C:\TEMP\res_Id=0_Iq=0_1000rpm"
resDir = r"C:\temp"
axLen = 0.05
symFactor = 4

# resDir = r"C:\Users\ganser\Documents\PyEMMO\Austausch Siemens\230321_DebugEisenverlusteReluktanz\Results\res__1PH8138_7xD0_Reluktanz_182Steps"
# lossParams = {"hyst": 165.9694, "eddy": 1.0529, "exc": 0.0}
# axLen = 0.31
# symFactor = 4

# %%
if freqdomain:
    lossesFreq = {}
    for side in ("rotor", "stator"):
        print(f"run freq. domain iron loss calculation for {side}")
        tstart = clockTime.time()
        lossesFreq[side], freqs = calcIronLoss.calcFreqDomainIronLosses(
            os.path.join(resDir, f"b_{side}.pos"), lossParams, symFactor, axLen
        )
        print(
            f"Freq. domain iron loss calculation for {side} took "
            + clockTime.strftime("%H:%M:%S", clockTime.gmtime(clockTime.time() - tstart))
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
if timedomain:
    # run time domain iron loss calculation
    losses = {}
    for side in ("rotor", "stator"):
        print(f"run time domain iron loss calculation for {side}")
        tstart = clockTime.time()
        losses[side], time = calcIronLoss.calcTimeDomainIronLosses(
            os.path.join(resDir, f"b_{side}.pos"), lossParams, symFactor, axLen
        )
        print(
            f"Time domain iron loss calculation for {side} took "
            + clockTime.strftime("%H:%M:%S", clockTime.gmtime(clockTime.time() - tstart))
        )

# print(f"Hysteresis: {np.mean(losses['hyst']) : .3f} W")
# print(f"Eddy Current: {np.mean(losses['eddy']) : .3f} W")
# print(f"Excess: {np.mean(losses['exc']) : .3f} W")

# %%
# Print results
if freqdomain:
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
if timedomain:
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
lossGetdpFile = os.path.join(resDir, "Pec_Lam.dat")
if os.path.isfile(lossGetdpFile):
    time, eddyLossOnelab = importResults.read_timetable_dat(lossGetdpFile)
    print(
        "\nOnelab eddy current loss results:\n"
        f"{'Eddy Current:':<14} {np.mean(eddyLossOnelab) : 8.3f} W"
    )

# %%
# Do some plots...
if freqdomain:
    fig, ax = plt.subplots()
    width = 0.3
    orders = (freqs / freqs[1])
    ax.bar(orders, lossesFreq["stator"]["eddy"], width, label="eddy current")
    ax.bar(orders + width, lossesFreq["stator"]["hyst"], width, label="hysteresis")
    plt.xticks(orders+width / 2, orders.astype(int))
    ax.set_xlim((0, 16))
    ax.set_xlabel("elec Order")
    ax.set_ylabel("Stator iron losses in W")
    ax.legend()

#%% plot eddy current losses
if timedomain:
    fig, ax = plt.subplots()
    # fig.suptitle("")
    ax.plot(time[:-1], losses["rotor"]["eddy"]+losses["stator"]["eddy"], label="time domain")
    PvEddyFreqSum = np.sum(lossesFreq['rotor']['eddy']+lossesFreq['stator']['eddy'])
    ax.plot([time[0],time[-1]], [PvEddyFreqSum,PvEddyFreqSum], label="freq. domain")
    ax.plot(time[1:], eddyLossOnelab[1:], label="GetDP (direct)")
    ax.set_xlabel("time in s")
    ax.set_ylabel("Eddy current losses in W")
    ax.legend()
# %%
