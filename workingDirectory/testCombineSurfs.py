#%%
from sys import path
from os.path import abspath, join, dirname
from numpy import deg2rad

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    # print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%%
import pyemmo as emmo
from pyemmo.definitions import RESULT_DIR
from pyemmo.script.script import Script
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.spline import Spline
from pyemmo.script.geometry.surface import Surface
from pyemmo.functions.runOnelab import createCmdCommand
from subprocess import run

#%%
myScript = Script("testGEO", scriptPath=RESULT_DIR, simuParams={})
pm = Point("p1", 0, 0, 0, 0.1)
p2 = Point("p2", 1, 0, 0, 0.1)
p3 = Point("p3", 1, 1, 0, 0.1)
p4 = Point("p4", 0, 1, 0, 0.1)

p7 = Point("p7", 1, 2, 0, 0.1)
p8 = Point("p8", 0, 2, 0, 0.1)

l1 = Line("l1", pm, p2)
l2 = Line("l2", p2, p3)
l3 = Line("l3", p3, p4)
l4 = Line("l4", p4, pm)

l5 = Line("l5", p3, p4)
l6 = Line("l6", p4, p8)
l7 = Line("l7", p8, p7)
l8 = Line("l8", p7, p3)

surf1 = Surface("s1", [l1, l2, l3, l4])
surf2 = Surface("s2", [l5, l6, l7, l8])
#%%
combinedSurf = surf1.combine(addSurf=surf2)
combinedSurf = combinedSurf.duplicate()
combinedSurf.translate(2, 0, 0)
#%%
p9 = p8.duplicate("p9")
p9.rotateZ(p7, deg2rad(-90))
circ1 = CircleArc("c1", startPoint=p8, centerPoint=p7, endPoint=p9)
# p10 = Point("p10",2,2,0,0.1)
p11 = Point("p11", 2, 3, 0, 0.1)
circ2 = CircleArc("c2", p7, p9, p11)
l9 = Line("l9", p9, p11)
l10 = l7.duplicate("l10")
surf3 = Surface("s3", [circ1, l9, circ2, l10])
surf3 = surf3.duplicate()
surf3.translate(2, 0, 0)
surf3.plot()
#%%
surf5 = combinedSurf.combine(surf3)
surf5 = surf5.duplicate()
surf5.translate(2, 0, 0)
#%%
surf1.addToScript(myScript)
surf2.addToScript(myScript)
combinedSurf.addToScript(myScript)
surf3.addToScript(myScript)
surf5.addToScript(myScript)
myScript.generateScript(mode=1)  # only geo file
run(createCmdCommand(onelabFile=myScript.getGeoFilePath(), useGUI=True))
#%%
myScript._resetGeometry()
r1 = 1
r2 = 1.2
rotAngle = deg2rad(45)
p1 = Point("p1", r1, 0, 0, 0.1)
p2 = Point("p2", r2, 0, 0, 0.1)
p3 = p1.duplicate()
p3.rotateZ(pm, rotAngle)
p4 = p2.duplicate()
p4.rotateZ(pm, rotAngle)
c1 = CircleArc("c1", p1, pm, p3)
l2 = Line("l2", p3, p4)
c3 = CircleArc("c3", p4, pm, p2)
l4 = Line("l4", p2, p1)
surf4 = Surface("s4", [c1, l2, c3, l4])
surf4.plot()
surf5 = surf4.duplicate()
surf5.rotateZ(pm, rotAngle)
surf5.plot()
surf6 = surf4.combine(surf5)
surf6.addToScript(myScript)
myScript.generateScript(mode=1)  # only geo file
run(createCmdCommand(onelabFile=myScript.getGeoFilePath(), useGUI=True))
#%%