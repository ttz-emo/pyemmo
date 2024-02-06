"""imports"""
from pyleecan.Classes.Material import Material as pyleecanMat
from ...script.material.material import Material


def build_pyemmo_material(pyleecan_material: pyleecanMat) -> Material:
    """Translates a pyleecan-material into a pyemmo-material.

    Args:
        pyleecanMaterial (pyleecanMat): Material in pyleecan format

    Returns:
        Material: Translated material in pyemmo format
    """
    try:
        conductivity = pyleecan_material.elec.rho
    except AttributeError:
        conductivity = None
    try:
        # TODO: Abfangen, falls mur_lin und BH nicht gesetzt sind -> Fehler ausgeben. Falls BH gegeben ist, kein mur_lin benötigt.
        rel_permeability = pyleecan_material.mag.mur_lin
    except AttributeError:
        rel_permeability = 1.0
    try:
        remanence = pyleecan_material.mag.Brm20
    except AttributeError:
        remanence = None
    try:
        alpha_br = pyleecan_material.mag.alpha_Br
    except AttributeError:
        alpha_br = None
    try:
        bh = pyleecan_material.mag.BH_curve.value
        bh[:, [0, 1]] = bh[:, [1, 0]]
    except AttributeError:
        bh = None
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
