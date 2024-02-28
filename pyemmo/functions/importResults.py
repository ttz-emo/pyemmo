"""Module to import simulation results from GetDP (Onelab)"""

import os
from os import path
from cmath import isclose
from typing import List, Tuple, Union
import warnings
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import numpy.typing as npt
from parse import parse
import gmsh
from .. import rootLogger as logger


def readTimeTableDat(filePath: str) -> Tuple[np.ndarray, np.ndarray]:
    """returns the Data from the the .*dat file witten in the TimeTable Format and returns
    the time and the corresponding data.

    Args:
        filePath (str): path to a file with .dat extension containing data in GetDP TimeTable format

    Returns:
        Tuple[np.ndarray, np.ndarray]: time and data vectors -> (time, data)

    """

    with open(filePath, "r", encoding="utf-8") as datFile:
        lines = []
        # remove comment lines
        for line in datFile.readlines():
            if line[0] != "#":
                lines.append(line)
    nbrLines = len(lines)
    if nbrLines == 1:
        # only one line -> probably RegionValue format (Virtual Work)
        valueList: List[str] = lines[0].strip().split(" ")
        # always use two values as pair
        nbrValues = len(valueList)
        # number of pairs must be int and dividable by 2
        assert nbrValues % 2 == 0
        nbrPairs = int(nbrValues / 2)
        time = np.zeros((nbrPairs,))
        values = np.zeros((nbrPairs,))
        for i in range(nbrPairs):
            time[i] = valueList[2 * i]
            values[i] = valueList[2 * i + 1]
    elif nbrLines > 1:
        time = np.zeros((nbrLines,))
        values = np.zeros((nbrLines,))
        for i, line in enumerate(lines):
            lineArr = line.strip().split(sep=" ")
            assert len(lineArr) == 2  # there must be two values in a line
            time[i] = float(lineArr[0])
            values[i] = float(lineArr[1])
    else:
        raise ValueError(f"Data imported from '{filePath}' was invalid!")
    return (time, values)


def splitData(
    time: List[float], data: List[float]
) -> Tuple[int, List[List[float]], List[List[float]]]:
    """Split up the time-data value pairs if there are multiple time vectors
    (e.g. time=[0,1,2,3,0,1,2] -> time[0]=[0,1,2,3], time[1]=[0,1,2]).
    Time-vectors must be increasing.


    Args:
        time (List[float]): 1D-Array with time values.
        data (List[float]): 1D-Array with data values.

    Returns:
        int: Number of simulations in the data set. (Number of splits).
        List[List[float]]: 2D time array.
        List[List[float]]: 2D data array.
    """
    # assert that the input vectors have the same size
    assert len(time) == len(data)
    nbrSims = 0  # number of simulations
    # init lists and arrays:
    timeVec = []
    timeArray = []
    dataVec = []
    dataArray = []
    startTime = time[0]  # init first element
    for i, actTime in enumerate(time):
        if actTime < startTime:  # if the next time value is smaller
            nbrSims += 1  # its a new simulation
            # append last nbrSims values to array
            timeArray.append(timeVec.copy())
            dataArray.append(dataVec.copy())
            # clear vectors so they can be refilled
            timeVec.clear()
            dataVec.clear()
        timeVec.append(actTime)
        dataVec.append(data[i])
        startTime = actTime
    # append last simulation to array
    timeArray.append(timeVec)
    dataArray.append(dataVec)
    return (nbrSims + 1, timeArray, dataArray)


