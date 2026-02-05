#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import annotations

from os.path import join

import pytest
import gmsh

from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.MagFEMM import MagFEMM
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Functions.load import load  # pylint: disable=no-name-in-module

from tests.api import TEST_API_DATA_DIR

TEST_API_PYLCN_DATA_DIR = join(TEST_API_DATA_DIR, "pyleecan")


def run_pyleecan_sim(
    pyleecan_model_file: str,
    speed: float = 1000,
    Id: float = 0.0,
    Iq: float = 0.0,
    nbr_steps_per_period: int = 32,
):
    # Load the machine
    machine = load(pyleecan_model_file)
    p = machine.stator.winding.p

    simu_femm = Simu1(
        name="FEMM_simulation",
        machine=machine,
        input=InputCurrent(
            OP=OPdq(N0=speed, Id_ref=Id, Iq_ref=Iq, Tem_av_ref=0),
            Na_tot=2048,
            Nt_tot=nbr_steps_per_period * p,
        ),
    )

    # # time discretization [s]
    # time = linspace(
    #     start=0, stop=60 / speed, num=nbr_steps_per_period * p, endpoint=False
    # )
    # simu_femm.input.time = time
    # # Angular discretization along the airgap circonference for flux density calculation
    # simu_femm.input.angle = linspace(start=0, stop=2 * pi, num=2048, endpoint=False)

    simu_femm.mag = MagFEMM(
        type_BH_stator=0,
        type_BH_rotor=0,
        file_name="",
        is_fast_draw=True,
        is_sliding_band=True,
        is_calc_torque_energy=True,
        T_mag=20,
        is_remove_ventS=False,
        is_remove_ventR=False,
    )

    # Only the magnetic module is defined
    simu_femm.elec = None
    simu_femm.force = None
    simu_femm.struct = None
    simu_femm.mag.is_periodicity_a = True
    simu_femm.mag.is_periodicity_t = True
    return simu_femm.run()


@pytest.fixture(scope="function", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


@pytest.fixture(scope="function")
def Toyota_Prius():
    """Fixture to load machine object for testing

    Stator Type: LamSlotWind
    Slot Type: SlotW11
    Rotor Type: LamHole
    Hole Type: HoleM50
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))


@pytest.fixture(scope="function")
def Toyota_Prius_2():
    """Fixture to load machine object for testing (old pyleecan version 1.3.8)

    Stator Type: LamSlotWind
    Slot Type: SlotW11
    Rotor Type: LamHole
    Hole Type: HoleM50
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))


@pytest.fixture(scope="function")
def SIPMSM_BA():
    """Fixture to load machine object for testing.
    Machine from bachelor thesis of Jan Knoll with 10 Poles, 12 Slots and 6 Axial
    Cooling Ducts on the stator. This results in a different symmetry on the stator than
    the number of slots.

    Stator Type: LamSlotWind
    Slot Type: SlotW22
    Rotor Type: LamSlotMag
    Hole Type: SlotM11
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "02_spmsm_muster_02.json"))


@pytest.fixture(scope="function")
def SYNRM_ZAW():
    """Fixture to load machine object for testing

    Stator Type: LamSlotWind
    Slot Type: SlotW28
    Rotor Type: LamHole
    Hole Type: HoleM54
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "03_synrm_muster_Bachelor_zaw.json"))


@pytest.fixture(scope="function")
def SYNRM_ZWW():
    """Fixture to load machine object for testing

    Stator Type: LamSlotWind
    Slot Type: SlotW28
    Rotor Type: LamHole
    Hole Type: HoleM54
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "03_synrm_muster_Bachelor_zaw.json"))


@pytest.fixture(scope="function")
def IPMSM():
    """Fixture to load machine object for testing

    Stator Type: LamSlotWind
    Slot Type: SlotW11
    Rotor Type: LamHole
    Hole Type: HoleM53
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "IPMSM_B.json"))


@pytest.fixture(scope="function")
def SIPMSM_1():
    """Fixture to load machine object for testing (Pyleecan version 1.2.1)

    Stator Type: LamSlotWind
    Slot Type: SlotW22
    Rotor Type: LamSlotMag
    Hole Type: SlotM11
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "SPMSM_002.json"))


@pytest.fixture(scope="function")
def SIPMSM_2():
    """Fixture to load machine object for testing (Pyleecan version 1.2.1)

    Stator Type: LamSlotWind
    Slot Type: SlotW22
    Rotor Type: LamSlotMag
    Hole Type: SlotM11
    """
    # Create a LamSlot object with some example parameters
    return load(join(TEST_API_PYLCN_DATA_DIR, "SPMSM_003.json"))
