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
from __future__ import annotations

import math

import gmsh
import numpy as np
import pytest

from pyemmo.api import air
from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.gmsh.gmsh_point import GmshPoint
from pyemmo.script.gmsh.gmsh_segment_surface import GmshSegmentSurface
from pyemmo.script.gmsh.gmsh_surface import GmshSurface

from ..script.gmsh.test_gmsh_seg_surface import create_segment
from ..script.gmsh.test_gmsh_surface import add_circle as add_gmsh_circle


def add_machine_seg_circ(
    center: GmshPoint, radius: float, nbr_segments: int
) -> MachineSegmentSurface:
    """Helper function to add a circular MachineSegmentSurface to the gmsh model. The
    circle is created with the given center and radius and is discretized with the
    given number of segments.

    Args:
        center (GmshPoint): Center point of the circle.
        radius (float): Radius of the circle.
        nbr_segments (int): Number of segments to discretize the circle.

    Returns:
        MachineSegmentSurface: The created circular MachineSegmentSurface.
    """
    circ = add_gmsh_circle(center, radius)
    return MachineSegmentSurface("circ_part_id", air, circ.id, nbr_segments)


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


@pytest.fixture(scope="function", name="machine_seg_surf")
def fixture_machine_segment_surface(gmsh_surface: GmshSegmentSurface):
    """Test MachineSegmentSurface object from fixture_gmsh_surface()"""
    return MachineSegmentSurface(
        part_id="part",
        material=air,
        tag=gmsh_surface.id,
        nbr_segments=gmsh_surface.nbr_segments,
    )


@pytest.fixture(scope="function", name="gmsh_surface")
def fixture_gmsh_surface():
    """Default test Surface"""
    return create_segment()


@pytest.fixture(scope="function")
def fixture_gmsh_circle():
    """Default test circle with radius 1 meter."""
    centerpoint = GmshPoint.from_coordinates(coords=(0, 0, 0))
    return add_gmsh_circle(centerpoint, 1)


def test_init_with_id():
    """Test the init of Surface"""
    nbr_segments = 8
    # add circle that fits into a perimeter of 1m nbr_segments times
    max_circ_radius = 2 * np.pi / 8
    radius = 0.75 * max_circ_radius
    circ = add_gmsh_circle(GmshPoint.from_coordinates(coords=(1, 0, 0)), radius)
    expected_part_id = "hole"
    expected_name = "Test surface"
    gmsh_surface = MachineSegmentSurface(
        part_id=expected_part_id,
        material=air,
        tag=circ.id,
        nbr_segments=nbr_segments,
        name=expected_name,
    )
    # test ``Transormable`` properties
    assert gmsh_surface.name == expected_name
    # test ``Surface`` properties
    assert len(gmsh_surface.curve) == 4
    assert gmsh_surface.curve == circ.curve
    assert gmsh_surface.points == circ.points
    assert not gmsh_surface.tools
    # test ``GmshSurface`` properties
    assert gmsh_surface.dim == 2
    assert gmsh_surface.id == circ.id
    assert math.isclose(gmsh_surface.area, np.pi * radius**2, rel_tol=1e-3)
    # test ``SegmentSurface`` properties
    assert gmsh_surface.nbr_segments == nbr_segments
    assert gmsh_surface.segment_nbr == 0
    # test ``MachineSegmentSurface`` properties
    assert gmsh_surface.part_id == expected_part_id
    assert gmsh_surface.material == air


def test_init_with_curveloop(machine_seg_surf: GmshSegmentSurface):
    """Test the init of Surface"""
    new_gmsh_surface_seg = MachineSegmentSurface.from_curve_loop(
        curve_loop=machine_seg_surf.curve,
        part_id="test id",
        material=air,
        nbr_segments=machine_seg_surf.nbr_segments,
    )
    assert new_gmsh_surface_seg.name == ""

    assert new_gmsh_surface_seg.curve == machine_seg_surf.curve
    assert new_gmsh_surface_seg.points == machine_seg_surf.points

    assert new_gmsh_surface_seg.dim == 2
    assert new_gmsh_surface_seg.id != machine_seg_surf.id
    assert np.isclose(
        new_gmsh_surface_seg.meanMeshLength, machine_seg_surf.meanMeshLength, rtol=1e-3
    )
    assert np.isclose(new_gmsh_surface_seg.area, machine_seg_surf.area, rtol=1e-3)

    assert new_gmsh_surface_seg.nbr_segments == machine_seg_surf.nbr_segments
    assert new_gmsh_surface_seg.segment_nbr == machine_seg_surf.segment_nbr
    assert np.isclose(new_gmsh_surface_seg.angle, machine_seg_surf.angle, rtol=1e-3)

    assert new_gmsh_surface_seg.part_id == "test id"
    assert new_gmsh_surface_seg.material == air


