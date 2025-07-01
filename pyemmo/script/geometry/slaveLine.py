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
from typing import List, Union

from ..material.material import Material
from .circleArc import CircleArc
from .line import Line
from .physicalElement import PhysicalElement
from .spline import Spline


###
# TODO: Rename SLAVE -> LINKED/LINK
# Eine Instanz der Klasse SlaveLine beschreibt die Slavekante eines Teilmodells einer zu simulierenden elektischen Maschine.
# \image html slaveLine.png
###
class SlaveLine(PhysicalElement):
    ###
    # Konstruktor der Klasse SlaveLine.
    #
    #   Attribute:
    #
    #       ID : Integer
    #       name : String
    #       material : Material
    #       geo_list : [Line]
    #
    ###
    def __init__(
        self,
        name: str,
        geo_list: List[Union[Line, CircleArc, Spline]],
        material: Material = None,
    ):
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geo_list=geo_list,
        )

        self.physicalElementType = "SlaveLine"  # the physical element type can be used to identify physical elements
