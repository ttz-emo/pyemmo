#!/usr/bin/env python

from __future__ import annotations

# set log level to diable necessary matplotlib log messages
import logging

# # PyEMMO-Pyleecan Tutorial
# This is a tutorial on how to create or load a Pyleecan machine and translate it to ONELAB using the PyEMMO pyleecan-api.
#
# This tutorial has the following sections:
# 1. Load or create a Pyleecan machine and how to modify its properties
# 2. How to use use the PyEMMO pyleecan-api to create a ONELAB model
# 4. How to run a simple simulation in ONELAB
# 5. What is possible, whats not?
# 6. User-defined results
#
# The notebook related to this tutorial is available on [GitHub](https://github.com/ttz-emo/pyemmo/blob/master/tutorials/pyleecan_api.ipynb).
# ## 1. Load or create a Pyleecan machine and how to modify its properties
#
# Pyleecan has a lot of useful tutorials under [Pyleecan tutorials][pylcn_tutorials].
# See those for further details on how to use the pyleecan motor toolbox.
#
# There are two ways to get a Pyleecan machine:
#
# - Load a existing machine using the `load` function.
# - Create a machine with a python script by using the Pyleecan classes.
#   See the [01_tuto_Machine.ipynb][pylcn_tutorial_machine] tutorial for that.
#
#
# You can load an existing Pyleecan model using:
#
# [pylcn_tutorials]: https://pyleecan.org/tutorials.html
# [pylcn_tutorial_machine]: https://pyleecan.org/01_tuto_Machine.html

# In[ ]:


logging.getLogger("matplotlib").setLevel(logging.ERROR)


# In[ ]:


# Load the machine
from os.path import join

from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load

IPMSM_A = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
# In Jupyter notebook, we set is_show_fig=False to skip call to fig.show() to avoid a warning message
# All plot methods return the corresponding matplotlib figure and axis to further edit the resulting plot
fig, ax = IPMSM_A.plot(is_show_fig=False)


# This can be a default machine from the Pyleecan `DATA` directory or you can create your own machine using the Pyleecan GUI.
# See [Pyleecan Webinar on how to use the GUI][GUI_webinar] or just try it yourself by running:
#
# ``
# python -m pyleecan
# ``
#
# in the command line.
#
# [GUI_webinar]: https://pyleecan.org/webinar_1.html

# Now you can modify the machine properties depending on the classes used.
# E.g. we can modify the magnets remanence flux density by accessing:

# In[ ]:


new_Br = 1.19  # Tesla
IPMSM_A.rotor.hole[0].magnet_0.mat_type.mag.Brm20 = new_Br
IPMSM_A.rotor.hole[0].magnet_1.mat_type.mag.Brm20 = new_Br


# Or you can modify the geoemtry by changing the respecive parameters.
# There parameters can be found in the Pyleecan documentation or for a existing machine by using the method `plot_schematics`.

# In[ ]:


# print rotor class info
print(f"Rotor parameters can be found in Pyleecan class: {type(IPMSM_A.rotor.hole[0])}")
# use plot_schematics to show parameters
_ = IPMSM_A.rotor.hole[0].plot_schematics(is_default=True, is_show_fig=False)


# In[ ]:


from matplotlib import pyplot as plt

fig, axes = plt.subplots(1, 2)  # create subplot to show results side by side
# plot inital config
fig, ax = IPMSM_A.rotor.plot(sym=8, fig=fig, ax=axes[0], is_show_fig=False)
_ = ax.set_ylim([-0.01, 0.065])
_ = ax.set_xlim([0.04, 0.08])
_ = ax.set_title(f"H2 = {IPMSM_A.rotor.hole[0].H2*1e3} mm")

# change parameter for magnet-lamination overlap
IPMSM_A.rotor.hole[0].H2 = 3e-3

# plot rotor segment after parameter change
fig, ax = IPMSM_A.rotor.plot(sym=8, fig=fig, ax=axes[1], is_show_fig=False)
_ = ax.set_ylim([-0.01, 0.065])
_ = ax.set_xlim([0.04, 0.08])
_ = ax.set_title(f"H2 = {IPMSM_A.rotor.hole[0].H2*1e3} mm")


# But we could also just load the JSON machine file in the Pyleecan GUI and modify the properties there.

