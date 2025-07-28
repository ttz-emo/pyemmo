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
# import logging
from __future__ import annotations

from math import isclose, pi, radians, sqrt

import pytest

from pyemmo.script.geometry.circleArc import CircleArc, Point


@pytest.fixture(scope="module")
def arc1() -> CircleArc:
    """Circle arc with start point on x-axis (1,0,0), center point (0,0,0) and end point
    on y axis (0,1,0)"""
    return CircleArc(
        "arc1", Point("P0", 1, 0, 0), Point("P center", 0, 0, 0), Point("P2", 0, 1, 0)
    )


def test_init():
    start_point = Point("P0", 1, 0, 0)
    center_point = Point("P center", 0, 0, 0)
    end_point = Point("P2", 0, 1, 0)
    arc = CircleArc("arc1", start_point, center_point, end_point)
    assert arc.name == "arc1"
    assert arc.start_point == start_point
    assert arc.center == center_point
    assert arc.end_point == end_point
    assert arc.radius == 1


@pytest.mark.parametrize(
    "start_point, center_point, end_point, expected_length",
    [
        (
            Point("P0", 1, 0, 0),
            Point("P center", 0, 0, 0),
            Point("P2", 0, 1, 0),
            pi / 2,
        ),
        (
            Point("P0", 1, 0, 0),
            Point("P center", 0, 0, 0),
            Point("P3", 0, -1, 0),
            pi / 2,
        ),
        (
            Point("P0", 1, 1, 0),
            Point("P center", 0, 0, 0),
            Point("P4", 0, 1, 1),
            sqrt(2) * pi / 4,
        ),
        (
            Point("P0", -1, 1, 0),
            Point("P center", 0, 0, 0),
            Point("P5", -1, -1, 0),
            sqrt(2) * pi / 2,
        ),
        (
            Point("P0", 1, 1, 0),
            Point("P center", 0, 0, 0),
            Point("P6", -1, -1, 0),
            sqrt(2) * pi,
        ),
    ],
)
def test_length(start_point, center_point, end_point, expected_length):
    """Test the length of a circle arc"""
    arc = CircleArc("Test length arc", start_point, center_point, end_point)
    if not isclose(arc.length, expected_length, abs_tol=radians(0.01)):
        # show assert error in pytest fail
        assert arc.length == expected_length


# TODO: Add tests for the following methods:
#   ...
