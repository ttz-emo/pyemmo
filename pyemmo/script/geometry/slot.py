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
"""Module for class Slot"""
from math import degrees, isclose, pi
from typing import List, Literal, Tuple, Union

from numpy import mean

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.surface import Surface
from pyemmo.script.material.material import Material

from .physicalElement import PhysicalElement

import gmsh


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
        windingDir: Literal[-1, 1] = 1,
        phase: float = 0,
        nbrTurns: int = 0,
        phyID: int = None,
    ):
        """
        Constuctor of the class Slot.

        Args:
            name (str): slot name
            geometricalElement (List[Surface]): List of surface(s) forming the slot
            material (Material): Slot material
            windingDir (Literal[1,-1]): Winding direction. Defaults to None.
            phase (float): winding phase angle in radians. Defaults to None.
            nbrTurns (int): number of winding turns in slot. Defaults to None.
            phyID (int): Physical Surface ID for Onelab Script. Defaults to None and will be set unique automatically.

        """
        super().__init__(
            name=name,
            material=material,
            geometricalElement=geometricalElement,
            phyID=phyID,
        )
        self.physicalElementType = "Slot"  # the physical element type can be used to identify physical elements
        ###Liste aus Flächen (Objekte der Klasse Surface).
        if self.geometricalElement:  # if list is not empty
            if self.geoElementType == Line:
                raise TypeError(
                    "Physical element type 'Slot' should only contain "
                    "Surface Elements but got type Line!"
                )
        # Material der Wicklung
        self.windDirection = windingDir  # set winding direction
        self.phase = phase  # set phase angle
        self.nbrTurns = nbrTurns  # set number of winding turns
        self.setColor()  # set color

        #Create physical objects with gmsh
        # surface_tag_list = [elem.id for elem in geometricalElement]
        # self._id = gmsh.model.addPhysicalGroup(2, surface_tag_list, name = name)

    @property
    def windDirection(self) -> Literal[-1, 1]:
        """Winding direction

        Returns:
            Literal[-1,1]: Winding direction (-1 = -z, 1 = +z)
        """
        return self._windDirection

    @windDirection.setter
    def windDirection(self, windDir: Literal[-1, 1]) -> None:
        """Setter of winding direction. Can be +1 or -1.

        Args:
            windDir (Union[Literal[1], Literal[): _description_
        """
        if windDir in (1, -1):
            self._windDirection = windDir
        else:
            raise (ValueError(f"Winding direction was not -1 or +1: {windDir}"))

    @property
    def phase(self) -> float:
        """slot winding phase angle

        Returns:
            float: phase angle in rad
        """
        return self._phase

    @phase.setter
    def phase(self, phaseAngle: float) -> None:
        """Setter of phase angle

        Args:
            phaseAngle (float): angle of winding phase in rad.
        """
        if isinstance(phaseAngle, (int, float)):
            self._phase = phaseAngle
        else:
            raise (ValueError(f"Phase angle was not a valid number: {phaseAngle}"))

    @property
    def nbrTurns(self) -> int:
        """Getter of number of winding turns in face attribute

        Returns:
            int: number of winding turns in slot.
        """
        return self._nbrTurns

    @nbrTurns.setter
    def nbrTurns(self, nbrTurnsInFace: Union[int, float]) -> None:
        """Setter of number of wires in face attribute

        Args:
            nbrTurnsInFace (int): number of winding turns in slot
        """
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

    def get_radial_position(self) -> Tuple[float, float]:
        """get the radial position of the slot.\n
        This is useful when sorting the slots in radial direction

        Returns:
            float: Radius of the center of the slots surface(s) in m
        """
        radList: List[float] = []
        for surf in self.geometricalElement:
            centerPoint = surf.calcCOG()
            radList.append(centerPoint.radius)
        return mean(radList)

    def get_circumferential_position(self) -> Tuple[float, float]:
        """get the circumferential position of the slot.\n
        This is useful when sorting the slots in circumfederal direction

        Returns:
            float: Angle of the center of the slots surface(s) in radians
        """
        if not self.geometricalElement:
            raise RuntimeError("No geometry to determine slot position.")
        phiList: List[float] = []
        for surf in self.geometricalElement:
            centerPoint = surf.calcCOG()
            phiList.append(centerPoint.getAngleToX())
        return mean(phiList)

    def setColor(self, colorName: str = None):  # overwrite set color
        """Set mesh color for Slot

        If no mesh color name is given => determine by phase OR use orange

        All available mesh colors are listed under
        `gmsh colors <https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_11_0/src/common/Colors.h>`__.

        Args:
            colorName (str, optional): `X11 color name <https://en.wikipedia.org/wiki/X11_color_names>`__
                as string. Defaults to Phase color.
        """
        if not colorName:
            phaseDeg = degrees(self.phase % (2 * pi))
            if isclose(phaseDeg, 0):
                # phase u
                super().setColor("Magenta")
            elif isclose(phaseDeg, 120):
                # phase v
                super().setColor("Yellow4")
            elif isclose(phaseDeg, 240):
                # phase w
                super().setColor("Cyan")
        else:
            super().setColor("Orange")
