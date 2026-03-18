#
# Copyright (c) 2018-2025 M. Schuler & V. Patil, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""Module for testing the import_results module"""
from __future__ import annotations

from os.path import abspath, join

import numpy as np
import pytest

from pyemmo.functions.import_results import (
    freq_from_signal,
    get_result_files,
    import_pos,
    import_pos_legacy,
    import_sp,
    plot_timetable_dat,
    read_RegionValue_dat,
    read_timetable_dat,
    split_data,
)

try:
    from .. import TEST_DATA_DIR
except ImportError:
    from pyemmo.definitions import TEST_DIR

    TEST_DATA_DIR = join(TEST_DIR, "data")
except Exception as exce:
    raise exce

IMP_RES_TEST_DATA_DIR = join(TEST_DATA_DIR, "functions", "import_results")


# @pytest.mark.parametrize(
#     "file_path",
#     [join(IMP_RES_TEST_DATA_DIR, "Ib_test.dat")],
# )
def test_read_timetable_dat():
    """Tests the function read_timetable_dat. Tests if the size and values of
    the data array are correct."""
    time, data = read_timetable_dat(join(IMP_RES_TEST_DATA_DIR, "Ib_test.dat"))
    assert data.size == 4, "Wrong data array size."
    assert time.size == 4, "Wrong time array size."
    assert_time_array = [0, 0, 0.01, 0.02]
    assert_data_array = np.reshape([0, 0, 1.0, 2.0], (4, 1))
    assert np.array_equal(assert_time_array, time)
    assert np.array_equal(assert_data_array, data)


@pytest.mark.parametrize(
    "file_path",
    [join(IMP_RES_TEST_DATA_DIR, "region_value_data.dat")],
)
def test_import_region_value(file_path):
    """
    Tests if the Time and Data Values are imported correctly from dat-file in
    Region Value format.
    """
    # read region value formated test file
    time, data = read_RegionValue_dat(file_path)
    # time assertion array
    target_time = np.array([0, 0.5], dtype=float)
    # data assertion array
    target_values = np.array([0.1, 1.5], dtype=float)
    # assert that the values match
    assert np.all(np.isclose(time, target_time, 1e-6))
    assert np.all(np.isclose(data, target_values, 1e-6))


def test_split_data():
    """Test split_data function"""
    time = np.array([0.0, 1.0, 2.0, 0.0, 1.0], dtype=float)
    values = np.array([0.1, 1.1, 2.1, 0.2, 1.2], dtype=float)
    test_nbr_sims, test_time_list, test_data_list = split_data(time, values)
    for x in range(time.size):
        if time[x] == 0:
            assert time[x + 1] != 0, "There is a same time step, twice in a row!"
    target_nbr_sims = 2
    target_time_1 = [
        np.array([0.0, 1.0, 2.0], dtype=float),
        np.array([0.0, 1.0], dtype=float),
    ]
    target_value_1 = [
        np.array([0.1, 1.1, 2.1], dtype=float),
        np.array([0.2, 1.2], dtype=float),
    ]
    assert (
        target_nbr_sims == test_nbr_sims
    ), " Incorrect number of Simulations imported! "

    assert np.array_equal(
        target_time_1[0], test_time_list[0]
    ), " Incorrect timesteps imported!"
    assert np.array_equal(
        target_time_1[1], test_time_list[1]
    ), "Incorrect timesteps imported!"

    assert np.array_equal(
        target_value_1[0], test_data_list[0]
    ), "Incorrect Values imported!"
    assert np.array_equal(
        target_value_1[1], test_data_list[1]
    ), "Incorrect Values imported!"


def test_plot_timetable_dat():
    """
    Tests that the number offigures created is equal to the number of
    Simulations.
    """
    file_path = join(IMP_RES_TEST_DATA_DIR, "Ib_test.dat")

    plot_list = plot_timetable_dat(
        file_path=file_path,
        data_label="DataLabel",
        title="Graph",
        savefig=False,
        showfig=False,
        savepath="",
    )
    number_of_figures = 2
    assert (
        len(plot_list) == number_of_figures
    ), "The number of figures does not match the number of simulations!"


def test_import_SP():
    """
    Tests the data name, time array, postion array and value array of the
    imported .pos file
    """
    file_path = join(IMP_RES_TEST_DATA_DIR, "btan_test.pos")
    test_tuple = import_sp(file_path)
    assert_tuple = (
        "b_tangent",
        [],
        [
            (0.06349364999999998, 0.0, 0.0),
            (0.0634912323563634, 0.0005540795906463301, 0.0),
            (0.06348397960956659, 0.001108116985986626, 0.0),
        ],
        [
            [-0.05582340238180805],
            [-0.05609076949641559],
            [-0.05854188999837832],
        ],
    )

    assert np.array_equal(
        test_tuple[0], assert_tuple[0]
    ), " Incorrect Data name Imported!"
    for x in range(len(assert_tuple[1]) - 1):
        assert np.array_equal(
            test_tuple[1][x], assert_tuple[1][x]
        ), "Incorrect Time-Array Imported!"

    for x in range(len(assert_tuple[2]) - 1):
        assert np.array_equal(
            test_tuple[2][x], assert_tuple[2][x]
        ), "Incorrect Postion-Array Imported!"

    for x in range(len(assert_tuple[3]) - 1):
        assert np.array_equal(
            test_tuple[3][x], assert_tuple[3][x]
        ), "Incorrect Value-Array Imported!"


