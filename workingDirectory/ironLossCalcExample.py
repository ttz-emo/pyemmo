#%% imports
import gmsh
import sys, os
import numpy as np
import time as clockTime
from matplotlib import pyplot as plt
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.calcIronLoss import writeSimple

#%%
tstart = clockTime.time()

gmsh.initialize(sys.argv)
gmsh.option.setNumber("General.Verbosity", 3)

# Import B-field for stator (with x,y,z components)
bFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res_30000rpm_0A", "b_stator.pos"
)

if os.path.isfile(bFilePath):
    gmsh.merge(bFilePath)
else:
    raise FileNotFoundError(f"File '{bFilePath}' could not be found!")

# check that view was loaded!
if gmsh.view.getTags().size == 0:
    raise ValueError(
        f"Given file '{bFilePath}' did not result in a Gmsh view! Make sure the file is in gmsh POS-format!"
    )
tend = clockTime.time()
print(f"\nImport of b_stator.pos took {tend-tstart} seconds.\n")

#%% Import data from view
tstart = clockTime.time()
# number of time steps
NBR_STEPS = int(gmsh.view.option.getNumber(tag=1, name="NbTimeStep"))
if NBR_STEPS < 2:
    raise ValueError("Only one timestep!")

time = []  # init time array

# get values of first time for init
dType, btags, gdata, gtime, numComp = gmsh.view.getModelData(tag=1, step=0)
# dType, gtags, gdata, gtime, numComp = gmsh.view.getHomogeneousModelData(1, 0) # does
# the same thing, but data is 1x3*N instead of 3xN (with N = number of triangles)

B_Data = np.zeros((NBR_STEPS, len(gdata), numComp))  # allocate memory
dBdt = np.zeros((NBR_STEPS - 1, len(gdata), numComp))

B_Data[0] = np.array(gdata)[:, :numComp]  # set first time step vaues
time.append(gtime)

bmin = bmax = B_Data[0]  # init bmin and bmax array

# get data for each time step
for step in range(1, NBR_STEPS):
    dType, ctags, cdata, ctime, numComp = gmsh.view.getModelData(1, step)
    B_Data[step] = np.array(cdata)[:, 0:numComp]
    # "0:numComp" because for linear elements B = rot(A) results in one value per
    # element (triangle), but that one value is exported for each node. So we
    # dont need to import the same value three times. This is not valid for second
    # order elements or interpolation functions

    # assert all(btags == ctags)
    bmax = np.maximum(bmax, B_Data[step])  # compare values elementwise
    bmin = np.minimum(bmin, B_Data[step])
    time.append(ctime)
    # calculate time derivative
    dBdt[step - 1] = (B_Data[step] - B_Data[step - 1]) / (time[step] - time[step - 1])
tend = clockTime.time()
print(f"\nImport and reading of data took {tend-tstart} seconds.\n")
#%% Plot B_min, b_max for x and y component over element number
tstart = clockTime.time()

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
ax.set_ylabel("B in T")
ax.set_title("B_y")

# Plot amplitude of B_x and B_y
fig, ax = plt.subplots()
# ax.plot(bmax-bmin)
ax.semilogy(ctags, bmax[:, 0] - bmin[:, 0])
ax.semilogy(ctags, bmax[:, 1] - bmin[:, 1])
# ax.legend(["$\Delta$B"])
ax.set_title("$\Delta$B")
ax.legend(["B_x", "B_y"])
ax.set_xlabel("Element number")
ax.set_ylabel("B in T")
ax.grid(True)

#%% Calculate hysteresis losses
symFactor = 4
machineLength = 0.05  # meter

sigma_h = 172  # hysteresis loss factor
Bm = (bmax - bmin) / 2  # magnitude is (max-min)/2
Hm = 1 / np.pi * sigma_h * Bm  # magnitude of H according to paper

# Plot Bm and Hm over element number
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

# Calculate hysteresis loss on element bases for all time steps
beta = 2
ph = np.abs(Hm[:, 0] * dBdt[:, :, 0]) + np.abs(Hm[:, 1] * dBdt[:, :, 1])


#%% Export loss data to gmsh
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

# save p_hyst-field to file:
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "p_hyst.pos"
)
gmsh.view.write(pHystView, pFilePath)
#%% Integrate that loss data over time with gmsh
gmsh.plugin.setNumber("Integrate", "View", pHystView - 1)
P_h_ViewTag = gmsh.plugin.run("Integrate")
# get list data from integral to adjust results by symmetry factor and machine length
# and show them as xy plot in gmsh
dtype, numElem, P_HystData = gmsh.view.getListData(P_h_ViewTag)
# skip unnecessary list and scale results by symmmetry and machine length:
assert len(P_HystData) == 1  # make sure there is only one element
# P_HystData = P_HystData[0] * symFactor * machineLength
P_HystData = P_HystData[0]  # extract data from list
P_HystData[3:] = P_HystData[3:] * symFactor * machineLength
# first 3 values are point coorinates to plot results (unimportant, could be changd too...)

