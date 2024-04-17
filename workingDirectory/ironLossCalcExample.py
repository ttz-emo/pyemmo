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
import gmsh
import sys, os
import numpy as np
import time as clockTime
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog

from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.calcIronLoss import write_simple

viewPos = [2, 3, 4, 5]


# %%
def intAndPlot(viewTag, symFactor, axLen, time, filePath, plotName: str):
    """Integrate that loss data over time with gmsh"""
    # integrate doesn't need the internal tag, but the number of the view in the actual
    # views (starting at 0)
    gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(viewTag))
    intViewTag = gmsh.plugin.run("Integrate")
    # get list data from integral to adjust results by symmetry factor and machine length
    # and show them as xy plot in gmsh
    dtype, numElem, intData = gmsh.view.getListData(intViewTag)
    # skip unnecessary list and scale results by symmmetry and machine length:
    assert len(intData) == 1  # make sure there is only one element
    # P_HystData = P_HystData[0] * symFactor * axLen
    intData = intData[0]  # extract data from list
    intData[3:] = intData[3:] * symFactor * axLen
    # first 3 values are point coorinates to plot results (unimportant, could be changd too...)

    gmsh.view.remove(intViewTag)  # remove old integral view
    intViewTag = gmsh.view.add(plotName)  # add new view for xy plot
    gmsh.view.addListData(
        tag=intViewTag, dataType=dtype[0], numEle=numElem[0], data=intData
    )

    # set view options
    gmsh.view.option.setNumber(intViewTag, "Type", 3)
    gmsh.view.option.setNumber(intViewTag, "TimeStep", len(time) - 1)
    gmsh.view.option.setNumber(intViewTag, "IntervalsType", 3)
    # RangeType:
    # 1: default, 2: custom, 3: per time step
    gmsh.view.option.setNumber(intViewTag, "RangeType", 2)

    gmsh.view.option.setNumber(intViewTag, "CustomMin", 0)
    gmsh.view.option.setNumber(intViewTag, "CustomMax", np.max(intData) * 1.2)
    # 0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler
    gmsh.view.option.setNumber(
        intViewTag, "Axes", viewPos[viewTag % 4]
    )  # FIXME

    # 0: manual, 1: automatic, 2: top left, 3: top right, 4: bottom left, 5: bottom right,
    # 6: top, 7: bottom, 8: left, 9: right, 10: full, 11: top third, 12: in model coordinatess
    gmsh.view.option.setNumber(intViewTag, "AutoPosition", 2)

    # save integral data as .dat file
    # gmsh.view.write(P_hystView, pFilePath)
    write_simple(
        filePath, time, intData[3:]
    )  # skip point coordinates in export
    # had to write new function here because gmsh newer version .dat format does not match
    # the old getdp format for import with matlab
    return intViewTag, intData


def printHomogenousModelData(
    values: np.ndarray,
    time: np.ndarray,
    tags: np.ndarray,
    viewName: str,
    resDir: str,
    resFileName: str,
):
    """print amplitude of B elementwise in Gmsh

    Args:
        values (np.ndarray): array of magnitudes (elementwise)
        time (np.ndarray): time vector
        tags (list[int]): mesh element list
        resDir (str): path to results directory
        viewName (str): name of view.
    """
    model = gmsh.model.getCurrent()  # or just get current model...
    BmView = gmsh.view.add(viewName)  # get tag of new view
    for step in range(len(time) - 1):
        gmsh.view.addHomogeneousModelData(
            tag=BmView,
            step=step + 1,
            modelName=model,
            dataType="ElementData",
            tags=tags,
            data=values[step],
            time=time[step],
        )
    # save field to file:
    pFilePath = os.path.join(resDir, resFileName)
    gmsh.view.write(BmView, pFilePath)


def printModelData(
    values: np.ndarray,
    time: np.ndarray,
    tags: np.ndarray,
    viewName: str,
    resDir: str,
    resFileName: str,
):
    """print amplitude of B elementwise in Gmsh

    Args:
        values (np.ndarray): array of vector values (elementwise)
        time (np.ndarray): time vector
        tags (list[int]): mesh element list
        viewName (str): name of view.
        resDir (str): path to results directory
        resFileName (str): name of pos file
    """
    model = gmsh.model.getCurrent()  # or just get current model...
    newView = gmsh.view.add(viewName)  # get tag of new view
    for step in range(len(time) - 1):
        gmsh.view.addModelData(
            tag=newView,
            step=step + 1,
            modelName=model,
            dataType="ElementData",
            tags=tags,
            data=values[step],
            time=time[step],
        )
    # save field to file:
    posFilePath = os.path.join(resDir, resFileName)
    gmsh.view.write(newView, posFilePath)


