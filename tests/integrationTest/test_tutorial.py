#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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

# import os
import subprocess
import sys
from os.path import abspath, join, normpath

import pytest

from pyemmo.definitions import ROOT_DIR

TUTORIAL_DIR = normpath(abspath(join(ROOT_DIR, "tutorials")))
tutorial_files = ["pyleecan_api.py"]


@pytest.mark.parametrize(("tutorial_file"), tutorial_files)
def test_run_tutorial_script(tutorial_file):
    """Test run tutorial files"""
    logger = logging.getLogger(__file__)
    logger.info("Running tutorial file: %s", tutorial_file)
    tuto_path = join(TUTORIAL_DIR, tutorial_file)
    retcode = subprocess.call([sys.executable, tuto_path], shell=False)
    assert retcode == 0, "Tutorial failed..."

    # with open(tuto_path, encoding="utf-8") as tuto_file:
    #     code = tuto_file.readlines()
    #     # remove lines with GUI call to run tutorial without UI
    #     _ = [code.remove(line) for line in code if "gmsh.fltk.run" in line]
    #     # remove get_ipython
    #     _ = [code.remove(line) for line in code if "get_ipython" in line]
    #     exec("".join(code))
