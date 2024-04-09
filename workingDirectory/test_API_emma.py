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
from os.path import abspath, dirname, isdir, isfile, join, normpath, realpath
from sys import path

# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = (
        "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\pyemmo"
    )
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
# %%
from pyemmo.api import json as api
from pyemmo.functions.runOnelab import findGmsh

# %%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')

modelDir = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom"
geoJsonPath = abspath(
    join(
        modelDir,
        "Test_1FE1051-4HF11_TherCom.json",
    )
)
extInfoPath = abspath(
    join(
        modelDir,
        "simuInfo.json",
    )
)
# %%
api.main(geo=geoJsonPath, extInfo=extInfoPath, model=modelDir, gmsh=gmshExe)
