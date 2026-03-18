#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""
This module tests the create_gmsh_point function from the create_gmsh_point.py module.
It verifies the conversion of pyleecan points to pyemmo points using the GmshPoint class.
"""

from __future__ import annotations

import gmsh
import numpy
from hypothesis import given, settings
from hypothesis import strategies as st

from pyemmo.api.pyleecan.create_gmsh_point import create_gmsh_point
from pyemmo.script.geometry.point import Point


class TestGmshPyleecan2GmshPoint:
    """PyTest class for testing of GmshArc class"""

    def setup_method(self):
        """Setup the Gmsh model for the tests."""
        gmsh.initialize()
        gmsh.model.add("test PyEMMO GmshPoint class")

    def teardown_method(self):
        """Close the Gmsh model after the tests."""
        gmsh.finalize()

    @settings(max_examples=50, derandomize=True)
    @given(
        pyleecan_point=st.complex_numbers(
            allow_nan=False,
            allow_infinity=False,
        )
    )
    def test_translate_point(self, pyleecan_point: complex) -> None:
        """test function to build pyemmo point from pyleecan point (np.complex)"""
        pyemmo_point: Point = create_gmsh_point(pyleecan_point=pyleecan_point)
        assert pyemmo_point.coordinate[0] == numpy.real(pyleecan_point)
        assert pyemmo_point.coordinate[1] == numpy.imag(pyleecan_point)
        assert pyemmo_point.coordinate[2] == 0
        assert pyemmo_point.name == ""  # default name is empty
        assert pyemmo_point.meshLength == 1e-3  # default mesh length
