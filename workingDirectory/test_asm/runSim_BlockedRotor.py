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

nbr_bars = 9

f_r = 50
I_eff = 20
n = 0
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 80
nbr_steps_per_period = 128
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 4  # Default=4 number of Segments per timestep
timestep = (
    (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / nbr_steps_per_period
)
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbr_timesteps = T_s * nbr_stator_periods / timestep

thers = 100  # Thershold for bar resistance reset in A

logging.info("Simulation should execute %i time steps.", int(nbrSteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbrSteps) * timestep)
# %%
resId = f"blockedRotor_{f_r}Hz_{nbr_stator_periods}Periods_{nbr_steps_per_period}Steps_R_dyn_thers_{thers}A"
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
        "Flag_ClearResults": 0,
        "verbosity level": 3,
        # "AxialLength_R": 1,
        # "AxialLength_S": 1,
        "NbrParallelPaths": 1,
        "R_endring_segment": 16e-7 / 2,  # Initial value: 16e-7,
        "L_endring_segment": 2e-9 / 2,
        "Flag_Cir_RotorCage": 1,
        "Flag_Dynamic_RotorBarResistance": 1,
        "thers_dyn_Bar": thers,
        "Flag_Calculate_VW": 0,
        #                           fineMesh or coarseMesh
        "msh": os.path.join(MODEL_DIR, "coarseMesh.msh"),
        # "Flag_SecondOrder": 0,
        "stop_criterion": 1e-8,
    },
    "ResId": resId,
    "pro": os.path.join(MODEL_DIR, MODEL_NAME + ".pro"),
    "res": os.path.join(
        MODEL_DIR,
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
    ),
    "exe": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\getdp.exe",
    "gmsh": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\gmsh.exe",
    # "log": f"{resId}.log",  # log file name
    # "hyst": 0, # 172.04,
    # "eddy": 0, # 1.0472,
    # "exc": 0,
    # "axLen": 0.2,
    # "sym": 4,
    "info": "Restart simulation to check R_Bar_runtime and calculate moving mean.",
    "datetime": time.ctime(),
    "PostOp": ["Get_LocalFields_Post"],  # GetBOnRadius - Get_LocalFields_Post
}
sim_res_dir = os.path.join(paramDict["res"], resId)
results = runCalcforCurrent(paramDict)
stop = time.perf_counter()
sim_duration = stop - start
logging.info(
    "Simulation took %s", str(datetime.timedelta(seconds=sim_duration))
)
if sim_duration > nbrSteps:
    results["sim_duration"] = str(datetime.timedelta(seconds=sim_duration))
# %%
out_dict = paramDict.copy()
out_dict.update(results)
json_res_path = os.path.join(paramDict["res"], resId, f"{resId}.json")
if not os.path.isfile(json_res_path):
    # only write to file if script has not been run before!
    # TODO: Move this to runCalcForCurrent function
    with open(json_res_path, "w", encoding="utf-8") as jFile:
        json.dump(out_dict, jFile, indent=4, cls=NumpyEncoder)
# %%
# plot currents
nbr_timesteps = len(results["time"]) # update number of timesteps with actual val
fig, ax = plt.subplots()
ax.plot(results["time"], results["current"]["a"], label="u")
ax.plot(results["time"], results["current"]["b"], label="v")
ax.plot(results["time"], results["current"]["c"], label="w")
ax.legend()
ax.grid(True)
ax.minorticks_on()

# %%
# PLOT STABSTRÖME
t, I_bars = (results["time"], results["current"]["bars"])
fig, axi = plt.subplots()
axi: Axes = axi
for nBar in range(nbr_bars):
    line_i = axi.plot(
        results["time"],
        I_bars[:, nBar],
        label=f"Bar {nBar+1}",
        marker=".",
        markersize=3,
    )
axi.set_ylabel("Strom in A")
if t[-1] > 2 * T_s:  # if specific amount of periods is calculated
    axi.set_xlim(
        t[int(t.size * ((nbr_stator_periods - 2) / nbr_stator_periods))], t[-1]
    )
