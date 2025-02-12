import gmsh
import numpy as np
import pytest

from pyemmo.script.gmsh.gmsh_point import GmshPoint

init_cases = [
    ("Point 1", np.array([0, 1, 0]), 1),
    ("Point 2", np.array([1, 0, 0]), 1e-3),
]


class TestGmshPoint:

    # @pytest.mark.parametrize("name, sp, ep", init_cases)
    def setup_method(self):
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")
        # self.line = Line(name=name, startPoint=sp, endPoint=ep)

    def teardown_method(self):
        gmsh.finalize()

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_coords3D(self, name, coords, ml):
        point = GmshPoint(name=name, coords=coords, meshLength=ml)
        gmsh.model.occ.synchronize()
        assert point.coordinate == (coords[0], coords[1], coords[2])
        assert point.meshLength == ml
        assert (
            str(point)
            == f"GmshPoint(tag={point.id}, coords=({float(coords[0])}, {float(coords[1])}, {float(coords[2])}))"
        )

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_coords2D(self, name, coords, ml):
        point = GmshPoint(name=name, coords=coords[0:2], meshLength=ml)
        gmsh.model.occ.synchronize()
        assert point.coordinate == (coords[0], coords[1], coords[2])
        assert point.meshLength == ml
        assert (
            str(point)
            == f"GmshPoint(tag={point.id}, coords=({float(coords[0])}, {float(coords[1])}, {float(coords[2])}))"
        )

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_id(self, name, coords, ml):
        point_tag = gmsh.model.occ.addPoint(coords[0], coords[1], coords[2], ml)
        gmsh.model.setEntityName(0, point_tag, name)
        gmsh.model.occ.synchronize()
        point = GmshPoint(point_tag)
        assert point.id == point_tag
        assert point.coordinate == (coords[0], coords[1], coords[2])
        assert point.meshLength == ml
        assert point.name == name

    @pytest.mark.parametrize(
        "tag, name, coords, ml",
        [
            pytest.param(
                1,
                "test",
                np.array([0, 0]),
                1,
                marks=pytest.mark.xfail(reason="tag and coords given"),
            ),
            pytest.param(
                -1,
                "test",
                np.array([0, 0]),
                "a",
                marks=pytest.mark.xfail(reason="mesh length not number"),
            ),
            pytest.param(
                -1,
                "test",
                np.array([0, 0]),
                0,
                marks=pytest.mark.xfail(reason="mesh length zero"),
            ),
            pytest.param(
                1,
                "test",
                np.array([]),
                1,
                marks=pytest.mark.xfail(reason="point does not exist"),
            ),
        ],
    )
    def test_init_fail(self, tag, name, coords, ml):
        GmshPoint(tag, name, coords, ml)

    def test_set_id(self):
        point = GmshPoint(-1, "test", np.array([0, 0, 0]), 1)
        point.id = 10
        assert point.id == 10

    def test_set_name(self):
        point = GmshPoint(-1, "test", np.array([0, 0, 0]), 1)
        point.name = "different name"
        assert point.name == "different name"

    def test_set_mesh_length(self):
        point = GmshPoint(-1, "test", np.array([0, 0, 0]), 1)
        point.meshLength = 0.1
        assert point.meshLength == 0.1

    @pytest.mark.parametrize(
        "new_coords",
        [
            pytest.param(
                np.array([0, 1, 0]),
                marks=pytest.mark.xfail(reason="coords is read-only"),
            )
        ],
    )
    def test_reset_coords(self, new_coords):
        point = GmshPoint(-1, "test point", (0, 0, 0), 1)
        point.coordinate = new_coords  # this raises attribute error

    @pytest.mark.parametrize(
        "new_x", [pytest.param(1, marks=pytest.mark.xfail(reason="x is read-only"))]
    )
    def test_reset_x(self, new_x):
        point = GmshPoint(-1, "test point", (0, 0, 0), 1)
        point.x = new_x
        assert point.coordinate[0] == new_x
        assert point.x == new_x

    @pytest.mark.parametrize(
        "coords, expected_angle",
        [
            (np.array([0, 0, 0]), 0.0),
            (np.array([1, 1, 0]), np.radians(45)),
            (np.array([-1, 1, 0]), np.radians(135)),
            (np.array([-1, 0, 0]), np.radians(180)),
            (np.array([0, -1, 0]), np.radians(270)),
        ],
    )
    def test_get_angle_to_x(self, coords: np.ndarray, expected_angle):
        point = GmshPoint(-1, "test", coords, 1)
        angle_to_x = point.getAngleToX()
        assert angle_to_x == expected_angle

    @pytest.mark.parametrize(
        "coords, expected_angle",
        [
            (np.array([0, 0, 0]), 0.0),
            (np.array([1, 1, 0]), 45),
            (np.array([-1, 1, 0]), 135),
            (np.array([-1, 0, 0]), 180),
            (np.array([0, -1, 0]), 270),
        ],
    )
    def test_get_angle_to_x_deg(self, coords: np.ndarray, expected_angle):
        point = GmshPoint(-1, "test", coords, 1)
        angle_to_x = point.getAngleToX(flag_deg=True)
        assert angle_to_x == expected_angle

    # TODO: Add test for Point methods:
    #   Point.translate
    #   Point.rotate
    #   Point.calcDist
    #   Point.coordinate
    #   Point.duplicate
    #   Point.isEqual
    #   Point.radius
