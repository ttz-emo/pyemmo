#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of
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
"""Module to test the create_airgaps functions"""

from __future__ import annotations

import math

import gmsh
import numpy as np
import pytest

from pyemmo.api import air
from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.api.json.create_airgaps import (
    create_airgap_surfaces,
    _create_band_contour,
    _create_band_surf,
)
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from pyemmo.script.gmsh.gmsh_point import GmshPoint
from pyemmo.script.gmsh.gmsh_segment_surface import GmshSegmentSurface
from pyemmo.script.gmsh.gmsh_surface import GmshSurface

from ...script.gmsh.test_gmsh_seg_surface import create_segment
from ...script.gmsh.test_gmsh_surface import add_circle as add_gmsh_circle


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
    """Default test Surface"""
    return create_segment()


@pytest.fixture(scope="function", name="machine_seg_surf")
def fixture_machine_segment_surface(gmsh_surface: GmshSegmentSurface):
    """Test MachineSegmentSurface object from fixture_gmsh_surface()"""
    return MachineSegmentSurface(
        part_id="part",
        material=air,
        tag=gmsh_surface.id,
        nbr_segments=gmsh_surface.nbr_segments,
    )


@pytest.fixture(scope="function")
def fixture_gmsh_circle():
    """Default test circle with radius 1 meter."""
    centerpoint = GmshPoint.from_coordinates(coords=(0, 0, 0))
    return add_gmsh_circle(centerpoint, radius=1)


def add_circle(
    center: GmshPoint, radius: float, nbr_segments: int
) -> MachineSegmentSurface:
    """Function to create MachineSegmentSurface circle"""
    circ = add_gmsh_circle(center, radius)
    return MachineSegmentSurface(
        part_id="Circle",
        material=air,
        tag=circ.id,
        name=circ.name,
        nbr_segments=nbr_segments,
    )


def test_create_band_contour_inwards(machine_seg_surf: MachineSegmentSurface):
    """Test band contour creation for symmetry = 8"""
    # machine_seg_surf has inner radius 1 meter and outer radius 1.3 meter
    inner_curve = machine_seg_surf.curve[-1]
    outer_curve = machine_seg_surf.curve[1]

    band_height = 0.03
    # create inner band
    inner_band_contour, new_interface, new_start_point = _create_band_contour(
        start_point=inner_curve.start_point,
        interface=[inner_curve],
        band_height=-band_height,
        symmetry=machine_seg_surf.nbr_segments,
    )

    assert len(inner_band_contour) == 4
    assert inner_curve in inner_band_contour
    assert outer_curve not in inner_band_contour
    assert new_interface[0].radius == inner_curve.radius - band_height
    assert all(
        np.isclose(new_start_point.coordinate, (inner_curve.radius - band_height, 0, 0))
    )


def test_create_band_contour_outwards(machine_seg_surf: MachineSegmentSurface):
    """Test band contour creation for symmetry = 8"""
    # machine_seg_surf has inner radius 1 meter and outer radius 1.3 meter
    inner_curve = machine_seg_surf.curve[-1]
    outer_curve = machine_seg_surf.curve[1]

    band_height = 0.03
    # create inner band
    band_contour, new_interface, new_start_point = _create_band_contour(
        start_point=outer_curve.start_point,
        interface=[outer_curve],
        band_height=+band_height,
        symmetry=machine_seg_surf.nbr_segments,
    )

    assert len(band_contour) == 4
    assert outer_curve in band_contour
    assert inner_curve not in band_contour
    assert new_interface[0].radius == outer_curve.radius + band_height
    assert all(
        np.isclose(new_start_point.coordinate, (outer_curve.radius + band_height, 0, 0))
    )


# TODO: Add tests for creating the airgap surfaces
# TODO: Add tests for creating the airgap surfaces with symmetry = 1!
