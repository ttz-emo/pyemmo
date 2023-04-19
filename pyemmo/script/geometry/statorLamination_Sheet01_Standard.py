from .statorLamination import StatorLamination
from .physicalElement import PhysicalElement
from .. import colorDict
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface
import math

###
# Ein Objekt der Klasse StatorLamination_Sheet01_Standard:
# \image html statorBlech.png
# Das Blechpaket wird mit addStatorToMachine() ausgewählt und mit addLaminationParameter() parametrisiert. Abschließend verknüpft die Funktion createStator() das Blech am Statorobjekt.
#
#   Beispiel:
#
#       pmsm1 = pyd.MachineSPMSM({...})
#       stator1 = pmsm1.addStatorToMachine("sheet01_standard", "slotForm_01")
#       stator1.addLaminationParameter({
#           "r_S_i": 65e-3,
#           "r_S_a": 100e-3,
#           "meshLength": 3e-3,
#           "material": steel_1010,
#           "machineCentrePoint": PBohrung,
#           })
#       stator1.addSlotParameter({...})
#       stator1.addAirGapParameter({...})
#       stator1.createStator()
#
###
class StatorLamination_Sheet01_Standard(StatorLamination):
    ###
    # Konstruktor der Klasse StatorLamination.
    #
    #   Input:
    #
    #       machineDict : dict
    #
    ###
    def __init__(self, machineDict):
        self._machineDict = machineDict
        StatorLamination.__init__(
            self,
            name="StatorLamination_Sheet01_Standard",
            geometricalElement=list(),
            material=None,
        )
        ###Name des Statorblechs
        self._name = "StatorLamination_Sheet01_Standard_" + str(self.id)
        self._createGeometry()

    ###_createGeometry() erzeugt die Blechgeometrie und definiert alle Attribute der Klasse.
    def _createGeometry(self):
        r_S_i = self._machineDict["r_S_i"]
        r_S_a = self._machineDict["r_S_a"]

        PCentre = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.getCoordinate()

        alpha = self._machineDict["angleGeoParts"]

        # Konstuktion der Punkte an der x-Achse
        pSi1 = Point(
            "pSi1",
            coordCentre[0] + r_S_i,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
        )
        pSi2 = pSi1.duplicate()
        pSi2.name = "pSi2"
        pSa1 = pSi1.duplicate()
        pSa1.translate(r_S_a - r_S_i, 0, 0)
        pSa1.name = "pSa1"
        pSa2 = pSa1.duplicate()
        pSa2.name = "pSa2"
        pSi2.rotateZ(PCentre, alpha)
        pSa2.rotateZ(PCentre, alpha)

        # Startposition berücksichtigen
        pSi1.rotateZ(PCentre, self._machineDict["startPosition"])
        pSi2.rotateZ(PCentre, self._machineDict["startPosition"])
        pSa1.rotateZ(PCentre, self._machineDict["startPosition"])
        pSa2.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lSi = CircleArc("lSi", pSi1, PCentre, pSi2)
        lBlech1 = Line("lSBlech1", pSi2, pSa2)
        lSa = CircleArc("lSa", pSa2, PCentre, pSa1)
        lBlech2 = Line("lSBlech2", pSa1, pSi1)

        # Flächenerzeugen
        surfaceStator = Surface("surfaceStator", [lSi, lBlech1, lSa, lBlech2])
        surfaceStator.setMeshColor(colorDict["SteelBlue"])

        # Bei jedem Baukausten müssen diese Attribute vorkommen
        ###Fläche des Bleches (halbe Nut bzw. Zahn) in einer Liste.
        self._geometricalElement = [surfaceStator]
        ###Material des Bleches.
        self._material = self._machineDict["material"]
        ###Innenkante des Bleches.
        # \image html innerLinePart.png
        self._innerLinePart = [lSi]
        ###Schnittkante zwischen 2 Blechen.
        # \image html betweenLinePart.png
        self._betweenLinePart = [lBlech2]
        ###Erster Punkt auf der Innenkante des Bleches.
        # \image html airDockingPoint3.png
        self._airDockingPoint1 = [pSi1]
        ###Erster Punkt auf der Innenkante des Bleches.
        # \image html airDockingPoint4.png
        self._airDockingPoint2 = [pSi2]

    ###Gibt eine Liste mit der Innenkante des Statorbleches zurück (siehe _innerLinePart).
    def getInnerLinePart(self):
        return self._innerLinePart

    ###Gibt eine Liste mit der Schnittkante zurück (siehe _betweenLinePart).
    def getBetweenLinePart(self):
        return self._betweenLinePart

    ###Gibt eine Liste mit dem airDockingPoint1 zurück (siehe _airDockingPoint1).
    def getAirDockingPoint1(self):
        return self._airDockingPoint1

    ###Gibt eine Liste mit dem airDockingPoint2 zurück (siehe _airDockingPoint2).
    def getAirDockingPoint2(self):
        return self._airDockingPoint2
