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
"""Module for AirArea Physical Element"""
from typing import List, Union

from ..material.material import Material
from .circleArc import CircleArc, Line
from .physicalElement import PhysicalElement
from .spline import Spline
from .surface import Surface


class AirGap(PhysicalElement):
    """
    Eine Instanz der AirGap ist ein Teil des Luftspalts einer elektrischen Maschine im
    dreidimensionalen Raum. Diese Klasse beschreibt sowohl den Luftraum auf der Rotor sowie auf
    der Stator-Seite.

        \\image html class_airGap.png

    Beim Verwenden vom Baukasten muss der Luftspalt vom Nutzer nicht manuell definiert werden.
    Die Ergänzung vom Luftraum muss bei der Erstellung vom Rotor bzw. Stator automatisch erfolgen
    (siehe RotorSPMSM.py).

    """

    def __init__(
        self,
        name: str,
        geometricalElement: List[Union[Surface, Line, CircleArc, Spline]],
        material: Material = None,
    ):
        """AirGap

        Args:
            name (str): Physical Element Name
            geometricalElement (List[Union[Surface, Line, CircleArc, Spline]]):
            List of geo elements
            material (Material, optional): Material of airgap. Defaults to None.
        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geometricalElement=geometricalElement,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirGap"
        self.setColor("SkyBlue")
