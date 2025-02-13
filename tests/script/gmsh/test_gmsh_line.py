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
TODO: Update gmsh_line test due to changes in the GmshLine class.

    Returns:
        _type_: _description_
"""
import logging

import gmsh
import numpy as np
import pytest

from pyemmo.script.gmsh.gmsh_line import GmshLine, Line
from pyemmo.script.gmsh.gmsh_point import GmshPoint, Point


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.fixture
def gmsh_points():
    p1 = Point("test point 1", 0.0, 0.0, 0.0, 0.2)
    p2 = Point("test point 2", 1.0, 1.0, 1.0, 0.2)
    gmsh.model.occ.synchronize()
    gmsh_p1 = GmshPoint(tag=p1.id)
    gmsh_p2 = GmshPoint(tag=p2.id)
    return gmsh_p1, gmsh_p2


@pytest.fixture
def gmsh_line(gmsh_points: tuple[GmshPoint, GmshPoint]):
    p1, p2 = gmsh_points
    line = Line(name="test_line", start_point=p1, end_point=p2)
    gmsh.model.occ.synchronize()
    return GmshLine(tag=line.id)


def test_gmsh_line_creation(
    gmsh_line: GmshLine, gmsh_points: tuple[GmshPoint, GmshPoint]
):
    p1, p2 = gmsh_points
    assert gmsh_line.tag == gmsh_line.id
    assert gmsh_line.start_point.isEqual(p1)
    assert gmsh_line.end_point.isEqual(p2)
    assert gmsh_line.name == "test_line"


def test_gmsh_line_tag(gmsh_line: GmshLine):
    new_tag = 10
    gmsh_line.tag = new_tag
    assert gmsh_line.tag == new_tag
    assert gmsh_line.id == new_tag


def test_gmsh_line_start_point(gmsh_line: GmshLine):
    new_start = GmshPoint(tag=3, coords=np.array([0.0, 0.0, 1.0]))
    gmsh_line.start_point = new_start
    assert gmsh_line.start_point == new_start


def test_gmsh_line_end_point(gmsh_line: GmshLine):
    new_end = GmshPoint(tag=4, coords=np.array([1.0, 1.0, 0.0]))
    gmsh_line.end_point = new_end
    assert gmsh_line.end_point == new_end


def test_gmsh_line_str(gmsh_line: GmshLine):
    expected_str = (
        f"GmshLine(tag={gmsh_line.tag}, name=test_line, type={gmsh_line.type}, "
        f"start_point=({gmsh_line.start_point.x:.1e}, {gmsh_line.start_point.y:.1e}, {gmsh_line.start_point.z:.1e}), "
        f"end_point=({gmsh_line.end_point.x:.1e}, {gmsh_line.end_point.y:.1e}, {gmsh_line.end_point.z:.1e}))"
    )
    logging.info(str(gmsh_line))
    assert str(gmsh_line) == expected_str


def test_gmsh_line_reflection_ctor():
    """
    Test to create GmshLine without start_point and end_point.
    """
    gmsh.model.occ.synchronize()
    gmsh_line_tag = 1  # tag has to match with the initialization above
    line = GmshLine(tag=gmsh_line_tag)
    assert isinstance(line.start_point, GmshPoint)
    assert isinstance(line.end_point, GmshPoint)
    assert line.tag == gmsh_line_tag
