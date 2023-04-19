# -*- coding: utf-8 -*-
import sys
from os import mkdir
from os.path import abspath, dirname, join, normpath, realpath, isdir
from matplotlib import font_manager

ROOT_DIR = normpath(abspath(join(dirname(__file__), ".."))).replace("\\", "/")
"""Path: ROOT_DIR is "PyDraft" root development directory with "dist", "doc", "pydraft",
"tests" and "workingDirectory" as subdirs. """

# Further import
try:
    from .functions.init_environment import get_config_dict
    from pydraft import USER_DIR
except ImportError:
    # Add root dir to python path
    sys.path.insert(0, ROOT_DIR)
    exec("from pydraft.functions.init_environment import get_config_dict")
    exec("from pydraft import PACKAGE_NAME, USER_DIR")

MAIN_DIR = dirname(realpath(__file__)).replace("\\", "/")  # main dir is pydraft
"""Path: MAIN_DIR is "pydraft" main package directory with "script", "functions" and
"api" as subpackages """

RESULT_DIR = join(USER_DIR, "Results").replace("\\", "/")
r"""Path: RESULT_DIR is "pydraft" default result directory to store model files and simulation results.
For Windows this is something like: 'C:\\Users\\Username\\AppData\\Roaming\\PyDraft\\Results' """
if not isdir(RESULT_DIR):
    mkdir(RESULT_DIR)
TEST_DIR = join(MAIN_DIR, "tests").replace("\\", "/")

CONF_PATH = join(USER_DIR, "main_config_dict.json").replace("\\", "/")

# Matplotlib definitions
# Get a "sans-serif" font as default (works for Linux and Windows)
DEFAULT_FONT = font_manager.FontProperties(family=["sans-serif"]).get_name()
DEFAULT_COLOR_MAP = "RdBu_r"

# Load the config file (create one if it doesn't exist)
config_dict = get_config_dict()

# default absolute geometric tolerance to check wheter points or distances are equal.
DEFAULT_GEO_TOL = 1e-7  # in [m]
