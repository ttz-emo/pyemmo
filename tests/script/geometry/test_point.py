#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of
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

import numpy as np
import pytest

from pyemmo.script.geometry.point import Point

init_cases = [("Point 1", 0, 1, 0), ("Point 2", 1, 0, 0)]


class TestPoint:

    # @pytest.mark.parametrize("name, sp, ep", init_cases)
    def setup_method(self):
        pass
        # self.line = Line(name=name, startPoint=sp, endPoint=ep)

    def teardown_method(self):
        pass

    @pytest.mark.parametrize("name, x,  y, z", init_cases)
    def test_init(self, name, x, y, z):
        point = Point(name, x, y, z)
        assert point.name == name
        assert point.coordinate == (x, y, z)
        assert point.x == x
        assert point.y == y
        assert point.z == z

    @pytest.mark.parametrize(
        "new_x", [0, 1, -1, pytest.param("a", marks=pytest.mark.xfail)]
    )
    def test_reset_x(self, new_x):
        point = Point("test point", 0, 0, 0)
        point.x = new_x
        assert point.coordinate[0] == new_x
        assert point.x == new_x

    @pytest.mark.parametrize(
        "point, expected_angle",
        [
            (Point("test", 0, 0, 0), 0.0),
            (Point("test", 1, 1, 0), np.radians(45)),
            (Point("test", -1, 1, 0), np.radians(135)),
            (Point("test", -1, 0, 0), np.radians(180)),
            (Point("test", 0, -1, 0), np.radians(270)),
        ],
    )
    def test_get_angle_to_x(self, point: Point, expected_angle):
        angle_to_x = point.getAngleToX()
        assert angle_to_x == expected_angle

    @pytest.mark.parametrize(
        "point, expected_angle",
        [
            (Point("test", 0, 0, 0), 0.0),
            (Point("test", 1, 1, 0), 45),
            (Point("test", -1, 1, 0), 135),
            (Point("test", -1, 0, 0), 180),
            (Point("test", 0, -1, 0), 270),
        ],
    )
    def test_get_angle_to_x_deg(self, point: Point, expected_angle):
        angle_to_x = point.getAngleToX(flag_deg=True)
        assert angle_to_x == expected_angle

    @pytest.mark.parametrize(
        "points",
        [
            (Point("test", 0, 0, 0), Point("test", 0, 0, 0)),
            (Point("", 10, 0, 0), Point("", 10, 0, 0)),
            pytest.param(
                (Point("name", 10, -4, 8), Point("other name", 10, -4, 8)),
                marks=pytest.mark.xfail(reason="fails because of different name"),
            ),
            pytest.param(
                (Point("name", 0, 0, 0), Point("name", 1, 1, 1)),
                marks=pytest.mark.xfail(
                    reason="fails because of different coordinates"
                ),
            ),
        ],
    )
    def test_equal(self, points: tuple[Point, Point]):
        """Test __eq__ method"""
        assert points[0] == points[1]

    @pytest.mark.parametrize(
        "points",
        [
            (Point("test", 0, 0, 0), Point("test", 0, 0, 0)),
            (Point("", 10, 0, 0), Point("", 10, 0, 0)),
            (Point("name", 10, -4, 8), Point("other name", 10, -4, 8)),
            pytest.param(
                (Point("name", 0, 0, 0), Point("name", 1, 1, 1)),
                marks=pytest.mark.xfail(
                    reason="fails because of different coordinates"
                ),
            ),
        ],
    )
    def test_is_equal_coords(self, points: tuple[Point, Point]):
        """Test isEqual() method"""
        assert points[0].isEqual(points[1])

    # TODO: Add test for Point methods:
    #   Point.calcDist
    #   Point.coordinate
    #   Point.duplicate
    #   Point.getAngleToX
    #   Point.isEqual
    #   Point.radius
