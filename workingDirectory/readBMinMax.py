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

# %% imports
import os
import sys

import gmsh
import numpy as np
from matplotlib import pyplot as plt

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.calcIronLoss import write_simple

# %%
gmsh.initialize(sys.argv)
gmsh.option.setNumber("General.Verbosity", 5)
# modelFilePath = os.path.join(
#     ROOT_DIR, "workingDirectory", "testPosImport", "Test_1FE1051-4HF11_TherCom.geo"
# )
# gmsh.open(modelFilePath)

## Write logfile to see if script is executed from python
# with open(
#     os.path.join(ROOT_DIR, "workingDirectory", "testPosImport", "ironlosses.log")
# ) as logfile:
#     logfile.write("Init of loss calculation...")

bFilePath = os.path.join(
    ROOT_DIR,
    "workingDirectory",
    "testPosImport",
    "res",
    "b_stator.pos",
    # ROOT_DIR, "workingDirectory", "testPosImport", "res_fullPeriod180Steps", "b_stator.pos"
)
# hFilePath = os.path.join(
#     ROOT_DIR, "workingDirectory", "testPosImport", "res", "h_stator.pos"
# )
if os.path.isfile(bFilePath):
    gmsh.merge(bFilePath)
else:
    raise FileNotFoundError(f"File '{bFilePath}' could not be found!")

# check that view was loaded!
if gmsh.view.getTags().size == 0:
    raise ValueError(
        f"Given file '{bFilePath}' did not result in a Gmsh view! Make sure the file is in gmsh POS-format!"
    )

# if os.path.isfile(hFilePath):
#     gmsh.merge(hFilePath)
# else:
#     raise FileNotFoundError(f"File '{hFilePath}' could not be found!")
# %% Import data from view
# number of time steps
NBR_STEPS = int(gmsh.view.option.getNumber(tag=1, name="NbTimeStep"))
if NBR_STEPS < 2:
    raise ValueError("Only one timestep!")
time = []
dType, btags, gdata, gtime, numComp = gmsh.view.getModelData(1, 0)  # init
# data = np.zeros((NBR_STEPS, len(gdata), len(gdata[0]))) # data copied twice
B_Data = np.zeros((NBR_STEPS, len(gdata), numComp))
dBdt = np.zeros((NBR_STEPS - 1, len(gdata), numComp))
B_Data[0] = np.array(gdata)[:, :numComp]
# dType, gtags, gdata, gtime, numComp = gmsh.view.getHomogeneousModelData(1, 0) # does
# the same thing, but data is 1x3*N instead of 3xN (with N = number of triangles)
time.append(gtime)
bmin = bmax = B_Data[0]  # init bmin and bmax array

for step in range(1, NBR_STEPS):
    dType, ctags, cdata, ctime, numComp = gmsh.view.getModelData(1, step)
    # dType, ctags, cdata, ctime, numComp = gmsh.view.getHomogeneousModelData(1, step)
    B_Data[step] = np.array(cdata)[:, 0:numComp]
    assert all(btags == ctags)
    bmax = np.maximum(bmax, B_Data[step])
    bmin = np.minimum(bmin, B_Data[step])
    time.append(ctime)
    dBdt[step - 1] = (B_Data[step] - B_Data[step - 1]) / (time[step] - time[step - 1])
# %%
# nodeTagDict = {}
# # ELEM_TYPE = 2  # 2 = triangle
# for triTag in btags:
#     elementType, nodeTags, dim, entityTag = gmsh.model.mesh.getElement(triTag)
#     nodeTagDict[int(triTag)] = nodeTags.tolist()
# # gmsh.model.mesh.getNode(76)

# nodeTagDictJson = json.dumps(nodeTagDict, indent=4)
# print(nodeTagDictJson)
# %%
fig, axes = plt.subplots(nrows=1, ncols=2)
ax = axes[0]
ax.plot(ctags, bmax[:, 0])
ax.plot(ctags, bmin[:, 0])
ax.legend(["B_max", "B_min"])
ax.set_xlabel("Element number")
ax.set_ylabel("B in T")
ax.set_title("B_x")

