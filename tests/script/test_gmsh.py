import os
import subprocess
from pyemmo.functions.runOnelab import createGMSHCommand
from tests import GMSH_EXE, TEST_DATA_DIR


def test_run_gmsh():
    """Simple test to check if gmsh executable is set correctly by automatic
    installation and mesh command is correct and runs."""
    geo_file = os.path.join(TEST_DATA_DIR, "MACHINE_TEST.geo")
    assert os.path.isfile(geo_file)
    gmsh_command = createGMSHCommand(
        gmshFile=geo_file, useGUI=False, gmshPath=GMSH_EXE, logFileName=""
    )
    out = subprocess.run(
        gmsh_command, check=True, capture_output=True, text=True
    )
    # TODO: Check that .db and .msh file are created and clean them up after
    # test run


if __name__ == "__main__":
    test_run_gmsh()
