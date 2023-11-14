def getRotorSurfaces(geometryList):
    """Filter the rotor-surfaces in ``lamination`` and ``magnet`` via surface name.

    Args:
        geometryList (_type_): _description_

    Returns:
        _type_: _description_
    """
    # =========================================
    # Zuweisung der Surfaces zu den Kategorien:
    # =========================================
    rotorLamSurfList = []
    rotorMagSurfList = []
    for i, surf in enumerate(geometryList):
        surfNameSplit = []
        surfSplit = surf.name.split("-")

        for u, split in enumerate(surfSplit):
            surfNameSplit.extend(split.split("_"))

        if surfNameSplit[0] == "Rotor" and surfNameSplit[2] == "Lamination":
            rotorLamSurfList.append(surf)
            print("rotorLamSurf:")
            print(f"gefunden: {surf.name}")

        elif surfNameSplit[0] == "Rotor" and surfNameSplit[2] == "Magnet":
            rotorMagSurfList.append(surf)
            print("rotorMagSurf:")
            print(f"gefunden: {surf.name}")

    return rotorLamSurfList, rotorMagSurfList

def getStatorSurfaces(geometryList):
    """Filter the stator-surfaces in ``lamination`` and ``winding`` via surface name.

    Args:
        geometryList (_type_): _description_

    Returns:
        _type_: _description_
    """
    # =========================================
    # Zuweisung der Surfaces zu den Kategorien:
    # =========================================
    statorLamSurfList = []
    statorWindSurfList = []
    for i, surf in enumerate(geometryList):
        surfNameSplit = []
        surfSplit = surf.name.split("-")

        for u, split in enumerate(surfSplit):
            surfNameSplit.extend(split.split("_"))

        if surfNameSplit[0] == "Stator" and surfNameSplit[2] == "Lamination":
            statorLamSurfList.append(surf)
            print("statorLamSurf:")
            print(f"gefunden: {surf.name}")

        # elif surfNameSplit[0] == "Rotor" and surfNameSplit[2] == "Magnet":
        #     statorWindSurfList.append(surf)
        #     print("rotorMagSurf:")
        #     print(f"gefunden: {surf.name}")

    return statorLamSurfList