#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
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

import unittest

import gmsh

from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.rotorIPMSM import RotorIPMSM


class TestRotorIPMSM(unittest.TestCase):
    """
    Tests der Klasse RotorIPMSM
    Aufbauend auf folgendem Tutorial: https://youtu.be/6tNS--WetLI
    Author: Max Ganser
    """

    @classmethod
    def setUpClass(cls):
        """
        Vordefinierte Setup Funktion die einmalig am Anfang der Testprozedur ausgeführt wird.
        Nützlich für beispielsweise zeitintensives Setup von Dingen die nicht verändert werden.
        Konkret z.B. Laden von vordefinierter, verifizierter Testgeometrie
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Vordefinierte teardown Funktion die einmalig am Ende der Testprozedur ausgeführt wird.
        Nützlich für beispielsweise Löschen von in Test erzeugten Datein und Ordnern.
        Konkret z.B. Löschen von abgespeicherten Geometrien
        """
        pass

    def setUp(self):
        """
        Vordefinierte Setup Funktion von Unittest
        Die Schreibweise "setUp" muss beachtet werden.
        Setup wird vor jeder Testmethode der Klasse TestRotorIPMSM ausgeführt
        """
        # RotorIPMSM Objekt für Tests erzeugen
        gmsh.initialize()
        self.rotorObj = RotorIPMSM(
            laminationType="Lam1",
            magnetType="Mag1",
            angleGeoParts=3.14,
            nbrGeoParts=2,
            symmetryFactor=2,
            startPosition=3.14,
        )

    def tearDown(self):
        """
        Vordefinierte Reset Funktion von Unittest
        Die Schreibweise "tearDown" muss beachtet werden!
        teardown wird nach jeder Testmethode der Klasse TestRotorIPMSM ausgeführt
        """
        gmsh.finalize()

    def test_initiavalue(self):
        # Setup

        # Sicherstellen, dass init Funktion Werte richtig setzt
        self.assertEqual(self.rotorObj._laminationType, "Lam1")
        self.assertEqual(self.rotorObj._magnetType, "Mag1")
        self.assertEqual(self.rotorObj._angleGeoParts, 3.14)
        self.assertEqual(self.rotorObj._nbrGeoParts, 2)
        self.assertEqual(self.rotorObj._symmetryFactor, 2)
        self.assertEqual(self.rotorObj._startPosition, 3.14)

    def test_addLaminationParameter(self):
        # Setup
        new_laminationDict = {
            "r_We": 0.1,
            "r_R": 1.1,
            "meshLength": 0.01,
            "machineCentrePoint": Point(name="P_name", x=0, y=0, z=0),
        }

        # Run
        self.rotorObj.addLaminationParameter(laminationDict=new_laminationDict)

        # Verify
        self.assertEqual(self.rotorObj._laminationDict, new_laminationDict)
        self.assertEqual(self.rotorObj._laminationDict["angleGeoParts"], 3.14)
        self.assertEqual(self.rotorObj._laminationDict["startPosition"], 3.14)


# Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
if __name__ == "__main__":
    unittest.main()
