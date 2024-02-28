"""
Rotor and Stator Contour Calculation Module

This module provides functions to calculate the rotor and stator contours of electric machines.

Functions:
- get_spmsm_rotor_cont: Calculates the rotor contour for Surface Permanent Magnet Synchronous Machine (SPMSM).
- get_even_rotor_cont: Calculates the rotor contour for Interior Permanent Magnet Synchronous Machine (IPMSM) and Synchronous Reluctance Machine (SynRM).
- get_winding_cont: Calculates the stator contour with winding.

Classes:
None

"""

from typing import Union

from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSCIM import MachineSCIM

from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line
from ...script.geometry.point import Point
from .get_rotor_stator_surfs import get_rotor_surfs
from .calcs_rotor_spmsm_cont import calc_spmsm_rotor_cont
from .calcs_even_rotor_cont import calc_even_rotor_cont
from .calc_wind_cont import calc_wind_contour


def get_spmsm_rotor_cont(
    geometry_list: list, machine: Machine, is_internal_rotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """
    Get the list of curves of the contour of the rotor with a surface magnet.

    Args:
        geometry_list (list): List of all surfaces of the machine (Pyemmo format).
        machine (Machine): Pyleecan machine.
        is_internal_rotor (bool, optional): True if the rotor is internal, False otherwise. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: List of rotor contour lines, right point of the rotor contour, and left point of the rotor contour.
    """

    rotor_lam_surf_list, rotor_mag_surf_list = get_rotor_surfs(
        geometry_list=geometry_list
    )

    if is_internal_rotor:
        (
            rotor_cont_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = calc_spmsm_rotor_cont(
            machine=machine,
            rotor_lam_surf_list=rotor_lam_surf_list,
            rotor_mag_surf_list=rotor_mag_surf_list,
            radius=machine.rotor.Rint,
            is_internal_rotor=is_internal_rotor,
        )
    else:
        (
            rotor_cont_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = calc_spmsm_rotor_cont(
            machine=machine,
            rotor_lam_surf_list=rotor_lam_surf_list,
            rotor_mag_surf_list=rotor_mag_surf_list,
            radius=machine.rotor.Rext,
            is_internal_rotor=is_internal_rotor,
        )

    return rotor_cont_line_list, r_point_rotor_cont, l_point_rotor_cont


def get_even_rotor_cont(
    geometry_list: list, machine: Machine, is_internal_rotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """
    Get the list of curves of the contour of the rotor for Interior Permanent Magnet Synchronous Machine (IPMSM) and Synchronous Reluctance Machine (SynRM).

    Args:
        geometry_list (list): List of all surfaces of the machine (Pyemmo format).
        machine (Machine): Pyleecan machine.
        is_internal_rotor (bool, optional): True if the rotor is internal, False otherwise. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: List of rotor contour lines, right point of the rotor contour, and left point of the rotor contour.
    """

    rotor_lam_surf_list = []

    for surf in geometry_list:
        if surf.idExt == "Pol":
            rotor_lam_surf_list.append(surf)

    if is_internal_rotor:
        (
            rotor_cont_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = calc_even_rotor_cont(
            rotor_lam_surf_list=rotor_lam_surf_list,
            radius=machine.rotor.Rint,
        )
    else:
        (
            rotor_cont_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = calc_even_rotor_cont(
            rotor_lam_surf_list=rotor_lam_surf_list,
            radius=machine.rotor.Rext,
        )

    return rotor_cont_line_list, r_point_rotor_cont, l_point_rotor_cont


def get_winding_cont(
    geometry_list: list, machine: Machine, is_internal_rotor: bool
) -> list[Union[Line, CircleArc]]:
    """
    Get the list of curves of the contour of the stator with winding.

    Args:
        geometry_list (list): List of all surfaces of the machine (Pyemmo format).
        machine (Machine): Pyleecan machine.
        is_internal_rotor (bool): True if the rotor is internal, False otherwise.

    Returns:
        list[Union[Line, CircleArc]]: List of stator contour lines.
    """
    stator_rint = machine.stator.Rint
    stator_rext = machine.stator.Rext

    if is_internal_rotor:
        stator_cont_line_list = calc_wind_contour(
            geometry_list=geometry_list,
            stator_rint=stator_rint,
            stator_rext=stator_rext,
        )
    elif isinstance(machine, MachineSCIM):
        pass
    else:
        stator_cont_line_list = calc_wind_contour(
            geometry_list=geometry_list,
            stator_rint=stator_rext,
            stator_rext=stator_rint,
        )

    return stator_cont_line_list
