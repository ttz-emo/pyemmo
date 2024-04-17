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

# %%
from os import path
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import createCmdCommand, findGetDP, findGmsh

# %% testfiles
scriptName = "TTZ_1FE1051-4HF11_TherCom"
testScriptPath = path.abspath(
    path.join(ROOT_DIR, "workingDirectory", "dummyScripts", scriptName)
)
testProFile = path.abspath(path.join(testScriptPath, scriptName + ".pro"))
# %% create cmd command
myCommand = createCmdCommand(
    onelabFile=testProFile,
    useGUI=False,
    gmshPath=findGmsh(),
    getdpPath=findGetDP(),
    paramDict={"finalrotor_pos": 10},
    postOperations=["GetBOnRadius", "Torque"],
)
print("\n\n" + myCommand)
# %%
