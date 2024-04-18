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
"""Module for Bar Physical Element"""

from typing import List, Union
from .physicalElement import PhysicalElement, Material, Surface


class Bar(PhysicalElement):
    """
    TODO
    """

    def __init__(
        self,
        name: str,
        geometricalElement: Union[Surface, List[Surface]],
        material: Material,
    ):
        """Bar defines a rotor bar for a induction machine

        Args:
            - name (str): Bar name
            - geometricalElement (Union[Surface, List[Surface]]):
                List of geometry objects
            - material (Material): Material of . Should be "air". Defaults to None.
        """
        # convert Surface to list of Surface for PhysicalElement init
        if isinstance(geometricalElement, Surface):
            geometricalElement = [geometricalElement]
        # make sure conductivity is defined for induced currents
        assert (
            material.conductivity > 0
        ), f"Material of Bar ({name}) must be elec. conducting!"
        super().__init__(
            name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "Bar"
        self.setColor("Orange")
