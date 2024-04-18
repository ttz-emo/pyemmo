#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""This module tests the build_pyemmo_point() function.
Following functions are included in this module:
* test_normal_point()
* test_center_point()
"""

import numpy
from hypothesis import given, settings, strategies as st

from pyemmo.script.geometry.point import Point
from pyemmo.api.pyleecan.build_pyemmo_point import build_pyemmo_point


@settings(max_examples=50, report_multiple_bugs=True, derandomize=True)
@given(pyleecan_point=st.complex_numbers(allow_nan=False))
def test_build_pyemmo_point(pyleecan_point: complex) -> None:
    pyemmo_point: Point = build_pyemmo_point(pyleecan_point=pyleecan_point)
    assert pyemmo_point.coordinate[0] == numpy.real(pyleecan_point)
    assert pyemmo_point.coordinate[1] == numpy.imag(pyleecan_point)
    assert pyemmo_point.coordinate[2] == 0
    assert pyemmo_point.name == "point_pylc"
    assert pyemmo_point.meshLength == 1e-3
