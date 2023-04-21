"""
This module is about import functions for model information (geometry and simulation information)
from json files
"""
import json
import numbers
from typing import Dict, List, Tuple, Union, Literal, Any

from numpy import pi, zeros
from numpy.linalg import norm

from ..script.material.material import Material
from ..script.material.electricalSteel import ElectricalSteel
from . import air

# ================================ START EXTENDED INFO FUNCTIONS ===================================


def importExtInfo(extInfoPath: str) -> dict:
    """import the extended info JSON file as dict

    Args:
        extInfoPath (str): path to the extended info file.

    Returns:
        dict: extended info dict
    """
    with open(extInfoPath, encoding="utf-8") as extInfoFile:
        extInfo: dict = json.load(extInfoFile)
    if not isinstance(extInfo, dict):
        raise (
            ImportError(
                f"The imported extended info file from '{extInfoPath}' was not imported as a dict!"
            )
        )
    return extInfo


def getMagDir(extendedInfo: dict) -> str:
    """Retrun the magnetization direction (parallel, radial, ...) from the extendedInfo dict"""
    magDirKey = "magDirection"
    if magDirKey in extendedInfo.keys():
        if isinstance(extendedInfo[magDirKey], str):
            return extendedInfo[magDirKey]
        raise ValueError(
            f"Magnetization direction (magDirection) is not type str: {extendedInfo[magDirKey]}"
        )
    raise KeyError(
        "Magnetization direction (magDirection) is missing from extended info dict!"
    )


def getCurrentAmpl(extendedInfo: dict) -> float:
    """Return the amplitude of the current vector from d and q component

    Args:
        extendedInfo (dict): dict with additional information for the simulation.

    Returns:
        float: norm of d and q component. Amplitude of the current phasor.
    """
    dCurrent, qCurrent = getCurrentdq(extendedInfo)
    return norm([dCurrent, qCurrent])


def getCurrentdq(extendedInfo: dict) -> Tuple[float]:
    """Return the values for d and q current from extended info as [id, iq]"""
    if "id" in extendedInfo.keys() and "iq" in extendedInfo.keys():
        return (extendedInfo["id"], extendedInfo["iq"])
    else:
        raise KeyError(
            "Identifier 'id' and/or 'iq' missing from extended Information dict!"
        )


def getWindingList(extendedInfo: dict) -> List[str]:
    """
    Get the winding list from the extended info dict.
    The winding list looks like:

        ['+u', '-v', '+v', '-w', '+w', '-u']

    Args:
        extendedInfo (dict): dict with simulation infos

    Raises:
        KeyError: if "winding" key not in extendedInfo

    Returns:
        List[str]: winding list with elements "<+,-><u,v,w>"
    """
    windKey = "winding"
    if not windKey in extendedInfo.keys():
        raise KeyError("Missing winding information from extended info.")
    else:
        windList: List[str] = extendedInfo[windKey]
    return windList


def getNbrOfTurns(extendedInfo: dict) -> float:
    """
    getNbrOfTurns return the number of winding turns in one slot side.
    The identifier in extendedInfo dict must be Ntps (number of turns per slot side).
    """
    ntpsKey = "Ntps"
    if ntpsKey in extendedInfo.keys():
        if isinstance(extendedInfo[ntpsKey], numbers.Number) and not isinstance(
            extendedInfo[ntpsKey], bool
        ):
            return float(extendedInfo[ntpsKey])
        msg = (
            "Number of turns per slot side variable (Ntps)"
            f"is not a valid number: {extendedInfo[ntpsKey]}"
        )
        raise ValueError(msg)
    raise KeyError(
        f"Number of turns per slot side variable ('{ntpsKey}') missing from extended info dict!"
    )


