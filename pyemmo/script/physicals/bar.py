#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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

from __future__ import annotations

import logging

from ..gmsh.gmsh_surface import GmshSurface
from ..material.material import Material
from .physical_element import PhysicalElement


class Bar(PhysicalElement):
    """
    :class:`Bar` represents the rotor bar of a squirrel cage induction machine.
    It is treated separately because in the simulation the bars should be connected via
    a electrical circuit boundary condition to accound for the endring segments.
    """

    def __init__(
        self,
        name: str,
        geo_list: GmshSurface | list[GmshSurface],
        material: Material,
    ):
        """Bar defines a rotor bar for a induction machine

        Args:
            name (str): Bar name
            geo_list (Union[Surface, List[Surface]]): List of geometry objects
            material (Material): Material of the rotor bar. Defaults to None.
        """
        # convert Surface to list of Surface for PhysicalElement init
        if isinstance(geo_list, GmshSurface):
            geo_list = [geo_list]
        # make sure conductivity is defined for induced currents
        if not material.conductivity:
            raise ValueError(
                f"Material of bar ({name}) must have electrical conductivity!"
            )
        if not material.linear:
            logger = logging.getLogger(__name__)
            logger.warning(
                "Material %s of rotor bar %s is non-linear!", material.name, name
            )
        super().__init__(name=name, material=material, geo_list=geo_list)
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "Bar"
        self.setColor("Orange")
