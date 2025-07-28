#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
"""Module test_gmsh_point.py for tests of the class GmshPoint."""
from __future__ import annotations

import gmsh
import numpy as np
import pytest

from pyemmo.definitions import DEFAULT_GEO_TOL as TOLERANCE
from pyemmo.script.gmsh.gmsh_point import GmshPoint

init_cases = [
    # name, coords, meshLength
    ("Point 1", np.array([0, 1, 0]), 1),
    ("Point 2", np.array([1, 0, 0]), 1e-3),
    ("Point 3", [0, 0, 1], 1e-3),
    ("Point 4", (1, 1, 0), 1e-3),
]


# pylint: disable=locally-disabled, too-many-public-methods
class TestGmshPoint:
    """Test class for GmshPoint."""

    # @pytest.mark.parametrize("name, sp, ep", init_cases)
    def setup_method(self):
        """Setup the Gmsh model for the tests."""
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")
        # self.line = Line(name=name, startPoint=sp, endPoint=ep)

    def teardown_method(self):
        """Close the Gmsh model after the tests."""
        gmsh.finalize()

    @pytest.fixture(scope="function")
    def gmsh_point(self):
        """Fixture to create a GmshPoint object."""
        point = GmshPoint.from_coordinates(name="test", coords=[0, 0, 0], meshLength=1)
        return point

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_coords3D(self, name, coords, ml):
        """Test the 3D initialization of a GmshPoint object."""
        point = GmshPoint.from_coordinates(name=name, coords=coords, meshLength=ml)
        gmsh.model.occ.synchronize()
        assert point.coordinate == (coords[0], coords[1], coords[2])
        assert point.x == coords[0]
        assert point.y == coords[1]
        assert point.z == coords[2]
        assert point.meshLength == ml
        assert str(point) == (
            f"GmshPoint(tag={point.id}, "
            f"coords=({float(coords[0])}, {float(coords[1])}, {float(coords[2])}))"
        )
        assert point.dim == 0
        assert point.name == name
        assert point.radius == np.linalg.norm(coords)

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_coords2D(self, name, coords, ml):
        """Test the 2D initialization of a GmshPoint object."""
        point = GmshPoint.from_coordinates(name=name, coords=coords[0:2], meshLength=ml)
        gmsh.model.occ.synchronize()
        assert point.coordinate == (coords[0], coords[1], 0.0)
        assert point.meshLength == ml
        assert (
            str(point)
            == f"GmshPoint(tag={point.id}, coords=({float(coords[0])}, {float(coords[1])}, 0.0))"
        )
        assert point.dim == 0
        assert point.name == name
        assert point.radius == np.linalg.norm(coords[0:2])

    @pytest.mark.parametrize("name, coords, ml", init_cases)
    def test_init_id(self, name, coords, ml):
        """Test the initialization of a GmshPoint object with a given tag."""
        point_tag = gmsh.model.occ.addPoint(coords[0], coords[1], coords[2], ml)
        gmsh.model.setEntityName(0, point_tag, name)
        gmsh.model.occ.synchronize()
        point = GmshPoint(point_tag)
        assert point.id == point_tag
        assert point.coordinate == (coords[0], coords[1], coords[2])
        assert point.x == coords[0]
        assert point.y == coords[1]
        assert point.z == coords[2]
        assert point.meshLength == ml
        assert point.name == name

    def test_init_mL_not_number(self):
        """Test that the initialization of a GmshPoint object fails with a non-numeric
        mesh size value."""
        with pytest.raises(TypeError):
            GmshPoint.from_coordinates(
                name="test", coords=np.array([0, 0, 0]), meshLength="a"
            )

    def test_init_mL_zero(self):
        """Test that the initialization of a GmshPoint object fails with a zero mesh
        size value."""
        with pytest.raises(ValueError):
            GmshPoint.from_coordinates(np.array([0, 0, 0]), 0, "test")

    def test_init_point_not_in_gmsh(self):
        """Test that the initialization of a GmshPoint object fails with a tag that does
        not exist in the Gmsh model."""
        with pytest.raises(ValueError):
            GmshPoint(tag=1)

    def test_set_id(self, gmsh_point: GmshPoint):
        """Test the setter for the id property of a GmshPoint object."""
        gmsh_point.id = 10
        assert gmsh_point.id == 10

    def test_set_name(self, gmsh_point: GmshPoint):
        """Test the setter for the name property of a GmshPoint object."""
        gmsh_point.name = "different name"
        assert gmsh_point.name == "different name"

    def test_set_mesh_length(self, gmsh_point: GmshPoint):
        """Test the setter for the meshLength property of a GmshPoint object."""
        gmsh_point.meshLength = 0.1
        assert gmsh_point.meshLength == 0.1

    def test_reset_coords(self, gmsh_point: GmshPoint):
        """Test that the setter for the coordinate property of a GmshPoint object raises
        an AttributeError."""
        with pytest.raises(AttributeError):
            gmsh_point.coordinate = np.array([0, 1, 0])  # this raises attribute error

    def test_reset_x(self, gmsh_point: GmshPoint):
        """Test that the setter for the x property of a GmshPoint object raises an
        AttributeError."""
        with pytest.raises(AttributeError):
            gmsh_point.x = 1.0  # this raises attribute error

    def test_translate(self, gmsh_point: GmshPoint):
        """Test the translation of a GmshPoint object."""
        gmsh_point.translate(1, 1, 1)
        assert gmsh_point.coordinate == (1, 1, 1)

    @pytest.mark.parametrize(
        "coords, angle, expected_coords",
        [
            ([0, 0, 0], 0.0, [0, 0, 0]),
            ([1, 1, 0], np.radians(45), [0, np.sqrt(2), 0]),
            ([-1, 1, 0], np.radians(135), [0, -np.sqrt(2), 0]),
            ([-1, 0, 0], np.radians(180), [1, 0, 0]),
            ([0, -1, 0], np.radians(270), [-1, 0, 0]),
            ([0, 1, 0], np.radians(-90), [1, 0, 0]),
        ],
    )
    def test_rotate_z(self, coords, angle, expected_coords):
        """Test the rotation of a GmshPoint object around the Z-axis."""
        point = GmshPoint.from_coordinates(name="test", coords=coords, meshLength=1)
        point.rotateZ(angle=angle)
        assert np.isclose(point.coordinate, expected_coords, atol=TOLERANCE).all

    def test_duplicate(self, gmsh_point: GmshPoint):
        """Test the duplication of a GmshPoint object."""
        new_point = gmsh_point.duplicate()
        assert new_point.coordinate == gmsh_point.coordinate
        assert new_point.meshLength == gmsh_point.meshLength
        assert new_point.name == gmsh_point.name + "_dup"

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
        """Test the calculation of the angle between the x-axis and a GmshPoint object."""
        point = GmshPoint.from_coordinates(name="test", coords=coords, meshLength=1)
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
        """Test the calculation of the angle between the x-axis and a GmshPoint object in
        degrees."""
        point = GmshPoint.from_coordinates(name="test", coords=coords, meshLength=1)
        angle_to_x = point.getAngleToX(flag_deg=True)
        assert angle_to_x == expected_angle

    def test_calc_distance(self):
        """Test the calculation of the distance between two GmshPoint objects."""
        point = GmshPoint.from_coordinates(name="test1", coords=[0, 0, 0], meshLength=1)
        other_point = GmshPoint.from_coordinates(
            name="test2", coords=[1, 1, 0], meshLength=1
        )
        distance = point.calcDist(other_point.coordinate)
        assert distance == np.sqrt(2)

    def test_plot(self, gmsh_point: GmshPoint):
        """Just make sure that the plot method does not raise an error."""
        gmsh_point.plot()

    # TODO: Add test for Point methods:
    #   Point.isEqual
