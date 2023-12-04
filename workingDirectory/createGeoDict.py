import sys
from os.path import join
from typing import List
import math


from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.Machine import Machine

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from .translateGeometry import translateGeometrySPMSM, buildGeoSPMSM
from .getRotorStatorContour import (
    getSurfMagContour,
    getWindingContour,
    # getIPMSMRotorContour,
)

# from workingDirectory.buildPyemmoMovingBand import buildPyemmoMovingBand


# ===========================================
# Definition of function 'createGeoDict':
# ===========================================
def createGeoDictSPMSM(
    machine: Machine,
    rotorSym: int,
    statorSym: int,
    isInternalRotor: bool,
    magnetFarthestRadius: float,
    magnetShortestRadius: float,
):
    """_summary_

    Args:
        machine (Machine): _description_
        rotorSym (int): _description_
        statorSym (int): _description_
        isInternalRotor (bool): _description_
        magnetFarthestRadius (float): _description_
        magnetShortestRadius (float): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """

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
        print(f"\nTranslation for {RotorSurfLabels[i]}:")
        pyemmoSurface, magnetizationDict = buildGeoSPMSM(
            bauteil=RotorSurfLabelsSplit2[i][0],
            detail=RotorSurfLabelsSplit2[i][2],
            machine=machine,
            label=RotorSurfLabels[i],
            surface=surf,
            magnetizationDict=magnetizationDict,
        )
        geometryList.append(pyemmoSurface)
    print("=============================")
    print("End of Translation for Rotor.")

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
        print(f"\nTranslation for {StatorSurfLabels[i]}:")
        pyemmoSurface, magnetizationDict = buildGeoSPMSM(
            bauteil=StatorSurfLabelsSplit2[i][0],
            detail=StatorSurfLabelsSplit2[i][2],
            machine=machine,
            label=StatorSurfLabels[i],
            surface=StatorSurf[i],
            magnetizationDict=magnetizationDict,
        )
        geometryList.append(pyemmoSurface)

    # ===========================
    # CutOuts in rotorLamination:
    # ===========================
    if isinstance(machine, MachineIPMSM):
        for surfToCutOut in geometryList:
            if surfToCutOut.name != "Rotor-0_Lamination":
                surfToCutOutSplit = surfToCutOut.name.split("-")
                if surfToCutOutSplit[0] == "Rotor":
                    geometryList[0].cutOut(surfToCutOut)

    print("===============================")
    print("End of Translation for Stator. ")
    print("===============================")
    print("End of Translation for machine.")
    print("===============================")

    plot(geoList=geometryList, linewidth=1, markersize=3)

    print("Plot of machine")
    print("End of function")
    print("===============")

    # -------------------------------------------
    # Generation of the rotor and stator contour:
    # -------------------------------------------
    print("Generate rotor and stator contour:")
    if isinstance(machine, MachineIPMSM):
        rotorContourLineList = getIPMSMRotorContour(
            geometryList=geometryList, machine=machine, isInternalRotor=isInternalRotor
        )
        statorContourLineList = getWindingContour(
            geometryList=geometryList, machine=machine, isInternalRotor=isInternalRotor
        )
    elif isinstance(machine, MachineSIPMSM):
        rotorContourLineList, lowestYPointRotor, biggestYPointRotor = getSurfMagContour(
            geometryList=geometryList, machine=machine, isInternalRotor=isInternalRotor
        )
        statorContourLineList = getWindingContour(
            geometryList=geometryList, machine=machine, isInternalRotor=isInternalRotor
        )
    else:
        raise TypeError("Unable to translate machine type!")

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------
    rotorRint = machine.rotor.Rint
    statorRext = machine.stator.Rext

    if rotorRint > 0:
        isShaft = True
    else:
        isShaft = False

    def detectInnerOuterLimit(
        geometryList: list[SurfaceAPI], rotorRint: float, statorRext: float
    ) -> list[SurfaceAPI]:
        """Overwrites the name of the curve, if its the most outlying curve (-> ``OuterLimit``) or the most innerlying curve (-> ``InnerLimit``).

        Attention when making the function call:\n
        If the machine has an external rotor:\n
        ``rotorRint`` replaced with ``statorRint``\n
        ``statorRext`` replaced with ``rotorRext``

        Args:
            geometryList (list[SurfaceAPI]): list of the machine surfaces
            rotorRint (float): inner radius of the rotor
            statorRext (float): outer radius of the stator

        Returns:
            list[SurfaceAPI]: _description_
        """
        for surf in geometryList:
            for curve in surf.curve:
                if isShaft:
                    if math.isclose(
                        a=curve.startPoint.radius, b=rotorRint, abs_tol=1e-6
                    ) and math.isclose(
                        a=curve.endPoint.radius, b=rotorRint, abs_tol=1e-6
                    ):
                        curve.name = "InnerLimit"
                if math.isclose(
                    a=curve.startPoint.radius, b=statorRext, abs_tol=1e-6
                ) and math.isclose(a=curve.endPoint.radius, b=statorRext, abs_tol=1e-6):
                    curve.name = "OuterLimit"
        return geometryList

    if isInternalRotor:
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList, rotorRint=rotorRint, statorRext=statorRext
        )
    else:
        rotorRext = machine.rotor.Rext
        statorRint = machine.stator.Rint
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList, rotorRint=statorRint, statorRext=rotorRext
        )

    return (
        geometryList,
        rotorContourLineList,
        statorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
    )
