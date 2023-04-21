"""This script creates a mind map of the pyemmo package structure"""
#%%
import os
import io
import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

WORKING_DIR = os.path.dirname(__file__)
mindFile = os.path.join(WORKING_DIR, "testMind.png")

## start mind map definiton with pydot
graph = pydot.Dot(graph_type="graph", rankdir="UD")

# add first layer of package structure 
root = "pyemmo"
geoPkg = "geometry"
packages = ["api", "functions", geoPkg , "script", "material"]
for package in packages:
    edge = pydot.Edge(root, package)
    graph.add_edge(edge)
    
## add second layer(s):
# geomety subpackage structure
geoSubPkgs = ["physicals", "tranformables", "toolkit"]
for package in geoSubPkgs:
    edge = pydot.Edge(geoPkg, package)
    graph.add_edge(edge)
## Create formatted output string in bytes format
png_str = graph.create(format="png")

# treat the DOT output as an image file
sio = io.BytesIO()
sio.write(png_str)
sio.seek(0)
img = mpimg.imread(sio)

# plot the image
imgplot = plt.imshow(img, aspect="equal")
plt.show()

#
# graph.write(mindFile, format='png')
# os.startfile(mindFile)

# %%
