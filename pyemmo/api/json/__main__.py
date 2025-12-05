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
from __future__ import annotations

import argparse
import logging

from ...definitions import RESULT_DIR
from .json import main

logger = logging.getLogger("pyemmo.api.json.__main__")
# 1. Check that all argvs are valid!
parser = argparse.ArgumentParser(
    description="Process Motor-JSON files to generate a Onelab Simulation."
)
parser.add_argument(
    "geo",
    help="path to the JSON geometry file ('geometry.json')",
    type=str,
)
parser.add_argument(
    "extInfo",
    help="path to the extended info JSON file ('extendedInfo.json')",
    type=str,
)
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
    help="path where the model files should be stored",
    type=str,
    default=RESULT_DIR,
)
parser.add_argument(
    "--res",
    help="path where the simulation results should be stored",
    type=str,
    default="",
)
parser.add_argument(
    "--log",
    help="logging level for execution. Options are: error, warning, info, debug. default is warning",
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
            logger.info("Removing log handler %s", handler.name)
            logger.removeHandler(handler)

# set log level
loglevel = args.log
logLevelNum = getattr(logging, loglevel.upper(), None)
if not isinstance(logLevelNum, int):
    raise ValueError(f"Invalid log level: {loglevel}")
# set log level of top level pyemmo logger:
pyemmoLogger = logging.getLogger("pyemmo")
pyemmoLogger.setLevel(logLevelNum)

logger.info("Set global log level to '%s'", loglevel)
logger.info("Running pyemmo.json.api.main()")
# TODO: Log arguments

main(
    geo=args.geo,
    extInfo=args.extInfo,
    gmsh=args.gmsh,
    getdp=args.getdp,
    model=args.mod,
    results=args.res,
)
