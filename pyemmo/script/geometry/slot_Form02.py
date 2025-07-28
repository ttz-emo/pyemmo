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
"""Module for class Slot_Form02"""
from __future__ import annotations

import math

from .circleArc import CircleArc
from .line import Line
from .point import Point
from .slot import Slot
from .surface import Surface


class Slot_Form02(Slot):
    def __init__(self, machineDict):
        self.machineDict = machineDict
        ###ID für die Physical Surface.
        super().__init__(
            name="Slot_Form02",
            geo_list=[],
            material=machineDict["material"],
        )
        self._name = "Slot_Form02_" + str(self.id)
        self._createGeometry()

    def _createGeometry(self):
        dockingLength = self.machineDict["rI_Stator"]
        angle_slotOP = math.atan2(self.machineDict["w_SlotOP"], dockingLength)

        PCentre: Point = self.machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.coordinate
        angleStart = self.machineDict["startPosition"]

        # Konstuktion der Punkte an der x-Achse
        pS1 = Point(
            "pSlot1",
            coordCentre[0] + dockingLength,
            coordCentre[1],
            coordCentre[2],
            self.machineDict["meshLength"],
        )
        pS2 = pS1.duplicate()
        pS2.rotateZ(PCentre, angle_slotOP)
        pS3 = pS1.duplicate()
        pS3.translate(self.machineDict["h_SlotOP"], 0, 0)
        pS4 = pS3.duplicate()
        pS4.rotateZ(PCentre, angle_slotOP)

        pS5 = pS1.duplicate()
        pS5.translate(self.machineDict["h_Wedge"], self.machineDict["w_Wedge"] / 2, 0)
        pS6 = pS3.duplicate()
        pS6.translate(self.machineDict["h_Slot"], 0, 0)
        pS7 = pS6.duplicate()
        pS7.translate(0, self.machineDict["w_Slot"], 0)

        pS1.rotateZ(PCentre, angleStart)
        pS2.rotateZ(PCentre, angleStart)
        pS3.rotateZ(PCentre, angleStart)
        pS4.rotateZ(PCentre, angleStart)
        pS5.rotateZ(PCentre, angleStart)
        pS6.rotateZ(PCentre, angleStart)
        pS7.rotateZ(PCentre, angleStart)

        # Konstuktion der Linien
        lS1 = CircleArc("lS1", pS1, PCentre, pS2)
        lS2 = Line("lS2", pS1, pS3)
        lS3 = Line("lS3", pS2, pS4)
        lS4 = CircleArc("lS4", pS3, PCentre, pS4)

        lS5 = Line("lS5", pS4, pS5)
        lS6 = Line("lS6", pS5, pS7)
        lS7 = Line("lS7", pS7, pS6)
        lS8 = Line("lS8", pS6, pS3)

        # Flächenerzeugen
        surfaceSlotOP = Surface("slotOP", [lS1, lS2, lS3, lS4])
        surfaceSlot = Surface("slotF1", [lS4, lS5, lS6, lS7, lS8])

        # Bei jedem Baukasten muss diese Definition identisch sein
        self._geo_list = [surfaceSlotOP, surfaceSlot]
        self._innerLinePart = [lS1]
        self._airDockingLine = [lS1]
        self._airDockingPoint = [pS1]
        self._laminationDockingLine = [lS3, lS5, lS6, lS7]
        self._laminationDockingPoint = [pS6]
        self._betweenLinePart = [lS8, lS2]

    @property
    def betweenLinePart(self):
        """Getter of betweenLinePart

        Returns:
            _type_: _description_
        """
        return self._betweenLinePart

    @property
    def airDockingLine(self):
        """Getter of airDockingLine

        Returns:
            _type_: _description_
        """
        return self._airDockingLine

    @property
    def innerLinePart(self):
        """Getter of innerLinePart

        Returns:
            _type_: _description_
        """
        return self._innerLinePart

    @property
    def airDockingPoint(self):
        """Getter of airDockingPoint

        Returns:
            _type_: _description_
        """
        return self._airDockingPoint

    @property
    def laminationDockingLine(self):
        """Getter of laminationDockingLine

        Returns:
            _type_: _description_
        """
        return self._laminationDockingLine

    @property
    def laminationDockingPoint(self):
        """Getter of laminationDockingPoint

        Returns:
            _type_: _description_
        """
        return self._laminationDockingPoint
