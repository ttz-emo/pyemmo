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
import unittest
from pyemmo.script.script import Script
from .. import save_path


class TestScript(unittest.TestCase):
    """
    Tests der Klasse Script
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
        # cls.maxDiff = None

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
        # Script Objekt für Tests erzeugen
        self.initParamDict = {
            "SYM": {
                "INIT_ROTOR_POS": 0.0,
                "ANGLE_INCREMENT": 1,
                "FINAL_ROTOR_POS": 90.0,
                "Id_eff": 2,
                "Iq_eff": 1,
                "SPEED_RPM": 1000,
                "ParkAngOffset": None,  # optional
                "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient
            },
            "MAT": {
                "TEMP_MAG": 20,
            },
        }
        self.scriptObj = Script(
            name="testScript",
            scriptPath=save_path,
            factory="Built-in",
            simuParams=self.initParamDict,
        )

    def tearDown(self):
        """
        Vordefinierte Reset Funktion von Unittest
        Die Schreibweise "tearDown" muss beachtet werden!
        teardown wird nach jeder Testmethode der Klasse TestRotorIPMSM ausgeführt
        """
        pass

    def test_initial_value(self):
        # Setup

        # Sicherstellen, dass init Funktion Werte richtig setzt
        self.assertEqual(self.scriptObj.name, "testScript")
        self.assertEqual(self.scriptObj.scriptPath, save_path)
        self.assertEqual(self.scriptObj.factory, "Build-in")
        # Test that the initial parameters are in the resulting param dict
        self.assertEqual(
            self.scriptObj.simParams["SYM"],
            self.scriptObj.simParams["SYM"] | self.initParamDict["SYM"],
        )
        self.assertEqual(
            self.scriptObj.simParams["MAT"],
            self.scriptObj.simParams["MAT"] | self.initParamDict["MAT"],
        )


if __name__ == "__main__":
    # """Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei"""
    unittest.main()
