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
from math import pi
from subprocess import run

from pyemmo.definitions import RESULT_DIR
from pyemmo.functions.run_onelab import createCmdCommand
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.spline import Spline
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.script import Script

pm = Point("p1", 0, 0, 0, 0.1)
# %% Airgap Band Surface recombination
nbrSegments = 8
nbrSegmentsInModel = 2
segmentAngle = 2 * pi / nbrSegments
rIn = 0.1
rOut = 0.15
p1 = Point("p1", rIn, 0, 0, 0.1)
p2 = Point("p2", rOut, 0, 0, 0.1)
p3 = p2.duplicate()
p3.rotateZ(pm, segmentAngle)
p4 = p1.duplicate()
p4.rotateZ(pm, segmentAngle)

p5 = p3.duplicate()
p5.rotateZ(pm, segmentAngle)
p6 = p4.duplicate()
p6.rotateZ(pm, segmentAngle)

p7 = p5.duplicate()
p7.rotateZ(pm, segmentAngle)
p8 = p6.duplicate()
p8.rotateZ(pm, segmentAngle)

l1 = Line("l1", p1, p2)
l2 = CircleArc("l2", p2, pm, p3)
l3 = CircleArc("l3", p3, pm, p5)
l31 = CircleArc("l3.1", p5, pm, p7)
l4 = Line("l4", p7, p8)
l51 = CircleArc("l5.1", p8, pm, p6)
l5 = CircleArc("l5", p6, pm, p4)
l6 = CircleArc("l6", p4, pm, p1)

surfSeg = Surface("Segment_1", [l1, l2, l3, l31, l4, l51, l5, l6])
surfSeg.plot()
# originalLoop = surfSeg.getCurve()
# newLoop: List[Union[Line, CircleArc, Spline]] = list()

# while originalLoop:
#     curve = originalLoop.pop()
#     newCurve = None
#     for otherCurve in originalLoop:
#         try:
#             newCurve = curve.combine(otherCurve)
#             break
#         except RuntimeError:
#             continue
#         except ValueError:
#             continue
#         except TypeError:
#             continue
#         except Exception as e:
#             raise(e)
#     if newCurve:
#         originalLoop.remove(otherCurve)
#         newLoop.append(newCurve)
#     else:
#         newLoop.append(curve)
# surfSeg.setCurve(newLoop)
# ... ->
surfSeg.recombineCurves()
surfSeg.setMeshLength(5e-3)
surfSeg.plot()
# %%
recombineScript = Script("testRecombineSurfs", scriptPath=RESULT_DIR, simuParams={})
surfSeg.addToScript(recombineScript)
recombineScript.generateScript(mode=1)  # only geo file
run(
    createCmdCommand(onelabFile=recombineScript.getGeoFilePath(), useGUI=True),
    check=True,
)

# %%
