import gmsh
import numpy as np
import pytest

from pyemmo.script.geometry.point import Point
from pyemmo.script.gmsh.gmsh_point import GmshPoint

init_cases = [("Point 1", 0, 1, 0, 1), ("Point 2", 1, 0, 0, 1)]


class TestGmshPoint:

    # @pytest.mark.parametrize("name, sp, ep", init_cases)
    def setup_method(self):
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")
        # self.line = Line(name=name, startPoint=sp, endPoint=ep)

    def teardown_method(self):
        gmsh.finalize()

    @pytest.mark.parametrize("name, x,  y, z, ml", init_cases)
    def test_init(self, name, x, y, z, ml):
        point = Point(name, x, y, z, ml)
        gmsh.model.occ.synchronize()
        gmsh_point = GmshPoint(point.id)
        assert gmsh_point.tag == point.id
        assert gmsh_point.coordinate == (x, y, z)
        assert gmsh_point.coordinate == point.coordinate
        assert (
            str(gmsh_point)
            == f"GmshPoint(tag={gmsh_point.tag}, coords=({float(x)}, {float(y)}, {float(z)}))"
        )

    @pytest.mark.xfail(reason="gmsh.model.occ.synchronize() not called", strict=True)
    def test_init_fail(self, name, x, y, z, ml):
        point = Point(name, x, y, z, ml)
        gmsh_point = GmshPoint(point.id)

    @pytest.mark.parametrize(
        "new_x", [0, 1, -1, pytest.param("a", marks=pytest.mark.xfail)]
    )
    def test_reset_x(self, new_x):
        point = Point("test point", 0, 0, 0, 1)
        point.x = new_x
        assert point.coordinate[0] == new_x
        assert point.x == new_x

    @pytest.mark.parametrize(
        "point, expected_angle",
        [
            (Point("test", 0, 0, 0, 1), 0.0),
            (Point("test", 1, 1, 0, 1), np.radians(45)),
            (Point("test", -1, 1, 0, 1), np.radians(135)),
            (Point("test", -1, 0, 0, 1), np.radians(180)),
            (Point("test", 0, -1, 0, 1), np.radians(270)),
        ],
    )
    def test_get_angle_to_x(self, point: Point, expected_angle):
        angle_to_x = point.getAngleToX()
        assert angle_to_x == expected_angle

    @pytest.mark.parametrize(
        "point, expected_angle",
        [
            (Point("test", 0, 0, 0, 1), 0.0),
            (Point("test", 1, 1, 0, 1), 45),
            (Point("test", -1, 1, 0, 1), 135),
            (Point("test", -1, 0, 0, 1), 180),
            (Point("test", 0, -1, 0, 1), 270),
        ],
    )
    def test_get_angle_to_x_deg(self, point: Point, expected_angle):
        angle_to_x = point.getAngleToX(flag_deg=True)
        assert angle_to_x == expected_angle

    # TODO: Add test for Point methods:
    #   Point.calcDist
    #   Point.coordinate
    #   Point.duplicate
    #   Point.getAngleToX
    #   Point.isEqual
    #   Point.radius