def test_init_with_id_newName(machine_seg_surf: GmshSegmentSurface):
    """Test the init of Surface"""
    new_gmsh_surface = MachineSegmentSurface(
        part_id="",
        material=air,
        nbr_segments=machine_seg_surf.nbr_segments,
        tag=machine_seg_surf.id,
        name="new name",
    )
    assert new_gmsh_surface.name == "new name"


def test_set_mesh_length(machine_seg_surf: MachineSegmentSurface):
    """Test setMeshLength() method"""
    machine_seg_surf.setMeshLength(0.1)
    assert np.isclose(machine_seg_surf.meanMeshLength, 0.1, rtol=1e-3)


def test_get_min_mesh_length(machine_seg_surf: MachineSegmentSurface):
    """Test getMinMeshLength() method"""
    min_ml = 1e-6
    machine_seg_surf.curve[0].start_point.meshLength = min_ml
    assert np.isclose(machine_seg_surf.getMinMeshLength(), min_ml, rtol=1e-3)


@pytest.mark.parametrize(
    "surf_fixture, expected_area",
    [
        ("gmsh_surface", (1.3**2 * np.pi - np.pi) / 8),
        ("fixture_gmsh_circle", np.pi),
    ],
)
def test_area(surf_fixture, expected_area: float, request):
    """Test area() property"""
    # request is a special fixture to request other fixtures. For more information see:
    # https://docs.pytest.org/en/7.1.x/reference/reference.html#id37
    surf: GmshSurface = request.getfixturevalue(surf_fixture)
    surf = MachineSegmentSurface("", air, surf.id, 1)
    assert np.isclose(surf.area, expected_area, rtol=1e-3)


# def test_translate(gmsh_surface: GmshSegmentSurface):
#     """Test translate() method"""
#     gmsh_surface.translate(1.1, -1.1, 0)  # translate surf into x by 1.1, y by -1.1
#     exspected_coords = [(1.1, -1.1, 0), (2.1, -1.1, 0), (2.1, -0.1, 0), (1.1, -0.1, 0)]
#     for coords in exspected_coords:
#         assert any(
#             all(np.isclose(coords, point.coordinate, atol=1e-6))
#             for point in gmsh_surface.points
#         )