axi.legend()
axi.grid(True)
axi.set_title(f"Stabströme")
# %%
# Stabspannung vs Stabstrom
resfile = os.path.join(sim_res_dir, "U_bars.dat")
if os.path.isfile(resfile):
    t, U_bars = read_timetable_dat(resfile)
    fig, ax = plt.subplots()
    ax: Axes = ax
    nBar = 0
    line_u = ax.plot(t, U_bars[:, nBar], label="Spannung", color="b")
    ax.set_ylabel("Spannung in V")

    axi: Axes = ax.twinx()
    line_i = axi.plot(
        results["time"],
        results["current"]["bars"][:, nBar],
        color="g",
        label="Strom",
    )
    axi.set_ylabel("Strom in A")
    ax.grid(True)
    ax.legend(handles=[line_u[0], line_i[0]])
    ax.set_title(f"Stab {nBar+1}")

    # %
    fig, ax = plt.subplots()
    ax: Axes = ax
    r_bar = np.mean(U_bars[1:, nBar] / I_bars[1:, nBar])
    line_u = ax.plot(
        t, U_bars[:, nBar] / I_bars[:, nBar], label="Widerstand", color="b"
    )
    ax.set_xlim(
        t[int(t.size * (nbr_stator_periods - 2) / nbr_stator_periods)], t[-1]
    )
    ax.set_ylim(-1e-5, 1e-5)
    ax.grid(True)

    # %
    fig, ax = plt.subplots()
    ax: Axes = ax
    for nBar in range(nbr_bars):
        line_u = ax.plot(t, U_bars[:, nBar], label=f"Stab {nBar}")
    ax.set_ylabel("Spannung in V")
    # ax.set_xlim(14.75,15)
    ax.legend()
    # ax.set_ylim(-1e-5,1e-5)
    ax.grid(True)

# %%
# Induzierte Spannung Stator
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
fig, ax = plt.subplots()
ax: Axes = ax
if os.path.isfile(os.path.join(sim_res_dir, "Ts_vw.dat")):
    t_t, ts_vw = read_RegionValue_dat(os.path.join(sim_res_dir, "Ts_vw.dat"))
    _, tr_vw = read_RegionValue_dat(os.path.join(sim_res_dir, "Tr_vw.dat"))
    torque_vw = np.mean([ts_vw, tr_vw], axis=0)
    # all Torques
    # line_ts = ax.plot(results["time"], results["torque"]["stator"], label=f"Ts (MST)")
    # line_tr = ax.plot(results["time"], results["torque"]["rotor"], label=f"Tr (MST)")
    # ax.plot(t_t, ts_vw, label=f"Ts (VW)")
    # ax.plot(t_t, tr_vw, label=f"Tr (VW)")
    ax.plot(t_t, torque_vw, "x-", label="VW")
    ax.legend()

# mean torque
results["torque"]["mean"] = np.mean(
    [results["torque"]["stator"], results["torque"]["rotor"]], axis=0
)

