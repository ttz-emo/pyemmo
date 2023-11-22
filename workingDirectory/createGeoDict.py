import sys
from os.path import join
from typing import List
import math

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
from pyleecan.Classes.MachineIPMSM import MachineIPMSM

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from workingDirectory.translateGeometry import translateGeometry
from workingDirectory.getRotorStatorContour import getRotorContour, getStatorContour

# from workingDirectory.buildPyemmoMovingBand import buildPyemmoMovingBand


# ===========================================
# Definition of function 'createGeoDict':
# ===========================================
def createGeoDict(machine):
    """_summary_

    Args:
        machine (_type_): _description_
    """

    RotorSurf = machine.rotor.build_geometry(sym=machine.rotor.slot.Zs, alpha=0)
    StatorSurf = machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)

    RotorSurfLabels = []
    StatorSurfLabels = []
    RotorSurfLabelsSplit1 = []
    StatorSurfLabelsSplit1 = []
    RotorSurfLabelsSplit2 = []
    StatorSurfLabelsSplit2 = []

    geometryList: List[SurfaceAPI] = []

    # =======================================
    # Loop of translation for rotor surfaces:
    # =======================================
    for i, surf in enumerate(RotorSurf):
        saveSpaceTemp = []
        RotorSurfLabelsSplit1 = []
        RotorSurfLabels.append(surf.label)
        RotorSurfLabelsSplit1.extend(surf.label.split("_"))

        for ii, split1 in enumerate(RotorSurfLabelsSplit1):
            saveSpaceTemp.extend(split1.split("-"))
        RotorSurfLabelsSplit2.append(saveSpaceTemp)
        print(f"\nTranslation for {RotorSurfLabels[i]}:")
        geometryList.append(
            translateGeometry(
                bauteil=RotorSurfLabelsSplit2[i][0],
                detail=RotorSurfLabelsSplit2[i][2],
                motor=machine,
                label=RotorSurfLabels[i],
                surface=RotorSurf[i],
            )
        )
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

        for ii, split1 in enumerate(StatorSurfLabelsSplit1):
            saveSpaceTemp.extend(split1.split("-"))

        StatorSurfLabelsSplit2.append(saveSpaceTemp)
        print(f"\nTranslation for {StatorSurfLabels[i]}:")
        geometryList.append(
            translateGeometry(
                bauteil=StatorSurfLabelsSplit2[i][0],
                detail=StatorSurfLabelsSplit2[i][2],
                motor=machine,
                label=StatorSurfLabels[i],
                surface=StatorSurf[i],
            )
        )

    # ===========================
    # CutOuts in rotorLamination:
    # ===========================
    if isinstance(machine, MachineIPMSM):
        for k, surfToCutOut in enumerate(geometryList):
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

    print("getRotorContour:")
    rotorContourLineList = getRotorContour(geometryList=geometryList, machine=machine)
    statorContourLineList = getStatorContour(geometryList=geometryList, machine=machine)
    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------
    rotorRint = machine.rotor.Rint
    statorRext = machine.stator.Rext
    if rotorRint > 0:
        isShaft = True
    else:
        isShaft = False

    for a, surf in enumerate(geometryList):
        for b, curve in enumerate(surf.curve):
            if isShaft:
                if math.isclose(
                    a=curve.startPoint.radius, b=rotorRint, abs_tol=1e-6
                ) and math.isclose(a=curve.endPoint.radius, b=rotorRint, abs_tol=1e-6):
                    curve.name = "InnerLimit"
            if math.isclose(
                a=curve.startPoint.radius, b=statorRext, abs_tol=1e-6
            ) and math.isclose(a=curve.endPoint.radius, b=statorRext, abs_tol=1e-6):
                curve.name = "OuterLimit"
                
    return geometryList, rotorContourLineList, statorContourLineList
