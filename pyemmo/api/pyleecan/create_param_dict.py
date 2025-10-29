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

from statistics import mean
from math import pi
from typing import Any

from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.Lamination import Lamination
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Simulation import Simulation as PyleecanSimulation

from .. import logger
from ..json import ROTOR_MAG_IDEXT
from . import PyleecanMachine
from .translate_winding import translate_winding


def create_param_dict(
    machine: PyleecanMachine,
    pyleecan_simulation: PyleecanSimulation,
) -> dict[str, Any]:
    """
    Builds a dictionary for communication between PYLEECAN, PyEMMO and ONELAB.

    This function constructs a dictionary containing various parameters related
    to the Pyleecan machine and simulation, which are necessary for communication
    with the pyemmo module. The dictionary is needed for setting the simulation
    parameters in ONELAB.

    Args:
        machine (PyleecanMachine): Pyleecan `Machine
            <https://pyleecan.org/pyleecan.Classes.Machine.html>`_ object.
        pyleecan_simulation (PyleecanSimulation): A Pyleecan `Simulation
            <https://pyleecan.org/pyleecan.Classes.Simulation.html>`_ object.
        mb_radius (float): The radius of the moving band.
        magnetization_dict (dict): A dictionary containing the magnet IdExt with
            corresponding magnetization angle.

    Raises:
        RuntimeError: Raised when encountering errors during execution.
        ValueError: Raised when the magnetization type is not 0, 1 or 3

    Returns:
        dict[str, any]: A dictionary containing the parameters for communication
        with PyEMMO.
    """
    # The following part of the function tests if 'Id_ref' and 'Iq_ref' are having values
    # and if so their values will directly be set in the dictionary under 'Id' and 'Iq'.
    # If only 'I0_Phi0' has a set value but 'Id_ref' and 'Iq_ref' don't 'Id' and 'Iq' will be
    # calculated.
    op = pyleecan_simulation.input.OP
    if isinstance(op, OPdq):
        i_d = op.Id_ref
        i_q = op.Iq_ref
    else:
        i_d = 0
        i_q = 0
        logger.warning(
            '!! Warning: No Values set for "Id_ref" and "Iq_ref" -> Id = Iq = 0 !!'
        )

    ## Calculate movingband radius
    # We define movingband radius to be rotor outer radius + 2/5 of the mechanical airgap
    r_ext_rotor = machine.rotor.comp_radius_mec()
    mb_radius = r_ext_rotor + 2 * (machine.stator.comp_radius_mec() - r_ext_rotor) / 5
    # --------------------------------------------------------------------------------------
    # The following part of the function tests if rotor or stator have magnets and if so
    # if there are more than one magnet build in.
    # If there are magnets, the type of the magnetization will be safed in 'pyemmoMagType'.
    # 'pyemmoMagType': [0] : parallel
    #                  [1] : radial
    #                  [2] : Hallbach (!! not implemented in pyemmo !!)
    #                  [3] : tangential
    # If there are no magnets in rotor and stator, 'pyemmoMagType' will be set to 'None'.
    # --------------------------------------------------------------------------------------

    lam_with_mag: Lamination = None
    pylcn_mag_type = None  # If machine doesn't have magnets, pyemmoMagType = None
    # Magnetization dict for pyemmo json api.
    # It has the magnet part_id as keys and the magnetization angle of the corresponding
    # magnet as value in radians. See `pyemmo.api.json.importJSON.getMagAngle`
    magnetization_dict = {}
    if pyleecan_simulation.machine.rotor.has_magnet():
        # Test, if rotor has magnet(s)
        lam_with_mag = pyleecan_simulation.machine.rotor
    elif pyleecan_simulation.machine.stator.has_magnet():
        # Test, if stator has magnet(s)
        lam_with_mag = pyleecan_simulation.machine.stator
    if lam_with_mag:
        nbr_magnets_in_model: float = (
            lam_with_mag.get_magnet_number() / lam_with_mag.get_Zs()
        )
        assert (
            nbr_magnets_in_model.is_integer()
        ), "Uneven number of magnets per segment!"
        if isinstance(lam_with_mag, LamHole):
            # Test, if lamWithMag has Holes where the magnet(s) sit(s) in
            if isinstance(lam_with_mag.hole, list):
                # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.
                pylcn_mag_type = lam_with_mag.hole[0].magnet_0.type_magnetization
                mag_dict = lam_with_mag.hole[0].get_magnet_dict()
                pylcn_magnetization_dict = lam_with_mag.hole[
                    0
                ].comp_magnetization_dict()
                for i in range(int(nbr_magnets_in_model)):
                    # get magnetization angle and add half pole pitch (pi/Zs)
                    magnetization_dict[ROTOR_MAG_IDEXT + f"{i}"] = (
                        pylcn_magnetization_dict[f"magnet_{i}"]
                        + pi / lam_with_mag.get_Zs()
                    )
            else:  # If lamWithMag has only one magnet
                pylcn_mag_type = lam_with_mag.hole.magnet_0.type_magnetization

        elif isinstance(lam_with_mag, LamSlotMag):
            # Test, if lamWithMag has Slots where the magnet(s) sit(s) in
            if isinstance(lam_with_mag.slot, list):
                # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.
                pylcn_mag_type = lam_with_mag.slot[0].magnet_0.type_magnetization
            else:  # If rotor has only one magnet
                pylcn_mag_type = lam_with_mag.magnet.type_magnetization
        else:
            raise RuntimeError(
                f'Lamination of type "{str(type(lam_with_mag))}" is not type LamHole or LamSlotMag.'
            )
    if pylcn_mag_type == 0:
        pyemmo_mag_type = "radial"
    elif pylcn_mag_type == 1:
        pyemmo_mag_type = "parallel"
    elif pylcn_mag_type == 3:
        pyemmo_mag_type = "tangential"
    else:
        raise ValueError(
            "Unknown pyleecan magnetization type with index: %i", pylcn_mag_type
        )

    sym_factor = machine.comp_periodicity_spatial()
    if sym_factor[1]:
        sym_factor = sym_factor[0] * 2
    else:
        sym_factor = sym_factor[0]
    logger.debug("Symmetry factor machine: %s", {sym_factor})
    swatem_winding, wind_layout = translate_winding(machine)
    sym_winding = swatem_winding.get_periodicity_t() * 2
    logger.debug("Symmetry factor winding: %s", {sym_winding})
    sym_factor = min(sym_winding, sym_factor)

    speed_rpm = pyleecan_simulation.input.OP.N0
    translation_param_dict = {
        "winding": wind_layout,  # winding layout
        # "wickSWAT": translateWinding(machine),
        "NpP": machine.stator.winding.Npcp,  # number of parallel paths per winding phase
        "Ntps": machine.stator.winding.Ntcoil,
        "z_pp": machine.stator.winding.p,  # number of pole pairs
        "Qs": machine.stator.slot.Zs,  # number of stator slots
        "movingband_r": mb_radius,  # moving band radius in meters
        "axLen_S": machine.stator.L1,  # axial length of stator
        "axLen_R": machine.rotor.L1,  # axial length of rotor
        "useFunctionMesh": True,  # use automatic mesh size generation
        "symFactor": sym_factor,  # symmetry factor for model (STANDARD = 1) has to be defined
        "startPos": 0,  # start rotor position in ° (STANDARD = 0°)
        "endPos": pyleecan_simulation.input.time.value[-1]
        * speed_rpm
        / 60
        * 360,  # end position in °
        "nbrSteps": pyleecan_simulation.input.time.value.size,  # number of time steps for simulation
        "rot_freq": speed_rpm / 60,  # mech freq in Hz
        "parkAngleOffset": None,  # park transformation offset angle in elec. ° (STANDARD = None)
        "analysisType": 0,  # 0=static; 1=transient (STANDARD = 1)
        "tempMag": 20,  # magnet temperature °C (STANDARD = 20°C)
        "r_z": 0.7,  # tooth radius in meterm (STANDARD = None)
        "r_j": 0.9,  # yoke radius in meter (STANDARD = None)
        "id": i_d,  # d-axis current in A
        "iq": i_q,  # q-axis current in A
        "modelName": machine.name,  # name of the model files
        "magType": pyemmo_mag_type,  # magnetization Type/ type of permament magnets(“parallel”, “radial” or “tangential”)
        "magAngle": magnetization_dict,
        "flag_openGUI": True,  # open Gmsh GUI after model generation (STANDARD = True)
        "calcIronLoss": False,
    }

    return translation_param_dict