def plotTimeTableDat(
    filePath: str,
    dataLabel: str = "",
    title: str = "",
    savefig: bool = False,
    showfig: bool = True,
    savePath: str = None,
) -> List[Figure]:
    """Plot the data in the filePath .dat-file and save the figure optionally.

    There can be several simulations in one .dat file. If so there will be one
    figure for each simulation.

    Args:
        filePath (str): path to the .dat-file in timetable-format
        dataLabel (str, optional): label of the ploted data on the y-axis.
            Defaults to ""
        title (str, optional): title of the figure. Defaults to ""
        savefig (bool, optional): flag to determine if the figure should be
            saved. Defaults to False.
        showfig (bool, optional): flag to determine if the figure should be
            displayed. Defaults to True.
        savePath (str, optional): path with filename and valid extension to
            save the figure. Defaults to None. E.g.
            "C:\\Users\\Test\\Pictures\\Test.png". If savePath is None figure
            will be saved with filePath and .png extension

    Returns:
        List[Figure]: Returns a list of matplotlib Figure objects

    """
    time, data = readTimeTableDat(filePath)
    nbrSim, timeArray, dataArray = splitData(time, data)
    # PLOT
    figureList: List[Figure] = []
    plt.ioff()
    for sim in range(nbrSim):
        # FIXME: with plt.ioff() only works on Python 3.11
        # with plt.ioff() if not showfig else plt.ion():
        fig, axes = plt.subplots()
        fig.set_dpi(200)
        axes.plot(timeArray[sim], dataArray[sim], marker=".")
        # show()
        # ax.set_aspect("equal", adjustable="box")
        # check that max or min is not close too close to zero to apply the y_lim
        maxVal = max(dataArray[sim])
        minVal = min(dataArray[sim])
        if not (
            isclose(maxVal, 0, abs_tol=0.1) or isclose(minVal, 0, abs_tol=0.1)
        ):
            fig.axes[0].set_ylim(
                bottom=minVal * (1.1 if min(dataArray[sim]) < 0 else 0.9),
                top=maxVal * (1.1 if max(dataArray[sim]) > 0 else 0.9),
            )
        axes.set(ylabel=dataLabel, xlabel="time in s", title=title + f"_{sim}")
        if savefig:
            if not savePath:
                savePath = path.abspath(path.splitext(filePath)[0])
            fig.savefig(savePath + f"_{sim}" + ".png")
        figureList.append(fig)
        # if showfig:
        #     fig.show()
        # else:
        #     fig.close()

    return figureList


def plotAllDat(dirPath: str) -> None:
    """Plot all .dat files as png in the folder dirPath

    Args:
        dirPath (str): path to the folder containing the .dat files
    """
    if path.isdir(dirPath):
        # if the folder for results exists
        for file in os.listdir(dirPath):
            filePath = os.path.join(dirPath, file)
            filename, fileExt = path.splitext(file)
            if fileExt == ".dat" and os.stat(filePath).st_size != 0:
                plotTimeTableDat(
                    path.abspath(filePath),
                    filename,
                    title=filename,
                    savefig=True,
                )


def importSP(
    posFilePath: str,
) -> Tuple[
    str, List[float], List[Tuple[float, float, float]], List[List[float]]
]:
    """Import values of POS files with the "Scalar Point" (SP) format

    Args:
        SPFilePath (str): path to pos file in SP format

    Returns:
        Tuple:
            - str: PostOperation quantity name
            - List[float]: List of time values
            - List[Tuple[float, float, float]]: List of tuple of position coordinates (x,y,z)
            - List[List[float]]]: List of List of quantity values for each point, and each timestep

    """
    _, filename = path.split(posFilePath)
    filename, ext = filename.split(".")
    if ext != "pos":
        raise ValueError(f"Given filepath '{posFilePath}' is not a POS-file!")
    with open(posFilePath, "r", encoding="utf-8") as dataFile:
        dataLines = dataFile.readlines()
    parsedName = parse('View "{}" {\n', dataLines.pop(0))
    if not parsedName:
        raise (
            RuntimeError(
                f"""Given file '{posFilePath}' did not contain correct first line: 'View "POS NAME" {{'. POS name could not be identified"""
            )
        )
    dataLines.pop(-1)  # remove last line (no information)
    # read time values
    time: List[float] = []
    timeStr = parse("TIME{{{}}};\n", dataLines[-1])
    if timeStr:  # if time values could be parsed
        dataLines.pop()  # remove time line from dataLines
        for timeVal in timeStr[0].split(","):
            time.append(float(timeVal))

    # read node values
    pos: List[Tuple[float, float, float]] = []  # position
    values: List[List[float]] = []  # result values
    for line in dataLines:
        parsedValues = parse("SP({:g},{:g},{:g}){{{}}};\n", line)
        if parsedValues:
            # first 3 elements are the coordinate values
            pos.append(parsedValues[0:3])
            valueList = []  # empty list for values of one point
            for value in parsedValues[3].split(","):
                valueList.append(float(value))
            values.append(valueList.copy())  # add copy of that list
            # valueList.clear()
        else:
            # if the parse function did not return values, the format was wrong
            raise (
                RuntimeError(
                    f"Given file '{posFilePath}' did not contain SP formatted values!"
                )
            )
    return parsedName[0], time, pos, values


