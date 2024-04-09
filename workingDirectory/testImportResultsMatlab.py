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
from sys import path
from os.path import abspath, join, dirname
from matplotlib.pyplot import plot, show
from matplotlib import pyplot as plt

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = (
        "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    )
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)

from pyemmo.functions.import_results import (
    plot_timetable_dat,
    read_timetable_dat,
    split_data,
)
from pyemmo.definitions import RESULT_DIR, MAIN_DIR

simDir = join(
    r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\matlab", ...
)  # FIXME: CREATE TESTFILE DIRECTORY
# TORQUE
plot_timetable_dat(
    join(simDir, "Ts.dat"),
    "Torque in Nm",
    title="Torque of IPM_1FE1051_modMagnet",
    savefig=True,
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

# PLOT INDUCED VOLTAGE
time = dict()
indVoltage = dict()
fig, ax = plt.subplots()
fig.set_dpi(300)
for phase in "ABC":
    time[phase], indVoltage[phase] = read_timetable_dat(
        join(simDir, "InducedVoltage" + phase + ".dat")
    )
    ax.plot(time[phase], indVoltage[phase])
show()
