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
Module to test translate surface function of api
import pyemmo.api.pyleecan.create_gmsh_surface
"""
from __future__ import annotations

import gmsh
import pytest
from pyleecan.Functions.labels import HOLEM_LAB, HOLEV_LAB, get_obj_from_label

from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.api.pyleecan import PyleecanMachine
from pyemmo.api.pyleecan.build_pyemmo_material import build_pyemmo_material
from pyemmo.api.pyleecan.create_gmsh_surf import create_gmsh_surface

from .testutils import (  # noqa # pylint: disable=W0611
    SYNRM_ZAW,
    Toyota_Prius,
    initialize_gmsh,
)


@pytest.mark.parametrize(
    ("machine", "nbr_main_surfs", "nbr_total_surfs"),
    [("Toyota_Prius", 1, 6), ("SYNRM_ZAW", 1, 4)],
)
def test_create_gmsh_surface(machine, request, nbr_main_surfs, nbr_total_surfs):
    """Function to test ``pyemmo.api.pyleecan.create_gmsh_surface``"""
    # get value of fixture
    machine: PyleecanMachine = request.getfixturevalue(machine)
    sym, _ = machine.rotor.comp_periodicity_geo()
    rotor_surfs = machine.rotor.build_geometry(sym=sym, alpha=0)

    surf = rotor_surfs.pop(0)
    lam_surf = create_gmsh_surface(
        surf,
        nbr_segments=sym,
        material=build_pyemmo_material(machine.rotor.mat_type),
        name=surf.label,
    )

    geometry_list: list[MachineSegmentSurface] = []
    geometry_list.append(lam_surf)
    for surf in rotor_surfs:
        # get pyleecan object for material identification
        pyleecan_obj = get_obj_from_label(machine, surf.label)
        if hasattr(pyleecan_obj, "mat_type"):
            material = pyleecan_obj.mat_type
        elif hasattr(pyleecan_obj, "mat_void"):
            material = pyleecan_obj.mat_void
        else:
            raise AttributeError(
                "Pyleecan object material can not be accessed by mat_type or mat_void."
            )

        # translating the surface
        pyemmo_surf = create_gmsh_surface(
            surf, sym, build_pyemmo_material(material), surf.label
        )
        pyemmo_surf.plot()
        if any(label in surf.label for label in (HOLEM_LAB, HOLEV_LAB)):
            lam_surf.cutOut(pyemmo_surf)
        else:
            geometry_list.append(pyemmo_surf)
    # there should only be the lamination surface in the geo list
    assert len(geometry_list) == nbr_main_surfs
    # there should be 5 surfaces subtracted from this lam surface
    assert len(lam_surf.tools) == (nbr_total_surfs - nbr_main_surfs)
    # there should be 6 surfaces created in gmsh
    assert len(gmsh.model.getEntities(2)) == nbr_total_surfs
