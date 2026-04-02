#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
Overview
========
This subpackage contains the software for the two PyEMMO interfaces (api's):

- :mod:`~pyemmo.api.json`
- :mod:`~pyemmo.api.pyleecan`

The :mod:`~pyemmo.api.json` interface is a general purpose interface to create ONELAB models through PyEMMO.
Therefore it provides a external interface via json formatted input files and can be run through the command line.

The :mod:`~pyemmo.api.pyleecan` api is a addon that allows to create ONELAB models from `PYLEECAN <https://pyleecan.org/>`_ machines.
PYLEECAN is a powerful open-source software for the design and analysis of electrical machines.
It provides various parameterized rotor and stator geometries and a graphical user interface to create and edit machine designs.
The :mod:`~pyemmo.api.pyleecan` api translates PYLEECAN machine objects into the geometry and material definitions required by the json api, which then creates the ONELAB model files for simulation.

Furthermore, the :mod:`~pyemmo.api` package holds the definition for the class :class:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface`, which is a :class:`~pyemmo.script.gmsh.gmsh_segment_surface.GmshSegmentSurface` with additional attributes :attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id` and :attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.material`.
"""
from __future__ import annotations

import logging

import gmsh

from ..script.material.material import Material

logger = logging.getLogger(__name__)

try:
    air = Material.load("Air")
    """Default air material to be used in pyemmo api.

    :meta private:
    """
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

if not gmsh.is_initialized():
    gmsh.initialize()
    if logger.getEffectiveLevel() < logging.DEBUG:
        # use fine resolution for arcs in debugging
        gmsh.option.setNumber("Geometry.NumSubEdges", 360)
