# %%

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog

import numpy as np

from pyemmo.functions import import_results, transform_coords

root = tk.Tk()
root.withdraw()
res_file = ""
if not res_file:
    res_file = filedialog.askopenfilename(
        defaultextension=".pos", filetypes=[("POS files", "*.pos")]
    )


quantity, time, position, data = import_results.importSP(res_file)

position = np.array(position)
data = np.array(data)
r, phi = transform_coords.cart2pol(position[:, 0], position[:, 1])

from matplotlib import pyplot as plt

fig, ax = plt.subplots()
ax.plot(np.rad2deg(phi), data)
ax.grid()
ax.set_ylabel("B_{rad} in T")
ax.set_xlabel("Angle in °")

sym = 12
nbr_segments = (position.shape[0]) * sym

print(f"Number of segments from results: {nbr_segments}")
