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
""" """
from __future__ import annotations

import logging
from math import pi
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Simulation import Simulation as PyleecanSimulation
from pyleecan.Functions.labels import (
    HOLEM_LAB,
    MAG_LAB,
    decode_label,
    get_obj_from_label,
)

from . import PyleecanMachine
from .label2part_id import label2part_id
from .translate_winding import translate_winding


def create_param_dict(
    machine: PyleecanMachine,
    pyleecan_simulation: PyleecanSimulation,
) -> dict[str, Any]:
    """
    Builds a dictionary for the usage :mod:`pyemmo.api.json` api with all relevant
    machine parameters. See `JSON API parameters <section-pyemmo.api.json-param>`_
    section in documentation for further details.

    Args:
        machine (PyleecanMachine): Pyleecan
            `Machine <https://pyleecan.org/pyleecan.Classes.Machine.html>`_ object.
        pyleecan_simulation (PyleecanSimulation): A Pyleecan
        `Simulation <https://pyleecan.org/pyleecan.Classes.Simulation.html>`_ object.

    Returns:
        dict[str, any]: A dictionary containing the parameters for communication
        with PyEMMO.

    Raises:
        RuntimeError: Raised when encountering errors during execution.
        NotImplementedError: Raised when Hallbach magnetization is defined in pyleecan
            machine because is not implemented in pyemmo.
    """
    logger = logging.getLogger(__name__)
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

    # calculate symmetry factor
    sym_factor, is_antiperiod = machine.comp_periodicity_spatial()
    if is_antiperiod:
        sym_factor = sym_factor * 2
    logger.debug("Symmetry factor machine: %s", {sym_factor})
    swatem_winding = translate_winding(machine)
    sym_winding = swatem_winding.get_periodicity_t() * 2
    logger.debug("Symmetry factor winding: %s", {sym_winding})
    sym_factor = min(sym_winding, sym_factor)

    # -----------------------------------------------------------------------------------
    # If there are magnets, the type of the magnetization type will be safed in
    # 'pyemmoMagType'.
    # 'pyemmoMagType': [0] : parallel
    #                  [1] : radial
    #                  [2] : Hallbach (not implemented in pyemmo -> Error)
    #                  [3] : tangential
    pyemmo_mag_type = None  # If machine doesn't have magnets, pyemmoMagType = None
    # Magnetization dict for json api.
    # It has the magnet part_id as keys and the magnetization angle of the corresponding
    # magnet as value in radians. See `pyemmo.api.json.importJSON.getMagAngle`
    magnetization_dict = {}
    # magnetization workflow from pyleecan.Simulation.MagElmer.solve_FEA
    # NOTE: We need to use rotor symmetry here, because json api exspects one angle per
    # magnet surface in segment dict. See `pyemmo.api.json.importJSON.getMagAngle`
    pyleecan_surf_list = machine.rotor.build_geometry(
        sym=machine.rotor.comp_periodicity_geo()[0]
    )
    for surf in pyleecan_surf_list:
        # label = short_label(surf.label)
        label_dict = decode_label(surf.label)
        if "surf_type" not in label_dict:
            # if there is no surf_type given from label
            continue
        point_ref = surf.point_ref
        if HOLEM_LAB in label_dict["surf_type"]:  # LamHole
            mag_obj = get_obj_from_label(machine, label_dict=label_dict)
            if mag_obj.type_magnetization in [1, None]:  # Parallel
                pyemmo_mag_type = "parallel"
                # calculate pole angle and angle of pole middle
                T_id = label_dict["T_id"]
                hole = mag_obj.parent
                Zh = hole.Zh
                alpha_p = 360 / Zh
                mag_0 = (
                    np.floor_divide(np.angle(point_ref, deg=True), alpha_p) + 0.5
                ) * alpha_p

                mag_dict = hole.comp_magnetization_dict()
                mag = mag_0 + np.rad2deg(mag_dict["magnet_" + str(T_id)])
                # modifiy magnetisation of south poles
                # NOTE: No need to set north/south pole info here. This is done by
                # `pyemmo.api.json.modelJSON.createMagnet`
                # if (label_dict["S_id"] % 2) == 1:
                #     mag = mag + 180
                magnetization_dict[label2part_id(surf.label)] = np.deg2rad(mag)
            else:
                raise RuntimeError(
                    "Only parallel magnetization available for HoleMagnet"
                )
        elif MAG_LAB in label_dict["surf_type"]:
            mag_obj = get_obj_from_label(machine, label_dict=label_dict)
            if mag_obj.type_magnetization == 0 and (label_dict["S_id"] % 2) == 0:
                mag = 0  # North pole magnet
                pyemmo_mag_type = "radial"
            elif mag_obj.type_magnetization == 0:
                mag = 180  # South pole magnet
                pyemmo_mag_type = "radial"
            elif mag_obj.type_magnetization == 1 and (label_dict["S_id"] % 2) == 0:
                mag = np.angle(point_ref) * 180 / pi  # North pole magnet
                pyemmo_mag_type = "parallel"
            elif mag_obj.type_magnetization == 1:
                mag = np.angle(point_ref) * 180 / pi + 180  # South pole magnet
                pyemmo_mag_type = "parallel"
            elif mag_obj.type_magnetization == 2:
                raise NotImplementedError(
                    "Hallbach magnetization not implemented in pyemmo."
                )
                Zs = mag_obj.parent.slot.Zs
                mag = str(-(Zs / 2 - 1)) + " * theta + 90 "
                pyemmo_mag_type = "hallback"
            else:
                continue
            magnetization_dict[label2part_id(surf.label)] = np.deg2rad(mag)
    if magnetization_dict and logger.getEffectiveLevel() <= logging.DEBUG - 1:
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        colors = prop_cycle.by_key()["color"]
        fig, ax = plt.subplots()
        for i, (name, angle) in enumerate(magnetization_dict.items()):

            ax.arrow(
                0,
                0,
                np.cos(angle),
                np.sin(angle),
                head_width=0.2,
                head_length=0.2,
                fc=colors[i],
                # ec="black",
                label=name,
            )
        ax.legend()
        fig.show()

    speed_rpm = pyleecan_simulation.input.OP.N0
    translation_param_dict = {
        "winding": swatem_winding.get_phases(),  # winding layout
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
