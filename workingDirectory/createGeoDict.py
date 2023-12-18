from typing import List, Union
import logging

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Machine import Machine

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from .translateGeometry import translateGeometry
from .getRotorStatorContour import (
    getSPMSMRotorContour,
    getWindingContour,
    getIPMSMRotorContour,
)
from .detectInnerOuterLimit import detectInnerOuterLimit
from .getMagnetizationDict import getMagnetizationDict


def createGeoDict(
    machine: Machine,
    isInternalRotor: bool,
) -> tuple[
    list[SurfaceAPI],
    list[Union[Line, CircleArc]],
    list[Union[Line, CircleArc]],
    Point,
    Point,
    dict,
]:
    """_summary_

    Args:
        machine (Machine): _description_
        rotorSym (int): _description_
        statorSym (int): _description_
        isInternalRotor (bool): _description_

    Raises:
        TypeError: _description_

    Returns:
        tuple[ list[SurfaceAPI], list[Union[Line, CircleArc]], list[Union[Line, CircleArc]], Point, Point, dict, ]: _description_
    """
    # TODO: Funktion heißt createGeoDict aber gibt Liste zurück...
    rotorSym = machine.rotor.comp_periodicity_geo()[0]
    statorSym = machine.stator.slot.Zs
    RotorSurf = machine.rotor.build_geometry(sym=rotorSym, alpha=0)
    StatorSurf = machine.stator.build_geometry(sym=statorSym, alpha=0)

    RotorSurfLabels = []
    StatorSurfLabels = []
    RotorSurfLabelsSplit1 = []
    StatorSurfLabelsSplit1 = []
    RotorSurfLabelsSplit2 = []
    StatorSurfLabelsSplit2 = []

    geometryList: List[SurfaceAPI] = []
    magnetizationDict = {}
    anglePointRefList = []

    rotorRint = machine.rotor.Rint
    statorRext = machine.stator.Rext

    # =======================================
    # Loop of translation for rotor surfaces:
    # =======================================
    for i, surf in enumerate(RotorSurf):
        saveSpaceTemp = []
        RotorSurfLabelsSplit1 = []
        RotorSurfLabels.append(surf.label)
        RotorSurfLabelsSplit1.extend(surf.label.split("_"))

        for split1 in RotorSurfLabelsSplit1:
            saveSpaceTemp.extend(split1.split("-"))
        RotorSurfLabelsSplit2.append(saveSpaceTemp)

        logging.debug("Geometry translation for %s:", RotorSurfLabels[i])

        pyemmoSurface, anglePointRefList = translateGeometry(
            nameSplitList=RotorSurfLabelsSplit2[i],
            machine=machine,
            label=RotorSurfLabels[i],
            surface=surf,
            anglePointRefList=anglePointRefList,
        )
        geometryList.append(pyemmoSurface)

    magnetizationDict = getMagnetizationDict(
        machine=machine,
        anglePointRefList=anglePointRefList,
        geometryList=geometryList,
        magnetizationDict=magnetizationDict
    )

    logging.debug("=============================")
    logging.debug("End of Translation for Rotor.")

    # ============================================
    # CutOuts in rotorLamination if IPMSM or SyRM:
    # ============================================
    if isinstance(machine, (MachineIPMSM, MachineSyRM)):
        for surfToCutOut in geometryList:
            if surfToCutOut.name != "Rotor-0_Lamination":
                surfToCutOutSplit = surfToCutOut.name.split("-")
                if surfToCutOutSplit[0] == "Rotor":
                    geometryList[0].cutOut(surfToCutOut)

    # ========================================
    # Loop of translation for stator surfaces:
    # ========================================
    for i, surf in enumerate(StatorSurf):
        saveSpaceTemp = []
        StatorSurfLabelsSplit1 = []
        StatorSurfLabels.append(surf.label)
        StatorSurfLabelsSplit1.extend(surf.label.split("_"))
        for split1 in StatorSurfLabelsSplit1:
            saveSpaceTemp.extend(split1.split("-"))

        StatorSurfLabelsSplit2.append(saveSpaceTemp)

        logging.debug("Translation for %s", StatorSurfLabels[i])

        pyemmoSurface, anglePointRefList = translateGeometry(
            nameSplitList=StatorSurfLabelsSplit2[i],
            machine=machine,
            label=StatorSurfLabels[i],
            surface=surf,
            anglePointRefList=anglePointRefList,
        )
        geometryList.append(pyemmoSurface)

    logging.debug("===============================")
    logging.debug("End of Translation for Stator. ")
    logging.debug("===============================")
    logging.debug("End of Translation for machine.")
    logging.debug("===============================")

    plot(geoList=geometryList, linewidth=1, markersize=3)

    logging.debug("Plot of machine")
    logging.debug("End of function")
    logging.debug("===============")

    # --------------------------------------
    # Generate the rotor and stator contour:
    # --------------------------------------
    logging.debug("Generating rotor and stator contour")
    if isinstance(machine, (MachineIPMSM, MachineSyRM)):
        (
            rotorContourLineList,
            lowestYPointRotor,
            biggestYPointRotor,
        ) = getIPMSMRotorContour(
            geometryList=geometryList,
            machine=machine,
            isInternalRotor=isInternalRotor,
        )
        statorContourLineList = getWindingContour(
            geometryList=geometryList,
            machine=machine,
            isInternalRotor=isInternalRotor,
        )
    elif isinstance(machine, MachineSIPMSM):
        (
            rotorContourLineList,
            lowestYPointRotor,
            biggestYPointRotor,
        ) = getSPMSMRotorContour(
            geometryList=geometryList,
            machine=machine,
            isInternalRotor=isInternalRotor,
        )
        statorContourLineList = getWindingContour(
            geometryList=geometryList,
            machine=machine,
            isInternalRotor=isInternalRotor,
        )
    else:
        raise TypeError("Unable to generate contours of this machine type!")

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    isShaft = bool(rotorRint > 0)

    if isInternalRotor:
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList,
            innerRadius=rotorRint,
            outerRadius=statorRext,
            isShaft=isShaft,
        )
    else:
        rotorRext = machine.rotor.Rext
        statorRint = machine.stator.Rint
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList,
            innerRadius=statorRint,
            outerRadius=rotorRext,
            isShaft=isShaft,
        )

    return (
        geometryList,
        rotorContourLineList,
        statorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
        magnetizationDict,
    )
