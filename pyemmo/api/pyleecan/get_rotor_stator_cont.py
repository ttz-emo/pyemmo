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
"""Rotor and Stator Contour Calculation Module

This module provides functions to calculate the rotor and stator contours of
electric machines.

Functions:
    -   ``get_spmsm_rotor_cont``: Calculates the rotor contour for Surface
        Permanent Magnet Synchronous Machine (SPMSM).
    -   ``get_even_rotor_cont``: Calculates the rotor contour for Interior
        Permanent Magnet Synchronous Machine (IPMSM) and Synchronous Reluctance
        Machine (SynRM).
    -   ``get_winding_cont``: Calculates the stator contour with winding.

"""

from typing import Union, List, Tuple, Dict

from pyleecan.Classes.Machine import Machine as PyleecanMachine
from pyleecan.Classes.MachineSCIM import MachineSCIM
from pyleecan.Classes.LamSlotWind import LamSlot, LamSlotWind

from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line
from ...script.geometry.point import Point
from ...functions.plot import plot
from ..json.SurfaceJSON import SurfaceAPI
from .get_rotor_stator_surfs import get_rotor_surfs
from .calcs_rotor_spmsm_cont import calc_spmsm_rotor_cont
from .calcs_even_rotor_cont import calc_even_rotor_cont
from .calc_wind_cont import calc_wind_contour
from .get_rotor_stator_surfs import get_stator_surfs


def get_spmsm_rotor_cont(
    geometry_list: list,
    machine: PyleecanMachine,
    is_internal_rotor: bool = True,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """
    Get the list of curves of the contour of the rotor with a surface magnet.

    Args:
        geometry_list (list): List of all surfaces of the machine (PyEMMO format).
        machine (PyleecanMachine): Pyleecan Machine object.
        is_internal_rotor (bool, optional): True if the rotor is internal,
            False if not. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: List of rotor contour
        lines, right point of the rotor contour, and left point of the rotor
        contour.
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
    geometry_list: list,
    machine: PyleecanMachine,
    is_internal_rotor: bool = True,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """
    Get the list of curves of the contour of the rotor for Interior Permanent
    Magnet Synchronous Machine (IPMSM) and Synchronous Reluctance Machine (SynRM).

    Args:
        geometry_list (list): List of all surfaces of the machine (PyEMMO format).
        machine (PyleecanMachine): Pyleecan Machine object.
        is_internal_rotor (bool, optional): True if the rotor is internal,
            False otherwise. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: List of rotor contour
        lines, right point of the rotor contour, and left point of the rotor
        contour.
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
    lamination_surf: SurfaceAPI,
    slot_surfs: List[SurfaceAPI],
    lamination: LamSlotWind,
) -> list[Union[Line, CircleArc]]:
    """
    Get the list of curves of the contour of a LamSlotWind object.

    Args:
        geometry_list (list): List of all surfaces of the machine (pyEMMO format).
        lamination (LamSlotWind): LamSlotWind Pyleecan object.
        is_internal (bool): True if the lamination is internal, False otherwise.

    Returns:
        list[Union[Line, CircleArc]]: List of stator contour lines.
    """
    r_int = lamination.Rint
    r_ext = lamination.Rext

    # TODO: Add left and right contour points for airgap surface generation

    cont_line_list = calc_wind_contour(
        lam_surf=lamination_surf,
        slot_surf_list=slot_surfs,
        rint=r_int,
        rext=r_ext,
        is_internal=lamination.is_internal,
    )
    return cont_line_list
