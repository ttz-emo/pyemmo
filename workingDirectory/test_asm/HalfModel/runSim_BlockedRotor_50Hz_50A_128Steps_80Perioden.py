# %%
# %matplotlib widget
import datetime
import json
import logging
import os
import time

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.import_maxwell import import_csv_data
from pyemmo.functions.import_results import (
    read_RegionValue_dat,
    read_timetable_dat,
)
from pyemmo.functions.runOnelab import runCalcforCurrent
from workingDirectory.test_asm.HalfModel.definitions import (
    MODEL_DIR,
    MODEL_NAME,
)


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


def import_mean_torque(res_dir: str) -> tuple[np.ndarray, np.ndarray]:
    """import the mean of stator and rotor MST torque.

    Args:
        res_dir (str): Result directory with Ts.dat and Tr.dat

    Returns:
        (np.ndarray, np.ndarray): Time and mean torque vector
    """
    resfile = os.path.join(
        res_dir,
        "Ts.dat",
    )
    _, torque_s = read_timetable_dat(resfile)
    resfile = os.path.join(
        res_dir,
        "Tr.dat",
    )
    t, torque_r = read_timetable_dat(resfile)
    torque_mean = np.mean([torque_s, torque_r], axis=0)
    return t, torque_mean


def autoscale_y(ax: Axes, margin=0.1):
    """This function rescales the y-axis based on the data that is visible given the
    current xlim of the axis.

    Args:
        ax (Axes): a matplotlib axes object-
        margin (float, optional): the fraction of the total height of the y-data to pad
            the upper and lower ylims. Defaults to 0.1.
    """

    def get_bottom_top(line: Line2D):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo, hi = ax.get_xlim()
        y_displayed = yd[((xd > lo) & (xd < hi))]
        h = np.max(y_displayed) - np.min(y_displayed)
        bot = np.min(y_displayed) - margin * h
        top = np.max(y_displayed) + margin * h
        return bot, top

    lines = ax.get_lines()
    bot, top = np.inf, -np.inf

    for line in lines:
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot:
            bot = new_bot
        if new_top > top:
            top = new_top

    ax.set_ylim(bot, top)


# %%
logging.debug(f"Start simulation at {time.ctime()}")

nbr_bars = 18

f_r = 50
I_eff = 50
n = 0
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 3
nbr_steps_per_period = 128
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 4  # Default=4 number of Segments per timestep
timestep = (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / nbr_steps_per_period
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbr_timesteps = T_s * nbr_stator_periods / timestep

flag_dynamic_resistance = False
thers = 100  # Thershold for bar resistance reset in A

logging.info("Simulation should execute %i time steps.", int(nbr_timesteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbr_timesteps) * timestep)

# %%
# %%
resId = f"SYM=1_blockedRotor_{f_r}Hz_{I_eff}A_{nbr_stator_periods}Periods_{nbr_steps_per_period}Steps"
if flag_dynamic_resistance:
    resId += "_R_dyn2"
    if thers:
        resId += f"_thers_{thers}A"
else:
    resId += "_R_stat"

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
        "Flag_Debug": 0,
        "Flag_ClearResults": 0,
        "verbosity level": 3,
        # "AxialLength_R": 1,
        # "AxialLength_S": 1,
        "NbrParallelPaths": 1,
        "R_endring_segment": 16e-7 / 2,  # Initial value: 16e-7,
        "L_endring_segment": 2e-9 / 2,
        "Flag_Cir_RotorCage": 1,
        "Flag_Dynamic_RotorBarResistance": flag_dynamic_resistance,
        "thers_dyn_Bar": thers,
        "Flag_Calculate_VW": 0,
        #                     mesh_veryFine, fineMesh or coarseMesh
        "msh": os.path.join(MODEL_DIR, "mesh_fine.msh"),
        # "Flag_SecondOrder": 0,
        "stop_criterion": 1e-8,
        "pA_deg": 90,
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
    "info": "Änderung der Schrittweite brachte keine Verbesserung der Simulationsergebnisse. Nächste Simulation mit Phasenverschiebung im Statorstromsystem. nbr_stator_periods reduziert auf 3 Perioden, da Spannungsverhalten bereits ab der 3. Periode erkennbar.",
    "datetime": time.ctime(),
    "PostOp": ["GetBOnRadius"],  # "GetBOnRadius" - "Get_LocalFields_Post"
}
sim_res_dir = os.path.join(paramDict["res"], resId)
start = time.perf_counter()
results = runCalcforCurrent(paramDict)
stop = time.perf_counter()
sim_duration = stop - start
if sim_duration > nbr_timesteps:
    results["sim_duration"] = str(datetime.timedelta(seconds=sim_duration))
    logging.info("Simulation took %s", str(datetime.timedelta(seconds=sim_duration)))
