from typing import Union

from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSCIM import MachineSCIM

from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.point import Point
from .getRotorStatorSurfaces import getRotorSurfaces
from .calcsSPMSMContour import calcSPMSMRotorContour
from .calcIPMSMContour import calcIPMSMRotorContour
from .calcWindContour import calcWindContour


def getSPMSMRotorContour(
    geometryList: list, machine: Machine, isInternalRotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Get a list of curves of the contour of the rotor with a surfacemagnet. 

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        machine (Machine): Pyleecan machine
        isInternalRotor (bool, optional): Internal or external Rotor. Defaults to True.

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: _description_
    """

    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext

    rotorLamSurfList, rotorMagSurfList = getRotorSurfaces(
        geometryList=geometryList
    )
    
    if isInternalRotor:
        (
            rotorContourLineList,
            rPointRotorCont,
            lPointRotorCont,
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
            rPointRotorCont,
            lPointRotorCont,
        ) = calcSPMSMRotorContour(
            machine=machine,
            rotorLamSurfList=rotorLamSurfList,
            rotorMagSurfList=rotorMagSurfList,
            radius=rotorRext,
            isInternalRotor=isInternalRotor,
        )

    return rotorContourLineList, rPointRotorCont, lPointRotorCont


def getIPMSMRotorContour(
    geometryList: list, machine: Machine, isInternalRotor: bool = True
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Get a list of curves of the contour of the rotor with a interior magnets. ``rotorContourLineList``

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        machine (Machine): Pyleecan machine
        isInternalRotor (bool, optional): Internal or external Rotor. Defaults to True.

    Returns:
        list[Line, CircleArc]: _description_
    """

    rotorRint = machine.rotor.Rint
    rotorRext = machine.rotor.Rext

    rotorLamSurfList = []
    
    for surf in geometryList:
        if surf.idExt == "Pol":
            rotorLamSurfList.append(surf)
            
    if isInternalRotor:
        (
            rotorContourLineList,
            rPointRotorCont,
            lPointRotorCont,
        ) = calcIPMSMRotorContour(
            rotorLamSurfList=rotorLamSurfList,
            radius=rotorRint,
        )
    else:
        (
            rotorContourLineList,
            rPointRotorCont,
            lPointRotorCont,
        ) = calcIPMSMRotorContour(
            rotorLamSurfList=rotorLamSurfList,
            radius=rotorRext,
        )

    return rotorContourLineList, rPointRotorCont, lPointRotorCont


def getWindingContour(
    geometryList: list, machine: Machine, isInternalRotor: bool
) -> list[Union[Line, CircleArc]]:
    """Get a list of curves of the contour of the lamination with a winding.

    Args:
        geometryList (list): _description_
        machine (Machine): _description_
        isInternalRotor (bool): _description_

    Returns:
        list[Union[Line, CircleArc]]: _description_
    """
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
