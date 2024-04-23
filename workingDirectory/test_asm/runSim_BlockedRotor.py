# %%
# %matplotlib widget
import os
import json
import logging
import time
import datetime
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from pyemmo.functions.runOnelab import runCalcforCurrent
from pyemmo.functions.import_results import (
    read_timetable_dat,
    # plot_all_dat,
    # plot_timetable_dat,
    read_RegionValue_dat,
)
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

f_r = 1
I_eff = 50
n = 0
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 4
nbr_steps_per_period = 256
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 8  # Default=4 number of Segments per timestep
timestep = (
    (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / nbr_steps_per_period
)
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbrSteps = T_s * nbr_stator_periods / timestep
logging.info("Simulation should execute %i time steps.", int(nbrSteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbrSteps) * timestep)
# %%
resId = "blockedRotor_1Hz_4Periods_256Steps_NewCirc"
# resId = "blockedRotor_1Hz_Circ"
paramDict = {
    "getdp": {
        "freq_rotor": f_r,
        "I_eff": I_eff,
        # "IQ_RMS": float(idq[1]),
        "RPM": float(n),
        "initrotor_pos": 0.0,
        "nbrStatorPeriods": nbr_stator_periods,
        "nbrStepsPerPeriod": nbr_steps_per_period,
        "d_theta": winkelschritt,
        "ResId": resId,
        "Flag_AnalysisType": 1,
        "Flag_PrintFields": 0,
        "Flag_Debug": 1,
        "Flag_ClearResults": 1,
        "verbosity level": 3,
        ## NEW
        # "AxialLength_R": 1,
        # "AxialLength_S": 1,
        "R_endring_segment": 16e-7 / 2,  # Initial value: 16e-7,
        "L_endring_segment": 2e-9 / 2,
        "Flag_Cir_RotorCage": 1,
        # "Flag_Calculate_VW": 1,
        "msh": os.path.join(MODEL_DIR, "coarseMesh.msh"), # fineMesh.msh
        # "Flag_SecondOrder": 0,
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
    "info": "Käfig-Ersatzschaltbild aktualisiert, sodass beide Kurzschlussringseiten separat modeliert werden.",
    "datetime": time.ctime(),
    "PostOp": ["GetBOnRadius"],
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
# Stabströme
t, I_bars = (results["time"], results["current"]["bars"])
fig, axi = plt.subplots()
axi: Axes = axi
for nbar in range(9):
    line_i = axi.plot(
        results["time"],
        results["current"]["bars"][:, nbar],
        label=f"Bar {nbar+1}",
    )
axi.set_ylabel("Strom in A")
axi.set_xlim(
    t[int(t.size * ((nbr_stator_periods - 2) / nbr_stator_periods))], t[-1]
)
axi.legend()
axi.grid(True)
axi.set_title(f"Stabströme")
# %%
respath = os.path.join(paramDict["res"], resId)
# plot_all_dat(respath)
# %%
# Stabspannung vs Stabstrom
u_bars_resfile = os.path.join(respath, "U_bars.dat")
if os.path.isfile(u_bars_resfile):
    t, U_bars = read_timetable_dat(u_bars_resfile)
    fig, ax = plt.subplots()
    ax: Axes = ax
    nbar = 8
    line_u = ax.plot(t, U_bars[:, nbar], label="Spannung", color="b")
    ax.set_ylabel("Spannung in V")

    axi: Axes = ax.twinx()
    line_i = axi.plot(
        results["time"], results["current"]["bars"][:, nbar], color="g"
    )
    axi.set_ylabel("Strom in A")
    ax.grid(True)
    ax.legend(handles=[line_u[0], line_i[0]])
    ax.set_title(f"Stab {nbar+1}")

    # %
    fig, ax = plt.subplots()
    ax: Axes = ax
    r_bar = np.mean(U_bars[1:, nbar] / I_bars[1:, nbar])
    line_u = ax.plot(
        t, U_bars[:, nbar] / I_bars[:, nbar], label="Widerstand", color="b"
    )
    ax.set_xlim(
        t[int(t.size * (nbr_stator_periods - 2) / nbr_stator_periods)], t[-1]
    )
    ax.set_ylim(-1e-5, 1e-5)
    ax.grid(True)

    # %
    fig, ax = plt.subplots()
    ax: Axes = ax
    for nbar in range(9):
        line_u = ax.plot(t, U_bars[:, nbar], label=f"Stab {nbar}")
    ax.set_ylabel("Spannung in V")
    # ax.set_xlim(14.75,15)
    ax.legend()
    # ax.set_ylim(-1e-5,1e-5)
    ax.grid(True)

# %% Induzierte Spannung Stator
fig, ax = plt.subplots()
ax: Axes = ax
# for phase in 'ABC':
line_u = ax.plot(
    results["time"][:-1], results["inducedVoltage"]["a"], label=f"U_ind,A"
)
line_u = ax.plot(
    results["time"][:-1], results["inducedVoltage"]["b"], label=f"U_ind,B"
)
line_u = ax.plot(
    results["time"][:-1], results["inducedVoltage"]["c"], label=f"U_ind,C"
)
# line_u = ax.plot(t, U_iB, label=f"U_iB")
# line_u = ax.plot(t, U_iC, label=f"U_iC")
# ax.set_ylabel("Spannung in V")
ax.legend(loc=1)
t = results["time"]
# ax.set_xlim(t[int(t.size * (nbr_stator_periods - 2) / nbr_stator_periods)], t[-1])
ax.grid(True)
# %%
# Plot Drehmoment
if os.path.isfile(os.path.join(respath, "Ts_vw.dat")):
    t_t, ts_vw = read_RegionValue_dat(os.path.join(respath, "Ts_vw.dat"))
    _, tr_vw = read_RegionValue_dat(os.path.join(respath, "Tr_vw.dat"))

    fig, ax = plt.subplots()
    ax: Axes = ax
    # all Torques
    # line_ts = ax.plot(results["time"], results["torque"]["stator"], label=f"Ts (MST)")
    # line_tr = ax.plot(results["time"], results["torque"]["rotor"], label=f"Tr (MST)")
    # ax.plot(t_t, ts_vw, label=f"Ts (VW)")
    # ax.plot(t_t, tr_vw, label=f"Tr (VW)")

    # mean torque
    ax.plot(
        results["time"],
        np.mean(
            [results["torque"]["stator"], results["torque"]["rotor"]], axis=0
        ),
        ".-",
        label="MST",
    )
    ax.plot(t_t, np.mean([ts_vw, tr_vw], axis=0), label="VW")
    # ax.set_ylabel("Spannung in V")
    ax.legend(loc=1)
    ax.set_xlim(
        t[int(t.size * (nbr_stator_periods - 1) / nbr_stator_periods)], t[-1]
    )
    # ax.set_ylim([150,280]) # medium zoom
    ax.set_ylim([210, 235])  # high zoom
    ax.set_title("Drehmoment")
    ax.grid(True)
# %%
logging.shutdown()
# %% FINAL