ax = axes[1]
ax.plot(ctags, bmax[:, 1])
ax.plot(ctags, bmin[:, 1])
ax.legend(["B_max", "B_min"])
ax.set_xlabel("Element number")
# ax.set_ylabel("B in T")
ax.set_title("B_y")

fig, ax = plt.subplots()
# ax.plot(bmax-bmin)
ax.semilogy(ctags, bmax[:, 0] - bmin[:, 0])
ax.semilogy(ctags, bmax[:, 1] - bmin[:, 1])
# ax.legend(["$\Delta$B"])
ax.set_title(r"$\Delta$B")
ax.legend(["B_x", "B_y"])
ax.set_xlabel("Element number")
ax.set_ylabel("B in T")
ax.grid(True)

# #%% Import h-field from view
# # number of time steps
# NBR_STEPS = int(gmsh.view.option.getNumber(tag=2, name="NbTimeStep"))
# # time = []
# dType, btags, gdata, gtime, numComp = gmsh.view.getModelData(1, 0)  # init
# H_Data = zeros((NBR_STEPS, len(gdata), 3))
# H_Data[0] = np.array(gdata)[:, 0:3]
# # dType, gtags, gdata, gtime, numComp = gmsh.view.getHomogeneousModelData(1, 0) # does
# # the same thing, but data is 1x3*N instead of 3xN (with N = number of triangles)

# for step in range(1, NBR_STEPS):
#     dType, ctags, cdata, ctime, numComp = gmsh.view.getModelData(1, step)
#     # dType, ctags, cdata, ctime, numComp = gmsh.view.getHomogeneousModelData(1, step)
#     H_Data[step] = np.array(cdata)[:, 0:3]
#     assert all(btags == ctags)
# %% Calculate hysteresis losses
symFactor = 4
machineLength = 0.05  # meter

sigma_h = 172  # hysteresis loss factor
Bm = (bmax - bmin) / 2
Hm = 1 / np.pi * sigma_h * Bm
fig, axes = plt.subplots(nrows=1, ncols=2)

ax = axes[0]
ax.plot(ctags, Bm)
ax.set_xlabel("Element number")
ax.set_ylabel("B in T")
ax.set_title("B_m")

ax = axes[1]
ax.plot(ctags, Hm)
ax.set_xlabel("Element number")
# ax.set_ylabel("B in T")
ax.set_title("H_m")

beta = 2
ph = np.abs(Hm[:, 0] * dBdt[:, :, 0]) + np.abs(Hm[:, 1] * dBdt[:, :, 1])
# fig, ax = plt.subplots()
# ax.plot(time[1:], ph)
# %%
# Calc mean of ph on elements
ph_mean = np.mean(ph, axis=0)
# Export mean data
model = gmsh.model.getCurrent()  # or just get current model...
pHystView = gmsh.view.add("Mean Hystersis Loss")  # get tag of new view
gmsh.view.addHomogeneousModelData(
    tag=pHystView,
    step=0,
    modelName=model,
    dataType="ElementData",
    tags=btags,
    data=ph_mean,
    time=0,
)

# %% Export data to gmsh
# gmsh.model.add("Test p_hyst export") # new model for view??
model = gmsh.model.getCurrent()  # or just get current model...
pHystView = gmsh.view.add("Hystersis Loss [W/m³]")  # get tag of new view
for step in range(len(time) - 1):
    gmsh.view.addHomogeneousModelData(
        tag=pHystView,
        step=step + 1,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=ph[step, :],
        time=time[step],
    )