# ## 2. How to use use the PyEMMO pyleecan-api to create a ONELAB model
# From here on its very easy to create a ONELAB machine model using the `pyemmo.api.pyleecan` api package.
# You simply need to call the `pyemmo.api.pyleecan.main.main` function.
# You will need to supply the **Pyleecan machine object** and a **path where the ONELAB model files shoud be stored**.
# You can optionally specify if the Gmsh GUI should be opened after the model has been generated.
# Additionally the Gmsh and GetDP executables to use for opening the GUI and run a simulation.

# In[ ]:


import logging

from pyemmo.api.pyleecan import main as pyleecan_api
from pyemmo.definitions import RESULT_DIR

# you can set the output verbosity of the model creation using the pyemmo logger.
# The logging module by default implements DEBUG, INFO, WARNING, ERROR, FATAL log
# levels, which are simply constants for integer levels, e.g. logging.DEBUG == 10
# You can use evel(logging.DEBUG -1) to trigger extended debugging, which shows
# additional information in plots and opens the Gmsh GUI at different levels in the
# model creation.
logging.getLogger("pyemmo").setLevel(logging.INFO)

# Run the main function of the pyleecan api:
pyemmo_script = pyleecan_api.main(
    pyleecan_machine=IPMSM_A,
    model_dir=join(RESULT_DIR, "Toyota_Prius_ONELAB"),  # path for the model files
    use_gui=False,  # select if you want to open the final model in Gmsh.
    gmsh="",  # optional gmsh executable.
    # If use_gui is True, pyemmo will try to find a executable on your computer.
    getdp="",  # optional getdp executable. For simulation in the GUI.
)


# The created geometry will be saved as a *.geo* file (Gmsh specific file format).
# The files used by GetDP to run a simulation will be saved as *.pro* files.
# If you now look at the contents of the newly created folder *\Toyota_Prius_ONELAB*, you will find the following model files:
#
# | Model File | Description|
# |------------|------------|
# | Toyota_Prius.geo | Geometry (CAD) |
# | Toyota_Prius.pro | Main Simulation Setup |
# | Toyota_Prius_param.geo | Global Machine and Simulation parameters |
# | machine_magstadyn_a.pro | Problem Template for Electrical Machines |
# | Circuit_SC_ASM.pro | Optional Circuit Definition (for Induction Machines) |
# | pyemmo_jsonAPI.log | PyEMMO Model Creation log-file |
#

# ## 4. How to run a simple simulation in ONELAB

# After creating a machine model you can start a simulation in the GUI by adjusting the parameters and clicking the "Run" button.
# Or you can use the `runCalcforCurrent` function and start a simulation from Python as a subprocess.
# Therefore you can specify the same parameters you find in GUI using a parameter dictionary like in the example below (``paramDict``).
# You can find all adjustable constants and parameters in the documentation under **ONELAB Model Constants** and **ONELAB Model Parameters**.
#
# For synchronous machines PyEMMO will try to calculate the dq-System offset between rotor and stator. See **dq-Offset calculation** for more details.

# In[ ]:


import os
import time

import numpy as np

from pyemmo.functions.run_onelab import find_getdp, run_simulation

# Simulation parameters
n = 1500
id = -10
iq = 50
resId = "test_simulation"  # result identifier and result folder name

# create param dict for simulation
param_dict = {
    # model .pro file path
    "pro": pyemmo_script.pro_file_path,
    # Gmsh Parameters
    "gmsh": {"exe": r"", "gmsf": 2, "verbosity level": 2},
    # GetDP Parameters
    "getdp": {
        "exe": find_getdp(),  # GetDP executable, you can use the function findGetDP
        # which tries to find the exe on you PC.
        # change gmsh and getdp verbosity level (0-99)
        # 0 - fatal, 1 - error, 2 - warning, 3 - info, 5 - debug, 99 - extended debug
        "verbosity level": 2,
        "Flag_Debug": 0,  # epxort debug infos and results from GetDP
        ## Analysis Parameters
        "Flag_AnalysisType": 1,  # 0 - static, 1 - transient
        "Flag_SrcType_Stator": 1,  # 1 - current source, 2 - voltage source (not finally implemented)
        "initrotor_pos": 0.0,  # initial rotor position in °
        "d_theta": 0.5,  # angular step size in °
        "finalrotor_pos": 45,  # final rotor position in °
        # "RPM": n, # rotational speed
        "Flag_EC_Magnets": 0,  # control magnet eddy current calculation
        #
        ## Result settings
        "res": pyemmo_script.results_path,  # main results folder
        "ResId": resId,  # current simulation result folder ID
        "Flag_PrintFields": 0,  # control field result output (.pos files, only last timestep)
        "Flag_ClearResults": 0,  # remove results if existing, otherwise existing results will be imported
        #
        ## Excitation parameters
        "ID_RMS": id / np.sqrt(2),
        "IQ_RMS": iq / np.sqrt(2),
    },
    # "log": f"{resId}.log",  # optional: log file name
    "info": "",  # optional: info string to save with simulation config
    "datetime": time.ctime(),  # optional: current time
    "PostOp": [],  # PostOperations to execute after simulation.
    # Standard Option is: GetBOnRadius
}


