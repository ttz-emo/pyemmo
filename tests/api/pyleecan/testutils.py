#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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

import logging
from os.path import join

import gmsh
import numpy as np
import pytest
from pyleecan.Classes.EEC_PMSM import EEC_PMSM
from pyleecan.Classes.Electrical import Electrical
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.InputVoltage import InputVoltage
from pyleecan.Classes.MagFEMM import MagFEMM
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Output import Output
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


def run_pyleecan_sim_voltage(
    pyleecan_model_file: str,
    speed: float = 1000,
    U_eff: float = 50.0,
    phase: float = 0.0,
    nbr_periods: int = 1,
    nbr_steps_per_period: int = 32,
    nbr_iterations: int = 2,
) -> Output:
    """Run voltage driven Pyleecan simulation with iterative update of Id and Iq to
    calculate the electrical equivalent circuit (EEC) parameters Ld and Lq.
    This is because the voltage source results are calculated with a EEC in Pyleecan,
    where the parameters are calculated from a reference electromagnetic femm simulation.

    Args:
        pyleecan_model_file (str): Path to the Pyleecan machine model file (json) to
            load for the simulation.
        speed (float, optional): Rotor mechanical speed in rpm.. Defaults to 1000.
        U_eff (float, optional): Effective value of source voltage in V. Defaults to
            50.0.
        phase (float, optional): Phase shift of input voltage in electrical degrees.
            Defaults to 0.0.
        nbr_periods (int, optional): Number of stator periods to simulate. Defaults to 1.
        nbr_steps_per_period (int, optional): Number of time steps per stator period.
            Defaults to 32.
        nbr_iterations (int, optional): Number of iterations for the iterative
            simulation to find the actual operating point. Defaults to 2.

    Returns:
        pyleecan.Classes.Output.Output: Pyleecan Simulation Output object. Where the
         results are stored in `Output.elec.eec` property.
    """
    logger = logging.getLogger(__name__)
    # Load the machine
    machine = load(pyleecan_model_file)
    p = machine.stator.winding.p
    Ts = 60 / speed / p  # electrical time period

    # Initialization of the Simulation
    simu_femm = Simu1(
        name="FEMM_simulation",
        machine=machine,
    )
    # Definition of the Electrical Equivalent Circuit
    eec = EEC_PMSM(  # No parameter enforced => compute all
        # Magnetic model to compute fluxlinkage:
        fluxlink=MagFEMM(is_periodicity_a=True, T_mag=20),
    )
    # The Electrical module is defined with the EEC
    simu_femm.elec = Electrical(eec=eec)

    # Only the magnetic module is defined
    simu_femm.mag = None
    simu_femm.force = None
    simu_femm.struct = None
    # run voltage simu
    logger.info(
        "Initializing Pyleecan voltage source simulation with reference current Id=1 A "
        "and Iq=1 A"
    )
    idq = [1.0, 1.0]
    simu_femm.input = InputVoltage(
        OP=OPdq(N0=speed, Id_ref=idq[0], Iq_ref=idq[1], Tem_av_ref=0),
        Na_tot=2048,
        time=np.linspace(
            0, Ts * nbr_periods, num=nbr_periods * nbr_steps_per_period, endpoint=False
        ),  # give time as linspace for more than one period
        is_periodicity_t=True,
        is_periodicity_a=True,
        # Nt_tot=nbr_steps_per_period * p,
    )
    simu_femm.input.OP.set_U0_UPhi0(U_eff * np.sqrt(2), np.deg2rad(phase))
    # Loop simulations until Id_ref and Iq_ref are stable (settled) within 10% tolerance
    # or after 3 iterations
    for iteration in range(1, nbr_iterations + 1):
        out = simu_femm.run()  # run simulation
        logger.info(
            "Iteration %i results: Id_ref=%.2f, Iq_ref=%.2f, Ld=%.2e, Lq=%.2e",
            iteration,
            out.elec.eec.OP.Id_ref,
            out.elec.eec.OP.Iq_ref,
            out.elec.eec.Ld,
            out.elec.eec.Lq,
        )
        if np.isclose(
            [out.elec.eec.OP.Id_ref, out.elec.eec.OP.Iq_ref], idq, rtol=0.1
        ).all():
            logger.info(
                "Simulation settled with Id_ref=%.2f A and Iq_ref=%.2f A after %d "
                "iterations.",
                out.elec.eec.OP.Id_ref,
                out.elec.eec.OP.Iq_ref,
                iteration + 1,
            )
            break
        logger.info(
            "Updating simulation reference currents Id_ref=%.2f and Iq_ref=%.2f and "
            "rerunning simulation.",
            out.elec.eec.OP.Id_ref,
            out.elec.eec.OP.Iq_ref,
        )
        idq = [out.elec.eec.OP.Id_ref, out.elec.eec.OP.Iq_ref]
        simu_femm.input.OP.Id_ref = idq[0]
        simu_femm.input.OP.Iq_ref = idq[1]
    return out


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
