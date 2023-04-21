# %%
from numpy import pi
from typing import List
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.surface import Surface

import matplotlib.pyplot as plt

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
#%%
S1.rotateZ(P1, pi / 4)
fig, ax = plt.subplots()
ax.set_aspect("equal", adjustable="box")
for i in range(4):
    S1.rotateZ(P1, i * pi / 2)  # rotate 90° to check plot
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

curves: List[Line] = S1.getCurve()
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
x = []
y = []
z = []
for p in points:
    coords = p.getCoordinate()
    print(coords)
    x.append(coords[0])
    y.append(coords[1])
    z.append(coords[2])
from numpy import mean, pi

print([mean(x), mean(y), mean(z)])
plt.plot(x, y, "bo")
plt.plot(mean(x), mean(y), color="green", marker="x", markersize=12)
plt.show()
# %%
