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
import setPath
from pyemmo import Point, Line, Surface
import matplotlib.pyplot as plt

P1 = Point("P1", 0.11, 0.21, 0, 1)
P2 = Point("P2", 2, 0, 0, 1)
P3 = Point("P3", 1, 1.75, 0, 1)
P4 = Point("P4", 0, 0.75, 0, 1)
L1 = Line("L1", P1, P2)
L2 = Line("L2", P2, P3)
L3 = Line("L3", P3, P4)
L4 = Line("L4", P4, P1)
S1 = Surface("S1", [L1, L3, L2, L4])

curves = S1.getCurve()
points = list()
for curve in curves:
    startPoint = curve.getP1()
    points.append(
        startPoint
    )  # only get startpoint because startpoint is also endpoint of other line
x = list()
y = list()
z = list()
for p in points:
    coords = p.getCoordinate()
    print(coords)
    x.append(coords[0])
    y.append(coords[1])
    z.append(coords[2])
from numpy import mean

print([mean(x), mean(y), mean(z)])
plt.plot(x, y, "bo")
plt.plot(mean(x), mean(y), color="green", marker="x", markersize=12)
# %%
