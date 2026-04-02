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
"""Module to test winding translation"""
from __future__ import annotations

from os.path import abspath, join

import pytest
from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

from pyemmo.api.pyleecan.translate_winding import translate_winding
from tests.api.pyleecan.testutils import TEST_API_PYLCN_DATA_DIR


@pytest.mark.parametrize(
    "machine_sample,exp_layout",
    [
        (
            "03_synrm_muster_Bachelor.json",
            [
                [[1, 2, -7, -8, 13, 14, -19, -20], []],
                [[5, 6, -11, -12, 17, 18, -23, -24], []],
                [[-3, -4, 9, 10, -15, -16, 21, 22], []],
            ],
        ),
        (
            "03_synrm_muster_Bachelor_zaw.json",
            [
                [
                    [1, 2, -7, -8, 13, 14, -19, -20],
                    [-7, -8, 13, 14, -19, -20, 1, 2],
                ],
                [
                    [5, 6, -11, -12, 17, 18, -23, -24],
                    [-11, -12, 17, 18, -23, -24, 5, 6],
                ],
                [
                    [-3, -4, 9, 10, -15, -16, 21, 22],
                    [9, 10, -15, -16, 21, 22, -3, -4],
                ],
            ],
        ),
        (
            "03_synrm_muster_Bachelor_zww.json",
            [
                [
                    [1, 2, -7, -8, 13, 14, -19, -20],
                    [-5, -6, 11, 12, -17, -18, 23, 24],
                ],
                [
                    [5, 6, -11, -12, 17, 18, -23, -24],
                    [-9, -10, 15, 16, -21, -22, 3, 4],
                ],
                [
                    [-3, -4, 9, 10, -15, -16, 21, 22],
                    [7, 8, -13, -14, 19, 20, -1, -2],
                ],
            ],
        ),
    ],
)
def test_translate_winding(machine_sample, exp_layout):
    """Function to test winding translation"""
    machine: Machine = load(abspath(join(TEST_API_PYLCN_DATA_DIR, machine_sample)))
    swat_em_datamodel = translate_winding(machine)
    wind_swat = swat_em_datamodel.get_phases()
    assert wind_swat == exp_layout
