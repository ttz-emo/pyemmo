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

from __future__ import annotations

# %%
import subprocess

from pyemmo.definitions import RESULT_DIR
from pyemmo.functions.runOnelab import createCmdCommand
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.spline import Spline
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.script import Script

# %%
myScript = Script("testGEO", scriptPath=RESULT_DIR, simuParams={})
p1 = Point("p1", 1, 0, 0, 0.1)
p2 = Point("p2", 2, 0, 0, 0.1)
p3 = Point("p3", 2, 1, 0, 0.1)
p4 = Point("p4", 1, 1, 0, 0.1)

p5 = Point("p5", 2, 1, 0, 0.1)
p6 = Point("p6", 1, 1, 0, 0.1)
p7 = Point("p7", 2, 2, 0, 0.1)
p8 = Point("p8", 1, 2, 0, 0.1)

l1 = Line("l1", p1, p2)
l2 = Line("l2", p2, p3)
l3 = Line("l3", p3, p4)
l4 = Line("l4", p4, p1)

l5 = Line("l5", p5, p6)
l6 = Line("l6", p6, p8)
l7 = Line("l7", p8, p7)
l8 = Line("l8", p7, p5)

s1 = Surface("s1", [l1, l2, l3, l4])
s2 = Surface("s2", [l5, l6, l7, l8])

s1.addToScript(myScript)
s2.addToScript(myScript)

# %% sort lines by center
curveList = s1.curve.copy()
curveDict = {}
for c in curveList:
    print(c.middle_point().radius, c.name)
# print(curveDict)
for key in sorted(curveDict):
    print(key, curveDict[key])
# %%
# add spline
spline = Spline("spline", p1, p3, [p2, p4], spline_type=0)
spline.addControlPoint(p8, 1)

# %%
spline.addToScript(myScript)

myScript.generateScript(mode=1)  # only geo file
subprocess.run(
    createCmdCommand(onelabFile=myScript.geoFilePath, useGUI=True), check=False
)
