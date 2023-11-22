import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    
from pyemmo.script.material.material import Material

# =============================================
# Definition of function 'buildPyemmoMaterial':
# =============================================
def buildPyemmoMaterial(pyleecanMaterial):
    """_summary_

    Args:
        pyleecanMaterial (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        conductivity = pyleecanMaterial.elec.rho
    except AttributeError:
        conductivity = None
    try:
        relPermeability = pyleecanMaterial.mag.mur_lin
    except AttributeError:
        relPermeability = None
    try:
        remanence = pyleecanMaterial.mag.Brm20
    except AttributeError:
        remanence = None
    try:
        alphaBr = pyleecanMaterial.mag.alpha_Br
    except AttributeError:
        alphaBr = None
    try:
        BH = pyleecanMaterial.mag.BH_curve.value
    except AttributeError:
        BH = None
    try:
        density = pyleecanMaterial.struct.rho
    except AttributeError:
        density = None

    pyemmoMaterial = Material(
        name=pyleecanMaterial.desc,
        conductivity=conductivity,
        relPermeability=relPermeability,
        remanence=remanence,
        tempCoefRem=alphaBr,
        BH=BH,
        density=density,
        thermalConductivity=None,
        thermalCapacity=None,
    )
    return pyemmoMaterial
