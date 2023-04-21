# %%
# Imports
import pandas
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.io as sio

# %% import ansys data
ansysResPath = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\230301_EisenverlustkennfeldAnsys.csv"
ansysResults = pandas.read_csv(ansysResPath)
for key in ansysResults.keys():
    if "offset_deg" in key:
        phiDQ = ansysResults[key]  # angle for dq offset in deg
    elif "I [A]" in key:
        iAnsys = ansysResults[key]  # current amplitude (effective value) in A_eff
    elif "AvgCoreLoss" in key:
        coreLossAnsys = ansysResults[key]  # core loss results
    elif "AvgTorque" in key and not "AvgTorqueRipple" in key:
        torque = ansysResults[key]  # core loss results
nbrDesignPoints = len(phiDQ)
phi = np.deg2rad(phiDQ)
idq = np.array([iAnsys * -np.sin(phi), iAnsys * np.cos(phi)])

ansysResMat = os.path.join(
    os.path.dirname(ansysResPath), os.path.split(ansysResPath)[1].split(".")[0] + ".mat"
)
sio.savemat(
    ansysResMat,
    {
        "coreLossAnsys": coreLossAnsys.tolist(),
        "torqueAnsys": torque.tolist(),
        "phiDQ_Ansys": phiDQ.to_list(),
        "iAmpAnsys": iAnsys.to_list(),
    },
)
# %%
# Load onelab results
RES_DIR = (
    r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"
)
coreLossOnelab = np.load(os.path.join(RES_DIR, "ironLossData.npy"))
# coreLossOnelabMatFile = os.path.join(RES_DIR, "230301_ironLossDataOnelab.mat")
# sio.savemat(
#     coreLossOnelabMatFile,
#     {
#         "coreLossOnelab": coreLossOnelab.tolist(),
#         # "phiDQ_Onelab": phiDQ.to_list(),
#         # "iAmpOnelab": iAnsys.to_list(),
#     },
# )
# %%
# plot results
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=100)
phiMesh, iMesh = np.meshgrid(np.rad2deg(phi), iAnsys)
ax.scatter(np.rad2deg(phi), iAnsys, coreLossAnsys, color=cm.jet(0))
ax.scatter(np.rad2deg(phi), iAnsys, coreLossOnelab, color=cm.jet(100))
plt.show()

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=100)
# phiMesh, iMesh = np.meshgrid(np.rad2deg(phi), iAnsys)
# ax.scatter(
#     np.rad2deg(phi), iAnsys, (coreLossOnelab - coreLossAnsys) / coreLossAnsys * 100
# )
# plt.show()
