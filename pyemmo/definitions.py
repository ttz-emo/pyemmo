# -*- coding: utf-8 -*-
import sys
from os import mkdir
from os.path import abspath, dirname, join, normpath, realpath, isdir
import logging
from matplotlib import font_manager

ROOT_DIR = normpath(abspath(join(dirname(__file__), ".."))).replace("\\", "/")
"""Path: ROOT_DIR is "pyemmo" root development directory with "dist", "doc", "pyemmo",
"tests" and "workingDirectory" as subdirs. """

# Further import
try:
    from .functions.init_environment import get_config_dict
    from pyemmo import USER_DIR
except ImportError:
    # Add root dir to python path
    sys.path.insert(0, ROOT_DIR)
    exec("from pyemmo.functions.init_environment import get_config_dict")
    exec("from pyemmo import PACKAGE_NAME, USER_DIR")

MAIN_DIR = dirname(realpath(__file__)).replace("\\", "/")  # main dir is pyemmo
"""Path: MAIN_DIR is "pyemmo" main package directory with "script", "functions" and
"api" as subpackages """

RESULT_DIR = join(USER_DIR, "Results").replace("\\", "/")
r"""Path: RESULT_DIR is "pyemmo" default result directory to store model files and simulation results.
For Windows this is something like: 'C:\\Users\\Username\\AppData\\Roaming\\pyemmo\\Results' """
if not isdir(RESULT_DIR):
    mkdir(RESULT_DIR)
TEST_DIR = join(ROOT_DIR, "tests").replace("\\", "/")

CONF_PATH = join(USER_DIR, "main_config_dict.json").replace("\\", "/")

# Matplotlib definitions
# Get a "sans-serif" font as default (works for Linux and Windows)
DEFAULT_FONT = font_manager.FontProperties(family=["sans-serif"]).get_name()
DEFAULT_COLOR_MAP = "RdBu_r"

# Load the config file (create one if it doesn't exist)
config_dict = get_config_dict()

# default absolute geometric tolerance to check wheter points or distances are equal.
DEFAULT_GEO_TOL = 1e-7  # in [m]
logging.debug("Default geometric tolerance is set to %e meter.",DEFAULT_GEO_TOL)
