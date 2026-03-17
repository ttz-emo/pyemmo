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
"""Module for class StatorLamination"""
from __future__ import annotations

from ..geometry.surface import Surface
from ..material.material import Material
from .physical_element import PhysicalElement


###
# Eine Instanz der StatorLamination ist das Blechpaket des Stators. Eine beliebige Geometrie kann mit der Klasse StatorLamination definiert werden.
# Diese Klasse sollte man nur im Expertenmodus verwenden.
# Dies kann beispielsweise beim Import und Weiterverarbeitung von Step-Dateien geschehen.
# Eine einfachere Anwendung bietet der Maschinenbaukasten von pyemmo.
# \image html statorBlech.png
###
class StatorLamination(PhysicalElement):
    def __init__(
        self,
        name: str,
        geo_list: list[Surface],
        material: Material,
        phyID=None,
    ):
        """Konstruktor der Klasse StatorLamination.

        Args:
            name (str): Lamination name.
            machineDict (dict): Machine parameter dict.
            geo_list (list[Surface]): List of surface elements that form the lamination.
            material (Material): Lamination material.

        """
        super().__init__(
            name=name,
            geo_list=geo_list,
            material=material,
            phyID=phyID,
        )
        self.physicalElementType = "Lamination"  # the physical element type can be used to identify physical elements

        self.setColor("SteelBlue")
