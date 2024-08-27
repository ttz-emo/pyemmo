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
"""Module for class MovingBand"""
from typing import List

from ..material.material import Material
from ..script import DEFAULT_GEO_TOL
from .circleArc import CircleArc
from .physicalElement import PhysicalElement


class MovingBand(PhysicalElement):
    """Eine Instanz der Klasse MovingBand beschreibt das Band im Luftspalt, die bei der Movingband-
    Simulationsmethode für die Drehung des Netzes verwendet wird. Das Movingband muss auf der Rotor-
    Seite einen Vollkreis beschreiben, ist jedoch auf der Stator-Seite nicht nötig.
        \\image html mb_Rotor.png
        \\image html mb_Stator.png
    """

    ###
    # Konstruktor der Klasse MovingBand.
    #
    #   Attribute:
    #
    #       ID : Integer
    #       name : String
    #       material : Material
    #       geo_list : [CircleArc]
    #       auxiliary : Boolean
    #
    ###
    def __init__(
        self,
        name: str,
        geo_list: List[CircleArc],
        material: Material = None,
        auxiliary: bool = False,
    ):
        """Create a moving band segment

        Args:
            name (str): Moving band segment name
            geo_list (List[CircleArc]): List of arc segments to build the mb segment.
            material (Material, optional): Airgap material. Defaults to None.
            auxiliary (bool, optional): Flag to determine if given moving band segment is auxillar.
            Defaults to False.
        """
        super().__init__(name=name, geo_list=geo_list, material=material)
        # make sure geo elements are circle arcs
        self.geo_list: List[CircleArc] = geo_list
        self.radius = geo_list[0].radius
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "MovingBand"
        ###Hilfslinien des Movingbands zur Ergänzung zum Vollkreis, bei einem Teilmodell.
        self._auxiliary = auxiliary

    @property
    def auxiliary(self) -> bool:
        """Gibt den Nutzer die Information zurück (Boolean), ob es sich bei dem Objekt um eine
        Hilfslinie handelt.

        Returns:
            bool: If MovingBand object is outside model segment (case symmetry) or not.
        """
        return self._auxiliary

    @property
    def radius(self) -> float:
        """Get the moving band radius"""
        return self._radius

    @radius.setter
    def radius(self, mbRadius: float):
        """setter of movingband radius

        Args:
            mbRadius (float): Movingband Radius

        Raises:
            ValueError: If the given radius does not match the radius of the given circle arcs.
        """
        for arc in self.geo_list:
            if abs(arc.radius - mbRadius) > DEFAULT_GEO_TOL:
                raise (
                    ValueError(
                        "Rotor Movingband domain got Circle Arc objects with different Radius:\n"
                        + f"Movingband radius: {mbRadius}\n"
                        + f"Radius of {arc.name}: {arc.radius}\n"
                    )
                )
        self._radius = mbRadius
