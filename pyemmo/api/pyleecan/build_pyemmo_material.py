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
"""Module: pyemmo_material_conversion"""

from __future__ import annotations

from numpy import inf, empty
from pyleecan.Classes.Material import Material as PyleecanMaterial
from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.Classes.MatElectrical import MatElectrical
from pyleecan.Classes.ImportMatrixVal import ImportMatrixVal

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
        elec_prop: MatElectrical = pyleecan_material.elec  # type: ignore
        conductivity = elec_prop.get_conductivity()
        if not isinstance(conductivity, (int, float)) or conductivity == inf:
            # case when rho = 0
            conductivity = 0.0
    except AttributeError:
        conductivity = 0.0

    # mag props
    mag_properties: MatMagnetics = pyleecan_material.mag  # type: ignore
    try:
        rel_permeability = mag_properties.mur_lin
        assert isinstance(rel_permeability, (int, float)), "mue_r must be a number"
    except AttributeError:
        rel_permeability = 0.0

    try:
        remanence = mag_properties.Brm20
        assert isinstance(remanence, (int, float)), "Br must be a number"

    except AttributeError:
        remanence = 0.0

    try:
        alpha_br = mag_properties.alpha_Br
        assert isinstance(alpha_br, (int, float)), "parameter alpha_Br must be a number"

    except AttributeError:
        alpha_br = 0.0

    try:
        # BH_curve can have type ImportMatrixVal, None
        if mag_properties.BH_curve is None:
            bh = empty(0)
        else:
            assert isinstance(
                mag_properties.BH_curve, ImportMatrixVal
            ), "BH_curve is not of type pyleecan.ImportMatrixVal"
            # switch b and h axis for pyemmo
            # BH_curve.value is a numpy array
            bh = mag_properties.BH_curve.value[:, [1, 0]]  # type: ignore
    except (AssertionError, AttributeError):
        bh = empty(0)
    # struct props
    try:
        density = pyleecan_material.struct.rho  # type: ignore
    except AttributeError:
        density = 0.0
    if bh.size == 0 and not rel_permeability:
        # pylint: disable=locally-disabled, line-too-long
        raise ValueError(
            f"No magnetic properties (mue_r and BH curve) defined in material '{pyleecan_material.name}'"
        )
    assert isinstance(pyleecan_material.name, str)

    pyemmo_material = Material(
        name=pyleecan_material.name,
        conductivity=conductivity,
        relPermeability=rel_permeability,
        remanence=remanence,
        tempCoefRem=alpha_br,
        BH=bh,
        density=density,
        thermalConductivity=0.0,
        thermalCapacity=0.0,
    )

    return pyemmo_material
