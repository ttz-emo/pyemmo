import os
from os import path, PathLike
from cmath import isclose
from typing import List, Tuple, Union
import warnings
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from parse import parse
import gmsh

from pyemmo.functions.import_results import (
    read_timetable_dat,
    importPos,
    read_RegionValue_dat,
    split_data,
    plot_timetable_dat,
    importSP,
    get_result_files,
)
import pytest

try:
    from .. import TEST_DATA_DIR
except ImportError:
    from pyemmo.definitions import TEST_DIR

    TEST_DATA_DIR = os.path.join(TEST_DIR, "data")
except Exception as exce:
    raise exce

IMP_RES_TEST_DATA_DIR = os.path.join(
    TEST_DATA_DIR, "functions", "import_results"
)


# @pytest.mark.parametrize(
#     "file_path",
#     [os.path.join(IMP_RES_TEST_DATA_DIR, "Ib_test.dat")],
# )
def test_read_timetable_dat():
    """Tests the function read_timetable_dat. Tests if the size and values of
    the data array are correct."""
    time, data = read_timetable_dat(
        os.path.join(IMP_RES_TEST_DATA_DIR, "Ib_test.dat")
    )
    assert data.size == 4, "Wrong data array size."
    assert time.size == 4, "Wrong time array size."
    assert_time_array = [0, 0, 0.01, 0.02]
    assert_data_array = np.reshape([0, 0, 1.0, 2.0], (4, 1))
    assert np.array_equal(assert_time_array, time)
    assert np.array_equal(assert_data_array, data)


@pytest.mark.parametrize(
    "file_path",
    [os.path.join(IMP_RES_TEST_DATA_DIR, "Surf_StLu2_test.dat")],
)
def test_Region_value(file_path):
    """
    Tests if the Time and Data Values are imported correctly from dat-file in
    Region Value format.
    """
    # read region value formated test file
    data_array = read_RegionValue_dat(file_path)
    # time assertion array
    time_array = np.ndarray(
        (1,), buffer=np.array([0.001666666666666667]), dtype=float
    )
    # data assertion array
    value_array = np.ndarray(
        (1,), buffer=np.array([7.609826513417671e-05]), dtype=float
    )
    # combine the assions arrays to a test tuple
    test_tuple = (time_array, value_array)
    # assert that the values match
    assert np.array_equal(
        data_array, test_tuple
    ), "Time and Data Values were imported incorrectly!"


def test_split_data():
    """Test split_data function"""
    time = np.array([0.0, 1.0, 2.0, 0.0, 1.0], dtype=float)
    values = np.array([0.1, 1.1, 2.1, 0.2, 1.2], dtype=float)
    test_tuple = split_data(time, values)
    for x in range(time.size):
        if time[x] == 0:
            assert (
                time[x + 1] != 0
            ), "There is a same time step, twice in a row!"
    nbr_sims = 2
    assert_time1 = [
        np.array([0.0, 1.0, 2.0], dtype=float),
        np.array([0.0, 1.0], dtype=float),
    ]
    assert_values1 = [
        np.array([0.1, 1.1, 2.1], dtype=float),
        np.array([0.2, 1.2], dtype=float),
    ]
    assert (
        nbr_sims == test_tuple[0]
    ), " Incorrect number of  Simulations imported! "

    assert np.array_equal(
        assert_time1[0], test_tuple[1][0]
    ), " Incorrect timesteps imported!"
    assert np.array_equal(
        assert_time1[1], test_tuple[1][1]
    ), "Incorrect timesteps imported!"

    assert np.array_equal(
        assert_values1[0], test_tuple[2][0]
    ), "Incorrect Values imported!"
    assert np.array_equal(
        assert_values1[1], test_tuple[2][1]
    ), "Incorrect Values imported!"


def test_plot_timetable_dat():
    """
    Tests that the number offigures created is equal to the number of
    Simulations.
    """
    file_path = os.path.join(IMP_RES_TEST_DATA_DIR, "Surf_StLu2_test.dat")

    plot_list = plot_timetable_dat(
        file_path=file_path,
        dataLabel="DataLabel",
        title="Graph",
        savefig=False,
        showfig=True,
        savePath=None,
    )
    number_of_figures = 1
    assert (
        len(plot_list) == number_of_figures
    ), "The number of figures does not match the number of simulations!"


def test_import_SP():
    """
    Tests the data name, time array, postion array and value array of the
    imported .pos file
    """
    file_path = os.path.join(IMP_RES_TEST_DATA_DIR, "btan_test.pos")
    test_tuple = importSP(file_path)
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


# @pytest.mark.parametrize(
#     "file_path",
#     [os.path.join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")],
# )
def test_import_pos():
    """
    Tests if the Imported values(gmsh mesh element tags,time,data array)
    from a POS file are correct.
    """
    file_path = os.path.join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")
    mesh_elemt_ids = np.load(
        (os.path.join(IMP_RES_TEST_DATA_DIR, "test_import_tuple0.npy")),
        allow_pickle=True,
    )
    time = np.load(
        (os.path.join(IMP_RES_TEST_DATA_DIR, "test_import_tuple1.npy")),
        allow_pickle=True,
    )
    data = np.load(
        (os.path.join(IMP_RES_TEST_DATA_DIR, "test_import_tuple2.npy")),
        allow_pickle=True,
    )
    imp_mesh_elem, imp_time, imp_data = importPos(file_path)
    assert np.array_equal(
        mesh_elemt_ids, imp_mesh_elem
    ), "Incorrect Mesh elements Imported!"
    assert np.array_equal(time, imp_time), "Incorrect Time stamps Imported!"
    assert np.array_equal(data, imp_data), "Incorrect Data Array Imported!"


# result_import = get_result_files(os.path.join(
#   IMP_RES_TEST_DATA_DIR, "functions", "import_results"
# ))
# np.save('get_result_files_dat.npy',result_import[0])
# np.save('get_result_files_pos.npy',result_import[1])


# @pytest.mark.parametrize(
#     "file_path",
#     [os.path.join(IMP_RES_TEST_DATA_DIR, "functions", "import_results")],
# )
def test_get_result_files():
    """Test the function get_result_files"""
    file_path = IMP_RES_TEST_DATA_DIR
    dat_file_list, pos_file_list = get_result_files(file_path)

    assert np.array_equal(
        dat_file_list, ["Ib_test.dat", "Surf_StLu2_test.dat"]
    ), "Incorrect list of .dat files!"
    assert np.array_equal(
        pos_file_list,
        [
            "AxialeLaenge_test.pos",
            "btan_test.pos",
            "pos_res_file_az.pos",
            "SP_fomatted_res_file.pos",
        ],
    ), "Incorrect list of .pos files!"


# if __name__ == "__main__":
# Test usage of importPos function:
# mesh_element_tag, time, data = importPos(
#   os.path.join(IMP_RES_TEST_DATA_DIR,"AxialeLaenge_test.pos")
# )
# print(mesh_element_tag)
# print(time)
# print(data)

# test_import_pos(
#     os.path.join(IMP_RES_TEST_DATA_DIR, "AxialeLaenge_test.pos")
# )

# test_import_pos(os.path.join( IMP_RES_TEST_DATA_DIR,"AxialeLaenge_test.pos"))
# print
# Test usage of get_result_files function:
# dat_file_list, pos_file_list = get_result_files(
#     os.path.join(IMP_RES_TEST_DATA_DIR, "functions", "import_results")
# )
# for filename in dat_file_list + pos_file_list:
#     print(filename)
