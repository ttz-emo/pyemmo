"""Script to run ASM simulation"""

# %%
# %matplotlib widget
import datetime
import json
import logging
import os
import time

import numpy as np
from definitions import MODEL_DIR, MODEL_NAME

from pyemmo.functions.import_results import (
    read_timetable_dat,
)
from pyemmo.functions.runOnelab import runCalcforCurrent


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

f_r = 4
I_eff = 50
n = 1000
f_s = f_r + 2 * n / 60
T_s = 1 / f_s
nbr_stator_periods = 3
nbr_steps_per_period = 128  # only needed in case n = 0
# Zum Abgleich mit Maxwell
Nbr_Sect = 2048  # Bandsegmentierung
multi = 8  # Default=4 number of Segments per timestep
timestep = (60 / (n * Nbr_Sect / multi)) if n > 0 else T_s / nbr_steps_per_period
winkelschritt = n / 60 * 360 * timestep  # Default: 0.703125
nbr_timesteps = T_s / timestep * nbr_stator_periods

flag_dynamic_resistance = False
thers = 100  # Thershold for bar resistance reset in A

logging.info("Simulation should execute %i time steps.", int(nbr_timesteps) + 1)
logging.debug("Timestep %e s.", timestep)
logging.debug("One time step equals %f° mechanical degrees.", winkelschritt)
logging.debug("Stop time of simulation: %.7e s", int(nbr_timesteps) * timestep)

# %%
# Add time stamp to simulation

resId = (
    time.strftime("%Y%m%d_%H%M", time.localtime())
    + f"_{I_eff}A_{n}rpm_{f_r}Hz_{nbr_stator_periods}Periods"
)
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
        "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
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
    "info": "",
    "datetime": time.ctime(),
    "PostOp": ["GetBOnRadius"],  # "GetBOnRadius" - "Get_LocalFields_Post"
}
sim_res_dir = os.path.join(paramDict["res"], resId)
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
            "Maybe simulation terminated. "
            "Checking time values..."
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
# Export Data for Maxwell
from pyemmo.functions.exportMaxwell import exportTabMaxwell

mxwl_export_dir = os.path.join(sim_res_dir, "export_maxwell")
if not os.path.isdir(mxwl_export_dir):
    os.mkdir(mxwl_export_dir)
# Export Bar Current
f_name_mxwl_export = os.path.join(mxwl_export_dir, "I_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    exportTabMaxwell(
        [out_dict["time"], results["current"]["bars"][:, 0]],
        identifier=["Time (s)", "I_Bar_Onelab (A)"],
        filepath=f_name_mxwl_export,
    )
# Export Bar Voltage
f_name_mxwl_export = os.path.join(mxwl_export_dir, "U_Bar_1.tab")
if not os.path.isfile(f_name_mxwl_export):
    resfile = os.path.join(sim_res_dir, "U_bars.dat")
    if os.path.isfile(resfile):
        t, U_bars = read_timetable_dat(resfile)
        exportTabMaxwell(
            [t, U_bars[:, 0]],
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

logging.shutdown()

#
