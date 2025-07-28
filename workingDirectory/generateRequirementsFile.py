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
"""Module to return requirements of pyemmo via pipreqs"""
from __future__ import annotations

import os
import subprocess
from os.path import join

from pyemmo.definitions import ROOT_DIR

pyemmo_DIR = os.path.join(ROOT_DIR, "pyemmo")

subprocess.run(f"pipreqs {pyemmo_DIR} --force")

try:
    with open(join(pyemmo_DIR, "requirements.txt"), encoding="utf-8") as reqFile:
        reqs = reqFile.readlines()
    print("\nRequired packages are:\n")
    for req in reqs:
        print(req, end=None)
except FileNotFoundError:
    print(f"Requirements file '{pyemmo_DIR}' not found!")
except Exception as exce:
    raise exce
