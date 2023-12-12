from typing import List
from math import pi

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
        print(f"\nTranslation for {RotorSurfLabels[i]}:")
        pyemmoSurface, anglePointRefList = translateGeometry(
            nameSplitList=RotorSurfLabelsSplit2[i],
            machine=machine,
            label=RotorSurfLabels[i],
            surface=surf,
            anglePointRefList=anglePointRefList,
        )
        geometryList.append(pyemmoSurface)

    # ----------------------------------------------------
    # Filling the magnetization dict if surface is magnet:
    # ----------------------------------------------------
    # Changing the 'idExt' of the SurfaceAPI to 'Mag0', 'Mag1', 'Mag2', ...
    # if the 'idExt' is 'Mag'
    lplCounter = 0
    for surfAPIRotor in geometryList:
        if surfAPIRotor.idExt == "Lpl":
            surfAPIRotor.setIdExt("Lpl" + str(lplCounter))
            lplCounter += 1
            
    # Changing the 'idExt' of the SurfaceAPI to 'Mag0', 'Mag1', 'Mag2', ...
    # if the 'idExt' is 'Mag'
    magCounter = 0
    for surfAPIRotor in geometryList:
        if surfAPIRotor.idExt == "Mag":
            surfAPIRotor.setIdExt("Mag" + str(magCounter))
            magCounter += 1

    if isinstance(machine, MachineSIPMSM):
        anglePointRef = anglePointRefList[0]
        magnetizationType = machine.rotor.magnet.type_magnetization

        if magnetizationType in (0, 1):  # radial & parallel
            magnetizationAngle = anglePointRef

        elif magnetizationType == 3:  # tangential
            magnetizationAngle = anglePointRef - 90 / pi

        magnetizationDict["Mag0"] = magnetizationAngle

    elif isinstance(machine, MachineIPMSM):
        magAngleDict = machine.rotor.hole[0].comp_magnetization_dict()
        if len(magAngleDict) == 1:
            anglePointRef = anglePointRefList[0]
            magnetizationType = machine.rotor.hole[
                0
            ].magnet_0.type_magnetization

            if magnetizationType in (0, 1):  # radial & parallel
                magnetizationAngle = anglePointRef

            elif magnetizationType == 3:  # tangential
                magnetizationAngle = anglePointRef - 90 / pi

            magnetizationDict["Mag0"] = magnetizationAngle
        else:
            for surfAPIRotor in geometryList:
                if surfAPIRotor.idExt == "Mag0":
                    magnetizationAngle = (
                        anglePointRefList[0] + magAngleDict["magnet_0"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

                elif surfAPIRotor.idExt == "Mag1":
                    magnetizationAngle = (
                        anglePointRefList[1] + magAngleDict["magnet_1"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

                elif surfAPIRotor.idExt == "Mag2":
                    magnetizationAngle = (
                        anglePointRefList[2] + magAngleDict["magnet_2"]
                    )
                    magnetizationDict[surfAPIRotor.idExt] = magnetizationAngle

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
        pyemmoSurface, anglePointRefList = translateGeometry(
            nameSplitList=StatorSurfLabelsSplit2[i],
            machine=machine,
            label=StatorSurfLabels[i],
            surface=surf,
            anglePointRefList=anglePointRefList,
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