def getRotFreq(extendedInfo: dict, unit: str = "Hz") -> float:
    """Get the mechanical rotation frequency of the rotor from the extended info dict.

    Args:
        extendedInfo (dict): Dict with additional information from a csv file
        unit (str, optional): Unit of the resulting rotational frequency. Defaults to "Hz".

    Options for :attr:`unit` are:
        - "hz"
        - "rad/s"
        - "rpm" or "1/min" or "min^-1"

    Raises:
        AttributeError: if the string given for "unit" is invalid
        KeyError: if the key "rot_freq" is missing from the extended info dict

    Returns:
        float: rotational frequency for the model
    """
    rotFreqKey = "rot_freq"
    if rotFreqKey in extendedInfo.keys():
        rotFreq = extendedInfo[rotFreqKey]
        if unit.lower() == "hz":
            return rotFreq
        if unit.lower() == "rad/s":
            return rotFreq * 2 * pi
        if unit in ("rpm", "1/min", "min^-1"):
            return rotFreq * 60
        raise AttributeError(f"Frequency unit not valid! Unit was '{unit}'")
    raise KeyError(
        f"Rotational frequency ('{rotFreqKey}') missing from extended info dict!"
    )


def getSymFactor(extendedInfo: dict) -> int:
    """getSymFactor returns the symmetry factor from the extended info dict"""
    symFactorKey = "symFactor"
    if symFactorKey in extendedInfo.keys():
        if float(extendedInfo[symFactorKey]).is_integer():
            return int(extendedInfo[symFactorKey])
        raise ValueError(
            f"Symmetry factor ('{symFactorKey}') is not type int: {extendedInfo[symFactorKey]}"
        )
    raise KeyError(
        f"Symmetry factor ('{symFactorKey}') missing from extended info dict!"
    )


def getNbrPolePairs(extendedInfo: dict) -> int:
    """getNbrPolePairs returns the the number of pole pairs from the extended info dict.
    Identifier is 'z_pp'."""
    nppKey = "z_pp"
    if nppKey in extendedInfo.keys():
        nbrPolePairs = extendedInfo[nppKey]
        if float(nbrPolePairs).is_integer():
            return int(nbrPolePairs)
        raise ValueError(
            f"number of pole pairs ('{nppKey}') is not type int: {nbrPolePairs}"
        )
    raise KeyError(
        f"number of pole pairs ('{nppKey}') missing from extended info dict!"
    )


def getNbrSlots(extendedInfo: dict) -> int:
    """returns the the number of stator slots from the extended info dict. Identifier is 'Qs'."""
    nppKey = "Qs"
    if nppKey in extendedInfo.keys():
        nbrSlots = extendedInfo[nppKey]
        if float(nbrSlots).is_integer():
            return int(nbrSlots)
        raise ValueError(f"number of slots ('{nppKey}') is not type int: {nbrSlots}")
    raise KeyError(f"number of slots ('{nppKey}') missing from extended info dict!")


def getElecFreq(extendedInfo: dict) -> float:
    """calcElecFreq calculates the electrical frequency in Hz from the extended info dict by
    :math:`f_\mathrm{el} = f_\mathrm{mech} \cdot pp`, where :math:`pp` is the number of pole
    pairs"""
    return getRotFreq(extendedInfo, "Hz") * getNbrPolePairs(extendedInfo)


def getAxialLength(extendedInfo: dict) -> Dict[str, float]:
    """get the axial length in meter of rotor and stator from the extended info dict"""
    if "axLen_S" in extendedInfo.keys() and "axLen_R" in extendedInfo.keys():
        return {
            "stator": extendedInfo["axLen_S"],
            "rotor": extendedInfo["axLen_R"],
        }
    msg = (
        "Axial length of rotor and/or stator ('axLen_R','axLen_S')"
        "missing from extended info dict!"
    )
    raise KeyError(msg)


def getMagTemperature(extendedInfo: dict) -> Union[float, None]:
    """get the magnet temperature from the extended info dict. Key is "tempMag".

    Args:
        extendedInfo (dict): dict with simulation info

    Returns:

        Union[float, None]: returns the value from the dict as float or None,
        if "tempMag" is missing from the dict.
    """
    if "tempMag" in extendedInfo.keys():
        return float(extendedInfo["tempMag"])
    return None


