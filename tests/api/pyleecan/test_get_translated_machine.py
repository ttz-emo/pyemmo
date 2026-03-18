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
"""Module to test pyemmo.api.pyleecan.get_translated_machine"""
from __future__ import annotations

import pytest

from pyemmo.api.pyleecan.translate_machine import translate_machine

from .testutils import (  # noqa # pylint: disable=W0611
    IPMSM,
    SIPMSM_1,
    SYNRM_ZAW,
    Toyota_Prius,
    initialize_gmsh,
)


@pytest.mark.parametrize("machine", ["Toyota_Prius", "IPMSM", "SIPMSM_1", "SYNRM_ZAW"])
def test_get_translated_machine(machine, request):
    """Function to test pyemmo.api.pyleecan.get_translated_machine"""
    machine = request.getfixturevalue(machine)

    geo_translation_dict = translate_machine(machine=machine)

    # TODO:
    # - Check if all relevant surfaces are translated
    # - Check symmetries
