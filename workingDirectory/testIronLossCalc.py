# %% imports
import gmsh
import sys, os
import numpy as np
import time as clockTime
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions import calcIronLoss

resDir = r"C:\temp"
axLen = 0.31
lossParams = {"hyst": 165.9694, "eddy": 1.0529, "exc": 0.0}
symFactor = 4

# %%
# run main
losses, time = calcIronLoss.main(
    os.path.join(resDir, "b_stator.pos"), lossParams, symFactor, axLen
)

#%% 
print(f"Hysteresis: {losses['hyst'][0] : .3f} W")
print(f"Eddy Current: {np.mean(losses['eddy']) : .3f} W")
print(f"Excess: {np.mean(losses['exc']) : .3f} W")