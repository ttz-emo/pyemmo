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
"""Module: pyemmo_create_geo_dict

This module provides functions to convert geometry elements from pyleecan to pyemmo format.

Functions:
    -   ``create_geo_dict``: Creates a dictionary containing geometry
        information for communication between Pyleecan and pyemmo.

Example:

    .. code:: python

        machine = MachineIPMSM(...)
        geometry_dict = create_geo_dict(machine)
        # Returns geometry objects suitable for pyemmo.

Raises:
    TypeError: If unable to generate contours of the given machine type.
"""

from __future__ import annotations

from pyleecan.Classes.LamH import LamH
from pyleecan.Classes.LamSlot import LamSlot
from pyleecan.Classes.SurfLine import SurfLine
from pyleecan.Functions.labels import (
    BAR_LAB,
    HOLEM_LAB,
    HOLEV_LAB,
    WIND_LAB,
    get_obj_from_label,
)

from .. import logger
from ..machine_segment_surface import MachineSegmentSurface
from . import PyleecanMachine
from .build_pyemmo_material import build_pyemmo_material
from .create_gmsh_surf import create_gmsh_surface


def create_geo_dict(
    machine: PyleecanMachine,
) -> dict[str, MachineSegmentSurface]:
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

    rotor_surfs: list[SurfLine] = machine.rotor.build_geometry(  # type: ignore
        sym=machine.rotor.comp_periodicity_geo()[0], alpha=0  # type: ignore
    )
    # is_internal_rotor = machine.rotor.is_internal  # type: ignore

    stator_surfs: list[SurfLine] = machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)  # type: ignore

    # all_surfs_labels = []
    # all_surfs_labels_split2 = []
    pyemmo_geo_dict: dict[str, MachineSegmentSurface] = {}
    angle_point_ref_list = []
    logger.debug("Geometry translation started")
    logger.debug("Identifying geometries by surface label:")
    for lam, pyleecan_surfs in (
        (machine.rotor, rotor_surfs),
        (machine.stator, stator_surfs),
    ):
        assert isinstance(lam, (LamH, LamSlot)), "lam is not type LamHole or LamSlot!"
        # create lamination surface separatly for subtraction
        lam_surf = create_gmsh_surface(
            pyleecan_surfs.pop(0), lam.get_Zs(), build_pyemmo_material(lam.mat_type)
        )
        pyemmo_geo_dict[lam_surf.part_id] = lam_surf
        for surf in pyleecan_surfs:
            # save_space_temp = []
            # all_surfs_labels_split1 = []
            # all_surfs_labels.append(surf.label)
            # all_surfs_labels_split1.extend(surf.label.split("_"))  # type: ignore

            # for split1 in all_surfs_labels_split1:
            #     save_space_temp.extend(split1.split("-"))
            # all_surfs_labels_split2.append(save_space_temp)

            # lam = machine.get_lam_by_label(all_surfs_labels_split1[0])
            obj = get_obj_from_label(machine, surf.label)
            if WIND_LAB in surf.label or BAR_LAB in surf.label:
                # NOTE: In case of winding or bar label the object returned is the
                # lamination and not the actual object itself. If so we have to get the
                # actual conductor material.
                material = obj.winding.conductor.cond_mat
            elif hasattr(obj, "mat_type"):
                material = obj.mat_type
            elif hasattr(obj, "mat_void"):
                material = obj.mat_void
            else:
                raise AttributeError(f"Cant get material from object {obj}")
            # translating the surface
            pyemmo_surf = create_gmsh_surface(
                surface=surf,
                nbr_segments=lam.get_Zs(),
                material=build_pyemmo_material(material),  # type:ignore
            )
            if HOLEM_LAB in surf.label or HOLEV_LAB in surf.label:
                lam_surf.cutOut(pyemmo_surf)
            pyemmo_geo_dict[pyemmo_surf.part_id] = pyemmo_surf

    # # ===============================
    # # Getting the magnetization_dict:
    # # ===============================
    # magnetization_dict = get_magnetization_dict(
    #     machine=machine,
    #     angle_point_ref_list=angle_point_ref_list,
    #     geometry_list=pyemmo_geo_dict,
    # )

    logger.debug("=======================================")
    logger.debug("End of geometry translation of machine.")
    logger.debug("=======================================")

    # plot(geoList=geometry_list, linewidth=1, markersize=3)

    logger.debug("End of geometry translation")
    logger.debug("===========================")

    # --------------------------------------
    # Generate the rotor and stator contour:
    # --------------------------------------
    # logger.debug("Generating rotor and stator contour")
    #     (
    #         rotor_contour_line_list,
    #         r_point_rotor_cont,
    #         l_point_rotor_cont,
    #     ) = get_even_rotor_cont(
    #         geometry_list=pyemmo_geo_dict,
    #         machine=machine,
    #         is_internal_rotor=is_internal_rotor,
    #     )
    # elif isinstance(machine.rotor, LamSlotMag):
    #     (
    #         rotor_contour_line_list,
    #         r_point_rotor_cont,
    #         l_point_rotor_cont,
    #     ) = get_spmsm_rotor_cont(
    #         geometry_list=pyemmo_geo_dict,
    #         machine=machine,
    #         is_internal_rotor=is_internal_rotor,
    #     )
    # elif isinstance(machine.rotor, LamSquirrelCage):
    #     lam_surf = pyemmo_geo_dict[ROTOR_LAM_IDEXT]
    #     slot_surf = pyemmo_geo_dict[ROTOR_BAR_IDEXT]
    #     rotor_contour_line_list = get_winding_cont(
    #         lamination_surf=lam_surf,
    #         slot_surfs=[slot_surf],
    #         lamination=machine.rotor,
    #     )
    #     l_point_rotor_cont, r_point_rotor_cont = get_lr_points(
    #         machine,
    #         rotor_contour_line_list,
    #         is_internal_rotor,
    #         radius=(machine.rotor.Rint if is_internal_rotor else machine.rotor.Rext),
    #     )

    # else:
    #     raise TypeError(
    #         f"Unable to generate contours of rotor lamination type {type(machine.rotor)}!"
    #     )
    # lam_surf = pyemmo_geo_dict[STATOR_LAM_IDEXT]
    # slot_surfs = [pyemmo_geo_dict[STATOR_SLOT_IDEXT]]
    # if (STATOR_SLOT_IDEXT + "1") in pyemmo_geo_dict:
    #     slot_surfs.append(pyemmo_geo_dict[STATOR_SLOT_IDEXT + "1"])
    # stator_contour_line_list = get_winding_cont(
    #     lamination_surf=lam_surf,
    #     slot_surfs=slot_surfs,
    #     lamination=machine.stator,
    # )

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    # has_shaft = bool(machine.rotor.Rint > 0)

    # if is_internal_rotor:
    #     pyemmo_geo_dict = detect_inner_outer_limit(
    #         geometry_list=pyemmo_geo_dict,
    #         inner_radius=machine.rotor.Rint,
    #         outer_radius=machine.stator.Rext,
    #         has_shaft=has_shaft,
    #     )
    # else:
    #     pyemmo_geo_dict = detect_inner_outer_limit(
    #         geometry_list=pyemmo_geo_dict,
    #         inner_radius=machine.stator.Rint,
    #         outer_radius=machine.rotor.Rext,
    #         has_shaft=has_shaft,
    #     )

    return pyemmo_geo_dict
