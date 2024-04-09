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

# %% Imports
from sys import path
from os.path import abspath, dirname, isfile, join
import json

# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = (
        "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    )
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
# from pyemmo.script.script import Script
# from pyemmo.script.geometry.primaryLine import PrimaryLine
# from pyemmo.script.geometry.slaveLine import SlaveLine
# from pyemmo.script.geometry.limitLine import LimitLine
# from pyemmo.script.geometry.rotor import Rotor
# from pyemmo.script.geometry.stator import Stator
# from pyemmo.script.geometry.machineAllType import MachineAllType
import pyemmo.api.json.json as api
from pyemmo.functions.runOnelab import findGmsh

# import subprocess
# from matplotlib import pyplot as plt
# import gmsh

# %%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')

workingDir = abspath(join(rootname, "Results", "Test_API_JSON"))
modelFileDir = join(workingDir, "model_files")
geoJsonFile = join(workingDir, "test_API_geometry.json")
infoJsonFile = join(workingDir, "test_API_simuInfo.json")
# %% NEW API ALGO
# check if json files exist
if isfile(geoJsonFile) and isfile(infoJsonFile):
    # call main
    # load json as dict and call main with dict
    with open(infoJsonFile, encoding="utf-8") as jf:
        infoDict = json.load(jf)

    api.main(geoJsonFile, infoJsonFile, modelFileDir)

else:
    raise (
        FileNotFoundError(
            f"Given json file(s) did not exist! Check '{geoJsonFile}' or '{infoJsonFile}'."
        )
    )

# %%
