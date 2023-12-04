"""init of script module"""

import json
import warnings
from os.path import dirname, join
from types import SimpleNamespace
from typing import Dict
from ..version import __version__, sha

colorDict = {}
try:
    with open(
        join(dirname(__file__), "default_color_dict.json"), "r", encoding="utf-8"
    ) as infile:
        colorDict: Dict[str, str] = json.load(infile)
except Exception:
    warnings.warn("Color Dict could not be imported...")

# define default parameters in parameter dict
default_param_dict = {"GEO": {}, "SYM": {}, "MAT": {}}
"""Default Script parameters dict, looks like:
    {\n
        "GEO": {\n
            "SYMMETRY_FACTOR": 1,\n
            "L_AX_R": 1.0,\n
            "L_AX_S": 1.0,\n
            "NBR_POLE_PAIRS": 4,\n
            "NBR_SLOTS": 12,\n
            "NBR_TURNS_IN_FACE": 20,\n
            "R_AIRGAP": 0.1,\n
        }, \n
        "SYM": {\n
            "INIT_ROTOR_POS": 0.0,\n
            "ANGLE_INCREMENT": 0.5,\n
            "FINAL_ROTOR_POS": 90.0,\n
            "Id_eff": 0,\n
            "Iq_eff": 1,\n
            "FLAG_NL": 1,\n
            "SPEED_RPM": 1000,\n
            "PATH_RES": "",\n
            "ParkAngOffset": None,  # optional\n
            "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient\n
            "FLAG_CHANGE_ROT_DIR": 0,\n
            "NBR_PARALLEL_PATHS": 1,\n
            "CALC_MAGNET_LOSSES": 0,\n
        }, \n
        "MAT": {\n
            "VALUE_DENSITY_LAM": 7800,\n
            "TEMP_MAG": 20,\n
        }\n
    } 
"""
default_param_dict["GEO"] ={
        "SYMMETRY_FACTOR": 1,
        "L_AX_R": 1.0,
        "L_AX_S": 1.0,
        "NBR_POLE_PAIRS": 4,
        "NBR_SLOTS": 12,
        "NBR_TURNS_IN_FACE": 20,
        "R_AIRGAP": 0.1,
    }
default_param_dict["SYM"] = {
        "INIT_ROTOR_POS": 0.0,
        "ANGLE_INCREMENT": 0.5,
        "FINAL_ROTOR_POS": 90.0,
        "Id_eff": 0,
        "Iq_eff": 1,
        "FLAG_NL": 1,
        "SPEED_RPM": 1000,
        "PATH_RES": "",
        "ParkAngOffset": None,  # optional
        "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient
        "FLAG_CHANGE_ROT_DIR": 0,
        "NBR_PARALLEL_PATHS": 1,
        "CALC_MAGNET_LOSSES": 0,
    }
default_param_dict["MAT"] = {
        "VALUE_DENSITY_LAM": 7800,
        "TEMP_MAG": 20,
    }

boundaryDomainDict = {
    "primary": "Surf_cutA0",
    "slave": "Surf_cutA1",
}
# stator specific domains
statorDomainDict = {
    # "domainS": "",
    "domainC": "StatorC",
    "domainCC": "StatorCC",
    "mb_all": "Stator_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    "airGap": "Stator_Airgap",
    "limit": "Surf_Inf",
}
# rotor specific domains:
rotorDomainDict = {
    # "domainS": "",
    "domainM": "Rotor_Magnets",
    "domainC": "RotorC",
    "domainCC": "RotorCC",
    "mb_all": "Rotor_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    # "rotor_moving": "",
    "mb_Mbaux": "Rotor_Bnd_MBaux",
    "airGap": "Rotor_Airgap",
    "limit": "Surf_bn0",
}
# additional line for pyemmo version in geo and pro files
versionStr = f"// This script was created with pyemmo (Version {__version__}"
# if git module is available, sha is the commit hash. Then add that too
if sha:
    versionStr += f", git {sha[0:6]}"
versionStr += ")\n\n"  # finalize version string
