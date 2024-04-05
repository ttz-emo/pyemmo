#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""init of script module"""

import json
import warnings
from os.path import dirname, join
from typing import Dict
from ..version import __version__, sha

colorDict = {}
try:
    with open(
        join(dirname(__file__), "default_color_dict.json"),
        encoding="utf-8",
    ) as infile:
        colorDict: Dict[str, str] = json.load(infile)
except Exception:
    warnings.warn("Color Dict could not be imported...")

# Define domain names globally
DOMAIN_PRIMARY = "primary"
DOMAIN_SECONDARY = "slave"
DOMAIN_LIMIT = "limit"
DOMAIN_MOVINGBAND = "mb_all"
DOMAIN_MOVINGBAND_AUX = "mb_Mbaux"
DOMAIN_AIRGAP = "airGap"
DOMAIN_ROTOR = "rotor_moving"
DOMAIN_STRANDED = "domainS"
DOMAIN_MAGNET = "domainM"
DOMAIN_LAMINATION = "domainLam"
DOMAIN_BAR = "domainBar"
DOMAIN_CONDUCTING = "domainC"
DOMAIN_NON_CONDUCTING = "domainCC"
DOMAIN = "domain"
DOMAIN_NON_LINEAR = "domainNL"
DOMAIN_LINEAR = "domainL"

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
            "R_ENDRING_SEGMENT": 0.,\n
            "L_ENDRING_SEGMENT": 0.,\n
        }, \n
        "MAT": {\n
            "VALUE_DENSITY_LAM": 7800,\n
            "TEMP_MAG": 20,\n
        }\n
    }
"""
default_param_dict["GEO"] = {
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
    "R_ENDRING_SEGMENT": 0.0,
    "L_ENDRING_SEGMENT": 0.0,
}
default_param_dict["MAT"] = {
    "VALUE_DENSITY_LAM": 7800,
    "TEMP_MAG": 20,
}

# Translate Domain names from pyemmo -> GetDP template
# ONLY DOMAINS SPECIFIED HERE WILL BE CREATED!
boundaryDomainDict = {
    DOMAIN_PRIMARY: "Surf_cutA0",
    DOMAIN_SECONDARY: "Surf_cutA1",
}
# stator specific domains
statorDomainDict = {
    # "domainS": "",
    DOMAIN_CONDUCTING: "StatorC",
    DOMAIN_NON_CONDUCTING: "StatorCC",
    DOMAIN_MOVINGBAND: "Stator_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    DOMAIN_AIRGAP: "Stator_Airgap",
    DOMAIN_LIMIT: "Surf_Inf",
}
# rotor specific domains:
rotorDomainDict = {
    # "domainS": "",
    DOMAIN_MAGNET: "Rotor_Magnets",
    DOMAIN_BAR: "Rotor_Bars",
    DOMAIN_CONDUCTING: "RotorC",
    DOMAIN_NON_CONDUCTING: "RotorCC",
    DOMAIN_MOVINGBAND: "Rotor_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    # "rotor_moving": "",
    DOMAIN_MOVINGBAND_AUX: "Rotor_Bnd_MBaux",
    DOMAIN_AIRGAP: "Rotor_Airgap",
    DOMAIN_LIMIT: "Surf_bn0",
}

# GETDP_DOMAINS ={
#     DOMAIN_PRIMARY: "Surf_cutA0",
#     DOMAIN_SECONDARY: "Surf_cutA1",
#     # "domainS": "",
#     DOMAIN_CONDUCTING: "StatorC",
#     DOMAIN_NON_CONDUCTING: "StatorCC",
#     DOMAIN_MOVINGBAND: "Stator_Bnd_MB",
#     # "domain": "",
#     # "domainNL": "",
#     # "domainL": "",
#     DOMAIN_AIRGAP: "Stator_Airgap",
#     DOMAIN_LIMIT: "Surf_Inf",

#     # "domainS": "",
#     DOMAIN_MAGNET: "Rotor_Magnets",
#     DOMAIN_BAR: "Rotor_Bars",
#     DOMAIN_CONDUCTING: "RotorC",
#     DOMAIN_NON_CONDUCTING: "RotorCC",
#     DOMAIN_MOVINGBAND: "Rotor_Bnd_MB",
#     # "domain": "",
#     # "domainNL": "",
#     # "domainL": "",
#     # "rotor_moving": "",
#     DOMAIN_MOVINGBAND_AUX: "Rotor_Bnd_MBaux",
#     DOMAIN_AIRGAP: "Rotor_Airgap",
#     DOMAIN_LIMIT: "Surf_bn0",
# }
# additional line for pyemmo version in geo and pro files
versionStr = f"// This script was created with pyemmo (Version {__version__}"
# if git module is available, sha is the commit hash. Then add that too
if sha:
    versionStr += f", git {sha[0:6]}"
versionStr += ")\n\n"  # finalize version string