ax.plot(
    results["time"],
    results["torque"]["mean"],
    "-",
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
ax.grid(True, "major", linestyle="-")
ax.grid(True, "minor", linestyle="--")
ax.minorticks_on()

# %
# PRINT DES MITTLEREN DREHOMMENTS
M_mean_dyn = np.mean(
    results["torque"]["stator"][
        int(nbr_timesteps * (nbr_stator_periods - 1) / nbr_stator_periods) :
    ]
)
print(
    f"Das mittlere Drehmoment der letzten Periode (dynamisch) sind {M_mean_dyn:.2f} Nm"
)
# read data from static resistance calculation
t_stat, M_stat = read_timetable_dat(
    r"C:\Users\ganser\AppData\Local\Programs\pyemmo\workingDirectory\test_asm\res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz\blockedRotor_50Hz_80Periods_64Steps_R_stat\Ts.dat"
)
M_mean_stat = np.mean(M_stat[int(t_stat.size * 79 / 80) :])
print(
    f"Das mittlere Drehmoment der letzten Periode (statisch) sind {M_mean_stat:.2f} Nm"
)

# ax.plot(t_stat, M_stat, ".-", label="statischer Widerstand")
# ax.legend()
# %%
# PLOT RESISTANCES
resfile = os.path.join(sim_res_dir, "R_bar_1.dat")
if os.path.isfile(resfile):
    R_bar_dc = 3.572345668067562e-05
    fig, ax = plt.subplots()
    ax: Axes = ax
    # for nBar in range(1,nbr_bars+1):
    for nBar in (1, 1):
        resfile = os.path.join(sim_res_dir, f"R_bar_{nBar}.dat")
        if os.path.isfile(resfile):
            t, R_bar = read_timetable_dat(resfile)
            ax.plot(t, R_bar, label=f"R_bar_{nBar}", marker=".")
    ax.plot(
        [t[0], t[-1]], [R_bar_dc, R_bar_dc], label=f"R_bar (DC)", marker=None
    )
    ax.set_ylim(bottom=0, top=3 * R_bar_dc)
    # ax.set_xlim(0, T_s)
    ax.legend()

    axi: Axes = ax.twinx()
    axi.plot(
        results["time"],
        np.abs(results["current"]["bars"][:, nBar - 1]),
        color="b",
        label=f"Strom Stab {nBar}",
        marker=".",
    )
    axi.set_ylabel("Strom in A")
    axi.grid(True)
    axi.legend()
    ax.legend()
    # plt.close()
    # plot_timetable_dat(resfile,dataLabel=f"R_{{bar,{nBar}}}")
else:
    logging.info(
        "No bar resistance results in result directory %s", sim_res_dir
    )
## ADD PLOT OF RUNTIME RESISTANCE
resfile = os.path.join(sim_res_dir, "R_bar_runtime_1.dat")
if os.path.isfile(resfile):
    # for nBar in range(1,nbr_bars+1):
    for nBar in (1, 1):
        resfile = os.path.join(sim_res_dir, f"R_bar_runtime_{nBar}.dat")
        if os.path.isfile(resfile):
            t, R_bar = read_timetable_dat(resfile)
            ax.plot(t, R_bar, label=f"R_bar_{nBar} (runtime)", marker=".")
    # ax.set_ylim(bottom=0, top=15 * R_bar_dc)
    # ax.set_xlim(T_s/4, T_s*3/4)
    ax.legend()
    # axi.set_ylim(0, 200)
# %%
fig, ax = plt.subplots()
ax: Axes = ax
timestep = t[1] - t[0]
amp = np.abs(np.fft.rfft(R_bar, axis=0))
# to get correct amplitude regarding the specific frequencies, the amplitudes
# must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
# is doubled since its part of the positive and negative side of the spectrum.
# Since I defined the number of frequencies to be only for the one sided spectrum,
# we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
freqs = np.fft.rfftfreq(nbr_timesteps, timestep)
nbr_freqs = len(freqs)
amp = np.concatenate(([amp[0] / nbr_freqs / 2], amp[1:] / (nbr_freqs)), axis=0)
amp = np.concatenate(([amp[0] / nbr_freqs / 2], amp[1:] / (nbr_freqs)), axis=0)
plt.stem(freqs, amp)
# %%
# Export Data for Maxwell
from pyemmo.functions.exportMaxwell import exportTabMaxwell

mxwl_export_dir = os.path.join(sim_res_dir,"export_maxwell")
if not os.path.isdir(mxwl_export_dir):
    os.mkdir(mxwl_export_dir)
# Export Bar Current
f_name_mxwl_export = os.path.join(mxwl_export_dir, "I_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], I_bars[:, 0]],
        identifier=["Time (s)", "I_Bar_Onelab (A)"],
        filepath=f_name_mxwl_export,
    )
# Export Bar Voltage
f_name_mxwl_export = os.path.join(mxwl_export_dir, "U_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], U_bars[:, 0]],
        identifier=["Time (s)", "V_Bar_Onelab (V)"],
        filepath=f_name_mxwl_export,
    )
# Export Torque
f_name_mxwl_export = os.path.join(mxwl_export_dir, "torque.tab")
if not os.path.isfile(f_name_mxwl_export):
    if any(np.equal(results["torque"]["mean"].shape, 1)):
        # reshape so single values are not in an own array
        results["torque"]["mean"] = results["torque"]["mean"].reshape(
            results["torque"]["mean"].size
        )
    exportTabMaxwell(
        [out_dict["time"], results["torque"]["mean"]],
        identifier=["Time (s)", "Torque_Onelab (Nm)"],
        filepath=f_name_mxwl_export,
    )
# %%
logging.shutdown()
# %% FINAL
