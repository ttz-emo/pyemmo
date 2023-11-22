from typing import List

from pyemmo.script.geometry.physicalElement import PhysicalElement
from .domain import Domain
from .stator import Stator, datamodel
from .statorLamination import StatorLamination
from .slot import Slot
from .line import Line
from .circleArc import CircleArc
from .point import Point
from .surface import Surface
from .airArea import AirArea
from .airGap import AirGap
from .limitLine import LimitLine
from .movingBand import MovingBand
from .slaveLine import SlaveLine
from .primaryLine import PrimaryLine
import math
from .. import colorDict

###
# Eine Instanz der Klasse StatorSPMSM beschreibt speziell den Stator einer permanent erregten Synchronmaschine mit Oberflächenmagneten im dreidimensionalen Raum.
# Diese Klasse wird in Verbindung mit der Klasse Maschinenklasse, MachineSPMSM verwendet.
# Die Art der Maschine wird mit der Maschinenklasse spezifiziert.
# Dies ist vorallem bei der Verwendung des Baukastens sinnvoll.
# Diese Unterklasse vom Stator arbeitet mit Bauelementen, die ebenfalls Unterklassen sind (bspw. slot_Form01 als Unterklasse von Slot).
###
class StatorPMSM(Stator):
    """
    Konstruktor der Klasse StatorPMSM.

    Input:
        lamninationType : String
        slotType : String
        nbrSlots: int
        angleGeoParts : Float
        nbrGeoParts : Int
        symmetryFactor : Int
        startPosition : Float (Optionaler Input)

    Bedeutung der Werte:
        laminationType : Name des Statorblechs z. B. sheet01_standard
        slotType : Name der einzusetzenden Nut z. B. slot_Form01
        nbrSlots : Anzahl der Statornuten (bei einem Vollmodell)
        angleGeoParts : Winkel des Teilmodells bei einer halben Nut, welche in der Klasse MachineSPMSM aus den Simulationsparametern berechnet wird.
        nbrGeoParts : Anzahl der Flächensegmete, die im Modell benötigt werden. Dieser Wert wird ebenfalls in MachineSPMSM bestimmt.
        symmetryFactor : Faktor des Teilmodells. Bei einem Vollmodell ist dieser Wert 1. Bei einem Viertelmodell 0.25.
        startPosition : Startwinkel mit dem die Simulation beginnen soll.
    """

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
        super().__init__(
            name="StatorSPMSM", nbrSlots=nbrSlots, axLen=axLen, winding=winding
        )
        ###Blechtype des Stators.
        self._laminationType = laminationType
        ###Nuttype des Stators.
        self._slotType = slotType
        ###Alle geometrischen Elemente, die den Stator beschreiben (Flächen und Linien mit Materialeigenschaften).
        self._physicalElements: List[PhysicalElement] = list()
        ###Winkel des Teilmodells bei einer halben Nut, welcher in der Klasse MachineSPMSM aus den Simulationsparametern berechnet wird.
        self._angleGeoParts = angleGeoParts
        ###Startwinkel mit dem die Simulation beginnen soll.
        self._startPosition = startPosition
        ###Anzahl der Flächensegmete, die im Modell benötigt werden. Dieser Wert wird ebenfalls in MachineSPMSM bestimmt.
        if float(nbrGeoParts).is_integer():
            self._nbrGeoParts = int(nbrGeoParts)
        else:
            raise ValueError(f"The number of segments is not an integer: {nbrGeoParts}")
        ###Faktor des Teilmodells. Bei einem Vollmodell ist dieser Wert 1. Bei einem Viertelmodell 4.
        if float(symmetryFactor).is_integer():
            self._symmetryFactor = int(symmetryFactor)
        else:
            raise ValueError(f"The symmetry factor is not an integer: {symmetryFactor}")

        ###Dictionary mit Blechparameter.
        self._laminationDict = None
        ###Dictionary mit Nutparameter.
        self._slotDict = None

    ###Mit addLaminationParameter() werden alle Parameter in das Laminationdictionary abgespeichert.
    def addLaminationParameter(self, laminationDict):
        self._laminationDict = laminationDict
        self._laminationDict["angleGeoParts"] = self._angleGeoParts
        self._laminationDict["startPosition"] = self._startPosition

    ###Mit addSlotParameter() werden alle Parameter in das Slotdictionary abgespeichert.
    def addSlotParameter(self, slotDict):
        self._slotDict = slotDict
        self._slotDict["startPosition"] = self._startPosition
        if self._laminationDict != None:
            self._slotDict["rI_Stator"] = self._laminationDict["r_S_i"]
            self._slotDict["machineCentrePoint"] = self._laminationDict[
                "machineCentrePoint"
            ]
        else:
            print("No definition of lamination. Use addLaminationParameter() first!")

    ###Mit addAirGapParameter werden alle Parameter in das Airgapdictionary abgespeichert.
    def addAirGapParameter(self, airGapDict):
        self._airGapDict = airGapDict
        if self._laminationDict == None or self._slotDict == None:
            print(
                "No defination of statorpart. Use addLaminationParameter() or addSlotParameter() first!"
            )

    ###createStator() erzeugt aus den Parameterdictionries und der ausgewählten Geometrie den Stator mit seinen Nutflächen.
    def createStator(self):
        if self._laminationDict == None or self._slotDict == None:
            print(
                "No definition of lamination or slot found. Use addLaminationParameter() or addSlotParameter to define your machine parts!"
            )
        else:
            if self._laminationType == "sheet01_standard":
                from .statorLamination_Sheet01_Standard import (
                    StatorLamination_Sheet01_Standard,
                )

                laminationPart = StatorLamination_Sheet01_Standard(self._laminationDict)

            if self._slotType == "slotForm_01":
                from .slot_Form01 import Slot_Form01

                slotPart = Slot_Form01(self._slotDict)

            # For testing:
            if self._slotType == "slotForm_03":
                from .slot_Form03 import Slot_Form03

                slotPart = Slot_Form03(self._slotDict)

            # slotForm_02 in Bearbeitung -> Noch nicht fertig definiert
            if self._slotType == "slotForm_02":
                print("i am here")
                from .slot_Form02 import Slot_Form02

                slotPart = Slot_Form02(self._slotDict)

            self._physicalRaw: List[PhysicalElement] = [laminationPart, slotPart]

        self._dockSlotToSheet()
        self._addAirSpace()
        self._createDuplicate()
        self._createConstraintLine()
        self._createDomainForStator()

    ###Diese Methode verbindet beide Flächen miteinander und entfernt übereinander liegende Punkte/Linien zwischen Blech und Nut.
    def _dockSlotToSheet(self):
        StatorSheet1 = self._physicalRaw[0]
        Slot1 = self._physicalRaw[1]

        allSlotOP = []
        allLamL = []
        allLamL2 = []

        for i1 in range(0, len(Slot1._innerLinePart)):
            sl_OP = {"SlotInnerLine": Slot1.innerLinePart[i1]}
            p1 = Slot1.innerLinePart[i1].startPoint
            p2 = Slot1.innerLinePart[i1].endPoint
            sl_OP["p1"] = p1
            sl_OP["p2"] = p2
            allSlotOP.append(sl_OP)

        for i2 in range(0, len(StatorSheet1._innerLinePart)):
            lamL1 = {"LaminationLine": StatorSheet1.innerLinePart[i2]}
            p1 = StatorSheet1.innerLinePart[i2].startPoint
            p2 = StatorSheet1.innerLinePart[i2].endPoint
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL.append(lamL1)

        for i3 in range(0, len(StatorSheet1._betweenLinePart)):
            lamL1 = {"LaminationLine": StatorSheet1.betweenLinePart[i2]}
            p1 = StatorSheet1.betweenLinePart[i2].startPoint
            p2 = StatorSheet1.betweenLinePart[i2].endPoint
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL2.append(lamL1)

        dockingPointSOP = Slot1.airDockingPoint[0]
        # prüfen welcher Punkt in allMagL der DockingPoint ist! -> Momentan allMagL darf nur ein Element besitzen -> Ansonsten hier eine For-Schleife einrichten.
        if allSlotOP[0]["p1"].coordinate == dockingPointSOP.coordinate:
            changePointSOP = allSlotOP[0]["p2"]
        elif allSlotOP[0]["p2"].coordinate == dockingPointSOP.coordinate:
            changePointSOP = allSlotOP[0]["p1"]

        # Punkt von Lamination holen, der verändert werden muss. Punkt wandert zu Ende des Magneten.
        testP = StatorSheet1.airDockingPoint1[0]
        for lElem in allLamL:
            if lElem["p1"].coordinate == testP.coordinate:
                lElem["LaminationLine"].startPoint = changePointSOP
            elif lElem["p2"].coordinate == testP.coordinate:
                lElem["LaminationLine"].endPoint = changePointSOP

        for lElem in allLamL2:
            if (
                StatorSheet1.betweenLinePart[0].startPoint.coordinate
                == testP.coordinate
            ):
                lElem["LaminationLine"].startPoint = Slot1.laminationDockingPoint[
                    0
                ]
            elif (
                StatorSheet1.betweenLinePart[0].endPoint.coordinate
                == testP.coordinate
            ):
                lElem["LaminationLine"].endPoint = Slot1.laminationDockingPoint[0]

        curveOfStatorSheet1 = StatorSheet1.geometricalElement[0].curve
        curveOfStatorSheet1 = curveOfStatorSheet1 + Slot1.laminationDockingLine
        StatorSheet1.geometricalElement[0].curve = curveOfStatorSheet1

    ###Mit addAirSpace() wird der Luftraum auf der Statorseite bis zum Movingband erzeugt und Materialeigenschaften definiert.
    def _addAirSpace(self):
        airGapLength = self._airGapDict["width"] / 4
        PCentre = self._laminationDict["machineCentrePoint"].duplicate()
        alpha = self._angleGeoParts
        pAir1: Point = self._physicalRaw[1].airDockingPoint[0].duplicate()
        pAir1.translate(
            -airGapLength * math.cos(alpha), -airGapLength * math.sin(alpha), 0
        )
        pAir2 = pAir1.duplicate()
        pAir2.rotateZ(PCentre, alpha)

        # createLine
        lAir1 = CircleArc("lAir1", pAir1, PCentre, pAir2)
        lAir2 = Line("lAir2", pAir1, self._physicalRaw[1].airDockingPoint[0])
        lAir3 = Line("lAir3", pAir2, self._physicalRaw[0].airDockingPoint2[0])
        sAir1 = Surface(
            "sAir1",
            [lAir1, lAir2, lAir3]
            + self._physicalRaw[0].innerLinePart
            + self._physicalRaw[1].innerLinePart,
        )
        sAir1.setMeshLength(airGapLength)
        airPart = AirGap("airStator", [sAir1], self._airGapDict["material"])
        self._physicalRaw.append(airPart)

    ###createDuplicate() vervollständig die Geometrie zum gewünschten Teil- bzw. Vollmodell.
    def _createDuplicate(self):
        # duplicate
        allGeo = self._physicalRaw[0].geometricalElement
        PCentre = self._laminationDict["machineCentrePoint"].duplicate()
        pH1 = self._physicalRaw[0].betweenLinePart[0].startPoint
        hilfsLinie1 = Line("L_hilf1", PCentre, pH1)
        ez = Point("p_Z", PCentre._x, PCentre._y, PCentre._z + 1, 1)
        hilfsLinie2 = Line("L_hilf2", PCentre, ez)
        surfaceStator2 = allGeo[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        allGeo.append(surfaceStator2)
        alpha = self._angleGeoParts * 2
        listGeo = []
        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in allGeo:
                sNew = s.duplicate()
                sNew.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                listGeo.append(sNew)

        wholeLamination = StatorLamination(
            "laminationSPMSM_Stator", allGeo + listGeo, self._laminationDict["material"]
        )
        self._physicalElements.append(wholeLamination)

        # duplicate Slot
        slotSurfs: List[Surface] = [self._physicalRaw[1].geometricalElement[1]]
        surfaceSlot2 = slotSurfs[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        slotSurfs.insert(0, surfaceSlot2)
        slot1 = Slot("", [surfaceSlot2], self._slotDict["material"])
        slot1.name = "slot_" + str(slot1.id)
        slot2 = Slot("", [slotSurfs[1]], self._slotDict["material"])
        slot2.name = "slot_" + str(slot2.id)
        allSlot = [slot1, slot2]

        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in slotSurfs:
                sNew2 = s.duplicate()
                sNew2.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                slot3 = Slot("", [sNew2], self._slotDict["material"])
                slot3.name = "slot_" + str(slot3.id)
                allSlot.append(slot3)

        self._physicalElements = self._physicalElements + allSlot

        # duplicate SlotOP
        allGeo3 = [self._physicalRaw[1].geometricalElement[0]]
        surfaceAir2 = allGeo3[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        allGeo3.append(surfaceAir2)
        listGeo3 = []
        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in allGeo3:
                sNew = s.duplicate()
                sNew.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                listGeo3.append(sNew)

        if self._slotDict["slot_OPAir"] == True:
            wholeAir = AirArea(
                "Airslot", allGeo3 + listGeo3, self._airGapDict["material"]
            )
        else:
            wholeAir = StatorLamination(
                "slotOP", allGeo3 + listGeo3, self._laminationDict["material"]
            )

        self._physicalElements.append(wholeAir)

        # duplicate AirGap
        allGeo4 = self._physicalRaw[2].geometricalElement
        surfaceAirGap2 = allGeo4[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        allGeo4.append(surfaceAirGap2)
        listGeo4 = []
        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in allGeo4:
                sNew = s.duplicate()
                sNew.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                listGeo4.append(sNew)

        wholeAirGap = AirGap(
            "statorAirGap", allGeo4 + listGeo4, self._airGapDict["material"]
        )
        self._physicalElements.append(wholeAirGap)

    ###Mit createConstraintLine werden alle Grenzlinien, Movingbands, primary- und Slavelinien definiert.
    def _createConstraintLine(self):
        angle = self._angleGeoParts
        pLimitOuter1 = Point(
            "pLimitOuter1",
            self._laminationDict["r_S_a"]
            + self._laminationDict["machineCentrePoint"]._x,
            self._laminationDict["machineCentrePoint"]._y,
            self._laminationDict["machineCentrePoint"]._z,
            1,
        )
        pLimitOuter2 = pLimitOuter1.duplicate()
        pLimitOuter2.rotateZ(self._laminationDict["machineCentrePoint"], angle)
        curveOuter = [
            CircleArc(
                "curveOuter",
                pLimitOuter1,
                self._laminationDict["machineCentrePoint"],
                pLimitOuter2,
            )
        ]
        mbStator: List[CircleArc] = [
            self._physicalRaw[2].geometricalElement[0].curve[0].duplicate()
        ]
        mbStator[0].rotateZ(self._laminationDict["machineCentrePoint"], -1 * angle)

        for i in range(1, self._nbrGeoParts):
            c1 = curveOuter[0].duplicate()
            c1.rotateZ(self._laminationDict["machineCentrePoint"], i * angle)
            curveOuter.append(c1)
            c2 = mbStator[0].duplicate()
            c2.rotateZ(self._laminationDict["machineCentrePoint"], i * angle)
            mbStator.append(c2)

        outerLimitLine = LimitLine("OuterLimitLine_Stator", curveOuter)
        mbStatorLine = MovingBand(
            "movingBand_StatorLine", mbStator, self._airGapDict["material"]
        )
        self._physicalElements.append(outerLimitLine)
        self._physicalElements.append(mbStatorLine)

        pprimary1 = Point("pprimary1", self._laminationDict["r_S_i"], 0, 0, 1)
        pprimary2 = Point("pprimary2", self._laminationDict["r_S_a"], 0, 0, 1)
        lLamprimary = Line("lLamprimary", pprimary1, pprimary2)
        lAir = self._physicalRaw[2].geometricalElement[0].curve[1].duplicate()
        lAir.rotateZ(self._laminationDict["machineCentrePoint"], -1 * angle)

        primaryLine1 = PrimaryLine("primary_StatorLine", [lLamprimary, lAir])
        self._physicalElements.append(primaryLine1)

        allslaveLine = primaryLine1.geometricalElement
        slaveLineArray = []
        for l in allslaveLine:
            l1 = l.duplicate()
            l1.rotateZ(
                self._laminationDict["machineCentrePoint"], self._nbrGeoParts * angle
            )
            slaveLineArray.append(l1)
        slaveLine1 = SlaveLine("slave_StatorLine", slaveLineArray)
        self._physicalElements.append(slaveLine1)
