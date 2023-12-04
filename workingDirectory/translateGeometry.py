import sys
import copy
from math import pi, isclose
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
from .createS1S2 import createS1S2
from .getMagnetizationAngle import getMagnetizationDict


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def buildGeoSPMSM(
    bauteil: str,  # Stator or Rotor
    detail: str,  # Lamination, HoleMag, HoleVoid
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label: str,
    surface: pyleecan.Classes.Surface.Surface,
    magnetizationDict: dict,
):
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

        else:
            raise ValueError(f"Wrong input for 'detail'. Your input was '{detail}'.")

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
            raise ValueError(f"Wrong input for 'detail'. Your input was '{detail}'.")

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


# ===========================================
# Definition of function 'translateGeometry': ORIGINAL
# ===========================================
def translateGeometrySPMSM(
    bauteil: str,  # Stator or Rotor
    detail: str,  # Lamination, HoleMag, HoleVoid
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label: str,
    surface: pyleecan.Classes.Surface.Surface,
    isInternalRotor: bool,
    magnetFarthestRadius: float,
    magnetShortestRadius: float,
):
    """_summary_

    Args:
        bauteil (str): _description_
        machine (pyleecan.Classes.Machine.Machine): _description_
        surface (pyleecan.Classes.Surface.Surface): _description_
        isInternalRotor (bool): _description_
        magnetFarthestRadius (float): _description_
        magnetShortestRadius (float): _description_

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
    isMag = False
    centerPoint = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1.0)
    if bauteil == "Rotor":
        if detail == "Lamination":
            pyleecanMat = machine.rotor.mat_type
            IdExt = "Pol"  # "RoNut" "Rotorblech"
            name = "Rotorblech"

        elif isinstance(machine.rotor, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM, SPSMSM

            if detail == "HoleMag":
                pyleecanMat = machine.rotor.hole[0].magnet_0.mat_type
                IdExt = "Mag"  # "Magnet"
                name = "Magnet"

            elif detail == "HoleVoid":
                pyleecanMat = machine.rotor.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"
                name = "Loch"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.rotor, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = machine.rotor.magnet.mat_type
                IdExt = "Mag"
                name = "Magnet"
                anglePointRef = angle(surface.point_ref)
                isMag = True

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.rotor, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail in ("Winding", "Bar"):
                pyleecanMat = machine.rotor.winding.conductor.cond_mat
                IdExt = "RoCu"  # "Rotor-Nut"
                name = "Rotor-Nut"

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
            nbrSegments=machine.get_pole_pair_number() * 2,
            angle=(2 * pi / (machine.get_pole_pair_number() * 2)),
            meshSize=0,
        )

        # ----------------------------
        # Adding the S1 and S2 Points:
        # ----------------------------
        if isMag:
            if isInternalRotor:
                createS1S2(
                    pyemmoSurface=pyemmoSurface,
                    anglePointRef=anglePointRef,
                    centerPoint=centerPoint,
                    magnetShortestRadius=magnetShortestRadius,
                    magnetFarthestRadius=magnetFarthestRadius,
                )
            else:
                createS1S2(
                    pyemmoSurface=pyemmoSurface,
                    anglePointRef=anglePointRef,
                    centerPoint=centerPoint,
                    magnetShortestRadius=magnetFarthestRadius,
                    magnetFarthestRadius=magnetShortestRadius,
                )

    # stator
    elif bauteil == "Stator":
        if detail == "Lamination":
            pyleecanMat = machine.stator.mat_type
            IdExt = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif isinstance(machine.stator, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM

            if detail == "HoleMag":
                pyleecanMat = machine.stator.hole[0].magnet_0.mat_type
                IdExt = "Mag"
                name = "Magnet"

            elif detail == "HoleVoid":
                pyleecanMat = machine.stator.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"
                name = "Loch"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.stator, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = machine.rotor.magnet.mat_type
                IdExt = "Mag"
                name = "Magnet"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.stator, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail == "Winding":
                pyleecanMat = machine.stator.winding.conductor.cond_mat
                IdExt = "StCu0"  # "Stator-Nut"
                name = "Stator-Nut"

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
            name=name,
            idExt=IdExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=machine.stator.slot.Zs,
            angle=(2 * pi / machine.stator.slot.Zs),
            meshSize=1.0,
        )

    return pyemmoSurface
