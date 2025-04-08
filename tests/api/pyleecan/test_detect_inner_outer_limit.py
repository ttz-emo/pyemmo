#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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
"""Module to test the detection of the model boundaries in the api."""
from os.path import abspath, join
from typing import List

import pytest
from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

from pyemmo.api.pyleecan.detect_inner_outer_limit import (
    detect_inner_outer_limit,
)
from pyemmo.api.pyleecan.translate_surfs import translate_surface
from pyemmo.script.geometry.segment_surface import SegmentSurface
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


@pytest.mark.parametrize(
    "machine_sample",
    [
        "00_prius_machine.json",
        "02_spmsm_muster_02.json",
        "03_synrm_muster_Bachelor.json",
    ],
)
def test_detect_inner_outer_limit(machine_sample):
    """Function to test the detection of the model boundaries in the api."""
    machine: Machine = load(abspath(join(TEST_API_PYLCN_DATA_DIR, machine_sample)))

    all_surfaces: list = machine.rotor.build_geometry(
        sym=machine.rotor.comp_periodicity_geo()[0], alpha=0
    )

    all_surfaces.extend(
        machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)
    )

    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SegmentSurface] = []
    angle_point_ref_list = []

    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        # translating the surface
        pyemmo_surf, angle_point_ref_list = translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    has_shaft = bool(machine.rotor.Rint > 0)

    if machine.rotor.is_internal:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.rotor.Rint,
            outer_radius=machine.stator.Rext,
            has_shaft=has_shaft,
        )
    else:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.stator.Rint,
            outer_radius=machine.rotor.Rext,
            has_shaft=has_shaft,
        )

    if machine_sample == "00_prius_machine.json":
        assert geometry_list[0].curve[3].name == "InnerLimit"
        assert geometry_list[6].curve[1].name == "OuterLimit"

    elif machine_sample == "02_spmsm_muster_02.json":
        assert geometry_list[2].curve[1].name == "OuterLimit"

    elif machine_sample == "03_synrm_muster_Bachelor.json":
        assert geometry_list[0].curve[3].name == "InnerLimit"
        assert geometry_list[4].curve[1].name == "OuterLimit"
