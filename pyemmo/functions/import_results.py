#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied
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

from __future__ import annotations

import json
import logging
import os
from cmath import isclose
from os import path

import gmsh
import numpy as np
import parse
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def read_timetable_dat(file_path: str | os.PathLike) -> tuple[np.ndarray, np.ndarray]:
    """
    returns the Data from the the .*dat file witten in the TimeTable Format
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
            return (np.array([]), np.array([]))
        time = np.reshape(data_array[0], (1))
        values = data_array[1:]
    else:
        # multi static or transient simulation(s)
        time = data_array[:, 0]
        values = data_array[:, 1:]

    return (time, values)


# pylint: disable=locally-disabled, invalid-name
def read_RegionValue_dat(file_path: str | os.PathLike) -> tuple[np.ndarray, np.ndarray]:
    """
    Import data from 'RegionValue' formatted .dat-file (GetDP resutl file).
    This usually only applies to torque results computed with the virtual works
    method.
    RegionValue format looks like:

        'time0 val0 time1 val1 ...'

    Args:
        file_path (Union[str, os.PathLike]): Path to results file.

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
        raise ValueError(
            "Multiple lines in 'RegionValue' format! "
            "There should only be one line containing all time steps!"
        )
    if not data_array.shape[0] > 0:
        raise ValueError(f"No data in {file_path} results file!")
    if not data_array.shape[0] % 2 == 0:
        raise ValueError(
            f"Odd number of values in RegionValue formatted file {file_path}!"
        )
    time = data_array[0::2]  # numpy slicing [start:stop:step]
    data = data_array[1::2]
    return time, data