def test_rotate_z(machine_seg_surf: MachineSegmentSurface):
    """Test rotateZ() method"""
    # rotate surf by 90 degrees around z-axis
    center = Point("center point", 0, 0, 0)
    machine_seg_surf.rotateZ(center, np.pi / 2)
    gmsh.model.occ.synchronize()  # NOTE: Need to sync to update the coordinates
    new_angle = 3 * np.pi / 4
    exspected_coords = [
        (0, 1, 0),
        (0, 1.3, 0),
        (np.cos(new_angle), np.sin(new_angle), 0),
        (1.3 * np.cos(new_angle), 1.3 * np.sin(new_angle), 0),
    ]
    for coords in exspected_coords:
        if not any(
            all(np.isclose(coords, point.coordinate, atol=1e-6))
            for point in machine_seg_surf.points
        ):
            points = ", ".join(str(point) for point in machine_seg_surf.points)
            raise AssertionError(
                f"Point with coordinates {coords} not found in points of " f"{points}."
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
def test_duplicate(machine_seg_surf: MachineSegmentSurface, name: str):
    """Test duplicate() method"""
    duplicate = machine_seg_surf.duplicate(name=name)
    assert machine_seg_surf.id != duplicate.id
    assert len(machine_seg_surf.points) == len(duplicate.points)
    assert len(machine_seg_surf.curve) == len(duplicate.curve)
    # lines are equal if they are of the same line type (line, arc, spline) and have
    # matching points. Method arePointsEqual() checks for the points coordinates.
    for curve in machine_seg_surf.curve:
        assert any(
            isinstance(curve, type(dup_line)) and curve.arePointsEqual(dup_line)
            for dup_line in duplicate.curve
        )
    assert machine_seg_surf.dim == duplicate.dim
    if name:
        assert duplicate.name == name
    else:
        assert duplicate.name == machine_seg_surf.name + "_dup"

    assert machine_seg_surf.meanMeshLength == duplicate.meanMeshLength


@pytest.mark.xfail(reason="not implemented mirror yet")
def test_mirror(machine_seg_surf: MachineSegmentSurface):
    """Test mirror() method. NOT IMPLEMENTED YET"""
    plane_point = Point("center point", 0, 0, 0)
    x_point = Point("x point", 1, 0, 0)
    y_point = Point("y point", 0, 1, 0)
    x_vector = Line(name="x vector", start_point=plane_point, end_point=x_point)
    y_vector = Line(name="y vector", start_point=plane_point, end_point=y_point)
    machine_seg_surf.mirror(
        planePoint=plane_point, planeVector1=x_vector, planeVector2=y_vector
    )


def test_combine(machine_seg_surf: MachineSegmentSurface):
    """Test combine() method"""
    add_surf = machine_seg_surf.rotate_duplicate(1)
    # FIXME: For now just make sure the combination creates a valid surface and does not
    # raise an error
    comb_surf = machine_seg_surf.combine(add_surf, removeObject=True, removeTool=True)


def test_cut_out_inside(machine_seg_surf: MachineSegmentSurface):
    """Test cutOut() method for circle that is **completly inside** the parent surface."""
    center = GmshPoint.from_coordinates(
        name="Center", coords=machine_seg_surf.calcCOG().coordinate
    )
    circ = add_machine_seg_circ(
        center,
        radius=machine_seg_surf.curve[0].length / 4,
        nbr_segments=machine_seg_surf.nbr_segments,
    )
    machine_seg_surf.cutOut(circ)
    # assert len(gmsh_surface.curve) == 8
    assert machine_seg_surf.dim == 2
    assert machine_seg_surf.name == "Test segment surface"
    assert machine_seg_surf.id == 3
    assert len(machine_seg_surf.tools) == 1
    assert machine_seg_surf.tools[0].id == circ.id


def test_cut_out_overlap(machine_seg_surf: MachineSegmentSurface):
    """Test cutOut() method for circle that **overlaps** the parent surface."""
    circ_center = machine_seg_surf.curve[
        0
    ].middle_point  # center point between start and
    circ_center = GmshPoint.from_coordinates(coords=circ_center.coordinate)
    # end point
    circ = add_machine_seg_circ(
        circ_center,
        radius=machine_seg_surf.curve[0].length / 4,
        nbr_segments=machine_seg_surf.nbr_segments,
    )
    machine_seg_surf.cutOut(circ)
    assert len(machine_seg_surf.curve) == 10
    assert machine_seg_surf.dim == 2
    assert machine_seg_surf.name == "Test segment surface"
    assert machine_seg_surf.id == 7


def test_cut_out_noIntersect(machine_seg_surf: MachineSegmentSurface):
    """Test cutOut() method for circle that **does not intersect** the parent
    surface -> Nothing should happen to the parent surface parameters."""
    circ_center = machine_seg_surf.points[0]
    circ = add_machine_seg_circ(
        circ_center,
        radius=0.1,
        nbr_segments=machine_seg_surf.nbr_segments,
    )
    circ.translate(0, -0.3, 0)  # move circle out of parent surface
    machine_seg_surf.cutOut(circ)
    assert len(machine_seg_surf.curve) == 4
    assert machine_seg_surf.dim == 2
    assert machine_seg_surf.name == "Test segment surface"
    assert machine_seg_surf.id == 1


def test_cut_out_greaterSymTool(machine_seg_surf: MachineSegmentSurface):
    """Test cutOut() method for circle that is **completly inside** the parent
    surface and has a greater symmetry than the parent surface. -> The tool
    should be cut out 3 times."""
    center = GmshPoint.from_coordinates(
        name="Center", coords=machine_seg_surf.calcCOG().coordinate
    )
    circ = add_machine_seg_circ(
        center,
        radius=machine_seg_surf.curve[0].length / 4,
        nbr_segments=3 * machine_seg_surf.nbr_segments,
    )
    # rotate circle so it fits into the segment 3 times
    circ.rotateZ(
        rotationPoint=GmshPoint.from_coordinates(coords=(0, 0)),
        angle=-machine_seg_surf.angle * 3 / 8,
    )
    machine_seg_surf.cutOut(circ)
    # assert len(gmsh_surface.curve) == 8
    assert machine_seg_surf.dim == 2
    assert machine_seg_surf.name == "Test segment surface"
    assert machine_seg_surf.id == 7
    assert len(machine_seg_surf.tools) == 3
    assert machine_seg_surf.tools[0].id == circ.id


def test_cut_out_lowerSymTool(machine_seg_surf: MachineSegmentSurface):
    """Test cutOut() method for circle that is **completly inside** the parent
    surface and has a lower symmetry than the parent surface. -> The parent
    surface should be duplicated, updated and the tool should be cut out once."""
    center = GmshPoint.from_coordinates(
        name="Center", coords=machine_seg_surf.calcCOG().coordinate
    )
    circ = add_machine_seg_circ(
        center,
        radius=machine_seg_surf.curve[0].length / 4,
        nbr_segments=machine_seg_surf.nbr_segments / 2,
    )
    # rotate circle so it fits into the segment 2 times
    circ.rotateZ(
        rotationPoint=GmshPoint.from_coordinates(coords=(0, 0)),
        angle=machine_seg_surf.angle / 2,
    )
    machine_seg_surf.cutOut(circ)
    # assert len(gmsh_surface.curve) == 8
    assert machine_seg_surf.dim == 2
    assert machine_seg_surf.name == "Test segment surface"
    assert machine_seg_surf.id == 3
    assert len(machine_seg_surf.tools) == 1
    assert machine_seg_surf.tools[0].id == circ.id


# TODO: Add tests for the following methods:
# Surface.allPoints
# Surface.calcCOG
# Surface.curve
# Surface.cutOut
# Surface.delete
# Surface.points
# Surface.recombineCurves


@pytest.mark.xfail(reason="not implemented subtraction yet")
def test_2_layer_subtract(machine_seg_surf: MachineSegmentSurface):
    """Test a two layer subtraction where the tool of the main surface has a tool
    aswell"""
    center = GmshPoint.from_coordinates(
        name="Center", coords=machine_seg_surf.calcCOG().coordinate
    )
    circ_big = add_machine_seg_circ(
        center, radius=0.25 / 2, nbr_segments=machine_seg_surf.nbr_segments
    )
    circ_small = add_machine_seg_circ(
        center, radius=0.1 / 2, nbr_segments=machine_seg_surf.nbr_segments
    )
    circ_big.cutOut(circ_small)  # SECOND LAYER CUT
    machine_seg_surf.cutOut(circ_big)  # FIRST LAYER CUT

    # TODO: Add assert statements


def test_rotate_duplicate(machine_seg_surf: MachineSegmentSurface):
    """Test rotate_duplicate() method"""
    # create a duplicate of the rotated surface
    dup_surf = machine_seg_surf.rotate_duplicate(1)
    assert dup_surf.segment_nbr == 1
    assert dup_surf.name == machine_seg_surf.name + " (Seg.: 1)"
    assert dup_surf.nbr_segments == machine_seg_surf.nbr_segments
    assert dup_surf.material == machine_seg_surf.material


def test_rotate_duplicate_wrongSym(machine_seg_surf: MachineSegmentSurface):
    """Test rotate_duplicate() method"""
    # create a duplicate of the rotated surface
    with pytest.raises(ValueError):
        machine_seg_surf.rotate_duplicate(10)


def test_plot(machine_seg_surf: MachineSegmentSurface):
    """Test plot() method"""
    machine_seg_surf.plot()
    machine_seg_surf.plot(symmetry=1)
