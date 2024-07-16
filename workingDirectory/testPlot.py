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
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.spline import Spline
from pyemmo.script.geometry.surface import Surface

P1 = Point("P1", 0, 0, 0, 1)
# make sure point is plotted even though no fig is given
P1.plot(tag=True)
# %%
P2 = Point("P2", 1, 0, 0, 1)
P3 = Point("P3", 1, 1.75, 0, 1)
P4 = Point("P4", 0, 1, 0, 1)
L1 = Line("L1", P1, P2)
L1.plot(marker="o", tag=True)
# %%
C1 = CircleArc("Circ1", P2, P1, P4)
C1.plot(tag=True, marker="o")
# %%
L2 = Line("L2", P2, P3)
L3 = Line("L3", P3, P4)
L4 = Line("L4", P4, P1)
S1 = Surface("S1", [L1, L3, L2, L4])
S1.plot(tag=True)
# %%
S1.rotateZ(P1, np.pi / 4)
fig, ax = plt.subplots()
ax: Axes = ax
ax.set_aspect("equal", adjustable="box")
for i in range(4):
    S1.rotateZ(P1, i * np.pi / 2)  # rotate 90° to check plot
    C1 = CircleArc(name="Arc1", startPoint=P2, centerPoint=P1, endPoint=P4)
    # diameter = C1.getRadius()*2
    # theta1, theta2 = C1.getAnglesToX(flag_deg=True)
    # arc = Arc(xy=(0,0),width=diameter,height=diameter,angle=0, theta1=theta1, theta2=theta2)
    # ax=fig.add_subplot(1,1,1)
    # ax.add_patch(arc)
    C1.plot(fig, tag=True)
    fig.axes[0].set(xlim=(-2, 2), ylim=(-2, 2))
plt.show()
# %%

curves: List[Line] = S1.curve
points: List[Point] = []
for curve in curves:
    startPoint = curve.startPoint
    endPoint = curve.endPoint
    # startCoords=startPoint.getCoordinate()
    # endCoords = endPoint.getCoordinate()
    # plt.plot([startCoords[0], endCoords[0]], [startCoords[1],endCoords[1]])
    # curve.plot()
    # only get startpoint because startpoint is also endpoint of other line
    points.append(startPoint)
# %%
fig, ax = plt.subplots(figsize=(4, 4))
S2 = Surface("S2", [L1, C1, L4])
S2.plot(fig)

# %%
# TEST Center of gravity
x = []
y = []
z = []
for p in points:
    coords = p.coordinate
    print(coords)
    x.append(coords[0])
    y.append(coords[1])
    z.append(coords[2])

print([np.mean(x), np.mean(y), np.mean(z)])
plt.plot(x, y, "bo")
plt.plot(np.mean(x), np.mean(y), color="green", marker="x", markersize=12)
plt.show()
# %%
# TEST PATCH
from matplotlib import patches

fig, ax = plt.subplots()
xy_point_list = []
for point in S2.points:
    xyz = point.coordinate
    xy_point_list.append((xyz[0], xyz[1]))
polygon = patches.Polygon(xy_point_list, facecolor="b", edgecolor="m")
ax.add_patch(polygon)
ax.axis("equal")
S2.plot(fig)
fig.show()

# We can see that this leeds to an error because the arc segments need to be
# discretized into several points...

# %%
# Dev Spline plot
from splines import Bernstein

control_points = np.array([[(0, 0), (1, 0), (1, 1), (2, 1)]])

s = Bernstein(control_points)
times = np.linspace(s.grid[0], s.grid[-1], 100)
fig, ax = plt.subplots()
for segment in control_points:
    xy = np.transpose(segment)
    ax.plot(*xy, "--")
    ax.scatter(*xy, color="grey")
xy_point_list = s.evaluate(times).T  # shape (2,100) -> (xy, index)
# ax.add_patch(
#     patches.Polygon(
#         xy_point_list.T, edgecolor="m", fill=0, closed=False
#     )
# )
ax.plot(*xy_point_list, "--")  # Equivalent to ax.plot(x_values, y_values, "--")
ax.axis("equal")

# %%
# TEST SPLINE PLOT
fig, ax = plt.subplots()
colorList = ("blue", "red", "green")
spline_type_list = ("Catmull-Rom Spline", "Bezierkurve", "Basis-Spline")
for spline_type in (0, 1, 2):
    points = S1.points
    my_spline = Spline(
        name=spline_type_list[spline_type],
        startPoint=points.pop(0),
        endPoint=points.pop(),
        controlPoints=points,
        SplineType=spline_type,
    )
    my_spline.plot(
        fig=fig,
        color=colorList[spline_type],
        linewidth=1,
        marker=".",
        markersize=7,
        tag=True,
    )

# %%
