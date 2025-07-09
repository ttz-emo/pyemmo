#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

import logging

import numpy as np
from matplotlib import pyplot as plt

from pyemmo.definitions import RESULT_DIR
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from pyemmo.script.script import Script

# %%


logging.getLogger().setLevel(logging.DEBUG)

C = Point("center point", 0, 0, 0, 0.3)
P1 = Point("point 1", 1, 0, 0, 0.3)
P2 = Point("point 2", -1, 0, 0, 0.3)
circArc = CircleArc("circle arc 1", P1, C, P2)
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_aspect("equal")
C.plot(fig)
P1.plot(fig)
P2.plot(fig)
print(circArc.getAnglesToX())
print(f"Radius: {circArc.radius}.")
print(f"Angle: {circArc.getAngle(inDeg=True)}.")
circArc.plot(fig)

# %%
angle = np.deg2rad(190)
P3 = Point("point 3", 1, 0, 0, 0.3)
P4 = Point("point 4", np.cos(angle), np.sin(angle), 0, 0.3)
circArc = CircleArc("circle arc 1", P3, C, P4)
print(f"Radius: {circArc.radius}.")
print(f"Angle: {circArc.getAngle(inDeg=True)}.")
circArc.plot(fig)
# %%

test_arc_script = Script("TestCircleArc", RESULT_DIR, {})
circArc.addToScript(test_arc_script)

test_arc_script.writeGeo()
import subprocess

subprocess.run("gmsh " + test_arc_script.geoFilePath)

# %%