# In[ ]:


# run simulation:
results = run_simulation(param_dict)


# After the simulation has finished, pyemmo automatically imports the standard global result values using `pyemmo.functions.import_results.main` function and output the results in a dictionary structure.
# Here we store this output in the variable `results`.
#
# Using `print` or `pprint` (pretty-print) we can show the dictionary keys.
#
# Depended on the simulation parameters defined in `param_dict["getdp"]`, not all of the keys must contain result data.

# In[ ]:


from pprint import pprint

pprint(results.keys())
pprint(results["flux"].keys())


# We can use ``matplotlib.pyplot`` to plot some time depended results:

# In[ ]:


# Plot torque, flux and induced voltage results
fig, ax = plt.subplots()
ax.plot(results["time"], results["torque"], ".-")
ax.set_ylabel("Torque in Nm")
ax.set_xlabel("Time in s")
ax.grid()

fig, ax = plt.subplots()
ax.plot(results["time"], results["flux"]["d"], ".-", label="d-flux linkage")
ax.plot(results["time"], results["flux"]["q"], ".-", label="q-flux linkage")
ax.set_ylabel("Flux linkage in Wb")
ax.set_xlabel("Time in s")
ax.grid()
ax.legend()

fig, ax = plt.subplots()
ax.plot(results["time"][1:], results["inducedVoltage"]["a"], ".-", label="Phase A")
ax.plot(results["time"][1:], results["inducedVoltage"]["b"], ".-", label="Phase B")
ax.plot(results["time"][1:], results["inducedVoltage"]["c"], ".-", label="Phase C")
ax.set_ylabel("Induced Voltage in V")
ax.set_xlabel("Time in s")
ax.grid()
ax.legend()


# ## 5. What is possible, whats not?
#
# The following design and geometry limitations are known:
#
# - Multi-phase windings with $m != 3$
# - Number of winding layers > 2 (not supported by SWAT-EM).
# - Wound rotor machines.
# - Multi-cage induction motors.
# - No multi-layered surface subtractions (you cannot cut out of tool surfaces in api)
# - No overlaping surfaces, e.g. air box overlaping magnet (does not work in pyleecan aswell).
#

# ## 6. User-defined results
# Finally lets talk about the definition of some user defined results appart from the standard global results seen in the simulation example before.
# We can use the ``Script`` method ``add_post_operation`` to add user-defined post operations to the GetDP input scripts.
# This requires some knowledge of the GetDP Syntax for evaluating PostProcessing quantities.
# You can find all available quantities in the `machine_magstadyn_a.pro` template file in the ``PostProcessing`` section.
#
# In the following example we are going to evaluate the force density in the stator airgap calculated by the Maxwell Stress Tensor.
# The name of the (predefined) GetDP post processing quantity is `Force_MST`, the name of the new ``PostOperation`` is "Airgap_Force" and the evaluation should be performed on the mesh element nodes of the boundary curve `Stator_Bnd_MB` (``OnRegion="NodesOf[Stator_Bnd_MB]"``).
#
# Before we run a new simulation and evaluate its results, we need to regenerate the .pro files for GetDP using `pyemmo_script.generateScript(2)`.

# In[ ]:


import gmsh

