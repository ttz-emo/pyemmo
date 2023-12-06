from math import pi
from numpy import angle

import pyleecan.Classes.Machine
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind
import pyleecan.Classes.Surface

from pyemmo.api.SurfaceJSON import SurfaceAPI
from .buildPyemmoMaterial import buildPyemmoMaterial
from .buildPyemmoLineList import buildPyemmoLineList
from .getMagnetizationDict import getMagnetizationDict


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translateGeometry(
    nameSplitList: list[str],  # list with the splitted names
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label: str,
    surface: pyleecan.Classes.Surface.Surface,
    magnetizationDict: dict,
) -> tuple[SurfaceAPI, dict]:
    isMag = False
    if nameSplitList[0] == "Rotor":
        if nameSplitList[2] == "Lamination":
            pyleecanMat = machine.rotor.mat_type
            idExt = "Pol"  # "RoNut" "Rotorblech"
            name = "Rotorblech"

        elif nameSplitList[2] == "Magnet":
            pyleecanMat = machine.rotor.magnet.mat_type
            idExt = "Mag"
            name = "Magnet"
            anglePointRef = angle(surface.point_ref)
            isMag = True

        elif nameSplitList[2] == "Hole":
            pyleecanMat = machine.rotor.hole.mat_type
            idExt = "Mag"
            name = "Magnet"
            anglePointRef = angle(surface.point_ref)
            isMag = True

        elif nameSplitList[2] == "HoleMag":
            pyleecanMat = machine.rotor.hole[0].magnet_0.mat_type
            idExt = "Mag"  # "Magnet"
            name = "Magnet"

        elif nameSplitList[2] == "HoleVoid":
            pyleecanMat = machine.rotor.hole[0].mat_void
            idExt = "Lpl"  # "Loch (Pollueke)"
            name = "Loch"
        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{nameSplitList[2]}'."
            )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=label,
            idExt=idExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=machine.get_pole_pair_number() * 2,
            angle=(2 * pi / (machine.get_pole_pair_number() * 2)),
            meshSize=0,
        )

        # ----------------------------------------------------
        # Filling the magnetization dict if surface is magnet:
        # ----------------------------------------------------
        if isMag:
            magnetizationDict = getMagnetizationDict(
                magnetizationDict=magnetizationDict,
                idExt=pyemmoSurface.idExt,
                anglePointRef=anglePointRef,
                magnetizationType=machine.rotor.magnet.type_magnetization,
            )

    # stator
    elif nameSplitList[0] == "Stator":
        if nameSplitList[2] == "Lamination":
            pyleecanMat = machine.stator.mat_type
            idExt = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif nameSplitList[2] == "Winding":
            pyleecanMat = machine.stator.winding.conductor.cond_mat
            name = "Stator-Nut"
            if nameSplitList[3] == "R0":
                idExt = "StCu0"  # "Stator-Nut"
            else:
                idExt = "StCu1"  # "Stator-Nut"

        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{nameSplitList[2]}'."
            )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=name,
            idExt=idExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=machine.stator.slot.Zs,
            angle=(2 * pi / machine.stator.slot.Zs),
            meshSize=1.0,
        )

    else:
        raise ValueError(
            f"Wrong input for 'bauteil'. 'bauteil' must be 'Rotor' or 'Stator'. Your input was '{bauteil}'."
        )

    return pyemmoSurface, magnetizationDict
