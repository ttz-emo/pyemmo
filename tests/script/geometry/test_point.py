import gmsh
import pytest

from pyemmo.script.geometry.point import Point

init_cases = [("Point 1", 0, 1, 0, 1), ("Point 2", 1, 0, 0, 1)]


class TestLine:

    # @pytest.mark.parametrize("name, sp, ep", init_cases)
    def setup_method(self):
        gmsh.initialize()
        gmsh.model.add("test PyEMMO Line class")
        # self.line = Line(name=name, startPoint=sp, endPoint=ep)

    def teardown_method(self):
        gmsh.finalize()

    @pytest.mark.parametrize("name, x,  y, z, ml", init_cases)
    def test_init(self, name, x, y, z, ml):
        point = Point(name, x, y, z, ml)
        assert point.name == name
        assert point.coordinate == (x, y, z)
        assert point.id == 1
        assert gmsh.model.get_entity_name(dim=0, tag=1) == name

    # TODO: Add test for Point methods:
    #   Point.calcDist
    #   Point.coordinate
    #   Point.duplicate
    #   Point.getAngleToX
    #   Point.isEqual
    #   Point.radius
