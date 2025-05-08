#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
from typing import Literal

import numpy as np


def phase2angle(phaseChar: Literal["u", "v", "w"]) -> float:
    """returns the angle of a specific phase name in "UVW"

    * U = 0
    * V = :math:`\\frac{2\\pi}{3}`
    * W = :math:`-\\frac{2\\pi}{3}`

    Args:
        PhaseChar (str): char object for the phase name (phase ID).
            Should be "u", "v" or "w".

    Raises:
        ValueError: PhaseChar should only by U,V or W
        ValueError: PhaseChar should only habe length=1

    Returns:
        Angle (float): phase angle
    """
    # Case uvw
    if len(phaseChar) == 1:  # if string PhaseChar is only one char
        if phaseChar.lower() == "u":
            return 0
        if phaseChar.lower() == "v":
            return 2 * np.pi / 3
        if phaseChar.lower() == "w":
            return -2 * np.pi / 3
        raise ValueError(
            f'Phase ID "{phaseChar}" is not uvw! Can not determine phase angle!'
        )
    raise ValueError(f'Phase ID "{phaseChar}"is not a single character!', phaseChar)


def phase2color(
    phaseChar: Literal["u", "v", "w"],
) -> Literal["IndianRed", "Yellow", "Aquamarine"]:
    """Get gmsh mesh color name for a phase-character. See `gmsh colors
    <https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_11_0/src/common/Colors.h>`_
    for all available colors.

    Args:
        PhaseChar (Literal["u","v","w"]): Character defining the phase [u,v or w].

    Raises:
        ValueError: if the phase character is different from u,v or w.
        ValueError: if the length of the PhaseChar string is geater 1.

    Returns:
        Literal["IndianRed", "Yellow", "Aquamarine"]:

        - u = "IndianRed"
        - v = "Yellow"
        - w = "Aquamarine"
    """
    # Case uvw
    if len(phaseChar) == 1:  # if string PhaseChar is only one char
        if phaseChar.lower() == "u":
            return "Magenta"
        if phaseChar.lower() == "v":
            return "Yellow4"
        if phaseChar.lower() == "w":
            return "Cyan"
        raise ValueError(
            f'Phase ID "{phaseChar}" is not uvw! Can not determine phase angle!'
        )

    raise ValueError(f'Phase ID "{phaseChar}"is not a single character!', phaseChar)
