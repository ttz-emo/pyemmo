import os
import pytest
import re
from pyemmo.functions.import_results import read_timetable_dat
from pyemmo.functions.import_results import read_RegionValue_dat
from pyemmo.definitions import TEST_DIR
import numpy as np

@pytest.mark.parametrize(
   "file_path",
    [
        
       ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"),
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Flux_0.dat"),
    ],
)
def test_read_timtable_dat_file_exists(file_path):
    """Test that the function raises a FileNotFound Error when a invalid file is given"""
    assert os.path.isfile(file_path),f"The data file '{file_path}' does not exist!"
@pytest.mark.parametrize(
    "file_path",
    [
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"),
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Flux_0.dat"),
    ],
)

def test_read_dat_file_size(file_path):
    """Test that the data file has atleast one value"""
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    assert data_array.size>0,f"The data file '{file_path}' does not contain any values!"

@pytest.mark.parametrize(
   "file_path",
    [
        
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"),
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Flux_0.dat"),
    ],
)
def test_read_Regionvalue_dat(file_path):
    """Test that the function raises a FileNotFound Error when a invalid file is given"""
    assert os.path.isfile(file_path),f"The data file '{file_path}' does not exist!"

@pytest.mark.parametrize(
   "file_path",
    [
        
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Ib.dat"),
        ("C:/Users/k54149/Documents/pyemmo/Results/Baukasten/Test_SPMSM/res_Test_SPMSM_Baukasten/Flux_0.dat"),
    ],
)
def test_read_Regionvalue_dat(file_path):
    """Test that there are no multiple lines in 'Region Value' format """
    data_array = np.loadtxt(file_path, dtype=float, comments="#")
    assert len(data_array.shape) == 1, "Multiple lines in 'RegionValue' format"
    
