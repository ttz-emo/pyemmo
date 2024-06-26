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
"""Module: pyemmo_material_conversion"""

from __future__ import annotations
from numpy import Inf
from pyleecan.Classes.Material import Material as PyleecanMaterial
from pyleecan.Classes.MatMagnetics import MatMagnetics
from ...script.material.material import Material


def build_pyemmo_material(pyleecan_material: PyleecanMaterial) -> Material:
    """Translates a pyleecan material into a pyemmo material.

    This function translates a pyleecan material into a pyemmo material.

    Args:
        pyleecan_material (PyleecanMaterial): The pyleecan material to be translated.

    Returns:
        Material: The translated pyemmo material.

    Notes:
        - Conductivity, relPermeability, remanence, tempCoefRem, BH, and density
          are extracted from the pyleecan material to construct the pyemmo material.
        - If any attribute is missing from the pyleecan material, it is set to None
          in the pyemmo material.

    """
    # elec props
    try:
        conductivity = pyleecan_material.elec.get_conductivity()
        if conductivity is Inf:
            # case when rho = 0
            conductivity = None
    except AttributeError:
        conductivity = None

    # mag props
    mag_properties: MatMagnetics = pyleecan_material.mag
    try:
        rel_permeability = mag_properties.mur_lin
    except AttributeError:
        rel_permeability = None

    try:
        remanence = mag_properties.Brm20
    except AttributeError:
        remanence = None

    try:
        alpha_br = mag_properties.alpha_Br
    except AttributeError:
        alpha_br = None

    try:
        # switch b and h axis for pyemmo
        bh = mag_properties.BH_curve.value[:, [1, 0]]
    except AttributeError:
        bh = None
    # struct props
    try:
        density = pyleecan_material.struct.rho
    except AttributeError:
        density = None
    if bh is None and rel_permeability is None:
        # pylint: disable=locally-disabled, line-too-long
        raise ValueError(
            f"No magnetic properties (mue_r and BH curve) defined in material '{pyleecan_material.name}'"
        )
    pyemmo_material = Material(
        name=pyleecan_material.name,
        conductivity=conductivity,
        relPermeability=rel_permeability,
        remanence=remanence,
        tempCoefRem=alpha_br,
        BH=bh,
        density=density,
        thermalConductivity=None,
        thermalCapacity=None,
    )

    return pyemmo_material
