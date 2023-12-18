"""Import of pi"""
from numpy import pi

from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.Machine import Machine

from pyemmo.api.SurfaceJSON import SurfaceAPI


def getMagnetizationDict(
    machine: Machine,
    anglePointRefList: list[float],
    magnetizationDict: dict,
    geometryList: list[SurfaceAPI],
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
    lplCounter = 0
    for surfAPIRotor in geometryList:
        if surfAPIRotor.idExt == "Lpl":
            surfAPIRotor.setIdExt("Lpl" + str(lplCounter))
            lplCounter += 1

    # Changing the 'idExt' of the SurfaceAPI to 'Mag0', 'Mag1', 'Mag2', ...
    # if the 'idExt' is 'Mag'
    magCounter = 0
    for surfAPIRotor in geometryList:
        if surfAPIRotor.idExt == "Mag":
            surfAPIRotor.setIdExt("Mag" + str(magCounter))
            magCounter += 1

    if isinstance(machine, MachineSIPMSM):
        anglePointRef = anglePointRefList[0]
        magnetizationType = machine.rotor.magnet.type_magnetization

        if len(anglePointRefList) == 1:
            if magnetizationType in (0, 1):  # radial & parallel
                magnetizationAngle = anglePointRef

            elif magnetizationType == 3:  # tangential
                magnetizationAngle = anglePointRef - 90 / pi

            magnetizationDict["Mag0"] = magnetizationAngle
        else:
            for surfAPIRotor in geometryList:
                if surfAPIRotor.idExt == "Mag0":
                    if magnetizationType in (0, 1):  # radial & parallel
                        magnetizationAngle = anglePointRefList[0]

                    elif magnetizationType == 3:  # tangential
                        magnetizationAngle = anglePointRefList[0] - 90 / pi

                    magnetizationDict["Mag0"] = magnetizationAngle

                elif surfAPIRotor.idExt == "Mag1":
                    if magnetizationType in (0, 1):  # radial & parallel
                        magnetizationAngle = anglePointRefList[1]

                    elif magnetizationType == 3:  # tangential
                        magnetizationAngle = anglePointRefList[1] - 90 / pi

                    magnetizationDict["Mag1"] = -magnetizationAngle

    elif isinstance(machine, MachineIPMSM):
        magAngleDict = machine.rotor.hole[0].comp_magnetization_dict()
        if len(magAngleDict) == 1:
            anglePointRef = anglePointRefList[0]
            magnetizationType = machine.rotor.hole[
                0
            ].magnet_0.type_magnetization

            if magnetizationType in (0, 1):  # radial & parallel
                magnetizationAngle = anglePointRef

            elif magnetizationType == 3:  # tangential
                magnetizationAngle = anglePointRef - 90 / pi

            magnetizationDict["Mag0"] = magnetizationAngle
        else:
            for surfAPIRotor in geometryList:
                if surfAPIRotor.idExt == "Mag0":
                    magnetizationAngle = (
                        anglePointRefList[0] + magAngleDict["magnet_0"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

                elif surfAPIRotor.idExt == "Mag1":
                    magnetizationAngle = (
                        anglePointRefList[1] + magAngleDict["magnet_1"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

                elif surfAPIRotor.idExt == "Mag2":
                    magnetizationAngle = (
                        anglePointRefList[2] + magAngleDict["magnet_2"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

    return magnetizationDict
