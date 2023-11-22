import pyleecan.Classes.Arc1
import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from workingDirectory.buildPyemmoPoint import buildPyemmoPoint

# =======================================
# Definition of function 'translateArc1':
# =======================================
def translateArc1(line: pyleecan.Classes.Arc1.Arc1):
    """_summary_

    Args:
        line (pyleecan.Classes.Arc1.Arc1): _description_

    Returns:
        _type_: _description_
    """
    # Translation for Pyleecan Arc1 to Pyemmo CircleArc
    # (An arc between two points (defined by a radius)):

    startPoint = buildPyemmoPoint(line.begin)
    endPoint = buildPyemmoPoint(line.end)
    centerPoint = buildPyemmoPoint(line.get_center())

    return startPoint, endPoint, centerPoint