else:
    # Imported results
    if "sim_duration" in results:
        logging.info(
            "Imported Results. Simulation took %s",
            str(results["sim_duration"]),
        )
    else:
        logging.warning(
            "Missing 'sim_duration' from results dict! "
            "Maybe simulation terminated. Checking time values..."
        )
        exspected_end_time = timestep * nbr_timesteps
        if np.isclose(results["time"][-1], exspected_end_time, atol=timestep):
            logging.debug(
                "End time is ok.\nExpected end time:%f\nActual end time:%f",
                exspected_end_time,
                results["time"][-1],
            )
        else:
            logging.error(
                "End time of simulation not matching!.\nExpected end time:%f\nActual end time:%f",
                exspected_end_time,
                results["time"][-1],
            )

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
i_last_period = int(results["time"].size - nbr_steps_per_period - 1)

# %%
# plot currents
nbr_timesteps = len(results["time"])  # update number of timesteps with actual val
fig, ax = plt.subplots()
ax.plot(results["time"], results["current"]["a"], label="u")
ax.plot(results["time"], results["current"]["b"], label="v")
ax.plot(results["time"], results["current"]["c"], label="w")
ax.legend()
ax.grid(True)
ax.set_xlim(results["time"][i_last_period], results["time"][-1])
ax.set_ylabel("Stator current in A")

# %%
# %%
# PLOT STABSTRÖME
t_I_bars, I_bars = (results["time"], results["current"]["bars"])
fig, ax = plt.subplots(2, 1)
axi: Axes = ax[0]
for nBar in range(nbr_bars):
    line_i = axi.plot(
        t_I_bars,
        I_bars[:, nBar],
        label=f"Bar {nBar+1}",
        marker=None,
        markersize=3,
    )
axi.set_ylabel("Strom in A")
# if t[-1] > 2 * T_s:  # if specific amount of periods is calculated
# axi.set_xlim(t_U_bars[int(nbr_timesteps/1.1)], t_U_bars[-1])
axi.set_xlim(0, t_I_bars[nbr_steps_per_period * 2])
axi.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left", ncol=1, borderaxespad=0)
axi.grid(True)
axi.set_title("Stabströme")

ax_zoomed: Axes = ax[1]
for nBar in range(nbr_bars):
    line_i = ax_zoomed.plot(
        t_I_bars[i_last_period:-1],
        I_bars[i_last_period:-1, nBar],
        label=f"Bar {nBar+1}",
        marker=".",
        markersize=3,
    )
ax_zoomed.set_ylabel("Strom in A")
ax_zoomed.grid(True)
# ax_zoomed.set_title("Stabströme")

