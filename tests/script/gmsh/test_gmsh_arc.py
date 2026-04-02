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
"""Module for testing of class GmshArc."""
from __future__ import annotations

import logging
import math

import gmsh
import numpy as np
import pytest

from pyemmo.definitions import DEFAULT_GEO_TOL as TOLERANCE
from pyemmo.script.gmsh.gmsh_arc import GmshArc
from pyemmo.script.gmsh.gmsh_point import GmshPoint


class TestGmshArc:
    """PyTest class for testing of GmshArc class"""

    def setup_method(self):
        """Setup the Gmsh model for the tests."""
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")

    def teardown_method(self):
        """Close the Gmsh model after the tests."""
        gmsh.finalize()

    @pytest.fixture
    def gmsh_arc(self):
        """Create a GmshArx with start_point, center and end_point."""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        arc = GmshArc.from_points(
            start_point=start,
            center_point=center,
            end_point=end,
            name="Quarter circle",
        )
        return arc

    def test_gmsh_arc_creation_with_points(self):
        """Test init of gmsh arc with GmshPoint objects"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        arc = GmshArc.from_points(
            start_point=start,
            center_point=center,
            end_point=end,
            name="Quarter circle",
        )

        assert arc.start_point.id == start.id
        assert arc.center.id == center.id
        assert arc.end_point.id == end.id
        assert arc.name == "Quarter circle"
        assert arc.radius == 1.0

    def test_gmsh_arc_creation_with_tag(self):
        """Test init of GmshArc with gmsh curve tag"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        arc_id = gmsh.model.occ.addCircleArc(start.id, center.id, end.id)
        arc_with_tag = GmshArc(tag=arc_id, name="Quarter circle")

        assert arc_with_tag.start_point.id == start.id
        assert arc_with_tag.center.id == center.id
        assert arc_with_tag.end_point.id == end.id
        assert arc_with_tag.name == "Quarter circle"
        assert arc_with_tag.radius == 1.0

    def test_gmsh_arc_invalid_creation(self):
        """Make sure wrong init raises ValueErrors"""
        with pytest.raises(ValueError):
            GmshArc(tag=2)

        with pytest.raises(ValueError):
            GmshArc.from_points(
                start_point=GmshPoint.from_coordinates(
                    coords=np.array([1.0, 0.0, 0.0])
                ),
                center_point=None,
                end_point=None,
            )

    def test_gmsh_arc_properties(self):
        """Test GmshArc Properties give correct values"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        arc = GmshArc.from_points(
            start_point=start,
            center_point=center,
            end_point=end,
            name="Quarter circle",
        )

        assert arc.dim == 1
        assert arc.start_point.id == start.id
        assert arc.end_point.id == end.id
        assert arc.center.id == center.id
        assert arc.name == "Quarter circle"

    def test_gmsh_arc_str(self):
        """Test string output of class GmshArc"""
        center = GmshPoint.from_coordinates(coords=np.array([0.0, 0.0, 0.0]))
        start = GmshPoint.from_coordinates(coords=np.array([1.0, 0.0, 0.0]))
        end = GmshPoint.from_coordinates(coords=np.array([0.0, 1.0, 0.0]))

        arc = GmshArc.from_points(
            start_point=start,
            center_point=center,
            end_point=end,
            name="Quarter circle",
        )

        expected_str = (
            f"GmshArc(name=Quarter circle, id={arc.id}, "
            f"start_point=({start.coordinate[0]}, {start.coordinate[1]}, {start.coordinate[2]}), "
            f"end_point=({end.coordinate[0]}, {end.coordinate[1]}, {end.coordinate[2]}))"
        )
        assert str(arc) == expected_str

    def test_length(self, gmsh_arc: GmshArc):
        """Test length method of class GmshArc"""
        assert np.isclose(gmsh_arc.length, math.pi / 2, atol=TOLERANCE)

    def test_duplicate(self, gmsh_arc: GmshArc):
        """Test duplicate method of class GmshGeometry"""
        dup_arc = gmsh_arc.duplicate()

        assert dup_arc.start_point.isEqual(gmsh_arc.start_point)
        assert dup_arc.end_point.isEqual(gmsh_arc.end_point)
        assert dup_arc.center.isEqual(gmsh_arc.center)
        assert dup_arc.name == gmsh_arc.name + "_dup"
        assert dup_arc.id != gmsh_arc.id

    def test_get_angles_to_X(self, gmsh_arc: GmshArc):
        """Test get_angles_to_X method of class CircleArc"""
        start_angle, end_angle = gmsh_arc.getAnglesToX()
        assert start_angle == 0.0
        assert end_angle == math.pi / 2

        start_angle, end_angle = gmsh_arc.getAnglesToX(inDeg=True)
        assert start_angle == 0.0
        assert end_angle == 90

    def test_get_angle(self, gmsh_arc: GmshArc):
        """Test get_angle method of class CircleArc"""
        arc_angle = gmsh_arc.getAngle(inDeg=False)
        assert arc_angle == math.pi / 2

        arc_angle = gmsh_arc.getAngle(inDeg=True)
        assert arc_angle == 90

    def test_plot(self, gmsh_arc: GmshArc):
        """Make sure plot does not raise an error"""
        gmsh_arc.plot()

    def test_combine(self, gmsh_arc: GmshArc):
        """Test combine method of abstract class GmshGeometry"""
        logger = logging.getLogger(__name__)
        add_arc = gmsh_arc.duplicate()
        add_arc.rotateZ(angle=gmsh_arc.getAngle())
        # We need to call sync() here because otherwise the rotation will only be available
        # in the OCC representation and not in the GMSH representation.
        gmsh.model.occ.synchronize()
        combined_arc: GmshArc = gmsh_arc.combine(add_arc)
        # after fuse we need to call sync() again to make the changes available for the
        # python api to check for the properties of the arc
        gmsh.model.occ.synchronize()
        logger.debug(f"Combined arc: {combined_arc}")

        assert combined_arc.center.coordinate == (0.0, 0.0, 0.0)
        assert any(
            all(np.isclose(combined_arc.start_point.coordinate, coords, atol=TOLERANCE))
            for coords in [(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
        )
        assert any(
            all(np.isclose(combined_arc.end_point.coordinate, coords, atol=TOLERANCE))
            for coords in [(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
        )
        assert combined_arc.dim == 1
        assert np.isclose(abs(combined_arc.getAngle(inDeg=True)), 180, atol=TOLERANCE)
        assert np.isclose(combined_arc.radius, 1, atol=TOLERANCE)
        assert np.isclose(combined_arc.length, math.pi, atol=TOLERANCE)
