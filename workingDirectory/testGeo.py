#%%
from sys import path
from os.path import abspath, join, dirname

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\PyDraft"
    # print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%%
from pydraft.definitions import RESULT_DIR
from pydraft.script.script import Script
from pydraft.script.geometry.point import Point
from pydraft.script.geometry.line import Line
from pydraft.script.geometry.surface import Surface
from pydraft.functions.runOnelab import createCmdCommand
from subprocess import run

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
myScript.generateScript(mode=1)  # only geo file
run(createCmdCommand(onelabFile=myScript.getGeoFilePath(), useGUI=True))