# %%
# Stabspannung vs Stabstrom
resfile = os.path.join(sim_res_dir, "U_bars.dat")
if os.path.isfile(resfile):
    t_U_bars, U_bars = read_timetable_dat(resfile)
    _, I_bars = read_timetable_dat(os.path.join(sim_res_dir, "I_bars.dat"))
    fig, ax = plt.subplots()
    ax: Axes = ax
    nBar = 0
    line_u = ax.plot(t_U_bars, U_bars[:, nBar], label="Spannung", color="b")
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
    ax.set_xlim([t_U_bars[i_last_period], t_U_bars[-1]])
    autoscale_y(ax)

    # %
    # Plot: R = U/I (Stab)
    fig, ax = plt.subplots()
    ax: Axes = ax
    r_bar = np.mean(U_bars[1:, nBar] / I_bars[1:, nBar])
    UdR = U_bars[1:, nBar] / I_bars[1:, nBar]
    ax.plot(t_U_bars[1:], UdR, label=f"Widerstand Stab {nBar}", color="b")
    ax.set_xlim(t_U_bars[i_last_period], t_U_bars[-1])
    ax.set_xlabel("time in s")
    ax.set_ylabel("Resistance in $\\Omega$")
    autoscale_y(ax)
    ax.grid(True)
    ax.legend()

    # %
    fig, ax = plt.subplots()
    ax: Axes = ax
    for nBar in range(nbr_bars):
        ax.plot(t_U_bars, U_bars[:, nBar], label=f"Stab {nBar+1}")
    ax.set_xlabel("time in s")
    ax.set_ylabel("Spannung in V")
    ax.set_xlim(t_U_bars[i_last_period], t_U_bars[i_last_period + nbr_steps_per_period])
    # place legend on the right hand side of the plot:
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left", ncol=1, borderaxespad=0)
    # ax.set_ylim(-1e-5,1e-5)
    ax.grid(True)


# %%
# %%
# Induzierte Spannung Stator
fig, ax = plt.subplots()
ax: Axes = ax
# for phase in 'ABC':
line_u = ax.plot(results["time"][:-1], results["inducedVoltage"]["a"], label=f"U_ind,A")
line_u = ax.plot(results["time"][:-1], results["inducedVoltage"]["b"], label=f"U_ind,B")
line_u = ax.plot(results["time"][:-1], results["inducedVoltage"]["c"], label=f"U_ind,C")
# line_u = ax.plot(t, U_iB, label=f"U_iB")
# line_u = ax.plot(t, U_iC, label=f"U_iC")
# ax.set_ylabel("Spannung in V")
ax.legend(loc=1)
t = results["time"]
# ax.set_xlim(t[int(t.size * (nbr_stator_periods - 2) / nbr_stator_periods)], t[-1])
ax.grid(True)


# %%
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

ax.plot(results["time"], results["torque"], "-", label=f"Half Model (MST, {resId})")

# %
# PRINT DES MITTLEREN DREHOMMENTS
M_mean_actual = np.mean(results["torque"][i_last_period:])
print(
    f"Das mittlere Drehmoment der letzten Periode (ID: {resId}) sind {M_mean_actual:.2f} Nm"
)

# read data from static resistance calculation (quarter model)
# Quater model result ID:
QM_res_ID = "blockedRotor_50Hz_50A_80Periods_128Steps_R_stat"
t_stat, M_stat = import_mean_torque(
    os.path.join(
        ROOT_DIR,
        r"workingDirectory\test_asm",
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
        QM_res_ID,
    )
)
M_mean_stat = np.mean(M_stat[int(t_stat.size * 79 / 80) :])
print(
    "Das mittlere Drehmoment der letzten Periode "
    f"(statisch, ID: {QM_res_ID}) sind {M_mean_stat:.2f} Nm"
)
ax.plot(
    t_stat,
    M_stat,
    "--",
    label=f"Quater Model (MST, {QM_res_ID})",
)
# Plot Maxwell results for comparison:
try:
    headers, data = import_csv_data(
        r"M:\AG_EM\11_Austausch\Max_Ganser\Vergleich_ASM_Maxwell_ONELAB\AP_fr_50Hz_Ieff_50A_n_0rpm\Maxwell_BlockedRotor_EndConnections_Fr50Hz_ISeff50A_EIP80\Torque Plot 1.csv"
    )
    data = np.array(data, dtype=float)
    t_mxwl = data[:, 0]
    torque_mxwl = data[:, 1]
    ax.plot(
        t_mxwl,
        torque_mxwl,
        label="Maxwell_BlockedRotor_EndConnections_Fr50Hz_ISeff50A_EIP80",
        alpha=0.5,
    )
    torque_mxwl_mean = np.mean(torque_mxwl[int(t_mxwl.size * 79 / 80) :])
    print(
        "Das mittlere Drehmoment der letzten Periode "
        "(Maxwell, ID: Maxwell_BlockedRotor_EndConnections_Fr50Hz_ISeff50A_EIP80) "
        f"sind {torque_mxwl_mean:.2f} Nm"
    )
