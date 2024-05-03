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

from pyemmo.functions.import_results import read_timetable_dat
from pyemmo.functions.import_results import read_RegionValue_dat
import pytest


@pytest.mark.parametrize(
    "file_path",
    [
        (
            "C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"
        )
    ],
)
def test_file_exists(file_path):
    """Tests if a File not Found Error is raised"""
    try:
        read_timetable_dat(file_path)
        os.path.isfile(
            "C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukast/Ib.dat"
        )
    except FileNotFoundError:
        pass
    except Exception as exce:
        assert False


@pytest.mark.parametrize(
    "file_path",
    [
        (
            "C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"
        )
    ],
)
def test_datasize_values(file_path):
    """Tests of the size and values of the data array are correct"""
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
    [
        (
            "C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Surf_StLu2.dat"
        )
    ],
)
def test_checkImportedValues(file_path):

    test_array = read_RegionValue_dat(file_path)
    assert_arrray = np.array((0.001666666666666667, 7.609826513417671e-05))
    assert np.array_equal(test_array, assert_arrray)
