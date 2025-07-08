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

# import logging
import concurrent.futures

# %%
import os

# import gmsh
import sys

# import time as clockTime
import numpy as np
from matplotlib import pyplot as plt

from pyemmo.definitions import ROOT_DIR

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


# from pyemmo.functions import importResults as imp
from pyemmo.functions import runOnelab

if __name__ == "__main__":
    # set result directory
    RES_DIR = os.path.join(os.path.dirname(__file__), "res")

    # simulation parameters
    nPhi = 4
    phi = np.linspace(0, np.pi / 2, nPhi)
    nI = 4
    Imax = 79  # A
    Iamp = np.linspace(Imax / nI, Imax, nI)
    nMax = 4000
    # uncomment for speed map:
    # nN = 3
    # n = np.linspace(nMax / nN, nMax, nN)
    # only nMax
    n = nMax

    # create grid for sim
    phiMap, iMap, nMap = np.meshgrid(phi, Iamp, n)
    idMap = iMap * (-np.sin(phiMap))
    iqMap = iMap * (np.cos(phiMap))
    print(f"Number of simulations: {iMap.size}")

    # % Remove old iron loss results
    # print("Removing results...")
    # removeLossRes(iMap, phiMap, nMap, RES_DIR=RES_DIR)
    # print("Results have been removed!")

    paramDictList = []
    # %
    for i in range(iMap.size):
        # %
        idq = iMap.flat[i] * np.array([-np.sin(phiMap.flat[i]), np.cos(phiMap.flat[i])])
        resId = (
            f"id_{np.round(idq[0],1)}A"
            + f"_iq_{np.round(idq[1],1)}A"
            + f"_n_{nMap.astype(int).flat[i]}"
        ).replace(".", "_")
        paramDictList.append(
            {
                "getdp": {
                    "ID_RMS": float(idq[0]),
                    "IQ_RMS": float(idq[1]),
                    "RPM": float(nMap.flat[i]),
                    "d_theta": 0.25,
                    "ResId": resId,
                    "Flag_PrintFields": 0,
                    "Flag_Debug": 0,
                },
                "ResId": resId,
                "pro": r"C:\Users\ganser\Documents\AustauschWorkstation\FE1084-4WP11-ONELAB\Test_1FE1084-4WP11_w_39.pro",
                "res": r"C:\Users\ganser\Documents\AustauschWorkstation\FE1084-4WP11-ONELAB\res",
                "exe": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\getdp.exe",
                "gmsh": r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-230206\gmsh.exe",
                "hyst": 172.04,
                "eddy": 1.0472,
                "exc": 0,
                "axLen": 0.2,
                "sym": 4,
            }
        )

    ##  run simulations
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(runOnelab.runCalcforCurrent, paramDictList)

    res_list = [result for result in results]

    # ## save data to file
    # ironLossResFile = os.path.join(RESULT_DIR, "ironLossData.npy")
    # # np.save(ironLossResFile, n)
    # # np.save(ironLossResFile, idq)
    # # LAST SAVE OVERWRITES FILE BY DEFAULT...
    # print("save iron losses...")
    # np.save(ironLossResFile, ironLossArray)
    # currentAngleFile = os.path.join(RESULT_DIR, "currentAngle.npy")
    # np.save(currentAngleFile, phi)

    # %% plot data for check
    # elementTag, time, bData = imp.importPos(bFilePath)
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # t, e = np.meshgrid(range(bData.shape[1]), time)
    # ax.plot_surface(t, e, np.linalg.norm(bData, axis=2))

    # load loss data
    RES_DIR = (
        r"C:\Users\ganser\AppData\Roaming\pyemmo\Results\res_Test_1FE1051_4HF11_TherCom"
    )
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
