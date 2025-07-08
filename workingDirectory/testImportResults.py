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

from cmath import atan
from genericpath import isfile

# %%
from os.path import join

from matplotlib import pyplot as plt

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions import import_results as resimport
from pyemmo.functions.import_results import (
    importSP,
    plot_timetable_dat,
    read_timetable_dat,
    split_data,
)

# %% single simulation in time table formated file:
resDir = join(ROOT_DIR, "workingDirectory", "testPosImport")
# TORQUE
datFileTorque = join(resDir, "TsSingleTimeTable.dat")
# import raw data
time, torque = read_timetable_dat(file_path=datFileTorque)
# split up data if needed
nbrSims, timeArray, torqueArray = split_data(time, torque)
# plot the torque data
plot_timetable_dat(
    file_path=datFileTorque,
    dataLabel="Torque in Nm",
    title="Torque of TestMachineAPI",
    savefig=True,
    showfig=True,
    savePath=None,
)

# %% two (multiple) simulations in time table formated file:
resDir = join(ROOT_DIR, "workingDirectory", "testPosImport")
# TORQUE
datFileTorque = join(resDir, "TsMultiTimeTable.dat")
# import raw data
time, torque = read_timetable_dat(file_path=datFileTorque)
# split up data if needed
nbrSims, timeArray, torqueArray = split_data(time, torque)
# plot the torque data
plot_timetable_dat(
    file_path=datFileTorque,
    dataLabel="Torque in Nm",
    title="Torque of TestMachineAPI",
    savefig=True,
    showfig=True,
    savePath=None,
)
# %% RegionValue formated file (VirtualWork results):
datFileTorqueVW = join(resDir, "Tr_vw.dat")
time, torque = resimport.read_RegionValue_dat(file_path=datFileTorqueVW)
# split up data if needed
nbrSims, timeArray, torqueArray = split_data(time, torque)
# PLOT TORQUE
for sim in range(nbrSims):
    fig, ax = plt.subplots()
    fig.set_dpi(300)
    ax.plot(timeArray[sim], torqueArray[sim])
    # show()
    # ax.set_aspect("equal", adjustable="box")
    fig.axes[0].set_ylim(
        bottom=min(torqueArray[sim]) * (1.1 if min(torqueArray[sim]) < 0 else 0.9),
        top=max(torqueArray[sim]) * 1.1,
    )
    # ax.autoscale()
# %% PLOT INDUCED VOLTAGE
time = dict()
indVoltage = dict()
fig, ax = plt.subplots()
fig.set_dpi(300)
for phase in "ABC":
    time[phase], indVoltage[phase] = read_timetable_dat(
        join(resDir, "InducedVoltage" + phase + ".dat")
    )
    n, t, data = split_data(time[phase], indVoltage[phase])
    for sim in range(n):
        ax.plot(t[sim], data[sim], label=f"Sim: {sim}, Phase: {phase}")
ax.legend()

# %% Import Radial Flux Density in Airgap
time = {}
pos = {}
angle = {}
Brad = {}

for machineSide in ["stator", "rotor"]:
    posFile = join(resDir, f"b_radial_airgap_{machineSide}.pos")
    if isfile(posFile):
        name, time[machineSide], pos[machineSide], Brad[machineSide] = importSP(posFile)
        angle[machineSide] = []
        for pNbr in range(len(pos[machineSide])):
            px = pos[machineSide][pNbr][0]
            py = pos[machineSide][pNbr][1]
            if py == 0:
                angle[machineSide].append(0.0)
            else:
                angle[machineSide].append(atan(px / py))
fig, ax = plt.subplots()
fig.set_dpi(300)
ax.plot(angle["rotor"], Brad["rotor"])
fig.show()

# %%
