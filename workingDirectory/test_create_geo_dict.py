import os
import sys
import logging
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
import workingDirectory.createGeoDict


def test_create_geo_dict():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )

    result = workingDirectory.createGeoDict.create_geo_dict(
        machine, machine.rotor.is_internal
    )

    logging.debug("------------------------------")
    logging.debug("Plot geometry_list:")
    plot(result[0])
    logging.debug("------------------------------")
    logging.debug("Plot rotor_contour_line_list:")
    plot(result[1], tag=True)
    logging.debug("------------------------------")
    logging.debug("Plot stator_contour_line_list:")
    plot(result[2], tag=True)
    logging.debug("------------------------------")
    logging.debug("magnetization_dict:")
    logging.debug(result[5])
    logging.debug("------------------------------")


test_create_geo_dict()
