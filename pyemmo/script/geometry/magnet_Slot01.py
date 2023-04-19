from .magnet import Magnet
from .physicalElement import PhysicalElement
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface
from .. import colorDict
import math


class Magnet_Slot01(Magnet):
    def __init__(self, machineDict, magnetisationDirection, magnetisationType):
        ###Dictionary mit allen Magnet-Parametern.
        self._machineDict = machineDict

        self.id = self._getNewID()
        magName = "Magnet_Slot01_" + str(self.id)
        super().__init__(
            magName,
            [],
            machineDict["material"],
            magnetisationDirection,
            magnetisationType,
        )
        self._createGeometry()

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
        coordCentre = PCentre.getCoordinate()

        r_M_bottom = rA_Rotor - d_Slot - h_M

        # Konstuktion der Punkte an der x-Achse:
        pMagnet1 = Point(
            "pMagnet1",
            coordCentre[0] + r_M_bottom,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
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
        self._geometricalElement = [surfaceMagnet]
        self._innerLinePart = [lMagnet4]
        self._airLinePart = []
        self._lamLinePart = [lMagnet1, lMagnet2, lMagnet3]
        self._laminationDockingPoint = [pMagnet1, pMagnet2, pMagnet3, pMagnet4]

        for s in self._geometricalElement:
            if self.getMagnetisationDirection() == 1:
                s.setMeshColor(colorDict["Red"])
            elif self.getMagnetisationDirection() == -1:
                s.setMeshColor(colorDict["Green"])

    def getInnerLinePart(self):
        return self._innerLinePart

    # def getAirDockingPoint(self):
    #     return self._airDockingPoint

    def getAirLinePart(self):
        return self._airLinePart

    def getLamLinePart(self):
        return self._lamLinePart

    def getLaminationDockingPoint(self):
        return self._laminationDockingPoint

    def getGeometricalElement(self):
        return self._geometricalElement
