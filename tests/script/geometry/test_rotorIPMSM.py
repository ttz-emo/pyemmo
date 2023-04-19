import unittest
from pydraft.script.geometry.rotorIPMSM import RotorIPMSM
from pydraft.script.geometry.point import Point


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
        pass

    def test_initial_value(self):
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
            "machineCentrePoint": Point(name="P_name", x=0, y=0, z=0, meshLength=0.1),
        }

        # Run
        self.rotorObj.addLaminationParameter(laminationDict=new_laminationDict)

        # Verify
        self.assertEqual(self.rotorObj._laminationDict, new_laminationDict)
        self.assertEqual(self.rotorObj._laminationDict["angleGeoParts"], 3.14)
        self.assertEqual(self.rotorObj._laminationDict["startPosition"], 3.14)


"""
Dieser Abschnitt ermöglicht das direkte Starten der Testmethoden beim ausführen der Datei
"""
if __name__ == "__main__":
    unittest.main()