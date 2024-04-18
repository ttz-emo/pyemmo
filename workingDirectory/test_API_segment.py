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
from os.path import abspath, dirname, isdir, isfile, join, normpath, realpath
from typing import List

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
# %%
from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.script import Script
from pyemmo.api.json import *
from pyemmo.functions.runOnelab import findGmsh, createCmdCommand
import subprocess
from matplotlib import pyplot as plt
import gmsh

# %%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')
# pyemmoPath = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\Software_V2"
# rootname = pyemmoPath
# rootname = abspath(join(dirname(__file__), ".."))
# rootname = join(MAIN_DIR, "..")
geoFile = abspath(
    join(
        rootname,
        r"Results\matlab\TTZ_1FE1051-4HF11_TherCom\TTZ_1FE1051-4HF11_TherCom.json",
    )
)
while not isfile(geoFile):
    print("Could not find given json file. Please enter path!")
    geoFile = str(input("Enter geometry file path:"))
    print("\n")

# %%
# get maschine surface list of segment
segSurfList = importMachineGeometry(geometryFile=geoFile)
# plot segment
from matplotlib import pyplot

fig, ax = pyplot.subplots()
ax.set_aspect("equal", adjustable="box")
fig.set_dpi(300)
for surf in segSurfList:
    surf.plot(fig=fig, color=[0, 0, 0])

# %% Import extended info
extInfoFile = abspath(
    join(rootname, r"Results\matlab\TTZ_1FE1051-4HF11_TherCom\simuInfo.json")
)
extendedInfo = importExtInfo(extInfoFile)
symFaktor = getSymFactor(extendedInfo)

# %% Test Segment export and cutting code
# SurfaceDict: Dict[str, Surface] = createSurfaceDict(segSurfList)

# # check if there are duplicated points in SurfaceDict
# # there should not be any!
# PointList: List[Point] = list()
# allPoints: List[Point] = list()
# for key in SurfaceDict.keys():
#     points = SurfaceDict[key].getPoints()
#     for newPoint in points:
#         allPoints.append(newPoint)
#         if newPoint not in PointList:
#             flag_equal = False
#             for testPoint in PointList:
#                 if newPoint.isEqual(testPoint):
#                     flag_equal = True
#                     print(f"Point {newPoint.getName()} has the same coordinates as {testPoint.getName()}!")
#             if not flag_equal:
#                 PointList.append(newPoint)
#         else:
#             print(f"The point {newPoint.getName()} is allready in the point list.")

# %% generate script
# script without machine
segmentScript = Script(
    name="1FE1051-4HF11_TherCom_Segment",
    scriptPath=RESULT_DIR,
    simuParams=getSimuParams(extendedInfo),
    factory="openCascade",
)
for surf in segSurfList:
    segmentScript._addSurface(surf)
segmentScript.generateScript(mode=1)
# %%

command = createCmdCommand(
    onelabFile=join(
        segmentScript.getScriptPath(), segmentScript.getName() + ".geo"
    ),
    useGUI=True,
    gmshPath=gmshExe,
)
subprocess.run(
    command,
    shell=True,
)

# %%
