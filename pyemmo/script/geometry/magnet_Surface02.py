"""Module for tool kit magnet 02"""
import math
from typing import Any, Dict

from .. import colorDict
from .circleArc import CircleArc
from .line import Line
from .magnet import Magnet
from .point import Point
from .surface import Surface


###
# Ein Objekt der Klasse Magnet_Surface02:
# \image html magnet_Surface02.png
# Der Magnettype wird mit addRotorToMachine() ausgewählt und mit addMagnetParameter()
# parametrisiert. Abschließend verknüpft die Funktion createRotor() den Magnet am Rotorobjekt.

###
class Magnet_Surface02(Magnet):
    """Magnet_Surface01

    Parameters:
        h_M (float): Magnet hight
        w_Mag (float): Magnet width
        r_Mag (float): Magnet contour radius
        magnetisationDirection (Literial[-1,1]): see Magnet
        magnetisationType (str): see Magnet
        material (Material)
        meshLength (float)

    Rotor parameters
        rA_Rotor (float): Rotor outer radius

    Beispiel:
        pmsm1 = pyd.MachineSPMSM({...})\n
        rotor1 = pmsm1.addRotorToMachine('sheet01_standard', 'magnet02_surface')\n
        rotor1.addLaminationParameter({...})\n
        rotor1.addMagnetParameter({'h_M' : 7.5e-3,\n
                'w_Mag' : 15e-3,\n
                'r_Mag' : 18e-3,\n
                'magnetisationDirection' : [1, -1, 1, -1, 1, -1, 1, -1],\n
                'magnetisationType' : 'radial',\n
                'material' : ndFe35,\n
                'meshLength' : 3e-3})\n
        rotor1.addAirGapParameter({...})\n
        rotor1.createRotor()\n
    """

    def __init__(self, machineDict, magnetisationDirection, magnetisationType):
        self._machineDict: Dict[str, Any] = machineDict
        self.id = self._getNewID()
        magSurf02Name = "Magnet_Surface02_" + str(self.id)
        super().__init__(
            name=magSurf02Name,
            geoElements=[],
            material=machineDict["material"],
            magDirection=magnetisationDirection,
            magType=magnetisationType,
        )
        self._createGeometry()

    ###_createGeometry() erzeugt die Magnetgeometrie und definiert alle Attribute der Klasse.
    def _createGeometry(self):
        dockingLength = self._machineDict["rA_Rotor"]
        h_M = self._machineDict["h_M"]
        width_M = self._machineDict["w_Mag"]
        r_Mag = self._machineDict["r_Mag"]

        PCentre = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.coordinate

        # Konstuktion der Punkte an der x-Achse
        pMagnet1 = Point(
            "pMagnet1",
            coordCentre[0] + dockingLength,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
        )
        alpha1 = math.asin(width_M / 2 / dockingLength)
        pMagnet1.rotateZ(PCentre, alpha1)
        pMagnet2 = pMagnet1.duplicate()
        pMagnet2.translate(0, -width_M / 2, 0)
        pMagnet2.name = "pMagnet2"
        pMagnet3 = pMagnet2.duplicate()
        pMagnet3.translate(h_M, 0, 0)

        centreMagX = pMagnet3.coordinate[0] - r_Mag
        centerMag = Point(
            "pCentreMag", centreMagX + coordCentre[0], coordCentre[1], coordCentre[2], 1
        )
        xMag4 = math.sqrt(math.pow(r_Mag, 2) - math.pow(width_M / 2, 2)) + centreMagX
        pMagnet4 = Point(
            "pMagnet4",
            xMag4 + coordCentre[0],
            width_M / 2 + coordCentre[1],
            +coordCentre[2],
            self._machineDict["meshLength"],
        )

        # Startposition berücksichtigen
        pMagnet1.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet2.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet3.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet4.rotateZ(PCentre, self._machineDict["startPosition"])
        centerMag.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lMagnet1 = Line("lMagnet1", pMagnet2, pMagnet1)
        lMagnet2 = Line("lMagnet2", pMagnet1, pMagnet4)
        lMagnet3 = CircleArc("lMagnet3", pMagnet4, centerMag, pMagnet3)
        lMagnet4 = Line("lMagnet4", pMagnet3, pMagnet2)

        # Flächenerzeugen
        surfaceMagnet = Surface(
            "surfaceMagnet", [lMagnet1, lMagnet2, lMagnet3, lMagnet4]
        )

        # Bei jedem Baukasten muss diese Definition identisch sein
        ###Fläche des halben Magneten in einer Liste.
        self.geometricalElement = [surfaceMagnet]
        ###Schnittkante des halben Magneten.
        # \image html innerLinePart02.png
        self._innerLinePart = [lMagnet1]
        ###Punkt zwischen Magnet und Luft an der Schnittkante.
        # \image html airDockingPoint02.png
        self._airDockingPoint = [pMagnet3]
        ###Alle Linien in einer Liste, die den Luftraum schneiden.
        # \image html airLinePart02.png
        self._airLinePart = [lMagnet3, lMagnet2]
        ###Punkt zwischen Blechpaket und Magneten an der Schnittkante.
        # \image html laminationDockingPoint02.png
        self._laminationDockingPoint = [pMagnet2]

        for surf in self.geometricalElement:
            if self.magDir == 1:
                surf.setMeshColor(colorDict["Red"])
            elif self.magDir == -1:
                surf.setMeshColor(colorDict["Green"])

    ###Gibt eine Liste mit der Schnittkante im Magneten zurück (siehe _innerLinePart).
    @property
    def innerLinePart(self) -> list:
        """get innerLinePart \n
        Gibt eine Liste mit der Schnittkante im Magneten zurück (siehe _innerLinePart).
        Returns:
            list: _innerLinePart
        """
        return self._innerLinePart

    ###Gibt eine Liste mit dem airDockingPoint zurück (siehe _airDockingPoint).
    @property
    def airDockingPoint(self) -> list:
        """get airDockingPoint \n
        Gibt eine Liste mit dem airDockingPoint zurück (siehe _airDockingPoint).
        Returns:
            list: _airDockingPoint
        """
        return self._airDockingPoint

    ###Gibt eine Liste mit airLinePart zurück (siehe _airLinePart).
    @property
    def airLinePart(self) -> list:
        """get airLinePart \n
        Gibt eine Liste mit airLinePart zurück (siehe _airLinePart).
        Returns:
            list: _airLinePart
        """
        return self._airLinePart

    ###Gibt eine Liste mit dem laminationDockingPoint zurück (siehe _laminationDockingPoint).
    @property
    def laminationDockingPoint(self) -> list:
        """get laminationDockingPoint \n
        Gibt eine Liste mit dem laminationDockingPoint zurück (siehe _laminationDockingPoint).
        Returns:
            list: _laminationDockingPoint
        """
        return self._laminationDockingPoint
