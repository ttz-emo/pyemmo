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

resDir = r"C:\temp"
# resDir = r"C:\Users\ganser\Documents\PyDraft\Austausch Siemens\230321_DebugEisenverlusteReluktanz\Results\res__1PH8138_7xD0_Reluktanz_182Steps"
axLen = 0.31
lossParams = {"hyst": 165.9694, "eddy": 1.0529, "exc": 0.0}
symFactor = 4

# %%
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
print("---------------------------------------------------------------------")
print("Frequency domain results:\n")
print(f"{'Rotor':>23} {'Stator':>11} {'Sum':>9}")
print(
    f"{'Hysteresis:':<14} {np.sum(lossesFreq['rotor']['hyst']) : 8.3f} W {np.sum(lossesFreq['stator']['hyst']) : 9.3f} W {np.sum(lossesFreq['stator']['hyst']+lossesFreq['rotor']['hyst']) : 9.3f} W"
)
print(
    f"{'Eddy Current:':<14} {np.sum(lossesFreq['rotor']['eddy']) : 8.3f} W {np.sum(lossesFreq['stator']['eddy']) : 9.3f} W {np.sum(lossesFreq['stator']['eddy']+lossesFreq['rotor']['eddy']) : 9.3f} W"
)
print(
    f"{'Excess:':<14} {np.sum(lossesFreq['rotor']['exc']) : 8.3f} W {np.sum(lossesFreq['stator']['exc']) : 9.3f} W {np.sum(lossesFreq['stator']['exc']+lossesFreq['rotor']['exc']) : 9.3f} W"
)
print("\n---------------------------------------------------------------------")
print("Time domain results:\n")
print(
    f"{'Hysteresis:':<14} {np.mean(losses['rotor']['hyst']) : 8.3f} W {np.mean(losses['stator']['hyst']) : 9.3f} W {np.mean(losses['stator']['hyst']+losses['rotor']['hyst']) : 9.3f} W"
)
print(
    f"{'Eddy Current:':<14} {np.mean(losses['rotor']['eddy']) : 8.3f} W {np.mean(losses['stator']['eddy']) : 9.3f} W {np.mean(losses['stator']['eddy']+losses['rotor']['eddy']) : 9.3f} W"
)
print(
    f"{'Excess:':<14} {np.mean(losses['rotor']['exc']) : 8.3f} W {np.mean(losses['stator']['exc']) : 9.3f} W {np.mean(losses['stator']['exc']+losses['rotor']['exc']) : 9.3f} W"
)
