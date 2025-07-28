#
# Copyright (c) 2018-2024 M. Schuler & Vu Nguyen, TTZ-EMO,
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
"""TODO: Module docstring"""

from __future__ import annotations

import os
import subprocess
from datetime import datetime

"""
Script to run pytest in powershell and save summary to date-marked log
"""

log_path = f".\\integrationTest\\logs"
if not os.path.isdir(log_path):
    os.makedirs(log_path)
curr_date = datetime.now().strftime("%Y%m%d_%H%M%S")

subprocess.run(
    f"powershell.exe (pytest test_api_integration.py -rA --show-capture=stdout --show-progress -vvv ^| tee ./logs/test_summary_{curr_date}.log)"
)
