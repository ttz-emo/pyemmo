"""imports"""
from numpy import Inf
from pyleecan.Classes.Material import Material as pyleecanMat
from pyleecan.Classes.MatMagnetics import MatMagnetics
from ...script.material.material import Material


def build_pyemmo_material(pyleecan_material: pyleecanMat) -> Material:
    """Translates a pyleecan-material into a pyemmo-material.

    Args:
        pyleecanMaterial (pyleecanMat): Material in pyleecan format

    Returns:
        Material: Translated material in pyemmo format
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
        # TODO: Abfangen, falls mur_lin und BH nicht gesetzt sind -> Fehler ausgeben. Falls BH gegeben ist, kein mur_lin benötigt.
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
