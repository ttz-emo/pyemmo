import sys
from math import pi

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

import pyleecan.Classes.Machine
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind

from pyemmo.api.SurfaceJSON import SurfaceAPI
from workingDirectory.buildPyemmoMaterial import buildPyemmoMaterial
from workingDirectory.buildPyemmoLineList import buildPyemmoLineList


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translateGeometry(
    bauteil,  # Stator or Rotor
    detail,  # Lamination, HoleMag, HoleVoid
    motor: pyleecan.Classes.Machine.Machine,  # Import of motor
    label,
    surface,
):
    """_summary_

    Args:
        bauteil (_type_): _description_
        detail (_type_): _description_
        motor (pyleecan.Classes.Machine.Machine): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if bauteil == "Rotor":
        if detail == "Lamination":
            pyleecanMat = motor.rotor.mat_type
            IdExt = "Pol"  # "RoNut" "Rotorblech"

        elif isinstance(motor.rotor, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM, SPSMSM

            if detail == "HoleMag":
                pyleecanMat = motor.rotor.hole[0].magnet_0.mat_type
                IdExt = "Mag"  # "Magnet"

            elif detail == "HoleVoid":
                pyleecanMat = motor.rotor.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(motor.rotor, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = motor.rotor.magnet.mat_type
                IdExt = "Mag"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(motor.rotor, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail in ("Winding", "Bar"):
                pyleecanMat = motor.rotor.winding.conductor.cond_mat
                IdExt = "RoCu"  # "Rotor-Nut"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=label,
            idExt=IdExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=motor.get_pole_pair_number(),
            angle=(2 * pi / motor.get_pole_pair_number()),
            meshSize=0,
        )
        return pyemmoSurface

    # stator
    elif bauteil == "Stator":
        if detail == "Lamination":
            pyleecanMat = motor.stator.mat_type
            IdExt = "StNut"  # "Statorblech"

        elif isinstance(motor.stator, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM

            if detail == "HoleMag":
                pyleecanMat = motor.stator.hole[0].magnet_0.mat_type
                IdExt = ""

            elif detail == "HoleVoid":
                pyleecanMat = motor.stator.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(motor.stator, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = motor.rotor.magnet.mat_type
                IdExt = "Mag"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(motor.stator, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail == "Winding":
                pyleecanMat = motor.stator.winding.conductor.cond_mat
                IdExt = "StCu"  # "Stator-Nut"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        else:
            raise ValueError(
                f"Wrong input for 'bauteil'. 'bauteil' must be 'Rotor' or 'Stator'. Your input was '{bauteil}'."
            )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=label,
            idExt=IdExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=motor.stator.slot.Zs * 2,
            angle=(2 * pi / (motor.stator.slot.Zs * 2)),
            meshSize=1.0,
        )
        return pyemmoSurface
