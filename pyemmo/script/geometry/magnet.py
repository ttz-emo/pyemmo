"""Module for class Magnet"""
from typing import List, Literal, Union

from ..material.material import Material
from .circleArc import CircleArc
from .line import Line
from .physicalElement import PhysicalElement
from .spline import Spline
from .surface import Surface


class Magnet(PhysicalElement):
    """Eine Instanz der Klasse Magnet beschreibt Magnetteile der elektrischen Maschine im
    dreidimensionalen Raum. Als optische Identifikation der Nord- und Südpole dienen die Farben
    Rot (Nord) und Grün (Süd) des Netzes.
        \\image html magnet.png
    """

    def __init__(
        self,
        name: str,
        geoElements: List[Union[Surface, Union[Line, CircleArc, Spline]]],
        material: Material,
        magDirection: Literal[-1, 1],
        magType: str,
        magVectorAngle: float = None,
        phyID: int = None,
    ):
        """
        Konstruktor der Klasse Magnet

        Args:
            name:           [str]       magnet (physical) name
            geoElements:    [list]      list of geometrical elements
            material:       [Material]
            magDirection:   [-1, 1]     magnetization direction (north or south pole)
            magType:        [str]       magnetization type ("parallel", "radial", "tangential")

            magVectorAngle: [float]     magnetization vector angle (depends on  position)
            (Default: None)\n
            phyID:          [int]       physical ID (Default: None)
        """
        super().__init__(name, geoElements, material, phyID)
        # the physical element type can be used to identify physical elements
        self._physicalElementType = "Magnet"
        ###Magnetisierungsrichtung des Magneten
        self._magnetisationDirection = magDirection
        ###Magnetisierungstype des Magneten (z. B. "radial").
        self._magnetisationType = magType
        ###Winkel des Richtungvektor für die Magnetisierung.
        self._magnetisationVectorAngle = magVectorAngle
        if magDirection == 1:
            self.setColor("Red")
        else:
            self.setColor("Green")

    def setMagnetisation(
        self, magnetisationType: str, magnetisationDirection: Literal[-1, 1]
    ):
        """set magnetisation type

        Args:
            magnetisationType (str): String literal like 'radial', 'parallel',...
            magnetisationDirection (Literal[-1,1]): South or north pole magnetisation.
        """
        self._magnetisationType = magnetisationType
        self._magnetisationDirection = magnetisationDirection
        if magnetisationDirection == 1:
            self.setColor("Red")
        else:
            self.setColor("Green")

    @property
    def magnetisationType(self) -> str:
        """get magnetisationType

        Returns:
            str: _magnetisationType
        """
        return self._magnetisationType

    @property
    def magnetisationDirection(self) -> Literal[-1, 1]:
        """getter of magnetisation direction

        Returns:
            -1 or 1: north or south pole magnetisation
        """
        return self._magnetisationDirection
    
    @property
    def magnetisationVectorAngle(self) -> float:
        """get magnetisation angle

        Returns:
            float: offset angle of magnetisation vector in rad
        """
        return self._magnetisationVectorAngle
    
    @magnetisationVectorAngle.setter
    def magnetisationVectorAngle(self, angle: float):
        """set of magnetisation angle

        Args:
            angle (float): offset angle in rad
        """
        self._magnetisationVectorAngle = angle

