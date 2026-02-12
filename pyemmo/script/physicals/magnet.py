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
"""Module for class Magnet"""
from __future__ import annotations

from typing import Literal

from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from ..geometry.spline import Spline
from ..geometry.surface import Surface
from ..material.material import Material
from .physicalElement import PhysicalElement


class Magnet(PhysicalElement):
    """Eine Instanz der Klasse Magnet beschreibt Magnetteile der elektrischen Maschine im
    dreidimensionalen Raum. Als optische Identifikation der Nord- und Südpole dienen die Farben
    Rot (Nord) und Grün (Süd) des Netzes.

        \\image html magnet.png

    """

    def __init__(
        self,
        name: str,
        geoElements: list[Surface | Line | CircleArc | Spline],
        material: Material,
        magDirection: Literal[-1, 1],
        magType: str,
        magVectorAngle: float = None,
        phyID: int = None,
    ):
        """
        Konstruktor der Klasse Magnet

        Args:
            name (str): magnet (physical) name
            geoElements (list): list of geometrical elements
            material (Material): Magnet material
            magDirection (Literal[-1, 1]): magnetization direction (north or
                south pole)
            magType (str): magnetization type ("parallel", "radial",
                "tangential")
            magVectorAngle (float): magnetization vector angle in rad. See
                ``Magnet.magAngle`` for more details. Defaults to None
            phyID (int): physical ID (Default: None)
        """
        super().__init__(name, geoElements, material, phyID)
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "Magnet"
        ###Magnetisierungsrichtung des Magneten (+1 oder -1)
        self.magDir = magDirection
        ###Magnetisierungstype des Magneten (z. B. "radial").
        self.magType = magType
        ###Winkel des Richtungvektor für die Magnetisierung.
        self.magAngle = magVectorAngle
        if magDirection == 1:
            self.setColor("Red")
        else:
            self.setColor("Green")

    def setMagnetisation(
        self,
        magnetisationType: Literal["parallel", "radial", "tangential"],
        magnetisationDirection: Literal[-1, 1],
    ):
        """set magnetization type

        Args:
            magnetisationType (str): String literal like 'radial', 'parallel',...
            magnetisationDirection (Literal[-1,1]): South or north pole magnetization.
        """
        self.magType = magnetisationType
        self.magDir = magnetisationDirection
        if magnetisationDirection == 1:
            self.setColor("Red")
        else:
            self.setColor("Green")

    @property
    def magType(self) -> Literal["parallel", "radial", "tangential"]:
        """Magnetization Type

        Returns:
            (Literal[&quot;parallel&quot;, &quot;radial&quot;, &quot;tangential&quot;]): Magnetization type
        """
        return self._magnetizationType

    @magType.setter
    def magType(self, newMagType: Literal["parallel", "radial", "tangential"]):
        """setter of magnetization type

        Args:
            newMagType (Literal[&quot;parallel&quot;, &quot;radial&quot;, &quot;tangential&quot;]):
             Magnetization type
        """
        if isinstance(newMagType, str):
            if newMagType in ("parallel", "radial", "tangential"):
                self._magnetizationType = newMagType
                return None
        raise TypeError(
            f'Wrong Magnetization Type: {newMagType}.\nMust be "parallel", "radial" or "tangential"'
        )

    @property
    def magDir(self) -> Literal[-1, 1]:
        """getter of magnetization direction

        Returns:
            -1 or 1: north or south pole magnetization
        """
        return self._magnetisationDirection

    @magDir.setter
    def magDir(self, newMagDir: Literal[-1, 1]):
        if newMagDir in (-1, 1):
            self._magnetisationDirection = newMagDir
        else:
            raise ValueError(
                f"Magnetizarion direction not in (-1, 1), but is: {newMagDir}"
            )

    @property
    def magAngle(self) -> float:
        """Magnetization vector angle

        Returns:
            float: offset angle of magnetization vector in rad
        """
        return self._magnetisationVectorAngle

    @magAngle.setter
    def magAngle(self, angle: float):
        """set of magnetization angle

        Args:
            angle (float): offset angle in rad
        """
        if not isinstance(angle, float):
            raise ValueError(
                f"Given magnetization angle is not type float but {type(angle)}!"
            )
        self._magnetisationVectorAngle = angle
