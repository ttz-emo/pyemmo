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
"""
Test module for automatic onelab installation by install_onelab.ps1 script.

The PowerShell script downloads the latest onelab version from the onelab
website (https://onelab.info/files) and installs it in
"tests/data/YYMMDD_onelab".
This script is called by tests/__init__.py and sets the gmsh and getdp
executable paths through the files "GMSH_TEST_PATH" and "GETDP_TEST_PATH" in
the tests directory.

This module uses the new gmsh installation for the tests and runs it on a
sample machine script ("tests/data/MACHINE_TEST.geo") to make sure the actual
gmsh version does work with the .geo files created by PyEMMO.
TODO: Create the test.geo machine script automatically to make sure that really
the latest PyEMMO version is tested.
"""
import os
from os.path import join
import subprocess
from pyemmo.functions.runOnelab import createGMSHCommand
from tests import GMSH_EXE, TEST_DATA_DIR
import logging


def test_run_gmsh():
    """Simple test to check if gmsh executable is set correctly by automatic
    installation and mesh command is correct and runs."""
    if not GMSH_EXE:
        logging.warning(
            "Skipping gmsh exe tests because GMSH_EXE was not set for tests"
        )
        return None
    model_name = "MACHINE_TEST"
    geo_file = join(TEST_DATA_DIR, model_name + ".geo")
    assert os.path.isfile(geo_file)
    gmsh_command = createGMSHCommand(
        gmshFile=geo_file, useGUI=False, gmshPath=GMSH_EXE, logFileName=""
    )
    _ = subprocess.run(
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
