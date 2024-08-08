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
"""Configuration file for setuptools (see
https://setuptools.pypa.io/en/latest/index.html for more info on setup)

Most of the metadata is defined by the pyproject.toml file.
Still using setup.py file for depenencies and version instead of pyproject.toml
because we want to access the version number in the script generation process"""

try:
    import setuptools
except ImportError:  # Install setuptools if needed
    from os import system
    from sys import executable

    # run 'pip install setuptools'
    system(f"{executable} -m pip install setuptools")

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
    exec(versionFile.read())
# from .pyemmo.version import __version__
# pylint: disable=locally-disabled, undefined-variable
PYEMMO_VERSION = __version__

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

PYTHON_REQUIRES = ">= 3.6"

# Pyleecan dependancies
install_requires = [
    "pyleecan>=1.5.1",
    "swat_em>=0.6.3",
    "pygetdp>=1.0.0",
    "gmsh>=4.10.3",
    "matplotlib>=3.3.4",
    "pandas>=1.2.4",
    "numpy>=1.23.1",
    "parse>=1.19.0",
    "splines>=0.3.2",
]

setuptools.setup(
    # name="pyemmo",
    version=PYEMMO_VERSION,
    # author="AG-EM TTZ-EMO",
    # author_email="max.schuler@thws.de",
    # description="PyEMMO is a interface for modeling electrical machines in the open-source FEA software Onelab",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url=r"https://gitlab.ttz-emo.thws.de/ag-em/pyemmo",
    # packages=setuptools.find_packages(
    #     include=[r"\pyemmo*"]
    #     # exclude=[r"\tests*", r"\workingDirectory*", r"\.vscode*", r"\egg-info*"]
    # ),
    # package data only works with binary packages!!!
    #   see -> https://stackoverflow.com/questions/7522250
    package_data={},
    include_package_data=True,
    # data_files=[
    #     ("", ["pyemmo/script/default_color_dict.json"]),
    #     (
    #         "",
    #         [
    #             "pyemmo/script/material/Material_new.db",
    #             "pyemmo/script/material/Material_old.db",
    #         ],
    #     ),
    # ],
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License ::Other/Proprietary License",
    #     "Operating System :: OS Independent",
    # ],
    # python_requires=PYTHON_REQUIRES,
    install_requires=install_requires,
)
