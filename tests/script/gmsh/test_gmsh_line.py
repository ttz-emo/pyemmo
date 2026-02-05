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
"""Module for GmshLine class and its reflection GmshPoint."""
from __future__ import annotations

import logging

import gmsh
import numpy as np
import pytest

from pyemmo.definitions import DEFAULT_GEO_TOL as TOLERANCE
from pyemmo.script.gmsh.gmsh_line import GmshLine
from pyemmo.script.gmsh.gmsh_point import GmshPoint


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.fixture
def gmsh_points():
    """Gmsh Points for testing GmshLine class"""
    gmsh_p1 = GmshPoint.from_coordinates(
        name="test point 1", coords=[0.0, 0.0, 0.0], meshLength=0.2
    )
    gmsh_p2 = GmshPoint.from_coordinates(
        name="test point 2", coords=[1.0, 1.0, 0.0], meshLength=0.2
    )
    return gmsh_p1, gmsh_p2


@pytest.fixture
def gmsh_line(gmsh_points: tuple[GmshPoint, GmshPoint]):
    """Create a GmshLine with start_point and end_point."""
    p1, p2 = gmsh_points
    line = GmshLine.from_points(start_point=p1, end_point=p2, name="test_line")
    # gmsh.model.occ.synchronize()
    return line


def test_gmsh_line_init_points(
    gmsh_line: GmshLine, gmsh_points: tuple[GmshPoint, GmshPoint]
):
    """Test to create GmshLine with start_point and end_point."""
    p1, p2 = gmsh_points
    assert gmsh_line.id == gmsh_line.id
    assert gmsh_line.start_point.isEqual(p1)
    assert gmsh_line.end_point.isEqual(p2)
    assert gmsh_line.name == "test_line"


def test_gmsh_line_init_id():
    """Test to create GmshLine without start_point and end_point."""
    gmsh_line_tag = 1  # tag has to match with the initialization above
    line = GmshLine(tag=gmsh_line_tag)
    assert isinstance(line.start_point, GmshPoint)
    assert isinstance(line.end_point, GmshPoint)
    assert line.id == gmsh_line_tag


def test_gmsh_line_id_setter(gmsh_line: GmshLine):

    new_tag = 10
    gmsh_line.id = new_tag
    assert gmsh_line.id == new_tag


def test_gmsh_line_start_point(gmsh_line: GmshLine):
    new_start = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 1.0]))
    with pytest.raises(AttributeError):
        gmsh_line.start_point = new_start


def test_gmsh_line_end_point(gmsh_line: GmshLine):
    new_end = GmshPoint.from_coordinates(coords=np.array([1.0, 1.0, 0.0]))
    with pytest.raises(AttributeError):
        gmsh_line.end_point = new_end


def test_gmsh_line_str(gmsh_line: GmshLine):
    expected_str = (
        f"GmshLine(name=test_line, id={gmsh_line.id}, "
        f"start_point=({gmsh_line.start_point.x:.1e}, {gmsh_line.start_point.y:.1e}, {gmsh_line.start_point.z:.1e}), "
        f"end_point=({gmsh_line.end_point.x:.1e}, {gmsh_line.end_point.y:.1e}, {gmsh_line.end_point.z:.1e}))"
    )
    assert str(gmsh_line) == expected_str


def test_length(gmsh_line: GmshLine):
    """Test to get the length of a GmshLine."""
    assert np.isclose(gmsh_line.length, np.sqrt(2), atol=TOLERANCE)


def test_switch_points(gmsh_line: GmshLine):
    """Test to switch the start_point and end_point of a GmshLine.
    Fail because the start_point and end_point are read-only properties."""
    with pytest.raises(AttributeError):
        gmsh_line.switchPoints()


def test_translate(gmsh_line: GmshLine):
    """Test to translate a GmshLine"""
    gmsh_line.translate(1, 1, 0)
    assert np.isclose(gmsh_line.start_point.coordinate, (1, 1, 0), atol=TOLERANCE).all()
    assert np.isclose(gmsh_line.end_point.coordinate, (2, 2, 0), atol=TOLERANCE).all()


def test_rotateZ(gmsh_line: GmshLine):
    """Test to rotate a GmshLine around the Z-axis."""
    gmsh_line.rotateZ(angle=np.radians(90))
    assert np.isclose(gmsh_line.start_point.coordinate, (0, 0, 0), atol=TOLERANCE).all()
    assert np.isclose(gmsh_line.end_point.coordinate, (-1, 1, 0), atol=TOLERANCE).all()


def test_duplicate(gmsh_line: GmshLine):
    """Test to duplicate a GmshLine."""
    duplicate = gmsh_line.duplicate()
    assert duplicate.start_point.isEqual(gmsh_line.start_point)
    assert duplicate.end_point.isEqual(gmsh_line.end_point)
    assert duplicate.name == gmsh_line.name + "_dup"
    assert duplicate.id != gmsh_line.id


def test_combine(gmsh_line: GmshLine):
    """Test to combine two GmshLine objects."""
    gmsh_line2 = GmshLine.from_points(
        start_point=GmshPoint.from_coordinates(
            name="test point 3", coords=[1.0, 1.0, 0.0], meshLength=0.2
        ),
        end_point=GmshPoint.from_coordinates(
            name="test point 4", coords=[2.0, 2.0, 0.0], meshLength=0.2
        ),
        name="test_line2",
    )
    combined_line = gmsh_line.combine(gmsh_line2)
    logger = logging.getLogger(__name__)
    logger.debug(f"Combined line: {combined_line}")
    assert isinstance(combined_line, GmshLine)
    assert combined_line.start_point.coordinate in [(0.0, 0.0, 0.0), (2.0, 2.0, 0.0)]
    assert combined_line.end_point.coordinate in [(0.0, 0.0, 0.0), (2.0, 2.0, 0.0)]
