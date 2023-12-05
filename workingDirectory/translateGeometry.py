from math import pi
from numpy import angle

import pyleecan.Classes.Machine
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind
import pyleecan.Classes.Surface

from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.definitions import DEFAULT_GEO_TOL
from .buildPyemmoMaterial import buildPyemmoMaterial
from .buildPyemmoLineList import buildPyemmoLineList
from .getMagnetizationAngle import getMagnetizationDict


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translateGeometry(
    bauteil: str,  # Stator or Rotor
    detail: str,  # Lamination, HoleMag, HoleVoid
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label: str,
    surface: pyleecan.Classes.Surface.Surface,
    magnetizationDict: dict,
) -> tuple[SurfaceAPI, dict]:
    isMag = False
    if bauteil == "Rotor":
        if detail == "Lamination":
            pyleecanMat = machine.rotor.mat_type
            idExt = "Pol"  # "RoNut" "Rotorblech"
            name = "Rotorblech"

        elif detail == "Magnet":
            pyleecanMat = machine.rotor.magnet.mat_type
            idExt = "Mag"
            name = "Magnet"
            anglePointRef = angle(surface.point_ref)
            isMag = True

        elif detail == "Hole":
            pyleecanMat = machine.rotor.hole.mat_type
            idExt = "Mag"
            name = "Magnet"
            anglePointRef = angle(surface.point_ref)
            isMag = True

        elif detail == "HoleMag":
            pyleecanMat = machine.rotor.hole[0].magnet_0.mat_type
            idExt = "Mag"  # "Magnet"
            name = "Magnet"

        elif detail == "HoleVoid":
            pyleecanMat = machine.rotor.hole[0].mat_void
            idExt = "Lpl"  # "Loch (Pollueke)"
            name = "Loch"
        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{detail}'."
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
    elif bauteil == "Stator":
        if detail == "Lamination":
            pyleecanMat = machine.stator.mat_type
            idExt = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif detail == "Winding":
            pyleecanMat = machine.stator.winding.conductor.cond_mat
            idExt = "StCu0"  # "Stator-Nut"
            name = "Stator-Nut"

        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{detail}'."
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
