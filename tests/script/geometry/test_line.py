import logging
from math import cos, radians, sin

import gmsh

from pyemmo.script.geometry.line import Line, Point


class TestLine:

    def setup_method(self):
        logging.info("Setup... Initializing gmsh api")
        gmsh.initialize()
        gmsh.model.add("test PyEMMO Line class")

        self.points: list[Point] = []
        for i, angle in enumerate(range(0, 360, 45)):
            self.points.append(
                Point(f"P{i}", cos(radians(angle)), sin(radians(angle)), 0, 1)
            )

    def test_init(self):
        sp = self.points[0]
        ep = self.points[1]
        line = Line("Test init line", sp, ep)
        assert line.name == "Test init line"
        assert line.startPoint == sp
        assert line.endPoint == ep
        assert line.id == 1
        assert line.startPoint.id == 1
        assert line.endPoint.id == 2
        # gmsh.model.occ.synchronize()
        # gmsh.fltk.run()

    def test_duplicate(self):
        """Test the duplication of a line segment"""
        sp = self.points[2]
        ep = self.points[3]
        line = Line("Original", sp, ep)
        dup_line = line.duplicate()
        assert dup_line.name == "Original_dup"
        assert line.arePointsEqual(dup_line)
        assert line.id == 1
        assert line.startPoint.id == 3
        assert line.endPoint.id == 4
        assert dup_line.id == 2
        assert dup_line.startPoint.id == 9
        assert dup_line.endPoint.id == 10

    def test_combine(self):
        """Test the combine function and the gmsh representation"""
        center_point = Point("Center", 0, 0, 0, 1)
        line_1 = Line("First line", self.points[0], center_point)
        line_2 = Line("Second line", center_point, self.points[4])
        combined_line = line_1.combine(line_2)
        assert combined_line.id == 3
        assert combined_line.name == f"combinedLine_{line_1.name}_{line_2.name}"
        assert combined_line.startPoint.isEqual(self.points[0])
        assert combined_line.endPoint.isEqual(self.points[4])

    # TODO: Add tests for the following methods:
    #   Line.complex
    #   Line.getPointDist
    #   Line.middlePoint
    #   Line.rotateZ

    def teardown_method(self):
        logging.info("Teardown")
        gmsh.finalize()
