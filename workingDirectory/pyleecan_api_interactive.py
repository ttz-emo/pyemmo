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
"""This module allows an easy invoke of the pyleecan api by a tkinter file dialog!"""
from __future__ import annotations

import logging
import os
import tkinter as tk
from tkinter import filedialog

from pyleecan.Functions.load import load  # pylint: disable=no-name-in-module

from pyemmo.api.pyleecan.main import main
from pyemmo.definitions import RESULT_DIR
from pyemmo.functions.clean_name import clean_name

logging.basicConfig(level=logging.DEBUG)
root = tk.Tk()
root.withdraw()
motor_file = r""
if not motor_file:
    motor_file = filedialog.askopenfilename()

if os.path.isfile(motor_file):
    # resDir = os.path.dirname(model_folder)
    # run pyleecan api
    pyleecan_machine = load(motor_file)
    model_name = clean_name(pyleecan_machine.name) if pyleecan_machine.name else "test"
    pyemmo_script = main(
        motor_file,
        model_dir=os.path.join(RESULT_DIR, model_name),
    )
else:
    raise ValueError(f"Given path ({motor_file}) was not a valid model file!")

# %%
