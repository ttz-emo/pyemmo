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
"""Magnetization Dictionary Generation Module.

This module provides a function to generate a dictionary containing magnetization
information for magnets in a given machine geometry. The dictionary includes the
magnet identifier ('Mag0', 'Mag1', ...), and the corresponding magnetization angle.

Module dependencies:
    - numpy.pi
    - pyleecan.Classes.MachineSIPMSM
    - pyleecan.Classes.MachineIPMSM
    - pyleecan.Classes.Machine
    - pyemmo.api.SurfaceJSON.SurfaceAPI

Functions:
    - ``get_magnetization_dict``: Return magnetization info of magnets in model.

Example:
    .. code:: python

        machine = MachineSIPMSM(...)
        angle_point_ref_list = [30, 60]
        geometry_list = [SurfaceAPI(...), SurfaceAPI(...), ...]

        magnetization_dict = get_magnetization_dict(
            machine,
            angle_point_ref_list,
            geometry_list
        )

    .. note::
        This function generates a magnetization dictionary for the specified
        machine geometry, supporting both SIPMSM and IPMSM.

"""

from __future__ import annotations

from numpy import pi
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineIPMSM import MachineIPMSM

# from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.Magnet import Magnet

from ..json import ROTOR_MAG_IDEXT
from ..machine_segment_surface import MachineSegmentSurface
from . import POLE_HOLE_IDEXT


def get_magnetization_dict(
    machine: Machine,
    angle_point_ref_list: list[float],
    geometry_list: list[MachineSegmentSurface],
) -> dict:
    """Generate a dictionary mapping magnets to their respective magnetization
    angles.

    This function calculates and returns a dictionary containing information about
    the magnetization of magnets in the specified machine geometry. The resulting
    dictionary includes the magnet identifier ('Mag0', 'Mag1', ...), and the
    corresponding magnetization angle.

    Args:
        machine (Machine): The machine object representing the geometry.
        angle_point_ref_list (list[float]): List of angle values corresponding
            to reference points for magnetization.
        geometry_list (list[SurfaceAPI]): List of surface geometry elements.

    Returns:
        dict: A dictionary containing magnetization information for each magnet
        in the geometry.

    Raises:
        ValueError: If the magnetization type is unsupported.

    Note:
        The function supports both SIPMSM and IPMSM.

    Example:
        .. code:: python

            machine = MachineSIPMSM(...)
            angle_point_ref_list = [30, 60]
            geometry_list = [SurfaceAPI(...), SurfaceAPI(...), ...]
            magnetization_dict = get_magnetization_dict(
                machine,
                angle_point_ref_list,
                geometry_list
            )
    """
    # TODO: This function works for specific cases but does only catch a few errors and
    # is very specific to the currently tested models...

    # Filling the magnetization dict if surface is magnet:
    magnetization_dict = {}

    # Changing the 'part_id' of the SurfaceAPI to 'Mag0', 'Mag1', 'Mag2', ...
    # if the 'part_id' is 'Mag'
    hole_counter = 0
    mag_counter = 0

    for surf_api in geometry_list:
        if surf_api.part_id == POLE_HOLE_IDEXT:
            surf_api.part_id = POLE_HOLE_IDEXT + str(hole_counter)
            hole_counter += 1

    for mag_surf in [surf for surf in geometry_list if surf.part_id == ROTOR_MAG_IDEXT]:
        mag_surf.part_id = ROTOR_MAG_IDEXT + str(mag_counter)
        mag_counter += 1

    if isinstance(machine, MachineSIPMSM):
        angle_point_ref = angle_point_ref_list[0]
        rotor: LamSlotMag = machine.rotor
        magnet: Magnet = rotor.magnet
        magnetization_type = magnet.type_magnetization

        if len(angle_point_ref_list) == 1:
            # only one magnet per pole
            if magnetization_type in (0, 1):  # radial & parallel
                magnetization_angle = angle_point_ref

            elif magnetization_type == 3:  # tangential
                magnetization_angle = angle_point_ref - 90 / pi
            else:
                raise ValueError(
                    f"Unknown magnetization type with index {magnetization_type}. "
                    "Valid indices are 0, 1 and 2!"
                )
            magnetization_dict[ROTOR_MAG_IDEXT + "0"] = magnetization_angle

        else:
            # multiple magnets per pole
            for mag_surf in [
                surf for surf in geometry_list if ROTOR_MAG_IDEXT in surf.part_id
            ]:
                if "0" in mag_surf.name:
                    if magnetization_type in (0, 1):  # radial & parallel
                        magnetization_angle = angle_point_ref_list[0]

                    elif magnetization_type == 3:  # tangential
                        magnetization_angle = angle_point_ref_list[0] - 90 / pi
                    magnetization_dict[ROTOR_MAG_IDEXT + "0"] = magnetization_angle

                elif "1" in mag_surf.name:
                    if magnetization_type in (0, 1):  # radial & parallel
                        magnetization_angle = angle_point_ref_list[1]

                    elif magnetization_type == 3:  # tangential
                        magnetization_angle = angle_point_ref_list[1] - 90 / pi
                    magnetization_dict[ROTOR_MAG_IDEXT + "1"] = -magnetization_angle
                else:
                    raise RuntimeError(
                        f"Magnet surface (part_id:{mag_surf.part_id}) '{mag_surf.name}' is "
                        "not index 0 or 1!"
                    )

    elif isinstance(machine, MachineIPMSM):
        mag_angle_dict = machine.rotor.hole[0].comp_magnetization_dict()
        if len(mag_angle_dict) == 1:
            angle_point_ref = angle_point_ref_list[0]
            magnetization_type = machine.rotor.hole[0].magnet_0.type_magnetization

            if magnetization_type in (0, 1):  # radial & parallel
                magnetization_angle = angle_point_ref

            elif magnetization_type == 3:  # tangential
                magnetization_angle = angle_point_ref - 90 / pi

            magnetization_dict[ROTOR_MAG_IDEXT + "0"] = magnetization_angle
        else:
            for mag_surf in geometry_list:
                if mag_surf.part_id == ROTOR_MAG_IDEXT + "0":
                    magnetization_angle = (
                        angle_point_ref_list[0] + mag_angle_dict["magnet_0"]
                    )
                    magnetization_dict[mag_surf.part_id] = magnetization_angle

                elif mag_surf.part_id == ROTOR_MAG_IDEXT + "1":
                    magnetization_angle = (
                        angle_point_ref_list[1] + mag_angle_dict["magnet_1"]
                    )
                    magnetization_dict[mag_surf.part_id] = magnetization_angle

                elif mag_surf.part_id == ROTOR_MAG_IDEXT + "2":
                    magnetization_angle = (
                        angle_point_ref_list[2] + mag_angle_dict["magnet_2"]
                    )
                    magnetization_dict[mag_surf.part_id] = magnetization_angle

    return magnetization_dict
