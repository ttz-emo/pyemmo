#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
from __future__ import annotations

from math import pi

# import xml.etree.ElementTree as ET # fixed per Issue: [B314:blacklist] in workingDirectory\Vu\bandit_log\bandit_log_20240809_105713.log line 139

try:
    import defusedxml.ElementTree as ET
except ImportError as exce:
    exce.msg += "Please use 'pip install defusedxml' to install missing package"
    raise exce


###
###
def getMaterialArray(
    xmlPath: str,
) -> list[dict[str, str | float | list[float]]]:
    """Die Funktion getMaterialArray() ist ein Parser speziell für die erstellten XML-Dokumente
    aus den Maxwell-Materialdaten (.amat). Als Input dient der vollständige Pfad der XML-Datei.
    Eine Liste mit allen Materialien und den Eigenschaften: elektrische Leitfähigkeit, magnetsiche
    Leitfähigkeit und der Magnetisierungskurve, werden dem Nutzer als Output-Variable zur
    Verfügung gestellt. Alle Werte werden auf SI-Einheiten umgerechnet.

    Args:
        xmlPath (str): path to the xml file

    Returns:
        List[Dict[str, Union[str, float, List[float]]]]: List of material dicts.

    The dicts look like:

            {
                "name": name,
                "conductivity": value,
                "relativePermeability": value,
                "BH": {
                    "B": valuesOfB,
                    "H": valuesOfH,
                }
            }
    """
    # Parser mit der Funktion aus Modul xml.etree.ElementTree
    root = ET.parse(xmlPath).getroot()

    # Leere Material-Liste (OUTPUT)
    materialArray = []

    # for-Schleife für jedes einzelne Material in root (alle Roh-daten die geparst wurden).
    for mat in root:
        ###Name des Materials
        name = mat.tag
        # Alle '-' Zeichen durch '_' ersetzen, da sonst die Weiterverarbeitung mit SQL eine Fehlermeldung bringt.
        name = name.replace("-", "_")
        # Material Dictionary erstellen. Die Dictionary werden nach und nach in die Material-Liste abgespeichert.
        matDict = {"name": name}
        # Wenn ein Material eine Magnetisierungskurve besitzt, werden die Listen B[] und H[] befüllt.
        B = []
        H = []
        unitH = ""
        unitB = ""

        for matAttr in mat:
            # Material besitzt Informationen über die elektrische Leitfähigkeit.
            if matAttr.tag == "conductivity":
                matDict["conductivity"] = matAttr.text
            # Material besitzt Informatinen über die magnetische Leitfähigkeit.
            if matAttr.tag == "permeability":
                matDict["relativePermeability"] = matAttr.text
            # Einheit von H der BH-Kurve bestimmen.
            if matAttr.tag == "permHUnite":
                unitH = matAttr.text
            # Einheit von B der BH-Kurve bestimmen.
            if matAttr.tag == "permBUnit":
                unitB = matAttr.text
            # BH-Kurve importieren.
            if matAttr.tag == "permBHcurve":
                # Alle H-Werte importieren
                for hElem in matAttr[0]:
                    hVal = float(hElem.text)
                    # Werte in SI-Einheiten umrechnen.
                    if unitH in ("Oe", "oe"):
                        hSI = 4 * pi * hVal / 1000
                    elif unitH == "kA_per_meter":
                        hSI = hVal / 1000
                    elif unitH == "A_per_meter":
                        hSI = hVal
                    else:
                        raise ValueError(
                            "Unit for magnetic field strength not defined."
                        )
                    # H-Wert in der H[]-Liste abspeichern (nach einander).
                    H.append(hSI)

                # Alle B-Werte importieren
                for bElem in matAttr[1]:
                    bVal = float(bElem.text)
                    # Werte in SI-Einheiten umrechnen.
                    if unitB.lower() == "gauss":
                        bSI = bVal * 1e4
                    elif unitB.lower() == "tesla":
                        bSI = bVal
                    else:
                        raise ValueError("Unit for magnetic flux density not defined.")
                    # B-Wert in der B[]-Liste abspeichern (nach einander).
                    B.append(bSI)
                # Listen in ein BH-Dict abspeichern.
                bhDict = {"B": B, "H": H}
                # BH-Dict in matDict abspeichern.
                matDict["BH"] = bhDict
        # Material-Liste (OUTPUT) mit den einzelnen Material-Dicts befüllen.
        if len(matDict) > 1:
            materialArray.append(matDict)
    # Material-Liste mit den einzelnen Materialien (Dict) zurück geben.
    return materialArray