gmsh.view.remove(P_h_ViewTag)  # remove old integral view
P_h_ViewTag = gmsh.view.add("Hystersis Loss [W]")  # add new view for xy plot
gmsh.view.addListData(
    tag=P_h_ViewTag, dataType=dtype[0], numEle=numElem[0], data=P_HystData
)

# set view options
gmsh.view.option.setNumber(P_h_ViewTag, "Type", 3)
gmsh.view.option.setNumber(P_h_ViewTag, "TimeStep", NBR_STEPS - 1)
gmsh.view.option.setNumber(P_h_ViewTag, "IntervalsType", 3)
# RangeType:
# 1: default, 2: custom, 3: per time step
gmsh.view.option.setNumber(P_h_ViewTag, "RangeType", 2)

gmsh.view.option.setNumber(P_h_ViewTag, "CustomMin", 0)
gmsh.view.option.setNumber(P_h_ViewTag, "CustomMax", np.max(P_HystData) * 1.2)
# 0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler
gmsh.view.option.setNumber(P_h_ViewTag, "Axes", 3)
# 0: manual, 1: automatic, 2: top left, 3: top right, 4: bottom left, 5: bottom right,
# 6: top, 7: bottom, 8: left, 9: right, 10: full, 11: top third, 12: in model coordinatess
gmsh.view.option.setNumber(P_h_ViewTag, "AutoPosition", 2)

# save integral data as .dat file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_hyst.dat"
)
# gmsh.view.write(P_hystView, pFilePath)
writeSimple(pFilePath, time, P_HystData[3:])  # skip point coordinates in export
# had to write new function here because gmsh newer version .dat format does not match
# the old getdp format for import with matlab

#%% Calculate EDDY CURRENT LOSSES
kc = 1.05  # loss parameter
# loss function for eddy current loss from paper:
pi2 = np.square(np.pi)
pc = kc / (2 * pi2) * (np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1]))
# Export data to gmsh
model = gmsh.model.getCurrent()  # get current model
eddyCurrentView = gmsh.view.add("Eddy Current Loss [W/m³]")  # get tag of new view
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


#%% Integrate
# Integrate Eddy Current losses
gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(eddyCurrentView))
integralView = gmsh.plugin.run("Integrate")
# get list data from integral to determine maximum and set y limits in plot
dtype, numElem, P_eddyData = gmsh.view.getListData(integralView)

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
gmsh.view.option.copy(P_h_ViewTag, integralView)  # copy options from first plot
gmsh.view.option.setNumber(integralView, "CustomMax", np.max(P_eddyData) * 1.2)
gmsh.view.option.setNumber(integralView, "AutoPosition", 3)  # 3: top right

# save integral values to file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_eddy.dat"
)
writeSimple(pFilePath, time, P_eddyData[3:])

#%% Calculate EXCESS LOSS
ke = 0  # factor was 0 in model... used greater value for testing
Ce = 8.763363  # constant factor (from paper)
pe = ke / Ce * np.power((np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1])), 0.75)
#% Export data to gmsh
model = gmsh.model.getCurrent()  # get current model ID
excessView = gmsh.view.add("Excess Loss [W/m³]")  # get tag of new view
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
#%% Integrate Excess losses
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
gmsh.view.option.copy(P_h_ViewTag, integralView)
gmsh.view.option.setNumber(integralView, "CustomMax", np.max(P_excData) * 1.2)
gmsh.view.option.setNumber(integralView, "AutoPosition", 4)  # 4: bottom left

# save integral values to file
pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_exc.dat"
)
writeSimple(pFilePath, time, P_excData[3:])

#%%
# Calc mean of all losses on elements
ph_mean = np.mean(ph + pc + pe, axis=0)
# Export mean data
model = gmsh.model.getCurrent()  # or just get current model...
pHystView = gmsh.view.add("Mean Total Loss [W/m³]")  # get tag of new view
gmsh.view.addHomogeneousModelData(
    tag=pHystView,
    step=0,
    modelName=model,
    dataType="ElementData",
    tags=btags,
    data=ph_mean,
    time=0,
)

#%% sum of Losses
# Add up iron losses and plot
Ptotal = P_HystData + P_eddyData + P_excData
print(f"Rms of total iron losses: {np.sqrt(np.mean(np.square(Ptotal)))}")
viewPsum = gmsh.view.add("Total Iron Losses [W]")
gmsh.view.addListData(viewPsum, dtype[0], numElem[0], Ptotal)

gmsh.view.option.copy(integralView, viewPsum)
gmsh.view.option.setNumber(viewPsum, "CustomMax", np.max(Ptotal) * 1.2)
gmsh.view.option.setNumber(viewPsum, "AutoPosition", 5)  # 5: bottom right

pFilePath = os.path.join(
    ROOT_DIR, "workingDirectory", "testPosImport", "res", "P_tot.dat"
)
writeSimple(pFilePath, time, Ptotal[3:])

tend = clockTime.time()
print(f"\nIron loss calculation and plotting took {tend-tstart} seconds.\n")
#%%
# Launch the GUI to see the results:
# if "-nopopup" not in sys.argv:
#     gmsh.fltk.run()

gmsh.finalize()