# save field to file:
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "p_hyst.pos"
)
gmsh.view.write(pHystView, pFilePath)
# %% Integrate
gmsh.plugin.setNumber("Integrate", "View", pHystView - 1)
P_hystView = gmsh.plugin.run("Integrate")
# get list data from integral to determine maximum and set y limits in plot
dtype, numElem, P_HystData = gmsh.view.getListData(P_hystView)
# %%
# skip unnecessary list and scale results by symmmetry and machine length:
assert len(P_HystData) == 1  # make sure there is only one element
# P_HystData = P_HystData[0] * symFactor * machineLength
P_HystData = P_HystData[0]  # extract data from list
P_HystData[3:] = P_HystData[3:] * symFactor * machineLength

# %%
# replace data in view with recalculated data
gmsh.view.remove(P_hystView)
P_hystView = gmsh.view.add("Hystersis Loss [W]")
gmsh.view.addListData(
    tag=P_hystView, dataType=dtype[0], numEle=numElem[0], data=P_HystData
)

# set view options
gmsh.view.option.setNumber(P_hystView, "Type", 3)
gmsh.view.option.setNumber(P_hystView, "TimeStep", NBR_STEPS - 1)
gmsh.view.option.setNumber(P_hystView, "IntervalsType", 3)
# RangeType:
# 1: default, 2: custom, 3: per time step
gmsh.view.option.setNumber(P_hystView, "RangeType", 2)

gmsh.view.option.setNumber(P_hystView, "CustomMin", 0)
gmsh.view.option.setNumber(P_hystView, "CustomMax", np.max(P_HystData) * 1.2)
# 0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler
gmsh.view.option.setNumber(P_hystView, "Axes", 3)
# 0: manual, 1: automatic, 2: top left, 3: top right, 4: bottom left, 5: bottom right,
# 6: top, 7: bottom, 8: left, 9: right, 10: full, 11: top third, 12: in model coordinatess
gmsh.view.option.setNumber(P_hystView, "AutoPosition", 2)

pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_hyst.dat"
)
# gmsh.view.write(P_hystView, pFilePath)
write_simple(pFilePath, time, P_HystData[3:])  # skip point coordinates in export


# %% Calculate EDDY CURRENT LOSSES
kc = 1.05  # loss parameter
# loss fucntion for hysteresis from paper:
pc = (
    1
    / 2
    / np.square(np.pi)
    * kc
    * (np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1]))
)
# Export data to gmsh
model = gmsh.model.getCurrent()  # get current model
eddyCurrentView = gmsh.view.add("Eddy Current Loss")  # get tag of new view
for step in range(len(time) - 1):
    # write every time step (except first, because derivative) to view
    gmsh.view.addHomogeneousModelData(
        tag=eddyCurrentView,
        step=step + 1,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=pc[step, :],
        time=time[step],
    )
# save new view data in pos file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "p_eddy.pos"
)
gmsh.view.write(eddyCurrentView, pFilePath)


# %% Integrate
# Integrate Eddy Current losses
gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(eddyCurrentView))
integralView = gmsh.plugin.run("Integrate")
# get list data from integral to determine maximum and set y limits in plot
dtype, numElem, P_eddyData = gmsh.view.getListData(integralView)

# skip unnecessary list and scale results by symmmetry and machine length:
assert len(P_eddyData) == 1  # make sure there is only one element
P_eddyData = P_eddyData[0] * symFactor * machineLength

gmsh.view.remove(integralView)
integralView = gmsh.view.add("Eddy Current Loss [W]")
# replace data in view with recalculated data
gmsh.view.addListData(
    tag=integralView, dataType=dtype[0], numEle=numElem[0], data=P_eddyData
)

# set options to display integral as xy plot
# gmsh.view.option.setString(integralView,"Type",)
gmsh.view.option.copy(P_hystView, integralView)
gmsh.view.option.setNumber(integralView, "CustomMax", np.max(P_eddyData) * 1.2)
gmsh.view.option.setNumber(integralView, "AutoPosition", 3)  # 3: top right

# save integral values to file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_eddy.dat"
)
gmsh.view.write(integralView, pFilePath)

