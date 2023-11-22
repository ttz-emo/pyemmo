#%%
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