pyemmo_script.add_post_operation(
    quantity_name="Force_MST",
    post_operation="Airgap_Force",
    # GetDP keyword arguments for PostOperations
    OnRegion="NodesOf[Stator_Bnd_MB]",
    # alternativly you could use:
    # OnGrid=(
    #     "{80.7e-3*Cos[$A*Pi/180],"
    #     "80.7e-3*Sin[$A*Pi/180],0}"
    #     r"{0:360/SymmetryFactor:360/3600,0,0}"
    # ),
    # to interpolate the results on a specific radius (80.7mm) in the airgap
    File=r"CAT_RESDIR\F_airgap.pos",
    Format="Gmsh",
    LastTimeStepOnly="",
)
pyemmo_script.add_post_operation(
    quantity_name="Force_MST_Cyl",
    post_operation="Airgap_Force",
    # GetDP keyword arguments for PostOperations
    OnRegion="NodesOf[Stator_Bnd_MB]",
    # alternativly you could use:
    # OnGrid=(
    #     "{80.7e-3*Cos[$A*Pi/180],"
    #     "80.7e-3*Sin[$A*Pi/180],0}"
    #     r"{0:360/SymmetryFactor:360/3600,0,0}"
    # ),
    # to interpolate the results on a specific radius in the airgap
    File=r"CAT_RESDIR\F_airgap_cyl.pos",
    Format="Gmsh",
    LastTimeStepOnly="",
)
pyemmo_script.generate(2)  # recreate pro files with new PostOperation


# Now we can run new simulation.
# We are reusing the ``param_dict`` of the previous simulation while only changing some specific parameters.

# In[ ]:


# run a new simulation and import + display the results for the force density

param_dict["getdp"]["Flag_AnalysisType"] = 0  # static simulation
# unset currents for simple no-load simulation
param_dict["getdp"]["ID_RMS"] = 0
param_dict["getdp"]["IQ_RMS"] = 0
# set flag to clear results if any and re-run the calculation
param_dict["getdp"]["Flag_ClearResults"] = 1
# set new results ID:
param_dict["getdp"]["ResId"] = "Calc_ForceDensity_noLoad"
# set post operation list to evaluate previously created PostOperation "Airgap_Force"
param_dict["PostOp"] = ["Airgap_Force"]

# run simulation:
results = run_simulation(param_dict)


# After the simulation has successfully finished, we can import the results using the pyemmo ``import_results`` module.
# Since the force density is a local, position depended quantity, the results are saved as `.pos` files, Gmsh's default field result format.
# We can import these files using the function `import_pos_parsedFormat`.
#
# In the code below we are going to compare the radial and tangential force density calculated from the xyz force density in Python vs. the rad-tan force density directly transformed in GetDP.

# In[ ]:


# since the force density is not in the standard results import, we have to import it
# manually:

# Arc patch to plot arcs
from matplotlib.patches import Arc

# function to import GetDP "GmshParsed" formatted output files:
from pyemmo.functions.import_results import import_pos_legacy

# function to transform cartesian to polar coordinates:
from pyemmo.functions.transform_coords import cart2pol

# First import force density in with xyz components:
# Since we did print the vector based force density on points, we get the data
# type "VP" for "vector value on points". Therefore we get the xyz coordinates
# of the mesh nodes and their corresponding force density values with xyz components.
# Due to a inconsistency in GetDP, the results are written out in GmshParsed format
# instead of newer Gmsh msh-format. msh formatted files can be imported by using
# the function ``importPos``.
data_type, nodes, sigma_xyz = import_pos_legacy(
    join(param_dict["getdp"]["res"], param_dict["getdp"]["ResId"], "F_airgap.pos")
)


# Show evaluation points (mesh nodes) in scatter plot

fig, ax = plt.subplots()
# scatter node coodrinates
ax.scatter(nodes[:, 0], nodes[:, 1], marker=".", s=10, label="Data points")
# add arc to show they are all on the same radius
arc = Arc(
    (0, 0),
    nodes[0, 0] * 2,
    nodes[0, 0] * 2,
    angle=0,
    theta1=0,
    theta2=45,
    color="red",
    label="Radius",
)
ax.add_patch(arc)
# set plot details
ax.set_aspect("equal", adjustable="datalim")
ax.grid()
ax.set_title("Evaluation nodes")
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")


# In[ ]:


# transform xy coordinates of the nodes to polar coorinates to then plot over the
# airgap angle:
r1, phi1 = cart2pol(nodes[:, 0], nodes[:, 1])