def getSimuParams(extendedInfo: dict) -> Dict[str, float]:
    """
    Return the simulation parameter dictionary needed for script class. See class :class:`Script
    <pyemmo.script.script.Script>` for details about the simulation dict.
    """
    idq = getCurrentdq(extendedInfo)
    endPos = extendedInfo["endPos"]
    # If is set to NaN in Matlab (-> "null" in JSON -> "None" in Python),
    # the angle will be calulated.
    parkAngleOffset = extendedInfo["parkAngleOffset"]
    simuParams = {
        "init_rotor_pos": extendedInfo["startPos"],
        "angle_increment": (endPos - extendedInfo["startPos"])
        / extendedInfo["nbrSteps"],
        "final_rotor_pos": endPos,
        "Id_eff": idq[0],
        "Iq_eff": idq[1],
        "rot_speed": getRotFreq(extendedInfo, "rpm"),
        "park_angle_offset": parkAngleOffset,
        "analysis_type": extendedInfo["analysisType"],
        "tempMag": getMagTemperature(extendedInfo),
        "nbrParallePaths": getNbrParalellPaths(extendedInfo),
    }
    return simuParams


def getModelName(extendedInfo: dict) -> str:
    """Return the model name from the extended info dict

    Args:
        extendedInfo (dict): dict from matlab side of api containing
        additional information for the simulation

    Raises:
        KeyError: If key "modelName" is not in extendedInfo.keys()

    Returns:
        str: Name for the to be generated model files
    """
    mNKey = "modelName"
    if mNKey in extendedInfo.keys():
        return extendedInfo[mNKey]
    raise KeyError(f"Name of model files ('{mNKey}') missing from extended info dict!")


def getFlagOpenGui(extendedInfo: dict) -> bool:
    """Return the flag openGUI from the extended info dict

    Args:
        extendedInfo (dict): dict from matlab side of api containing
        additional information for the simulation

    Raises:
        KeyError: If key "flag_openGUI" is not in extendedInfo.keys()
    Returns:
        bool: True if the GUI should be opened
    """
    fogKey = "flag_openGUI"
    if fogKey in extendedInfo.keys():
        return extendedInfo[fogKey]
    raise KeyError(f"Name of model files ('{fogKey}') missing from extended info dict!")


def getMovingbandRadius(extendedInfo: dict) -> float:
    """
    return the the movingband radius from the extended info dict.
    Identifier is 'movingband_r'.
    """
    mbKey = "movingband_r"
    if mbKey in extendedInfo.keys():
        return float(extendedInfo[mbKey])
    else:
        raise KeyError(
            f"Movingband radius ('{mbKey}') missing from extended info dict!"
        )


def getNbrParalellPaths(extendedInfo: dict) -> int:
    """getNbrParalellPaths returns the number of parallel winding paths per strand
    from the extended info dict. Identifier is 'NpP'."""
    mbKey = "NpP"
    if mbKey in extendedInfo.keys():
        if float(extendedInfo[mbKey]).is_integer():
            return int(extendedInfo[mbKey])
        msg = (
            "The parameter 'number of parallel paths per strand' was not an integer!"
            f"But type {type(extendedInfo[mbKey])}"
        )
        raise TypeError(msg)
    msg = f"Number of parallel paths per strand ('{mbKey}') missing from extended info dict!"
    raise KeyError(msg)


def getFlagCalcIronLoss(extendedInfo: dict) -> bool:
    """getIronLossFlag returns true if the iron loss calculation post processing
    should be started. Identifier is 'calcIronLoss'."""
    mbKey = "calcIronLoss"
    if mbKey in extendedInfo.keys():
        if isinstance(extendedInfo[mbKey], bool):
            return extendedInfo[mbKey]
        msg = (
            "The parameter 'calcIronLoss' was not a bool!"
            f"But type {type(extendedInfo[mbKey])}"
        )
        raise TypeError(msg)
    msg = f"Iron loss calculation flag ('{mbKey}') missing from extended info dict!"
    raise KeyError(msg)


# ==================================== END EXTENDED INFO FUNCTIONS =================================
# ====================================== START MATERIAL FUNCTIONS ==================================


