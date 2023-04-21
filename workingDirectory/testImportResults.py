#%%
from cmath import atan
from genericpath import isfile
from sys import path
from os.path import abspath, join, dirname
from matplotlib.pyplot import plot, show
from matplotlib import pyplot as plt

try:
    rootDir = abspath(join(dirname(__file__), ".."))
except:
    rootDir = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootDir}'")
print(f'rootname is "{rootDir}"')
path.append(rootDir)

from pyemmo.functions.importResults import (
    plotTimeTableDat,
    readTimeTableDat,
    splitData,
    plotAllDat,
    importSP,
)

#%% time table formated file:
resDir = join(rootDir, "Results", "Test_API_JSON", "model files", "res_TestAPI_JSON")
# TORQUE
datFileTorque = join(resDir, "Ts.dat")
# import raw data
time, torque = readTimeTableDat(filePath=datFileTorque)
# split up data if needed
nbrSims, timeArray, torqueArray = splitData(time, torque)
# plot the torque data
plotTimeTableDat(
    filePath=datFileTorque,
    dataLabel="Torque in Nm",
    title="Torque of TestMachineAPI",
    savefig=True,
    showfig=True,
    savePath=None,
)
# time, torque = readTimeTableDat()
# # SPLIT SIM-DATA
# nbrSims, timeArray, torqueArray = splitData(time, torque)
# # PLOT TORQUE
# for sim in range(nbrSims):
#     fig, ax = plt.subplots()
#     fig.set_dpi(300)
#     ax.plot(timeArray[sim], torqueArray[sim])
#     # show()
#     # ax.set_aspect("equal", adjustable="box")
#     fig.axes[0].set_ylim(
#         bottom=min(torqueArray[sim]) * (1.1 if min(torqueArray[sim]) < 0 else 0.9),
#         top=max(torqueArray[sim]) * 1.1,
#     )
#     # ax.autoscale()
#%% RegionValue formated file (VirtualWork results):
# TORQUE
datFileTorqueVW = join(resDir, "Tr_vw.dat")
# import raw data
time, torque = readTimeTableDat(filePath=datFileTorque)
# split up data if needed
nbrSims, timeArray, torqueArray = splitData(time, torque)
# plot the torque data
plotTimeTableDat(
    filePath=datFileTorqueVW,
    dataLabel="Torque in Nm",
    title="Torque of TestMachineAPI (Virtual Work)",
    savefig=True,
    showfig=True,
    savePath=None,
)
#%% PLOT INDUCED VOLTAGE
time = dict()
indVoltage = dict()
fig, ax = plt.subplots()
fig.set_dpi(300)
for phase in "ABC":
    time[phase], indVoltage[phase] = readTimeTableDat(
        join(resDir, "InducedVoltage" + phase + ".dat")
    )
    # ax.plot(time[phase], indVoltage[phase])
# show()

#%% Import Radial Flux Density in Airgap
time = dict()
pos = dict()
angle = dict()
Brad = dict()

for machineSide in ["stator", "rotor"]:
    posFile = join(resDir, f"b_radial_airgap_{machineSide}.pos")
    if isfile(posFile):
        name, time[machineSide], pos[machineSide], Brad[machineSide] = importSP(posFile)
        angle[machineSide] = list()
        for pNbr in range(len(pos[machineSide])):
            px = pos[machineSide][pNbr][0]
            py = pos[machineSide][pNbr][1]
            angle[machineSide].append(atan(px / py))
fig, ax = plt.subplots()
fig.set_dpi(300)
ax.plot(angle["rotor"], Brad["rotor"])
show()

# %%