except Exception:
    logging.exception("Could not plot Maxwell Torque results...")

# Adjust plot appearance:
ax.set_ylabel("Drehmoment in NM")
ax.grid(True, "major", linestyle="-")
ax.grid(True, "minor", linestyle="--")
ax.minorticks_on()
ax.set_xlim([t[i_last_period], t[-1]])
autoscale_y(ax, 0.05)
ax.legend(
    bbox_to_anchor=(0.0, 1.02, 1.0, 0.102),
    loc="lower left",
    ncol=1,
    mode="expand",
    borderaxespad=0.0,
    fontsize=8,
)
# %%
# %%
# PLOT internal GetDP resistances
resfile = os.path.join(sim_res_dir, "R_bar_1.dat")
if os.path.isfile(resfile):
    R_bar_dc = 3.572345668067562e-05
    fig, ax = plt.subplots()
    ax: Axes = ax
    # # Plot all bars:
    # for nBar in range(1,nbr_bars+1):
    # resfile = os.path.join(sim_res_dir, f"R_bar_{nBar}.dat")
    # if os.path.isfile(resfile):
    #     t, R_bar = read_timetable_dat(resfile)
    #     ax.plot(t, R_bar, label=f"R_bar_{nBar}", marker=".")

    # Plot Bar 1 only:
    resfile = os.path.join(sim_res_dir, "R_bar_1.dat")
    if os.path.isfile(resfile):
        t_R_bars, R_bar = read_timetable_dat(resfile)
        ax.plot(t_R_bars, R_bar, label="R (berechnet)", marker=".")
    # Plot DC resistance line:
    ax.plot(
        [t_R_bars[0], t_R_bars[-1]],
        [R_bar_dc, R_bar_dc],
        label="R (DC)",
        marker=None,
    )
    ax.set_ylim(bottom=0, top=100 * R_bar_dc)
    # ax.set_xlim(0, T_s)
    if t_R_bars[-1] >= nbr_stator_periods * T_s:
        ax.set_xlim(T_s * (nbr_stator_periods - 1), T_s * nbr_stator_periods)
    ax.legend()

    axi: Axes = ax.twinx()
    axi.plot(
        results["time"],
        np.abs(results["current"]["bars"][:, 0]),
        color="b",
        label="|Stabstrom|",
        marker=".",
        alpha=0.3,
    )
    axi.set_ylabel("Strom in A")
    axi.grid(True)
    ax.minorticks_on()
    axi.legend()
    ax.legend()
    # plt.close()
    # plot_timetable_dat(resfile,dataLabel=f"R_{{bar,{nBar}}}")
else:
    logging.info("No bar resistance results in result directory %s", sim_res_dir)
## ADD PLOT OF RUNTIME RESISTANCE
resfile = os.path.join(sim_res_dir, "R_bar_runtime_1.dat")
if os.path.isfile(resfile):
    t_Rrt_bars, R_bar = read_timetable_dat(resfile)
    ax.plot(t_Rrt_bars, R_bar, label=f"R_runtime (Circuit)", marker=".", ls="--")
    ax.legend()

    fig, ax = plt.subplots()
    ax: Axes = ax
    timestep = t_Rrt_bars[1] - t_Rrt_bars[0]
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

mxwl_export_dir = os.path.join(sim_res_dir, "export_maxwell")
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
    if any(np.equal(results["torque"].shape, 1)):
        # reshape so single values are not in an own array
        results["torque"] = results["torque"].reshape(results["torque"].size)
    exportTabMaxwell(
        [out_dict["time"], results["torque"]],
        identifier=["Time (s)", "Torque_Onelab (Nm)"],
        filepath=f_name_mxwl_export,
    )

