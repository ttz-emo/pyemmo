from .slot import Slot
from .physicalElement import PhysicalElement
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface
import math


class Slot_Form02(Slot):
    def __init__(self, machineDict):
        self._machineDict = machineDict
        ###ID für die Physical Surface.
        Slot.__init__(
            self,
            name="Slot_Form02",
            geometricalElement=list(),
            material=machineDict["material"],
        )
        self._name = "Slot_Form02_" + str(self.id)
        self._createGeometry()

    def _createGeometry(self):

        dockingLength = self._machineDict["rI_Stator"]
        angle_slotOP = math.atan2(self._machineDict["w_SlotOP"], dockingLength)

        PCentre = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.getCoordinate()
        angleStart = self._machineDict["startPosition"]

        # Konstuktion der Punkte an der x-Achse
        pS1 = Point(
            "pSlot1",
            coordCentre[0] + dockingLength,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
        )
        pS2 = pS1.duplicate()
        pS2.rotateZ(PCentre, angle_slotOP)
        pS3 = pS1.duplicate()
        pS3.translate(self._machineDict["h_SlotOP"], 0, 0)
        pS4 = pS3.duplicate()
        pS4.rotateZ(PCentre, angle_slotOP)

        pS5 = pS1.duplicate()
        pS5.translate(self._machineDict["h_Wedge"], self._machineDict["w_Wedge"] / 2, 0)
        pS6 = pS3.duplicate()
        pS6.translate(self._machineDict["h_Slot"], 0, 0)
        pS7 = pS6.duplicate()
        pS7.translate(0, self._machineDict["w_Slot"], 0)

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
        self._geometricalElement = [surfaceSlotOP, surfaceSlot]
        self._innerLinePart = [lS1]
        self._airDockingLine = [lS1]
        self._airDockingPoint = [pS1]
        self._laminationDockingLine = [lS3, lS5, lS6, lS7]
        self._laminationDockingPoint = [pS6]
        self._betweenLinePart = [lS8, lS2]

    def getBetweenLinePart(self):
        return self._betweenLinePart

    def getairDockingLine(self):
        return self._airDockingLine
    
    def getInnerLinePart(self):
        return self._innerLinePart

    def getairDockingPoint(self):
        return self._airDockingPoint

    def getLaminationDockingLine(self):
        return self._laminationDockingLine

    def getLaminationDockingPoint(self):
        return self._laminationDockingPoint
