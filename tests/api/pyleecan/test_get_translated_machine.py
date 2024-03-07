import os
import math
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions import load

from pyemmo.definitions import TEST_DIR
import pyemmo.api.pyleecan.get_translated_machine


def test_get_translated_machine():
    # pylint: disable=locally-disabled,  no-member
    machine: Machine = load.load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )

    (
        movingband_r,
        magnetization_dict,
        geo_translation_dict,
    ) = pyemmo.api.pyleecan.get_translated_machine.get_translated_machine(
        machine=machine,
    )
    # check movingband radius
    assert math.isclose(movingband_r, 0.0797, abs_tol=1e-16)
    # check magnetization directions
    assert math.isclose(
        magnetization_dict["Mag0"], 0.5462703245568578, rel_tol=1e-12
    )
    assert math.isclose(
        magnetization_dict["Mag1"], 0.2391278388405909, rel_tol=1e-12
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
        assert key in geo_translation_dict
