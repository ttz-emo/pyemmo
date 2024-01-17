"""Import of pi"""
from numpy import pi

from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.Machine import Machine

from pyemmo.api.SurfaceJSON import SurfaceAPI


def get_magnetization_dict(
    machine: Machine,
    angle_point_ref_list: list[float],
    magnetization_dict: dict,
    geometry_list: list[SurfaceAPI],
) -> dict:
    """Get the magnetization dict with the magnet and the magnetization angle.

    Args:
        magnetizationDict (dict): Dict with magnet corresponding magnetization angle
        idExt (str): IdExt of the surface
        anglePointRef (float): Angle of the pointRef
        magnetizationType (int): 0: radial | 1: parallel | 3: tangential

    Returns:
        dict: magnetizationDict with magnet and corresponding magnetization angle
    """
    # ----------------------------------------------------
    # Filling the magnetization dict if surface is magnet:
    # ----------------------------------------------------
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
