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
"""Init for API subpackage"""
from __future__ import annotations

import logging

import gmsh

from .. import logFmt, rootLogger
from ..script.material.material import Material

try:
    air = Material.load("Air")
    air.density = 1.2041
except FileNotFoundError:
    air = Material(
        name="Air",
        conductivity=0,
        relPermeability=1,
        remanence=0,
        density=1.204,
        thermalConductivity=0.0261,
        thermalCapacity=1.005,
    )
air.name = "PYEMMO_AIR"


logger = rootLogger  # test to get script.py log in local model log file
# logger = logging.getLogger("pyemmo.api.json")  # init module logger
ch = logging.StreamHandler()
ch.setFormatter(logFmt)
logger.addHandler(ch)

if not gmsh.is_initialized():
    gmsh.initialize()
    if logging.getLogger().level < logging.DEBUG:
        # use fine resolution for arcs in debugging
        gmsh.option.setNumber("Geometry.NumSubEdges", 360)
