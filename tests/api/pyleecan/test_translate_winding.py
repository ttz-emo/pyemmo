import os
import sys
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
from pyemmo.definitions import TEST_DIR


def test_translate_winding_single_layer():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "03_synrm_muster_Bachelor.json")
        )
    )


def test_translate_winding_tooth_coil():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "03_synrm_muster_Bachelor_zaw.json")
        )
    )


def test_translate_winding_two_layer():
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "03_synrm_muster_Bachelor_zww.json")
        )
    )
