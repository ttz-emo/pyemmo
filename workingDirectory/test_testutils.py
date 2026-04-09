# %%
from __future__ import annotations

import logging
from os.path import join, normpath
from pprint import pformat
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

phase = {}

for ps in range(190, 230, 5):
    out = run_pyleecan_sim_voltage(
        test_file,
        speed=speed,
        U_eff=63 / 1000 * speed,
        phase=ps,
        nbr_periods=1,
        nbr_steps_per_period=8,
        nbr_iterations=1,
    )

    # %
    res: OutElec = out.elec
    # pprint(res.as_dict())
    print("Operating point:")
    print(f"Id = {res.OP.Id_ref:.2f} A, Iq = {res.OP.Iq_ref:.2f} A")
    print(f"Ud = {res.OP.Ud_ref:.2f} V, Uq = {res.OP.Uq_ref:.2f} V")
    print(f"Tem = {res.Tem_av:.2f} Nm")
    phase[ps] = {
        "torque": res.Tem_av,
        "id": res.OP.Id_ref,
        "iq": res.OP.Iq_ref,
        "ud": res.OP.Ud_ref,
        "uq": res.OP.Uq_ref,
    }

# %%
from matplotlib import pyplot as plt

# plot torque vs phase
fig, ax = plt.subplots()
phases = list(phase.keys())
torques = [phase[ps]["torque"] for ps in phases]
ax.plot(phases, torques, marker="o")
ax.set_xlabel("Phase offset in deg elec.")
ax.set_ylabel("Torque (Nm)")
ax.set_title("Torque vs Phase Offset")
plt.show()

# %%