# %%
# PLOT STABSTROM, -SPANNUNG UND -WIDERSTAND
# Plot U_bar
fig, ax = plt.subplots()
ax: Axes = ax
nBar = 0
ax.plot(results["time"], U_bars[:, nBar], label="Spannung", color="b", marker=".")
ax.set_ylabel("Spannung in V")
ax.grid(alpha=0.5, color="b")
ax.set_title(f"Stab {nBar+1}")
ax.set_xlim(T_s * (nbr_stator_periods - 1), T_s * nbr_stator_periods)

# Plot I_bar
axi: Axes = ax.twinx()
line_i = axi.plot(
    results["time"],
    results["current"]["bars"][:, nBar],
    marker=".",
    color="g",
    label="Strom",
)
axi.set_ylabel("Strom in A")
axi.grid(alpha=0.5, color="g")

# Plot R_bar (runtime)
resfile = os.path.join(sim_res_dir, f"R_bar_runtime_1.dat")
if os.path.isfile(resfile):
    axr = ax.twinx()
    axr.set_yticks([])
    t_R_bar_rt, R_bar_rt = read_timetable_dat(resfile)
    axr.plot(t_R_bar_rt, R_bar_rt, label=f"Stabwiderstand", marker=".", color="r")

# Add single legend
ax.legend(loc="best")


# %%
# %%
# Compare torque

fig, ax = plt.subplots()
ax: Axes = ax
nBar = 0

line_i = ax.plot(
    results["time"],
    results["torque"],
    marker=".",
    markersize=4,
    mfc=(1, 1, 1),
    label=resId,
)

## Plot Torque when resetting to DC Resistance
t_t_reset_DC, torque_reset_DC = import_mean_torque(
    os.path.join(
        ROOT_DIR,
        r"workingDirectory\test_asm",
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
        "blockedRotor_50Hz_80Periods_128Steps_R_dyn_thers_100A",
    )
)
line_i = ax.plot(
    t_t_reset_DC,
    torque_reset_DC,
    marker=".",
    markersize=4,
    markevery=1,
    mfc=(1, 1, 1),
    label="Reset DC",
    alpha=1,
)
## Plot Torque without resetting of resistance
t_t_no_reset, torque_no_reset = import_mean_torque(
    os.path.join(
        ROOT_DIR,
        r"workingDirectory\test_asm",
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
        "blockedRotor_50Hz_80Periods_64Steps_R_stat",
    )
)
line_i = ax.plot(
    t_t_no_reset,
    torque_no_reset,
    marker=".",
    markersize=4,
    markevery=1,
    mfc=(1, 1, 1),
    label="No Reset",
    alpha=1,
)
ax.legend()
ax.set_xlabel("time in s")
ax.set_ylabel("torque in Nm")
ax.grid(alpha=0.5)
ax.set_xlim(t[i_last_period], t[i_last_period + nbr_steps_per_period])
autoscale_y(ax)
print(f"Mean Reset DC = {np.mean(torque_reset_DC[int(t_t_reset_DC.size * 79 / 80) :])}")
print(
    f"""Mean {resId} = {np.mean(results["torque"][int(results["time"].size * 79 / 80) :])}"""
)

# %%
# %%
# Compare currents
fig, ax = plt.subplots()
ax: Axes = ax
nBar = 0
line_i = ax.plot(
    results["time"],
    results["current"]["bars"][:, nBar],
    marker=".",
    label=resId,
)

resfile = os.path.join(
    ROOT_DIR,
    r"workingDirectory\test_asm",
    "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
    "blockedRotor_50Hz_80Periods_128Steps_R_dyn_thers_100A",
    "I_bar_1.dat",
)
t_dyn, I_bar_dyn1 = read_timetable_dat(resfile)
line_i = ax.plot(
    t_dyn,
    I_bar_dyn1,
    marker="",
    label="Reset DC",
)
ax.legend()
ax.grid(alpha=0.5)
ax.set_title(f"Bar {nBar+1}")
ax.set_xlim(t[i_last_period], t[i_last_period + nbr_steps_per_period])
autoscale_y(ax)
ax.set_xlabel("time in s")
ax.set_ylabel("current in A")

# %%
logging.shutdown()
