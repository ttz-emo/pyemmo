import logging

import gmsh
import pytest

from pyemmo.script.geometry.surface import Line, Point, Surface


class TestSurface:

    def setup_method(self):
        logging.debug("Setup... Initializing gmsh api")
        gmsh.initialize()
        gmsh.model.add("test PyEMMO Line class")

    @pytest.fixture
    def test_surface(self):
        """Default test Surface"""
        points: list[Point] = []
        for i, xy in enumerate([(0, 0), (0, 1), (1, 1), (1, 0)]):
            points.append(Point(f"P{i}", xy[0], xy[1], 0, 1))
        lines: list[Line] = []
        for i, point in enumerate(points):
            lines.append(Line(f"L{i}", points[i - 1], point))
        return Surface("Test surface", lines)

    def test_init(self, test_surface: Surface):
        """Test the init of Surface"""
        assert test_surface.id == 1
        assert len(test_surface.curve) == 4
        assert test_surface.name == "Test surface"

    def test_translate(self, test_surface: Surface):
        """Test translate() method"""
        test_surface.translate(1.1, 0, 0)  # translate surf into x by 1.1
        exspected_coords = [(1.1, 0, 0), (2.1, 0, 0), (2.1, 1.0, 0), (1.1, 1.0, 0)]
        for coords in exspected_coords:
            assert any(coords == point.coordinate for point in test_surface.points)
        # gmsh.model.occ.synchronize()
        # gmsh.fltk.run()

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

    def teardown_method(self):
        logging.debug("Teardown")
        gmsh.finalize()
