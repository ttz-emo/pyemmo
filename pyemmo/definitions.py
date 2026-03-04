#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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

import logging
import sys
from os import mkdir
from os.path import abspath, dirname, isdir, join, normpath, realpath

from matplotlib import font_manager

logger = logging.getLogger(__name__)
ROOT_DIR = normpath(abspath(join(dirname(__file__), ".."))).replace(
    "\\", "/"
)  #: :meta hide-value:
"""Path: ROOT_DIR is "pyemmo" root development directory with "dist", "doc", "pyemmo",
"tests" and "workingDirectory" as subfolders.

:meta hide-value:
"""

# Further import
try:
    from pyemmo import USER_DIR

    from .functions.init_environment import get_config_dict
except ImportError:
    # Add root dir to python path
    sys.path.insert(0, ROOT_DIR)

    # fixed per Issue: [B102:exec_used]
    # exec("from pyemmo.functions.init_environment import get_config_dict")
    # exec("from pyemmo import PACKAGE_NAME, USER_DIR")

    from pyemmo import USER_DIR
    from pyemmo.functions.init_environment import get_config_dict

MAIN_DIR = dirname(realpath(__file__)).replace("\\", "/")  # main dir is pyemmo
r"""Path: MAIN_DIR is "pyemmo" main package directory with "script", "functions" and
"api" as subpackages. Should be ``ROOT_DIR\pyemmo``.

:meta hide-value:
"""

RESULT_DIR = join(USER_DIR, "Results").replace("\\", "/")
r"""Path: RESULT_DIR is "pyemmo" default result directory to store model files
and simulation results. For Windows this is something like:
``'C:\\Users\\Username\\AppData\\Roaming\\pyemmo\\Results'``

For Linux its:
``'/home/.local/share/Results'``

:meta hide-value:
"""
if not isdir(RESULT_DIR):
    logger.info("Default results directory has not been created or was removed!")
    logger.info("Creating results folder: RESULT_DIR = %s!", RESULT_DIR)
    mkdir(RESULT_DIR)
TEST_DIR = join(ROOT_DIR, "tests").replace("\\", "/")

CONF_PATH = join(USER_DIR, "main_config_dict.json").replace("\\", "/")

# Matplotlib definitions
# Get a "sans-serif" font as default (works for Linux and Windows)
DEFAULT_FONT = font_manager.FontProperties(family=["sans-serif"]).get_name()
DEFAULT_COLOR_MAP = "RdBu_r"
LINE_COLOR = "b"  # blue
POINT_COLOR = "k"  # black

# Load the config file (create one if it doesn't exist)
config_dict = get_config_dict()

# default absolute geometric tolerance to check wheter points or distances are equal.
DEFAULT_GEO_TOL = 1e-7  # in [m]
"""Pyemmo default geometric tolerance e.g. used when checking for equality of
coordinates."""
logger.debug("Default geometric tolerance is set to %e meter.", DEFAULT_GEO_TOL)
