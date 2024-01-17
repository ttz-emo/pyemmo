from typing import Union

from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSCIM import MachineSCIM

from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from .getRotorStatorSurfaces import getRotorSurfaces
from .calcsSPMSMContour import calc_spmsm_rotor_cont
from .calcIPMSMContour import calc_even_rotor_cont
from .calcWindContour import calcWindContour


def get_spmsm_rotor_cont(
    geometry_list: list, machine: Machine, is_internal_rotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Get a list of curves of the contour of the rotor with a surfacemagnet.

    Args:
        geometry_list (list): List with all surfaces of the machine (Pyemmo format)
        machine (Machine): Pyleecan machine
        is_internal_rotor (bool, optional): Internal or external Rotor. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: _description_
    """

    rotor_lam_surf_list, rotor_mag_surf_list = getRotorSurfaces(
        geometryList=geometry_list
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
    """Get a list of curves of the contour of the rotor.
    machine types: IPMSM, SynRM

    Args:
        geometry_list (list): List with all surfaces of the machine (Pyemmo format)
        machine (Machine): Pyleecan machine
        is_internal_rotor (bool, optional): Internal or external Rotor. Defaults to True.

    Returns:
        list[Line, CircleArc]: _description_
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
    """Get a list of curves of the contour of the lamination with a winding.

    Args:
        geometryList (list): _description_
        machine (Machine): _description_
        isInternalRotor (bool): _description_

    Returns:
        list[Union[Line, CircleArc]]: _description_
    """
    stator_rint = machine.stator.Rint
    stator_rext = machine.stator.Rext

    if is_internal_rotor:
        stator_cont_line_list = calcWindContour(
            geometryList=geometry_list,
            statorRint=stator_rint,
            statorRext=stator_rext,
        )
    elif isinstance(machine, MachineSCIM):
        pass
    else:
        stator_cont_line_list = calcWindContour(
            geometryList=geometry_list,
            statorRint=stator_rext,
            statorRext=stator_rint,
        )

    return stator_cont_line_list
