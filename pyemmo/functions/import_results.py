#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied
# Sciences Wuerzburg-Schweinfurt.
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
"""Module to import simulation results from GetDP (Onelab)"""

import os
import warnings
from cmath import isclose
from os import PathLike, path
from typing import List, Tuple, Union

import gmsh
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from parse import parse

from .. import rootLogger as logger


def read_timetable_dat(
    file_path: PathLike,
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
        raise FileNotFoundError(f"Given results file '{file_path}' did not exist!")
    # Try to import the data via numpy. Should work for most cases!
    # standard 'delemiter' is whitespace.
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    if len(data_array.shape) == 1:
        # static simulation
        if not data_array.size > 1:
            # there must be at least one time + value
            raise ValueError(
                f"Less than one value was imported from {file_path}. " "There must be at least one time-value pair!"
            )
        time = np.reshape(data_array[0], (1))
        values = data_array[1:]
    else:
        # multi static or transient simulation(s)
        time = data_array[:, 0]
        values = data_array[:, 1:]

    return (time, values)


# pylint: disable=locally-disabled, invalid-name
def read_RegionValue_dat(
    file_path: PathLike,
) -> Tuple[np.ndarray, np.ndarray]:
    """Import data from 'RegionValue' formatted .dat-file (GetDP resutl file).
    This usually only applies to torque results computed with the virtual works
    method.
    RegionValue format looks like:
        'time0 val0 time1 val1 ...'

    Args:
        file_path (PathLike): Path to results file.

    Returns:
        Tuple[np.ndarray, np.ndarray]: time and data vector with shape:
        (nbr_timesteps,)
    """
    # make sure dat file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Given results file '{file_path}' did not exist!")
    # import the data via numpy. Should work for most cases!
    # standard 'delemiter' is whitespace.
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    # make sure there is only one line of data in the results file
    if not len(data_array.shape) == 1:
        raise ValueError("Multiple lines in 'RegionValue' format! " "There should only be one line containing all time steps!")
    if not data_array.shape[0] > 0:
        raise ValueError(f"No data in {file_path} results file!")
    if not data_array.shape[0] % 2 == 0:
        raise ValueError(f"Odd number of values in RegionValue formatted file {file_path}!")
    time = data_array[0::2]  # numpy slicing [start:stop:step]
    data = data_array[1::2]
    return time, data


def split_data(time: np.ndarray, data: np.ndarray) -> Tuple[int, List[np.ndarray], List[np.ndarray]]:
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
    if not len(time.shape) == 1:
        raise ValueError("Given time array is not a vector!")
    # make sure that data shape has number of timesteps
    if time.shape[0] not in data.shape:
        raise ValueError("Time and data array have different length!")
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


def plot_timetable_dat(
    file_path: str,
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
            Defaults to "".
        title (str, optional): title of the figure. Defaults to ""
        savefig (bool, optional): flag to determine if the figure should be
            saved. Defaults to False.
        showfig (bool, optional): flag to determine if the figure should be
            displayed. Defaults to True.
        savePath (str, optional): path with filename and valid extension to
            save the figure. Defaults to None. E.g. "C:\\Users\\Test\\Pictures
            \\Test.png". If savePath is None figure will be saved with filePath
            and .png extension

    Returns:
        List[Figure]: Returns a list of matplotlib Figure objects.

    """
    time, data = read_timetable_dat(file_path)
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
        # check that max or min is not too close to zero to apply the y_lim
        maxVal = max(dataArray[sim])
        minVal = min(dataArray[sim])
        if not (isclose(maxVal, 0, abs_tol=0.1) or isclose(minVal, 0, abs_tol=0.1)):
            fig.axes[0].set_ylim(
                bottom=minVal * (1.1 if min(dataArray[sim]) < 0 else 0.9),
                top=maxVal * (1.1 if max(dataArray[sim]) > 0 else 0.9),
            )
        axes.set(ylabel=dataLabel, xlabel="time in s", title=title + f"_{sim}")
        if savefig:
            if not savePath:
                savePath = path.abspath(path.splitext(file_path)[0])
            fig.savefig(savePath + f"_{sim}" + ".png")
        figureList.append(fig)
        # if showfig:
        #     fig.show()
        # else:
        #     fig.close()

    return figureList


def plot_all_dat(dir_path: PathLike) -> None:
    """Plot all .dat files as png in the folder dirPath

    Args:
        dirPath (PathLike): Path to the folder containing the .dat files.
    """
    if path.isdir(dir_path):
        # if the folder for results exists
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            filename, extention = path.splitext(file)
            if extention == ".dat" and os.stat(file_path).st_size != 0:
                plot_timetable_dat(
                    path.abspath(file_path),
                    filename,
                    title=filename,
                    savefig=True,
                )
    else:
        raise RuntimeError(f"Given result foler '{dir_path}'did not exist!")


def importSP(
    posFilePath: str,
) -> Tuple[str, List[float], List[Tuple[float, float, float]], List[List[float]]]:
    """Import values of POS files with the "Scalar Point" (SP) format

    Args:
        SPFilePath (str): path to pos file in SP format

    Returns:
        Tuple:
            - str: PostOperation quantity name
            - List[float]: List of time values
            - List[Tuple[float, float, float]]: List of tuple of position
                coordinates (x,y,z)
            - List[List[float]]]: List of List of quantity values for each
                point, and each timestep

    """
    _, filename = path.split(posFilePath)
    filename, ext = filename.split(".")
    if ext != "pos":
        raise ValueError(f"Given filepath '{posFilePath}' is not a POS-file!")
    with open(posFilePath, encoding="utf-8") as dataFile:
        dataLines = dataFile.readlines()
    parsedName = parse('View "{}" {\n', dataLines.pop(0))
    if not parsedName:
        raise (
            RuntimeError(
                f"Given file '{posFilePath}' did not contain correct first "
                """line: 'View "POS NAME" {{'. """
                "POS name could not be identified"
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
            raise (RuntimeError(f"Given file '{posFilePath}' did not contain " "SP formatted values!"))
    return parsedName[0], time, pos, values


def importPos(pos_file: Union[str, PathLike]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Import POS file via gmsh api.

    TODO: Does not work for SP-formatted pos files.
        -> Use function getListData()

    Args:
        pos_file (Union[str, PathLike]): _description_

    Returns:
        Tuple[np.ndarray, List[float], np.ndarray]:
            - gmsh mesh element tags
            - time
            - data array
    """
    # check file extension
    _, filename = path.split(pos_file)
    filename, ext = filename.split(".")
    if ext != "pos":
        raise ValueError(f"Given filepath '{pos_file}' is not a POS-file!")

    finalize_gmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize()  # init gmsh
        # if gmsh wasn't init before -> close it a the end
        finalize_gmsh = True
    gmsh.open(pos_file)  # load view

    # check that view was loaded:
    view_tags = gmsh.view.getTags()
    if view_tags.size == 0:
        gmsh.finalize()
        raise ValueError(f"Given file '{pos_file}' did not result in a Gmsh view. Is file " "in gmsh POS-format?")
    # get number of time steps in SIMULATION (not all time steps have to be
    # saved)
    nbr_steps = int(gmsh.view.option.getNumber(tag=view_tags[-1], name="NbTimeStep"))
    time = []  # init time vector
    # init data containers with first time step
    _, element_tags, cdata, ctime, nbr_components = gmsh.view.getModelData(tag=view_tags[-1], step=0)
    # data format of 'cdata':
    #   vector: number of components = 3
    #   scalar: number of components = 1
    if not cdata:
        _, element_tags, cdata, ctime, nbr_components = gmsh.view.getModelData(view_tags[-1], nbr_steps - 1)
        if not cdata:
            gmsh.finalize()
            raise ValueError(f"No data found in {pos_file}!")
        warnings.warn(f"Import file '{pos_file}' did only contain last timestep!")
        # Only last time step happens if PostProcessing is called at runtime
        # (in 'Resolution').
        # Return only that timestep
        if finalize_gmsh:
            gmsh.finalize()
        return (
            element_tags,
            np.array(ctime),
            np.array(cdata)[:, :nbr_components],
        )
    # else: there was data for the first timestep...
    data = np.zeros((nbr_steps, len(cdata), nbr_components))  # init data array
    # set init value of first time step:
    data[0] = np.array(cdata)[:, :nbr_components]
    time.append(ctime)  # add first time step
    # loop through time steps an extract data
    for step in range(1, nbr_steps):
        _, _, cdata, ctime, _ = gmsh.view.getModelData(view_tags[-1], step)
        data[step] = np.array(cdata)[:, :nbr_components]
        time.append(ctime)
    if finalize_gmsh:
        # if gmsh wasn't init before:
        gmsh.finalize()
    return element_tags, np.array(time), data


def get_result_files(
    result_folder: PathLike,
) -> Tuple[list[PathLike], list[PathLike]]:
    """Return a list of GetDP result files from the folder ``resDir``.
    GetDP results can be .pos or .dat files.

    Args:
        result_folder (PathLike): Path to GetDP results.

    Returns:
        Tuple[list[PathLike], list[PathLike]]: List of .pos and list of .dat
            files in the given folder.
    """
    if os.path.isdir(result_folder):
        dat_file_list = []
        pos_file_list = []
        for results_file in os.listdir(result_folder):
            _, ext = os.path.splitext(results_file)
            if ext == ".dat":
                dat_file_list.append(results_file)
            elif ext == ".pos":
                pos_file_list.append(results_file)
        if len(dat_file_list) == 0:
            logger.warning("No result files found in '%s'", result_folder)
        return dat_file_list, pos_file_list
    raise FileNotFoundError(f"Results folder {result_folder} does not exist.")