def split_data(
    time: np.ndarray, data: np.ndarray
) -> tuple[int, list[np.ndarray], list[np.ndarray]]:
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
    savePath: str = "",
) -> list[Figure]:
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
    figureList: list[Figure] = list()
    # plt.ioff()
    for sim in range(nbrSim):
        # FIXME: with plt.ioff() only works on Python 3.11
        # with plt.ioff() if not showfig else plt.ion():
        sim_data = dataArray[sim]
        fig, axes = plt.subplots()
        fig.set_dpi(200)
        axes.plot(timeArray[sim], sim_data)  # , marker=".")
        # show()
        # ax.set_aspect("equal", adjustable="box")
        # check that max or min is not too close to zero to apply the y_lim
        if 1 in sim_data.shape:
            maxVal = np.nanmax(sim_data)
            minVal = np.nanmin(sim_data)
        else:
            # multi data array
            # FIXME: Make sure second axis is really data axis
            maxVal = np.nanmax(sim_data[:, 0])
            minVal = np.nanmin(sim_data[:, 0])
        if not (isclose(maxVal, 0, abs_tol=0.1) or isclose(minVal, 0, abs_tol=0.1)):
            fig.axes[0].set_ylim(
                bottom=minVal * (1.1 if minVal < 0 else 0.9),
                top=maxVal * (1.1 if maxVal > 0 else 0.9),
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


def plot_all_dat(dir_path: str | os.PathLike) -> None:
    """Plot all .dat files as png in the folder dirPath

    Args:
        dirPath (Union[str, os.PathLike]): Path to the folder containing the .dat files.
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
) -> tuple[str, list[float], list[tuple[float, float, float]], list[list[float]]]:
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
    parsedName = parse.parse('View "{}" {\n', dataLines.pop(0))
    if not isinstance(parsedName, parse.Result):
        raise (
            RuntimeError(
                f"Given file '{posFilePath}' did not contain correct first "
                """line: 'View "POS NAME" {{'. """
                "POS name could not be identified"
            )
        )
    dataLines.pop(-1)  # remove last line (no information)
    # read time values
    timeStr = parse.parse("TIME{{{}}};\n", dataLines[-1])
    if isinstance(timeStr, parse.Result):  # if time values could be parsed
        time: list[float] = []
        dataLines.pop()  # remove time line from dataLines
        for timeVal in timeStr[0].split(","):
            time.append(float(timeVal))
    elif timeStr is None:
        # no time step given in results file. Only single time step evaluated!
        time = []
    else:
        raise TypeError(
            "Parsing of TIME line in SP formatted file did not return parse.Result object."
        )

    # read node values
    pos: list[tuple[float, float, float]] = []  # position
    values: list[list[float]] = []  # result values
    for line in dataLines:
        parsedValues = parse.parse("SP({:g},{:g},{:g}){{{}}};\n", line)
        if isinstance(parsedValues, parse.Result):
            # first 3 elements are the coordinate values
            pos.append(parsedValues[0:3])
            valueList = []  # empty list for values of one point
            for value in parsedValues[3].split(","):
                valueList.append(float(value))
            values.append(valueList.copy())  # add copy of that list
            # valueList.clear()
        else:
            # if the parse function did not return values, the format was wrong
            raise RuntimeError(
                f"Given file '{posFilePath}' did not contain SP formatted values!"
            )
    return parsedName[0], time, pos, values


def load_view(pos_file: str) -> tuple[bool, int]:
    """Load view from post processing file (ending .pos)

    Args:
        pos_file (str): .pos file path

    Returns:
        bool: flag to indicate if gmsh had to be initialized.
        int: Gmsh view tag.
    """
    finalize_gmsh = False
    if not gmsh.isInitialized():
        gmsh.initialize()  # init gmsh
        # if gmsh wasn't init before -> close it a the end
        finalize_gmsh = True

    nbr_views_loaded = gmsh.view.getTags().size

    gmsh.open(pos_file)  # load view

    # check that view was loaded:
    view_tags = gmsh.view.getTags()

    # check if new view has been created, otherwise raise error
    if isinstance(view_tags, np.ndarray) and view_tags.size == nbr_views_loaded:
        if finalize_gmsh:
            gmsh.finalize()
        raise ValueError(
            f"Given file '{pos_file}' did not result in a Gmsh view. Is file "
            "in gmsh POS-format?"
        )
    return finalize_gmsh, view_tags[-1]


def importPos(pos_file: str | os.PathLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Import POS file via gmsh api.

    .. todo::

        Does not work for SP-formatted pos files.
            -> Use function getListData()

    Args:
        pos_file (Union[str, Union[str, os.PathLike]]): _description_

    Returns:
        Tuple[np.ndarray, List[float], np.ndarray]:
            - gmsh mesh element tags
            - time
            - data array
    """
    # check file extension
    path, filename = os.path.split(pos_file)
    filename, ext = os.path.splitext(filename)
    if ext != ".pos":
        raise ValueError(f"Given filepath '{pos_file}' is not a POS-file!")

    # Check if pos file is in old GmshParsed format. See function import_pos_parsedFormat!
    with open(pos_file, "r") as file:
        if file.readline().startswith("View"):
            logger.warning(
                "Result file '%s' is in old gmsh parsed format. "
                "Try to convert it to new format...",
                pos_file,
            )
            logger.info(
                "Alternativly use function import_pos_parsedFormat(...) to import "
                "parsed formatted data!"
            )
            # if function is in GmshParsed format, export as .msh file to update file
            # format and the use as new results file
            filename = filename + ".msh"  # update filename
            _, view_tag = load_view(pos_file)
            pos_file = os.path.join(path, filename)  # update result file path
            gmsh.view.write(view_tag, pos_file)  # export as .msh

    # load view from result file
    finalize_gmsh, view_tag = load_view(pos_file)

    # get number of time steps in SIMULATION (not all time steps have to be
    # saved)
    nbr_steps = int(gmsh.view.option.getNumber(tag=view_tag, name="NbTimeStep"))
    time = []  # init time vector
    # init data containers with first time step
    _, element_tags, cdata, ctime, nbr_components = gmsh.view.getModelData(
        tag=view_tag, step=0
    )
    # check type of element tags and convert to numpy
    if not isinstance(element_tags, np.ndarray):
        element_tags = np.array(element_tags)
    # data format of 'cdata':
    #   vector: number of components = 3
    #   scalar: number of components = 1
    if not cdata:
        _, element_tags, cdata, ctime, nbr_components = gmsh.view.getModelData(
            view_tag, nbr_steps - 1
        )
        if not cdata:
            gmsh.finalize()
            raise ValueError(f"No data found in {pos_file}!")
        logging.warning("Import file '%s' did only contain last timestep!", pos_file)
        # Only last time step happens if PostProcessing is called at runtime
        # (in 'Resolution').
        # Return only that timestep
        if finalize_gmsh:
            gmsh.finalize()
        # check type of element tags and convert to numpy
        if not isinstance(element_tags, np.ndarray):
            element_tags = np.array(element_tags)
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
        _, _, cdata, ctime, _ = gmsh.view.getModelData(view_tag, step)
        data[step] = np.array(cdata)[:, :nbr_components]
        time.append(ctime)
    if finalize_gmsh:
        # if gmsh wasn't init before:
        gmsh.finalize()
    return element_tags, np.array(time), data


# TODO: move implementation of importPos to this function:
# def _import_pos_mshFormat(view_tag: int, step: int): ...


def import_pos_parsedFormat(file_path: str) -> tuple[str, np.ndarray, np.ndarray]:
    """Import data from older .pos format 'GmshParsed'.
    See this for more info about parsed file format:
    https://gmsh.info/doc/texinfo/gmsh.html#Gmsh-file-formats:~:text=More%20explicitly%2C%20the%20syntax%20for%20a%20parsed%20View%20is%20the%20following

    Args:
        file_path (str): path to result file

    Returns:
        tuple[str,np.ndarray,np.ndarray]:
            - GmshParsed results data type (like SP for scalar point or VL for vector line)
            - Node coordinates in shape (number of elements, number of nodes * 3)
            - Data array in shape (number of element, number of simulation steps * number of values per node)
    """
    finalize_gmsh, view_tag = load_view(file_path)

    # check that view was loaded:
    dTypeArray, numElem, data = gmsh.view.getListData(view_tag, returnAdaptive=False)
    for i, data_type in enumerate(dTypeArray):
        # translate data type to number of data values per step
        if data_type[0] == "S":  # scalar values
            nbr_data = 1
        elif data_type[0] == "V":  # vector result
            nbr_data = 3
        elif data_type[0] == "T":  # tensor result
            raise NotImplementedError("Tensor data import not implemented.")
        else:
            raise ValueError(f"Unknown data type '{data_type}' in result.")

        # match second character to get number of node coordinates per element
        match data_type[1]:
            case "P":  # point results
                nbr_coords = [3]  # number of coordinates per element
            case "L":  # line results
                # we get results with coords [x1,x2, y1,y2, z1,z2] but data with
                # [x1,y1,z1, x2,y2,z2]
                nbr_coords = [3, 3]  # number of coordinates per element
            case "T":  # triangle results
                nbr_coords = [3, 3, 3]  # 3 point per triangle
            case _:
                raise ValueError(
                    f"Cannot import values for Gmsh parsed data type {data_type}!"
                )
        # calc number of steps (unnecessary)
        nbr_steps = (data[i].size / numElem[i] - sum(nbr_coords)) / nbr_data
        assert nbr_steps % 1 == 0, "Number of timesteps turns out to be non-int!"

        # FIXME: Import time step information
        # assert nbr_steps == int(
        #     gmsh.view.option.getNumber(tag=view_tag, name="NbTimeStep")
        # )

        # if nbr_steps>1:
        #     with open(file_path, encoding="utf-8") as dataFile:
        #         dataLines = dataFile.readlines()
        #     dataLines.pop(-1)  # remove last line (no information)
        #     # read time values
        #     timeStr = parse.parse("TIME{{{}}};\n", dataLines[-1])
        #     if isinstance(timeStr, parse.Result):  # if time values could be parsed
        #         time: list[float] = []
        #         dataLines.pop()  # remove time line from dataLines
        #         for timeVal in timeStr[0].split(","):
        #             time.append(float(timeVal))
        #     elif timeStr is None:
        #         # no time step given in results file. Only single time step evaluated!
        #         time = []
        #     else:
        #         raise TypeError(
        #             "Parsing of TIME line in SP formatted file did not return parse.Result object."
        #         )

        # reshape data by (number of elements, number of data values)
        # where number of data values = num_data * nbr_steps
        reshaped_data = data[i].reshape((numElem[i], int(data[i].size / numElem)))

        # extract element node data
        # TODO: This could be reshaped by nbr_coords
        nodes = reshaped_data[:, 0 : sum(nbr_coords)]

        # extract data
        # TODO: This could be reshaped by nbr_coords
        out_data = reshaped_data[:, sum(nbr_coords) :]

        if finalize_gmsh:
            gmsh.finalize()

        return data_type, nodes, out_data

    # return dataType, numElem, data


def get_result_files(
    result_folder: str | os.PathLike,
) -> tuple[list[str | os.PathLike], list[str | os.PathLike]]:
    """Return a list of GetDP result files from the folder ``resDir``.
    GetDP results can be .pos or .dat files.

    Args:
        result_folder (Union[str, os.PathLike]): Path to GetDP results.

    Returns:
        Tuple[list[Union[str, os.PathLike]], list[Union[str, os.PathLike]]]: List of .dat
            and list of .pos files in the given folder.
    """
    if not os.path.isdir(result_folder):
        raise FileNotFoundError(f"Results folder {result_folder} does not exist.")
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


def load_param_file(setup_file: str | os.PathLike) -> dict:
    """load the parameter json file create in
    ``pyemmo.functions.runOnelab.runCalcForCurrent`` function"""
    if not os.path.isfile(setup_file):
        raise FileNotFoundError(f"Could not find setup.json file: {setup_file}")
    with open(setup_file, encoding="utf-8") as file:
        return json.load(file)


def main(
    sim_param: dict | str | os.PathLike,
) -> dict[str, np.ndarray | dict[str, np.ndarray]]:
    """Import results for standard GetDP simulation of a model created with PyEMMO.

    You can easily run simulations with the ``pyemmo.functions.runOnelab`` module!

    Args:
        sim_param (dict | str | os.PathLike): simulation parameter dict or path to saved
            parameter dict as json file.

    Raises:
        FileNotFoundError: If parameter file is path but given json file is not found.

    Returns:
        dict[str, np.ndarray |dict[str, np.ndarray]]: results for given simulation
    """
    if not isinstance(sim_param, dict):
        sim_param = load_param_file(sim_param)
    logging.info("Import results for result-ID '%s'", sim_param["getdp"]["ResId"])
    results_dict = {}  # init results
    # get results folder from parameters
    simulation_res_dir = os.path.join(
        sim_param["getdp"]["res"], sim_param["getdp"]["ResId"]
    )
    dat_files, _ = get_result_files(simulation_res_dir)

    # 1. Phase currents and voltages
    results_dict["current"] = {}
    results_dict["voltage"] = {}
    for index in "abc":
        # For case Current_Source OR Voltage_Source & Stator Circuit -> I_{a,b,c}
        res_file_name = f"I{index}.dat"
        if res_file_name in dat_files:
            results_dict["time"], results_dict["current"][index] = read_timetable_dat(
                os.path.join(simulation_res_dir, res_file_name)
            )
            dat_files.remove(res_file_name)
        # In case of Voltage_Source
        res_file_name = f"I{index}_w.dat"
        if res_file_name in dat_files:
            _, results_dict["current"][index + "w"] = read_timetable_dat(
                os.path.join(simulation_res_dir, res_file_name)
            )
            dat_files.remove(res_file_name)

        # For case Current_Source OR Voltage_Source & Stator Circuit -> I_{a,b,c}
        res_file_name = f"U{index}.dat"
        if res_file_name in dat_files:
            _, results_dict["voltage"][index] = read_timetable_dat(
                os.path.join(simulation_res_dir, res_file_name)
            )
            dat_files.remove(res_file_name)
        # In case of Voltage_Source
        res_file_name = f"U{index}_w.dat"
        if res_file_name in dat_files:
            _, results_dict["voltage"][index + "w"] = read_timetable_dat(
                os.path.join(simulation_res_dir, res_file_name)
            )
            dat_files.remove(res_file_name)

    if not results_dict["current"]:
        # Error because we need to import time here!
        raise FileNotFoundError(
            "Could not find any result file for stator phase current I_{a,b,c} or I_{a,b,c}w"
        )
    # We dont check for voltage imports because in case of current source there is no global voltage

    # optional import bar currents and voltages
    res_file = os.path.join(simulation_res_dir, "I_bars.dat")
    if os.path.isfile(res_file):
        results_dict["time"], results_dict["current"]["bars"] = read_timetable_dat(
            res_file
        )
    res_file = os.path.join(simulation_res_dir, "U_bars.dat")
    if os.path.isfile(res_file):
        results_dict["time"], results_dict["voltage"]["bars"] = read_timetable_dat(
            res_file
        )

    # 2. Torque Results
    results_dict["torque"] = {}
    results_dict["torque_vw"] = {}
    for side in ["rotor", "stator"]:
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque"][side] = read_timetable_dat(res_file)
        # Virtual Work results
        res_file = os.path.join(simulation_res_dir, f"T{side[0]}_vw.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["torque_vw"][side] = read_timetable_dat(res_file)
    if {"rotor", "stator"} <= results_dict["torque"].keys():
        results_dict["rotor torque"] = results_dict["torque"]["rotor"]
        results_dict["stator torque"] = results_dict["torque"]["stator"]
        # try to calc mean torque
        if np.isclose(
            np.mean(results_dict["rotor torque"]),
            np.mean(results_dict["stator torque"]),
            rtol=0.1,
        ):
            # mean diviation is smaller 10%
            # need to check this because if one of the results is misscalulated and just
            # returns 0 the mean result will give wrong results...
            # calc mean torque
            results_dict["torque"] = np.mean(
                [
                    results_dict["rotor torque"],
                    results_dict["stator torque"],
                ],
                axis=0,
            )
        else:
            logging.warning(
                (
                    "MST Torque for rotor and stator diviates more than 10%! "
                    "Check results carefully!"
                )
            )

    # 3. Flux results
    results_dict["flux"] = {}
    for index in "abcdq0":
        res_file = os.path.join(simulation_res_dir, f"Flux_{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["flux"][index] = read_timetable_dat(res_file)

    # 4. Induced voltage
    results_dict["inducedVoltage"] = {}
    for index in "ABC":
        res_file = os.path.join(simulation_res_dir, f"InducedVoltage{index}.dat")
        if os.path.isfile(res_file):
            # get first char in machine side to index rotor and stator results
            _, results_dict["inducedVoltage"][index.lower()] = read_timetable_dat(
                res_file
            )

    # 5. Rotor position
    res_file = os.path.join(simulation_res_dir, "RotorPos_deg.dat")
    if os.path.isfile(res_file):
        # get first char in machine side to index rotor and stator results
        _, results_dict["rotorPos"] = read_timetable_dat(res_file)

    # 6. Core loss
    # Check if file hystLoss_rotor.dat allready exists -> loss calculated
    core_loss_dict = {}
    if os.path.exists(os.path.join(simulation_res_dir, "hystLoss_rotor.dat")):
        logging.info(
            "Importing core loss values for %s...", sim_param["getdp"]["ResId"]
        )
        for side in ["rotor", "stator"]:
            core_loss_dict[side] = {}
            for loss_type in ("hyst", "eddy", "exc"):
                _, core_loss_dict[side][loss_type] = read_timetable_dat(
                    os.path.join(
                        simulation_res_dir,
                        str(loss_type) + f"Loss_{side}" + ".dat",
                    )
                )
    if core_loss_dict:
        results_dict["coreLoss"] = core_loss_dict
        # pylint: disable=locally-disabled, logging-not-lazy, logging-fstring-interpolation, line-too-long
        logging.debug("Iron loss for '" + sim_param["getdp"]["ResId"] + "'")
        logging.debug(f"{'Rotor':>24} {'Stator':>11} {'Gesamt':>11}")
        logging.debug(
            f"{'Hysteresis:':<14} {np.mean(core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['stator']['hyst']+core_loss_dict['rotor']['hyst']) : 9.3f} W"
        )
        logging.debug(
            f"{'Eddy Current:':<14} {np.mean(core_loss_dict['rotor']['eddy']) : 8.3f} W {np.mean(core_loss_dict['stator']['eddy']) : 9.3f} W {np.mean(core_loss_dict['stator']['eddy']+core_loss_dict['rotor']['eddy']) : 9.3f} W"
        )
        logging.debug(
            f"{'Excess:':<14} {np.mean(core_loss_dict['rotor']['exc']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']) : 9.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['rotor']['exc']) : 9.3f} W"
        )
        logging.debug(
            "---------------------------------------------------------------------"
        )
        logging.debug(
            f"{'Summe:':<14} {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']) : 8.3f} W {np.mean(core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W {np.mean(core_loss_dict['rotor']['exc']+core_loss_dict['rotor']['eddy']+core_loss_dict['rotor']['hyst']+core_loss_dict['stator']['exc']+core_loss_dict['stator']['eddy']+core_loss_dict['stator']['hyst']) : 9.3f} W"
        )
    return results_dict
