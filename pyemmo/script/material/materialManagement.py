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
"""Dieses Modul dient als Schnittstelle zur Bearbeitung der Material-Datenbank.
Zusätzlich kann die Software DB-Browser zur Visualisierung der Datenbank verwendet werden."""
import os
import pathlib
import sqlite3
from typing import Dict, Union

import matplotlib.pyplot as plt
import pandas
from genericpath import isfile


def addMaterial(
    dataBase: str,
    materialName: str,
    conductivity: float,
    relativePermeability: float,
    remanence: float = None,
    bh: str = None,
) -> None:
    """
    Die Funktion addMaterial() ergänzt die ausgewählte Datenbank um das eingegebene Material.
    Existiert die angegebene Datenbank nicht, wird diese neu angelegt.

    Args:
           dataBase (str): name of the database (e.g. "material.db")
           materialName (str): name of the material to add to the database
           conductivity (float): electrical conductivity in S/m (siemens per meter)
           relativePermeability (float): relative magnetic permeability
           remanence (float): remanent flux density of the material in T (Tesla). Defaults to None.
           bh (str): path to the .tab- or .xlsx file containing the BH-curve. Defaults to None.

    Returns:
        Nothing (None)

    Example:

        .. code:: python

            addMaterial('Material.db', 'air', 0, 1, 0)
            addMaterial('Material.db', 'steel1010', 2000000, 0, 0, 'C:\\...\\Material_Raw\\steel1010.tab')
    """
    # Verbindung zur Datenbank herstellen
    pathDataBase = os.path.join(
        pathlib.Path(__file__).parent.absolute(), dataBase
    )
    connection = sqlite3.connect(pathDataBase)
    cursor = connection.cursor()

    # Materialtabelle erzeugen, wenn sie noch nicht existiert
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Material(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT, conductivity REAL, relPermeability REAL, remanence REAL, BHCurve TEXT, UNIQUE(Name))"
    )

    # Prüfen ob es sich um ein lineares oder nicht lineares Material handelt
    # -> NL bh = Pfad der Rohdaten
    if bh == None:
        lin = "Linear"
    else:
        lin = "NL"

    # Zeilenanzahl prüfen
    cursor.execute("SELECT COUNT(*) FROM Material;")
    rownum1 = cursor.fetchone()[0]

    # Material ergänzen, wenn nicht vorhanden
    # FIXME: remanence should be real value not string!
    if remanence == None:
        info = (
            materialName,
            conductivity,
            relativePermeability,
            "no information",
            lin,
        )
    else:
        info = (
            materialName,
            conductivity,
            relativePermeability,
            remanence,
            lin,
        )
    cursor.execute(
        "INSERT OR IGNORE INTO Material (Name, conductivity, relPermeability, remanence, BHCurve) VALUES(?, ?, ?, ?, ?);",
        (info),
    )
    connection.commit()

    # Zeilenanzahl erneut prüfen
    cursor.execute("SELECT COUNT(*) FROM Material;")
    rownum2 = cursor.fetchone()[0]

    # Ist die Zeilenanzahl gleich, wurde kein neues Material hinzugefügt und das Programm wird beendet.
    if rownum1 == rownum2:
        if bh == None:
            connection.close()
            return None

    # Ist die Zeilenanzahl nicht gleich -> Wurde ein neues Material hinzugefügt.
    # -> Bei linearen Materialien muss keine zusätzliche Information an die DB übergeben werden
    # -> Bei nicht linearen Materialien muss die BH-Kurve noch übergeben werden.
    if bh != None:
        cursor.execute(
            "select ID From Material WHERE Name = '%s'" % materialName
        )
        idMat = cursor.fetchone()[0]
        bhName = "BH_Curve"
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS %s(ID INTEGER NOT NULL, H REAL, B REAL, Temp REAL, FOREIGN KEY (ID) REFERENCES Material (ID))"
            % bhName
        )
        if type(bh) != dict:
            try:
                file = pandas.read_table(bh)
            except UnicodeDecodeError:
                file = pandas.read_excel(bh)
            allValue = file.values
            H = []
            B = []
            Temp = []
            for i in range(len(allValue)):
                H.append(allValue[i][0])
                B.append(allValue[i][1])
                try:
                    Temp.append(allValue[i][2])
                except IndexError:
                    Temp.append("no information")
        else:
            H = bh["H"]
            B = bh["B"]
            Temp = []
            try:
                Temp = bh["Temp"]
            except KeyError:
                for i in range(len(H)):
                    Temp.append("no information")

        for i in range(len(H)):
            bhWert = (
                idMat,
                H[i],
                B[i],
                Temp[i],
            )
            cursor.execute(
                "INSERT INTO %s(ID, H, B, Temp) VALUES(?,?,?,?);" % bhName,
                bhWert,
            )

    connection.commit()
    connection.close()


