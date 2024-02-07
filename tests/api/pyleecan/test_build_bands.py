import os
import math

from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR
import pyemmo.api.pyleecan.translate_surfs
import pyemmo.api.pyleecan.get_magnetization_dict
import pyemmo.api.pyleecan.get_translated_machine
import pyemmo.api.pyleecan.createGeoDict
from pyemmo.api.json.SurfaceJSON import SurfaceAPI


def test_build_bands():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )
    is_internal_rotor = machine.rotor.is_internal
    (
        diff_radius,
        max_radius,
    ) = pyemmo.api.pyleecan.get_translated_machine.calcs_radii(
        machine=machine, is_internal_rotor=is_internal_rotor
    )

    # =================================================================
    # Translation of geometry and creation of rotor and stator contour:
    # =================================================================
    (
        geometry_list,
        rotor_cont_line_list,
        stator_cont_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    ) = pyemmo.api.pyleecan.createGeoDict.create_geo_dict(
        machine,
        is_internal_rotor,
    )

    # ====================================
    # Calculation of the MovingBand radii:
    # ====================================
    number_of_bands = 5
    wp = diff_radius / number_of_bands
    band_radius_list = []

    for i in range(1, number_of_bands + 1):
        band_radius_list.append(max_radius + wp * i)

    (
        rotor_air_gap1,
        rotor_air_gap2,
        movingband_r,
    ) = pyemmo.api.pyleecan.get_translated_machine.build_bands_rotor(
        machine=machine,
        band_radius_list=band_radius_list,
        r_point_rotor_cont=r_point_rotor_cont,
        l_point_rotor_cont=l_point_rotor_cont,
        rotor_cont_line_list=rotor_cont_line_list,
    )
    (
        stator_air_gap1,
        stator_air_gap2,
    ) = pyemmo.api.pyleecan.get_translated_machine.build_bands_stator(
        machine=machine,
        stator_cont_line_list=stator_cont_line_list,
        band_radius_list=band_radius_list,
    )

    all_bands = [
        rotor_air_gap1,
        rotor_air_gap2,
        stator_air_gap1,
        stator_air_gap2,
    ]
    geometry_list.extend(all_bands)

    assert isinstance(all_bands, list)
    assert number_of_bands == 5
    assert len(all_bands) == 4
    assert math.isclose(diff_radius, 0.0005, abs_tol=1e-6)
    assert len(geometry_list) == 12
    assert is_internal_rotor is True
    assert math.isclose(
        magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-6
    )
    assert math.isclose(
        magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-6
    )
    assert math.isclose(max_radius, 0.0795, abs_tol=1e-6)
    assert math.isclose(movingband_r, 0.07970000000000001, abs_tol=1e-6)
    assert rotor_air_gap1.idExt == "LuR1"
    assert len(rotor_air_gap1.curve) == 4
    assert rotor_air_gap2.idExt == "LuR2"
    assert len(rotor_air_gap2.curve) == 4
    assert stator_air_gap1.idExt == "StLu1"
    assert len(stator_air_gap1.curve) == 8
    assert stator_air_gap2.idExt == "StLu2"
    assert len(stator_air_gap2.curve) == 4
    assert len(stator_cont_line_list) == 5
