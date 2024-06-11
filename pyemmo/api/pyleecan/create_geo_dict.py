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
"""Module: pyemmo_create_geo_dict

This module provides functions to convert geometry elements from pyleecan to pyemmo format.

Module dependencies:
    - pyleecan.Classes.MachineIPMSM.MachineIPMSM
    - pyleecan.Classes.MachineSIPMSM.MachineSIPMSM
    - pyleecan.Classes.MachineSyRM.MachineSyRM
    - pyleecan.Classes.Machine.Machine
    - ...functions.plot.plot
    - ...script.geometry.line.Line
    - ...script.geometry.circleArc.CircleArc
    - ...script.geometry.point.Point
    - ..json.SurfaceJSON.SurfaceAPI
    - ..logger

Functions:
    -   ``create_geo_dict``: Creates a dictionary containing geometry
        information for communication between Pyleecan and pyemmo.

Example:

    .. code:: python

        machine = MachineIPMSM(...)
        is_internal_rotor = True
        (
            geometry_list,
            rotor_contour_lines,
            stator_contour_lines,
            r_point_rotor_cont,
            l_point_rotor_cont,
            magnetization_dict
        ) = create_geo_dict(machine, is_internal_rotor)
        # Returns geometry objects, contour lines, and magnetization dictionary suitable for pyemmo.

Raises:
    TypeError: If unable to generate contours of the given machine type.
"""

from typing import List, Union

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.LamSquirrelCage import LamSquirrelCage

from pyleecan.Classes.Machine import Machine as PyleecanMachine

from ...functions.plot import plot
from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from ...script.geometry.point import Point
from ..json.SurfaceJSON import SurfaceAPI
from .. import logger
from ..json.modelJSON import createSurfaceDict
from .translate_surfs import translate_surface
from .get_rotor_stator_cont import (
    get_spmsm_rotor_cont,
    get_winding_cont,
    get_even_rotor_cont,
)
from .calcs_rotor_spmsm_cont import get_lr_points
from .detect_inner_outer_limit import detect_inner_outer_limit
from .get_magnetization_dict import get_magnetization_dict


def create_geo_dict(
    machine: PyleecanMachine,
    is_internal_rotor: bool,
) -> tuple[
    list[SurfaceAPI],
    list[Union[Line, CircleArc]],
    list[Union[Line, CircleArc]],
    Point,
    Point,
    dict,
]:
    """
    Creates a dictionary containing geometry information for communication
    between Pyleecan and pyemmo.

    This function translates the machine geometry into a format suitable for
    communication with pyemmo.
    It generates geometry objects, contour lines, and magnetization dictionaries for the machine.

    Args:
        machine (PyleecanMachine): The machine object to translate into pyemmo-compatible geometry.
        is_internal_rotor (bool): True if the rotor is internal, False otherwise.

    Returns:
        tuple: A tuple containing:
            - list[SurfaceAPI]: List of geometry surfaces.
            - list[Union[Line, CircleArc]]: List of rotor contour lines.
            - list[Union[Line, CircleArc]]: List of stator contour lines.
            - Point: Rightmost point of the rotor contour.
            - Point: Leftmost point of the rotor contour.
            - dict: Dictionary containing magnetization information.
    """
    all_surfaces: list = machine.rotor.build_geometry(
        sym=machine.rotor.comp_periodicity_geo()[0], alpha=0
    )

    all_surfaces.extend(
        machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)
    )

    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []

    logger.debug("Geometry translation started")

    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        logger.debug(
            "Geometry translation of %s started:", all_surfs_labels[i]
        )

        # translating the surface
        pyemmo_surf, angle_point_ref_list = translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    # ===============================
    # Getting the magnetization_dict:
    # ===============================
    magnetization_dict = get_magnetization_dict(
        machine=machine,
        angle_point_ref_list=angle_point_ref_list,
        geometry_list=geometry_list,
    )

    logger.debug("=======================================")
    logger.debug("End of geometry translation of machine.")
    logger.debug("=======================================")

    # plot(geoList=geometry_list, linewidth=1, markersize=3)

    logger.debug("End of geometry translation")
    logger.debug("===========================")

    # --------------------------------------
    # Generate the rotor and stator contour:
    # --------------------------------------
    logger.debug("Generating rotor and stator contour")
    # create dict with idExt as keys and surface items:
    geo_dict = createSurfaceDict(geometry_list)
    if isinstance(machine.rotor, LamHole):
        # CutOuts in rotorLamination if IPMSM or SynRM:
        for surf_to_cutout in geometry_list:
            if surf_to_cutout.name in ("Loch", "Magnet"):
                geometry_list[0].cutOut(surf_to_cutout)
        (
            rotor_contour_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = get_even_rotor_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
    elif isinstance(machine.rotor, LamSlotMag):
        (
            rotor_contour_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = get_spmsm_rotor_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
    elif isinstance(machine.rotor, LamSquirrelCage):
        lam_surf = geo_dict["Pol"]
        slot_surf = geo_dict["RoCu"]
        rotor_contour_line_list = get_winding_cont(
            lamination_surf=lam_surf,
            slot_surfs=[slot_surf],
            lamination=machine.rotor,
            is_internal=not is_internal_rotor,
        )
        l_point_rotor_cont, r_point_rotor_cont = get_lr_points(
            machine,
            rotor_contour_line_list,
            is_internal_rotor,
            radius=(
                machine.rotor.Rint if is_internal_rotor else machine.rotor.Rext
            ),
        )

    else:
        raise TypeError(
            f"Unable to generate contours of rotor lamination type {type(machine.rotor)}!"
        )
    lam_surf = geo_dict["StNut"]
    slot_surfs = [geo_dict["StCu0"]]
    if "StCu1" in geo_dict:
        slot_surfs.append(geo_dict["StCu1"])
    stator_contour_line_list = get_winding_cont(
        lamination_surf=lam_surf,
        slot_surfs=slot_surfs,
        lamination=machine.stator,
        is_internal=is_internal_rotor,
    )

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    has_shaft = bool(machine.rotor.Rint > 0)

    if is_internal_rotor:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.rotor.Rint,
            outer_radius=machine.stator.Rext,
            has_shaft=has_shaft,
        )
    else:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.stator.Rint,
            outer_radius=machine.rotor.Rext,
            has_shaft=has_shaft,
        )

    return (
        geometry_list,
        rotor_contour_line_list,
        stator_contour_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    )
