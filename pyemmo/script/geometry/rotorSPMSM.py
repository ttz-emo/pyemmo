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
from __future__ import annotations

import math

from .airArea import AirArea
from .airGap import AirGap
from .circleArc import CircleArc
from .domain import Domain
from .limitLine import LimitLine
from .line import Line
from .magnet import Magnet
from .movingBand import MovingBand
from .physicalElement import PhysicalElement
from .point import Point
from .primaryLine import PrimaryLine
from .rotor import Rotor
from .rotorLamination import RotorLamination
from .rotorLamination_Sheet01_Standard import RotorLamination_Sheet01_Standard
from .slaveLine import SlaveLine
from .spline import Spline
from .surface import Surface


###
# Eine Instanz der Klasse RotorSPMSM beschreibt speziell den Rotor einer permanent erregten Synchronmaschine mit Oberflächenmagneten im dreidimensionalen Raum.
# Diese Klasse wird in Verbindung mit der Klasse Maschinenklasse, MachineSPMSM verwendet.
# Die Art der Maschine wird mit der Maschinenklasse spezifiziert.
# Dies ist vorallem bei der Verwendung des Baukastens sinnvoll.
# Diese Unterklasse vom Rotor arbeitet mit Bauelementen, die ebenfalls Unterklassen sind (bspw. magnet_Surface01 als Unterklasse von Magnet).
###
class RotorSPMSM(Rotor):
    def __init__(
        self,
        laminationType: str,
        magnetType: str,
        angleGeoParts: float,
        nbrGeoParts: int,
        symmetryFactor: int,
        startPosition: float = 0,
        axLen: float = 1.0,
    ):
        """Konstruktor der Klasse RotorSPMSM.

        Args:
            laminationType (str): Name des Rotorblechs z. B. sheet01_standard
            magnetType (str): Name des einzusetzenden Magneten z. B. magnet03_surface
            angleGeoParts (float): Winkel des Teilmodells bei einem halben Pol, welches in der Klasse MachineSPMSM aus den Simulationsparametern berechnet wird.
            nbrGeoParts (int): Anzahl der Flächensegmete, die im Modell benötigt werden. Dieser Wert wird ebenfalls in MachineSPMSM bestimmt.
            symmetryFactor (int): Faktor des Teilmodells. Bei einem Vollmodell ist dieser Wert 1. Bei einem Viertelmodell 0.25.
            startPosition (float, optional): Startwinkel mit dem die Simulation beginnen soll. Defaults to 0.
            axLen (float, optional): Axial length of rotor. Defaults to 1.0.

        Raises:
            ValueError: _description_
        """
        super().__init__(physicalElementList=[], name="RotorSPMSM", axLen=axLen)
        self.laminationType = laminationType
        self.magnetType = magnetType
        ###Dictionary mit Blechparameter.
        self.laminationDict = None
        ###Dictionary mit Magnetparameter.
        self.magnetDict = None
        self.angleGeoParts = angleGeoParts
        self.startPosition = startPosition
        if float(nbrGeoParts).is_integer():
            self.nbrGeoParts = int(nbrGeoParts)
        else:
            raise ValueError(f"Number of geometry parts is not int!: {nbrGeoParts}")
        self.symmetryFactor = symmetryFactor

    ###Mit addLaminationParameter werden alle Parameter in das Laminationdictionary abgespeichert.
    def addLaminationParameter(self, laminationDict):
        # TODO: change lamDict to single attributes
        self.laminationDict = laminationDict
        self.laminationDict["angleGeoParts"] = self.angleGeoParts
        self.laminationDict["startPosition"] = self.startPosition

    ###Mit addMagnetParameter werden alle Parameter in das Magnetdictionary abgespeichert.
    def addMagnetParameter(self, magnetDict):
        self.magnetDict = magnetDict
        self.magnetDict["startPosition"] = self.startPosition
        if self.laminationDict != None:
            self.magnetDict["rA_Rotor"] = self.laminationDict["r_R"]
            self.magnetDict["machineCentrePoint"] = self.laminationDict[
                "machineCentrePoint"
            ]
        else:
            print("No definition of lamination. Use addLaminationParameter() first!")

    ###Mit addAirGapParameter werden alle Parameter in das Airgapdictionary abgespeichert.
    def addAirGapParameter(self, airGapDict):
        self._airGapDict = airGapDict
        if self.laminationDict == None or self.magnetDict == None:
            print(
                "No defination of rotorpart. Use addLaminationParameter() or addMagnetParameter() first!"
            )

    ###createRotor() erzeugt aus den Parameterdictionries und der ausgewählten Geometrie den Rotor mit seinen Oberflächenmagneten.
    def createRotor(self):
        if self.laminationDict == None or self.magnetDict == None:
            print(
                "No definition of lamination or magnet found. Use addLaminationParameter() or addMagnetParameter to define your machine parts!"
            )
        else:
            # ONLY ONE SHEET TYPE POSSIBLE BY NOW...
            # if self._laminationType == "sheet01_standard":
            #     from .rotorLamination_Sheet01_Standard import (
            #         RotorLamination_Sheet01_Standard,
            #     )
            laminationPart = RotorLamination_Sheet01_Standard(self.laminationDict)

            if self.magnetType == "magnet01_surface":
                from .magnet_Surface01 import Magnet_Surface01

                magnetPart = Magnet_Surface01(
                    self.magnetDict,
                    self.magnetDict["magnetisationDirection"][0],
                    self.magnetDict["magnetisationType"],
                )

            if self.magnetType == "magnet02_surface":
                from .magnet_Surface02 import Magnet_Surface02

                magnetPart = Magnet_Surface02(
                    self.magnetDict,
                    self.magnetDict["magnetisationDirection"][0],
                    self.magnetDict["magnetisationType"],
                )

            if self.magnetType == "magnet03_surface":
                from .magnet_Surface03 import Magnet_Surface03

                magnetPart = Magnet_Surface03(
                    self.magnetDict,
                    self.magnetDict["magnetisationDirection"][0],
                    self.magnetDict["magnetisationType"],
                )

            self._physicalElements: list[PhysicalElement] = [
                laminationPart,
                magnetPart,
            ]

        self._dockMagnetToSheet()
        self._addAirSpace()
        self._createDuplicate()
        self._createConstraintLine()
        mag: Magnet = self._physicalElements[1]
        if mag.magType in ("radial", "parallel"):
            allAngle = self._calculateAngleForParallelMagnet()
            for i, mag in enumerate(self.getAllMagnet()):
                mag.magAngle = allAngle[i]
        else:
            raise RuntimeError(f"Wrong magnetization type:{mag.magType}")
        self._createDomainForRotor()

    ###Die Methode _calculateAngleForParallelMagnet wird nur bei der parallelen oder tangentialen Magnetisierung verwendet. Diese Funktion berechnet den Winkel des Magnetisierungs-Richtungs-Vektors.
    def _calculateAngleForParallelMagnet(self):
        Magnet1: Magnet = self._physicalElements[1]
        dockingPointM = Magnet1.laminationDockingPoint[0].duplicate()
        coordDPM = dockingPointM.coordinate
        angleParallel1 = math.atan2(coordDPM[1], coordDPM[0])
        allAngleParallel = [angleParallel1]
        alpha = self.angleGeoParts * 2
        for i in range(1, int(self.nbrGeoParts / 2)):
            dockingPointM.rotateZ(self.laminationDict["machineCentrePoint"], alpha)
            coordDPM = dockingPointM.coordinate
            angle = math.atan2(coordDPM[1], coordDPM[0])
            allAngleParallel.append(angle)
        return allAngleParallel

    ###Diese Methode verbindet beide Flächen miteinander und entfernt übereinander liegende Punkte/Linien zwischen Blech und Magnet.
    def _dockMagnetToSheet(self):
        RotorSheet1 = self._physicalElements[0]
        Magnet1 = self._physicalElements[1]
        allMagL = []
        allLamL = []
        allLamL2 = []

        for i1 in range(0, len(Magnet1._innerLinePart)):
            magL1 = {"MagnetLine": Magnet1.innerLinePart[i1]}
            p1 = Magnet1.innerLinePart[i1].start_point
            p2 = Magnet1.innerLinePart[i1].end_point
            magL1["p1"] = p1
            magL1["p2"] = p2
            allMagL.append(magL1)

        for i2 in range(0, len(RotorSheet1._outerLinePart)):
            lamL1 = {"LaminationLine": RotorSheet1.outerLinePart[i2]}
            p1 = RotorSheet1.outerLinePart[i2].start_point
            p2 = RotorSheet1.outerLinePart[i2].end_point
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL.append(lamL1)

        for i3 in range(0, len(RotorSheet1._betweenLinePart)):
            lamL1 = {"LaminationLine": RotorSheet1.betweenLinePart[i2]}
            p1 = RotorSheet1.betweenLinePart[i2].start_point
            p2 = RotorSheet1.betweenLinePart[i2].end_point
            lamL1["p1"] = p1
            lamL1["p2"] = p2
            allLamL2.append(lamL1)

        dockingPointM = Magnet1.laminationDockingPoint[0]
        # prüfen welcher Punkt in allMagL der DockingPoint ist! -> Momentan allMagL darf nur ein Element besitzen -> Ansonsten hier eine For-Schleife einrichten.
        if allMagL[0]["p1"].coordinate == dockingPointM.coordinate:
            changePointM = allMagL[0]["p2"]
        elif allMagL[0]["p2"].coordinate == dockingPointM.coordinate:
            changePointM = allMagL[0]["p1"]

        # Punkt von Lamination holen, der verändert werden muss. Punkt wandert zu Ende des Magneten.
        testP = RotorSheet1.airDockingPoint1[0]
        for lElem in allLamL:
            if lElem["p1"].coordinate == testP.coordinate:
                lElem["LaminationLine"].start_point = changePointM
            elif lElem["p2"].coordinate == testP.coordinate:
                lElem["LaminationLine"].end_point = changePointM

        for lElem in allLamL2:
            if lElem["p1"].coordinate == testP.coordinate:
                lElem["LaminationLine"].start_point = dockingPointM
            elif lElem["p2"].coordinate == testP.coordinate:
                lElem["LaminationLine"].end_point = dockingPointM

        curveOfRotorSheet1 = RotorSheet1.geo_list[0].curve
        curveOfRotorSheet1.append(Magnet1.innerLinePart[0])
        RotorSheet1.geo_list[0].curve = curveOfRotorSheet1

    ###Mit addAirSpace() wird der Luftraum auf der Rotorseite bis zum Movingband erzeugt und Materialeigenschaften definiert.
    def _addAirSpace(self):
        airGapLength = self._airGapDict["width"] / 4
        PCentre = self.laminationDict["machineCentrePoint"].duplicate()
        alpha = self.angleGeoParts
        pMagAir: Point = self._physicalElements[1].airDockingPoint[0]
        pAir1: Point = pMagAir.duplicate()  # mmagnet center point on airgap side
        for line in self._physicalElements[1].airLinePart:
            line: Line | CircleArc | Spline
            if pMagAir in line.points:  # only set mesh on line near airgap
                line.setMeshLength(
                    airGapLength
                )  # set mesh of magnet-air interface points mesh is homogeneous
        pAir1.translate(
            airGapLength * math.cos(alpha), airGapLength * math.sin(alpha), 0
        )
        pAir2 = pAir1.duplicate()  # p2 is airspace point on segemnt center near airgap
        pAir2.rotateZ(PCentre, alpha)

        # createLine
        lAir1 = CircleArc("lAir1", pAir1, PCentre, pAir2)
        lAir2 = Line("lAir2", pAir1, self._physicalElements[1].airDockingPoint[0])
        lAir3 = Line("lAir3", pAir2, self._physicalElements[0].airDockingPoint2[0])
        sAir1 = Surface(
            "sAir1",
            [lAir1, lAir2, lAir3]
            + self._physicalElements[0].outerLinePart
            + self._physicalElements[1].airLinePart,
        )
        # sAir1.setMeshLength(airGapLength)
        airPart = AirArea("airRotor", [sAir1], self._airGapDict["material"])
        self._physicalElements.append(airPart)

        pAir3 = pAir1.duplicate()
        pAir3.translate(
            airGapLength * math.cos(alpha), airGapLength * math.sin(alpha), 0
        )
        pAir4 = pAir3.duplicate()
        pAir4.rotateZ(PCentre, alpha)
        lAir4 = CircleArc("lAir4", pAir3, PCentre, pAir4)
        lAir5 = Line("lAir5", pAir1, pAir3)
        lAir6 = Line("lAir6", pAir2, pAir4)
        sAirGap1 = Surface("sAir2", [lAir1, lAir4, lAir5, lAir6])
        sAirGap1.setMeshLength(
            airGapLength
        )  # set mesh length of airgap surface to heigth of segment. Thats good practice for calculating the maxwell stress tensor torque
        airGapPart = AirGap("airGapRotor", [sAirGap1], self._airGapDict["material"])
        self._physicalElements.append(airGapPart)
        return None

    ###createDuplicate() vervollständig die Geometrie zum gewünschten Teil- bzw. Vollmodell.
    def _createDuplicate(self):
        # duplicate Rotorsheet (to get one rotor segment)
        rotorLam: RotorLamination | RotorLamination_Sheet01_Standard = (
            self._physicalElements[0]
        )
        rotorLamSurfList = rotorLam.geo_list
        PCentre = self.laminationDict["machineCentrePoint"].duplicate()
        pH1 = rotorLam.betweenLinePart[
            0
        ].start_point  # betweenLinePart not defined in parent-class RotorLamination
        hilfsLinie1 = Line("L_hilf1", PCentre, pH1)
        ez = Point("p_Z", PCentre._x, PCentre._y, PCentre._z + 1, 1)
        hilfsLinie2 = Line("L_hilf2", PCentre, ez)
        surfaceRotor2 = rotorLamSurfList[0].mirror(
            PCentre, hilfsLinie1, hilfsLinie2
        )  # mirror half segment to get full rotor lamination segemnt
        rotorLamSurfList.append(surfaceRotor2)
        alpha = self.angleGeoParts * 2
        dupRotorLamSurfList = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            for rotLamSurf in rotorLamSurfList:
                sNew = rotLamSurf.duplicate()
                sNew.rotateZ(self.laminationDict["machineCentrePoint"], i * alpha)
                dupRotorLamSurfList.append(sNew)
        rotorLam.geo_list = (
            rotorLamSurfList + dupRotorLamSurfList
        )  # add the new duplicated rotor surfaces to the physicalElement

        # duplicate Magnet
        magnet: Magnet = self._physicalElements[1]
        magSurfList = magnet.geo_list
        surfaceMag2 = magSurfList[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        magSurfList.append(surfaceMag2)
        dupMagnetList: list[Magnet] = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            dupMagSurfList: list[Surface] = []  # clear previous magnet surf list
            for magSurf in magSurfList:
                sNew2 = magSurf.duplicate()
                sNew2.rotateZ(self.laminationDict["machineCentrePoint"], i * alpha)
                dupMagSurfList.append(sNew2)
            dupMag = Magnet(
                name="magnet_SPMSM",
                geoElements=dupMagSurfList.copy(),
                material=self.magnetDict["material"],
                magDirection=self.magnetDict["magnetisationDirection"][i],
                magType=self.magnetDict["magnetisationType"],
                magVectorAngle=0.0,
            )
            dupMag.name = "magnet_SPMSM_" + str(dupMag.id)
            dupMagnetList.append(dupMag)

        # OLD VERSION
        # wholeMagnet = [self._physicalElements[1]] + allMag
        # self._physicalElements = self._physicalElements + wholeMagnet
        # NEW:
        self._physicalElements += dupMagnetList

        # duplicate AirSpace
        airPhys: AirArea = self._physicalElements[2]
        airSurfList = airPhys.geo_list
        dupAirSurf = airSurfList[0].mirror(
            PCentre, hilfsLinie1, hilfsLinie2
        )  # mirror for full segment
        airSurfList.append(dupAirSurf)
        dupAirSegmentSurfList = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            # for number of segemnts duplicate and rotate the air surfaces to get all geo-elements
            for airSurf in airSurfList:
                sNew = airSurf.duplicate()
                sNew.rotateZ(self.laminationDict["machineCentrePoint"], i * alpha)
                dupAirSegmentSurfList.append(sNew)
        airPhys.geo_list = airSurfList + dupAirSegmentSurfList
        # self._physicalElements.append(
        #     AirArea(
        #         name="rotorAir",
        #         geo_list=dupAirSegmentSurfList.copy(),
        #         material=self._airGapDict["material"],
        #     )
        # )
        # dupAirSegmentSurfList.clear()

        # duplicate AirGap
        airgapPhys: AirGap = self._physicalElements[3]
        airgapSurfList = airgapPhys.geo_list
        surfaceAirGap2 = airgapSurfList[0].mirror(PCentre, hilfsLinie1, hilfsLinie2)
        airgapSurfList.append(surfaceAirGap2)
        dupAirgapSurfList = []
        for i in range(1, int(self.nbrGeoParts / 2)):
            for airgapSurf in airgapSurfList:
                sNew = airgapSurf.duplicate()
                sNew.rotateZ(self.laminationDict["machineCentrePoint"], i * alpha)
                dupAirgapSurfList.append(sNew)
        airgapPhys.geo_list = airgapSurfList + dupAirgapSurfList

    ###Mit createConstraintLine werden alle Grenzlinien, Movingbands, primary- und Slavelinien definiert.
    def _createConstraintLine(self):
        angle = self.angleGeoParts
        centerPoint: Point = self.laminationDict["machineCentrePoint"]
        pLimitInner1 = Point(
            "pLimitInner1",
            self.laminationDict["r_We"] + centerPoint.coordinate[0],
            centerPoint.coordinate[1],
            centerPoint.coordinate[2],
            1,
        )
        pLimitInner2 = pLimitInner1.duplicate()
        pLimitInner2.rotateZ(self.laminationDict["machineCentrePoint"], angle)
        curveInner = [
            CircleArc(
                "curveInner",
                pLimitInner1,
                self.laminationDict["machineCentrePoint"],
                pLimitInner2,
            )
        ]
        for i in range(1, self.nbrGeoParts):
            c1 = curveInner[0].duplicate()
            c1.rotateZ(self.laminationDict["machineCentrePoint"], i * angle)
            curveInner.append(c1)

        # create moving band lines
        airgap_surf1: Surface = self._physicalElements[3].geo_list[0]
        mb_line_list: list[CircleArc] = []
        mbNegDirection = airgap_surf1.curve[1].duplicate()
        mbNegDirection.rotateZ(self.laminationDict["machineCentrePoint"], -angle)
        mb_line_list.append(mbNegDirection)

        for i in range(1, self.nbrGeoParts):
            c1 = curveInner[0].duplicate()
            c1.rotateZ(self.laminationDict["machineCentrePoint"], i * angle)
            curveInner.append(c1)
        for i in range(1, self.nbrGeoParts):
            c2 = mb_line_list[0].duplicate()
            c2.rotateZ(self.laminationDict["machineCentrePoint"], i * angle)
            mb_line_list.append(c2)

        mbRotorLine = MovingBand(
            "movingBand_RotorLine",
            mb_line_list,
            self._airGapDict["material"],
            False,
        )
        self._physicalElements.append(mbRotorLine)

        allMBAux = []
        for i in range(1, int(self.symmetryFactor)):
            mbRotor_aux = []
            for l_mb in mb_line_list:
                l_mb_aux = l_mb.duplicate()
                l_mb_aux.rotateZ(
                    self.laminationDict["machineCentrePoint"],
                    i * self.nbrGeoParts * angle,
                )
                mbRotor_aux.append(l_mb_aux)
            mbAux = MovingBand("", mbRotor_aux, self._airGapDict["material"], True)
            mbAux.name = "mb_Aux_" + str(mbAux.id)
            allMBAux.append(mbAux)
        self._physicalElements = self._physicalElements + allMBAux

        innerLimitLine = LimitLine("innerLimitLine_Rotor", curveInner)
        self._physicalElements.append(innerLimitLine)

        pprimary1 = Point("pprimary1", self.laminationDict["r_We"], 0, 0, 1)
        pprimary2 = Point("pprimary2", self.laminationDict["r_R"], 0, 0, 1)
        lLamprimary = Line("lLamprimary", pprimary1, pprimary2)

        lAir = self._physicalElements[2].geo_list[0].curve[2].duplicate()
        lAir.rotateZ(self.laminationDict["machineCentrePoint"], -angle * 2)
        lAirGap = self._physicalElements[3].geo_list[0].curve[2].duplicate()
        lAirGap.rotateZ(self.laminationDict["machineCentrePoint"], -angle)

        primaryLine1 = PrimaryLine("primary_RotorLine", [lLamprimary, lAir, lAirGap])
        self._physicalElements.append(primaryLine1)

        allslaveLine = primaryLine1.geo_list
        slaveLineArray = []
        for l in allslaveLine:
            l1 = l.duplicate()
            l1.rotateZ(
                self.laminationDict["machineCentrePoint"],
                self.nbrGeoParts * angle,
            )
            slaveLineArray.append(l1)
        slaveLine1 = SlaveLine("slave_RotorLine", slaveLineArray)
        self._physicalElements.append(slaveLine1)

    ###createDomainForRotor gruppiert alle PhysicalElements für die Simulation.
    def _createDomainForRotor(self):
        allPhy = self.sortPhysicals()

        ###DomainC beinhaltet alle Physical Elements, die leitend sind.
        self._domainC = Domain("DomainC_Rotor", allPhy["domainC"])
        self._domainCC = Domain("DomainCC_Rotor", allPhy["domainCC"])

        ###DomainAirGap beinhaltet alle Physical Elements, die einen Luftspalt auf der Rotorseite (Luftspalt bis zum Moving Band) beschreiben.
        self._domainAirGap = Domain("Domain_Rotor_Airgap", allPhy["airGap"])

        ###DomainM beinhaltet alle Physical Elements, die magnetisiert sind.
        self._domainM = Domain("DomainM_Rotor", allPhy["domainM"])

        ###mb beinhaltet alle Physical Elements, die eine Moving Band auf der Rotorseite beschreiben.
        self._mb = Domain("Domain_MB_Rotor", allPhy["mb_all"])

        ###mbBaux beinhaltet alle Hilfslinien des MovingBands (Ergänzung zum Vollkreis), die wegen der Symmetrie ergänzt werden mussten. MovingBand auf der Rotorseite muss ein vollständiger Kreis beschreiben.
        self._mbBaux = Domain("Domain_Rotor_Bnd_MBaux", allPhy["mb_Mbaux"])

        ###DomainS beinhaltet alle Physical Elements, die bestromt werden.
        self._domainS = Domain("DomainS_Rotor", allPhy["domainS"])

        ###domain beinhaltet alle Physical Elements, die den gesamten Rotor beschreiben.
        self._domain = Domain("Domain_Rotor", allPhy["domain"])

        ###domainL beinhaltet alle Physical Elements, die ein lineares Material besitzen.
        self._domainL = Domain("DomainL_Rotor", allPhy["domainL"])
        ###domainNL beinhaltet alle Physical Elements, die ein nicht lineares Material besitzen.
        self._domainNL = Domain("DomainNL_Rotor", allPhy["domainNL"])

        ###rotorMoving beinhaltet alle Physical Elements, die während der Simulation rotiert werden müssen.
        self._rotorMoving = Domain("DomainRotor_Moving", allPhy["rotor_moving"])

        ###primarykante vom Rotor.
        self._domainPrimary = Domain("Domain_PrimaryRegion_Rotor", allPhy["primary"])

        ###Slavekante vom Rotor.
        self._domainSlave = Domain("Domain_SlaveRegion_Rotor", allPhy["slave"])

        ###Innengrenze der elektrischen Maschine (Welle).
        self._domainInnerLimit = Domain("Domain_InnerLimit_Rotor", allPhy["limit"])

    # ###sortPhysicals ist eine Sortierfunktion, die die PhysicalElements den passenden Domainen zuweist.
    # def sortPhysicals(self):
    #     phy_domainS = []  # Eingeprägte Ströme
    #     phy_domainM = []  # Magnete
    #     mb_all = []  # Moving Band

    #     phy_domain = []  # Alle Flächen
    #     phy_domainNL = []  # Alle nicht linearen Flächen
    #     phy_domainL = []  # Alle linearen Flächen

    #     phy_rotor_Moving = []  # Alle Teile die sich drehen, inkl. Moving Band (alle)
    #     mb_Mbaux = []  # Bei Teilmodell -> die restlichen Moving Band
    #     phy_airgap = []  # Luftspalt im Rotor

    #     phy_primaryLine = []  # Teilmodell primarykante
    #     phy_slaveLine = []  # Teilmodell Slavekante
    #     limit_Line = []
    #     for s in self._physicalElement:

    #         # domainS und domainC zuweisen
    #         try:
    #             s.isSlot()
    #             if s.getImposedCurrent():
    #                 phy_domainS.append(s)
    #             if s.getConducting():
    #                 phy_domainC.append(s)
    #         except AttributeError:
    #             pass

    #         # domainM zuweisen
    #         try:
    #             s.isMagnet()
    #             phy_domainM.append(s)
    #         except AttributeError:
    #             pass

    #         # MB und rotor_bnd_Mbaux zuweisen
    #         try:
    #             s.isMovingBand()
    #             mb_all.append(s)

    #             if s.isAuxiliary():
    #                 mb_Mbaux.append(s)

    #             phy_rotor_Moving.append(s)
    #         except AttributeError:
    #             pass

    #         geoElem = s.geo_list
    #         if geoElem[0].getType() == "Surface":
    #             phy_domain.append(s)
    #             mat = s.getMaterial()
    #             if mat != None and mat.linear == True:
    #                 phy_domainL.append(s)
    #             elif mat != None and mat.linear == False:
    #                 phy_domainNL.append(s)
    #             phy_rotor_Moving.append(s)

    #         try:
    #             s.isAirGap()
    #             phy_airgap.append(s)
    #         except AttributeError:
    #             pass

    #         try:
    #             s.isprimaryLine()
    #             phy_primaryLine.append(s)
    #         except AttributeError:
    #             pass

    #         try:
    #             s.isSlaveLine()
    #             phy_slaveLine.append(s)
    #         except AttributeError:
    #             pass

    #         try:
    #             s.isLimitLine()
    #             limit_Line.append(s)
    #         except AttributeError:
    #             pass

    #     sortedPhy = {
    #         "domainS": phy_domainS,
    #         "domainM": phy_domainM,
    #         "mb_all": mb_all,
    #         "domain": phy_domain,
    #         "domainNL": phy_domainNL,
    #         "domainL": phy_domainL,
    #         "rotor_moving": phy_rotor_Moving,
    #         "mb_Mbaux": mb_Mbaux,
    #         "airGap": phy_airgap,
    #         "primary": phy_primaryLine,
    #         "slave": phy_slaveLine,
    #         "limit": limit_Line,
    #     }

    #     return sortedPhy

    ###
    # Mit addToScript wird der Rotor zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    ###
    def addToScript(self, script):
        if len(self._physicalElements) > 0:
            self._createDomainForRotor()
        self._domainS.addToScript(script)
        self._domainM.addToScript(script)
        self._mb.addToScript(script)
        self._domain.addToScript(script)
        self._domainL.addToScript(script)
        self._domainNL.addToScript(script)
        self._rotorMoving.addToScript(script)
        self._mbBaux.addToScript(script)
        self._domainAirGap.addToScript(script)
        self._domainPrimary.addToScript(script)
        self._domainSlave.addToScript(script)
        self._domainInnerLimit.addToScript(script)

    ###Mit getAllMagnet werden alle Magnetelemente als Output dem Nutzer zur Verfügung gestellt.
    def getAllMagnet(self) -> list[Magnet]:
        allMag = []
        for phy in self.physicalElements:
            try:
                if isinstance(phy, Magnet):
                    allMag.append(phy)
            except AttributeError:
                pass
        return allMag
