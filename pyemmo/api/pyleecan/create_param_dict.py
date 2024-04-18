#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Lamination import Lamination
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.OPdq import OPdq

from .. import logger
from .translate_winding import translate_winding


def create_param_dict(
    machine: Machine,
    pyleecan_simulation: Simulation,
    mb_radius: float,
    magnetization_dict: dict,
) -> dict[str, any]:
    """This function builds a dictionary for communication between pyleecan and pyemmo.

    Args:
        machine (Machine): machine in pyleecan format
        pyleecanSimulation (Simulation): simulation parameter in pyleecan format
        movingband_r (float): radius of the movingBand
        magnetizationDict (dict): dictionary which contains the magnet with corresponding magnetizationangle

    Raises:
        RuntimeError: _description_

    Returns:
        dict[str, any]: _description_
    """
    # The following part of the function tests if 'Id_ref' and 'Iq_ref' are having values
    # and if so their values will directly be set in the dictionary under 'Id' and 'Iq'.
    # If only 'I0_Phi0' has a set value but 'Id_ref' and 'Iq_ref' don't 'Id' and 'Iq' will be
    # calculated.

    op = pyleecan_simulation.input.OP

    if isinstance(op, OPdq):
        id = op.Id_ref
        iq = op.Iq_ref

    else:
        id = 0
        iq = 0
        logger.warning(
            '!! Warning: No Values set for "Id_ref" and "Iq_ref" -> Id = Iq = 0 !!'
        )

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

    if (
        pyleecan_simulation.machine.rotor.has_magnet()
    ):  # Test, if rotor has magnet(s)
        lam_with_mag = pyleecan_simulation.machine.rotor

    elif (
        pyleecan_simulation.machine.stator.has_magnet()
    ):  # Test, if stator has magnet(s)
        lam_with_mag = pyleecan_simulation.machine.stator

    else:  # If rotor doesn't have magnets, pyemmoMagType = None
        pyemmo_mag_type = None

    if lam_with_mag:
        if isinstance(
            lam_with_mag, LamHole
        ):  # Test, if lamWithMag has Holes where the magnet(s) sit(s) in
            if isinstance(
                lam_with_mag.hole, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmo_mag_type = lam_with_mag.hole[
                    0
                ].magnet_0.type_magnetization

            else:  # If lamWithMag has only one magnet
                pyemmo_mag_type = lam_with_mag.hole.magnet_0.type_magnetization

        elif isinstance(
            lam_with_mag, LamSlotMag
        ):  # Test, if lamWithMag has Slots where the magnet(s) sit(s) in
            if isinstance(
                lam_with_mag.slot, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmo_mag_type = lam_with_mag.slot[
                    0
                ].magnet_0.type_magnetization

            else:  # If rotor has only one magnet
                pyemmo_mag_type = lam_with_mag.magnet.type_magnetization

        else:
            # Error
            raise RuntimeError(
                f'Lamination of type "{str(type(lam_with_mag))}" is not type LamHole or LamSlotMag.'
            )
    if pyemmo_mag_type == 0:
        pyemmo_mag_type = "radial"
    elif pyemmo_mag_type == 1:
        pyemmo_mag_type = "parallel"
    elif pyemmo_mag_type == 3:
        pyemmo_mag_type = "tangential"

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
        "id": id,  # d-axis current in A
        "iq": iq,  # q-axis current in A
        "modelName": machine.name,  # name of the model files
        "magType": pyemmo_mag_type,  # magnetization Type/ type of permament magnets(“parallel”, “radial” or “tangential”)
        "magAngle": magnetization_dict,
        "flag_openGUI": True,  # open Gmsh GUI after model generation (STANDARD = True)
        "calcIronLoss": False,
    }

    return translation_param_dict
