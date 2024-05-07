import os
from os.path import join
import subprocess
from pyemmo.functions.runOnelab import createGMSHCommand
from tests import GMSH_EXE, TEST_DATA_DIR


def test_run_gmsh():
    """Simple test to check if gmsh executable is set correctly by automatic
    installation and mesh command is correct and runs."""
    model_name = "MACHINE_TEST"
    geo_file = join(TEST_DATA_DIR, model_name + ".geo")
    assert os.path.isfile(geo_file)
    gmsh_command = createGMSHCommand(
        gmshFile=geo_file, useGUI=False, gmshPath=GMSH_EXE, logFileName=""
    )
    out = subprocess.run(
        gmsh_command, check=True, capture_output=True, text=True
    )
    for res_ext in (".db", ".msh"):
        res_file = join(TEST_DATA_DIR, model_name + res_ext)
        if os.path.isfile(res_file):
            os.remove(res_file)
        else:
            raise FileNotFoundError(
                f"Coult not find gmsh result file: {res_file}"
            )


if __name__ == "__main__":
    test_run_gmsh()
