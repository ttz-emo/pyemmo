import unittest
from pyemmo.script.script import Script
from .. import TEST_RES_DIR


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
            scriptPath=TEST_RES_DIR,
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
        self.assertEqual(self.scriptObj.scriptPath, TEST_RES_DIR)
        self.assertEqual(self.scriptObj.factory, "Built-in")
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
