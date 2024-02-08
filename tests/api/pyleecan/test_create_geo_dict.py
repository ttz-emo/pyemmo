import os
import math
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

from pyemmo.definitions import TEST_DIR
import pyemmo.api.pyleecan.createGeoDict


def test_create_geo_dict():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )

    (
        geometry_list,
        rotor_contour_line_list,
        stator_contour_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    ) = pyemmo.api.pyleecan.createGeoDict.create_geo_dict(
        machine, machine.rotor.is_internal
    )
    # assert for geometry_list
    assert len(geometry_list) == 8

    # asserts for rotor_contour_line_list
    assert len(rotor_contour_line_list) == 1

    # assert for stator_contour_line_list
    assert len(stator_contour_line_list) == 5

    # asserts for r_point_rotor_cont
    assert math.isclose(r_point_rotor_cont.coordinate[0], 0.0795, abs_tol=1e-6)
    assert math.isclose(r_point_rotor_cont.coordinate[1], 0, abs_tol=1e-6)
    assert math.isclose(r_point_rotor_cont.coordinate[2], 0, abs_tol=1e-6)
    assert r_point_rotor_cont.meshLength == 0.001

    # asserts for l_point_rotor_cont
    assert math.isclose(
        l_point_rotor_cont.coordinate[0], 0.05621498910433053, abs_tol=1e-6
    )
    assert math.isclose(
        l_point_rotor_cont.coordinate[1], 0.05621498910433053, abs_tol=1e-6
    )
    assert math.isclose(l_point_rotor_cont.coordinate[2], 0, abs_tol=1e-6)
    assert l_point_rotor_cont.meshLength == 0.001

    # asserts magnetization_dict
    assert math.isclose(
        magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-12
    )
    assert math.isclose(
        magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-12
    )
