# %%
import os
import json
import logging
import time
import datetime
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from pyemmo.functions.runOnelab import runCalcforCurrent
from pyemmo.functions.import_results import read_timetable_dat, plot_all_dat
from definitions import MODEL_NAME, MODEL_DIR

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

add_StreamHandler = True
for handler in root_logger.handlers:
    if type(handler) is logging.StreamHandler:
        print("StreamHandler vorhanden.")
        add_StreamHandler = False
        break

if add_StreamHandler:
    c_handler = logging.StreamHandler()
    root_logger.addHandler(c_handler)

logger = logging.getLogger("matplotlib").setLevel(logging.WARNING)

# %%
logging.debug(f"Start simulation at {time.ctime()}")
start = time.perf_counter()

f_r = 4
I_eff = 50
n = 1000
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 1
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 4  # Default=4 number of Segments per timestep
timestep = (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / 90
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbrSteps = T_s / timestep * nbr_stator_periods
logging.info("Simulation should execute %i time steps.", int(nbrSteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbrSteps) * timestep)
# %%
resId = f"test + {time.ctime()}"
paramDict = {
    "getdp": {
        "freq_rotor": f_r,
        "I_eff": I_eff,
        # "IQ_RMS": float(idq[1]),
        "RPM": float(n),
        "nbStatorPeriods": nbr_stator_periods,
        "d_theta": winkelschritt,
        "ResId": resId,
        "Flag_AnalysisType": 1,
        "Flag_PrintFields": 0,
        "Flag_Debug": 0,
        "Flag_ClearResults": 1,
        "verbosity level": 5,
        "L_endring_segment": 2e-9,
        "R_endring_segment": 1e-16,
        "msh": os.path.join(MODEL_DIR, "coarseMesh.msh"),  # fineMesh.msh
    },
    "ResId": resId,
    "pro": os.path.join(MODEL_DIR, MODEL_NAME + ".pro"),
    "res": os.path.join(
        MODEL_DIR,
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
    ),
    "exe": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\getdp.exe",
    "gmsh": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\gmsh.exe",
    # "hyst": 0, # 172.04,
    # "eddy": 0, # 1.0472,
    # "exc": 0,
    # "axLen": 0.2,
    # "sym": 4,
    "info": "Reset speed to 1000 rpm.",
    "PostOp": ["test", "GetBOnRadius"],
    "datetime": time.ctime(),
}

results = runCalcforCurrent(paramDict)
stop = time.perf_counter()
sim_duration = stop - start
logging.info(
    "Simulation took %s", str(datetime.timedelta(seconds=sim_duration))
)
if sim_duration > nbrSteps * 3:
    results["simlation_duration"] = sim_duration
# %%
out_dict = paramDict.copy()
out_dict.update(results)
with open(
    os.path.join(paramDict["res"], resId, f"{resId}.json"),
    "w",
    encoding="utf-8",
) as jFile:
    json.dump(out_dict, jFile, indent=4, cls=NumpyEncoder)
# %%

# plot currents
fig, ax = plt.subplots()
ax.plot(results["time"], results["current"]["a"])
ax.plot(results["time"], results["current"]["b"])
ax.plot(results["time"], results["current"]["c"])

# %%
fig, ax = plt.subplots()
ax.grid()
ax.plot(results["current"]["bars"], linewidth=0.5)

# %%
respath = os.path.join(paramDict["res"], resId)
plot_all_dat(respath)
# %%
t, U_bars = read_timetable_dat(os.path.join(respath, "U_bars.dat"))
fig, ax = plt.subplots()
ax: Axes = ax
nbar = 8
line_u = ax.plot(t, U_bars[:, nbar], label="Spannung", color="b")
ax.set_ylabel("Spannung in V")
t, I_bars = read_timetable_dat(os.path.join(respath, "I_bars.dat"))
axi: Axes = ax.twinx()
line_i = axi.plot(t, I_bars[:, nbar], label="Strom", color="g")
axi.set_ylabel("Strom in A")
ax.set_xlim(13, None)
ax.grid(True)
ax.legend(handles=[line_u[0], line_i[0]])
ax.set_title(f"Stab {nbar+1}")
# %%
t, I_bars = read_timetable_dat(os.path.join(respath, "I_bars.dat"))
fig, axi = plt.subplots()
axi: Axes = axi
for nbar in range(9):
    line_i = axi.plot(t, I_bars[:, nbar], label=f"Bar {nbar+1}")
axi.set_ylabel("Strom in A")
axi.set_xlim(8, 10)
axi.legend()
axi.grid(True)
axi.set_title(f"Stabströme")

# %%
fig, ax = plt.subplots()
ax: Axes = ax
r_bar = np.mean(U_bars[1:, nbar] / I_bars[1:, nbar])
line_u = ax.plot(
    t, U_bars[:, nbar] / I_bars[:, nbar], label="Widerstand", color="b"
)
ax.set_xlim(13, None)
ax.set_ylim(-1e-5, 1e-5)
ax.grid(True)

# %%
fig, ax = plt.subplots()
ax: Axes = ax
for nbar in range(9):
    line_u = ax.plot(t, U_bars[:, nbar], label=f"Stab {nbar}")
ax.set_ylabel("Spannung in V")
# ax.set_xlim(14.75,15)
ax.legend()
# ax.set_ylim(-1e-5,1e-5)
ax.grid(True)

# %%
fig, ax = plt.subplots()
ax: Axes = ax
for nbar in range(9):
    line_u = ax.plot(t, I_bars[:, nbar], label=f"Stab {nbar}")
# ax.set_ylabel("Spannung in V")
ax.set_xlim(13, 15)
ax.legend()
# ax.set_ylim(-1e-5,1e-5)
ax.grid(True)

# %%
t, U_iA = read_timetable_dat(os.path.join(respath, "InducedVoltageA.dat"))
t, U_iB = read_timetable_dat(os.path.join(respath, "InducedVoltageB.dat"))
t, U_iC = read_timetable_dat(os.path.join(respath, "InducedVoltageC.dat"))
fig, ax = plt.subplots()
ax: Axes = ax
# for phase in 'ABC':
line_u = ax.plot(t, U_iA, label=f"U_iA")
line_u = ax.plot(t, U_iB, label=f"U_iB")
line_u = ax.plot(t, U_iC, label=f"U_iC")
# ax.set_ylabel("Spannung in V")
ax.set_xlim(14.5, 15)
ax.legend()
# ax.set_ylim(-1e-5,1e-5)
ax.grid(True)
# %%
logging.shutdown()
# %% FINAL
