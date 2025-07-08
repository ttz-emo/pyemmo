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
"""This script creates a mind map of the pyemmo package structure"""

import io

# %%
import os

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pydot

# %%
WORKING_DIR = os.path.dirname(__file__)
mindFile = os.path.join(WORKING_DIR, "testMind.png")

## start mind map definiton with pydot
graph = pydot.Dot(graph_type="graph", rankdir="UD")

# add first layer of package structure
root = "pyemmo"
geoPkg = "geometry"
packages = ["api", "functions", geoPkg, "script", "material"]
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

# %% create GetDP template domain graph
graph = pydot.Dot(graph_type="graph", rankdir="UD")

DomainC = "DomainC"  #    : with massive conductors
DomainCC = "DomainCC"  #   : non-conducting domain
DomainM = "DomainM"  #    : with permanent magnets
DomainB = "DomainB"  #    : with inductors
DomainS = "DomainS"  #    : with imposed current density
DomainL = "DomainL"  #    : with linear permeability (no jacobian matrix)
DomainNL = "DomainNL"  #   : with nonlinear permeability (jacobian matrix)
DomainV = "DomainV"  #    : with additional vxb term
DomainKin = "DomainKin"  #  : region number for mechanical equation
DomainDummy = "DomainDummy"  # : region number for postpro with functions
DomainPlotMovingGeo = "DomainPlotMovingGeo"  # : region with boundary lines of geo for visualisation of moving rotor

# DomainC
RotorC = "RotorC"
StatorC = "StatorC"
graph.add_edge(pydot.Edge(DomainC, StatorC))
graph.add_edge(pydot.Edge(StatorC, "PyEMMO StatorC"))
graph.add_edge(pydot.Edge(DomainC, RotorC))
graph.add_edge(pydot.Edge(RotorC, "PyEMMO RotorC"))

# TODO: FINISH THIS GRAPH...

png_str = graph.create(format="png")

# treat the DOT output as an image file
sio = io.BytesIO()
sio.write(png_str)
sio.seek(0)
img = mpimg.imread(sio)

# plot the image
imgplot = plt.imshow(img, aspect="equal")
plt.show()

# %%