def importPos(
    posFile: Union[str, os.PathLike]
) -> Tuple[npt.NDArray[np.uint64], List[float], npt.NDArray]:
    """Import POS file via gmsh api.

    TODO: Does not work for SP-formatted pos files. -> Use function getListData()
    Args:
        posFile (Union[str, os.PathLike]): _description_

    Returns:
        Tuple[np.ndarray, List[float], np.ndarray]:
            - gmsh mesh element tags
            - time
            - data array
    """
    # check file extension
    _, filename = path.split(posFile)
    filename, ext = filename.split(".")
    if ext != "pos":
        raise ValueError(f"Given filepath '{posFile}' is not a POS-file!")

    finGmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize()  # init gmsh
        finGmsh = True  # if gmsh wasn't init before -> close it a the end
    gmsh.open(posFile)  # load view

    # check that view was loaded:
    viewTags = gmsh.view.getTags()
    if viewTags.size == 0:
        gmsh.finalize()
        raise ValueError(
            f"Given file '{posFile}' did not result in a Gmsh view. Is file in gmsh POS-format?"
        )
    # get number of time steps in SIMULATION (not all time steps have to be saved)
    nbrSteps = int(
        gmsh.view.option.getNumber(tag=viewTags[-1], name="NbTimeStep")
    )
    time = []  # init time vector
    # init data containers with first time step
    _, elementTags, cdata, ctime, numComp = gmsh.view.getModelData(
        tag=viewTags[-1], step=0
    )
    elementTags: npt.NDArray[np.uint64] = elementTags
    # data format of 'cdata':
    #   vector: number of components = 3
    #   scalar: number of components = 1
    if not cdata:
        # sometimes only the last timestep is saved to the pos file
        _, elementTags, cdata, ctime, numComp = gmsh.view.getModelData(
            viewTags[-1], nbrSteps - 1
        )
        if not cdata:
            gmsh.finalize()
            raise ValueError(f"No data found in {posFile}!")
        warnings.warn(
            f"Import file '{posFile}' did only contain last timestep!"
        )
        # Only last time step happens if PostProcessing is called at runtime (in 'Resolution').
        # Return only that timestep
        if finGmsh:
            gmsh.finalize()
        return (
            elementTags,
            [ctime],
            np.array(cdata)[:, :numComp],
        )
    # else: there was data for the first timestep
    data = np.zeros((nbrSteps, len(cdata), numComp))  # init data array
    data[0] = np.array(cdata)[:, :numComp]  # set init value of first time step
    time.append(ctime)  # add first time step
    # loop through time steps an extract data
    for step in range(1, nbrSteps):
        _, _, cdata, ctime, _ = gmsh.view.getModelData(viewTags[-1], step)
        data[step] = np.array(cdata)[:, :numComp]
        time.append(ctime)
    if finGmsh:
        # if gmsh wasn't init before:
        gmsh.finalize()
    return (elementTags, time, data)


def getResFileList(
    resDir: os.PathLike,
) -> tuple[list[os.PathLike], list[os.PathLike]]:
    """Return a list of GetDP result files from the folder ``resDir``.
    GetDP results can be .pos or .dat files.

    Args:
        resDir (os.PathLike): Path to GetDP results.

    Returns:
        list[os.PathLike]: List of importable result file paths.
    """
    assert isinstance(resDir, str)
    if os.path.isdir(resDir):
        datFileList = []
        posFileList = []
        for resFile in os.listdir(resDir):
            _, ext = os.path.splitext(resFile)
            if ext == ".dat":
                # file is valid results file
                datFileList.append(resFile)
            if ext == ".pos":
                posFileList.append(resFile)
        if len(datFileList) == 0:
            logger.warning("No result files found in '%s'", resDir)
        return datFileList, resFile
    raise FileNotFoundError(f"Results folder {resDir} does not exist.")