def ironLossInteractive(
    bFilePath: os.PathLike,
    axLen: float,
    lossParams: tuple,
    symFactor: int,
    elemId: int,
):
    """_summary_

    Args:
        bFilePath (os.PathLike): _description_

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        ValueError: _description_
    """
    finGmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize(sys.argv)  # init gmsh
        finGmsh = True  # if gmsh wasn't init before -> close it a the end
    tstart = clockTime.time()

    gmsh.option.setNumber("General.Verbosity", 3)

    # Import B-field for stator (with x,y,z components)
    # bFilePath = os.path.join(
    #     ROOT_DIR, "workingDirectory", "testPosImport", "res_30000rpm_0A", "b_stator.pos"
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
    tend = clockTime.time()
    resDir, fileName = os.path.split(bFilePath)
    try:
        machineSide = fileName.split(".")[0].split("_")[1]
    except Exception:
        machineSide = ""

    print(f"\nImport of {fileName} took {tend-tstart} seconds.\n")

    # %% Import data from view
    print("Importing model data into python...")
    tstart = clockTime.time()
    # number of time steps
    actTag = gmsh.view.getTags()[-1]
    NBR_STEPS = int(gmsh.view.option.getNumber(tag=actTag, name="NbTimeStep"))
    if NBR_STEPS < 2:
        raise ValueError("Only one timestep!")

    time = []  # init time array

    # get values of first time for init
    dType, btags, gdata, gtime, numComp = gmsh.view.getModelData(
        tag=actTag, step=0
    )
    # dType, gtags, gdata, gtime, numComp = gmsh.view.getHomogeneousModelData(1, 0) # does
    # the same thing, but data is 1x3*N instead of 3xN (with N = number of triangles)
    nbrElements = len(btags)
    B_Data = np.zeros((NBR_STEPS, len(gdata), numComp))  # allocate memory
    dBdt = np.zeros((NBR_STEPS - 1, len(gdata), numComp))

    B_Data[0] = np.array(gdata)[:, :numComp]  # set first time step vaues
    time.append(gtime)

    # normB = np.linalg.norm(B_Data, axis=2)
    # bmin = bmax =  normB[0] # init bmin and bmax array
    bmin = bmax = B_Data[0]  # init bmin and bmax array

    # get data for each time step
    for step in range(1, NBR_STEPS):
        dType, ctags, cdata, ctime, numComp = gmsh.view.getModelData(
            actTag, step
        )
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
        dBdt[step - 1] = (B_Data[step] - B_Data[step - 1]) / (
            time[step] - time[step - 1]
        )
    tend = clockTime.time()
    print(f"\nImport and reading of data took {tend-tstart} seconds.\n")
    # %% Plot B_min, b_max for x and y component over element number
    if elemId is None:
        elemId = 0
    else:
        elemId = np.where(btags == elemId)[0][0]
    tstart = clockTime.time()

    # fig, axes = plt.subplots(nrows=1, ncols=2)
    # ax = axes[0]
    # ax.plot(ctags, bmax[:, 0])
    # ax.plot(ctags, bmin[:, 0])
    # ax.legend(["B_max", "B_min"])
    # ax.set_xlabel("Element number")
    # ax.set_ylabel("B in T")
    # ax.set_title("B_x")

    # ax = axes[1]
    # ax.plot(ctags, bmax[:, 1])
    # ax.plot(ctags, bmin[:, 1])
    # ax.legend(["B_max", "B_min"])
    # ax.set_xlabel("Element number")
    # ax.set_ylabel("B in T")
    # ax.set_title("B_y")

    # # Plot amplitude of B_x and B_y
    # fig, ax = plt.subplots()
    # # ax.plot(bmax-bmin)
    # ax.semilogy(ctags, bmax[:, 0] - bmin[:, 0])
    # ax.semilogy(ctags, bmax[:, 1] - bmin[:, 1])
    # # ax.legend(["$\Delta$B"])
    # ax.set_title("$\Delta$B")
    # ax.legend(["B_x", "B_y"])
    # ax.set_xlabel("Element number")
    # ax.set_ylabel("B in T")
    # ax.grid(True)

    # %% Calculate hysteresis losses

    print("Calculating hysteresis losses...")
    sigma_h = lossParams[0]  # hysteresis loss factor
    Bm = (bmax - bmin) / 2  # magnitude is (max-min)/2

    printHomogenousModelData(
        [np.linalg.norm(Bm, axis=1)],
        [0],
        btags,
        viewName=f"Amplitude of B ({machineSide})",
        resDir=resDir,
        resFileName=f"B_m_{machineSide}.pos",
    )
    printModelData(
        dBdt,
        time[0:-1],
        btags,
        f"dB/dt ({machineSide})",
        resDir=resDir,
        resFileName=f"dBdt_{machineSide}",
    )
    gmsh.fltk.run()

    BmArray = np.tile(Bm, (NBR_STEPS, 1, 1))
    BminArray = np.tile(bmin, (NBR_STEPS, 1, 1))
    # phaseB = np.arcsin(np.divide(B_Data-np.mean(B_Data,axis=0),BmArray))
    bMeanFree = B_Data - BminArray - BmArray
    if False:
        # first try: calculate cos(phi) by means of cos(arcsin(B)) = sqrt(1 - (b/bm)^2), but
        # calculating phi from arcsin doesn't work, because it gives values from -pi to pi
        # instead of 0 to 2*pi
        bAC2 = bMeanFree**2
        BzuBamp = np.divide(bAC2, BmArray**2)
        cosPhi = np.sqrt(1 - BzuBamp)
    else:
        if False:
            # calculating phi from arcsin doesn't work, because it gives values from -pi to pi
            # instead of 0 to 2*pi... Would need to do a case distinction.
            phi = np.arcsin(
                bMeanFree / BmArray
            )  # FIXME: dont need to calc all values
            phi0 = phi[0, :, :]
        else:
            # second try with phase from fft
            bfft = np.fft.rfft(B_Data[:-1, :, :], axis=0)
            amp = np.abs(bfft)
            nbrFreqs = int(np.round((NBR_STEPS - 1) / 2))
            amp = np.concatenate(
                ([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0
            )
            phase = np.angle(bfft)
            tStep = time[1]
            freqs = np.abs(
                np.fft.fftfreq(NBR_STEPS - 1, tStep)[: nbrFreqs + 1]
            )

            # find phi0 by fft
            for elem in range(nbrElements):
                # FIXME: Assume that freq. of max. amplitude is the same for x and y comp.
                #   -> norm                                         +1 because skipping DC
                fMaxInd = np.linalg.norm(amp[1:, elem, :], axis=1).argmax() + 1
                phi0 = phase[fMaxInd, :, :]
            # find phi0 by detecting zero points
            zero_crossings = np.where(np.diff(np.sign(B_Data), axis=0))[0]

            # fMaxIndex equals order of that spectral part
            phi = np.linspace(
                phi0 + np.pi / 2,
                fMaxInd * (2 * np.pi) + phi0 + np.pi / 2,
                NBR_STEPS,
            )
        # calc cos(phi)
        cosPhi = np.cos(phi)
    Hm = 1 / np.pi * sigma_h * Bm  # magnitude of H according to paper
    Hirr = Hm * cosPhi

    # Plot Bm and Hm over element number
    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax1 = axes[0]
    ax1.plot(time, bMeanFree[:, elemId, 0] / np.max(bMeanFree[:, elemId, 0]))
    ax1.set_xlabel("time in s")
    ax1.set_ylabel(r"$B/B_{\mathrm{max}}$")
    ax1.yaxis.label.set_color("C0")
    ax1.tick_params(axis="y", colors="C0")
    # ax1.grid(color="C0")
    ax1.set_title("x-Comp")
    ax1.grid(True)

    ax12 = ax1.twinx()
    ax12.plot(time, Hirr[:, elemId, 0] / np.max(Hirr[:, elemId, 0]), "C1")
    ax12.yaxis.label.set_color("C1")
    ax12.tick_params(axis="y", colors="C1")
    ax12.set_ylabel(r"$H_{\mathrm{irr}}/H_{\mathrm{irr,max}}$")

    ax2 = axes[1]
    ax2.plot(time, bMeanFree[:, elemId, 1] / np.max(bMeanFree[:, elemId, 1]))
    ax2.set_xlabel("time in s")
    ax2.set_ylabel(r"$B/B_{\mathrm{max}}$")
    ax2.yaxis.label.set_color("C0")
    ax2.tick_params(axis="y", colors="C0")
    # ax2.grid(color="C0")
    ax2.set_title("y-Comp")
    ax2.grid(True)

    ax21 = ax2.twinx()
    ax21.plot(time, Hirr[:, elemId, 1] / np.max(Hirr[:, elemId, 1]), "C1")
    ax21.yaxis.label.set_color("C1")
    ax21.tick_params(axis="y", colors="C1")
    ax21.set_ylabel(r"$H_{\mathrm{irr}}/H_{\mathrm{irr,max}}$")
    fig.tight_layout()

    # Plot x and y comp. of Bm and Hm over element number
    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax1 = axes[0]
    ax1.plot(time, bMeanFree[:, elemId, 0])
    ax1.plot(time, bMeanFree[:, elemId, 1])
    ax1.set_xlabel("time in s")
    ax1.set_ylabel("B in T")
    ax1.legend(["x", "y"])
    # ax1.set_title("B field in T")
    ax1.grid()
    ax2 = axes[1]
    ax2.plot(time, Hirr[:, elemId, 0])
    ax2.plot(time, Hirr[:, elemId, 1])
    ax2.set_xlabel("time in s")
    ax2.set_ylabel("H in A/m")
    ax2.legend(["x", "y"])
    # ax2.set_title("$H_{\mathrm{irr}}$ in A/m")
    ax2.grid()
    fig.tight_layout()

    # Plot Ellipsis
    fig, ax = plt.subplots()
    ps = ax.plot(
        Hirr[:, elemId, :] / np.max(Hirr[:, elemId, :]),
        bMeanFree[:, elemId, :] / np.max(bMeanFree[:, elemId, :]),
    )
    ps[0].set_color("C3")
    ps[1].set_color("C4")
    ax.grid(True)
    ax.set_xlabel(r"$H_{\mathrm{irr}}/H_{\mathrm{irr,max}}$")
    ax.set_ylabel(r"$B/B_{\mathrm{max}}$")
    ax.legend(["x", "y"])
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    # ax.set_title("EEL for Stator-Element")
    # Calculate hysteresis loss on element bases for all time steps
    # beta = 2
    ph = np.sum(
        np.abs(Hirr[1:] * dBdt), axis=2
    )  # + np.abs(Hm * dBdt[:, :, 1])

    # %% Export loss data to gmsh
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
    pFilePath = os.path.join(resDir, f"p_hyst_{machineSide}.pos")
    gmsh.view.write(pHystView, pFilePath)
    # %% Integrate that loss data over time with gmsh
    # integrate doesn't need the internal tag, but the number of the view in the actual
    # views (starting at 0)
    # gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(pHystView))
    # P_h_ViewTag = gmsh.plugin.run("Integrate")
    # # get list data from integral to adjust results by symmetry factor and machine length
    # # and show them as xy plot in gmsh
    # dtype, numElem, P_HystData = gmsh.view.getListData(P_h_ViewTag)
    # # skip unnecessary list and scale results by symmmetry and machine length:
    # assert len(P_HystData) == 1  # make sure there is only one element
    # # P_HystData = P_HystData[0] * symFactor * axLen
    # P_HystData = P_HystData[0]  # extract data from list
    # P_HystData[3:] = P_HystData[3:] * symFactor * axLen
    # # first 3 values are point coorinates to plot results (unimportant, could be changd too...)

    # gmsh.view.remove(P_h_ViewTag)  # remove old integral view
    # P_h_ViewTag = gmsh.view.add("Hystersis Loss [W]")  # add new view for xy plot
    # gmsh.view.addListData(
    #     tag=P_h_ViewTag, dataType=dtype[0], numEle=numElem[0], data=P_HystData
    # )

    # # set view options
    # gmsh.view.option.setNumber(P_h_ViewTag, "Type", 3)
    # gmsh.view.option.setNumber(P_h_ViewTag, "TimeStep", NBR_STEPS - 1)
    # gmsh.view.option.setNumber(P_h_ViewTag, "IntervalsType", 3)
    # # RangeType:
    # # 1: default, 2: custom, 3: per time step
    # gmsh.view.option.setNumber(P_h_ViewTag, "RangeType", 2)

    # gmsh.view.option.setNumber(P_h_ViewTag, "CustomMin", 0)
    # gmsh.view.option.setNumber(P_h_ViewTag, "CustomMax", np.max(P_HystData) * 1.2)
    # # 0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler
    # gmsh.view.option.setNumber(P_h_ViewTag, "Axes", 3)
    # # 0: manual, 1: automatic, 2: top left, 3: top right, 4: bottom left, 5: bottom right,
    # # 6: top, 7: bottom, 8: left, 9: right, 10: full, 11: top third, 12: in model coordinatess
    # gmsh.view.option.setNumber(P_h_ViewTag, "AutoPosition", 2)

    # # save integral data as .dat file
    # pFilePath = os.path.join(resDir, f"p_hyst_{machineSide}.dat")
    # # gmsh.view.write(P_hystView, pFilePath)
    # writeSimple(pFilePath, time, P_HystData[3:])  # skip point coordinates in export
    # # had to write new function here because gmsh newer version .dat format does not match
    # # the old getdp format for import with matlab
    P_h_ViewTag, P_HystData = intAndPlot(
        pHystView,
        symFactor,
        axLen,
        time,
        os.path.join(resDir, f"p_hyst_{machineSide}.dat"),
        "Hystersis Loss [W]",
    )

    # %% calculate FREQUENCY BASED hysteresis losses
    # calculate element wise fft of b-field
    bfft = np.fft.rfft(B_Data[:-1, :, :], axis=0)
    amp = np.abs(bfft)
    phase = np.angle(bfft)
    nbrFreqs = int(np.round((NBR_STEPS - 1) / 2))
    # to get correct amplitude regarding the specific frequencies, the amplitudes
    # must be corrected by 1/nbrFreqs and DC-part by 1/(2*nbrFreqs) because its value
    # is doubled since its part of the positive and negative side of the spectrum.
    # Since I defined the number of frequencies to be only for the one sided spectrum,
    # we have to double the value for amp[0] and use only nbrFreqs for amp[1:]
    amp = np.concatenate(
        ([amp[0] / nbrFreqs / 2], amp[1:] / (nbrFreqs)), axis=0
    )
    tStep = time[1]
    freqs = np.abs(
        np.fft.fftfreq(NBR_STEPS - 1, tStep)[: nbrFreqs + 1]
    )  # +1 because DC-signal

    # idx = np.argsort(freqs)
    # elemId = 0  #

    fig, ax = plt.subplots()
    bars = ax.bar(
        freqs[1:], amp[1:, elemId, 0], 10
    )  # 1: because skiping DC-part to see main harmonics
    ax.bar_label(bars, fmt="%.4f")
    ax.set_title("x- and y-comp of B")
    fig, ax = plt.subplots()
    bars = ax.bar(
        freqs[1:], amp[1:, elemId, 1], 5
    )  # 1: because skiping DC-part to see main harmonics
    ax.set_title("norm(B)")
    # bars = plt.bar(freqs[1:], amp[1:,elemId,2],10) # 1: because skiping DC-part to see main harmonics
    ax.bar_label(bars, fmt="%.4f")
    # plt.bar(freqs, amp[:,elemId],10) # full spectrum

    # plot b field of element over time
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(time, B_Data[:, elemId, 0], label="x-comp")
    axs[0].plot(time, B_Data[:, elemId, 1], label="y-comp")
    axs[1].plot(
        time, np.linalg.norm(B_Data[:, elemId, :], axis=1), label="y-comp"
    )
    axs[0].grid(True)
    axs[1].grid(True)
    # ax.legend(("x", "y"))
    # Mittelwert des Zeitverlaufs (DC)
    print(
        f"Mittelwert der x- und y Komponente von B für Element {elemId}: {np.mean(B_Data[:,elemId,[0,1]],axis=0)}"
    )

    fig, ax = plt.subplots()
    bars = ax.bar(
        freqs[1:] / freqs[1],
        np.linalg.norm(np.mean(amp[1:, :, :], axis=1), axis=1),
        3,
    )
    ax.set_title("Mean Hysteresis loss (over elements)")
    ax.set_ylabel("Loss Density [W/m³]")
    ax.set_xlabel("Harmonic")
    # # bars = plt.bar(freqs[1:], amp[1:,elemId,2],10) # 1: because skiping DC-part to see main harmonics
    # ax.bar_label(bars, fmt="%.1e")

    # Field plot in gmsh
    # norm of x,y,z components over the sum of all frequencies
    # phFreq = np.linalg.norm(
    #     np.sum(sigma_h * freqs * (amp.transpose() ** 2), axis=2), axis=0
    # )
    # norm of xyz comp.
    phFreq = np.linalg.norm(sigma_h * freqs * (amp.transpose() ** 2), axis=0)
    pHFreqView = gmsh.view.add(
        "Hystersis Loss (FFT) [W/m³]"
    )  # get tag of new view
    gmsh.view.addHomogeneousModelData(
        tag=pHFreqView,
        step=0,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=np.sum(phFreq, axis=1),
        time=0,
    )
    # plot loss density over frequency
    pHFreqView2 = gmsh.view.add(
        f"Hystersis Loss (FFT) harmonic (f0={freqs[1]:.1f}) [W/m³]"
    )  # get tag of new view
    for i, freq in enumerate(freqs):
        gmsh.view.addHomogeneousModelData(
            tag=pHFreqView2,
            step=i,
            modelName=model,
            dataType="ElementData",
            tags=btags,
            data=phFreq[:, i],
            time=freq / freqs[1],  # /(1/time[-1]), # time harmonic
        )
    # 0: none, 1: time series, 2: harmonic data, 3: automatic, 4: step data, 5: multi-step data,
    # 6: real eigenvalues, 7: complex eigenvalues
    gmsh.view.option.setNumber(pHFreqView2, "ShowTime", 2)
    # plot mean Value of time domain hysteresis losses for comparison
    pHMeanView = gmsh.view.add(
        "Hystersis Loss (Time Domain, mean) [W/m³]"
    )  # get tag of new view
    gmsh.view.addHomogeneousModelData(
        tag=pHMeanView,
        step=0,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=np.mean(ph, axis=0),
        time=0,
    )
    # save p_hyst-field to file:
    pFilePath = os.path.join(resDir, f"p_hyst_freq_{machineSide}.pos")

    # add frequency calculation plot in gmsh
    gmsh.view.write(pHFreqView, pFilePath)
    gmsh.plugin.setNumber("Integrate", "View", gmsh.view.getIndex(pHFreqView))
    intViewTag = gmsh.plugin.run("Integrate")
    # get list data from integral to adjust results by symmetry factor and machine length
    # and show them as xy plot in gmsh
    dtype, numElem, PHystFreq = gmsh.view.getListData(intViewTag)
    # skip unnecessary list and scale results by symmmetry and machine length:
    assert len(PHystFreq) == 1  # make sure there is only one element
    PHystFreq = PHystFreq[0]  # extract data from list
    PHystFreq[3:] = PHystFreq[3:] * symFactor * axLen
    # first 3 values are point coorinates to plot results (unimportant, could be changd too...)
    print(f"Hysteresis Loss calculated via frequency: {PHystFreq[3]:.3}  W")

    # save integral data as .dat file
    pFilePath = os.path.join(resDir, f"p_hyst_freq_{machineSide}.dat")
    write_simple(
        pFilePath, [0], PHystFreq[3:]
    )  # skip point coordinates in export

    # %% Calculate EDDY CURRENT LOSSES ---------------------------------------------------
    print("Calculating eddy current losses...")

    kc = lossParams[1]  # loss parameter
    # loss function for eddy current loss from paper:
    pi2 = np.square(np.pi)
    pc = kc / (2 * pi2) * (np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1]))
    # Export data to gmsh
    model = gmsh.model.getCurrent()  # get current model
    eddyCurrentView = gmsh.view.add(
        "Eddy Current Loss [W/m³]"
    )  # get tag of new view
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
    pFilePath = os.path.join(resDir, f"p_eddy_{machineSide}.pos")
    gmsh.view.write(eddyCurrentView, pFilePath)

    # EDDY CURRENTS VIA FREQUENCY ---------------------------------------------------
    # norm of xyz comp.
    pcFreq = np.linalg.norm(kc * freqs**2 * (amp.transpose() ** 2), axis=0)
    pcFreqView = gmsh.view.add(
        "Eddy Current Loss (FFT) [W/m³]"
    )  # get tag of new view
    gmsh.view.addHomogeneousModelData(
        tag=pcFreqView,
        step=0,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=np.sum(pcFreq, axis=1),
        time=0,
    )
    # plot loss density over frequency
    pcFreqView2 = gmsh.view.add(
        f"Eddy Current Loss (FFT) harmonic (f0={freqs[1]:.1f}) [W/m³]"
    )  # get tag of new view
    for i, freq in enumerate(freqs):
        gmsh.view.addHomogeneousModelData(
            tag=pcFreqView2,
            step=i,
            modelName=model,
            dataType="ElementData",
            tags=btags,
            data=pcFreq[:, i],
            time=freq / freqs[1],  # /(1/time[-1]), # time harmonic
        )
    # 0: none, 1: time series, 2: harmonic data, 3: automatic, 4: step data, 5: multi-step data,
    # 6: real eigenvalues, 7: complex eigenvalues
    gmsh.view.option.setNumber(pHFreqView2, "ShowTime", 2)

    # %% Integrate
    # Integrate Eddy Current losses ---------------------------------------------------
    gmsh.plugin.setNumber(
        "Integrate", "View", gmsh.view.getIndex(eddyCurrentView)
    )
    integralView = gmsh.plugin.run("Integrate")
    # get list data from integral to determine maximum and set y limits in plot
    dtype, numElem, P_eddyData = gmsh.view.getListData(integralView)

    assert len(P_eddyData) == 1  # make sure there is only one element
    P_eddyData = P_eddyData[0] * symFactor * axLen

    gmsh.view.remove(integralView)
    integralView = gmsh.view.add("Eddy Current Loss [W]")
    # replace data in view with recalculated data
    gmsh.view.addListData(
        tag=integralView, dataType=dtype[0], numEle=numElem[0], data=P_eddyData
    )

    # set options to display integral as xy plot
    # gmsh.view.option.setString(integralView,"Type",)
    gmsh.view.option.copy(
        P_h_ViewTag, integralView
    )  # copy options from first plot
    gmsh.view.option.setNumber(
        integralView, "CustomMax", np.max(P_eddyData) * 1.2
    )
    gmsh.view.option.setNumber(integralView, "AutoPosition", 3)  # 3: top right

    # save integral values to file
    pFilePath = os.path.join(resDir, f"p_eddy_{machineSide}.dat")
    write_simple(pFilePath, time, P_eddyData[3:])

    # %% Calculate EXCESS LOSS ---------------------------------------------------
    ke = lossParams[
        2
    ]  # factor was 0 in model... used greater value for testing
    if np.abs(ke) > 1e6:
        Ce = 8.763363  # constant factor (from paper)
        pe = (
            ke
            / Ce
            * np.power(
                (np.square(dBdt[:, :, 0]) + np.square(dBdt[:, :, 1])), 0.75
            )
        )
        # % Export data to gmsh
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
        pFilePath = os.path.join(resDir, f"p_exc_{machineSide}.pos")
        gmsh.view.write(excessView, pFilePath)

        # %% Integrate Excess losses ---------------------------------------------------
        gmsh.plugin.setNumber(
            "Integrate", "View", gmsh.view.getIndex(excessView)
        )
        integralView = gmsh.plugin.run("Integrate")

        # get list data from integral to determine maximum and set y limits in plot
        dtype, numElem, P_excData = gmsh.view.getListData(integralView)

        # skip unnecessary list and scale results by symmmetry and machine length:
        assert len(P_excData) == 1  # make sure there is only one element
        P_excData = P_excData[0] * symFactor * axLen

        gmsh.view.remove(integralView)
        integralView = gmsh.view.add("Excess Losses [W]")
        # replace data in view with recalculated data
        gmsh.view.addListData(
            tag=integralView,
            dataType=dtype[0],
            numEle=numElem[0],
            data=P_excData,
        )
        gmsh.view.option.copy(P_h_ViewTag, integralView)
        gmsh.view.option.setNumber(
            integralView, "CustomMax", np.max(P_excData) * 1.2
        )
        gmsh.view.option.setNumber(
            integralView, "AutoPosition", 4
        )  # 4: bottom left

        # save integral values to file
        pFilePath = os.path.join(resDir, f"P_exc_{machineSide}.dat")
        write_simple(pFilePath, time, P_excData[3:])
    else:
        pe = np.zeros(ph.shape)
        P_excData = np.zeros(P_HystData.shape)
    # %% Print sum of all losses
    totalLossView = gmsh.view.add(
        "Total Core Loss [W/m³]"
    )  # get tag of new view
    pCore = ph + pc + pe
    for step in range(len(time) - 1):
        # write every time step (except first, because derivative) to view
        gmsh.view.addHomogeneousModelData(
            tag=totalLossView,
            step=step + 1,
            modelName=model,
            dataType="ElementData",
            tags=btags,
            data=pCore[step, :],
            time=time[step],
        )
    # save new view data in pos file
    pFilePath = os.path.join(resDir, f"p_core_{machineSide}.pos")
    gmsh.view.write(totalLossView, pFilePath)
    # %% Calc mean of all losses on elements ---------------------------------------------------
    pTotal_mean = np.mean(pCore, axis=0)
    # Export mean data
    model = gmsh.model.getCurrent()  # or just get current model...
    pHystView = gmsh.view.add("Mean Total Loss [W/m³]")  # get tag of new view
    gmsh.view.addHomogeneousModelData(
        tag=pHystView,
        step=0,
        modelName=model,
        dataType="ElementData",
        tags=btags,
        data=pTotal_mean,
        time=0,
    )

    # %% sum of Losses
    # Add up iron losses and plot
    Ptotal = P_HystData + P_eddyData + P_excData
    print(f"Rms of total iron losses: {np.sqrt(np.mean(np.square(Ptotal)))}")
    viewPsum = gmsh.view.add("Total Iron Losses [W]")
    gmsh.view.addListData(viewPsum, dtype[0], numElem[0], Ptotal)

    gmsh.view.option.copy(integralView, viewPsum)
    gmsh.view.option.setNumber(viewPsum, "CustomMax", np.max(Ptotal) * 1.2)
    gmsh.view.option.setNumber(viewPsum, "AutoPosition", 5)  # 5: bottom right

    pFilePath = os.path.join(resDir, "p_total.dat")
    write_simple(pFilePath, time, Ptotal[3:])

    tend = clockTime.time()
    # print(f"\nTotal iron loss calculation and plotting took {tend-tstart} seconds.\n")

    if finGmsh:
        gmsh.finalize()

    print("-------------------------------------------------------")
    return (P_HystData, P_eddyData, P_excData)