@pytest.mark.parametrize(
    ("parsed_pos_file", "dType", "numElem", "numNodes", "numDataPoints"),
    [
        (join(IMP_RES_TEST_DATA_DIR, "btan_test.pos"), "SP", 181, 1, 1),
        (
            join(IMP_RES_TEST_DATA_DIR, "SP_fomatted_res_file.pos"),
            "SP",
            1,
            1,
            3,
        ),
        (
            join(IMP_RES_TEST_DATA_DIR, "VL_GmshParsed_static.pos"),
            "VL",
            3,
            2,
            3,
        ),
    ],
)
def test_import_pos_parsed(parsed_pos_file, dType, numElem, numNodes, numDataPoints):
    """Test _import_pos_parsedFormat function

    Args:
        parsed_pos_file (str): Path to GmshParsed formatted .pos file
        dType (str): Data type (in SP,SL,ST,VP,VL,VT)
        numElem (int): number of elements in result file.
        numNodes (int): Number of nodes per element.
        numDataPoints (int): number of data values per node.
    """
    data_type, nodes, data = import_pos_legacy(parsed_pos_file)
    assert data_type == dType
    # numNodes * 3 = number of coordinates
    assert nodes.shape == (numElem, numNodes * 3)
    assert data.shape == (numElem, numNodes * numDataPoints)


# @pytest.mark.parametrize(
#     "file_path",
#     [join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")],
# )
def test_import_pos():
    """
    Tests if the imported values (gmsh mesh element tags, time, data array)
    from a POS file are correct.
    """
    test_posFile_path = join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")
    mesh_elemt_ids = np.load(
        (join(IMP_RES_TEST_DATA_DIR, "import_pos_mesh_elem_ids.npy")),
        allow_pickle=True,
    )
    time = np.load(
        (join(IMP_RES_TEST_DATA_DIR, "import_pos_time.npy")),
        allow_pickle=True,
    )
    data = np.load(
        (join(IMP_RES_TEST_DATA_DIR, "import_pos_data.npy")),
        allow_pickle=True,
    )
    imp_mesh_elem, imp_time, imp_data = import_pos(test_posFile_path)
    assert np.array_equal(
        mesh_elemt_ids, imp_mesh_elem
    ), "Incorrect Mesh elements Imported!"
    assert np.array_equal(time, imp_time), "Incorrect Time stamps Imported!"
    assert np.array_equal(data, imp_data), "Incorrect Data Array Imported!"


@pytest.mark.parametrize(
    "test_pos_path",
    [
        abspath(join(IMP_RES_TEST_DATA_DIR, "VL_GmshParsed_static.pos")),
        abspath(join(IMP_RES_TEST_DATA_DIR, "SP_GmshParsed_transient.pos")),
    ],
)
def test_import_pos_parsed_workaround(test_pos_path):
    """Just make sure the workaround for GmshParsed formatted pos files works"""
    imp_mesh_elem, imp_time, imp_data = import_pos(test_pos_path)


# @pytest.mark.parametrize(
#     "file_path",
#     [join(IMP_RES_TEST_DATA_DIR, "functions", "import_results")],
# )
def test_get_result_files():
    """Test the function get_result_files"""
    file_path = IMP_RES_TEST_DATA_DIR
    dat_file_list, pos_file_list = get_result_files(file_path)
    dat_file_list.sort()
    assert np.array_equal(
        dat_file_list, ["Ib_test.dat", "region_value_data.dat"]
    ), "Incorrect list of .dat files!"
    pos_file_list.sort()
    assert np.array_equal(
        pos_file_list,
        [
            "AxialeLaenge_test.pos",
            "SP_GmshParsed_transient.pos",
            "SP_fomatted_res_file.pos",
            "VL_GmshParsed_static.pos",
            "btan_test.pos",
        ],
    ), "Incorrect list of .pos files!"


def test_freq_from_signal():
    """Test the function freq_from_signal"""
    # Test signal with known frequency
    fs = 1000  # Sampling frequency
    f = 5  # Frequency of the signal
    t = np.arange(0, 1, 1 / fs)  # Time vector of 1 second
    # Generate sine wave signal with noise:
    signal = np.sin(2 * np.pi * f * t) + 0.1 * np.random.normal(0, 1, len(t))

    estimated_freq = freq_from_signal(signal, fs)
    assert np.isclose(
        estimated_freq, f, atol=0.5
    ), "Estimated frequency is not close to actual frequency!"


# if __name__ == "__main__":
# Test usage of importPos function:
# mesh_element_tag, time, data = importPos(
#   join(IMP_RES_TEST_DATA_DIR,"AxialeLaenge_test.pos")
# )
# print(mesh_element_tag)
# print(time)
# print(data)

# test_import_pos(
#     join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")
# )

# test_import_pos(join( IMP_RES_TEST_DATA_DIR,"AxialeLaenge_test.pos"))
# print
# Test usage of get_result_files function:
# dat_file_list, pos_file_list = get_result_files(
#     join(IMP_RES_TEST_DATA_DIR, "functions", "import_results")
# )
# for filename in dat_file_list + pos_file_list:
#     print(filename)
