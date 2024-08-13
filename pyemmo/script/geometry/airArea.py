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
from typing import List

from .physicalElement import Material, PhysicalElement, Surface


class AirArea(PhysicalElement):
    """
    Eine Instanz der Klasse AirArea beschreibt jeden beliebigen Luftraum innerhalb der
    elektrischen Maschine im dreidimensionalen Raum. Für den Luftspalt existiert eine eigene
    Klasse AirGap. Diese Klasse ist eine abgeleitete Klasse der Basisklasse PhysicalElement.
    Beim Verwenden vom Baukasten muss der Luftspalt vom Nutzer nicht manuell definiert werden.
    Die Ergänzung vom Luftraum muss bei der Erstellung vom Rotor bzw. Stator automatisch erfolgen
    (siehe RotorSPMSM.py).

        \\image html class_airArea.png

    """

    ###
    # Konstruktor der Klasse AirArea.
    #
    #   Attribute:
    #
    #       ID : Integer
    #       name : String
    #       material : Material
    #       geometricalElement : [Surface]
    #
    ###
    def __init__(
        self,
        name: str,
        geometricalElement: List[Surface],
        material: Material = None,
    ):
        """AirArea is any area defined with material air except from the Airgap surface

        Args:
            - name (str): Domain name
            - geometricalElement (List[Union[Surface, Line, CircleArc, Spline]):
            List of geometry objects
            - material (Material, optional): Material of AirArea. Should be "air". Defaults to None.
        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geometricalElement=geometricalElement,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirArea"
        self.setColor("SkyBlue")
