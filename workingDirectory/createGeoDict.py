from typing import List

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.Machine import Machine

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from .translateGeometry import translateGeometry
from .getRotorStatorContour import (
    getSurfMagContour,
    getWindingContour,
    getIPMSMContour,
)
from .detectInnerOuterLimit import detectInnerOuterLimit

def createGeoDict(
    machine: Machine,
    rotorSym: int,
    statorSym: int,
    isInternalRotor: bool,
):
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
        print(f"\nTranslation for {RotorSurfLabels[i]}:")
        pyemmoSurface, magnetizationDict = translateGeometry(
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
        pyemmoSurface, magnetizationDict = translateGeometry(
            bauteil=StatorSurfLabelsSplit2[i][0],
            detail=StatorSurfLabelsSplit2[i][2],
            machine=machine,
            label=StatorSurfLabels[i],
            surface=surf,
            magnetizationDict=magnetizationDict,
        )
        geometryList.append(pyemmoSurface)

    # =====================================
    # CutOuts in rotorLamination if IPMSM:
    # =====================================
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
        (
            rotorContourLineList,
            lowestYPointRotor,
            biggestYPointRotor,
        ) = getIPMSMContour(
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
        ) = getSurfMagContour(
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
        raise TypeError("Unable to translate machine type!")

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    isShaft = bool(rotorRint > 0)

    if isInternalRotor:
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList,
            rotorRint=rotorRint,
            statorRext=statorRext,
            isShaft=isShaft,
        )
    else:
        rotorRext = machine.rotor.Rext
        statorRint = machine.stator.Rint
        geometryList = detectInnerOuterLimit(
            geometryList=geometryList,
            rotorRint=statorRint,
            statorRext=rotorRext,
            isShaft=isShaft,
        )

    return (
        geometryList,
        rotorContourLineList,
        statorContourLineList,
        lowestYPointRotor,
        biggestYPointRotor,
    )
