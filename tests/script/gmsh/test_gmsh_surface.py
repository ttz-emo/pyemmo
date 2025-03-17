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

from pyemmo.script.gmsh.gmsh_surface import GmshArc, GmshLine, GmshPoint, GmshSurface


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.fixture
def gmsh_surface():
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
    """Create a test Circle"""
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


def test_init(gmsh_surface: GmshSurface):
    """Test the init of Surface"""
    assert len(gmsh_surface.curve) == 4
    assert gmsh_surface.name == "Test surface"
    # TODO: Add more assert statements


def test_translate(gmsh_surface: GmshSurface):
    """Test translate() method"""
    gmsh_surface.translate(1.1, 0, 0)  # translate surf into x by 1.1
    exspected_coords = [(1.1, 0, 0), (2.1, 0, 0), (2.1, 1.0, 0), (1.1, 1.0, 0)]
    for coords in exspected_coords:
        assert any(coords == point.coordinate for point in gmsh_surface.points)


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
