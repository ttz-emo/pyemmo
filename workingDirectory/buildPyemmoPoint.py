import sys
from pyemmo.script.geometry.point import Point

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

# ==========================================
# Definition of funciton 'buildPyemmoPoint':
# ==========================================
def buildPyemmoPoint(pyleecanPoint):
    """_summary_

    Args:
        pyleecanPoint (_type_): _description_

    Returns:
        _type_: _description_
    """
    coords = [pyleecanPoint.real, pyleecanPoint.imag]

    pyemmoPoint = Point(name="test", x=coords[0], y=coords[1], z=0, meshLength=1.0)

    return pyemmoPoint