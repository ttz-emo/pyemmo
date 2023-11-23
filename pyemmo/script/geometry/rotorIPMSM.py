from typing import List

from pyemmo.script.geometry.physicalElement import PhysicalElement
from .domain import Domain
from .rotor import Rotor
from .rotorLamination import RotorLamination
from .magnet import Magnet
from .line import Line
from .circleArc import CircleArc
from .point import Point
from .surface import Surface
from .airArea import AirArea
from .airGap import AirGap
from .movingBand import MovingBand
from .limitLine import LimitLine
from .primaryLine import PrimaryLine
from .slaveLine import SlaveLine
import math


class RotorIPMSM(Rotor):
    def __init__(
        self,
        laminationType,
        magnetType,
        angleGeoParts,
        nbrGeoParts: int,
        symmetryFactor,
        axLen: float = 1.0,
        startPosition=0,
        laminationDict=None,
        magnetDict=None,
        airGapDict=None,
    ):
        super().__init__(physicalElementList=[], name="RotorIPMSM", axLen=axLen)
        self._laminationType = laminationType
        self._magnetType = magnetType

        self._angleGeoParts = angleGeoParts
        self._startPosition = startPosition
        if float(nbrGeoParts).is_integer():
            self._nbrGeoParts = int(nbrGeoParts)
        else:
            raise ValueError(f"The number of segments is not an integer: {nbrGeoParts}")
        if float(symmetryFactor).is_integer():
            self._symmetryFactor = int(symmetryFactor)
        else:
            raise ValueError(f"The symmetry factor is not an integer: {symmetryFactor}")
        # Wenn laminationDict nicht None: Setzte Lamination Parameter
        if laminationDict:
            self.addLaminationParameter(laminationDict)

        # Wenn magnetDict nicht None: Setzte Magnet Parameter
        if magnetDict:
            self.addMagnetParameter(magnetDict)

        if airGapDict:
            self.addAirGapParameter(airGapDict)

    def addLaminationParameter(self, laminationDict):
        self._laminationDict = laminationDict
        self._laminationDict["angleGeoParts"] = self._angleGeoParts
        self._laminationDict["startPosition"] = self._startPosition

    def addMagnetParameter(self, magnetDict):
        self._magnetDict = magnetDict
        self._magnetDict["startPosition"] = self._startPosition
        if self._laminationDict != None:
            self._magnetDict["rA_Rotor"] = self._laminationDict["r_R"]
            self._magnetDict["machineCentrePoint"] = self._laminationDict[
                "machineCentrePoint"
            ]
        else:
            print("No definition of lamination. Use addLaminationParameter() first!")

    def addAirGapParameter(self, airGapDict):
        self._airGapDict = airGapDict
        if self._laminationDict == None:
            print("No defination of rotorpart. Use addLaminationParameter() first!")

    def createRotor(self):
        if self._laminationDict == None or self._magnetDict == None:
            print(
                "No definition of lamination or magnet found. Use addLaminationParameter() or addMagnetParameter to define your machine parts!"
            )
        else:
            if self._laminationType == "sheet01_standard":
                from .rotorLamination_Sheet01_Standard import (
                    RotorLamination_Sheet01_Standard,
                )

                laminationPart = RotorLamination_Sheet01_Standard(self._laminationDict)

            if self._magnetType == "magnet_Slot01":
                from .magnet_Slot01 import MagnetSlot01

                magnetPart = MagnetSlot01(
                    self._magnetDict,  # comment Max: In _init_ definition von Magnet-Klasse heißt das Argument "machineDict"... (Wahrscheinlich nur ungenauer Variablenname)
                    self._magnetDict["magnetisationDirection"][0],
                    self._magnetDict["magnetisationType"],
                )
            self._physicalRaw = [laminationPart, magnetPart]

        self._dockMagnetToSheet()
        self._addAirSpace()
        self._createDuplicate()
        self._createConstraintLine()
        self._createDomainForRotor()  # create rotor domains

        mag: Magnet = self._physicalRaw[1]
        if mag.magType in ("parallel", "tangential"):
            allAngle = self._calculateAngleForParallelMagnet()
            allMag = self.getAllMagnet()
            for i, mag in enumerate(allMag):
                mag.magAngle = allAngle[i]

    def _calculateAngleForParallelMagnet(self):
        Magnet1 = self._physicalRaw[1]
        dockingPointM = Magnet1.laminationDockingPoint[0].duplicate()
        coordDPM = dockingPointM.coordinate
        angleParallel1 = math.atan2(coordDPM[1], coordDPM[0])
        allAngleParallel = [angleParallel1]
        alpha = self._angleGeoParts * 2
        for i in range(1, int(self._nbrGeoParts / 2)):
            dockingPointM.rotateZ(self._laminationDict["machineCentrePoint"], alpha)
            coordDPM = dockingPointM.coordinate
            angle = math.atan2(coordDPM[1], coordDPM[0])
            allAngleParallel.append(angle)
        return allAngleParallel

    def _dockMagnetToSheet(self):
        """
        _dockMagnetToSheet(self)

        Diese Methode verändert die Linien der Rotorblech-Kontur, sodass diese nicht die Magnetlinien schneiden
        und zwei getrennte Regionen entstehen können.
        """
        # Get physicals and extract all lines
        Rotorsheet = self._physicalRaw[0]
        Magnet1 = self._physicalRaw[1]

        # alle Magnetlinien extrahieren die das Blechpaket schneiden
        MagLList = Magnet1.lamLinePart

        # alle Magnetlinien extrahieren die auf der Symmetrieachse liegen
        MagCenterLList = Magnet1.innerLinePart
        if not MagCenterLList:
            # MagCenterLList ist leer
            # Magnet liegt nicht auf der zentralen Achse (-> zwei getrennte Magnete vorhanden)
            # TBD!
            Warning(
                "Nicht auf der Symmetrieachse liegende Magnete sind noch nicht implementiert!"
            )
        else:
            # Magnet liegt auf der x-Achse -> Magnetform aus Blechpaket ausschneiden
            # Vorgehen: Duplizieren der Symmetrielinie (BetweenLinePart) des Blechs
            #           und aufteilen in zwei neue Linen mit Anfangs und Endpunkt von Magnet..
            #           Anschließend übrige Magnetlinien zur Blechkontur hinzfügen

            OldLamCenterL = Rotorsheet.betweenLinePart[0]
            LamCenterL_bottom = OldLamCenterL.duplicate(
                OldLamCenterL.name + "_1"
            )  # untere Linie muss dupliziert werden wegen Reihenfolge der Linien in der LineList der Fläche
            LamCenterL_top = OldLamCenterL
            LamCenterL_top.endPoint = MagCenterLList[
                0
            ].startPoint  # P1 in  MagCenterL ist immer Punkt nahe Rotoroberfläche!!!
            # P2 in LamCenterL ist immer Punkt nach der Welle

            LamCenterL_bottom.startPoint = MagCenterLList[
                0
            ].endPoint  # P2 in MagCenterL ist immer Punkt nahe Welle!
            # P1 in LamCenterL ist immer Punkt nach der Rotoroberfläche

            ## Neue Linien und Magnetlinien zu RotorlinienListe hinzufügen:
            # alle Rotorlinien kopieren (ID behalten!):
            LamLList = Rotorsheet.geometricalElement[0].curve

            # Rotoroberflächen-nahe Linie ist bereits in LamLList enthalten
            # Magnetlinien hinzufügen
            for line in MagLList:
                LamLList.append(line)
            # Wellennahelinie hinzufügen
            LamLList.append(LamCenterL_bottom)

    def _addAirSpace(self):
        """
        _addAirSpace(self)

        Diese Methode erzeugt die rotorseitigegn, geometrischen Bereiche im Luftspalt (ohne Magnete)
        """
        airGapLength = (
            self._airGapDict["width"] / 3
        )  # comment Max: von 4 -> 3 geändert, weil keine Unterteilung des Luftspalts nötig
        PCentre = self._laminationDict["machineCentrePoint"].duplicate()
        alpha = self._angleGeoParts
        laminationPart = self._physicalRaw[0]
        P1: Point = laminationPart.airDockingPoint1[0].duplicate()
        P2: Point = laminationPart.airDockingPoint2[0].duplicate()
        P3 = P1.duplicate()
        P3.translate(
            math.cos(alpha) * airGapLength, math.sin(alpha) * airGapLength, 0
        )  # ACHTUNG: Rotorsegment ist bereits einmal um alpha gedreht
        P4 = P3.duplicate()
        P4.rotateZ(PCentre, alpha)

        # create airgap lines
        l_rechts = Line("lAir1", P1, P3)
        l_aussen = CircleArc("lAir2", P3, PCentre, P4)
        l_links = Line("lAir3", P4, P2)
        l_innen = CircleArc("lAir4", P2, PCentre, P1)

        # create airgap surface
        s_AirGap = Surface("sAir", [l_rechts, l_aussen, l_links, l_innen])
        s_AirGap.setMeshLength(airGapLength)
        RotorAirgap = AirGap("airGapRotor", [s_AirGap], self._airGapDict["material"])
        self._physicalRaw.append(RotorAirgap)

    def _createDuplicate(self):
        """
        _createDuplicate(self)

        Diese Funktion spiegelt die bereits gedrehten Halbsegmente zu Vollsegmenten und
        dupliziert diese anschließend entsprechend der angegebenen
        Symmetrie (_nbrGeoParts)
        """
        ## duplicate Rotorsheet ##
        allGeo = self._physicalRaw[0].geometricalElement
        PCentre = self._laminationDict["machineCentrePoint"].duplicate()
        pH1 = self._physicalRaw[0].betweenLinePart[0].startPoint.duplicate()
        hilfsLinie1 = Line("L_hilf1", PCentre, pH1)
        ez = Point("p_Z", PCentre._x, PCentre._y, PCentre._z + 1, 1)
        hilfsLinie2 = Line("L_hilf2", PCentre, ez)
        surfaceRotor2 = allGeo[0].mirror(
            PCentre, hilfsLinie1, hilfsLinie2, name=allGeo[0].name + "_mirror"
        )
        allGeo.append(surfaceRotor2)
        alpha = self._angleGeoParts * 2
        listGeo = []
        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in allGeo:
                sNew = s.duplicate(name=s.name + "_duplicate_" + str(i))
                sNew.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                listGeo.append(sNew)

        wholeLamination = RotorLamination(
            "laminationIPMSM_Rotor", allGeo + listGeo, self._laminationDict["material"]
        )
        self._physicalElements.append(wholeLamination)

        ## duplicate Magnet ##
        # Mirror magnet surface to get full magnet (segment)
        allGeo2 = self._physicalRaw[1].geometricalElement
        surfaceMag2 = allGeo2[0].mirror(
            PCentre, hilfsLinie1, hilfsLinie2, name=allGeo[0].name + "_mirror"
        )
        allGeo2.append(surfaceMag2)
        allMag = []
        for i in range(1, int(self._nbrGeoParts / 2)):
            magSur = []
            for s in allGeo2:
                sNew2 = s.duplicate(name=s.name + "_duplicate_" + str(i))
                sNew2.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                magSur.append(sNew2)
            mag2 = Magnet(
                "magnet_SPMSM",
                magSur,
                self._magnetDict["material"],
                self._magnetDict["magnetisationDirection"][i],
                self._magnetDict["magnetisationType"],
                0.0,
            )
            mag2.name = self._magnetType + "_" + str(mag2.id)
            allMag.append(mag2)

        wholeMagnet = [self._physicalRaw[1]] + allMag
        self._physicalElements = self._physicalElements + wholeMagnet

        ## duplicate AirGap ##
        # find Airgap Element in _physicalRaw
        for physical in self._physicalRaw:
            if type(physical) is AirGap:
                AirGapGeo = physical.geometricalElement.copy()
                break  # break for loop if airgap is found
        if AirGapGeo is None:
            raise ValueError("No physical element of type AirGap found")
        # Mirror the Airgap surface and add to AirGapGeo to get one full Airgap segment
        surfaceAirGap = AirGapGeo[0].mirror(
            PCentre, hilfsLinie1, hilfsLinie2, name=allGeo[0].name + "_mirror"
        )
        AirGapGeo.append(surfaceAirGap)

        # Duplicate full Airgap segment
        AirgapGeoList = AirGapGeo.copy()  # Initial
        for i in range(1, int(self._nbrGeoParts / 2)):
            for s in AirGapGeo:
                sNew = s.duplicate(name=s.name + "_duplicate_" + str(i))
                sNew.rotateZ(self._laminationDict["machineCentrePoint"], i * alpha)
                AirgapGeoList.append(sNew)

        wholeAirGap = AirGap("rotorAirGap", AirgapGeoList, self._airGapDict["material"])
        self._physicalElements.append(wholeAirGap)

    def _createConstraintLine(self):
        angle = self._angleGeoParts

        ## Define inner radial limit (at shaft radius) ##
        # create limit points
        pLimitInner1 = Point(
            "pLimitInner1",
            self._laminationDict["r_We"]
            + self._laminationDict["machineCentrePoint"]._x,
            self._laminationDict["machineCentrePoint"]._y,
            self._laminationDict["machineCentrePoint"]._z,
            1,
        )
        pLimitInner2 = pLimitInner1.duplicate(name="pLimitInner2")
        pLimitInner2.rotateZ(self._laminationDict["machineCentrePoint"], angle)
        # create limit curve (shaft)
        curveInner = [
            CircleArc(
                "curveInner",
                pLimitInner1,
                self._laminationDict["machineCentrePoint"],
                pLimitInner2,
            )
        ]
        # duplicate limit curve
        for i in range(1, self._nbrGeoParts):
            c1 = curveInner[0].duplicate(
                name=curveInner[0].name + "_duplicate_" + str(i)
            )
            c1.rotateZ(self._laminationDict["machineCentrePoint"], i * angle)
            curveInner.append(c1)
        # Create Limitline and add to physicalElement
        innerLimitLine = LimitLine("innerLimitLine_Rotor", curveInner)
        self._physicalElements.append(innerLimitLine)

        ## Movingband Rotor ##
        mbRotor1 = []
        mbNegDirection = (
            self._physicalRaw[2]
            .geometricalElement[0]
            .curve[1]
            .duplicate(name="lAirGap")
        )  # duplicate the outer airgap line (movingband line)
        mbNegDirection.rotateZ(
            self._laminationDict["machineCentrePoint"], -angle
        )  # Rückdrehung wegen Startposition

        # mbRotor1.append(mbNegDirection)
        # mbRotor1.append(self._physicalRaw[2].geometricalElement[0].getCurve()[1])

        # Rotate and Duplicate
        for i in range(0, self._nbrGeoParts):
            c2 = mbNegDirection.duplicate(mbNegDirection.name + "_duplicate_" + str(i))
            c2.rotateZ(self._laminationDict["machineCentrePoint"], i * angle)
            mbRotor1.append(c2)

        # Create MovingBand and add to physicalElement
        mbRotorLine = MovingBand(
            "movingBand_RotorLine", mbRotor1, self._airGapDict["material"], False
        )
        self._physicalElements.append(mbRotorLine)

        ## Movingband Aux ##
        allMBAux = []
        for i in range(1, self._symmetryFactor):
            mbRotor_aux = []
            for l_mb in mbRotor1:
                l_mb_aux = l_mb.duplicate()
                l_mb_aux.rotateZ(
                    self._laminationDict["machineCentrePoint"],
                    i * self._nbrGeoParts * angle,
                )
                mbRotor_aux.append(l_mb_aux)
            # create MovinBand and add to allMBAux
            mbAux = MovingBand(
                name="",
                geometricalElement=mbRotor_aux,
                material=self._airGapDict["material"],
                auxiliary=True,
            )
            mbAux.name = "mb_Aux_" + str(mbAux.id)
            allMBAux.append(mbAux)
        # append Movingband Aux Rotor to physicalElement
        for movingband in allMBAux:
            self._physicalElements.append(movingband)

        ## primaryline ##
        pprimary1 = Point("pprimary1", self._laminationDict["r_We"], 0, 0, 1)
        pprimary2 = Point("pprimary2", self._laminationDict["r_R"], 0, 0, 1)
        lLamprimary = Line("lLamprimary", pprimary1, pprimary2)

        lAirGapprimary = (
            self._physicalRaw[2]
            .geometricalElement[0]
            .curve[0]
            .duplicate(name="lAirgapprimary")  # duplicate part of airgap on x-axis
        )
        lAirGapprimary.rotateZ(
            self._laminationDict["machineCentrePoint"], -angle
        )  # Rückrotation damit Linie auf x-Achse liegt

        # create primaryLine and append to physicalElement
        primaryLine1 = PrimaryLine("primary_RotorLine", [lLamprimary, lAirGapprimary])
        self._physicalElements.append(primaryLine1)

        ## Slavelines ##
        SlaveLineList = []
        for l in primaryLine1.geometricalElement:
            l1 = l.duplicate()  # duplicate primarylines
            l1.rotateZ(
                self._laminationDict["machineCentrePoint"], self._nbrGeoParts * angle
            )  # Rotate copied Lines
            SlaveLineList.append(l1)  # append to SlavelineList
        SlaveLineList[0].name = "lLamSlave"
        SlaveLineList[1].name = "lAirgapSlave"
        # Create Slaveline and append to physicalElement
        slaveLine1 = SlaveLine("slave_RotorLine", SlaveLineList)
        self._physicalElements.append(slaveLine1)

    def _createDomainForRotor(self):
        allPhy = self.sortPhysicals()
        self._domainS = Domain("DomainS_Rotor", allPhy["domainS"])
        self._domainM = Domain("DomainM_Rotor", allPhy["domainM"])
        self._domainC = Domain("DomainC_Rotor", allPhy["domainC"])
        self._mb = Domain("Domain_MB_Rotor", allPhy["mb_all"])
        self._domain = Domain("Domain_Rotor", allPhy["domain"])
        self._domainL = Domain("DomainL_Rotor", allPhy["domainL"])
        self._domainNL = Domain("DomainNL_Rotor", allPhy["domainNL"])

        self._rotorMoving = Domain("DomainRotor_Moving", allPhy["rotor_moving"])
        self._mbBaux = Domain("Domain_Rotor_Bnd_MBaux", allPhy["mb_Mbaux"])
        self._domainAirGap = Domain("Domain_Rotor_Airgap", allPhy["airGap"])

        self._domainPrimary = Domain("Domain_PrimaryRegion_Rotor", allPhy["primary"])
        self._domainSlave = Domain("Domain_SlaveRegion_Rotor", allPhy["slave"])
        self._domainInnerLimit = Domain("Domain_InnerLimit_Rotor", allPhy["limit"])

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

    #         geoElem = s.geometricalElement
    #         if geoElem[0].getType() == "Surface":
    #             phy_domain.append(s)
    #             mat = s.getMaterial()
    #             if mat != None and mat.isLinear() == True:
    #                 phy_domainL.append(s)
    #             elif mat != None and mat.isLinear() == False:
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

    def getAllMagnet(self) -> List[Magnet]:
        MagList: List[Magnet] = list()
        for physElem in self._physicalElements:
            if physElem.type == "Magnet":
                MagList.append(physElem)
        return MagList
