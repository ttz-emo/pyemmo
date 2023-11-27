import math
import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from .buildPyemmoPoint import buildPyemmoPoint
from pyemmo.script.geometry.point import Point
import pyleecan.Classes.Arc2

# =======================================
# Definition of function 'translateArc2':
# =======================================
def translateArc2(line: pyleecan.Classes.Arc2.Arc2):
    """_summary_

    Args:
        line (pyleecan.Classes.Arc2.Arc2): _description_

    Returns:
        _type_: _description_
    """
    # Calculation for Arc2
    # (An arc between two points (defined by the begin  point and a center and angle))

    startPoint = buildPyemmoPoint(line.begin)
    centerPoint = buildPyemmoPoint(line.center)
    # FIXME: namen von centerpoint in der klammer überprüfen, ob er mit der von pyleecan übereinstimmt

    # Berechnung des Endpunkts des Kreisbogens
    angleRad = line.get_angle()
    endPoint_x = (
        centerPoint.coordinate[0]
        + (startPoint.coordinate[0] - centerPoint.coordinate[0]) * math.cos(angleRad)
        - (startPoint.coordinate[1] - centerPoint.coordinate[1]) * math.sin(angleRad)
    )
    endPoint_y = (
        centerPoint.coordinate[1]
        + (startPoint.coordinate[0] - centerPoint.coordinate[0]) * math.sin(angleRad)
        + (startPoint.coordinate[1] - centerPoint.coordinate[1]) * math.cos(angleRad)
    )
    endPoint = Point(name="endPoint", x=endPoint_x, y=endPoint_y, z=0, meshLength=1.0)

    return startPoint, endPoint, centerPoint