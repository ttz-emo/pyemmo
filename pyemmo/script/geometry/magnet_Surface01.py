from .magnet import Magnet
from .point import Point
from .line import Line
from .circleArc import CircleArc
from .surface import Surface
from .. import colorDict


###
# Ein Objekt der Klasse Magnet_Surface01:
# \image html magnet_Surface01.png
# Der Magnettype wird mit addRotorToMachine() ausgewählt und mit addMagnetParameter() parametrisiert. Abschließend verknüpft die Funktion createRotor() den Magnet am Rotorobjekt.
#
#   Beispiel:
#
#       pmsm1 = pyd.MachineSPMSM({...})
#       rotor1 = pmsm1.addRotorToMachine('sheet01_standard', 'magnet01_surface')
#       rotor1.addLaminationParameter({...})
#       rotor1.addMagnetParameter({'h_M' : 7e-3,
#           'angularWidth_i' : math.pi/10,
#           'angularWidth_a' : math.pi/12,
#           'magnetisationDirection' : [1, -1, 1, -1, 1, -1, 1, -1],
#           'magnetisationType' : 'radial',
#           'material' : ndFe35,
#           'meshLength' : 3e-3})
#       rotor1.addAirGapParameter({...})
#       rotor1.createRotor()
#
###
class Magnet_Surface01(Magnet):
    """Class Magnet_Surface01

    The parameters must be given by a dict with the exact matching parameter names!

    Parameters:
        rA_Rotor (float): Rotor outer radius
        h_M (float): Magnet hight
        angularWidth_i (float): Inner angular width
        angularWidth_a (float): Outer angular width
        magnetisationDirection (Literial[-1,1]): see definition in Class
            :class:`~pyemmo.script.geometry.magnet.Magnet`
        magnetisationType (str): see definition in Class
            :class:`~pyemmo.script.geometry.magnet.Magnet`
        material (Material): Material of magnet.
        meshLength (float):

    .. figure:: ../image_Doku/magnet_Surface01.png
        :align: center

        Parameter description for Magnet_Surface01
    """

    ###
    # Konstuktor der Klasse Magnet_Surface01.
    #
    #   Input:
    #
    #       machineDict : Dict
    #       magnetisationDirection : Integer
    #       magnetisationType : String
    #
    ###
    def __init__(self, machineDict, magnetisationDirection, magnetisationType):
        ###Dictionary mit allen Magnet-Parametern.
        self._machineDict = machineDict

        self.id = self._getNewID()
        magName = "Magnet_Surface01_" + str(self.id)
        super().__init__(
            magName,
            [],
            machineDict["material"],
            magnetisationDirection,
            magnetisationType,
            0.0,
        )

        self._createGeometry()

    ###_createGeometry() erzeugt die Magnetgeometrie und definiert alle Attribute der Klasse.
    def _createGeometry(self):
        dockingLength = self._machineDict["rA_Rotor"]
        h_M = self._machineDict["h_M"]
        angle_ri = self._machineDict["angularWidth_i"]
        angle_ra = self._machineDict["angularWidth_a"]
        magnet_centre = self._machineDict["machineCentrePoint"]

        PCentre = magnet_centre.duplicate()
        coordCentre = PCentre.coordinate

        # Konstuktion der Punkte an der x-Achse
        pMagnet1 = Point(
            "pMagnet1",
            coordCentre[0] + dockingLength,
            coordCentre[1],
            coordCentre[2],
            self._machineDict["meshLength"],
        )
        pMagnet2 = pMagnet1.duplicate()
        pMagnet2.name = "pMagnet2"
        pMagnet3 = Point(
            name="pMagnet3",
            x=coordCentre[0] + dockingLength + h_M,
            y=coordCentre[1],
            z=coordCentre[2],
            meshLength=self._machineDict["meshLength"],
        )
        pMagnet4 = pMagnet3.duplicate()
        pMagnet4.name = "pMagnet4"
        pMagnet2.rotateZ(PCentre, angle_ri)
        pMagnet4.rotateZ(PCentre, angle_ra)

        # Startposition berücksichtigen
        pMagnet1.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet2.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet3.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet4.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lMagnet1 = CircleArc("lMagnet1", pMagnet1, PCentre, pMagnet2)
        lMagnet2 = Line("lMagnet2", pMagnet2, pMagnet4)
        lMagnet3 = CircleArc("lMagnet3", pMagnet4, PCentre, pMagnet3)
        lMagnet4 = Line("lMagnet4", pMagnet3, pMagnet1)

        # Flächenerzeugen
        surfaceMagnet = Surface(
            "surfaceMagnet", [lMagnet1, lMagnet2, lMagnet3, lMagnet4]
        )

        # Bei jedem Baukasten muss diese Definition identisch sein
        ###Fläche des halben Magneten in einer Liste.
        self._geometricalElement = [surfaceMagnet]
        ###Schnittkante des halben Magneten.
        # \image html innerLinePart01.png
        self._innerLinePart = [lMagnet1]
        ###Punkt zwischen Magnet und Luft an der Schnittkante.
        # \image html airDockingPoint01.png
        self._airDockingPoint = [pMagnet3]
        ###Alle Linien in einer Liste, die den Luftraum schneiden.
        # \image html airLinePart01.png
        self._airLinePart = [lMagnet3, lMagnet2]
        ###Punkt zwischen Blechpaket und Magneten an der Schnittkante.
        # \image html laminationDockingPoint01.png
        self._laminationDockingPoint = [pMagnet1]

        for s in self._geometricalElement:
            if self.magDir == 1:
                s.setMeshColor(colorDict["Red"])
            elif self.magDir == -1:
                s.setMeshColor(colorDict["Green"])

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
        Gibt eine Liste mit dem airDockingPoint zurück (siehe _airDockingPoint)

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
