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
import gmsh
import numpy as np
import pytest

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.gmsh.gmsh_surface import GmshArc, GmshLine, GmshPoint, GmshSurface


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


@pytest.fixture(scope="function", name="gmsh_surface")
def fixture_gmsh_surface():
    """Default test Surface

          y
            |
    (1,0).---------------.(1,1)
            |               |
            |               |
            |               |
            |               |
            |               |
    (0,0).---------------.(0,1)---->
            |                      x

    """
    return create_rectangle()


@pytest.fixture(scope="function")
def fixture_gmsh_circle():
    """Default test circle with radius 1 meter."""
    centerpoint = GmshPoint(-1, coords=(0, 0, 0))
    return add_circle(centerpoint, 1)


def create_rectangle():
    """Default test Surface

            |
    (1,0).---------------.(1,1)
            |               |
            |               |
            |               |
            |               |
            |               |
    (0,0).---------------.(0,1)---->
            |

    """
    points: list[GmshPoint] = []
    for i, xy in enumerate([(0, 0), (0, 1), (1, 1), (1, 0)]):
        points.append(GmshPoint(-1, f"P{i}", np.array([xy[0], xy[1], 0])))
    lines: list[GmshLine] = []
    for i, point in enumerate(points):
        lines.append(
            GmshLine(tag=-1, name=f"L{i}", start_point=points[i - 1], end_point=point)
        )
    return GmshSurface(tag=-1, name="Test surface", curves=lines)


def add_circle(center: GmshPoint, radius: float):
    """Create a test Circle with ``radius`` at ``center`` contructed by 4 arcs."""
    points: list[GmshPoint] = []
    for i, xy in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
        x, y, _ = center.coordinate
        dx = x
        dy = y
        points.append(
            GmshPoint(
                -1,
                name=f"P{i}",
                coords=[xy[0] * radius + dx, xy[1] * radius + dy, 0],
                meshLength=2 * np.pi * radius / 60,
            )
        )
    lines: list[GmshArc] = []
    for i, point in enumerate(points):
        lines.append(
            GmshArc(
                tag=-1,
                name=f"L{i}",
                start_point=points[i - 1],
                center_point=center,
                end_point=point,
            )
        )
    return GmshSurface(-1, lines, f"Circle {radius=:.1f}")


def test_init_with_curveloop(gmsh_surface: GmshSurface):
    """Test the init of Surface"""
    assert len(gmsh_surface.curve) == 4
    assert gmsh_surface.dim == 2
    assert gmsh_surface.name == "Test surface"
    assert np.isclose(gmsh_surface.meanMeshLength, 1e-3, rtol=1e-3)


def test_init_with_id(gmsh_surface: GmshSurface):
    """Test the init of Surface"""
    new_gmsh_surface = GmshSurface(tag=gmsh_surface.id)
    assert len(new_gmsh_surface.curve) == len(gmsh_surface.curve)
    assert new_gmsh_surface.dim == 2
    assert new_gmsh_surface.name == "Test surface"
    assert np.isclose(
        new_gmsh_surface.meanMeshLength, gmsh_surface.meanMeshLength, rtol=1e-3
    )


def test_init_with_id_newName(gmsh_surface: GmshSurface):
    """Test the init of Surface"""
    new_gmsh_surface = GmshSurface(tag=gmsh_surface.id, name="new name")
    assert new_gmsh_surface.name == "new name"


def test_set_mesh_length(gmsh_surface: GmshSurface):
    """Test setMeshLength() method"""
    gmsh_surface.setMeshLength(0.1)
    assert np.isclose(gmsh_surface.meanMeshLength, 0.1, rtol=1e-3)


def test_get_min_mesh_length(gmsh_surface: GmshSurface):
    """Test getMinMeshLength() method"""
    min_ml = 1e-6
    gmsh_surface.curve[0].start_point.meshLength = min_ml
    assert np.isclose(gmsh_surface.getMinMeshLength(), min_ml, rtol=1e-3)


@pytest.mark.parametrize(
    "surf_fixture, expected_area",
    [
        ("gmsh_surface", 1.0),
        ("fixture_gmsh_circle", np.pi),
    ],
)
def test_area(surf_fixture, expected_area: float, request):
    """Test area() property"""
    # request is a special fixture to request other fixtures. For more information see:
    # https://docs.pytest.org/en/7.1.x/reference/reference.html#id37
    surf: GmshSurface = request.getfixturevalue(surf_fixture)
    assert np.isclose(surf.area, expected_area, rtol=1e-3)


def test_translate(gmsh_surface: GmshSurface):
    """Test translate() method"""
    gmsh_surface.translate(1.1, -1.1, 0)  # translate surf into x by 1.1, y by -1.1
    exspected_coords = [(1.1, -1.1, 0), (2.1, -1.1, 0), (2.1, -0.1, 0), (1.1, -0.1, 0)]
    for coords in exspected_coords:
        assert any(
            all(np.isclose(coords, point.coordinate, atol=1e-6))
            for point in gmsh_surface.points
        )


