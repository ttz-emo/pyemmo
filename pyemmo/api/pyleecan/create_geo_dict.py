"""
translate_geo Module

This module provides functions to translate the geometry of a machine from Pyleecan to pyemmo format.

Functions:
- create_geo_dict: Translates the machine geometry into a format suitable for communication with pyemmo.

Classes:
None

"""

from typing import List, Union

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Machine import Machine

from ...functions.plot import plot
from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from ...script.geometry.point import Point
from ..json.SurfaceJSON import SurfaceAPI
from .. import logger
from .translate_surfs import translate_surface
from .get_rotor_stator_cont import (
    get_spmsm_rotor_cont,
    get_winding_cont,
    get_even_rotor_cont,
)
from .detectInnerOuterLimit import detect_inner_outer_limit
from .get_magnetization_dict import get_magnetization_dict


def create_geo_dict(
    machine: Machine,
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
    Creates a dictionary containing geometry information for communication between Pyleecan and pyemmo.

    This function translates the machine geometry into a format suitable for communication with pyemmo.
    It generates geometry objects, contour lines, and magnetization dictionaries for the machine.

    Args:
        machine (Machine): The machine object to translate into pyemmo-compatible geometry.
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

    plot(geoList=geometry_list, linewidth=1, markersize=3)

    logger.debug("End of geometry translation")
    logger.debug("===========================")

    # --------------------------------------
    # Generate the rotor and stator contour:
    # --------------------------------------
    logger.debug("Generating rotor and stator contour")
    if isinstance(machine, (MachineIPMSM, MachineSIPMSM, MachineSyRM)):
        if isinstance(machine, (MachineIPMSM, MachineSyRM)):
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
        elif isinstance(machine, MachineSIPMSM):
            (
                rotor_contour_line_list,
                r_point_rotor_cont,
                l_point_rotor_cont,
            ) = get_spmsm_rotor_cont(
                geometry_list=geometry_list,
                machine=machine,
                is_internal_rotor=is_internal_rotor,
            )

        stator_contour_line_list = get_winding_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )

    else:
        raise TypeError("Unable to generate contours of this machine type!")

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
