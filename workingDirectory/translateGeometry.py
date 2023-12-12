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


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translateGeometry(
    nameSplitList: list[str],  # list with the splitted names
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label: str,
    surface: pyleecan.Classes.Surface.Surface,
    anglePointRefList: list,
) -> tuple[SurfaceAPI, list]:
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
            anglePointRefList.append(angle(surface.point_ref))
            isMag = True

        elif nameSplitList[2] == "Hole":
            pyleecanMat = machine.rotor.hole.mat_type
            idExt = "Mag"
            name = "Magnet"
            anglePointRefList.append(angle(surface.point_ref))
            isMag = True

        elif nameSplitList[2] == "HoleMag":
            pyleecanMat = machine.rotor.hole[0].magnet_0.mat_type

            idExt = "Mag"  # "Magnet"
            name = "Magnet"
            anglePointRefList.append(angle(surface.point_ref))
            isMag = True
            # magCounter += 1

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

    # stator
    elif nameSplitList[0] == "Stator":
        if nameSplitList[2] == "Lamination":
            pyleecanMat = machine.stator.mat_type
            idExt = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif nameSplitList[2] == "Winding":
            pyleecanMat = machine.stator.winding.conductor.cond_mat
            name = "Stator-Nut"
            Q = machine.stator.slot.Zs
            p = machine.stator.winding.p
            m = machine.stator.winding.qs
            q = Q / (2 * m * p)
            if nameSplitList[3] == "R0":
                if q == 0.5:
                    if nameSplitList[4] == "T0":
                        idExt = "StCu0"  # "Stator-Nut"
                    else:
                        idExt = "StCu1"  # "Stator-Nut"
                else:
                    idExt = "StCu0"  # "Stator-Nut"
            elif nameSplitList[3] == "R1":
                # BUG, FIXME: 'T0' kann für q=0.5 Wicklung mit Ober- und
                # Schicht vorkommen. Dann ist für R0 und R1 beides mal 'T0'
                # Das führt dazu, dass beide StCu0 benannt werden und nur eins
                # der beiden Segmente erzeugt wird!
                if q == 0.5 and nameSplitList[4] == "T0":
                    idExt = "StCu1"  # "Stator-Nut"
                elif q == 0.5 and nameSplitList[4] == "T1":
                    # TODO: Außen liegende und linke Nuthälfte... Geht das? Mehr als 
                    # zwei Wicklungen pro Nut?
                    idExt = "StCu1"  # "Stator-Nut"
                else:
                    idExt = "StCu1"  # "Stator-Nut"
            else:
                raise ValueError(
                    f"Radial Index of '{nameSplitList.join('_')}' was not R0 or R1, but '{nameSplitList[3]}'"
                )

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
            f"Wrong input for 'bauteil'. 'bauteil' must be 'Rotor' or 'Stator'. Your input was '{nameSplitList[0]}'."
        )

    return pyemmoSurface, anglePointRefList
