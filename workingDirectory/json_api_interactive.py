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

import logging
import os
import re
import tkinter as tk
from tkinter import filedialog

from pyemmo.api.json import json

logger = logging.getLogger("pyemmo")
logger.setLevel(logging.DEBUG)

root = tk.Tk()
root.withdraw()
model_folder = r""
if not model_folder:
    model_folder = filedialog.askdirectory()

if os.path.isdir(model_folder):
    # resDir = os.path.dirname(model_folder)
    # get list of file from that folder that end with .json:
    file_list = [file for file in os.listdir(model_folder) if file.endswith(".json")]
    # extract parameter file path:
    param_file_path = ""
    for file in file_list:
        if re.match(r".*([sS]imu).*([iI]nfo).*(\.json)", file):
            param_file_name = file_list.pop(file_list.index(file))
            param_file_path = os.path.join(model_folder, param_file_name)
            break
    if not param_file_path:
        raise FileNotFoundError("No parameter file found in model folder!")
    # there should only be one json file left which is the model file
    assert len(file_list) == 1, "There are multiple or no model file in the folder!"
    model_file_name = file_list[0]
    model_file_path = os.path.join(model_folder, model_file_name)
    # run json api
    pyemmo_script = json.main(model_file_path, param_file_path, model=model_folder)
else:
    raise ValueError(f"Given path ({model_folder}) was not a valid model folder!")

# %%
