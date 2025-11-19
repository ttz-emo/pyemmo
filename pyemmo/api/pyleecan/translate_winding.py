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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Module to translate winding data from Pyleecan to PyEMMO.

This module provides functions to translate winding data from Pyleecan, to
PyEMMO by the SWAT-EM package.

Functions:
    -   ``translate_winding``: Translates the winding from Pyleecan to PyEMMO
        format.

Note:
    The winding translation process involves generating a winding data model
    using the PyEMMO `datamodel` class, extracting winding information from the
    Pyleecan machine object, and formatting it according to the SWAT-EM
    conventions.

    TODO: Perhaps return only the data model object and call the
    ``get_phases()`` function directly in ``createParamDict``.
"""

from __future__ import annotations

import swat_em
from pyleecan.Classes.Machine import Machine


def translate_winding(
    machine: Machine,
) -> tuple[
    swat_em.datamodel,
    list[
        (
            list[list[int] | list[int]]
            | list[list[int] | list[int]]
            | list[list[int] | list[int]]
        )
    ],
]:
    """
    Translates the winding from Pyleecan to PyEMMO.

    Args:
        machine (Machine): The Pyleecan machine.

    Returns:
        tuple: A tuple containing the following elements:

            - ``swat-em.datamodel``: The datamodel object representing the winding.
            - list: A list containing information about the winding in a list of
              lists representing the winding layout for each phase. Each inner
              list contains:

                * List of integers: Positive integers representing active slots.

                * List of integers: Negative integers representing inactive slots.
    """
    # TODO: It might be possible to only return the data model object and
    # then call the 'get_phases()' function directly in 'createParamDict'.
    winding = swat_em.datamodel()
    if machine.stator.winding.qs != 3:
        raise NotImplementedError("Can't handle phase number %i (!=3)")
    winding.genwdg(
        Q=machine.stator.slot.Zs,
        P=machine.stator.winding.p * 2,
        m=machine.stator.winding.qs,
        w=(
            machine.stator.winding.coil_pitch
            if machine.stator.winding.Nlayer > 1
            else -1
        ),
        layers=machine.stator.winding.Nlayer,
        turns=machine.stator.winding.Ntcoil,
    )
    wind_swat = winding.get_phases()
    return winding, wind_swat
