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
import numpy as np
import pytest

from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.segment_surface import SegmentSurface

from .test_surface import add_circle


class TestSegmentSurface:

    def setup_method(self):
        pass

    @pytest.fixture
    def test_surface(self):
        """Default circular test segment (cylinder segment)"""
        center_point = Point("Center point", 0, 0, 0)
        nbr_segments = 8
        angle = 2 * np.pi / nbr_segments
        radius_inner = 1.0
        thickness = 0.3
        radius_outer = radius_inner + thickness
        points: list[Point] = [
            Point("P1", radius_inner, 0, 0),
            Point("P2", radius_outer, 0, 0),
            Point("P3", radius_outer * np.cos(angle), radius_outer * np.sin(angle), 0),
            Point("P4", radius_inner * np.cos(angle), radius_inner * np.sin(angle), 0),
        ]

        lines = [
            Line("L1", points[0], points[1]),
            CircleArc("Outer curve", points[1], center_point, points[2]),
            Line("L2", points[2], points[3]),
            CircleArc("Inner curve", points[3], center_point, points[0]),
        ]
        return SegmentSurface("Test segment surface", lines, nbr_segments=8)

    def test_init(self, test_surface: SegmentSurface):
        """Test the init of Surface"""
        assert len(test_surface.curve) == 4
        assert test_surface.name == "Test segment surface"
        assert test_surface.nbr_segments == 8
        assert test_surface.segment_nbr == 0
        assert test_surface.angle == 2 * np.pi / test_surface.nbr_segments

    # def test_translate(self, test_surface: Surface):
    #     """Test translate() method"""
    #     test_surface.translate(1.1, 0, 0)  # translate surf into x by 1.1
    #     # TODO: Update expected coorinates
    #     exspected_coords = [(1.1, 0, 0), (2.1, 0, 0), (2.1, 1.0, 0), (1.1, 1.0, 0)]
    #     for coords in exspected_coords:
    #         assert any(coords == point.coordinate for point in test_surface.points)

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

    def test_segment_cutOut(self, test_surface: SegmentSurface):
        """Test a two layer subtraction where the tool of the main surface has a tool
        aswell"""
        center = Point(
            "point in center of test_surface",
            1.15 * np.cos(2 * np.pi / test_surface.nbr_segments / 2),
            1.15 * np.sin(2 * np.pi / test_surface.nbr_segments / 2),
            0,
        )
        # create a circle with the same number of segments as the test surface
        center_circle = add_circle(center, radius=0.05)
        center_circle = SegmentSurface(
            "center circle", center_circle.curve, nbr_segments=8
        )
        test_surface.cutOut(center_circle)  # FIRST LAYER CUT
        assert test_surface.tools == [center_circle]  # check if the tool is set
        assert test_surface.nbr_segments == 8
        assert center_circle.nbr_segments == 8

        # create another circle with with double the number of segments
        center2 = center.duplicate("center2")  # duplicate center point
        # rotate center point -1/4 of the segment angle
        center2.rotateZ(
            Point("global center", 0, 0, 0), -2 * np.pi / test_surface.nbr_segments / 4
        )
        double_circle = add_circle(center2, radius=0.01)
        double_circle = SegmentSurface(
            "double circle", double_circle.curve, nbr_segments=16
        )
        # cut out the double circle from the test surface
        test_surface.cutOut(double_circle)
        assert len(test_surface.tools) == 3  # check that an extra tool is added
        assert test_surface.nbr_segments == 8

    def test_duplicate(self, test_surface: SegmentSurface):
        """Test the duplicate method"""
        # Duplicate the test surface
        duplicated_surface = test_surface.duplicate("Duplicated surface")
        assert duplicated_surface.name == "Duplicated surface"
        assert len(duplicated_surface.curve) == 4
        assert len(duplicated_surface.points) == 4
        assert duplicated_surface.nbr_segments == 8
        assert duplicated_surface.segment_nbr == 0

    def test_plot_noSym(self, test_surface: SegmentSurface):
        """Test the plot method"""
        # plot the surface without symmetry
        figure = test_surface.plot(tag=True, symmetry=None)

    def test_plot_fullSym(self, test_surface: SegmentSurface):
        """Test the plot method"""
        # plot surface with symmetry to make sure the whole surface is plotted
        figure = test_surface.plot(symmetry=1)

    def test_plot_wrongSym(self, test_surface: SegmentSurface):
        """Test the plot method"""
        with pytest.raises(ValueError):
            test_surface.plot(symmetry=3)  # invalid symmetry value

    def teardown_method(self):
        pass
