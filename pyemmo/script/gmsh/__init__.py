#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
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
This module inits the gmsh subpackage of PyEMMO.

The module is part of the PyEMMO project, developed by TTZ-EMO at the Technical
University of Applied Sciences Würzburg-Schweinfurt.

Author:
    Max Schuler
"""
from typing import Literal, Tuple

DimTag = Tuple[Literal[0, 1, 2], int]
SurfDimTag = Tuple[Literal[2], int]
