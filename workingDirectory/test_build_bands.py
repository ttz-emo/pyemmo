import sys
import os
import logging
from typing import List

from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    # sys.path.append("C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo\\tests")

from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR
from pyemmo.api.modelJSON import SurfaceAPI
import workingDirectory.translate_surfs
import workingDirectory.get_magnetization_dict
import workingDirectory.get_translated_machine
import workingDirectory.createGeoDict


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
    ) = workingDirectory.get_translated_machine.calcs_radii(
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
    ) = workingDirectory.createGeoDict.create_geo_dict(
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
    ) = workingDirectory.get_translated_machine.build_bands_rotor(
        machine=machine,
        band_radius_list=band_radius_list,
        r_point_rotor_cont=r_point_rotor_cont,
        l_point_rotor_cont=l_point_rotor_cont,
        rotor_cont_line_list=rotor_cont_line_list,
    )
    (
        stator_air_gap1,
        stator_air_gap2,
    ) = workingDirectory.get_translated_machine.build_bands_stator(
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
    logging.debug("-------------------")
    logging.debug("Plot all_bands:")
    plot(all_bands)
    logging.debug("-------------------")
    logging.debug("Plot geometry_list:")
    plot(geometry_list)
    logging.debug("-------------------")

test_build_bands()