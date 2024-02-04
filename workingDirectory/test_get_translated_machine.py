import os
import sys
import logging
import math
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
    )

    assert len(all_bands) == 4  # make sure there are 4 movingband objects
    assert len(geometry_list) == 12  # make sure the are 12 surfaces
    # check movingband radius
    assert math.isclose(movingband_r, 0.0797, abs_tol=1e-16)
    # check magnetization directions
    assert math.isclose(
        magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-3
    )
    assert math.isclose(
        magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-3
    )
    for key in (
        "Pol",
        "Lpl0",
        "Mag0",
        "Lpl1",
        "Mag1",
        "Lpl2",
        "StNut",
        "StCu0",
        "LuR1",
        "LuR2",
        "StLu1",
        "StLu2",
    ):
        assert key in geo_translation_dict.keys()

    # logging.debug("-------------------")
    # logging.debug("Plot geometry_list:")
    # plot(geometry_list)
    # logging.debug("------------------------------")
    # logging.debug("Plot all_bands:")
    # plot(all_bands)
    # logging.debug("------------------------------")
    # logging.debug("movingband_r:")
    # logging.debug(movingband_r)
    # logging.debug("------------------------------")
    # logging.debug("magnetization_dict:")
    # logging.debug(magnetization_dict)
    # logging.debug("------------------------------")
    # logging.debug("geo_translation_dict:")
    # logging.debug(geo_translation_dict)
    # logging.debug("------------------------------")


test_get_translated_machine()
