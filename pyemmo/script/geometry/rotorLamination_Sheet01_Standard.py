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
from typing import List
from .rotorLamination import RotorLamination
from .. import colorDict
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface


###
# Ein Objekt der Klasse RotorLamination_Sheet01_Standard:
# \image html rotorBlech.png
# Das Blechpaket wird mit addRotorToMachine() ausgewählt und mit addLaminationParameter() parametrisiert. Abschließend verknüpft die Funktion createRotor() das Blech am Rotorobjekt.
#
#   Beispiel:
#
#       pmsm1 = pyd.MachineSPMSM({...})
#       rotor1 = pmsm1.addRotorToMachine('sheet01_standard', 'magnet01_surface')
#       rotor1.addLaminationParameter({
#           "r_We": 20e-3,
#           "r_R": 55e-3,
#           "meshLength": 3e-3,
#           "material": steel_1010,
#           "machineCentrePoint": PBohrung
#           })
#       rotor1.addMagnetParameter({...})
#       rotor1.addAirGapParameter({...})
#       rotor1.createRotor()
#
###
class RotorLamination_Sheet01_Standard(RotorLamination):
    def __init__(self, machineDict: dict):
        """Konstruktor der Klasse RotorLamination Type Sheet01_Standard

        Args:
            machineDict (dict): Machine parameter dict
        """
        super().__init__(
            name="RotorLamination_Sheet01_Standard",
            material=machineDict["material"],
            geometricalElement=[],
        )
        ###Alle Parameter zur Beschreibung des Rotorblechs.
        self._machineDict = machineDict
        ###Name des Rotorsblech
        self.name = "RotorLamination_Sheet01_Standard_" + str(self.id)
        self._createGeometry()

    ###_createGeometry() erzeugt die Blechgeometrie und definiert alle Attribute der Klasse.
    def _createGeometry(self):
        r_We = self._machineDict["r_We"]
        r_R = self._machineDict["r_R"]

        PCentre = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.coordinate

        alpha = self._machineDict["angleGeoParts"]

        # Konstuktion der Punkte an der x-Achse
        pWelle1 = Point(
            "pWelle1",
            coordCentre[0] + r_We,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
        )
        pWelle2 = pWelle1.duplicate()
        pWelle2.name = "pWelle2"
        pRotor1 = pWelle1.duplicate()
        pRotor1.translate(r_R - r_We, 0, 0)
        pRotor1.name = "pRotor1"
        pRotor2 = pRotor1.duplicate()
        pRotor2.name = "pRotor2"
        pWelle2.rotateZ(PCentre, alpha)
        pRotor2.rotateZ(PCentre, alpha)

        # Startposition berücksichtigen
        pWelle1.rotateZ(PCentre, self._machineDict["startPosition"])
        pWelle2.rotateZ(PCentre, self._machineDict["startPosition"])
        pRotor1.rotateZ(PCentre, self._machineDict["startPosition"])
        pRotor2.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lWelle = CircleArc("lWelle", pWelle1, PCentre, pWelle2)
        lBlech1 = Line("lBlech1", pWelle2, pRotor2)
        lRotorAussen = CircleArc("lRotorAussen", pRotor2, PCentre, pRotor1)
        lBlech2 = Line("lBlech2", pRotor1, pWelle1)

        # Flächenerzeugen
        surfaceRotor = Surface(
            "surfaceRotor", [lWelle, lBlech1, lRotorAussen, lBlech2]
        )

        surfaceRotor.setMeshColor(colorDict["SteelBlue"])

        # Bei jedem Baukausten müssen diese Attribute vorkommen
        ###Fläche des Bleches (halber Pol) in einer Liste.
        self._geometricalElement = [surfaceRotor]
        ###Außenkante des Bleches.
        # \image html outerLinePart.png
        self._outerLinePart = [lRotorAussen]
        ###Schnittkante zwischen 2 Blechen.
        # \image html betweenLinePart.png
        self._betweenLinePart = [lBlech2]
        ###Erster Punkt auf der Außenkante des Bleches.
        # \image html airDockingPoint1.png
        self._airDockingPoint1 = [pRotor1]
        ###Zweiter Punkt auf der Außenkante des Bleches.
        # \image html airDockingPoint2.png
        self._airDockingPoint2 = [pRotor2]

    ###Gibt eine Liste mit der Außenkante des Bleches zurück (siehe _outerLinePart).
    @property
    def outerLinePart(self) -> List[CircleArc]:
        """Get the boundary line(s) of the rotor lamination towards the airgap

        Returns:
            List[CircleArc]: ...
        """
        return self._outerLinePart

    ###Gibt eine Liste mit der Schnittkante zurück (siehe _betweenLinePart).
    @property
    def betweenLinePart(self) -> List[Line]:
        """Gibt eine Liste mit der Schnittkante zurück. Schnittkante zwischen 2 Blechen.

        Returns:
            List[Line]: list of line between to lamination segments?
        """
        return self._betweenLinePart

    ###Gibt eine Liste mit dem airDockingPoint1 zurück (siehe _airDockingPoint1).
    @property
    def airDockingPoint1(self) -> List[Point]:
        """Get point of lamination segment at airgap interface near x-Axis

        Returns:
            List[Point]: interface point to airgap near x-axis
        """
        return self._airDockingPoint1

    ###Gibt eine Liste mit dem airDockingPoint2 zurück (siehe _airDockingPoint2).
    @property
    def airDockingPoint2(self) -> List[Point]:
        """Get point of lamination segment at airgap interface on interface line to next segment in math. positive direction.

        Returns:
            List[Point]: interface point to airgap near next lamination (CCW direction)
        """
        return self._airDockingPoint2
