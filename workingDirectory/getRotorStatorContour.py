from typing import Union

from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSCIM import MachineSCIM

from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from .getRotorStatorSurfaces import getRotorSurfaces
from .calcsSPMSMContour import calcSPMSMRotorContour

# from .calcIPMSMContour import calcIPMSMRotorContour
from .calcWindContour import calcWindContour


def getSurfMagContour(
    geometryList: list, machine: Machine, isInternalRotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Get a list of curves of the contour of the rotor with a surfacemagnet. ``rotorContourLineList``

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        machine (Machine): Pyleecan machine
        isInternalRotor (bool, optional): Internal or external Rotor. Defaults to True.

    Returns:
        list[Line, CircleArc]: _description_
    """

    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext

    rotorLamSurfList, rotorMagSurfList = getRotorSurfaces(geometryList=geometryList)
    if isInternalRotor:
        (
            rotorContourLineList,
            lowestYPointRotor,
            biggestYPointRotor,
        ) = calcSPMSMRotorContour(
            machine=machine,
            rotorLamSurfList=rotorLamSurfList,
            rotorMagSurfList=rotorMagSurfList,
            radius=rotorRint,
            isInternalRotor=isInternalRotor,
        )
    else:
        (
            rotorContourLineList,
            lowestYPointRotor,
            biggestYPointRotor,
        ) = calcSPMSMRotorContour(
            machine=machine,
            rotorLamSurfList=rotorLamSurfList,
            rotorMagSurfList=rotorMagSurfList,
            radius=rotorRext,
            isInternalRotor=isInternalRotor,
        )

    return rotorContourLineList, lowestYPointRotor, biggestYPointRotor


def getWindingContour(geometryList: list, machine: Machine, isInternalRotor: bool):
    statorRint = machine.stator.Rint
    statorRext = machine.stator.Rext
    if isInternalRotor:
        statorContourLineList = calcWindContour(
            geometryList=geometryList,
            statorRint=statorRint,
            statorRext=statorRext,
        )
    elif isinstance(machine, MachineSCIM):
        pass
    else:
        statorContourLineList = calcWindContour(
            geometryList=geometryList,
            statorRint=statorRext,
            statorRext=statorRint,
        )

    return statorContourLineList
