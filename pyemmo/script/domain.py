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
"""Module for Class Domain"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .physicals.physicalElement import PhysicalElement

if TYPE_CHECKING:
    from .script import Script
# pylint: disable=locally-disabled, line-too-long


class Domain:
    """Eine Instanz der Klasse Domain ist die Gruppierung von PhysicalElement-Objekten.

    Input:
        name : string
        physicalElement : [PhysicalElement]

    Beispiel:
        Diese Magnetdomaine (siehe Bild) besteht aus 2 PhysicalElements-Objekten und 4
        Surface-Objekten.

        \\image html domain_Magnet.png
    """

    def __init__(
        self,
        name: str,
        physicalElements: list[PhysicalElement] | PhysicalElement,
    ):
        self.name = name
        self.physicals = physicalElements

    @property
    def name(self) -> str:
        """getter of domain Name

        Returns:
            str: Domain name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """setter of domain name

        Args:
            name (str): New domain name
        """
        self._name = name

    @property
    def physicals(self) -> list[PhysicalElement]:
        """List of physical surfaces/lines (PhysicalElement objects) belonging to
        the domain.

        Returns:
            List[PhysicalElement]: List of physical surfaces/lines
        """
        return self._physicals

    @physicals.setter
    def physicals(self, physicalElements: PhysicalElement | list[PhysicalElement]):
        """setter of physical element list

        Args:
            physicalElements (PhysicalElement | List[PhysicalElement]): New physicals

        Raises:
            TypeError: If physicalElements not is list
        """
        if isinstance(physicalElements, list):
            if all(
                isinstance(physElem, PhysicalElement) for physElem in physicalElements
            ):
                self._physicals = physicalElements
                return None
        if isinstance(physicalElements, PhysicalElement):
            self._physicals = [physicalElements]
            return None
        raise TypeError(
            f"Should be List[PhysicalElement] or PhysicalElement but is: {type(physicalElements)}"
        )

    def addPhysicalElements(self, physicalElementList: list[PhysicalElement]):
        """append PhysicalElements to the domain"""
        if isinstance(physicalElementList, list):
            self.physicals.extend(physicalElementList)
        else:
            raise ValueError("Argument 'physicalElementList' was not type list!")

    ###
    # Mit addToScript wird die Domain zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    #   Beispiel:
    #
    #       myScript = Script(...)
    #       Domain1.addToScript(myScript)
    #
    ###
    def addToScript(self, script: Script):
        """call script._addDomain().
        Function is for development and testing reasons.

        Args:
            script (Script): Skript to add the Domain to.
        """
        script._addDomain(self)
