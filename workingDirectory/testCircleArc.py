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
from os.path import abspath, dirname, join
from sys import path
from matplotlib import pyplot as plt
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point

# try:
print(f"__file__ is {__file__}")
rootname = abspath(join(dirname(__file__), ".."))
# except:
#     rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
# print(f"Could not determine root. Setting it manually to '{rootname}'")
# print(f'rootname is "{rootname}"')

path.append(rootname)

C = Point("c", 1, 1, 0, 0.3)
P1 = Point("p1", 2, 1, 0, 0.3)
P2 = Point("p2", 0, 1, 0, 0.3)
circArc = CircleArc("ca1", P1, C, P2)
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
