import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
from pyemmo.script.geometry.point import Point
# ==========================================
# Definition of function 'buildPyemmoPoint':
# ==========================================
def buildPyemmoPoint(pyleecanPoint):
    """This function translates a ``point`` from ``pyleecan``-format into ``pyemmo``-format.

    Args:
        pyleecanPoint (_type_): _description_

    Returns:
        _type_: _description_
    """
    coords = [pyleecanPoint.real, pyleecanPoint.imag]

    pyemmoPoint = Point(name="test", x=coords[0], y=coords[1], z=0, meshLength=1.0)

    return pyemmoPoint