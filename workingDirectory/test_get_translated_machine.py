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
import workingDirectory.get_translated_machine


def test_get_translated_machine():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )

    (
        all_bands,
        geometry_list,
        movingband_r,
        magnetization_dict,
        geo_translation_dict,
    ) = workingDirectory.get_translated_machine.get_translated_machine(
        machine=machine,
        is_internal_rotor=machine.rotor.is_internal,
    )

    logging.debug("-------------------")
    logging.debug("Plot geometry_list:")
    plot(
        geometry_list,
    )
    logging.debug("------------------------------")
    logging.debug("Plot all_bands:")
    plot(all_bands)
    logging.debug("------------------------------")
    logging.debug("movingband_r:")
    logging.debug(movingband_r)
    logging.debug("------------------------------")
    logging.debug("magnetization_dict:")
    logging.debug(magnetization_dict)
    logging.debug("------------------------------")
    logging.debug("geo_translation_dict:")
    logging.debug(geo_translation_dict)
    logging.debug("------------------------------")


test_get_translated_machine()
