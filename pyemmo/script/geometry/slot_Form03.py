from .slot import Slot

"""Module for class Slot_Form03"""
import math
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface


class Slot_Form03(Slot):
    def __init__(self, machineDict):
        self.machineDict = machineDict
        super().__init__(
            name="Slot_Form03",
            geometricalElement=[],
            material=machineDict["material"],
        )
        self._name = "Slot_Form03_" + str(self.id)
        self._createGeometry()

    def _createGeometry(self):
        """Create the slot geometry"""
        dockingLength = self.machineDict["rI_Stator"]
        angle_slotOP = math.atan2(self.machineDict["w_SlotOP"], dockingLength)
        PCentre: Point = self.machineDict["machineCentrePoint"]
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
        pS6.translate(self.machineDict["h_Slot"], self.machineDict["r_Slot"], 0)
        pS7 = pS3.duplicate()
        pS7.translate(self.machineDict["h_Slot"] + self.machineDict["r_Slot"], 0, 0)
        pRot = pS3.duplicate()
        pRot.translate(self.machineDict["h_Slot"], 0, 0)

        pS1.rotateZ(PCentre, angleStart)
        pS2.rotateZ(PCentre, angleStart)
        pS3.rotateZ(PCentre, angleStart)
        pS4.rotateZ(PCentre, angleStart)
        pS5.rotateZ(PCentre, angleStart)
        pS6.rotateZ(PCentre, angleStart)
        pS7.rotateZ(PCentre, angleStart)
        pRot.rotateZ(PCentre, angleStart)

        # Konstuktion der Linien
        lS1 = CircleArc("lS1", pS1, PCentre, pS2)
        lS2 = Line("lS2", pS1, pS3)
        lS3 = Line("lS3", pS2, pS4)
        lS4 = CircleArc("lS4", pS3, PCentre, pS4)

        lS5 = Line("lS5", pS4, pS5)
        lS6 = Line("lS6", pS5, pS6)
        lS7 = CircleArc("lS7", pS6, pRot, pS7)
        lS8 = Line("lS9", pS7, pS3)

        # Flächenerzeugen
        surfaceSlotOP = Surface("slotOP", [lS1, lS2, lS3, lS4])
        surfaceSlot = Surface("slotF1", [lS4, lS5, lS6, lS7, lS8])

        # Bei jedem Baukasten muss diese Definition identisch sein
        self._geometricalElement = [surfaceSlotOP, surfaceSlot]
        self._innerLinePart = [lS1]
        self._airDockingPoint = [pS1]
        self._laminationDockingLine = [lS3, lS5, lS6, lS7]
        self._laminationDockingPoint = [pS7]  #
        self._betweenLinePart = [lS8, lS2]

    @property
    def betweenLinePart(self):
        """Getter of betweenLinePart

        Returns:
            _type_: _description_
        """
        return self._betweenLinePart

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
