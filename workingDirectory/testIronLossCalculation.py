"""Module to test iron loss calculation"""
# %%
import os
import time as clockTime
import numpy as np
import gmsh
import subprocess
from typing import List
import logging
from matplotlib import pyplot as plt
from pyemmo.definitions import ROOT_DIR, RESULT_DIR

# from pyemmo.functions import importResults as imp
from pyemmo.functions import runOnelab
from pyemmo.functions import calcIronLoss
from pyemmo.api import json


def log_subprocess_output(pipe: subprocess.PIPE):
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        logging.info("got line from subprocess: %r", line)


# %% init simulations
# RESULT_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results"
gmshPath = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\gmsh.exe"
getdpPath = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\getdp.exe"

geoFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.geo")
paramFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom_param.geo")
proFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.pro")
calFile = os.path.join(RESULT_DIR, "machine_magstadyn_a.pro")
if not os.path.exists(proFile):
    json.main(
        geo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\Test_1FE1051-4HF11_TherCom.json",
        extInfo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\simuInfo.json",
        model=RESULT_DIR,
    )
RES_DIR = (
    r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"
)
if not os.path.isdir(RES_DIR):
    os.mkdir(RES_DIR)
# simulation parameters
nI = 10
phi = np.linspace(0, np.pi / 2, nI)
Iamp = 40
idq = Iamp * np.array([-np.sin(phi), np.cos(phi)])
ironLossArray = np.zeros((nI, 2, 3))

logging.basicConfig(
    filename=os.path.join(RES_DIR, "ironLossCalc.log"),
    filemode="w",
    format="%(levelname)s - %(message)s",
    level=logging.DEBUG,
)
# %% run simulations
processList: List[subprocess.Popen] = []
for iStrom, stromdq in enumerate(idq.transpose()):
    # gmsh.initialize()
    # gmsh.option.setNumber("General.Verbosity", 5)
    # gmsh.open(geoFile)
    # gmsh.open(proFile)
    # gmsh.merge(paramFile)
    # gmsh.merge(proFile)
    # gmsh.merge(calFile)
    # # gmsh.fltk.run()
    # gmsh.parser.setNumber("SPEED_RPM", [drehz])
    # gmsh.parser.setNumber("Id_eff", [stromdq[0]])
    # gmsh.parser.setNumber("Iq_eff", [stromdq[1]])
    # gmsh.onelab.setNumber("ANGLE_INCREMENT", [10])
    resId = f"id_{np.round(stromdq[0],1)}A_iq_{np.round(stromdq[1],1)}A".replace(
        ".", "_"
    )
    # gmsh.parser.setString("ResId", resId)
    # # gmsh.onelab.run(command="check")
    # gmsh.finalize()
    # 0f", ID_RMS);
    # 0f", IQ_RMS);
    # f", d_theta);
    # RPM);
    # ResId());
    paramDict = {
        "ID_RMS": stromdq[0],
        "IQ_RMS": stromdq[1],
        "d_theta": 10,
        "ResId": resId,
    }
    resDir = os.path.join(RES_DIR, resId)
    if not os.path.isdir(resDir):
        # only run if dir not exists
        cmdCommand = runOnelab.createCmdCommand(
            proFile,
            False,
            gmshPath=gmshPath,
            # getdpPath=getdpPath,
            logFileName=f"gmsh{resId}.log",
            paramDict=paramDict,
            postOperations=["GetB"],
        )
        # processList.append(
        #     subprocess.Popen(cmdCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # )
        logging.debug("running simlation %s", resId)
        gmshProc = subprocess.Popen(
            cmdCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        with gmshProc.stdout:
            log_subprocess_output(gmshProc.stdout)
        # gmshProc.communicate()
        exitCode = gmshProc.wait()
        # gmshProc.terminate()

    # did not save dat files... allways calc iron losses
    for iSide, side in enumerate(["rotor", "stator"]):
        logging.debug("Calculating iron loss for simulation: %s", resId)
        bFilePath = os.path.join(resDir, f"b_{side}.pos")
        ironLoss = calcIronLoss.main(
            bFilePath,
            lossFactor={"hyst": 172, "eddy": 1, "exc": 0},
            symFactor=4,
            axialLength=0.05,
        )
        # logging.debug("iron loss for simulation '%s' is:", resId)
        # (f"Iron losses for {resId} on {side} are: {ironLoss}")
        ironLossArray[iStrom, iSide, :] = list(ironLoss.values())
# %% save data to file
ironLossResFile = os.path.join(RES_DIR, "ironLossData.npy")
# np.save(ironLossResFile, n)
# np.save(ironLossResFile, idq)
# LAST SAVE OVERWRITES FILE BY DEFAULT...
np.save(ironLossResFile, ironLossArray)

# %%
# gmsh.initialize()
# gmsh.option.setNumber("General.Verbosity", 1)

# %% plot data for check
# elementTag, time, bData = imp.importPos(bFilePath)
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# t, e = np.meshgrid(range(bData.shape[1]), time)
# ax.plot_surface(t, e, np.linalg.norm(bData, axis=2))
#
# %% load loss data
ironLossResFile = os.path.join(RES_DIR, "ironLossData.npy")
ironLossArray = np.load(ironLossResFile)

# %% plot loss data for check
from matplotlib import cm

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=300)
# fig.set
# t, e = np.meshgrid(np.rad2deg(phi), n)
# ax.plot_surface(t, e, np.sum(ironLossArray[:, :, 1, :], axis=2), cmap=cm.jet)

# %%
