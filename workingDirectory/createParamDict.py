import logging

from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.Simulation import Simulation
from pyleecan.Classes.Lamination import Lamination
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.OPdq import OPdq

from .translateWinding import translateWinding


def createParamDict(
    machine: Machine,
    pyleecanSimulation: Simulation,
    movingband_r: float,
    magnetizationDict: dict,
) -> dict[str, any]:
    """This function builds a dictionary for communication between pyleecan and pyemmo.

    Args:
        machine (Machine): machine in pyleecan format
        pyleecanSimulation (Simulation): simulation parameter in pyleecan format
        movingband_r (float): radius of the movingBand 
        magnetizationDict (dict): dictionary which contains the magnet with corresponding magnetizationangle

    Raises:
        RuntimeError: _description_

    Returns:
        dict[str, any]: _description_
    """
    # The following part of the function tests if 'Id_ref' and 'Iq_ref' are having values
    # and if so their values will directly be set in the dictionary under 'Id' and 'Iq'.
    # If only 'I0_Phi0' has a set value but 'Id_ref' and 'Iq_ref' don't 'Id' and 'Iq' will be
    # calculated.

    op = pyleecanSimulation.input.OP

    if isinstance(op, OPdq):
        Id = op.Id_ref
        Iq = op.Iq_ref

    else:
        Id = 0
        Iq = 0
        logging.warning(
            '!! Warning: No Values set for "Id_ref" and "Iq_ref" -> Id = Iq = 0 !!'
        )

    # --------------------------------------------------------------------------------------
    # The following part of the function tests if rotor or stator have magnets and if so
    # if there are more than one magnet build in.
    # If there are magnets, the type of the magnetization will be safed in 'pyemmoMagType'.
    # 'pyemmoMagType': [0] : parallel
    #                  [1] : radial
    #                  [2] : Hallbach (!! not implemented in pyemmo !!)
    #                  [3] : tangential
    # If there are no magnets in rotor and stator, 'pyemmoMagType' will be set to 'None'.
    # --------------------------------------------------------------------------------------

    lamWithMag: Lamination = None

    if (
        pyleecanSimulation.machine.rotor.has_magnet()
    ):  # Test, if rotor has magnet(s)
        lamWithMag = pyleecanSimulation.machine.rotor

    elif (
        pyleecanSimulation.machine.stator.has_magnet()
    ):  # Test, if stator has magnet(s)
        lamWithMag = pyleecanSimulation.machine.stator

    else:  # If rotor doesn't have magnets, pyemmoMagType = None
        pyemmoMagType = None

    if lamWithMag:
        if isinstance(
            lamWithMag, LamHole
        ):  # Test, if lamWithMag has Holes where the magnet(s) sit(s) in
            if isinstance(
                lamWithMag.hole, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmoMagType = lamWithMag.hole[0].magnet_0.type_magnetization

            else:  # If lamWithMag has only one magnet
                pyemmoMagType = lamWithMag.hole.magnet_0.type_magnetization

        elif isinstance(
            lamWithMag, LamSlotMag
        ):  # Test, if lamWithMag has Slots where the magnet(s) sit(s) in
            if isinstance(
                lamWithMag.slot, list
            ):  # Test, if lamWithMag has more than one magnet
                # The magnetization Type for all magnets in the machine will be set
                # in the same Type as the firt magnet in the list.

                pyemmoMagType = lamWithMag.slot[0].magnet_0.type_magnetization

            else:  # If rotor has only one magnet
                pyemmoMagType = lamWithMag.magnet.type_magnetization

        else:
            # Error
            raise RuntimeError(
                f'Lamination of type "{str(type(lamWithMag))}" is not type LamHole or LamSlotMag.'
            )
    if pyemmoMagType == 0:
        pyemmoMagType = "radial"
    elif pyemmoMagType == 1:
        pyemmoMagType = "parallel"
    elif pyemmoMagType == 3:
        pyemmoMagType = "tangential"


    symFactor = machine.comp_periodicity_spatial()
    if symFactor[1]:
        symFactor = symFactor[0] * 2
    else:
        symFactor = symFactor[0]
    print(f"Symmetry factor machine: {symFactor}")
    swatemWinding, windLayout = translateWinding(machine)
    symWinding = swatemWinding.get_periodicity_t()*2
    print(f"Symmetry factor winding: {symWinding}")
    symFactor = min(symWinding, symFactor)

    speed_rpm = pyleecanSimulation.input.OP.N0
    translationParameterDict = {
        "winding": windLayout,  # winding layout
        # "wickSWAT": translateWinding(machine),
        "NpP": machine.stator.winding.Npcp,  # number of parallel paths per winding phase
        "Ntps": machine.stator.winding.Ntcoil,
        "z_pp": machine.stator.winding.p,  # number of pole pairs
        "Qs": machine.stator.slot.Zs,  # number of stator slots
        "movingband_r": movingband_r,  # moving band radius in meters
        "axLen_S": machine.stator.L1,  # axial length of stator
        "axLen_R": machine.rotor.L1,  # axial length of rotor
        "symFactor": symFactor,  # symmetry factor for model (STANDARD = 1) has to be defined
        "startPos": 0,  # start rotor position in ° (STANDARD = 0°)
        "endPos": pyleecanSimulation.input.time.value[-1]
        * speed_rpm
        / 60
        * 360,  # end position in °
        "nbrSteps": pyleecanSimulation.input.time.value.size,  # number of time steps for simulation
        "rot_freq": speed_rpm / 60,  # mech freq in Hz
        "parkAngleOffset": None,  # park transformation offset angle in elec. ° (STANDARD = None)
        "analysisType": 0,  # 0=static; 1=transient (STANDARD = 1)
        "tempMag": 20,  # magnet temperature °C (STANDARD = 20°C)
        "r_z": 0.7,  # tooth radius in meterm (STANDARD = None)
        "r_j": 0.9,  # yoke radius in meter (STANDARD = None)
        "id": Id,  # d-axis current in A
        "iq": Iq,  # q-axis current in A
        "modelName": machine.name,  # name of the model files
        "magType": pyemmoMagType,  # magnetization Type/ type of permament magnets(“parallel”, “radial” or “tangential”)
        "magAngle": magnetizationDict,
        "flag_openGUI": True,  # open Gmsh GUI after model generation (STANDARD = True)
        "calcIronLoss": False,
    }

    return translationParameterDict
