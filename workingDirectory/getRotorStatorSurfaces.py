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
    
    for surf in geometryList:
        if surf.idExt == "Pol":
            rotorLamSurfList.append(surf)
            print("rotorLamSurf:")
            print(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag0":
            rotorMagSurfList.append(surf)
            print("rotorMagSurf:")
            print(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag1":
            rotorMagSurfList.append(surf)
            print("rotorMagSurf:")
            print(f"gefunden: {surf.name}")
        elif surf.idExt == "Mag2":
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
    
    for surf in geometryList:
        if surf.idExt == "StNut":
            statorLamSurfList.append(surf)
            print("statorLamSurf:")
            print(f"gefunden: {surf.name}")

    return statorLamSurfList