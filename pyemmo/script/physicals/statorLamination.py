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
"""Module for class StatorLamination"""
from __future__ import annotations

from ..gmsh.gmsh_surface import GmshSurface
from ..material.material import Material
from .physical_element import PhysicalElement


class StatorLamination(PhysicalElement):
    """Class for stator lamination

    .. image:: ../../images/StatorBlech.png
        :scale: 100%
        :alt: Example for a ``StatorLamination`` physical surface.
        :align: center
    """

    def __init__(
        self,
        name: str,
        geo_list: list[GmshSurface],
        material: Material,
        phyID=None,
    ):
        """Create a object of StatorLamination.

        Args:
            name (str): Lamination name.
            geo_list (list[GmshSurface]): List of surface elements that form the lamination.
            material (Material): Lamination material.
            phyID (int | None, optional): Gmsh physical element index. Defaults to next
                available index in current gmsh model. Get ID with :attr:`id`.
        """
        super().__init__(
            name=name,
            geo_list=geo_list,
            material=material,
            phyID=phyID,
        )
        self.physicalElementType = "Lamination"  # the physical element type can be used to identify physical elements

        self.setColor("SteelBlue")
