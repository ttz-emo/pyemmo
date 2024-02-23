"""Module to import simulation results from GetDP (Onelab)"""

import os
from os import path
from cmath import isclose
from typing import List, Tuple, Union
import warnings
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from parse import parse
import gmsh
from .. import rootLogger as logger


def read_timetable_dat(
    file_path: os.PathLike,
) -> Tuple[np.ndarray, np.ndarray]:
    """returns the Data from the the .*dat file witten in the TimeTable Format
    and returns the time and the corresponding data.

    TimeTable format is a whitespace separated list of time-value pairs and
    looks like:

        time0 val0_0 (val0_1 ...)\n
        time1 val1_0 (val1_1 ...)\n
        ...\n

    For most result types (torque, induced voltage, flux (all integral typ
    results)) there is only one value per time step. But for special results,
    like rotor bar current, there can be multiple values per time step (like
    rotor current per bar).

    Args:
        file_path (str): path to a file with .dat extension containing data in
        GetDP TimeTable format

    Returns:
        Tuple[np.ndarray, np.ndarray]: time and data array -> (time, data)

    """
    # make sure dat file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Given results file '{file_path}' did not exist!"
        )
    # Try to import the data via numpy. Should work for most cases!
    # standard 'delemiter' is whitespace.
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    time = data_array[:, 0]
    values = data_array[:, 1:]
    return (time, values)

# pylint: disable=locally-disabled, invalid-name
def read_RegionValue_dat(
    file_path: os.PathLike,
) -> Tuple[np.ndarray, np.ndarray]:
    """Import data from 'RegionValue' formatted .dat-file (GetDP resutl file).
    This usually only applies to torque results computed with the virtual works
    method.
    RegionValue format looks like:
        'time0 val0 time1 val1 ...'

    Args:
        file_path (os.PathLike): Path to results file.

    Returns:
        Tuple[np.ndarray, np.ndarray]: time and data vector with shape:
        (nbr_timesteps,)
    """
    # make sure dat file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Given results file '{file_path}' did not exist!"
        )
    # import the data via numpy. Should work for most cases!
    # standard 'delemiter' is whitespace.
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    # make sure there is only one line of data in the results file
    assert len(data_array.shape) == 1, "Multiple lines in 'RegionValue' format"
    assert data_array.shape[0] > 0, f"No data in {file_path} results file!"
    assert data_array.shape[0] % 2 == 0, "Odd number of values!"
    time = data_array[0::2]  # numpy slicing [start:stop:step]
    data = data_array[1::2]
    return time, data


def split_data(
    time: np.ndarray, data: np.ndarray
) -> Tuple[int, List[np.ndarray], List[np.ndarray]]:
    """Split up the time-data value pairs if there are multiple time vectors
    (e.g. time=[0,1,2,3,0,1,2] -> time[0]=[0,1,2,3], time[1]=[0,1,2]).
    Time-vectors must be increasing.

    Args:
        time (np.ndarray): 1D-Array with time values.
        data (np.ndarray): 1D- ord 2D-Array with data values.

    Returns:
        int: Number of simulations in the data set. (Number of splits).
        list(np.ndarray): 2D time array.
        list(np.ndarray): 2D data array.
    """
    # make sure time and data are type ndarray
    if not isinstance(time, np.ndarray) or not isinstance(data, np.ndarray):
        raise TypeError("Time and data array must be numpy ndarray!")
    assert len(time.shape) == 1, "Given time array is not a vector!"
    # assert that data shape has number of timesteps
    assert time.shape[0] in data.shape, "Time and data array have diverent len"
    time_axis = data.shape.index(time.shape[0])  # get time axis
    # get the indices where time values are equal (e.g. time = [0, 0]) or the
    # difference of the time vector is negative (e.g. time = [0,1,2,0], so
    # diff(time) = [1,1,-2] -> split at third index)
    # +1 because diff gives (nbr_time - 1) values!
    split_indices = np.where(np.diff(time) <= 0)[0] + 1
    time_vec_list = np.split(time, split_indices)  # split time
    data_list = np.split(data, split_indices, axis=time_axis)  # split data
    nbrSims = len(time_vec_list)  # number of simulations
    return nbrSims, time_vec_list, data_list


def plotTimeTableDat(
    filePath: str,
    dataLabel: str = "",
    title: str = "",
    savefig: bool = False,
    showfig: bool = True,
    savePath: str = None,
) -> List[Figure]:
    """Plot the data in the filePath .dat-file and save the figure optionally.

    There can be several simulations in one .dat file. If so there will be one figure for each simulation.

    Args:
        filePath (str): path to the .dat-file in timetable-format
        dataLabel (str, optional): label of the ploted data on the y-axis. Defaults to ""
        title (str, optional): title of the figure. Defaults to ""
        savefig (bool, optional): flag to determine if the figure should be saved. Defaults to False.
        showfig (bool, optional): flag to determine if the figure should be displayed. Defaults to True.
        savePath (str, optional): path with filename and valid extension to save the figure.
            Defaults to None. E.g. "C:\\Users\\Test\\Pictures\\Test.png". If savePath is None
            figure will be saved with filePath and .png extension

    Returns:
        List[Figure]: Returns a list of matplotlib Figure objects

    """
    time, data = read_timetable_dat(filePath)
    nbrSim, timeArray, dataArray = split_data(time, data)
    # PLOT
    figureList: List[Figure] = list()
    # plt.ioff()
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
) -> Tuple[np.ndarray, List[float], np.ndarray]:
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
    # data format of 'cdata':
    #   vector: number of components = 3
    #   scalar: number of components = 1
    if not cdata:
        _, _, cdata, ctime, numComp = gmsh.view.getModelData(
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
        return (ctime, np.array(cdata)[:, :numComp])
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
