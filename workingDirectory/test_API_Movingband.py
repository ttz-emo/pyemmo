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

# %% Imports and stuff
from setPath import pathRes
import pyemmo as emmo
from pyemmo.api.json import *
from os.path import abspath, join


import subprocess

# %%
pyemmoPath = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\Software_V2"
rootname = pyemmoPath
# rootname = abspath(join(dirname(__file__), ".."))
myScript = emmo.Script("siemensTestMachine", pathRes)
Path2CSV = join(
    abspath(join(rootname, "..")), r"Siemens\Looplines_TTZMitLuftspalt\areaCSV"
)

dataFrameDict = getMachineDFDict(
    csvFilePath=Path2CSV
)  # get maschine dataframe
extendInfo = getDataFrameFromCSV(join(Path2CSV, "duplicationInformation.csv"))
MaschineSurfList = createMachineGeometryFromSegment(
    dataFrameDict, extendInfo.symmetriefaktor[0]
)
MaschineSurfaceDict = createSurfaceDict(dataFrameDict)
# %% Create the moving band lines and object
############ VERSION 1 ############
# find the airgap line
pinball = 1e-6
mbRadius = extendInfo.movingband_r[0]
symFaktor = extendInfo.symmetriefaktor[0]
lineCount = 0
mbLines = list()

# get the moving band lines
for key in MaschineSurfaceDict.keys():
    for line in MaschineSurfaceDict[key].getCurve():
        if (abs(line.getP1().calcDist() - mbRadius) < pinball) and (
            abs(line.getP2().calcDist() - mbRadius) < pinball
        ):
            lineCount += 1
            mbLines.append(line)
            nbrSegRotor = int(
                dataFrameDict[key].Quantity[0] / symFaktor
            )  # we made sure its the rotor mb line so this must be the number of rotor-segments
            angleRotor = dataFrameDict[key].Angle[0]
# print("There were ", str(lineCount), " inner movingband lines")
# print("There are ", str(nbrSegRotor), " rotor segments in model with symmetry ", symFaktor)
# duplicate to get all inner movingband lines
mbInLines = mbLines.copy()
for line in mbLines:
    for i in range(1, nbrSegRotor):
        mbLine = line.duplicate()
        mbLine.rotateZ(angle=i * angleRotor)
        mbInLines.append(mbLine)
# %% ############ VERSION 2 ############
mbLinesRotor = list()
mbLinesStator = list()
for surface in MaschineSurfList:
    for line in surface.getCurve():
        linename = line.getName()
        if "LuA" in linename and "LuM" in linename:
            surfaceName = surface.getName()
            # print("Found airgap line in Surface \"", surfaceName,":", linename)
            if (
                "LuR" in surfaceName or "RoLu" in surfaceName
            ):  # its the rotor moving band line
                mbLinesRotor.append(line)
            elif "StLu" in surfaceName:
                mbLinesStator.append(line)
# Ergebnis: Version 1 braucht 0.3s; Version 2 braucht 0.4s
# #%%
# MB_inner = pyd.MovingBand(
#     name="mbRotor_i",
#     geometricalElement=mbLinesRotor,
#     material=None,
#     auxiliary=False
# )
# Append MB_inner to RotorPhysicals

# # Generate Script with moving band lines (for testing)
# scriptName="TestMovinbandGeneration"
# TestMBScript = pyd.Script(scriptName, pathRes)
# mbInLines = mbLinesRotor+mbLinesStator
# for line in mbInLines:
#     line.addToScript(TestMBScript)
# MB_inner.addToScript(TestMBScript)
# TestMBScript.generateScript()
# subprocess.run([r'C:\Users\ganser\AppData\Local\Programs\gmsh-4.5.6-Windows64\gmsh.exe', join(rootname, r'resultDirectory\\'+scriptName+'.geo')], shell = True)

# #%% # Create auxiliary lines and movingband objects
# if symFaktor > 1: # only generate auxiliary movingband if there is symmetry
#     mbAuxLines = list()
#     MB_AuxList = list()
#     symAngle = 2*pi/symFaktor
#     # here order of for-loops had to be changed because for example for symFaktor=4 we need 3 auxiliary movingband (mb) objects, each containing the same number of lines as the inner mb
#     for i in range(1,symFaktor): # for every symmetry part
#         for line in mbInLines: # for every inner line
#             mbAuxLine = line.duplicate()
#             mbAuxLine.rotateZ(angle=(i*symAngle))
#             mbAuxLines.append(mbAuxLine)
#             ### TESTING
#             mbAuxLine.addToScript(TestMBScript) # add the line to the test script
#             ### TESTING
#         MB_AuxList.append(
#             pyd.MovingBand(
#                 name=("mbRotor_Aux_" + str(i)),
#                 geometricalElement=mbAuxLines.copy(), # copy list because is cleared for next iteration
#                 material=air,
#                 auxiliary=True
#             )
#         )
#         mbAuxLines.clear() # clear so the old lines are no longer in the list for the next moving band part
# #%% Stator Movingband lines and object


# # TESTING
# for MBAux in MB_AuxList:
#     MBAux.addToScript(TestMBScript)
# TestMBScript.generateScript() # generate test script with aux lines
# subprocess.run([r'C:\Users\ganser\AppData\Local\Programs\gmsh-4.5.6-Windows64\gmsh.exe', join(rootname, r'resultDirectory\\'+scriptName+'.geo')], shell = True)
