from math import pi
from numpy import angle

import pyleecan.Classes.Machine
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind
import pyleecan.Classes.Surface

from pyemmo.api.SurfaceJSON import SurfaceAPI
from .buildPyemmoMaterial import build_pyemmo_material
from .buildPyemmoLineList import build_pyemmo_line_list


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translate_surfs(
    name_split_list: list[str],  # list with the splitted names
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    surface: pyleecan.Classes.Surface.Surface,
    angle_point_ref_list: list,
) -> tuple[SurfaceAPI, list]:
    if name_split_list[0] == "Rotor":
        if name_split_list[2] == "Lamination":
            pyleecan_mat = machine.rotor.mat_type
            id_ext = "Pol"  # "RoNut" "Rotorblech"
            name = "Rotorblech"

        elif name_split_list[2] == "Magnet":
            pyleecan_mat = machine.rotor.magnet.mat_type
            id_ext = "Mag"
            name = "Magnet"
            angle_point_ref_list.append(angle(surface.point_ref))

        elif name_split_list[2] == "Hole":
            pyleecan_mat = machine.rotor.hole.mat_type
            id_ext = "Mag"
            name = "Magnet"
            angle_point_ref_list.append(angle(surface.point_ref))

        elif name_split_list[2] == "HoleMag":
            pyleecan_mat = machine.rotor.hole[0].magnet_0.mat_type

            id_ext = "Mag"  # "Magnet"
            name = "Magnet"
            angle_point_ref_list.append(angle(surface.point_ref))

        elif name_split_list[2] == "HoleVoid":
            pyleecan_mat = machine.rotor.hole[0].mat_void
            id_ext = "Lpl"  # "Loch (Pollueke)"
            name = "Loch"

        elif name_split_list[2] == "Ventilation":
            pyleecan_mat = machine.rotor.axial_vent[0].mat_void
            id_ext = "Lpl"  # "Loch (Pollueke)"
            name = "Loch"

        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{name_split_list[2]}'."
            )

        nbr_seg = machine.rotor.comp_periodicity_geo()[0]

    # stator
    elif name_split_list[0] == "Stator":
        if name_split_list[2] == "Lamination":
            pyleecan_mat = machine.stator.mat_type
            id_ext = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif name_split_list[2] == "Winding":
            pyleecan_mat = machine.stator.winding.conductor.cond_mat
            name = "Stator-Nut"
            z = machine.stator.slot.Zs
            p = machine.stator.winding.p
            m = machine.stator.winding.qs
            q = z / (2 * m * p)
            if name_split_list[3] == "R0":
                if q == 0.5:
                    if name_split_list[4] == "T0":
                        id_ext = "StCu0"  # "Stator-Nut"
                    else:
                        id_ext = "StCu1"  # "Stator-Nut"
                else:
                    id_ext = "StCu0"  # "Stator-Nut"
            elif name_split_list[3] == "R1":
                # BUG, FIXME: 'T0' kann für q=0.5 Wicklung mit Ober- und
                # Schicht vorkommen. Dann ist für R0 und R1 beides mal 'T0'
                # Das führt dazu, dass beide StCu0 benannt werden und nur eins
                # der beiden Segmente erzeugt wird!
                if q == 0.5 and name_split_list[4] == "T0":
                    id_ext = "StCu1"  # "Stator-Nut"
                elif q == 0.5 and name_split_list[4] == "T1":
                    # TODO: Außen liegende und linke Nuthälfte... Geht das? Mehr als
                    # zwei Wicklungen pro Nut?
                    id_ext = "StCu1"  # "Stator-Nut"
                else:
                    id_ext = "StCu1"  # "Stator-Nut"
            else:
                raise ValueError(
                    f"Radial Index of '{name_split_list.join('_')}' was not R0 or R1, but '{name_split_list[3]}'"
                )

        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{name_split_list[2]}'."
            )

        nbr_seg = machine.stator.comp_periodicity_geo()[0]

    else:
        raise ValueError(
            f"Wrong input for 'bauteil'. 'bauteil' must be 'Rotor' or 'Stator'. Your input was '{name_split_list[0]}'."
        )

    angle_seg = 2 * pi / nbr_seg
    pyemmo_mat = build_pyemmo_material(pyleecan_mat)
    pyemmo_surf = SurfaceAPI(
        name=name,
        idExt=id_ext,
        curves=build_pyemmo_line_list(surface.line_list),
        material=pyemmo_mat,
        nbrSegments=nbr_seg,
        angle=angle_seg,
        meshSize=0,
    )

    return pyemmo_surf, angle_point_ref_list
