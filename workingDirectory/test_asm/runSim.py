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
from pyemmo.functions.import_results import (
    read_timetable_dat,
    plot_all_dat,
    plot_timetable_dat,
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

f_r = 4
I_eff = 50
n = 1000
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 80
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 8  # Default=4 number of Segments per timestep
timestep = (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / 90
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbrSteps = T_s / timestep * nbr_stator_periods
logging.info("Simulation should execute %i time steps.", int(nbrSteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbrSteps) * timestep)
# %%
resId = f"{I_eff}A_{n}rpm_{f_r}Hz_{nbr_stator_periods}Periods"
paramDict = {
    "getdp": {
        "RPM": float(n),
        "nbrStatorPeriods": nbr_stator_periods,
        "d_theta": winkelschritt,
        "freq_rotor": f_r,
        "I_eff": I_eff,
        # "IQ_RMS": float(idq[1]),
        "initrotor_pos": 0.0,
        "ResId": resId,
        "Flag_AnalysisType": 1,
        "Flag_PrintFields": 0,
        "Flag_Debug": 1,
        "Flag_ClearResults": 0,
        "verbosity level": 3,
        # "AxialLength_R": 1,
        # "AxialLength_S": 1,
        "NbrParallelPaths": 1,
        "R_endring_segment": 16e-7 / 2,  # Initial value: 16e-7,
        "L_endring_segment": 2e-9 / 2,
        "Flag_Cir_RotorCage": 1,
        "Flag_Dynamic_RotorBarResistance": 0,
        # "Flag_Calculate_VW": 1,
        #                          fineMesh or coarseMesh
        "msh": os.path.join(MODEL_DIR, "fineMesh.msh"),
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
    "info": "Neue Simulation bei 1000 rpm, 4Hz mit statischem Rotorstab Widerstand.",
    "datetime": time.ctime(),
    "PostOp": [],
}

results = runCalcforCurrent(paramDict)
stop = time.perf_counter()
sim_duration = stop - start
logging.info(
    "Simulation took %s", str(datetime.timedelta(seconds=sim_duration))
)
if sim_duration > 1:
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
# plot_all_dat(respath)
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
# ax.set_xlim(13, None)
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
# axi.set_xlim(8, 10)
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
# ax.set_xlim(13, None)
# ax.set_ylim(-1e-5, 1e-5)
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
ax.set_ylabel("Strom in A")
# ax.set_xlim(13, 15)
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
# ax.set_xlim(14.5, 15)
ax.legend()
# ax.set_ylim(-1e-5,1e-5)
ax.grid(True)
# %%
# Plot Drehmoment
fig, ax = plt.subplots()
ax: Axes = ax
if os.path.isfile(os.path.join(respath, "Ts_vw.dat")):
    t_t, ts_vw = read_RegionValue_dat(os.path.join(respath, "Ts_vw.dat"))
    _, tr_vw = read_RegionValue_dat(os.path.join(respath, "Tr_vw.dat"))

    # all Torques
    # line_ts = ax.plot(results["time"], results["torque"]["stator"], label=f"Ts (MST)")
    # line_tr = ax.plot(results["time"], results["torque"]["rotor"], label=f"Tr (MST)")
    # ax.plot(t_t, ts_vw, label=f"Ts (VW)")
    # ax.plot(t_t, tr_vw, label=f"Tr (VW)")
    ax.plot(t_t, np.mean([ts_vw, tr_vw], axis=0), label="VW")

# mean torque
results["torque"]["mean"] = np.mean(
    [results["torque"]["stator"], results["torque"]["rotor"]], axis=0
)
ax.plot(
    results["time"],
    results["torque"]["mean"],
    ".-",
    label="MST",
)
# ax.set_ylabel("Spannung in V")
ax.legend(loc=1)
# ax.set_xlim(
#     t[int(t.size * (nbr_stator_periods - 1) / nbr_stator_periods)], t[-1]
# )
# ax.set_ylim([-25,60]) # medium zoom
# ax.set_ylim([210, 235])  # high zoom
ax.set_title("Drehmoment")
ax.grid(True)
# %%
# PLOT RESISTANCES
resfile = os.path.join(respath, "R_bar_1.dat")
if os.path.isfile(resfile):
    R_bar_dc = 5.19932563e-05
    fig, ax = plt.subplots()
    ax: Axes = ax
    # for nBar in range(1,nbr_bars+1):
    for nBar in (1, 5, 9):
        resfile = os.path.join(respath, f"R_bar_{nBar}.dat")
        if os.path.isfile(resfile):
            t, R_bar = read_timetable_dat(resfile)
            ax.plot(t, R_bar, label=f"R_bar_{nBar}", marker=".")
    ax.set_ylim(bottom=0, top=3 * R_bar_dc)
    ax.legend()
    # plt.close()
    # plot_timetable_dat(resfile,dataLabel=f"R_{{bar,{nBar}}}")
else:
    logging.info(f"No bar resistance results in result directory {respath}")
# %%
# Export Data for Maxwell
from pyemmo.functions.exportMaxwell import exportTabMaxwell

# Export Bar Current
f_name_mxwl_export = os.path.join(respath, "I_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], I_bars[:, 0]],
        identifier=["Time (s)", "I_Bar_Onelab (A)"],
        filepath=f_name_mxwl_export,
    )
# Export Bar Voltage
f_name_mxwl_export = os.path.join(respath, "U_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], U_bars[:, 0]],
        identifier=["Time (s)", "V_Bar_Onelab (V)"],
        filepath=f_name_mxwl_export,
    )
# Export Torque
f_name_mxwl_export = os.path.join(respath, "torque.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], results["torque"]["mean"]],
        identifier=["Time (s)", "Torque_Onelab (Nm)"],
        filepath=f_name_mxwl_export,
    )
# %%
logging.shutdown()
# %% FINAL
