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
import os
from os.path import abspath, dirname, isfile, join, isdir

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
# from pyemmo.script.script import Script
# from pyemmo.script.geometry.primaryLine import PrimaryLine
# from pyemmo.script.geometry.slaveLine import SlaveLine
# from pyemmo.script.geometry.limitLine import LimitLine
# from pyemmo.script.geometry.rotor import Rotor
# from pyemmo.script.geometry.stator import Stator
# from pyemmo.script.geometry.machineAllType import MachineAllType
from pyemmo.api.json.json import main
from pyemmo.functions.runOnelab import findGmsh
from pyemmo.definitions import TEST_DIR, ROOT_DIR

# import subprocess
# from matplotlib import pyplot as plt
# import gmsh

# %%
# try to find gmsh in system path
gmshExe = findGmsh()
print(f'gmsh exe is "{gmshExe}"')

workingDir = abspath(join(ROOT_DIR, "Results", "Test_API_JSON"))
if not isdir(workingDir):
    os.mkdir(workingDir)
modelFileDir = join(workingDir, "model_files")
if not isdir(modelFileDir):
    os.mkdir(modelFileDir)
geoJsonFile = join(
    TEST_DIR, "data", "reluctance_json", "reluctance_machine.json"
)
infoJsonFile = join(
    TEST_DIR, "data", "reluctance_json", "reluctance_info.json"
)
assert os.path.isfile(geoJsonFile)
assert os.path.isfile(infoJsonFile)
# %% NEW API ALGO
# check if json files exist
if isfile(geoJsonFile) and isfile(infoJsonFile):
    # call main with file path:
    main(geoJsonFile, infoJsonFile, modelFileDir)

#     # load json as dict and call main with dict
#     with open(geoJsonFile, "r", encoding="utf-8") as jf:
#         geoDictList = json.load(jf)
#     with open(infoJsonFile, "r", encoding="utf-8") as jf:
#         infoDict = json.load(jf)
#     main(geoDictList, infoDict, modelFileDir)
else:
    raise (
        FileNotFoundError(
            f"Given json file(s) did not exist! Check '{geoJsonFile}' or '{infoJsonFile}'."
        )
    )

# %%
