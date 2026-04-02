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

import gmsh
import numpy as np
import pytest

from pyemmo.script.gmsh.gmsh_arc import GmshArc
from pyemmo.script.gmsh.gmsh_line import GmshLine, GmshPoint
from pyemmo.script.gmsh.gmsh_surface import GmshSurface
from pyemmo.script.gmsh.utils import (  # is_straigt
    create_disk,
    filter_curves_on_radius,
    filter_lines_at_angle,
    get_dim_tags,
    get_max_radius,
    get_min_radius,
    get_point_tags,
)
from pyemmo.script.physicals.physical_element import PhysicalElement

from .test_gmsh_surface import add_circle


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.fixture(scope="function", autouse=True)
def add_new_model():
    """Create a new gmsh model every time a test function is called.
    This is necessary since the parameters (like mesh size) might change during
    execution. Even tough a new surface is create by the a fixture every time a new
    test is called, by synchronizing the model, changes in a old geometry might be
    transfered to the new one. E.g. If the mesh size of a point of a surface is changed
    in one test, this mesh size might be transfered to the new surface if its in the
    same model.
    """
    # we need to create a new model for each test!
    gmsh.model.add("test_model")


def test_get_dim_tags():
    """Test the get_dim_tags function"""
    # create gmsh line with tag 1 (dim = 1)
    line = GmshLine.from_points(
        start_point=GmshPoint.from_coordinates(coords=(0, 0)),
        end_point=GmshPoint.from_coordinates(coords=(0, 1)),
    )
    # create gmsh surface with tag 2 (dim = 2)
    gmsh.model.occ.add_rectangle(0, 0, 0, 1, 0.5, tag=2)
    surface = GmshSurface(tag=2)
    # create physical element with line tag 3 (dim = 1)
    physical_line_tag = gmsh.model.occ.get_entities(1)[2][1]
    physical_element = PhysicalElement(
        name="Physical Line", geo_list=[GmshLine(tag=abs(physical_line_tag))]
    )
    # create a list of geometries that includes the line, surface, and physical element
    geo_list = [line, surface, physical_element]

    result = get_dim_tags(geo_list)

    assert result == [
        (line.dim, line.id),
        (surface.dim, surface.id),
        (1, physical_line_tag),
    ]


def test_get_point_tags():
    """Test the get_point_tags function"""
    surf = GmshSurface(tag=gmsh.model.occ.addRectangle(0, 0, 0, 1, 0.5))
    line = GmshLine(
        tag=gmsh.model.occ.addLine(
            gmsh.model.occ.addPoint(2, 0, 0), gmsh.model.occ.addPoint(2, 1, 0)
        )
    )
    point = GmshPoint.from_coordinates(coords=(3, 1))
    dim_tags = [(0, point.id), (2, surf.id), (1, line.id)]
    result = get_point_tags(dim_tags)

    assert result == [1, 2, 3, 4, 5, 6, 7]


def test_get_max_radius():
    """Test the get_max_radius function"""
    dx = 1.0
    dy = 0.5
    surf = GmshSurface(tag=gmsh.model.occ.addRectangle(0, 0, 0, dx, dy))

    result = get_max_radius([(2, surf.id)])

    assert result == np.sqrt(dx**2 + dy**2)


def test_get_min_radius():
    """Test the get_min_radius function"""
    dx = 1.0
    dy = 0.5
    surf = GmshSurface(tag=gmsh.model.occ.addRectangle(dx, dy, 0, dx, dy))

    result = get_min_radius([(2, surf.id)])

    assert result == np.sqrt(dx**2 + dy**2)


def test_filter_curves_on_radius():
    """Test the filter_curves_on_radius function"""
    radius = 1.0
    gmsh_circle = add_circle(
        center=GmshPoint.from_coordinates(coords=(0, 0)), radius=radius
    )

    result = filter_curves_on_radius(gmsh_circle.curve, radius=radius)

    assert len(result) == 4
    assert result == gmsh_circle.curve


def test_filter_lines_at_angle():
    """Test the filter_lines_at_angle function"""
    # Create a line with a 45° angle
    lines = [
        GmshLine.from_points(
            start_point=GmshPoint.from_coordinates(coords=(0, 0)),
            end_point=GmshPoint.from_coordinates(coords=(1, 1)),
        )
    ]
    # Create another line with a 45° angle without origin
    lines.append(
        GmshLine.from_points(
            start_point=GmshPoint.from_coordinates(coords=(0.5, 0.5)),
            end_point=GmshPoint.from_coordinates(coords=(1.5, 1.5)),
        )
    )

    # Create a line with a 90° angle
    lines.append(
        GmshLine.from_points(
            start_point=GmshPoint.from_coordinates(coords=(0, 0)),
            end_point=GmshPoint.from_coordinates(coords=(0, 1)),
        )
    )

    # Create a second line at a 0° angle
    lines.append(
        GmshLine.from_points(
            start_point=GmshPoint.from_coordinates(coords=(0, 0)),
            end_point=GmshPoint.from_coordinates(coords=(1, 0)),
        )
    )

    # Create a second line at a 180° angle
    lines.append(
        GmshLine.from_points(
            start_point=GmshPoint.from_coordinates(coords=(0, 0)),
            end_point=GmshPoint.from_coordinates(coords=(-1, 0)),
        )
    )

    # Filter lines at an angle of 45 degrees
    result = filter_lines_at_angle(lines, angle=np.pi / 4)

    assert len(result) == 2
    assert result[0] == lines[0]  # Should only return the first line
    assert result[1] == lines[1]  # Should only return the first line

    # filter lines at 90 deg
    result = filter_lines_at_angle(lines, angle=np.pi / 2)
    assert len(result) == 1
    assert result[0] == lines[2]

    # filter lines at 0 deg
    result = filter_lines_at_angle(lines, angle=0)
    assert len(result) == 1
    assert result[0] == lines[3]

    # filter lines at 180 deg
    result = filter_lines_at_angle(lines, angle=np.pi)
    assert len(result) == 1
    assert result[0] == lines[4]


def test_create_disk():
    radius = 0.2
    contour = create_disk(radius)  # ceate circle at origin
    assert len(contour) == 4
    assert all(isinstance(line, GmshArc) for line in contour)
    assert all(arc.radius == radius for arc in contour)
