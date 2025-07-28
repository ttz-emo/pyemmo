#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of
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
"""Module for testing of class GmshSpline."""
from __future__ import annotations

import gmsh
import numpy as np
import pytest

from pyemmo.definitions import DEFAULT_GEO_TOL as TOLERANCE
from pyemmo.script.gmsh.gmsh_point import GmshPoint
from pyemmo.script.gmsh.gmsh_spline import GmshSpline


class TestGmshSpline:
    """PyTest class for testing of GmshSpline class"""

    def setup_method(self):
        """Setup the Gmsh model for the tests."""
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")

    def teardown_method(self):
        """Close the Gmsh model after the tests."""
        gmsh.finalize()

    @pytest.fixture
    def gmsh_spline(self):
        """Create a GmshSpline with start_point, center and end_point."""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        spline = GmshSpline.from_points(
            points=[start, center, end],
            name="Test Spline",
        )
        return spline

    def test_gmsh_spline_creation_with_points(self):
        """Test init of gmsh spline with GmshPoint objects"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        spline = GmshSpline.from_points(
            points=[start, center, end],
            name="Test Spline",
        )

        assert spline.start_point.id == start.id
        # assert spline.control_points[0].id == center.id
        assert spline.end_point.id == end.id
        assert spline.name == "Test Spline"
        assert gmsh.model.getType(1, spline.id) == "Bezier"

    def test_gmsh_spline_creation_with_tag(self):
        """Test init of GmshSpline with gmsh curve tag"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        spline_id = gmsh.model.occ.addSpline([start.id, center.id, end.id])
        spline_with_tag = GmshSpline(tag=spline_id, name="Test Spline")

        assert len(spline_with_tag.points) == 2
        assert spline_with_tag.start_point.id == start.id
        # assert spline_with_tag.control_points[0].id == center.id
        assert spline_with_tag.end_point.id == end.id
        assert spline_with_tag.name == "Test Spline"

    def test_gmsh_spline_invalid_creation(self):
        """Make sure wrong init raises ValueErrors"""
        with pytest.raises(ValueError):
            GmshSpline(tag=2)

        with pytest.raises(TypeError):
            GmshSpline.from_points(points=None)

    def test_gmsh_spline_properties(self):
        """Test GmshSpline Properties give correct values"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        spline = GmshSpline.from_points(
            points=[start, center, end],
            name="Test Spline",
        )

        assert spline.dim == 1
        assert spline.start_point.id == start.id
        assert spline.end_point.id == end.id
        # assert spline.control_points[0].id == center.id
        assert spline.name == "Test Spline"

    def test_gmsh_spline_str(self):
        """Test string output of class GmshSpline"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        spline = GmshSpline.from_points(
            points=[start, center, end],
            name="Test Spline",
        )
        return
        # TODO:
        expected_str = ""
        assert str(spline) == expected_str

    def test_length(self, gmsh_spline: GmshSpline):
        """Test length method of class GmshSpline"""
        expected_length = 1.6232135
        assert np.isclose(gmsh_spline.length, expected_length, atol=TOLERANCE)

    def test_duplicate(self, gmsh_spline: GmshSpline):
        """Test duplicate method of class GmshGeometry"""
        dup_spline: GmshSpline = gmsh_spline.duplicate()

        assert dup_spline.start_point.isEqual(gmsh_spline.start_point)
        assert dup_spline.end_point.isEqual(gmsh_spline.end_point)
        # assert dup_spline.control_points == gmsh_spline.control_points
        assert dup_spline.name == gmsh_spline.name + "_dup"
        assert dup_spline.id != gmsh_spline.id

    def test_plot(self, gmsh_spline: GmshSpline):
        """Make sure plot does not raise an error"""
        gmsh_spline.plot()
