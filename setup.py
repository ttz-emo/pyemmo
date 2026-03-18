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
"""
Configuration file for setuptools (see
https://setuptools.pypa.io/en/latest/index.html for more info on setup)

Most of the metadata is defined by the pyproject.toml file.
Still using setup.py file for depenencies and version instead of pyproject.toml
because we want to access the version number in the script generation process
"""

from __future__ import annotations

import setuptools

# /!\ Increase the number before a release
# See https://www.python.org/dev/peps/pep-0440/
# Examples :
# First alpha of the release 0.1.0 : 0.1.0a1
# First beta of the release 1.0.0 : 1.0.0b1
# Second release candidate of the release 2.6.4 : 2.6.4rc2
# Release 1.1.0 : 1.1.0
# First post release of the release 1.1.0 : 1.1.0.post1


# get version from version.py file in package,
#  because we need to access the version number from pyemmo.script

with open("pyemmo/version.py", encoding="utf-8") as versionFile:
    file_content = versionFile.read()
    version = [x for x in file_content.split("\n") if "__version__" in x][0].split("=")[
        1
    ]
    version = version.replace('"', "").replace(" ", "")

PYEMMO_VERSION = version  # # pylint: disable=locally-disabled, undefined-variable


setuptools.setup(
    version=PYEMMO_VERSION,
)
