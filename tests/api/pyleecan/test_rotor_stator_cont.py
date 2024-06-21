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
"""Module to test the rotor and stator contour function of the pyleecan api."""
from os.path import abspath, join
import math
from typing import List
import pytest
from pyleecan.Classes.Machine import Machine

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyemmo.api.json.modelJSON import SurfaceAPI

# from pyemmo.script.geometry.point import Point
from pyemmo.definitions import TEST_DIR
from pyemmo.api.json.modelJSON import createSurfaceDict
from pyemmo.api.pyleecan.translate_surfs import translate_surface
from pyemmo.api.pyleecan.get_rotor_stator_cont import (
    get_even_rotor_cont,
    get_spmsm_rotor_cont,
    get_winding_cont,
)
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


def get_translated_machine(machine: Machine):
    """Local functionto get api geometry list."""
    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []

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
        ) = translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    return geometry_list, machine.rotor.is_internal


def contour_function(get_rotor_cont_function, machine_file):
    """Function to test the the contour identification functions"""
    machine: Machine = load(
        abspath(join(TEST_API_PYLCN_DATA_DIR, machine_file))
    )
    geometry_list, is_internal = get_translated_machine(machine)

    result = get_rotor_cont_function(
        geometry_list=geometry_list,
        machine=machine,
        is_internal_rotor=is_internal,
    )

    # general asserts
    assert result is not None
    assert isinstance(geometry_list, list)
    assert is_internal == machine.rotor.is_internal

    # asserts for spmsm
    # result[0] = rotor_cont_line_list,
    # result[1] = r_point_rotor_cont,
    # result[2] = l_point_rotor_cont
    if isinstance(machine, MachineSIPMSM):
        assert len(geometry_list) == 4
        assert len(result[0]) == 9
        # asserts for r_point_rotor_cont
        assert math.isclose(result[1].coordinate[0], 0.059, abs_tol=1e-6)
        assert math.isclose(result[1].coordinate[1], 0, abs_tol=1e-6)
        assert math.isclose(result[1].coordinate[2], 0, abs_tol=1e-6)
        assert result[1].meshLength == 0.001

        # asserts for l_point_rotor_cont
        assert math.isclose(
            result[2].coordinate[0], 0.047732002668121894, abs_tol=1e-6
        )
        assert math.isclose(
            result[2].coordinate[1], 0.03467932988525591, abs_tol=1e-6
        )
        assert math.isclose(result[2].coordinate[2], 0, abs_tol=1e-6)
        assert result[2].meshLength == 0.001

    # asserts for SyRM
    # result[0] = rotor_cont_line_list,
    # result[1] = r_point_rotor_cont,
    # result[2] = l_point_rotor_cont
    elif isinstance(machine, MachineSyRM):
        assert len(geometry_list) == 6
        # pylint: disable=locally-disabled, comparison-with-callable
        if get_rotor_cont_function == get_even_rotor_cont:
            assert len(result[0]) == 1

            # asserts for r_point_rotor_cont
            assert math.isclose(result[1].coordinate[0], 0.0406, abs_tol=1e-6)
            assert math.isclose(result[1].coordinate[1], 0, abs_tol=1e-6)
            assert math.isclose(result[1].coordinate[2], 0, abs_tol=1e-6)
            assert result[1].meshLength == 0.001

            # asserts for l_point_rotor_cont
            assert math.isclose(
                result[2].coordinate[0], 2.486033002269127e-18, abs_tol=1e-18
            )
            assert math.isclose(result[2].coordinate[1], 0.0406, abs_tol=1e-6)
            assert math.isclose(result[2].coordinate[2], 0, abs_tol=1e-6)
            assert result[2].meshLength == 0.001

        elif get_rotor_cont_function == get_winding_cont:
            assert len(result) == 5


@pytest.mark.parametrize(
    "test_function",
    [
        (
            get_spmsm_rotor_cont,
            "02_spmsm_muster_02.json",
        ),
        (
            get_even_rotor_cont,
            "03_synrm_muster_Bachelor.json",
        ),
        # (
        #     get_winding_cont,
        #     "03_synrm_muster_Bachelor.json",
        # ),
    ],
)
def test_main_functions(test_function):
    """Main function to run different test by pytest parametrize"""
    get_rotor_cont_function, machine_file = test_function
    contour_function(get_rotor_cont_function, machine_file)


def test_winding_contour_function():
    """test for function get_winding_cont() of pyleecan API."""
    machine: Machine = load(
        abspath(join(TEST_DIR, "data", "03_synrm_muster_Bachelor.json"))
    )
    geometry_list, _ = get_translated_machine(machine)
    geo_dict = createSurfaceDict(geometry_list)
    contour_line_list = get_winding_cont(
        lamination_surf=geo_dict["StNut"],
        slot_surfs=[geo_dict["StCu0"]],
        lamination=machine.stator,
    )
    # general asserts
    assert contour_line_list is not None
    assert len(contour_line_list) == 5
    assert all(contour_line_list)  # no None objects


def test_winding_contour_function():
    """test for function get_winding_cont() of pyleecan API."""
    machine: Machine = load(
        abspath(join(TEST_DIR, "data", "03_synrm_muster_Bachelor.json"))
    )
    geometry_list, _ = get_translated_machine(machine)
    geo_dict = createSurfaceDict(geometry_list)
    contour_line_list = get_winding_cont(
        lamination_surf=geo_dict["StNut"],
        slot_surfs=[geo_dict["StCu0"]],
        lamination=machine.stator,
    )
    # general asserts
    assert contour_line_list is not None
    assert len(contour_line_list) == 5
    assert all(contour_line_list)  # no None objects


# if __name__ == "__main__":
#     test_main_functions(
#         (
#             get_winding_cont,
#             "03_synrm_muster_Bachelor.json",
#         )
#     )
# test_winding_contour_function()