###
# Die Funktion plotBHCurve() plottet die Magnetisierungskennlinie eines nicht linearen Materials.
#
#   Input:
#
#       dataBase : string (Datenbankname z. B. material.db)
#       materialName : string
#
#   Output:
#
#       None
#
#   Beispiel:
#
#       plotBHCurve('Material.db', 'steel1010')
#
###
def plotBHCurve(dataBase, materialName):
    pathDataBase = os.path.join(
        pathlib.Path(__file__).parent.absolute(), dataBase
    )
    connection = sqlite3.connect(pathDataBase)
    cursor = connection.cursor()
    cursor.execute(
        "select linear From Material WHERE Name = '%s'" % materialName
    )
    lin = cursor.fetchone()[0]
    if lin == 0:
        cursor.execute(
            "select ID From Material WHERE Name = '%s'" % materialName
        )
        idMat = cursor.fetchone()[0]
        bhName = "BH_" + str(idMat) + "_" + materialName
        cursor.execute(f"select H From {bhName} WHERE ID = '{idMat}'")
        htuple = cursor.fetchall()
        cursor.execute(f"select B From {bhName} WHERE ID = '{idMat}'")
        btuple = cursor.fetchall()
        h = []
        b = []
        for i in range(len(htuple)):
            h.append(htuple[i][0])
            b.append(btuple[i][0])

        plt.plot(h, b)
        plt.grid(b=True, which="major", color="#666666", linestyle="-")
        plt.minorticks_on()
        plt.grid(
            b=True, which="minor", color="#999999", linestyle="-", alpha=0.2
        )
        plt.xlim(h[0], h[len(h) - 1])
        plt.title("BH-Kennlinie")
        plt.xlabel("FeldstÃ¤rke H")
        plt.ylabel("Flussdichte B")

    connection.close()


###
# Die Funktion addBHtoMaterial() ergänzt die Datenbank um eine Magnetisierungskennlinie für ein definiertes Material. In diesem Fall MUSS das Material bereits in der Datenbank existieren!
#
#   Input:
#
#       dataBase : string (Datenbankname z. B. material.db)
#       materialName : string
#       bh : string (Pfad der .tab- bzw. .xlsx-Datei)
#
#   Output:
#
#       None
#
#   Beispiel:
#
#       addBHtoMaterial('Material.db', 'steel1010', 'C:\\...\\steel_1010BH.xlsx')
#
###
def addBHtoMaterial(dataBase, materialName, bh):
    # Verbindung zur Datenbank herstellen
    pathDataBase = os.path.join(
        pathlib.Path(__file__).parent.absolute(), dataBase
    )
    connection = sqlite3.connect(pathDataBase)
    cursor = connection.cursor()

    cursor.execute("select ID From Material WHERE Name = '%s'" % materialName)
    idMat = cursor.fetchone()[0]
    bhName = "BH_" + str(idMat) + "_" + materialName
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS %s(ID integer not null, H real, B real)"
        % bhName
    )
    cursor.execute("DELETE FROM %s" % bhName)

    try:
        file = pandas.read_table(bh)
    except UnicodeDecodeError:
        file = pandas.read_excel(bh)
    allValue = file.values
    H = []
    B = []
    for i in range(len(allValue)):
        H.append(allValue[i][0])
        B.append(allValue[i][1])

    for i in range(len(H)):
        bhWert = (
            idMat,
            H[i],
            B[i],
        )
        cursor.execute(
            "INSERT INTO %s(ID, H, B) VALUES(?,?,?);" % bhName, bhWert
        )

    cursor.execute(
        "UPDATE Material SET relPermeability = 0, remanence = 0, linear = 0 WHERE ID = %s"
        % idMat
    )
    connection.commit()
    connection.close()