# %% Calculate EXCESS LOSS
ke = 0  # factor was 0 in model... used greater value for testing
Ce = 8.763363  # constant factor (from paper)
pe = 1 / Ce * ke * np.power((np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1])), 0.75)
# % Export data to gmsh
model = gmsh.model.getCurrent()  # get current model ID
excessView = gmsh.view.add("Excess Loss")  # get tag of new view
for step in range(len(time) - 1):
    gmsh.view.addHomogeneousModelData(
        tag=excessView,
        step=step + 1,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=pe[step, :],
        time=time[step],
    )
# save to file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "p_exc.pos"
)
gmsh.view.write(excessView, pFilePath)
# %% Integrate Excess losses
gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(excessView))
integralView = gmsh.plugin.run("Integrate")

# get list data from integral to determine maximum and set y limits in plot
dtype, numElem, P_excData = gmsh.view.getListData(integralView)

# skip unnecessary list and scale results by symmmetry and machine length:
assert len(P_excData) == 1  # make sure there is only one element
P_excData = P_excData[0] * symFactor * machineLength

gmsh.view.remove(integralView)
integralView = gmsh.view.add("Excess Losses [W]")
# replace data in view with recalculated data
gmsh.view.addListData(
    tag=integralView, dataType=dtype[0], numEle=numElem[0], data=P_excData
)

gmsh.view.option.copy(P_hystView, integralView)
gmsh.view.option.setNumber(integralView, "CustomMax", np.max(P_excData) * 1.2)
# 0: manual, 1: automatic, 2: top left, 3: top right, 4: bottom left, 5: bottom right,
# 6: top, 7: bottom, 8: left, 9: right, 10: full, 11: top third, 12: in model coordinatess
gmsh.view.option.setNumber(integralView, "AutoPosition", 4)

# %% save integral values to file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_exc.dat"
)
gmsh.view.write(integralView, pFilePath)

# %% sum of Losses
# Add up iron losses and plot
Ptotal = P_HystData + P_eddyData + P_excData
viewPsum = gmsh.view.add("Total Iron Losses [W]")
gmsh.view.addListData(viewPsum, dtype[0], numElem[0], Ptotal)
# gmsh.view.option.setString(integralView,"Type",)
gmsh.view.option.copy(integralView, viewPsum)
gmsh.view.option.setNumber(viewPsum, "CustomMax", np.max(Ptotal) * 1.2)
gmsh.view.option.setNumber(viewPsum, "AutoPosition", 5)  # 5: bottom right

pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_tot.dat"
)
write_simple(pFilePath, time, Ptotal[3:])

# %%
# get all model entitys (imported)
# entities = gmsh.model.getEntities()  # results in 77 surfaces for view bn

# %% SOME TESTING ON ENITITIES
# for e in entities:
#     # Dimension and tag of the entity:
#     dim = e[0] # is allways =2 here because just surfaces
#     tag = e[1]
#     # Get the mesh nodes for the entity (dim, tag):
#     nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)
#     # Get the mesh elements for the entity (dim, tag):
#     elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
#     # * Type and name of the entity:
#     entityType = gmsh.model.getType(e[0], e[1])
#     name = gmsh.model.getEntityName(e[0], e[1])
#     if len(name): name += ' '
#     print("Entity " + name + str(e) + " of type " + entityType)

#     # * Number of mesh nodes and elements:
#     numElem = sum(len(i) for i in elemTags)
#     print(" - Mesh has " + str(len(nodeTags)) + " nodes and " + str(numElem) +
#           " elements")
#     # * List all types of elements making up the mesh of the entity:
#     for t in elemTypes:
#         name, dim, order, numv, parv, _ = gmsh.model.mesh.getElementProperties(
#             t)
#         print(" - Element type: " + name + ", order " + str(order) + " (" +
#               str(numv) + " nodes in param coord: " + str(parv) + ")")

# %%
# Launch the GUI to see the results:
if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
