import sys
from os.path import join

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
from typing import List

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from workingDirectory.translateGeometry import translateGeometry

# ===========================================
# Definition of function 'createGeoDict':
# ===========================================
def createGeoDict():
    Toyota_Prius = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
    # Import SPMSM:
    SPMSM_motor = load(join(DATA_DIR, "Machine", "SPMSM_002.json"))
    # Import ASM:
    SCIM_motor = load(join(DATA_DIR, "Machine", "SCIM_L2EP_48s_2p.json"))
    RotorSurf = Toyota_Prius.rotor.build_geometry(sym=2, alpha=0)
    StatorSurf = Toyota_Prius.stator.build_geometry(sym=2, alpha=0)

    RotorSurfLabels = []
    StatorSurfLabels = []
    RotorSurfLabelsSplit1 = []
    StatorSurfLabelsSplit1 = []
    RotorSurfLabelsSplit2 = []
    StatorSurfLabelsSplit2 = []

    testList: List[SurfaceAPI] = []

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
        testList.append(
            translateGeometry(
                bauteil=RotorSurfLabelsSplit2[i][0],
                detail=RotorSurfLabelsSplit2[i][2],
                motor=Toyota_Prius,
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
        testList.append(
            translateGeometry(
                bauteil=StatorSurfLabelsSplit2[i][0],
                detail=StatorSurfLabelsSplit2[i][2],
                motor=Toyota_Prius,
                label=StatorSurfLabels[i],
                surface=StatorSurf[i],
            )
        )

    print("===============================")
    print("End of Translation for Stator.")
    print("===============================")
    print("End of Translation for machine.")
    print("===============================")

    plot(testList)

createGeoDict()