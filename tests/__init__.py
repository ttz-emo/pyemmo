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
import sys
import os
import subprocess
from os.path import join, dirname, abspath
from pyemmo.definitions import TEST_DIR

try:
    import hypothesis
except ImportError:
    pass
else:
    from hypothesis import configuration

    configuration.set_hypothesis_home_dir(join(TEST_DIR, ".hypothesis_venv"))

TEST_DATA_DIR = os.path.join(TEST_DIR, "data")

# # add pyemmo to path
# test_root = abspath(join(dirname(__file__), ".."))
# print(f"Parent directory in tests.__init__.py is: {test_root}")
# if test_root not in sys.path:
#     sys.path.append(test_root)

save_path = join(TEST_DIR, "Results").replace("\\", "/")
"""save_path is the path where the test resutls should be stored temporarily"""

# Download and install the newest ONELAB installation for testing
subprocess.run(f"powershell.exe {TEST_DIR}\\install_onelab.ps1", check=False)
gmsh_exe_id = "GMSH_TEST_PATH"
GMSH_EXE = ""
if gmsh_exe_id in os.environ:
    GMSH_EXE = os.environ[gmsh_exe_id]

getdp_exe_id = "GETDP_TEST_PATH"
GETDP_EXE = ""
if getdp_exe_id in os.environ:
    GETDP_EXE = os.environ[getdp_exe_id]
