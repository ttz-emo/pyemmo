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
import logging
import os
import platform
import subprocess

from pyemmo.definitions import TEST_DIR

try:
    from hypothesis import configuration
except ImportError:
    pass
else:
    configuration.set_hypothesis_home_dir(os.path.join(TEST_DIR, ".hypothesis_venv"))

TEST_DATA_DIR = os.path.join(TEST_DIR, "data")

# # add pyemmo to path
# test_root = abspath(join(dirname(__file__), ".."))
# print(f"Parent directory in tests.__init__.py is: {test_root}")
# if test_root not in sys.path:
#     sys.path.append(test_root)

save_path = os.path.join(TEST_DIR, "Results").replace("\\", "/")
"""save_path is the path where the test resutls should be stored temporarily"""


GMSH_EXE = ""
GETDP_EXE = ""
if platform.system() == "Windows":
    # Download and install the newest ONELAB installation for testing
    try:
        p = subprocess.run(
            ["powershell", os.path.join(TEST_DIR, "install_onelab.ps1")],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        # subprocess failed -> no determination of executables
        logging.warning(
            "Failed to execute 'install_onelab.ps1' properly. "
            "Could not determine ONELAB executables for testing!"
        )
    else:
        if not p.stderr:
            output = [x for x in p.stdout.decode().split("\r\n") if len(x) > 1]
            GMSH_EXE = os.path.abspath(output[-2])
            GETDP_EXE = os.path.abspath(output[-1])
            logging.info(
                "Found Gmsh and GetDP executables for testing.\n%s\n%s",
                GMSH_EXE,
                GETDP_EXE,
            )
        else:
            # additional check because ps does not return non-zero for typos...
            logging.warning(
                "Failed to execute 'install_onelab.ps1' properly. Error:\n%s",
                p.stderr,
            )
else:
    logging.warning(
        "Determination of ONELAB executables for testing not implemented "
        "for non-Windows distibution yet!"
    )
