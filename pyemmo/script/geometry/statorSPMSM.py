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
"""Module for PMSM Stator"""
from __future__ import annotations

import math

from pyemmo.script.geometry.physicalElement import PhysicalElement

from .airArea import AirArea
from .airGap import AirGap
from .circleArc import CircleArc
from .limitLine import LimitLine
from .line import Line
from .movingBand import MovingBand
from .point import Point
from .primaryLine import PrimaryLine
from .slaveLine import SlaveLine
from .slot import Slot
from .slot_Form01 import Slot_Form01
from .slot_Form02 import Slot_Form02
from .slot_Form03 import Slot_Form03
from .stator import Stator, datamodel
from .statorLamination import StatorLamination
from .statorLamination_Sheet01_Standard import (
    StatorLamination_Sheet01_Standard,
)
from .surface import Surface


###
# Eine Instanz der Klasse StatorSPMSM beschreibt speziell den Stator einer permanent erregten Synchronmaschine mit Oberflächenmagneten im dreidimensionalen Raum.
# Diese Klasse wird in Verbindung mit der Klasse Maschinenklasse, MachineSPMSM verwendet.
# Die Art der Maschine wird mit der Maschinenklasse spezifiziert.
# Dies ist vorallem bei der Verwendung des Baukastens sinnvoll.
# Diese Unterklasse vom Stator arbeitet mit Bauelementen, die ebenfalls Unterklassen sind (bspw. slot_Form01 als Unterklasse von Slot).
###
class StatorPMSM(Stator):
    """Class for PMSM Stator"""

    def __init__(
        self,
        laminationType,
        slotType,
        nbrSlots: int,
        angleGeoParts: float,
        nbrGeoParts: int,
        symmetryFactor: int,
        axLen: float = 1.0,
        winding: datamodel = None,
        startPosition: float = 0.0,
    ):
        """
        Konstruktor der Klasse StatorPMSM.

        Args:
            lamninationType (str): Name des Statorblechs z. B. sheet01_standard
            slotType (str): Name der einzusetzenden Nut z. B. slot_Form01
            nbrSlots (int): Anzahl der Statornuten (bei einem Vollmodell)
            angleGeoParts (float): Winkel des Teilmodells bei einer halben Nut, welche in der Klasse
             MachineSPMSM aus den Simulationsparametern berechnet wird.
            nbrGeoParts (int): Anzahl der Flächensegmete, die im Modell benötigt werden. Dieser Wert
             wird ebenfalls in MachineSPMSM bestimmt.
            symmetryFactor (int): Faktor des Teilmodells. Bei einem Vollmodell ist dieser Wert 1.
             Bei einem Viertelmodell 4.
            startPosition (float): Startwinkel mit dem die Simulation beginnen soll. Defaults to 0.0
        """
        super().__init__(
            name="StatorSPMSM", nbrSlots=nbrSlots, axLen=axLen, winding=winding
        )
        ###Blechtype des Stators.
        self.laminationType = laminationType
        ###Nuttype des Stators.
        self.slotType = slotType
        ###Winkel des Teilmodells bei einer halben Nut, welcher in der Klasse MachineSPMSM aus den Simulationsparametern berechnet wird.
        self.angleGeoParts = angleGeoParts
        ###Startwinkel mit dem die Simulation beginnen soll.
        self.startPosition = startPosition
        ###Anzahl der Flächensegmete, die im Modell benötigt werden. Dieser Wert wird ebenfalls in MachineSPMSM bestimmt.
        if float(nbrGeoParts).is_integer():
            self.nbrGeoParts = int(nbrGeoParts)
        else:
            raise ValueError(
                f"The number of segments is not an integer: {nbrGeoParts}"
            )
        ###Faktor des Teilmodells. Bei einem Vollmodell ist dieser Wert 1. Bei einem Viertelmodell 4.
        if float(symmetryFactor).is_integer():
            self.symmetryFactor = int(symmetryFactor)
        else:
            raise ValueError(
                f"The symmetry factor is not an integer: {symmetryFactor}"
            )

        ###Dictionary mit Blechparameter.
        self.laminationDict = None
        ###Dictionary mit Nutparameter.
        self.slotDict = None

    def addLaminationParameter(self, laminationDict: dict):
        """Mit addLaminationParameter() werden alle Parameter in das Laminationdictionary abgespeichert.

        Args:
            laminationDict (diot): lamination parameter dict.
        """
        self.laminationDict = laminationDict
        self.laminationDict["angleGeoParts"] = self.angleGeoParts
        self.laminationDict["startPosition"] = self.startPosition

    def addSlotParameter(self, slotDict: dict):
        """Mit addSlotParameter() werden alle Parameter in das Slotdictionary abgespeichert.

        Args:
            slotDict (dict): Slot parameter dict.
        """
        self.slotDict = slotDict
        self.slotDict["startPosition"] = self.startPosition
        if self.laminationDict is not None:
            self.slotDict["rI_Stator"] = self.laminationDict["r_S_i"]
            self.slotDict["machineCentrePoint"] = self.laminationDict[
                "machineCentrePoint"
            ]
        else:
            print(
                "No definition of lamination. Use addLaminationParameter() first!"
            )

    def addAirGapParameter(self, airGapDict: dict):
        """Mit addAirGapParameter werden alle Parameter in das Airgapdictionary abgespeichert.

        Args:
            airGapDict (dict): Airgap parameter dict.
        """
        self.airGapDict = airGapDict
        if self.laminationDict is None or self.slotDict is None:
            print(
                "No defination of statorpart. Use addLaminationParameter() or addSlotParameter() first!"
            )

    def createStator(self):
        """createStator() erzeugt aus den Parameterdictionries und der ausgewählten Geometrie den Stator mit seinen Nutflächen."""
        if self.laminationDict is None or self.slotDict is None:
            print(
                "No definition of lamination or slot found. Use addLaminationParameter() or addSlotParameter to define your machine parts!"
            )
        else:
            if self.laminationType == "sheet01_standard":
                laminationPart = StatorLamination_Sheet01_Standard(
                    self.laminationDict
                )

            if self.slotType == "slotForm_01":
                slotPart = Slot_Form01(self.slotDict)

            if self.slotType == "slotForm_03":
                slotPart = Slot_Form03(self.slotDict)

            if self.slotType == "slotForm_02":
                slotPart = Slot_Form02(self.slotDict)

            self.physicalRaw: list[PhysicalElement] = [
                laminationPart,
                slotPart,
            ]

        self._dockSlotToSheet()
        self._addAirSpace()
        self._createDuplicate()
        self._createConstraintLine()
        self._createDomainForStator()

    def _dockSlotToSheet(self):
        """Diese Methode verbindet beide Flächen miteinander und entfernt übereinander liegende Punkte/Linien zwischen Blech und Nut."""
        statorSheet1: StatorLamination_Sheet01_Standard = self.physicalRaw[0]
        slot1: Slot_Form01 = self.physicalRaw[1]

        allSlotOP: list[dict] = []
        allLamL: list[dict] = []
        allLamL2: list[dict] = []

        for inLineSlot in slot1.innerLinePart:
            sl_OP = {"SlotInnerLine": inLineSlot}
            p1 = inLineSlot.startPoint
            p2 = inLineSlot.endPoint
            sl_OP["p1"] = p1
            sl_OP["p2"] = p2
            allSlotOP.append(sl_OP)

        for inLineLam in statorSheet1.innerLinePart:
            lamL1 = {"LaminationLine": inLineLam}
            p1 = inLineLam.startPoint
            p2 = inLineLam.endPoint
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL.append(lamL1)

        for interLamLine in statorSheet1.betweenLinePart:
            lamL1 = {"LaminationLine": interLamLine}
            p1 = interLamLine.startPoint
            p2 = interLamLine.endPoint
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL2.append(lamL1)

        dockingPointSlotOpening = slot1.airDockingPoint[0]
        # prüfen welcher Punkt in allMagL der DockingPoint ist! -> Momentan allMagL darf nur ein Element besitzen -> Ansonsten hier eine For-Schleife einrichten.
        if slot1.innerLinePart[0].startPoint.isEqual(dockingPointSlotOpening):
            changePointSOP = slot1.innerLinePart[0].endPoint
        elif slot1.innerLinePart[0].endPoint.isEqual(dockingPointSlotOpening):
            changePointSOP = slot1.innerLinePart[0].startPoint

        # Punkt von Lamination holen, der verändert werden muss. Punkt wandert zu Ende des Magneten.
        statorAirDockPoint = statorSheet1.airDockingPoint1[0]
        for lElem in allLamL:
            if lElem["p1"].coordinate == statorAirDockPoint.coordinate:
                lElem["LaminationLine"].startPoint = changePointSOP
            elif lElem["p2"].coordinate == statorAirDockPoint.coordinate:
                lElem["LaminationLine"].endPoint = changePointSOP

        for lElem in allLamL2:
            if statorSheet1.betweenLinePart[0].startPoint.isEqual(
                statorAirDockPoint
            ):
                lElem["LaminationLine"].startPoint = (
                    slot1.laminationDockingPoint[0]
                )
            elif statorSheet1.betweenLinePart[0].endPoint.isEqual(
                statorAirDockPoint
            ):
                lElem["LaminationLine"].endPoint = (
                    slot1.laminationDockingPoint[0]
                )

        curveOfStatorSheet1 = statorSheet1.geometricalElement[0].curve
        curveOfStatorSheet1 = curveOfStatorSheet1 + slot1.laminationDockingLine
        statorSheet1.geometricalElement[0].curve = curveOfStatorSheet1

    def _addAirSpace(self):
        """Mit addAirSpace() wird der Luftraum auf der Statorseite bis zum Movingband erzeugt und Materialeigenschaften definiert."""
        airGapLength = self.airGapDict["width"] / 4
        centerPoint: Point = self.laminationDict[
            "machineCentrePoint"
        ].duplicate()
        alpha = self.angleGeoParts
        pAir1: Point = self.physicalRaw[1].airDockingPoint[0].duplicate()
        pAir1.translate(
            -airGapLength * math.cos(alpha), -airGapLength * math.sin(alpha), 0
        )
        pAir2 = pAir1.duplicate()
        pAir2.rotateZ(centerPoint, alpha)

        # createLine
        lAir1 = CircleArc("lAir1", pAir1, centerPoint, pAir2)
        lAir2 = Line("lAir2", pAir1, self.physicalRaw[1].airDockingPoint[0])
        lAir3 = Line("lAir3", pAir2, self.physicalRaw[0].airDockingPoint2[0])
        sAir1 = Surface(
            "sAir1",
            [lAir1, lAir2, lAir3]
            + self.physicalRaw[0].innerLinePart
            + self.physicalRaw[1].innerLinePart,
        )
        sAir1.setMeshLength(airGapLength)
        airPart = AirGap("airStator", [sAir1], self.airGapDict["material"])
        self.physicalRaw.append(airPart)

    ###createDuplicate() vervollständig die Geometrie zum gewünschten Teil- bzw. Vollmodell.
    def _createDuplicate(self):
        # duplicate
        allGeo = self.physicalRaw[0].geometricalElement
        centerPoint: Point = self.laminationDict[
            "machineCentrePoint"
        ].duplicate()
        pH1 = self.physicalRaw[0].betweenLinePart[0].startPoint
        hilfsLinie1 = Line("L_hilf1", centerPoint, pH1)
        ez = Point(
            "p_Z",
            centerPoint.coordinate[0],
            centerPoint.coordinate[1],
            centerPoint.coordinate[2] + 1,
            1,
        )
        hilfsLinie2 = Line("L_hilf2", centerPoint, ez)
        surfaceStator2: Surface = allGeo[0].mirror(
            centerPoint, hilfsLinie1, hilfsLinie2
        )
        allGeo.append(surfaceStator2)
        alpha = self.angleGeoParts * 2
        listGeo: list[Surface] = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            for s in allGeo:
                sNew = s.duplicate()
                sNew.rotateZ(
                    self.laminationDict["machineCentrePoint"], i * alpha
                )
                listGeo.append(sNew)

        wholeLamination = StatorLamination(
            "laminationSPMSM_Stator",
            allGeo + listGeo,
            self.laminationDict["material"],
        )
        self._physicalElements.append(wholeLamination)

        # duplicate Slot
        slotSurfs: list[Surface] = [self.physicalRaw[1].geometricalElement[1]]
        surfaceSlot2 = slotSurfs[0].mirror(
            centerPoint, hilfsLinie1, hilfsLinie2
        )
        slotSurfs.insert(0, surfaceSlot2)
        slot1 = Slot("", [surfaceSlot2], self.slotDict["material"])
        slot1.name = "slot_" + str(slot1.id)
        slot2 = Slot("", [slotSurfs[1]], self.slotDict["material"])
        slot2.name = "slot_" + str(slot2.id)
        allSlot = [slot1, slot2]

        for i in range(1, int(self.nbrGeoParts / 2)):
            for s in slotSurfs:
                sNew2 = s.duplicate()
                sNew2.rotateZ(
                    self.laminationDict["machineCentrePoint"], i * alpha
                )
                slot3 = Slot("", [sNew2], self.slotDict["material"])
                slot3.name = "slot_" + str(slot3.id)
                allSlot.append(slot3)

        self.physicalElements = self._physicalElements + allSlot

        # duplicate SlotOP
        allGeo3 = [self.physicalRaw[1].geometricalElement[0]]
        surfaceAir2 = allGeo3[0].mirror(centerPoint, hilfsLinie1, hilfsLinie2)
        allGeo3.append(surfaceAir2)
        listGeo3 = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            for s in allGeo3:
                sNew = s.duplicate()
                sNew.rotateZ(
                    self.laminationDict["machineCentrePoint"], i * alpha
                )
                listGeo3.append(sNew)

        if self.slotDict["slot_OPAir"]:
            wholeAir = AirArea(
                "Airslot", allGeo3 + listGeo3, self.airGapDict["material"]
            )
        else:
            wholeAir = StatorLamination(
                "slotOP", allGeo3 + listGeo3, self.laminationDict["material"]
            )

        self._physicalElements.append(wholeAir)

        # duplicate AirGap
        allGeo4 = self.physicalRaw[2].geometricalElement
        surfaceAirGap2 = allGeo4[0].mirror(
            centerPoint, hilfsLinie1, hilfsLinie2
        )
        allGeo4.append(surfaceAirGap2)
        listGeo4 = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            for s in allGeo4:
                sNew = s.duplicate()
                sNew.rotateZ(
                    self.laminationDict["machineCentrePoint"], i * alpha
                )
                listGeo4.append(sNew)

        wholeAirGap = AirGap(
            "statorAirGap", allGeo4 + listGeo4, self.airGapDict["material"]
        )
        self._physicalElements.append(wholeAirGap)

    ###Mit createConstraintLine werden alle Grenzlinien, Movingbands, primary- und Slavelinien definiert.
    def _createConstraintLine(self):
        angle = self.angleGeoParts
        machineCenterPoint: Point = self.laminationDict["machineCentrePoint"]
        pLimitOuter1 = machineCenterPoint.duplicate("pLimitOuter1")
        pLimitOuter1.translate(self.laminationDict["r_S_a"], 0, 0)
        pLimitOuter2 = pLimitOuter1.duplicate()
        pLimitOuter2.rotateZ(machineCenterPoint, angle)
        curveOuter = [
            CircleArc(
                "curveOuter",
                pLimitOuter1,
                machineCenterPoint,
                pLimitOuter2,
            )
        ]
        mbStator: list[CircleArc] = [
            self.physicalRaw[2].geometricalElement[0].curve[0].duplicate()
        ]
        mbStator[0].rotateZ(machineCenterPoint, -1 * angle)

        for i in range(1, self.nbrGeoParts):
            c1 = curveOuter[0].duplicate()
            c1.rotateZ(machineCenterPoint, i * angle)
            curveOuter.append(c1)
            c2 = mbStator[0].duplicate()
            c2.rotateZ(machineCenterPoint, i * angle)
            mbStator.append(c2)

        outerLimitLine = LimitLine("OuterLimitLine_Stator", curveOuter)
        mbStatorLine = MovingBand(
            "movingBand_StatorLine", mbStator, self.airGapDict["material"]
        )
        self._physicalElements.append(outerLimitLine)
        self._physicalElements.append(mbStatorLine)

        pprimary1 = Point("pprimary1", self.laminationDict["r_S_i"], 0, 0, 1)
        pprimary2 = Point("pprimary2", self.laminationDict["r_S_a"], 0, 0, 1)
        lLamprimary = Line("lLamprimary", pprimary1, pprimary2)
        lAir = self.physicalRaw[2].geometricalElement[0].curve[1].duplicate()
        lAir.rotateZ(machineCenterPoint, -1 * angle)

        primaryLine1 = PrimaryLine("primary_StatorLine", [lLamprimary, lAir])
        self._physicalElements.append(primaryLine1)

        allslaveLine = primaryLine1.geometricalElement
        slaveLineArray = []
        for l in allslaveLine:
            l1 = l.duplicate()
            l1.rotateZ(machineCenterPoint, self.nbrGeoParts * angle)
            slaveLineArray.append(l1)
        slaveLine1 = SlaveLine("slave_StatorLine", slaveLineArray)
        self._physicalElements.append(slaveLine1)
