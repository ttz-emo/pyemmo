#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
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
"""Convert winding phase angle to index character or vice versa."""
from __future__ import annotations

from typing import Literal

import numpy as np

from ..colors import Colors


def angle2phase(phase_angle: float, phase_names: tuple[str] = ("u", "v", "w")) -> str:
    r"""
    Converts a given phase angle within 0 to 2*pi to its corresponding phase name.
    The function maps a phase angle to a phase name based on evenly distributed
    phase angles derived from the number of phase names provided. For a standard
    3-phase winding phase angle for phase 1 must be within 0\deg ± 60\deg, phase 2 = 120\deg ±
    60\deg, ...
    If the given phase angle is within a tolerance range of one of the calculated phase
    angles, the corresponding phase name is returned. Otherwise, a ValueError is raised.

    Args:
        phase_angle (float): The phase angle in radians [0,2*pi] to be converted.
        phase_names (list[str], optional): A list of phase names corresponding to
            the calculated phase angles. Defaults to ["u", "v", "w"].

    Returns:
        str: The phase name corresponding to the given phase angle.

    Raises:
        ValueError: If the phase angle does not match any of the calculated
            phase angles within the tolerance range.

    Example:
        >>> angle2phase(np.pi / 3, ["A", "B", "C"]) # 120 \deg
        'B'
        >>> angle2phase(np.pi / 100, ["A", "B", "C"]) # 1.8 \deg
        'A'
    """

    # get range for phase angle
    angle_tol = 2 * np.pi / len(phase_names) / 2
    phase_angles = 2 * np.pi / len(phase_names) * np.arange(len(phase_names))
    if np.isclose(phase_angle, phase_angles, atol=angle_tol).any():
        # get index of phase angle in phase_angles
        phase_index = np.where(np.isclose(phase_angle, phase_angles, atol=angle_tol))[
            0
        ][0]
        return phase_names[phase_index]
    raise ValueError(
        f"Phase angle {np.rad2deg(phase_angle)} is not in range of phase angles "
        f"{np.rad2deg(phase_angles)} +- {angle_tol} deg!"
    )


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
            return "Yellow"
        if phaseChar.lower() == "w":
            return "Cyan"
        if isinstance(phaseChar, str):
            # if not in uvw, but is str (eg. for multiphase windings), return unicode
            # number of char from list of ONELAB colors
            return list(Colors.keys())[ord(phaseChar)]
        raise ValueError(
            f'Phase ID "{phaseChar}" is not uvw! Can not determine phase angle!'
        )

    raise ValueError(f'Phase ID "{phaseChar}"is not a single character!', phaseChar)
