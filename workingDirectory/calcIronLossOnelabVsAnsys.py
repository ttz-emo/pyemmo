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
"""Module to test iron loss calculation"""

from __future__ import annotations

# import logging
import concurrent.futures

# %%
import os
import subprocess
import sys
import time

import numpy as np
import pandas
import scipy.io as sio

from pyemmo.definitions import RESULT_DIR, ROOT_DIR

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from pyemmo.api import json

# from pyemmo.functions import importResults as imp
from pyemmo.functions import core_loss, run_onelab

RES_DIR = (
    r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051-4HF11_TherCom"
    # + datetime.date.today().isoformat()
)


# %%
def runCalcforCurrent(stromdq):
    resId = f"id_{np.round(stromdq[0],1)}A_iq_{np.round(stromdq[1],1)}A".replace(
        ".", "_"
    )
    print(f"Running job: {resId}")
    paramDict = {
        "ID_RMS": stromdq[0],
        "IQ_RMS": stromdq[1],
        "d_theta": 5,
        "RPM": 1000,
        "ResId": resId,
        "Flag_PrintFields": 0,
        "Flag_Debug": 0,
    }
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
        cmdCommand = run_onelab.create_command(
            proFile,
            useGUI=False,
            # gmshPath=gmshPath,
            # getdpPath=getdpPath,
            params=paramDict,
            postops=["GetB"],
        )
        print("cmd command is: ", cmdCommand)
        n = 0
        while n < 5:
            try:
                subprocess.run(
                    cmdCommand,
                    capture_output=False,
                    stdout=subprocess.DEVNULL,
                    check=True,
                )
            except Exception as exce:
                print(f"Try {n}: job '{resId}' failed! Because {exce}")
                time.sleep(0.1)
                n += 1
            else:
                n = 5

    # did not save dat files... allways calc iron losses
    totalLoss = 0.0
    for side in ["rotor", "stator"]:
        bFilePath = os.path.join(resDir, f"b_{side}.pos")
        try:
            ironLoss, _ = core_loss.main(
                bFilePath,
                loss_factor={"hyst": 172.04, "eddy": 1.05, "exc": 0},
                sym_factor=4,
                axial_length=0.05,
            )
            for _, lossVals in ironLoss.items():
                totalLoss += lossVals.mean()
            # print(f"Iron losses for {resId} on {side} are: {ironLoss[side]}")
        except Exception as exce:
            print(f"Failed to calculate iron loss for '{resId}', because of: {exce}")
    return totalLoss


# %%
if __name__ == "__main__":
    # init simulations
    # RESULT_DIR = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results"
    geoFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.geo")
    mshFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.msh")
    paramFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom_param.geo")
    calFile = os.path.join(RESULT_DIR, "machine_magstadyn_a.pro")
    proFile = os.path.join(RESULT_DIR, "Test_1FE1051-4HF11_TherCom.pro")
    if not os.path.exists(proFile):
        json.main(
            geo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\Test_1FE1051-4HF11_TherCom.json",
            extInfo=r"C:\Users\ganser\AppData\Local\Programs\pyemmo\Results\matlab\Test_1FE1051-4HF11_TherCom\simuInfo.json",
            model=RESULT_DIR,
        )
    if not os.path.isdir(RES_DIR):
        os.mkdir(RES_DIR)
    # create mesh file:
    if not os.path.exists(mshFile):
        meshCommand = run_onelab.create_command(geoFile, useGUI=False)
        subprocess.run(meshCommand)

    ## simulation parameters
    ansysResPath = r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\230301_EisenverlustkennfeldAnsys.csv"
    ansysResults = pandas.read_csv(ansysResPath)
    for key in ansysResults.keys():
        if "offset_deg" in key:
            phiDQ = ansysResults[key]  # angle for dq offset in deg
        elif "I [A]" in key:
            iAnsys = ansysResults[key]
    nbrDesignPoints = len(phiDQ)

    phi = np.deg2rad(phiDQ)
    idq = np.array([iAnsys * -np.sin(phi), iAnsys * np.cos(phi)])

    # nbrSteps = 11
    # iAmp = np.linspace(0, 40, nbrSteps)
    # dqAngle = np.linspace(0, 90, nbrSteps)

    # [x, y] = np.meshgrid(iAmp, dqAngle)
    # phi = np.deg2rad(y.reshape(nbrSteps**2))
    # idq = np.array([x.reshape(nbrSteps**2) * -np.sin(phi), x.reshape(nbrSteps**2) * np.cos(phi)])

    # ironLossArray = np.zeros((nI, 2, 3))

    ##  run simulations
    ironLossArray = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(runCalcforCurrent, list(np.transpose(idq)))
        # future = executor.submit(runCalcforCurrent, list(np.transpose(idq)))
        # try:
        #     result = future.result()
        #     ironLossArray.append(result)
        # except Exception as exce:
        #     print("Process failed...")
        #     raise exce

    try:
        for result in results:
            ironLossArray.append(result)
    except Exception as exce:
        print("Process failed...")
        raise exce

    ## save data to file
    ironLossResFile = os.path.join(RES_DIR, "ironLossData.npy")
    # np.save(ironLossResFile, n)
    # np.save(ironLossResFile, idq)
    # LAST SAVE OVERWRITES FILE BY DEFAULT...
    print("save iron losses...")
    np.save(ironLossResFile, ironLossArray)

    coreLossOnelabMatFile = os.path.join(RES_DIR, "230301_ironLossDataOnelab.mat")
    sio.savemat(
        coreLossOnelabMatFile,
        {
            "coreLossOnelab": ironLossArray,
            "phiDQ_Onelab": phiDQ.tolist(),
            "iAmpOnelab": iAnsys.tolist(),
        },
    )
