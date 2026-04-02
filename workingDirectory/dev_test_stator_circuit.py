#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""Test stator voltage input"""
from __future__ import annotations

import datetime
import json
import logging

# %%
import os
import time

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from pyemmo.functions.import_results import (
    read_RegionValue_dat,
    read_timetable_dat,
)
from pyemmo.functions.run_onelab import run_simulation

MODEL_NAME = "IPMSM_Muster_1"
MODEL_DIR = r"D:\pyemmo\Results\pyleecanAPI\prius_debug"


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

p = 4
U_eff = 50
n = 750
f_s = p * n / 60
T_s = 1 / f_s
nbr_stator_periods = 3
nbr_sect = 2048 / 2  # Bandsegmentierung
multi = 2  # Default=4 number of Segments per timestep
timestep = T_s / 40
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbr_steps = T_s / timestep * nbr_stator_periods
logging.info("Simulation should execute %i time steps.", int(nbr_steps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbr_steps) * timestep)
# %%
resId = f"{U_eff}V_{n}rpm_{nbr_stator_periods}Periods"
paramDict = {
    "getdp": {
        "RPM": float(n),
        "nbrStatorPeriods": nbr_stator_periods,
        "initrotor_pos": 0.0,
        "d_theta": winkelschritt,
        "finalrotor_pos": winkelschritt * nbr_steps,
        "Flag_SrcType_Stator": 2,  # 1:current source, 2:voltage source, 0:CEMF (not available yet)
        "CircuitConnection": 0,  # 0:Star, 1:Delta
        "VV": U_eff * np.sqrt(2),  # voltage amplitude
        "pA_deg": -10.0,  # phase offset for source with Sin
        "ResId": resId,
        "Flag_AnalysisType": 1,
        "Flag_PrintFields": 0,
        "Flag_Debug": 1,
        "Flag_ClearResults": 1,
        "verbosity level": 3,
        # "AxialLength_R": 1,
        # "AxialLength_S": 1,
        "NbrParallelPaths": 1,
        # "R_endring_segment": 16e-7 / 2,  # Initial value: 16e-7,
        # "L_endring_segment": 2e-9 / 2,
        # "Flag_Cir_RotorCage": 0,
        # "Flag_Calculate_VW": 1,
        "msh": os.path.join(MODEL_DIR, "default.msh"),
        # "Flag_SecondOrder": 0,
    },
    "ResId": resId,
    "pro": os.path.join(MODEL_DIR, MODEL_NAME + ".pro"),
    "res": os.path.join(MODEL_DIR, f"res_{MODEL_NAME}"),
    "exe": r"getdp.exe",
    "gmsh": r"gmsh.exe",
    # TODO: Extend gmsh element to dict with parameters, like:
    # "gmsh": {
    #     "exe": "gmsh.exe",
    #     "gmsf": 2,  # global mesh size factor
    #     "NbrMbSegments": Nbr_Sect,  # Number of moving band mesh elements
    # },
    # "hyst": 0, # 172.04,
    # "eddy": 0, # 1.0472,
    # "exc": 0,
    # "axLen": 0.2,
    # "sym": 4,
    "info": "",
    "datetime": time.ctime(),
    "PostOp": [],
}

results = run_simulation(paramDict)
stop = time.perf_counter()
sim_duration = stop - start
logging.info("Simulation took %s", str(datetime.timedelta(seconds=sim_duration)))
if sim_duration > 1:
    results["simlation_duration"] = sim_duration
# %%
# cmd command is:
# gmsh.exe D:\pyemmo\Results\pyleecanAPI\prius_debug\IPMSM_Muster_1.geo -run  -v 3  &&
# getdp.exe D:\pyemmo\Results\pyleecanAPI\prius_debug\IPMSM_Muster_1.pro
# -solve Analysis
# -v 3
# -setnumber RPM 750.0
# -setnumber nbrStatorPeriods 3
# -setnumber initrotor_pos 0.0
# -setnumber d_theta 0.703125
# -setnumber finalrotor_pos 135.0
# -setnumber VV 169.7056274847714
# -setstring ResId 120V_750rpm_3Periods
# -setnumber Flag_AnalysisType 1
# -setnumber Flag_PrintFields 0
# -setnumber Flag_Debug 1
# -setnumber Flag_ClearResults 1
# -setnumber NbrParallelPaths 1
# -setstring ResPath D:\pyemmo\Results\pyleecanAPI\prius_debug\res_IPMSM_Muster_1

# %%
out_dict = paramDict.copy()
out_dict.update(results)
with open(
    os.path.join(paramDict["res"], resId, f"{resId}.json"),
    "w",
    encoding="utf-8",
) as jFile:
    json.dump(out_dict, jFile, indent=4, cls=NumpyEncoder)

respath = os.path.join(paramDict["res"], resId)

