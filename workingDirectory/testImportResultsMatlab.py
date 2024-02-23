from sys import path
from os.path import abspath, join, dirname
from matplotlib.pyplot import plot, show
from matplotlib import pyplot as plt

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)

from pyemmo.functions.importResults import plotTimeTableDat, read_timetable_dat, split_data
from pyemmo.definitions import RESULT_DIR, MAIN_DIR

simDir = join(r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\matlab", ...) # FIXME: CREATE TESTFILE DIRECTORY
# TORQUE
plotTimeTableDat(join(simDir, "Ts.dat"),"Torque in Nm", title="Torque of IPM_1FE1051_modMagnet", savefig=True)
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
