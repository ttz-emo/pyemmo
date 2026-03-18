#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
from __future__ import annotations

from os.path import join

import pytest

from pyemmo.functions.run_onelab import create_command
from tests import GETDP_EXE, GMSH_EXE, TEST_DATA_DIR, TEST_TEMP_DIR


@pytest.mark.parametrize(
    (
        "onelabFile",
        "useGUI",
        "gmshPath",
        "getdpPath",
        "logFileName",
        "paramDict",
        "postOperations",
        "command",
    ),
    [
        (
            join(TEST_DATA_DIR, "onelab", "Toyota_Prius", "Toyota_Prius.pro"),
            False,
            GMSH_EXE,
            GETDP_EXE,
            r"my_log_file_name.log",
            {
                "verbosity level": 3,
                "param1": 10.0,
                # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                "res": join(TEST_TEMP_DIR, "create_cmd_command", "res"),
            },
            [],  # post operation list
            f"""{GMSH_EXE} "{join(TEST_DATA_DIR, "onelab", "Toyota_Prius", "Toyota_Prius.geo")}" -run && {GETDP_EXE} "{join(TEST_DATA_DIR, "onelab", "Toyota_Prius", "Toyota_Prius.pro")}" -solve Analysis -v 3 -setnumber param1 10.0 -setstring res {join(TEST_TEMP_DIR, "create_cmd_command", "res")}""",
        ),
        (  # GUI -> TRUE
            join(TEST_DATA_DIR, "onelab", "Toyota_Prius", "Toyota_Prius.pro"),
            True,
            GMSH_EXE,
            GETDP_EXE,
            r"my_log_file_name.log",
            {
                "verbosity level": 3,
                "param1": 10.0,
                # "msh": os.path.join(MODEL_DIR, "mesh_veryFine.msh"),
                "res": join(TEST_TEMP_DIR, "create_cmd_command", "res"),
            },
            [],  # post operation list
            f"""{GMSH_EXE} "{join(TEST_DATA_DIR, "onelab", "Toyota_Prius", "Toyota_Prius.pro")}\"""",
        ),
    ],
)
def test_create_cmd_command(
    onelabFile: str,
    useGUI: bool,
    gmshPath: str,
    getdpPath: str,
    logFileName: str,
    paramDict: dict,
    postOperations: list[str],
    command: str,
):

    created_command = create_command(
        onelabFile,
        useGUI,
        gmshPath,
        getdpPath,
        logFileName,
        paramDict,
        postOperations,
    )
    assert command == created_command
