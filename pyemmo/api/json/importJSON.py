#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This module is about import functions for model information (geometry and simulation information)
from json files
"""
from __future__ import annotations

import json
import numbers
from typing import Any, Literal

from numpy import pi, zeros
from numpy.linalg import norm

from ...functions.clean_name import clean_name
from ...script.material.electricalSteel import ElectricalSteel
from ...script.material.material import Material
from .. import air, logger


# ================================ START EXTENDED INFO FUNCTIONS ===================================
class InvalidSheetThicknessError(Exception):
    """
    .. todo::

        write descriptions

    Attributes:
        input -- input that caused the error
        message -- explanation of the error
    """

    def __init__(self, sheet_thickness, message="Invalid sheet thickness provided"):
        self.input_value = sheet_thickness
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.input_value}"


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


# FIXME: Rename this to get_mag_TYPE!
def getMagDir(extendedInfo: dict) -> str:
    """Retrun the magnetization direction (parallel, radial, ...) from the extendedInfo dict"""
    magDirKey = "magType"
    if magDirKey in extendedInfo.keys():
        if isinstance(extendedInfo[magDirKey], str):
            return extendedInfo[magDirKey]
        raise ValueError(
            f"Magnetization direction (magType) is not type str: {extendedInfo[magDirKey]}"
        )
    raise KeyError(
        "Magnetization direction (magType) is missing from extended info dict!"
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


def getCurrentdq(extendedInfo: dict) -> tuple[float]:
    """Return the values for d and q current from extended info as [id, iq]"""
    if "id" in extendedInfo.keys() and "iq" in extendedInfo.keys():
        return (extendedInfo["id"], extendedInfo["iq"])
    else:
        raise KeyError(
            "Identifier 'id' and/or 'iq' missing from extended Information dict!"
        )


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def getWindingList(extendedInfo: dict) -> list[list[list[int]]]:
    """Get winding layout from extended info dict. The layout must be in form of
    the SWAT-EM winding layout. The layout looks something like:

    single-layer winding:
        [[phase_u1], [phase_v1], [phase_w1]]

    double-layer winding:
        [[[phase_u1], [phase_u2]], [[phase_v1], [phase_v2]], [[phase_w1], [phase_w2]]]

    Where phase_u1 is a list of integers representing the slot ID and the winding direction
    (with their sign). See`this <https://swat-em.readthedocs.io/en/latest/reference.html#swat_em.datamodel.datamodel.set_phases>`__
    SWAT-EM method for more details.

    Args:
        extendedInfo (dict): dict with simulation infos

    Raises:
        KeyError: if "winding" key not in extendedInfo

    Returns:
        list[list[list[int]]]: SWAT-EM formatted winding layout
    """
    windKey = "winding"
    if not windKey in extendedInfo.keys():
        raise KeyError("Missing winding information from extended info.")
    # windList: List[str] = extendedInfo[windKey]
    windList = extendedInfo[windKey]
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
        symFactor = extendedInfo[symFactorKey]
        if float(symFactor).is_integer() and symFactor > 0:
            # symmetry is positiv integer
            return int(symFactor)
        raise ValueError(
            f"Symmetry factor ('{symFactorKey}') is not type int: {symFactor}"
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
    r"""calcElecFreq calculates the electrical frequency in Hz from the extended info dict by
    :math:`f_\mathrm{el} = f_\mathrm{mech} \cdot pp`, where :math:`pp` is the number of pole
    pairs"""
    return getRotFreq(extendedInfo, "Hz") * getNbrPolePairs(extendedInfo)


def getAxialLength(extendedInfo: dict) -> dict[str, float]:
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


def getMagTemperature(extendedInfo: dict) -> float | None:
    """get the magnet temperature from the extended info dict. Key is "tempMag".

    Args:
        extendedInfo (dict): dict with simulation info

    Returns:

        Union[float, None]: returns the value from the dict as float or None,
        if "tempMag" is missing from the dict.
    """
    if "tempMag" in extendedInfo.keys():
        if isinstance(extendedInfo["tempMag"], numbers.Number):
            return float(extendedInfo["tempMag"])
        raise ValueError(
            f"Magnet temperature ('tempMag') is not type float: {extendedInfo['tempMag']}"
        )
    return None


def getSimuParams(extendedInfo: dict) -> dict[str, dict[str, float]]:
    """
    Return the simulation parameter dictionary needed for script class. See class :class:`Script
    <pyemmo.script.script.Script>` for details about the simulation dict.
    """
    idq = getCurrentdq(extendedInfo)
    endPos = extendedInfo["endPos"]
    simuParams = {
        "SYM": {
            "INIT_ROTOR_POS": extendedInfo["startPos"],
            "ANGLE_INCREMENT": (endPos - extendedInfo["startPos"])
            / extendedInfo["nbrSteps"],
            "FINAL_ROTOR_POS": endPos,
            "Id_eff": idq[0],
            "Iq_eff": idq[1],
            "SPEED_RPM": getRotFreq(extendedInfo, "rpm"),
            "ParkAngOffset": extendedInfo["parkAngleOffset"],
            "ANALYSIS_TYPE": extendedInfo["analysisType"],
            "NBR_PARALLEL_PATHS": extendedInfo["NpP"],
        },
        "MAT": {
            "TEMP_MAG": getMagTemperature(extendedInfo),
        },
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
        correctScriptName = clean_name(extendedInfo[mNKey])
        return correctScriptName
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


def getMagAngle(extendedInfo: dict) -> dict:
    """Returns the magnetization angle dictionary.\n
    This dictionary defines the *magnetization vector angle in rad* with the
    magnet surface IdExt as key. Identifier is 'magAngle'.
    The magAngle dict looks like:

    .. code-block:: python

        {
            "Mag1": 0.192,
            "Mag2": 0.344,
            ...
        }
    """
    mbKey = "magAngle"
    if mbKey in extendedInfo.keys():
        if isinstance(extendedInfo[mbKey], dict):
            return extendedInfo[mbKey]
        msg = (
            "The parameter 'magAngle' was not a dict!"
            f"But type {type(extendedInfo[mbKey])}"
        )
        raise TypeError(msg)
    msg = f"Magnetization angle flag ('{mbKey}') missing from extended info dict!"
    raise KeyError(msg)


# ==================================== END EXTENDED INFO FUNCTIONS =================================
# ====================================== START MATERIAL FUNCTIONS ==================================


def createMaterial(matDict: dict[str, dict[Literal["wert"], Any]]) -> Material:
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
        # TODO: Optimize code by introducing default mat dict and iterating
        #  over its elements!
        magMatDict: dict = matDict["elektromagnetik"]
        conductivity = magMatDict.get("el_lw", {}).get("wert")
        if not isinstance(conductivity, (int, float)):
            conductivity = None
        # linear magnetic permerability
        permeability = magMatDict.get("mue_r", {}).get("wert")
        if not isinstance(permeability, (int, float)):
            permeability = None
        # remanent flux density [T]
        remanence = magMatDict.get("b_rem", {}).get("wert")
        if not isinstance(remanence, (int, float)):
            remanence = None
            remanenceTempCoef = None
        else:
            if "tk_rem_100" in magMatDict.keys():
                remanenceTempCoef = magMatDict["tk_rem_100"]["wert"]
                if not isinstance(remanenceTempCoef, (int, float)):
                    # if not valid value for temperature coefficient of remanence
                    remanenceTempCoef = None  # set to None
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
                # else:
                # raise ValueError(f"BH-Curve of Material '{name}' is empty!")
            elif "kl_1" in bhDict.keys():
                ...  # TODO: add temperatur depended BH curve to material
            else:
                msg = (
                    f"No valid keys for bh curve in material dict for material '{name}'."
                    f"Keys are {bhDict.keys()}"
                )
                raise KeyError(msg)
        if bhCurve is None:
            # check that there is a magnetic property
            if not permeability:
                msg = (
                    f"Material '{name}' does not have magnetic properties!"
                    "(neither relative permeability nor BH-Curve)"
                )
                raise AttributeError(msg)
            elif permeability < 1:
                # pylint: disable=locally-disabled,  line-too-long
                logger.warning(
                    "Permeability of material '%s' is smaller than 1! Resetting it to 1 for model.",
                    name,
                    exc_info=1,
                )
                permeability = 1.0
    else:
        raise ValueError(f"Material '{name}' missing 'elektromagnetik' section!")

    density = matDict.get("dichte", {}).get("wert")
    if not isinstance(density, (int, float)):
        density = None
    # check for sheet thickness
    # if valid value (>0, <5e-3) for thickness is given -> create steel mat
    try:
        sheetThickness = matDict["d"]["wert"]
        if not isinstance(sheetThickness, (int, float)):
            raise InvalidSheetThicknessError(
                sheetThickness,
                f"Invalid sheet thickness type {type(sheetThickness)}",
            )
        if sheetThickness > 5e-3:
            # add warning to log and raise InvalidSheetThicknessError (which is catched
            # by try-except statment) to create standard material
            logger.warning(
                """Sheet thickness of material %s is greater 5mm: %f meter!
                Creating standard material instead of electrical steel material!""",
                name,
                sheetThickness,
            )
            raise InvalidSheetThicknessError(sheetThickness)
        mat = createSteelMaterial(
            matDict,
            name,
            conductivity,
            permeability,
            bhCurve,
            density,
            sheetThickness,
        )
    except (KeyError, InvalidSheetThicknessError):
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
    materialDict,
    name,
    conductivity,
    permeability,
    bhCurve,
    density,
    sheetThickness,
) -> ElectricalSteel:
    emDict: dict = materialDict["elektromagnetik"]
    try:
        lossParams = []
        for lossChar in ("h", "w", "z"):
            lossParam = emDict["sigma_" + lossChar]["wert"]
            if not isinstance(lossParam, float):
                # TODO: Add warning
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
            f"Missing reference induction from material dict for material '{name}'."
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
    if isinstance(materialName, str):
        if "air" in materialName.lower() or "luft" in materialName.lower():
            return True
        return False
    if isinstance(materialName, list):
        if not materialName:  # if materialName is empty
            return True
        raise TypeError("Imported material name is unempty list, not string!")
    raise TypeError("Imported material name has type" + str(type(materialName)))


# ======================================= END MATERIAL FUNCTIONS ===================================
