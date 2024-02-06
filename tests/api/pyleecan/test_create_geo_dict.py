import os
import sys
import logging
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR
import pyemmo.api.pyleecan.createGeoDict


def test_create_geo_dict():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )

    result = pyemmo.api.pyleecan.createGeoDict.create_geo_dict(
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
