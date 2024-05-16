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

# from .. import TEST_DATA_DIR

TEST_DATA_DIR = r"C:\Users\k54149\Documents\pyemmo\tests\data"
# TEST_DATA_DIR = r"D:\pyemmo\tests\data"


@pytest.mark.parametrize(
    "file_path",
    [os.path.join(TEST_DATA_DIR, "Ib_test.dat")],
)
def test_file_exists(file_path):
    """Tests if a File not Found Error is raised."""
    try:
        read_timetable_dat(file_path)
        os.path.isfile(os.path.join(TEST_DATA_DIR, "Ib_test.dat"))
    except FileNotFoundError:
        pass
    except Exception as exce:
        assert False


@pytest.mark.parametrize(
    "file_path",
    [os.path.join(TEST_DATA_DIR, "Ib_test.dat")],
)
def test_datasize_values(file_path):
    """Tests if the size and values of the data array are correct."""
    read_timetable_dat(file_path)
    test_data_array = np.loadtxt(file_path, dtype=float, comments="#")

    assert test_data_array.size == 8, " Wrong Data size "
    assert_data_array = [
        [0, 0],
        [0, 0],
        [0.0008333333333333333, 0],
        [0.001666666666666667, 0],
    ]
    assert np.array_equal(
        test_data_array, assert_data_array
    ), " data values are incorrect!"


@pytest.mark.parametrize(
    "file_path",
    [os.path.join(TEST_DATA_DIR, "Surf_StLu2_test.dat")],
)
def test_Region_value(file_path):
    """Tests if the Time and Data Values are imported correctly from dat-file in Region Value format."""
    data_array = read_RegionValue_dat(file_path)
    time_array = np.ndarray(
        (1,), buffer=np.array([0.001666666666666667]), dtype=float
    )
    value_array = np.ndarray(
        (1,), buffer=np.array([7.609826513417671e-05]), dtype=float
    )

    test_tuple = (time_array, value_array)

    assert np.array_equal(
        data_array, test_tuple
    ), "Time and Data Values were imported incorrectly!"


def test_split_data():

    time = np.ndarray(
        (5,), buffer=np.array([0.0, 1.0, 2.0, 0.0, 1.0]), dtype=float
    )
    values = np.ndarray(
        (5,), buffer=np.array([0.1, 1.1, 2.1, 0.2, 1.2]), dtype=float
    )

    test_tuple = split_data(time, values)

    for x in range(np.size(time)):

        if time[x] == 0:
            assert (
                time[x + 1] != 0
            ), "There is a same time step, twice in a row!"

    nbr_sims = int
    nbr_sims = 2

    assert_time1 = [
        (np.ndarray((3,), buffer=np.array([0.0, 1.0, 2.0]), dtype=float)),
        (np.ndarray((2,), buffer=np.array([0.0, 1.0]), dtype=float)),
    ]
    assert_values1 = [
        (np.ndarray((3,), buffer=np.array([0.1, 1.1, 2.1]), dtype=float)),
        (np.ndarray((2,), buffer=np.array([0.2, 1.2]), dtype=float)),
    ]

    asserttuple = (nbr_sims, assert_time1, assert_values1)
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
    """Tests that the number offigures created is equal to the number of Simulations"""
    file_path = os.path.join(TEST_DATA_DIR, "Surf_StLu2_test.dat")

    Plot_list = plot_timetable_dat(
        file_path, "DataLabel", "Graph", False, True, None
    )
    number_of_figures = 1
    assert (
        len(Plot_list) == number_of_figures
    ), " The number of figures created is not equal to the number of Simulations!"


def test_import_SP():
    """Tests the Data-name,Time vector,Postion array and Value array of the imported .pos file"""
    file_path = os.path.join(TEST_DATA_DIR, "btan_test.pos")
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
        assert np.array_equal(test_tuple[3][x], assert_tuple[3][x])
        "Incorrect Value-Array Imported!"


# tuple_import = importPos(os.path.join( TEST_DATA_DIR,"AxialeLaenge_test.pos"))
# np.save('test_import_tuple0.npy',tuple_import[0])
# np.save('test_import_tuple1.npy',tuple_import[1])
# np.save('test_import_tuple2.npy',tuple_import[2])
@pytest.mark.parametrize(
    "file_path",
    [os.path.join(TEST_DATA_DIR, "AxialeLaenge_test.pos")],
)
def test_import_pos(file_path):
    """Tests if the Imported values(gmsh mesh element tags,time,data array) from a POS file are correct"""
    mesh_elemt_ids = np.load((os.path.join( TEST_DATA_DIR,"test_import_tuple0.npy")), allow_pickle=True)
    time = np.load((os.path.join( TEST_DATA_DIR,"test_import_tuple1.npy")), allow_pickle=True)
    data = np.load((os.path.join( TEST_DATA_DIR,"test_import_tuple2.npy")), allow_pickle=True)
    imp_mesh_elem, imp_time, imp_data = importPos(file_path)
    assert np.array_equal(mesh_elemt_ids,imp_mesh_elem),"Incorrect Mesh elements Imported!"    
    assert np.array_equal(time,imp_time),"Incorrect Time stamps Imported!"
    assert np.array_equal(data,imp_data),"Incorrect Data Array Imported!"
   
  
#result_import = get_result_files(os.path.join(TEST_DATA_DIR, "functions", "import_results"))
#np.save('get_result_files_dat.npy',result_import[0])
#np.save('get_result_files_pos.npy',result_import[1])

@pytest.mark.parametrize(
    "file_path",
    [os.path.join(TEST_DATA_DIR,"functions", "import_results")],
)
def test_get_results_file(file_path):
    test_import_dat,test_import_pos = get_result_files(file_path)
    result_dat = np.load((os.path.join( TEST_DATA_DIR,"get_result_files_dat.npy")), allow_pickle=True)
    result_pos = np.load((os.path.join( TEST_DATA_DIR,"get_result_files_pos.npy")), allow_pickle=True)
    assert np.array_equal(test_import_dat,result_dat),"Incorrect list of .dat files!"
    assert np.array_equal(test_import_pos,result_pos),"Incorrect list of .pos files!"

if __name__ == "__main__":
    # Test usage of importPos function:
    # mesh_element_tag, time, data = importPos(os.path.join( TEST_DATA_DIR,"AxialeLaenge_test.pos"))
    # print(mesh_element_tag)
    # print(time)
    # print(data)

    test_import_pos(os.path.join(TEST_DATA_DIR, "AxialeLaenge_test.pos"))

    # test_import_pos(os.path.join( TEST_DATA_DIR,"AxialeLaenge_test.pos"))
    # print
    # Test usage of get_result_files function:
    dat_file_list, pos_file_list = get_result_files(
        os.path.join(TEST_DATA_DIR, "functions", "import_results")
    )
    for filename in dat_file_list + pos_file_list:
        print(filename)
