#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Module: translate_surfs

This module provides functions for translating surfaces from pyleecan format to
pyemmo format.

Functions:
    -   ``build_pyemmo_material``: Translates a pyleecan-material into a pyemmo-
        material.

    -   ``build_pyemmo_line_list``: Translates a list of pyleecan curves into a
        list of pyemmo curves.

    -   ``translate_surfs``: Translates pyleecan surfaces into pyemmo surfaces.
"""

from __future__ import annotations

from math import pi

import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind
import pyleecan.Classes.Machine
import pyleecan.Classes.Surface
from numpy import angle

from ...script.geometry.segment_surface import SegmentSurface
from ..json import (
    ROTOR_BAR_IDEXT,
    ROTOR_LAM_IDEXT,
    ROTOR_MAG_IDEXT,
    STATOR_LAM_IDEXT,
    STATOR_SLOT_IDEXT,
)
from . import POLE_HOLE_IDEXT, PyleecanMachine
from .build_pyemmo_line_list import build_pyemmo_line_list
from .build_pyemmo_material import build_pyemmo_material


def translate_surface(
    name_split_list: list[str],  # list with the splitted names
    machine: PyleecanMachine,
    surface: pyleecan.Classes.Surface.Surface,
    angle_point_ref_list: list,
) -> tuple[SegmentSurface, list]:
    """
    Translates pyleecan surfaces into pyemmo surfaces.

    Args:
        name_split_list (list[str]): List with the splitted names.
        machine (pyleecan.Classes.Machine.Machine): Import of the motor.
        surface (pyleecan.Classes.Surface.Surface): Pyleecan surface to be
            translated.
        angle_point_ref_list (list): List of angle point references.

    Raises:
        ValueError: If there is an issue with the input values.

    Returns:
        tuple[SurfaceAPI, list]: Translated pyemmo surface and updated angle
        point reference list.
    """
    if name_split_list[0] == "Rotor":
        if name_split_list[2] == "Lamination":
            pyleecan_mat = machine.rotor.mat_type
            id_ext = ROTOR_LAM_IDEXT  # "RoNut" "Rotorblech"
            name = "Rotor Lamination"

        elif name_split_list[2] in ("Magnet", "Hole", "HoleMag"):
            id_ext = ROTOR_MAG_IDEXT
            name = "Magnet"
            angle_point_ref_list.append(angle(surface.point_ref))

            if name_split_list[2] == "Magnet":
                pyleecan_mat = machine.rotor.magnet.mat_type

            elif name_split_list[2] == "Hole":
                pyleecan_mat = machine.rotor.hole.mat_type

            elif name_split_list[2] == "HoleMag":
                pyleecan_mat = machine.rotor.hole[0].magnet_0.mat_type

        elif name_split_list[2] in ("HoleVoid", "Ventilation"):
            # TODO: Could we here directly set the index for the specific hole?
            id_ext = POLE_HOLE_IDEXT  # "Loch (Pollueke)"
            name = "Loch"  # important to keep name for correct cut out!

            if name_split_list[2] == "HoleVoid":
                pyleecan_mat = machine.rotor.hole[0].mat_void

            elif name_split_list[2] == "Ventilation":
                pyleecan_mat = machine.rotor.axial_vent[0].mat_void
        elif name_split_list[2] == "Bar":
            # Rotor Bar for SCIM
            pyleecan_mat = machine.rotor.winding.conductor.cond_mat
            id_ext = ROTOR_BAR_IDEXT  # "RoNut" "Rotorblech"
            name = "Rotor Bar"
        else:
            raise ValueError(
                f"Wrong input for 'detail'. Your input was '{name_split_list[2]}'."
            )

        nbr_seg = machine.rotor.comp_periodicity_geo()[0]

    # stator
    elif name_split_list[0] == "Stator":
        if name_split_list[2] == "Lamination":
            pyleecan_mat = machine.stator.mat_type
            id_ext = STATOR_LAM_IDEXT  # "Statorblech"
            name = "Stator Lamination"

        elif name_split_list[2] == "Winding":
            pyleecan_mat = machine.stator.winding.conductor.cond_mat
            name = "Stator Slot"
            z = machine.stator.slot.Zs
            p = machine.stator.winding.p
            m = machine.stator.winding.qs
            q = z / (2 * m * p)
            if name_split_list[3] == "R0":
                if q == 0.5:
                    if name_split_list[4] == "T0":
                        id_ext = STATOR_SLOT_IDEXT + "0"
                    else:
                        id_ext = STATOR_SLOT_IDEXT + "1"
                else:
                    id_ext = STATOR_SLOT_IDEXT + "0"
            elif name_split_list[3] == "R1":
                # BUG, FIXME: 'T0' kann für q=0.5 Wicklung mit Ober- und
                # Schicht vorkommen. Dann ist für R0 und R1 beides mal 'T0'
                # Das führt dazu, dass beide StCu0 benannt werden und nur eins
                # der beiden Segmente erzeugt wird!
                if q == 0.5 and name_split_list[4] == "T0":
                    id_ext = STATOR_SLOT_IDEXT + "1"
                elif q == 0.5 and name_split_list[4] == "T1":
                    # TODO: Außen liegende und linke Nuthälfte... Geht das? Mehr als
                    # zwei Wicklungen pro Nut?
                    id_ext = STATOR_SLOT_IDEXT + "1"
                else:
                    id_ext = STATOR_SLOT_IDEXT + "1"
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
    pyemmo_surf = SegmentSurface(
        name=name,
        idExt=id_ext,
        curves=build_pyemmo_line_list(surface.line_list),
        material=build_pyemmo_material(pyleecan_mat),
        nbrSegments=nbr_seg,
        angle=angle_seg,
        meshSize=0,
    )

    return pyemmo_surf, angle_point_ref_list
