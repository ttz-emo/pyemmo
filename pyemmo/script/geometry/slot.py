from typing import Dict, List, Literal, Tuple, Union
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.material.material import Material
from .physicalElement import PhysicalElement
from .. import colorDict
from math import degrees
from numpy import mean

###
# Eine Instanz der Klasse Slot beschreibt eine Nut einer elektrischen Maschine im dreidimensionalen Raum.
# Eine Bestromung der Nuten wird über die Funktion addExcitation() beschrieben.
# Alle Eigenschaften zur Beschreibung der Stromdichte werden als Dict übergeben.
# \image html slot.png
###
class Slot(PhysicalElement):
    """Class Slot"""

    def __init__(
        self,
        name: str,
        geometricalElement: List[Surface],
        material: Material,
        windingDir: Union[Literal[1], Literal[-1]] = 1,
        phase: float = 0,
        nbrTurns: int = 0,
        phyID: int = None,
    ):
        """
        Constuctor of the class Slot.

        Attribute:
            name (str): slot name
            geometricalElement (List[Surface]): List of surface(s) forming the slot
            material (Material): Slot material
            windingDir (Literal[1,-1]): Winding direction. Defaults to None.
            phase (float): winding phase angle in radians. Defaults to None.
            nbrTurns (int): number of winding turns in slot. Defaults to None.
            phyID (int): Physical Surface ID for Onelab Script. Defaults to None and will be set unique automatically.

        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geometricalElement=geometricalElement,
            phyID=phyID,
        )
        self._physicalElementType = "Slot"  # the physical element type can be used to identify physical elements
        ###Liste aus Flächen (Objekte der Klasse Surface).
        if self.geometricalElement:  # if list is not empty
            if self.getGeoElementType() == Line:
                raise TypeError(
                    f"Physical element type 'Slot' should only contain Surface  Elements but got type Line!"
                )
        # Material der Wicklung
        self.material = material # FIXME: redefinition of material. Allready defined in pe!
        self.windDirection = windingDir  # set winding direction
        self.phase = phase  # set phase angle
        self.nbrTurns = nbrTurns  # set number of winding turns
        # set color
        self.setColor("Orange")

    @property
    def windDirection(self) -> Union[Literal[1], Literal[-1]]:
        """Getter of winding direction"""
        return self._windDirection

    @windDirection.setter
    def windDirection(self, windDir: Union[Literal[1], Literal[-1]]) -> None:
        """Setter of winding direction. Can be +1 or -1."""
        if windDir in (1, -1):
            self._windDirection = windDir
        else:
            raise (ValueError(f"Winding direction was not -1 or +1: {windDir}"))

    @property
    def phase(self) -> float:
        """Getter of phase angle"""
        return self._phase

    @phase.setter
    def phase(self, phaseAngle: float) -> None:
        """Setter of phase angle [radians]"""
        if isinstance(phaseAngle, (int, float)):
            self._phase = phaseAngle
        else:
            raise (ValueError(f"Phase angle was not a valid number: {phaseAngle}"))

    @property
    def nbrTurns(self) -> int:
        """Getter of number of winding turns in face attribute"""
        return self._nbrTurns

    @nbrTurns.setter
    def nbrTurns(self, nbrTurnsInFace: int) -> None:
        """Setter of number of wires in face attribute"""
        if isinstance(nbrTurnsInFace, int):
            self._nbrTurns = nbrTurnsInFace
        elif isinstance(nbrTurnsInFace, float):
            # nbrTurnsInFace: float = nbrTurnsInFace
            if nbrTurnsInFace.is_integer():
                self._nbrTurns = int(nbrTurnsInFace)
            else:
                raise (ValueError(f"Number of turns is not type int: {nbrTurnsInFace}"))
        else:
            raise (
                ValueError(f"Number of turns in face is not a number: {nbrTurnsInFace}")
            )

    def getPhase(self, phaseStr: str = None) -> Union[float, str]:
        """
        Getter of phase angle attribute. With the parameter phaseStr, the output of the function can be modified.
        For example if the result should the phase as character in 'UVW', the phaseStr must be 'UVW'. Otherwise the angle of the phase in rad will be given.

        Input:
            phaseStr: str (len=3)!
        Output
            phase: str | float
        """
        if phaseStr is not None and len(phaseStr) != 3:
            raise ValueError(
                f"Parameter phaseStr must be None or string with length 3, but is: {phaseStr}"
            )
        if phaseStr is None:
            return self.phase
        else:
            angleDeg = degrees(self.phase) % 360
            # this results in phase index: 0->0, 120->1, 240->2
            phaseIndex = (
                round(angleDeg / 120, None) % 3
            )  # mod 3, to make sure 2 Pi is handled correctly
            phase = phaseStr[phaseIndex]
            return phase

    def getRadialPosition(self) -> Tuple[float, float]:
        """get the radial position of the slot.
        This usefull when sorting the slots in circumfederal direction

        Returns
            float: Angle of the center of the slots surface(s) in radians
            float: Radius of the center of the slots surface(s) in m
        """
        radList: List[float] = list()
        phiList: List[float] = list()
        for surf in self.geometricalElement:
            centerPoint = surf.calcCOG()
            phiList.append(centerPoint.getAngleToX())
            radList.append(centerPoint.getRadius())
        return (mean(phiList), mean(radList))
