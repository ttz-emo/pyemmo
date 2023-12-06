import sys

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

import pyleecan.Classes.Segment
import pyleecan.Classes.Arc1
import pyleecan.Classes.Arc2
import pyleecan.Classes.Arc3
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from .buildPyemmoPoint import buildPyemmoPoint
from .translateArc1 import translateArc1
from .translateArc2 import translateArc2
from .translateArc3 import translateArc3

# =============================================
# Definition of function 'buildPyemmoLineList':
# =============================================
def buildPyemmoLineList(pyleecanLineList):
    """_summary_

    Args:
        pyleecanLineList (_type_): _description_

    Returns:
        _type_: _description_
    """
    pyemmoLineList = []
    returnlist = []
    for line in pyleecanLineList:
        if isinstance(line, pyleecan.Classes.Segment.Segment):
            pyemmoLineList = Line(
                # name=list(line.prop_dict.values())[0],
                name="test",
                startPoint=buildPyemmoPoint(line.begin),
                endPoint=buildPyemmoPoint(line.end),
            )
            returnlist.append(pyemmoLineList)
        elif isinstance(line, pyleecan.Classes.Arc1.Arc1):
            startPoint, endPoint, centerPoint = translateArc1(line=line)

            # Erzeugung des Kreisobjekts
            pyemmoLineList = CircleArc(
                name="test",
                startPoint=startPoint,
                endPoint=endPoint,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)

        elif isinstance(line, pyleecan.Classes.Arc2.Arc2):
            startPoint, endPoint, centerPoint = translateArc2(line=line)
            pyemmoLineList = CircleArc(
                name="test",
                startPoint=startPoint,
                endPoint=endPoint,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)

        elif isinstance(line, pyleecan.Classes.Arc3.Arc3):
            startPoint, endPoint, centerPoint, centerPointArc = translateArc3(line=line)
            pyemmoLineList = CircleArc(
                name="test",
                startPoint=startPoint,
                endPoint=centerPointArc,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)
            pyemmoLineList = CircleArc(
                name="test",
                startPoint=centerPointArc,
                endPoint=endPoint,
                centerPoint=centerPoint,
            )
            returnlist.append(pyemmoLineList)

    return returnlist