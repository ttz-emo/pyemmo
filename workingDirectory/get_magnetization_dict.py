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
    - get_magnetization_dict(
        machine: Machine,
        angle_point_ref_list: list[float],
        geometry_list: list[SurfaceAPI]
    ) -> dict

Example:
    machine = MachineSIPMSM(...)
    angle_point_ref_list = [30, 60]
    geometry_list = [SurfaceAPI(...), SurfaceAPI(...), ...]
    
    magnetization_dict = get_magnetization_dict(machine, angle_point_ref_list, geometry_list)

    Note: This function generates a magnetization dictionary for the specified 
    machine geometry, supporting both SIPMSM and IPMSM.

Args:
    machine (Machine): The machine object representing the geometry.
    angle_point_ref_list (list[float]): List of angle values corresponding to 
        reference points for magnetization.
    geometry_list (list[SurfaceAPI]): List of surface geometry elements.

Returns:
    dict: A dictionary containing magnetization information for each magnet in the geometry.

"""
from numpy import pi

from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.Machine import Machine

from pyemmo.api.SurfaceJSON import SurfaceAPI


def get_magnetization_dict(
    machine: Machine,
    angle_point_ref_list: list[float],
    geometry_list: list[SurfaceAPI],
) -> dict:
    """Generate a dictionary mapping magnets to their respective magnetization angles.

    This function calculates and returns a dictionary containing information about
    the magnetization of magnets in the specified machine geometry. The resulting
    dictionary includes the magnet identifier ('Mag0', 'Mag1', ...), and the
    corresponding magnetization angle.

    Args:
        machine (Machine): The machine object representing the geometry.
        angle_point_ref_list (list[float]): List of angle values corresponding to reference points for magnetization.
        geometry_list (list[SurfaceAPI]): List of surface geometry elements.

    Returns:
        dict: A dictionary containing magnetization information for each magnet in the geometry.

    Raises:
        ValueError: If the magnetization type is unsupported.

    Note:
        The function supports both SIPMSM and IPMSM.

    Example:
        ```
        machine = MachineSIPMSM(...)
        angle_point_ref_list = [30, 60]
        geometry_list = [SurfaceAPI(...), SurfaceAPI(...), ...]
        magnetization_dict = get_magnetization_dict(machine, angle_point_ref_list, geometry_list)
        ```
    """
    # ----------------------------------------------------
    # Filling the magnetization dict if surface is magnet:
    # ----------------------------------------------------
    magnetization_dict = {}

    # Changing the 'idExt' of the SurfaceAPI to 'Mag0', 'Mag1', 'Mag2', ...
    # if the 'idExt' is 'Mag'
    lpl_counter = 0
    mag_counter = 0

    for surf_api in geometry_list:
        if surf_api.idExt == "Lpl":
            surf_api.setIdExt("Lpl" + str(lpl_counter))
            lpl_counter += 1

        elif surf_api.idExt == "Mag":
            surf_api.setIdExt("Mag" + str(mag_counter))
            mag_counter += 1

    if isinstance(machine, MachineSIPMSM):
        angle_point_ref = angle_point_ref_list[0]
        magnetization_type = machine.rotor.magnet.type_magnetization

        if len(angle_point_ref_list) == 1:
            if magnetization_type in (0, 1):  # radial & parallel
                magnetization_angle = angle_point_ref

            elif magnetization_type == 3:  # tangential
                magnetization_angle = angle_point_ref - 90 / pi

            magnetization_dict["Mag0"] = magnetization_angle

        else:
            for surf_api in geometry_list:
                if surf_api.idExt == "Mag0":
                    if magnetization_type in (0, 1):  # radial & parallel
                        magnetization_angle = angle_point_ref_list[0]

                    elif magnetization_type == 3:  # tangential
                        magnetization_angle = angle_point_ref_list[0] - 90 / pi

                    magnetization_dict["Mag0"] = magnetization_angle

                elif surf_api.idExt == "Mag1":
                    if magnetization_type in (0, 1):  # radial & parallel
                        magnetization_angle = angle_point_ref_list[1]

                    elif magnetization_type == 3:  # tangential
                        magnetization_angle = angle_point_ref_list[1] - 90 / pi

                    magnetization_dict["Mag1"] = -magnetization_angle

    elif isinstance(machine, MachineIPMSM):
        mag_angle_dict = machine.rotor.hole[0].comp_magnetization_dict()
        if len(mag_angle_dict) == 1:
            angle_point_ref = angle_point_ref_list[0]
            magnetization_type = machine.rotor.hole[
                0
            ].magnet_0.type_magnetization

            if magnetization_type in (0, 1):  # radial & parallel
                magnetization_angle = angle_point_ref

            elif magnetization_type == 3:  # tangential
                magnetization_angle = angle_point_ref - 90 / pi

            magnetization_dict["Mag0"] = magnetization_angle
        else:
            for surf_api in geometry_list:
                if surf_api.idExt == "Mag0":
                    magnetization_angle = (
                        angle_point_ref_list[0] + mag_angle_dict["magnet_0"]
                    )
                    magnetization_dict[surf_api.idExt] = magnetization_angle

                elif surf_api.idExt == "Mag1":
                    magnetization_angle = (
                        angle_point_ref_list[1] + mag_angle_dict["magnet_1"]
                    )
                    magnetization_dict[surf_api.idExt] = magnetization_angle

                elif surf_api.idExt == "Mag2":
                    magnetization_angle = (
                        angle_point_ref_list[2] + mag_angle_dict["magnet_2"]
                    )
                    magnetization_dict[surf_api.idExt] = magnetization_angle

    return magnetization_dict
