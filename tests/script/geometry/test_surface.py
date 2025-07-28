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
from __future__ import annotations

import pytest

from pyemmo.script.geometry.surface import CircleArc, Line, Point, Surface


def add_circle(center: Point, radius: float):
    """Create a test Circle"""
    points: list[Point] = []
    for i, xy in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
        x, y, _ = center.coordinate
        dx = x
        dy = y
        points.append(Point(f"P{i}", xy[0] * radius + dx, xy[1] * radius + dy, 0))
    lines: list[CircleArc] = []
    for i, point in enumerate(points):
        lines.append(CircleArc(f"L{i}", points[i - 1], center, point))
    return Surface(f"Circle {radius=:.1f}", lines)


class TestSurface:

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

    def test_init(self, test_surface: Surface):
        """Test the init of Surface"""
        assert len(test_surface.curve) == 4
        assert test_surface.name == "Test surface"
        # TODO: Add more assert statements

    def test_translate(self, test_surface: Surface):
        """Test translate() method"""
        test_surface.translate(1.1, 0, 0)  # translate surf into x by 1.1
        exspected_coords = [(1.1, 0, 0), (2.1, 0, 0), (2.1, 1.0, 0), (1.1, 1.0, 0)]
        for coords in exspected_coords:
            assert any(coords == point.coordinate for point in test_surface.points)

    # TODO: Add tests for the following methods:
    # Surface.allPoints
    # Surface.calcCOG
    # Surface.combine
    # Surface.curve
    # Surface.cutOut
    # Surface.delete
    # Surface.duplicate
    # Surface.points
    # Surface.recombineCurves
    # Surface.rotateZ

    def test_2_layer_subtract(self, test_surface: Surface):
        """Test a two layer subtraction where the tool of the main surface has a tool
        aswell"""
        center = Point("Center", 0.5, 0.5, 0)
        circ_big = add_circle(center, radius=0.4)
        circ_small = add_circle(center, radius=0.15)
        circ_big.cutOut(circ_small)  # SECOND LAYER CUT
        test_surface.cutOut(circ_big)  # FIRST LAYER CUT
        # TODO: Add assert statements

    def teardown_method(self):
        pass
