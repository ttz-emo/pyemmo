#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

# import pytest
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
