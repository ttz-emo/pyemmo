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
"""

from __future__ import annotations

import logging

import swat_em
from pyleecan.Classes.Machine import Machine


def translate_winding(machine: Machine) -> swat_em.datamodel:
    """
    Translates the winding from Pyleecan to PyEMMO.

    Args:
        machine (Machine): The Pyleecan machine.

    Returns:
        ``swat-em.datamodel``: The datamodel object representing the winding.
    """
    swat_emm_winding = swat_em.datamodel()
    # FIXME: genwdg() can fail for pyleecan WindingUD. Try to use
    # machine.stator.winding.wind_mat to directly set swatem winding layout.
    swat_emm_winding.genwdg(
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
    wind_swat = swat_emm_winding.get_phases()
    try:
        if wind_swat is None:
            raise RuntimeError(
                f"Could not translate winding of pyleecan machine {machine.name}",
            )
    except RuntimeError as exce:
        logger = logging.getLogger(__name__)
        logger.error(
            "Winding data: Q=%i, p=%i, m=%i, w=%i, layers=%i, turns=%.1f - Pyleecan winding type: %s",
            machine.stator.slot.Zs,
            machine.stator.winding.p,
            machine.stator.winding.qs,
            machine.stator.winding.coil_pitch,
            machine.stator.winding.Nlayer,
            machine.stator.winding.Ntcoil,
            str(type(machine.stator.winding).__name__),
            exc_info=True,
        )
        raise exce
    except Exception as exce:
        raise exce

    return swat_emm_winding