def createMaterial(matDict: Dict[str, Dict[Literal["wert"], Any]]) -> Material:
    """create a pyemmo material object based on matDict format

    Args:
        matDict (Dict[str,Dict[Literal["wert"], Any]]): material dict extracted from matlab api side.

    Returns:
        Material: Material object generated from Matlab dict.
    """
    name = matDict["name"]["wert"]
    if isAir(name):
        return air
    if "elektromagnetik" in matDict.keys():
        magMatDict: dict = matDict["elektromagnetik"]
        if "el_lw" in magMatDict.keys():
            conductivity = magMatDict["el_lw"]["wert"]
        else:
            conductivity = None
        # linear magnetic permerability
        if "mue_r" in magMatDict.keys():
            permeability = magMatDict["mue_r"]["wert"]
        else:
            permeability = None
        # remanent flux density [T]
        if "b_rem" in magMatDict.keys():
            remanence = magMatDict["b_rem"]["wert"]
            if "tk_rem_100" in magMatDict.keys():
                remanenceTempCoef = magMatDict["tk_rem_100"]["wert"]
        else:
            remanence = None
            remanenceTempCoef = None
        # BH Curve
        bhCurve = None
        if "bh_kl" in magMatDict.keys():
            bhDict: dict = magMatDict["bh_kl"]
            if isinstance(bhDict["wert"], list):
                # one BH-curve
                nbrBasePoints = len(bhDict["wert"])
                if nbrBasePoints > 0:
                    bhCurve = zeros((nbrBasePoints, 2))
                    for i, hbArray in enumerate(bhDict["wert"]):
                        bhCurve[i] = [hbArray[1], hbArray[0]]
                else:
                    raise ValueError(f"BH-Curve of Material '{name}' is empty!")
            elif "kl_1" in bhDict.keys():
                ...  # TODO: add temperatur depended BH curve to material
            else:
                msg = (
                    f"No valid keys for bh curve in material dict for material '{name}'."
                    f"Keys are {bhDict.keys()}"
                )
                raise KeyError(msg)
        else:
            # check that there is a magnetic property
            if not permeability:
                msg = (
                    f"Material '{name}' does not have magnetic properties!"
                    "(neither relative permeability nor BH-Curve)"
                )
                raise AttributeError(msg)
    else:
        raise ValueError(f"Material '{name}' missing 'elektromagnetik' section!")

    if "dichte" in matDict.keys():
        density = matDict["dichte"]["wert"]
    else:
        density = None

    try:
        sheetThickness = matDict["d"]["wert"]
        assert sheetThickness < 1
        mat = createSteelMaterial(
            matDict, name, conductivity, permeability, bhCurve, density, sheetThickness
        )
    except (KeyError, AssertionError, TypeError):
        mat = Material(
            name=name,
            conductivity=conductivity,
            relPermeability=permeability,
            remanence=remanence,
            tempCoefRem=remanenceTempCoef,
            BH=bhCurve,
            density=density,
        )
    except Exception as exce:
        raise exce
    return mat


def createSteelMaterial(
    materialDict, name, conductivity, permeability, bhCurve, density, sheetThickness
) -> ElectricalSteel:
    emDict: dict = materialDict["elektromagnetik"]
    try:
        lossParams = []
        for lossChar in ("h", "w", "z"):
            lossParam = emDict["sigma_" + lossChar]["wert"]
            if not isinstance(lossParam, float):
                lossParams.append(0)
            else:
                lossParams.append(lossParam)
    except KeyError as keyErr:
        raise KeyError(
            "Missing loss parameter from material dict for material " + name
        ) from keyErr
    except Exception as exc:
        raise exc

    try:
        refInd = emDict["bez_ind"]["wert"]
    except KeyError as keyErr:
        raise KeyError(
            "Missing reference induction from material dict for material " + name
        ) from keyErr
    except Exception as exc:
        raise exc

    return ElectricalSteel(
        name=name,
        conductivity=conductivity,
        relPermeability=permeability,
        BH=bhCurve,
        density=density,
        sheetThickness=sheetThickness,
        lossParams=lossParams,
        referenceFluxDensity=refInd,
        referenceFrequency=50,  # setting to 50Hz allways
    )


def isAir(materialName: str):
    """
    isAir checks if the material name contains "air" or "luft" and returns True if it does so
    """
    if "air" in materialName.lower() or "luft" in materialName.lower():
        return True
    return False


# ======================================= END MATERIAL FUNCTIONS ===================================
