"""Module to test iron loss calculation"""
# %%
import os
import sys

# import time as clockTime
import numpy as np

# import gmsh
import subprocess

# import logging
import concurrent.futures
from matplotlib import pyplot as plt
from pyemmo.definitions import ROOT_DIR, RESULT_DIR

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# from pyemmo.functions import importResults as imp
from pyemmo.functions import runOnelab
from pyemmo.functions import calcIronLoss
from pyemmo.api import json

#%%
def runCalcforCurrent(stromdq):
    resId = f"id_{np.round(stromdq[0],1)}A_iq_{np.round(stromdq[1],1)}A".replace(
        ".", "_"
    )
    print(f"Running job: {resId}")
    paramDict = {
        "ID_RMS": stromdq[0],
        "IQ_RMS": stromdq[1],
        "d_theta": 25,
        "ResId": resId,
        "Flag_PrintFields": 0,
        "Flag_Debug": 0,
    }
    RES_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"
    # gmshPath = (
    #     r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\gmsh.exe"
    # )
    # getdpPath = (
    #     r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\getdp.exe"
    # )
    proFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.pro")
    resDir = os.path.join(RES_DIR, resId)
    if not os.path.isdir(resDir):
        # only run if dir not exists
        cmdCommand = runOnelab.createCmdCommand(
            proFile,
            useGUI=False,
            # gmshPath=gmshPath,
            # getdpPath=getdpPath,
            paramDict=paramDict,
            postOperations=["GetB"],
        )
        print("cmd command is: ", cmdCommand)
        subprocess.run(cmdCommand, capture_output=False, stdout=subprocess.DEVNULL)
    # did not save dat files... allways calc iron losses
    ironLoss = {}
    totalLoss = 0
    for iSide, side in enumerate(["rotor", "stator"]):
        bFilePath = os.path.join(resDir, f"b_{side}.pos")
        ironLoss[side] = calcIronLoss.main(
            bFilePath,
            lossFactor={"hyst": 172.04, "eddy": 1.05, "exc": 0},
            symFactor=4,
            axialLength=0.05,
        )
        totalLoss += sum(ironLoss[side].values())
        print(f"Iron losses for {resId} on {side} are: {ironLoss[side]}")
    return totalLoss


if __name__ == "__main__":
    # init simulations
    # RESULT_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results"
    geoFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.geo")
    paramFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom_param.geo")
    calFile = os.path.join(RESULT_DIR, "machine_magstadyn_a.pro")
    proFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.pro")
    if not os.path.exists(proFile):
        json.main(
            geo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\Test_1FE1051-4HF11_TherCom.json",
            extInfo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\simuInfo.json",
            model=RESULT_DIR,
        )
    RES_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"

    # simulation parameters
    nI = 10
    phi = np.linspace(0, np.pi / 2, nI)
    Iamp = 40
    idq = Iamp * np.array([-np.sin(phi), np.cos(phi)])
    # ironLossArray = np.zeros((nI, 2, 3))

    ##  run simulations
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(runCalcforCurrent, list(np.transpose(idq)))

    ironLossArray = [result for result in results]

    ## save data to file
    ironLossResFile = os.path.join(RES_DIR, "ironLossData.npy")
    # np.save(ironLossResFile, n)
    # np.save(ironLossResFile, idq)
    # LAST SAVE OVERWRITES FILE BY DEFAULT...
    print("save iron losses...")
    np.save(ironLossResFile, ironLossArray)
    currentAngleFile = os.path.join(RES_DIR, "currentAngle.npy")
    np.save(currentAngleFile, phi)

    # %% plot data for check
    # elementTag, time, bData = imp.importPos(bFilePath)
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # t, e = np.meshgrid(range(bData.shape[1]), time)
    # ax.plot_surface(t, e, np.linalg.norm(bData, axis=2))

    # load loss data
    RES_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051_4HF11_TherCom"
    ironLossResFile = os.path.join(RES_DIR, "ironLossData.npy")
    ironLossArray = np.load(ironLossResFile)
    currentAngleFile = os.path.join(RES_DIR, "currentAngle.npy")
    phi = np.load(currentAngleFile)

    # plot loss data for check
    plt.rcParams["text.usetex"] = False
    fig, ax = plt.subplots(dpi=200)
    ax.plot(np.rad2deg(phi), ironLossArray)
    ironLossAnsys = [
        3.4639754269280911,
        2.4311998630198408,
        1.465993504080445,
        0.74026863038513635,
        0.43203352372358339,
        2.95170853433992,
        1.9266203194539919,
        1.063024528865669,
        0.52032317217409962,
    ]
    ironLossAnsys.sort(reverse=True)
    phiAnsys = [0, 22.5, 45, 67.5, 90, 11.25, 33.75, 56.25, 78.75]
    phiAnsys.sort()
    ax.plot(phiAnsys, ironLossAnsys)
    ax.grid()
    ax.set_xlabel("Current angle in elec deg")
    ax.set_ylabel("Total core loss in W")
    ax.set_title("Ieff=40A and n=1000rpm")
    ax.legend(["Onelab", "Ansys"])

    # from matplotlib import cm
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=300)
    # fig.set
    # t, e = np.meshgrid(np.rad2deg(phi), n)
    # ax.plot_surface(t, e, np.sum(ironLossArray[:, :, 1, :], axis=2), cmap=cm.jet)

# %%
