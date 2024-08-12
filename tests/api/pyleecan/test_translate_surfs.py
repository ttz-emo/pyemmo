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
"""
Module to test translate surface function of api
import pyemmo.api.pyleecan.translate_surfs
"""
from os.path import abspath, join
from typing import List

from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

from pyemmo.api.json.modelJSON import SurfaceAPI
import pyemmo.api.pyleecan.translate_surfs
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


def test_translate_surfs():
    """Function to test ``pyemmo.api.pyleecan.translate_surfs``"""
    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []
    machine: Machine = load(
        abspath(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))
    )
    all_surfaces: list = machine.rotor.build_geometry(
        sym=machine.rotor.comp_periodicity_geo()[0], alpha=0
    )

    all_surfaces.extend(
        machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)
    )
    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        # translating the surface
        (
            pyemmo_surf,
            angle_point_ref_list,
        ) = pyemmo.api.pyleecan.translate_surfs.translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    assert len(geometry_list) == 8

    expected_data = [
        ("Pol", 4),
        ("Lpl", 5),
        ("Mag", 6),
        ("Lpl", 4),
        ("Mag", 6),
        ("Lpl", 5),
        ("StNut", 13),
        ("StCu0", 7),
    ]

    for i, (expected_id_ext, expected_len) in enumerate(expected_data):
        test_surf = geometry_list[i]
        assert test_surf.idExt == expected_id_ext
        assert len(test_surf.curve) == expected_len


if __name__ == "__main__":
    test_translate_surfs()
