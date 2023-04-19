import xml.etree.ElementTree as ET
from typing import List, Dict, Union
from math import pi


###
###
def getMaterialArray(xmlPath: str) -> List[Dict[str, Union[str, float, List[float]]]]:
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
                        raise ValueError("Unit for magnetic field strength not defined.")
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
