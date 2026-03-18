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
from __future__ import annotations

from os.path import join

from pyemmo.api import air
from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.script.gmsh.gmsh_point import GmshPoint
from tests import TEST_DATA_DIR

from ..script.gmsh.test_gmsh_surface import add_circle as add_gmsh_circle

TEST_API_DATA_DIR = join(TEST_DATA_DIR, "api")


def add_circle(
    center: GmshPoint, radius: float, nbr_segments: int
) -> MachineSegmentSurface:
    """Function to create MachineSegmentSurface circle"""
    circ = add_gmsh_circle(center, radius)
    return MachineSegmentSurface(
        part_id="Circle",
        material=air,
        tag=circ.id,
        name=circ.name,
        nbr_segments=nbr_segments,
    )