def test_rotate_z(gmsh_surface: GmshSurface):
    """Test rotateZ() method"""
    # rotate surf by 90 degrees around z-axis
    center = Point("center point", 0, 0, 0)
    gmsh_surface.rotateZ(center, np.pi / 2)
    exspected_coords = [(0, 0, 0), (0, 1, 0), (-1, 0, 0), (-1, 1, 0)]
    for coords in exspected_coords:
        assert any(
            all(np.isclose(coords, point.coordinate, atol=1e-6))
            for point in gmsh_surface.points
        )


@pytest.mark.parametrize(
    "name",
    [
        "new name",
        "",
        pytest.param(
            123, marks=pytest.mark.xfail(reason="New name has to be a string")
        ),
    ],
)
def test_duplicate(gmsh_surface: GmshSurface, name: str):
    """Test duplicate() method"""
    duplicate = gmsh_surface.duplicate(name=name)
    assert gmsh_surface.id != duplicate.id
    assert gmsh_surface.points != duplicate.points
    # lines are equal if they are of the same line type (line, arc, spline) and have
    # matching points
    assert gmsh_surface.curve == duplicate.curve
    assert gmsh_surface.dim == duplicate.dim
    if name:
        assert duplicate.name == name
    else:
        assert duplicate.name == gmsh_surface.name + "_dup"

    assert gmsh_surface.meanMeshLength == duplicate.meanMeshLength


@pytest.mark.xfail(reason="not implemented mirror yet")
def test_mirror(gmsh_surface: GmshSurface):
    """Test mirror() method. NOT IMPLEMENTED YET"""
    plane_point = Point("center point", 0, 0, 0)
    x_point = Point("x point", 1, 0, 0)
    y_point = Point("y point", 0, 1, 0)
    x_vector = Line(name="x vector", start_point=plane_point, end_point=x_point)
    y_vector = Line(name="y vector", start_point=plane_point, end_point=y_point)
    gmsh_surface.mirror(
        planePoint=plane_point, planeVector1=x_vector, planeVector2=y_vector
    )


def test_combine(gmsh_surface: GmshSurface):
    """Test combine() method"""
    add_surf = add_circle(gmsh_surface.points[0], gmsh_surface.curve[0].getPointDist())
    # FIXME: For now just make sure the combination creates a valid surface and does not
    # raise an error
    comb_surf = gmsh_surface.combine(add_surf, removeObject=True, removeTool=True)


def test_cut_out_inside(gmsh_surface: GmshSurface):
    """Test cutOut() method for circle that is **completly inside** the parent surface."""
    center = GmshPoint(name="Center", coords=[0.5, 0.5, 0])
    circ = add_circle(center, radius=0.4)
    gmsh_surface.cutOut(circ)
    assert len(gmsh_surface.curve) == 8
    assert gmsh_surface.dim == 2
    assert gmsh_surface.name == "Test surface"
    assert gmsh_surface.id == 3


def test_cut_out_overlap(gmsh_surface: GmshSurface):
    """Test cutOut() method for circle that **overlaps** the parent surface."""
    circ_center = gmsh_surface.points[0]
    circ = add_circle(circ_center, radius=gmsh_surface.curve[0].getPointDist() / 2)
    gmsh_surface.cutOut(circ)
    assert len(gmsh_surface.curve) == 5
    assert gmsh_surface.dim == 2
    assert gmsh_surface.name == "Test surface"
    assert gmsh_surface.id == 3


def test_cut_out_noIntersect(gmsh_surface: GmshSurface):
    """Test cutOut() method for circle that **does not intersect** the parent surface."""
    circ_center = gmsh_surface.points[0]
    circ = add_circle(circ_center, radius=0.1)
    circ.translate(-0.3, 0, 0)  # move circle out of parent surface
    gmsh_surface.cutOut(circ)
    assert len(gmsh_surface.curve) == 4
    assert gmsh_surface.dim == 2
    assert gmsh_surface.name == "Test surface"
    assert gmsh_surface.id == 1


# TODO: Add tests for the following methods:
# Surface.allPoints
# Surface.calcCOG
# Surface.curve
# Surface.cutOut
# Surface.delete
# Surface.points
# Surface.recombineCurves


@pytest.mark.xfail(reason="not implemented subtraction yet")
def test_2_layer_subtract(gmsh_surface: GmshSurface):
    """Test a two layer subtraction where the tool of the main surface has a tool
    aswell"""
    center = GmshPoint(name="Center", coords=[0.5, 0.5, 0])
    circ_big = add_circle(center, radius=0.4)
    circ_small = add_circle(center, radius=0.15)
    circ_big.cutOut(circ_small)  # SECOND LAYER CUT
    gmsh_surface.cutOut(circ_big)  # FIRST LAYER CUT
    # TODO: Add assert statements