if __name__ == "__main__":
    # root = tk.Tk()
    # root.withdraw()
    # initFilePath = filedialog.askopenfilename()

    # if os.path.isfile(initFilePath):
    #     resDir = os.path.dirname(initFilePath)
    # else:
    #     raise ValueError(
    #         f"Given B field ('b_rotor.pos' or 'b_stator.pos') file ('{initFilePath}') not found!"
    #     )

    lossParams = (172.04, 1.047, 0)
    # RES_DIR = r"C:\TEMP\res_Id=0_Iq=0_1000rpm"
    # elemId = {
    #     "rotor": 1637,
    #     "stator": 4574,
    # }
    RES_DIR = "C:/temp"
    elemId = {
        "rotor": 7767,
        "stator": 18605,
    }

    # lossParams = (165.9694, 1.0529, 0)
    # RES_DIR = r"C:\Users\ganser\Documents\PyDraft\Austausch Siemens\230321_DebugEisenverlusteReluktanz\Results\res__1PH8138_7xD0_Reluktanz"
    # elemId = {
    #     "rotor": 16259,
    #     "stator": 40503,
    # }
    # RES_DIR = r"C:\Users\ganser\Documents\PyDraft\Austausch Siemens\230321_DebugEisenverlusteReluktanz\Results\res__1PH8138_7xD0_Reluktanz_182Steps"
    # elemId = {
    #     "rotor": 12803,
    #     "stator": 27545,
    # }
    gmsh.initialize()
    resDict = {}
    for side in ["rotor", "stator"]:
        print("-------------------------------------------------------")
        print("Iron loss calculation for " + side)
        filepath = os.path.join(RES_DIR, f"b_{side}.pos")
        resDict[side] = ironLossInteractive(
            bFilePath=filepath,
            axLen=0.31,
            lossParams=lossParams,
            symFactor=4,
            elemId=elemId[side],
        )
    sumLoss = np.array([0, 0, 0], dtype="float64")  # init sum section
    for side, lossVals in resDict.items():
        print(f"{side.upper()} LOSSES:")
        print(f"{'Hysteresis: ' : <15}" + str(np.mean(lossVals[0][3:])))
        print(f"{'Eddy-Current: ' : <15}" + str(np.mean(lossVals[1][3:])))
        print(f"{'Excess: ' : <15}" + str(np.mean(lossVals[2][3:])) + "\n")
        sumLoss += [
            np.mean(lossVals[0][3:]),
            np.mean(lossVals[1][3:]),
            np.mean(lossVals[2][3:]),
        ]
    print("SUM LOSSES")
    print(f"{'Hysteresis: ' : <15}{sumLoss[0]}")
    print(f"{'Eddy-Current: ' : <15}{sumLoss[1]}")
    print(f"{'Excess: ' : <15}{sumLoss[2]}" + "\n")
    # Add display sum of iron loss parts and plot
    # Ptotal = P_HystData + P_eddyData + P_excData
    # print(f"Rms of total iron losses: {np.sqrt(np.mean(np.square(Ptotal)))}")
    # viewPsum = gmsh.view.add("Total Iron Losses [W]")
    # gmsh.view.addListData(viewPsum, "SP", 1, Ptotal)

    # gmsh.view.option.copy(integralView, viewPsum)
    # gmsh.view.option.setNumber(viewPsum, "CustomMax", np.max(Ptotal) * 1.2)
    # gmsh.view.option.setNumber(viewPsum, "AutoPosition", 5)  # 5: bottom right

    # pFilePath = os.path.join(resDir, "p_total.dat")
    # writeSimple(pFilePath, time, Ptotal[3:])

    # Launch the GUI to see the results:
    if "-nopopup" not in sys.argv:
        gmsh.fltk.run()
    gmsh.finalize()
