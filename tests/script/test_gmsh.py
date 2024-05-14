import pytest
import os
import subprocess
from pyemmo.functions.runOnelab import createGMSHCommand
from tests import GMSH_EXE, TEST_DATA_DIR


# @pytest.mark.parametrize("test_name,corrected_name",[
#     ('test#name','test_name'),
#     ('0testname','_0testname'),
# ])
def test_run_gmsh():
    """Simple test to check if gmsh executable is set correctly by automatic
    installation and mesh command is correct and runs."""
    geo_file = os.path.join(TEST_DATA_DIR, "MACHINE_TEST.geo")
    assert os.path.isfile(geo_file)
    gmsh_command = createGMSHCommand(
        gmshFile=geo_file, useGUI=False, gmshPath=GMSH_EXE, logFileName=""
    )
    out = subprocess.run(
        gmsh_command, check=False, capture_output=True, text=True
    )
    print(out)


if __name__ == "__main__":
    test_run_gmsh()
