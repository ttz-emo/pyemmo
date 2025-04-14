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
"""Module for class Magnet_Slot01"""

from .. import colorDict
from ..gmsh.gmsh_surface import GmshSurface
from .line import Line
from .magnet import Magnet
from .point import Point
from .surface import Surface


class MagnetSlot01(Magnet):
    def __init__(self, machineDict, magnetisationDirection, magnetisationType):
        ###Dictionary mit allen Magnet-Parametern.
        self._machineDict = machineDict

        self.id = self._getNewID()
        magName = "MagnetSlot01_" + str(self.id)
        super().__init__(
            name=magName,
            geoElements=[],
            material=machineDict["material"],
            magDirection=magnetisationDirection,
            magType=magnetisationType,
            magVectorAngle=0.0,
        )
        self._createGeometry()

    @property
    def airLinePart(self):
        """get airLinePart

        Returns:
            _type_: _airLinePart
        """
        return self._airLinePart

    @property
    def lamLinePart(self):
        """get lamLinePart

        Returns:
            _type_: _lamLinePart
        """
        return self._lamLinePart

    @property
    def laminationDockingPoint(self):
        """get laminationDockingPoint

        Returns:
            _type_: _laminationDockingPoint
        """
        return self._laminationDockingPoint

    @property
    def innerLinePart(self):
        """get innerLinePart

        Returns:
            _type_: _innerLinePart
        """
        return self._innerLinePart

    def _createGeometry(self):
        rA_Rotor = self._machineDict["rA_Rotor"]
        h_M = self._machineDict["h_Mag"]
        width_M = self._machineDict["w_Mag"]
        # Slot Parameters
        # h_Slot =
        # w_Slot =
        # Slot distance (at central line of magnet-top) from rotor diameter:
        d_Slot = self._machineDict["d_Slot"]

        PCentre: Point = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.coordinate

        r_M_bottom = rA_Rotor - d_Slot - h_M

        # Konstuktion der Punkte an der x-Achse:
        pMagnet1 = Point(
            "pMagnet1",
            coordCentre[0] + r_M_bottom,
            coordCentre[1],
            coordCentre[2],
        )
        pMagnet2 = pMagnet1.duplicate()
        pMagnet2.translate(0, width_M / 2, 0)
        pMagnet2.name = "pMagnet2"
        pMagnet3 = pMagnet2.duplicate(name="pMagnet3")
        pMagnet3.translate(h_M, 0, 0)
        pMagnet4 = pMagnet1.duplicate(name="pMagnet4")
        pMagnet4.translate(h_M, 0, 0)

        # Startposition berücksichtigen
        pMagnet1.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet2.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet3.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet4.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        # Achtung!: Richtung der Linien, sowie Anfang und Endpunkt müssen bei allen MagSlot-Klassen gleich sein
        # Das ist wichtig für die Identifikation der Linien beim Ausschneiden des Slots aus der Blech-Fläche

        lMagnet1 = Line("lMagnet1", pMagnet1, pMagnet2)
        lMagnet2 = Line("lMagnet2", pMagnet2, pMagnet3)
        lMagnet3 = Line("lMagnet3", pMagnet3, pMagnet4)
        lMagnet4 = Line("lMagnet4", pMagnet4, pMagnet1)

        # Flächenerzeugen
        surfaceMagnet = Surface(
            "surfaceMagnet", [lMagnet1, lMagnet2, lMagnet3, lMagnet4]
        )

        # Bei jedem Baukasten muss diese Definition identisch sein
        self._geo_list = [surfaceMagnet]
        self._innerLinePart = [lMagnet4]
        self._airLinePart = []
        self._lamLinePart = [lMagnet1, lMagnet2, lMagnet3]
        self._laminationDockingPoint = [pMagnet1, pMagnet2, pMagnet3, pMagnet4]

        for s in self.geo_list:
            if isinstance(s, GmshSurface):
                if self.magDir == 1:
                    s.mesh_color = colorDict["Red"]
                elif self.magDir == -1:
                    s.mesh_color(colorDict["Green"])

    # def getAirDockingPoint(self):
    #     return self._airDockingPoint
