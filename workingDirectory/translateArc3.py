import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

import pyleecan.Classes.Arc3
from .build_pyemmo_point import build_pyemmo_point


# =======================================
# Definition of function 'translateArc3':
# =======================================
def translateArc3(line: pyleecan.Classes.Arc3.Arc3):
    """_summary_

    Args:
        line (pyleecan.Classes.Arc3.Arc3): _description_

    Returns:
        _type_: _description_
    """
    # Calculation for Arc3(Half circle define by two points))
    # Berechnung des Mittelpunkts eines Halbkreises
    startPoint = build_pyemmo_point(line.begin)
    endPoint = build_pyemmo_point(line.end)
    centerPoint = build_pyemmo_point(line.get_center())
    centerArcPoint = build_pyemmo_point(line.get_middle())

    return startPoint, endPoint, centerPoint, centerArcPoint
