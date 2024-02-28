import os
import pytest
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

from pyemmo.api.pyleecan.translate_winding import translate_winding
from pyemmo.definitions import TEST_DIR


@pytest.mark.parametrize(
    "machine_sample",
    [
        "03_synrm_muster_Bachelor.json",
        "03_synrm_muster_Bachelor_zaw.json",
        "03_synrm_muster_Bachelor_zww.json",
    ],
)
def test_translate_winding(machine_sample):
    machine: Machine = load(
        os.path.abspath(os.path.join(TEST_DIR, "data", machine_sample))
    )
    _, wind_swat = translate_winding(machine)

    if machine_sample == "03_synrm_muster_Bachelor.json":
        assert wind_swat[0] == [[1, 2, -7, -8, 13, 14, -19, -20], []]
        assert wind_swat[1] == [[5, 6, -11, -12, 17, 18, -23, -24], []]
        assert wind_swat[2] == [[-3, -4, 9, 10, -15, -16, 21, 22], []]

    elif machine_sample == "03_synrm_muster_Bachelor_zaw.json":
        assert wind_swat[0] == [
            [1, 2, -7, -8, 13, 14, -19, -20],
            [-7, -8, 13, 14, -19, -20, 1, 2],
        ]
        assert wind_swat[1] == [
            [5, 6, -11, -12, 17, 18, -23, -24],
            [-11, -12, 17, 18, -23, -24, 5, 6],
        ]
        assert wind_swat[2] == [
            [-3, -4, 9, 10, -15, -16, 21, 22],
            [9, 10, -15, -16, 21, 22, -3, -4],
        ]

    elif machine_sample == "03_synrm_muster_Bachelor_zww.json":
        assert wind_swat[0] == [
            [1, 2, -7, -8, 13, 14, -19, -20],
            [-5, -6, 11, 12, -17, -18, 23, 24],
        ]
        assert wind_swat[1] == [
            [5, 6, -11, -12, 17, 18, -23, -24],
            [-9, -10, 15, 16, -21, -22, 3, 4],
        ]
        assert wind_swat[2] == [
            [-3, -4, 9, 10, -15, -16, 21, 22],
            [7, 8, -13, -14, 19, 20, -1, -2],
        ]
