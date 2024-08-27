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
"""Module for primary boundary Line"""
from typing import List

from .physicalElement import Material, PhysicalElement
from .transformable import Transformable


class PrimaryLine(PhysicalElement):
    """
    Eine Instanz der Klasse MasterLine beschreibt die Masterkante eines Teilmodells einer zu
    simulierenden elektischen Maschine.\n
        \\image html masterLine.png
    """

    def __init__(
        self,
        name: str,
        geo_list: List[Transformable],
        material: Material = None,
    ):
        """init of PrimaryLine boundary PhysicalElement

        Args:
            name (str)
            geo_list (List[Transformable])
            material (Material, optional): Defaults to None.
        """
        # FIXME: Material hat keinen Einfluss... Sollte standardmaeßig auf None gesetzt werden
        super().__init__(name=name, material=material, geo_list=geo_list)
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "PrimaryLine"
