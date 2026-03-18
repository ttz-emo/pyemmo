#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
Define function :func:`~pyemmo.api.pyleecan.build_pyemmo_material.build_pyemmo_material`
to convert PYLEECAN materials to pyemmo materials.
"""

from __future__ import annotations

import logging

from numpy import empty, inf
from pyleecan.Classes.ImportMatrixVal import ImportMatrixVal
from pyleecan.Classes.MatElectrical import MatElectrical
from pyleecan.Classes.Material import Material as PyleecanMaterial
from pyleecan.Classes.MatMagnetics import MatMagnetics

from ...script.material.material import Material

try:
    # try to load PYLEECAN copper material to catch error with copper1
    from os.path import join

    from pyleecan.definitions import DATA_DIR
    from pyleecan.Functions.load import load  # pylint: disable=no-name-in-module

    copper1: PyleecanMaterial = load(join(DATA_DIR, "Material", "Copper1.json"))
    copper2: PyleecanMaterial = load(join(DATA_DIR, "Material", "Copper2.json"))
except Exception:  # pylint: disable=W0718
    copper1 = None
    copper2 = None


# FIXME: Need to implement ElectricalSteel creation for loss data and lamination thickness!
def build_pyemmo_material(pyleecan_material: PyleecanMaterial) -> Material:
    """Translates a PYLEECAN material into a pyemmo material.

    This function translates a PYLEECAN material into a pyemmo material.

    Args:
        pyleecan_material (PyleecanMaterial): The PYLEECAN material to be translated.

    Returns:
        Material: The translated pyemmo material.

    Notes:
        - Conductivity, relPermeability, remanence, tempCoefRem, BH, and density
          are extracted from the PYLEECAN material to construct the pyemmo material.
        - If any attribute is missing from the PYLEECAN material, it is set to its
          default value in the pyemmo material.

    """
    logger = logging.getLogger(__name__)
    if "Copper1" in pyleecan_material.name and copper2 is not None:
        # TODO: Check if material really missing magnetic properies
        logger.warning(
            "Material 'Copper1' used without magnetic properties. "
            "Replacing it with PYLEECAN default material 'Copper2'"
        )
        pyleecan_material = copper2
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
    if mag_properties is None:
        raise ValueError(
            f"No magnetic properties in PYLEECAN material {pyleecan_material.name}. "
            "Please set with `material.mag = MatMagnetics(...)`"
        )
    try:
        rel_permeability = mag_properties.mur_lin
        if rel_permeability is None:
            rel_permeability = 1.0
        else:
            assert isinstance(rel_permeability, (int, float)), "mue_r must be a number"
    except AttributeError:
        rel_permeability = 1.0

    try:
        remanence = mag_properties.Brm20
        if remanence is None:
            remanence = 0
        else:
            assert isinstance(remanence, (int, float)), "Br must be a number"
    except AttributeError:
        remanence = 0.0

    try:
        alpha_br = mag_properties.alpha_Br
        if alpha_br is None:
            alpha_br = 0.0
        else:
            assert isinstance(
                alpha_br, (int, float)
            ), "parameter alpha_Br must be a number"

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
        if density is None:
            density = 0.0
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
