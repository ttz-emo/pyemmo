# %% Imports
from random import random
from typing import Dict, List, Union

from numpy import equal
from pyemmo.definitions import RESULT_DIR
from pyemmo.script.script import Script
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.material.material import Material
import pandas
import math
from os.path import join, abspath
import subprocess

# %% data import
defSimParamDict = {
    "init_rotor_pos": 0,
    "angle_increment": 1,
    "final_rotor_pos": 90,
    "Id_eff": 0,
    "Iq_eff": 0,
    "rot_speed": 1000,
    "park_angle_offset": 0,
    "analysis_type": 1,
    "magTemp": 20,
}
myScript = Script(name="csv_Geo", scriptPath=RESULT_DIR, simuParams=defSimParamDict)
fc_dir = (
    r"C:\Users\ganser\AppData\Local\Programs\pyemmo\workingDirectory\freecad"  # FreeCAD folder
)
csvFilename = "lineTable.csv"
myDataFrame = pandas.read_csv(abspath(join(fc_dir, csvFilename)))
mL = 1
mLBlech = 2e-2
mLMagnet = 1e-2
mLLuft = 0.7e-2
mLLuftspalt = 3e-3

# %% Material aus Datenbank laden
steel_1010 = Material()
steel_1010.loadMatFromDataBase("Material_new.db", "steel_1010")
ndFe35 = Material()
ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")
air = Material()
air.loadMatFromDataBase("Material_new.db", "air")

# %% Alle Rohdaten auslesen und pyemmo-Objekte erzeugen
surfDict: Dict[str, List[Union[Line, CircleArc]]] = {}
for i in range(0, len(myDataFrame)):
    startPoint = Point(
        "",
        float(myDataFrame["AnfP_x"][i]),
        float(myDataFrame["AnfP_y"][i]),
        float(myDataFrame["AnfP_z"][i]),
        mL,
    )
    endPoint = Point(
        "",
        float(myDataFrame["EndP_x"][i]),
        float(myDataFrame["EndP_y"][i]),
        float(myDataFrame["EndP_z"][i]),
        mL,
    )
    startPoint.name = f"p_{startPoint.id}"
    endPoint.name = f"p_{endPoint.id}"
    # Create Line from Points
    linetype: str = myDataFrame["Type"][i]
    if linetype == "Arc":
        centerPoint = Point(
            "",
            float(myDataFrame["RundP_x"][i]),
            float(myDataFrame["RundP_y"][i]),
            float(myDataFrame["RundP_z"][i]),
            mL,
        )
        centerPoint.name = "p_" + str(centerPoint.id)
        actLine = CircleArc("", startPoint, centerPoint, endPoint)
    elif linetype == "Line":
        actLine = Line("", startPoint, endPoint)
    else:
        msg = f"Unknown line type '{linetype}'"
        raise (TypeError(msg))
    # set Line name
    actLine.name = "l_" + str(actLine.id)

    # sort lines by surf name
    surfName = myDataFrame["Name"][i]
    if surfName in surfDict.keys():
        surfDict[surfName].append(actLine)
    else:
        surfDict[surfName] = [actLine]
# %% Line plot
from pyemmo.functions.plot import plot
from matplotlib import pyplot

fig, ax = pyplot.subplots()
for surfName, lineList in surfDict.items():
    plot(lineList, fig, tag=True)
ax.set_aspect("equal")
fig.suptitle("Lineplot")

# %% Surfaces erzeugen
surfList: List[Surface] = list()
for surfname, lineList in surfDict.items():
    actSurf = Surface(surfname, lineList)
    surfList.append(actSurf)

# %% Surface plot
from matplotlib.pyplot import text

fig, ax = pyplot.subplots()
for surf in surfList:
    color = [random() for i in range(3)]
    surf.plot(fig, color=color)
    centercoords = surf.calcCOG().getCoordinate()
    text(
        centercoords[0],
        centercoords[1],
        surf.name,
        fontsize=7,
        verticalalignment="center",
        horizontalalignment="center",
    )
ax.set_aspect("equal")
fig.suptitle("Surface Plot")

# %% Meshlänge zuweisen
for surf in surfList:
    surfName = surf.name
    if "Rotorblech" in surfname:
        surf.setMeshLength(mLBlech)
    elif "Magnet" in surfname:
        surf.setMeshLength(mLMagnet)
    elif "Luftspalt" in surfname:
        surf.setMeshLength(mLLuftspalt)
    elif "Luft" in surfname:
        surf.setMeshLength(mLLuft)
    else:
        print("Unknown surface name to set mesh length")

# %% Dummy Objekte zum befüllen
from pyemmo.script.geometry.rotorLamination import RotorLamination
from pyemmo.script.geometry.magnet import Magnet
from pyemmo.script.geometry.airGap import AirGap
from pyemmo.script.geometry.airArea import AirArea
from pyemmo.script.geometry.domain import Domain
from pyemmo.functions import runOnelab

allPhysical = []
for surf in surfList:
    if "Rotorblech" in surf.name:
        phyObject = RotorLamination(surf.name, [surf], steel_1010)
    elif "Magnet" in surf.name:
        if "North" in surf.name:
            phyObject = Magnet(surf.name, [surf], ndFe35, 1, "radial")
        elif "South" in surf.name:
            phyObject = Magnet(surf.name, [surf], ndFe35, -1, "radial")
        else:
            phyObject = Magnet(surf.name, [surf], ndFe35, 1, "radial")
    elif "Luftspalt" in surf.name:
        phyObject = AirGap(surf.name, [surf], air)
    elif "Luft" in surf.name:
        phyObject = AirArea(surf.name, [surf], air)
    allPhysical.append(phyObject)

domTest = Domain("domTest", allPhysical)
domTest.addToScript(myScript)
myScript.generateScript(mode=1)
# %% Run gmsh
command = runOnelab.createCmdCommand(myScript.getGeoFilePath(), useGUI=True)
subprocess.run(command)

# %%
