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

# %% Add the top folder to the path so the software is recognized without being installed (as a package)
from sys import path
from os.path import abspath, join, dirname

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = (
        "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    )
    # print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
# %% test database
from pyemmo.script.material import materialManagement
from pyemmo.functions import xml2pyemmo
from pyemmo.definitions import ROOT_DIR


dataBaseName = "Material_new.db"

# matArray = xml2pyemmo.getMaterialArray(join(ROOT_DIR, "pyemmo\\script\\material", ))
# %%
for mat in matArray:
    try:
        conductivity = mat["conductivity"]
    except KeyError:
        conductivity = 0

    try:
        relativePermeability = mat["relativePermeability"]
    except KeyError:
        relativePermeability = 0

    try:
        BH = mat["BH"]
    except KeyError:
        BH = None

    # materialManagement.addMaterial(
    #     dataBase, mat["name"], conductivity, relativePermeability, None, BH
    # )