###
# Die Funktion deleteMaterial() kann ein Material aus der Datenbank entfernt werden!
#
#   Input:
#
#       dataBase : string (Datenbankname z. B. material.db)
#       materialName : string
#
#   Output:
#
#       None
#
#   Beispiel:
#
#       deleteMaterial('Material.db', 'gold')
#
###
def deleteMaterial(dataBase, materialName):
    # Verbindung zur Datenbank herstellen
    pathDataBase = os.path.join(
        pathlib.Path(__file__).parent.absolute(), dataBase
    )
    connection = sqlite3.connect(pathDataBase)
    cursor = connection.cursor()

    cursor.execute("select ID From Material WHERE Name = '%s'" % materialName)
    idMat = cursor.fetchone()[0]
    bhName = "BH_" + str(idMat) + "_" + materialName
    cursor.execute("DROP TABLE IF EXISTS %s" % bhName)
    cursor.execute("DELETE FROM Material WHERE ID = %s" % idMat)

    connection.commit()
    connection.close()


###
# Die Funktion getMaterial() importiert Materialdaten aus der angebenen Datenbank und gibt diese als Dictionary zurück!
#
#   Input:
#
#       dataBase : string (Datenbankname z. B. material.db)
#       materialName : string
#
#   Output:
#
#       ans : dict
#       ans['name'] : string
#       ans['conductivity'] : float
#       ans['relPermeability'] : float
#       ans['remanence'] : float
#       ans['BH'] : list [B[], H[]]
#       ans['linear'] : boolean
#
#   Beispiel:
#
#       gold = getMaterial('Material.db', 'gold')
#       print(gold['name'])
#       >>gold
#       print(gold['conductivity'])
#       >>41000000
#       print(gold['relPermeability'])
#       >>0.99996
#       print(gold['remanence'])
#       >>0
#
###
def getMaterial(
    dataBase: str, materialName: str
) -> Dict[str, Union[str, float, list]]:
    """get Material from database by material name.

    Args:
        dataBase (str): database name
        materialName (str): material name

    Returns:
        dict: material parameter dict

            - name (str): material name
            - conductivity (float): electrical conductivity in
            - relPermeability (float): relative magnetic permeability in
            - remanence (float): Remanent flux denity in T
            - BH (list or None): BH-curve. B in T and H in A/m
            - linear (bool): linearity flag

    """
    pathDataBase = os.path.join(
        pathlib.Path(__file__).parent.absolute(), dataBase
    )
    if isfile(pathDataBase):
        connection = sqlite3.connect(pathDataBase)
        cursor = connection.cursor()
        cursor.execute(
            f"select Name From Material WHERE Name = '{materialName}'"
        )
        matName = cursor.fetchone()[0]
        cursor.execute(
            f"select conductivity From Material WHERE Name = '{materialName}'"
        )
        conductivity = cursor.fetchone()[0]
        cursor.execute(
            f"select relPermeability From Material WHERE Name = '{materialName}'"
        )
        relPerm = cursor.fetchone()[0]
        cursor.execute(
            f"select remanence From Material WHERE Name = '{materialName}'"
        )
        remanence = cursor.fetchone()[0]
        cursor.execute(
            f"select BHCurve From Material WHERE Name = '{materialName}'"
        )
        lin = cursor.fetchone()[0]
        if lin == "NL":
            cursor.execute(
                f"select ID From Material WHERE Name = '{materialName}'"
            )
            idMat = cursor.fetchone()[0]
            cursor.execute(f"select H From BH_Curve WHERE ID = '{idMat}'")
            htuple = cursor.fetchall()
            cursor.execute(f"select B From BH_Curve WHERE ID = '{idMat}'")
            btuple = cursor.fetchall()
            bhArray = []
            for i, hList in enumerate(htuple):
                bhArray.append([btuple[i][0], hList[0]])
        else:
            bhArray = None
        connection.close()
    else:
        raise FileNotFoundError(
            f"Could not find database file {pathDataBase}!"
        )

    if lin == "NL":
        flagLinear = False
    else:
        flagLinear = True

    return {
        "name": matName,
        "conductivity": conductivity,
        "relPermeability": relPerm,
        "remanence": remanence,
        "BH": bhArray,
        "linear": flagLinear,
    }
