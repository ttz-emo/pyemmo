# %%
#
import os
from typing import List
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import scipy.interpolate as interp
from pyemmo.functions.import_results import read_timetable_dat

# from pyemmo.definitions import ROOT_DIR
from definitions import MODEL_DIR  # MODEL_NAME


def time_derivate(time: np.ndarray, values: np.ndarray) -> np.ndarray:
    # Calculate differences
    dt = np.diff(time)  # Differences in t
    dy = np.diff(values)  # Differences in y

    # Calculate the time derivative dy/dt
    dydt = dy / dt
    # Create an interpolation function
    interp_func = interp.interp1d(
        (time[:-1] + time[1:]) / 2, dydt, fill_value="extrapolate"
    )
    return interp_func(time)


def extract_axes(ax2: Axes):
    new_ax = ax2
    # Create a new figure and add the extracted axes to it
    fig2 = plt.figure()

    # Add the extracted axes to the new figure
    new_ax = fig2.add_axes(
        [0.1, 0.1, 0.8, 0.8]
    )  # [left, bottom, width, height] in normalized coordinates

    # Now copy the contents of the original ax2 to the new_ax
    for line in ax2.get_lines():
        new_ax.plot(
            line.get_xdata(),
            line.get_ydata(),
            label=line.get_label(),
            color=line.get_color(),
        )
    new_ax.set_title(ax2.get_title())
    new_ax.set_xlabel(ax2.get_xlabel())
    new_ax.set_ylabel(ax2.get_ylabel())
    new_ax.legend()
    return fig, new_ax


f_r = 50
I_eff = 50
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

# blockedRotor_50Hz_80Periods_128Steps_R_dyn2_thers_100A -> 20 A !!!
resId = "blockedRotor_50Hz_80Periods_128Steps_R_dyn2_thers_100A"
sim_res_dir = os.path.join(
    os.path.join(
        MODEL_DIR,
        "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
    ),
    resId,
)

R_bar_dc = 3.572345668067562e-05

# %%
# Import der Daten für einen spezifischen Stab
stab = 2
resfile = os.path.join(sim_res_dir, f"I_bar_{stab}.dat")
t, ibar = read_timetable_dat(resfile)
ibar = ibar[:, 0]
resfile = os.path.join(sim_res_dir, f"R_bar_{stab}.dat")
t_r, rbar = read_timetable_dat(resfile)
rbar = rbar[:, 0]

# Plot Stabstrom und Widerstand über den Zeitschritt (immer eine Periode)
fig, axes = plt.subplots(3, 1)
axes: List[Axes]
i_bar_rms_period = np.zeros(nbr_stator_periods)
r_bar_mean_period = np.zeros(nbr_stator_periods)
r_bar_i_max = np.zeros(nbr_stator_periods)
for period in range(nbr_stator_periods):
    # +1 because next period starts with new value
    i_start = (period * nbr_steps_per_period) + (0 if period == 0 else 1)
    i_stop = (period + 1) * nbr_steps_per_period
    i_bar_period = ibar[i_start:i_stop]
    i_bar_rms_period[period] = np.sqrt(np.mean(np.square(i_bar_period)))
    axes[0].plot(
        i_bar_period,
        label=f"Period {period}",
    )
    r_bar_period = rbar[i_start:i_stop]
    r_bar_mean_period[period] = np.mean(r_bar_period)
    r_bar_i_max[period] = r_bar_period[
        np.where(i_bar_period == np.max(i_bar_period))
    ]
    axes[1].plot(
        r_bar_period,
        label=f"Period {period}",
    )
    axes[2].plot(
        time_derivate(
            t_r[i_start:i_stop],
            r_bar_period,
        )
    )
axes[0].grid()
axes[0].set_title(f"Verlauf der Perioden (Stab {stab})")
axes[0].set_ylabel("Stabstrom")

axes[1].set_ylabel("Stabwiderstand")
axes[1].set_xlabel("Zeitschritt")
axes[1].grid()
res_ax = axes[1]
res_ax.set_ylim([0, 0.5e-3])

axes[2].grid()
lim = 0.1
axes[2].set_ylim([-lim, lim])

