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
"""Main module of pyleecan api"""

from __future__ import annotations

import argparse
import logging
import os

from ... import rootLogger as logger
from ...definitions import RESULT_DIR
from . import use_pyleecan
from .main import main

if use_pyleecan:
    from pyleecan.Functions import load

if __name__ == "__main__":
    if not use_pyleecan:
        raise ModuleNotFoundError("Please install pyleecan!")
    # 1. Check that all argvs are valid!
    parser = argparse.ArgumentParser(
        description=(
            "Process Pyleecan machine data (saved as JSON file) to generate "
            "a Onelab Simulation."
        )
    )
    parser.add_argument(
        "file",
        help="Path to the Pyleecan-Machine-JSON file",
        type=str,
    )
    # parser.add_argument(
    #     "extInfo",
    #     help="path to the extended info JSON file ('extendedInfo.json')",
    #     type=str,
    # )
    parser.add_argument(
        "--gmsh",
        help="path to the Gmsh executable",
        type=str,
        default="",
    )
    parser.add_argument(
        "--getdp", help="path to the GetDP executable", type=str, default=""
    )
    parser.add_argument(
        "--mod",
        help="path where the model files should be stored. Defaults to {PyEMMO_RESUTLS_DIR}\\pyleecan",
        type=str,
        default=os.path.join(RESULT_DIR, "pyleecan"),
    )
    parser.add_argument(
        "--log",
        help="logging level for execution. Options are: 'error', 'warning', 'info', 'debug'. Default is warning",
        type=str,
        default="WARNING",
    )
    parser.add_argument(
        "-v",
        help="set execution to verbose. Verbosity level equals logging level.",
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()

    # remove commandline handler if not verbose
    if not args.v:
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                logger.removeHandler(handler)

    # set log level
    loglevel = args.log
    logLevelNum = getattr(logging, loglevel.upper(), None)
    if not isinstance(logLevelNum, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logger.setLevel(logLevelNum)

    main(
        pyleecan_machine=load.load(args.file),  # pylint: disable=no-member,E0606
        model_dir=args.mod,
        gmsh=args.gmsh,
        getdp=args.getdp,
    )
