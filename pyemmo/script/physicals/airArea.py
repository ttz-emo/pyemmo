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
""""""
from __future__ import annotations

from ..gmsh.gmsh_surface import GmshSurface
from ..material.material import Material
from .physical_element import PhysicalElement


class AirArea(PhysicalElement):
    """
    An instance of the class :class:`AirArea` describes any air space within the
    electric machine.
    A separate class :class:`~pyemmo.script.physicals.airgap.AirGap` exists for the
    airgap between rotor and stator.

    .. image:: ../../images/class_airArea.png
        :scale:  100%
        :alt: Example for a ``AirArea`` physical surface.
        :align: center
    |
    """

    def __init__(
        self,
        name: str,
        geo_list: list[GmshSurface],
        material: Material = None,
    ):
        """AirArea is any area defined with material air except from the Airgap surface

        Args:
            name (str): Physical name
            geo_list (list[GmshSurface]): List of surfaces.
            material (Material, optional): Material of AirArea. Should be "air".
                Defaults to None.
        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geo_list=geo_list,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirArea"
        self.setColor("SkyBlue")