# %%
fig, axes = plt.subplots(3, 1)
for bar in range(1, 10):
    stab = bar
    resfile = os.path.join(sim_res_dir, f"I_bar_{stab}.dat")
    t, ibar = read_timetable_dat(resfile)
    ibar = ibar[:, 0]
    resfile = os.path.join(sim_res_dir, f"R_bar_{stab}.dat")
    t_r, rbar = read_timetable_dat(resfile)
    rbar = rbar[:, 0]
    for period in range(nbr_stator_periods):
        i_start = (period * nbr_steps_per_period) + (0 if period == 0 else 1)
        i_stop = (period + 1) * nbr_steps_per_period
        i_bar_period = ibar[i_start:i_stop]
        i_bar_rms_period[period] = np.sqrt(np.mean(np.square(i_bar_period)))

        r_bar_period = rbar[i_start:i_stop]
        r_bar_mean_period[period] = np.mean(r_bar_period)
        r_bar_i_max[period] = r_bar_period[
            np.where(i_bar_period == np.max(i_bar_period))
        ]
    axes[0].plot(i_bar_rms_period, "-", label=f"Stab {stab}")
    axes[1].plot(r_bar_mean_period, "-", label=f"Stab {stab}")
    ## Plot Mittleren Stabwiderstands des oben ausgewählten Stabs pro Periode
    axes[2].plot(r_bar_i_max, "-", label=f"Stab {stab}")
axes[0].grid()
axes[0].set_ylabel(r"$I_{\mathrm{eff,Periode}}$")
axes[0].set_xlabel("elek. Periode")

axes[1].set_yscale("log")
axes[1].grid()
axes[1].set_ylabel(r"$\overline{R_\mathrm{Stab}}$")
axes[1].set_xlabel("elek. Periode")

axes[2].grid()
axes[2].set_ylabel(r"$R_\mathrm{Stab}(I_\mathrm{max})$")
axes[2].set_xlabel("elek. Periode")
axes[2].set_yscale("log")


axes[0].legend(
    loc="upper center",
    bbox_to_anchor=(0.68, 1.4),
    ncol=3,
    fancybox=True,
    shadow=True,
)

# %% Extract derivative plot and have a closer look
fig, ax = extract_axes(axes[2])
ax.grid()
lim = 0.1
ax.set_ylim([-lim, lim])

# %%
# PLOT MEAN RESISTANCE OVER PERIOD
fig, ax = plt.subplots()
for stab in range(1, 10):
    resfile = os.path.join(sim_res_dir, f"R_bar_{stab}.dat")
    t, rbar = read_timetable_dat(resfile)
    r_bar_mean_period = np.zeros(nbr_stator_periods)
    for period in range(nbr_stator_periods):
        # +1 because next period starts with new value
        r_bar_period = rbar[
            (period * nbr_steps_per_period) : (
                (period + 1) * nbr_steps_per_period
            )
        ]
        r_bar_mean_period[period] = np.mean(r_bar_period)

    ax.plot(r_bar_mean_period, ".-", label=f"Stab {stab}")
    ax.set_ylabel(r"Mittlerer Stabwiderstand $\overline{R_{Stab}}$")
    ax.set_xlabel("elek. Periode")
ax.grid()
ax.legend()


# PLOT RMS OF BAR CURRENT OVER PERIOD
fig, ax = plt.subplots()
for stab in range(1, 10):
    resfile = os.path.join(sim_res_dir, f"I_bar_{stab}.dat")
    t, ibar = read_timetable_dat(resfile)
    i_bar_rms_period = np.zeros(nbr_stator_periods)
    for period in range(nbr_stator_periods):
        # +1 because next period starts with new value
        i_bar_period = ibar[
            (period * nbr_steps_per_period)
            + 1 : ((period + 1) * nbr_steps_per_period)
        ]
        i_bar_rms_period[period] = np.sqrt(np.mean(np.square(i_bar_period)))

    ax.plot(i_bar_rms_period, ".-", label=f"Stab {stab}")
    ax.set_ylabel("Stabstrom pro Periode in A(rms)")
    ax.set_xlabel("elek. Periode")
ax.grid()
ax.legend(loc="upper right")
# %%
