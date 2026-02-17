#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
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
"""Test the class PhysicalElement"""
from __future__ import annotations

import gmsh
import pytest

from pyemmo.api import air
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.gmsh.gmsh_point import GmshPoint
from pyemmo.script.physicals.physicalElement import PhysicalElement

from ..gmsh.test_utils import add_circle


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


class TestSurfacePhysical:

    def setup_method(self):
        pass

    @pytest.fixture
    def test_surface(self):
        """Default test Surface

             |
        (1,0).---------------.(1,1)
             |               |
             |               |
             |               |
             |               |
             |               |
        (0,0).---------------.(0,1)---->
             |

        """
        points: list[Point] = []
        for i, xy in enumerate([(0, 0), (0, 1), (1, 1), (1, 0)]):
            points.append(Point(f"P{i}", xy[0], xy[1], 0))
        lines: list[Line] = []
        for i, point in enumerate(points):
            lines.append(Line(f"L{i}", points[i - 1], point))
        return Surface("Test surface", lines)

    @pytest.mark.xfail(
        reason="PhysicalElement is not meant to be used with non-Gmsh geometries anymore."
        "Physical classes should be moved to gmsh package before adapting tests!"
    )
    def test_init_fails(self, test_surface: Surface):
        """Test the init of Surface"""
        name = "test physical"
        physical = PhysicalElement(name, [test_surface], material=air)
        assert physical.name == name
        assert physical.geo_list == [test_surface]
        assert physical.geoElementType == Surface
        assert physical.material == air

    def test_init(self):
        """Test the init of Surface"""
        test_surface = add_circle(
            GmshPoint.from_coordinates(name="center", coords=[0, 0, 0], meshLength=1.0),
            1.1,
        )
        name = "test physical"
        physical = PhysicalElement(name, [test_surface], material=air)
        assert physical.name == name
        assert physical.geo_list == [test_surface]
        assert physical.geoElementType == Surface
        assert physical.material == air

    def teardown_method(self):
        pass
