#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
This module provides a function to translate Pyleecan surface labels to corresponding part IDs
used in the pyemmo API. It maps specific label patterns from Pyleecan to standardized part
identifiers, facilitating interoperability between Pyleecan and pyemmo.
Functions:
    label2part_id(label: str) -> str:
        Translates a Pyleecan surface label to the corresponding pyemmo part ID. If the label
        does not match any known pattern, the original label is returned. Raises a ValueError
        if the label does not contain a rotor or stator lamination label.
"""

from __future__ import annotations

from pyleecan.Functions.labels import (
    BAR_LAB,
    LAM_LAB,
    MAG_LAB,
    ROTOR_LAB,
    STATOR_LAB,
    WIND_LAB,
    HOLEM_LAB,
    HOLEV_LAB,
    SHAFT_LAB,
    decode_label,
)

from ..json import (
    ROTOR_BAR_IDEXT,
    ROTOR_LAM_IDEXT,
    ROTOR_MAG_IDEXT,
    STATOR_LAM_IDEXT,
    STATOR_SLOT_IDEXT,
)


# pylint: disable=too-few-public-methods, too-many-arguments, too-many-locals
def label2part_id(label: str) -> str:
    """Translate the Pyleecan surface label to the corresponding part ID in the pyemmo
    api. If the surface has no api relevant label the original label is returned.

    Args:
        label (str): Pyleecan surface label

    Returns:
        str: Part ID from pyemmo.api.json. For example, Pyleecan Rotor Lamination with
        label "Rotor-0 Lamination" will be translated to "rotor lamination".
    """
    label_dict = decode_label(label)
    # calculate sum of indices for single index
    if "index" in label_dict:
        index = sum((label_dict["R_id"], label_dict["T_id"], label_dict["S_id"]))
    else:
        index = 0
    if STATOR_LAB in label_dict["lam_label"]:
        if LAM_LAB in label_dict["surf_type"]:
            return STATOR_LAM_IDEXT
        if WIND_LAB in label_dict["surf_type"]:
            # FIXME: This does not allways fit the pyemmo api winding name specification
            # We need to set a index if a slot is divided in multiple (2) slot surface
            # sides for as fractional slot winding.
            # With different symmetries in the model it can happen that more than one slot
            # is created for the stator, even if the winding is an integer slot winding!
            return STATOR_SLOT_IDEXT + f"{index}"
        return label
    if ROTOR_LAB in label_dict["lam_label"]:
        if LAM_LAB in label_dict["surf_type"]:
            return ROTOR_LAM_IDEXT
        if BAR_LAB in label_dict["surf_type"]:
            return ROTOR_BAR_IDEXT + f"{index}"
        if MAG_LAB in label_dict["surf_type"] or HOLEM_LAB in label_dict["surf_type"]:
            return ROTOR_MAG_IDEXT + f"""{label_dict["index"]}"""
        return label
    if HOLEV_LAB in label:
        return label
    if SHAFT_LAB in label:
        return label
    if "Frame" in label:
        return label
    raise ValueError(
        f"Pyleecan surface label did not contain rotor or stator lamination label: {label}"
    )
