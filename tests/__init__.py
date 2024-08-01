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
import os
import platform
import subprocess
from os.path import abspath, dirname, join

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


GMSH_EXE = ""
GETDP_EXE = ""
if platform.system() == "Windows":
    # Download and install the newest ONELAB installation for testing
    subprocess.run(
        ["powershell", f"{TEST_DIR}\\install_onelab.ps1"], check=True
    )
    gmsh_exe_id = "GMSH_TEST_PATH"  # default file name from ps script
    getdp_exe_id = "GETDP_TEST_PATH"  # default file name from ps script

    exe_paths = []
    for file in (gmsh_exe_id, getdp_exe_id):
        # utf-16 encoding default for my powershell version
        with open(os.path.join(TEST_DIR, file), encoding="utf-16") as f:
            # read exe path but skip newline char
            exe_paths.append(f.readline()[:-1])
    # set Gmsh and GetDP paths
    for path in exe_paths:
        if "gmsh.exe" in path:
            GMSH_EXE = path
        elif "getdp.exe" in path:
            GETDP_EXE = path
        else:
            pass
# # Skipping environ var solution because vs-code needs to be restarted to
# # actually get the environ changes...
# if gmsh_exe_id in my_env:
#     GMSH_EXE = my_env[gmsh_exe_id]
#     print(f"Gmsh exe is {GMSH_EXE}")
# else:
#     raise FileNotFoundError(f"Could not find gmsh exe in environ: {my_env}")

# if getdp_exe_id in my_env:
#     GETDP_EXE = my_env[getdp_exe_id]
#     print(f"getdp exe is {GETDP_EXE}")
# else:
#     raise FileNotFoundError(f"Could not find getdp exe in environ: {my_env}")
