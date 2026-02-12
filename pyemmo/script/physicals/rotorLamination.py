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
from __future__ import annotations

from ..geometry.surface import Surface
from ..material.material import Material
from .physicalElement import PhysicalElement


###
# Eine Instanz der RotorLamination ist das Blechpaket des Rotors. Eine beliebige Geometrie kann mit der Klasse RotorLamination definiert werden.
# Diese Klasse sollte nur im Expertenmodus angewandt werden.
# Dies kann beispielsweise beim Import und Weiterverarbeitung von Step-Dateien geschehen.
# Eine einfachere Anwendung bietet der Maschinenbaukasten von pyemmo.
# \image html RotorBlech.png
###
class RotorLamination(PhysicalElement):
    """Class for rotor lamination"""

    def __init__(
        self,
        name: str,
        geo_list: list[Surface],
        material: Material,
        phyID: int = None,
    ):
        super().__init__(
            name=name,
            material=material,
            geo_list=geo_list,
            phyID=phyID,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "Lamination"
        self.setColor("SteelBlue")
