# %%
from __future__ import annotations

import logging
from os.path import join, normpath
from pprint import pformat, pprint
from sys import path

from pyleecan.Classes.OutElec import OutElec

from pyemmo.definitions import ROOT_DIR

logging.basicConfig(level=logging.INFO)

if normpath(ROOT_DIR) in [normpath(p) for p in path]:
    path.remove(normpath(ROOT_DIR))
path.insert(0, normpath(ROOT_DIR))
logging.info("Updated Python path: %s", pformat(path))

# Import from tests after updating path
# pylint: disable=wrong-import-position
from tests import TEST_DATA_DIR
from tests.api.pyleecan.testutils import run_pyleecan_sim_voltage

test_file = join(TEST_DATA_DIR, "api", "pyleecan", "Toyota_Prius.json")
speed = 1000

out = run_pyleecan_sim_voltage(
    test_file,
    speed=speed,
    U_eff=63 / 1000 * speed,
    phase=90,
    nbr_periods=1,
    nbr_steps_per_period=8,
    nbr_iterations=2,
)

# %%
res: OutElec = out.elec
pprint(res.as_dict())

# %%