try:
    if "voltage" not in results:
        results["voltage"] = {}
    for phase in "abc":
        _, results["voltage"][phase] = read_timetable_dat(
            os.path.join(respath, f"U{phase}.dat")
        )
        _, results["voltage"][phase + "_L"] = read_timetable_dat(
            os.path.join(respath, f"U{phase}_w.dat")
        )
        _, results["current"][phase + "_L"] = read_timetable_dat(
            os.path.join(respath, f"I{phase}_w.dat")
        )
except:
    pass
# %%
# Show voltages in stator circuit
fig, ax = plt.subplots()
ax: Axes = ax
for phase in "abc":
    ax.plot(results["time"], results["voltage"][phase], label=f"Input Voltage {phase}")
# extra loop to have results in order
for phase in "abc":
    ax.plot(results["time"], results["voltage"][phase + "_L"], label=f"U_L,{phase}")
ax.set_ylabel("Spannung in V")
ax.grid(True)
ax.legend()
ax.set_xlim([results["time"][-1] - T_s, results["time"][-1]])

# %%
# show input and line currents
try:
    fig, ax = plt.subplots()
    for phase in "abc":
        ax.plot(results["time"], results["current"][phase], label=phase)
    for phase in "abc":
        ax.plot(
            results["time"],
            results["current"][phase + "_L"],
            label=phase + " line",
            linestyle="--",
        )
    ax.set_ylabel("phase current in A")
    ax.set_xlabel("time in s")
    ax.grid(True)
    ax.legend(loc=2)
except Exception as e:
    logging.error(e)
# %%
# compare input voltage and input current
fig, ax = plt.subplots()
ax: Axes = ax
axi: Axes = ax.twinx()
for phase in "abc":
    ax.plot(results["time"], results["voltage"][phase], label=f"U_{phase}")
    # ax.plot(results["time"], results["voltage"][phase], label=f"U_L,{phase}")

    axi.plot(results["time"], results["current"][phase], label=f"I_{phase}")

for a in (ax, axi):
    a.set_xlim([results["time"][-1] - T_s, results["time"][-1]])
ax.grid(True)
ax.set_ylabel("Spannung in V")
ax.legend(loc=1)

axi.set_ylabel("Strom in A")
axi.legend(loc=2)

# %%
# compare line voltage and line current
fig, ax = plt.subplots()
ax: Axes = ax
axi: Axes = ax.twinx()
for phase in "abc":
    ax.plot(results["time"], results["voltage"][phase + "_L"], label=f"U_{phase},L")
    # ax.plot(results["time"], results["voltage"][phase], label=f"U_L,{phase}")

    axi.plot(
        results["time"],
        results["current"][phase + "_L"],
        label=f"I_{phase},L",
        linestyle="--",
    )
for a in (ax, axi):
    a.set_xlim([results["time"][-1] - T_s, results["time"][-1]])
ax.grid(True)
ax.set_ylabel("Spannung in V")
ax.legend(loc=1)

axi.set_ylabel("Strom in A")
axi.legend(loc=2)

# %%

# %%
# Show induced voltage in stator phases
fig, ax = plt.subplots()
ax: Axes = ax
# for phase in 'ABC':
line_u = ax.plot(results["time"], results["inducedVoltage"]["A"], label="U_iA")
line_u = ax.plot(results["time"], results["inducedVoltage"]["B"], label="U_iB")
line_u = ax.plot(results["time"], results["inducedVoltage"]["C"], label="U_iC")
# ax.set_ylabel("Spannung in V")
# ax.set_xlim(14.5, 15)
ax.legend()
# ax.set_ylim(-1e-5,1e-5)
ax.grid(True)

# %%
try:
    # plot currents
    fig, ax = plt.subplots()
    ax.plot(results["time"], results["flux"]["a"], label="a")
    ax.plot(results["time"], results["flux"]["b"], label="b")
    ax.plot(results["time"], results["flux"]["c"], label="c")
    ax.plot(results["time"], results["flux"]["d"], label="d")
    ax.plot(results["time"], results["flux"]["q"], label="q")
    ax.set_ylabel("flux in Wb")
    ax.set_xlabel("time in s")
    ax.grid(True)
    ax.legend()
except Exception as e:
    logging.error(e)


# %%
# Plot Drehmoment
fig, ax = plt.subplots()
ax: Axes = ax
if os.path.isfile(os.path.join(respath, "Ts_vw.dat")):
    t_t, ts_vw = read_RegionValue_dat(os.path.join(respath, "Ts_vw.dat"))
    _, tr_vw = read_RegionValue_dat(os.path.join(respath, "Tr_vw.dat"))
    ax.plot(t_t, np.mean([ts_vw, tr_vw], axis=0), label="VW")

ax.plot(
    results["time"],
    results["torque"],
    ".-",
    label="MST",
)
ax.legend(loc=1)
ax.set_title("Drehmoment")
ax.grid(True)

# %%
logging.shutdown()
# %% FINAL
