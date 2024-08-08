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
"""Module for toolkit magnet Surface03"""
import math
from typing import Any, Dict

from .. import colorDict
from .line import Line
from .magnet import Magnet
from .point import Point
from .surface import Surface


###
# Ein Objekt der Klasse Magnet_Surface03:
# \image html magnet_Surface03.png
# Der Magnettype wird mit addRotorToMachine() ausgewählt und mit addMagnetParameter()
# parametrisiert. Abschließend verknüpft die Funktion createRotor() den Magnet am
# Rotorobjekt.
#
#   Beispiel:
#
#       pmsm1 = pyd.MachineSPMSM({...})
#       rotor1 = pmsm1.addRotorToMachine('sheet01_standard', 'magnet03_surface')
#       rotor1.addLaminationParameter({...})
#       rotor1.addMagnetParameter({
#                'h_M' : 7.5e-3,
#                'w_Mag' : 12e-3,
#                'magnetisationDirection' : [1, -1, 1, -1, 1, -1, 1, -1],
#                'magnetisationType' : 'radial',
#                'material' : ndFe35,
#                'meshLength' : 3e-3})
#       rotor1.addAirGapParameter({...})
#       rotor1.createRotor()
#
###
class Magnet_Surface03(Magnet):
    ###
    # Konstuktor der Klasse Magnet_Surface03.
    #
    #   Input:
    #
    #       machineDict : Dict
    #       magnetisationDirection : Integer
    #       magnetisationType : String
    #
    ###
    def __init__(self, machineDict, magnetisationDirection, magnetisationType):
        self._machineDict: Dict[str, Any] = machineDict
        self.id = self._getNewID()
        magName = "Magnet_Surface03_" + str(self.id)
        super().__init__(
            name=magName,
            geoElements=[],
            material=machineDict["material"],
            magDirection=magnetisationDirection,
            magType=magnetisationType,
        )
        self._createGeometry()

    ###_createGeometry() erzeugt die Magnetgeometrie und definiert alle Attribute der Klasse.
    def _createGeometry(self):
        dockingLength: float = self._machineDict["rA_Rotor"]
        magnetheight: float = self._machineDict["h_M"]
        magnetWidth: float = self._machineDict["w_Mag"]

        globalCenter: Point = self._machineDict[
            "machineCentrePoint"
        ].duplicate()
        centerCoords = globalCenter.coordinate

        # Konstuktion der Punkte an der x-Achse
        pMagnet1 = Point(
            "pMagnet1",
            centerCoords[0] + dockingLength,
            centerCoords[1],
            centerCoords[2],
            self._machineDict["meshLength"],
        )
        alpha1 = math.asin(magnetWidth / 2 / dockingLength)
        pMagnet1.rotateZ(globalCenter, alpha1)
        pMagnet2 = pMagnet1.duplicate()
        pMagnet2.translate(0, -magnetWidth / 2, 0)
        pMagnet2.name = "pMagnet2"
        pMagnet3 = pMagnet2.duplicate()
        pMagnet3.translate(magnetheight, 0, 0)
        pMagnet4 = pMagnet3.duplicate()
        pMagnet4.translate(0, magnetWidth / 2, 0)

        # Startposition berücksichtigen
        pMagnet1.rotateZ(globalCenter, self._machineDict["startPosition"])
        pMagnet2.rotateZ(globalCenter, self._machineDict["startPosition"])
        pMagnet3.rotateZ(globalCenter, self._machineDict["startPosition"])
        pMagnet4.rotateZ(globalCenter, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lMagnet1 = Line("lMagnet1", pMagnet2, pMagnet1)
        lMagnet2 = Line("lMagnet2", pMagnet1, pMagnet4)
        lMagnet3 = Line("lMagnet3", pMagnet4, pMagnet3)
        lMagnet4 = Line("lMagnet4", pMagnet3, pMagnet2)

        # Flächenerzeugen
        surfaceMagnet = Surface(
            "surfaceMagnet", [lMagnet1, lMagnet2, lMagnet3, lMagnet4]
        )

        # Bei jedem Baukasten muss diese Definition identisch sein
        ###Fläche des halben Magneten in einer Liste.
        self.geometricalElement = [surfaceMagnet]
        ###Schnittkante des halben Magneten.
        # \image html innerLinePart03.png
        self._innerLinePart = [lMagnet1]
        ###Punkt zwischen Magnet und Luft an der Schnittkante.
        # \image html airDockingPoint03.png
        self._airDockingPoint = [pMagnet3]
        ###Alle Linien in einer Liste, die den Luftraum schneiden.
        # \image html airLinePart03.png
        self._airLinePart = [lMagnet3, lMagnet2]
        ###Punkt zwischen Blechpaket und Magneten an der Schnittkante.
        # \image html laminationDockingPoint03.png
        self._laminationDockingPoint = [pMagnet2]

        for surf in self.geometricalElement:
            if self.magDir() == 1:
                surf.setMeshColor(colorDict["Red"])
            elif self.magDir() == -1:
                surf.setMeshColor(colorDict["Green"])

    ###Gibt eine Liste mit der Schnittkante im Magneten zurück (siehe _innerLinePart).
    @property
    def innerLinePart(self) -> list:
        """get innerLinePart \n
        Gibt eine Liste mit der Schnittkante im Magneten zurück (siehe _innerLinePart).
        Returns:
            list: _innerLinePart
        """
        return self._innerLinePart

    ###Gibt eine Liste mit dem airDockingPoint zurück (siehe _airDockingPoint).
    @property
    def airDockingPoint(self) -> list:
        """get airDockingPoint \n
        Gibt eine Liste mit dem airDockingPoint zurück (siehe _airDockingPoint).
        Returns:
            list: _airDockingPoint
        """
        return self._airDockingPoint

    ###Gibt eine Liste mit airLinePart zurück (siehe _airLinePart).
    @property
    def airLinePart(self) -> list:
        """get airLinePart \n
        Gibt eine Liste mit airLinePart zurück (siehe _airLinePart).
        Returns:
            list: _airLinePart
        """
        return self._airLinePart

    ###Gibt eine Liste mit dem laminationDockingPoint zurück (siehe _laminationDockingPoint).
    @property
    def laminationDockingPoint(self) -> list:
        """get laminationDockingPoint \n
        Gibt eine Liste mit dem laminationDockingPoint zurück (siehe _laminationDockingPoint).
        Returns:
            list: _laminationDockingPoint
        """
        return self._laminationDockingPoint
