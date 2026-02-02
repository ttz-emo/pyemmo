#
# Copyright (c) 2025 M. Schuler, TTZ-EMO,
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
# %%
"""This module allows an easy invoke of the json api by a tkinter file dialog!"""
from __future__ import annotations

import os
from os.path import join
from pyemmo.api.json.json import main
from pyemmo.api.json import (
    STATOR_LAM_IDEXT,
    STATOR_SLOT_IDEXT,
    STATOR_AIRGAP_IDEXT,
    ROTOR_LAM_IDEXT,
    ROTOR_MAG_IDEXT,
    ROTOR_AIRGAP_IDEXT,
)
from pyemmo.definitions import USER_DIR

stator_lam_dict = {
    "Name": "rotor core",
    "IdExt": "rotor lamination",
    "Lines": [...],
    "Material": {
        "name": "steel mat",
        "conductivity": 1.923076875e6,
        "relPermeability": 1000,
        "BHCurve": {"default": []},
        "density": 7680,
        "sheetThickness": 0.5e-3,
        "lossParams": [5000, 18e3, 0],
    },
    "Quantity": 4,
    "Meshsize": None,
}
from pyemmo.api.json.modelJSON import createAPISurf

surf = createAPISurf(stator_lam_dict)
fig = surf.plot(tag=True)
# %%
model_folder = join(USER_DIR, "scripted_machine")
param_file_path = join(model_folder, "param.json")
model_file_path = join(model_folder, "geometry.json")
# run json api to create ONELAB Model
pyemmo_script = main(
    geo=model_file_path,
    extInfo=param_file_path,
    model=model_folder,
    gmsh="",
    getdp="",
    results="",
)

# %%