# create unit vectors to calculate radial and tangential components
hat_e_rad = np.array([np.cos(phi1), np.sin(phi1)]).reshape(2, len(phi1))
hat_e_tan = np.array([-np.sin(phi1), np.cos(phi1)]).reshape(2, len(phi1))

# radial component is scalar product of unit vector in radial direction
# with force density vector
sigma_xyz_rad = np.diag(np.dot(sigma_xyz[:, 0:2], hat_e_rad))

# same goes for the tangential component using the tangential unit vetor
sigma_xyz_tan = np.diag(np.dot(sigma_xyz[:, 0:2], hat_e_tan))


# Add plot of radial force density
fig, ax = plt.subplots()

ax.plot(
    np.rad2deg(phi1),  # transform circumferential angle from rad to deg
    sigma_xyz_rad,  # radial force density calculated from xyz
    ".",
    label=r"$\sigma_\mathrm{rad}$ from $\sigma_\mathrm{xyz}$",
)


# Second import force density allready transformed in polar components in GetDP:

data_type, nodes, sigma_rphiz = import_pos_legacy(
    join(param_dict["getdp"]["res"], param_dict["getdp"]["ResId"], "F_airgap_cyl.pos")
)

# convert xy coordinates to r-phi
r2, phi2 = cart2pol(nodes[:, 0], nodes[:, 1])  # xy -> r-phi

# add plot of radial force density directly calculated from GetDP
ax.plot(
    np.rad2deg(phi2),  # rad -> deg
    sigma_rphiz[:, 0],  # show radial comp (index 0)
    "o",
    fillstyle="none",
    label=r"$\sigma_{rad}$ from GetDP",
)
ax.grid()
ax.set_xlabel("Mech. angle in deg")
ax.set_ylabel(r"$\sigma_\mathrm{rad}$ in N/m²")
_ = ax.legend()


# In[ ]:


## Do the same plot for the tangential components:
fig, ax = plt.subplots()
ax.plot(
    np.rad2deg(phi1),  # transform circumferential angle from rad to deg
    sigma_xyz_tan,  # sigma_tan
    ".",
    label=r"$\sigma_\mathrm{tan}$ from $\sigma_\mathrm{xyz}$",
)

ax.plot(
    np.rad2deg(phi2),  # rad -> deg
    sigma_rphiz[:, 1],  # show tangentail comp (index 1)
    "o",
    fillstyle="none",
    label=r"$\sigma_{tan}$ from GetDP",
)
ax.grid()
ax.set_xlabel("Mech. angle in deg")
ax.set_ylabel(r"$\sigma_\mathrm{tan}$ in N/m²")
_ = ax.legend()


# In[ ]:


# We can further check if the results are really equal:

# Check the amplitude
try:
    assert np.allclose(
        np.linalg.norm(sigma_xyz, axis=1),
        np.linalg.norm(sigma_rphiz, axis=1),
        atol=1e-9,
    )

    # check radial component
    assert np.allclose(
        sigma_xyz_rad,
        sigma_rphiz[:, 0],
        atol=1e-9,
    )
    #
    # check tangential component
    assert np.allclose(
        sigma_xyz_tan,
        sigma_rphiz[:, 1],  # sigma_tan
        atol=1e-9,
    )
except Exception as e:
    logging.getLogger(__name__).warning("MST Force results missmatch!", exc_info=True)


# With the Gmsh python api its easy to also visualize results and show them in the Gmsh GUI:

# In[ ]:


# check if gmsh was initialized
if not gmsh.isInitialized():
    gmsh.initialize()
else:
    # unshow all other views if gmsh has been run before
    for tag in gmsh.view.getTags():
        gmsh.view.option.setNumber(tag, "Visible", 0)

# open result file with Gmsh
gmsh.merge(
    join(param_dict["getdp"]["res"], param_dict["getdp"]["ResId"], "F_airgap.pos")
)

# run GUI to show results:
gmsh.fltk.run()


# In[ ]:


# we could further load the created mesh from the mesh file:
mesh_file = join(pyemmo_script.script_path, pyemmo_script.name + ".msh")
if os.path.isfile(mesh_file):
    gmsh.merge(mesh_file)
    gmsh.fltk.run()
else:
    logging.getLogger(__name__).warning("Could not find mesh file")
