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
"""Module for primary boundary line"""
from __future__ import annotations

from ..gmsh.gmsh_line import GmshLine
from .physical_element import Material, PhysicalElement


class PrimaryLine(PhysicalElement):
    """
    The :class:`PrimaryLine` and :class:`~pyemmo.script.physicals.secondaryLine.SecondaryLine`
    classes descript the boundary lines at symmetry axes of the machine model where
    the field results are mirror.

    .. image:: ../../images/primary_line.svg
        :scale:  100%
        :alt: Example for a ``PrimaryLine`` physical curve.
        :align: center
    """

    def __init__(
        self,
        name: str,
        geo_list: list[GmshLine],
        material: Material = None,
    ):
        """init of PrimaryLine boundary PhysicalElement

        Args:
            name (str)
            geo_list (list[GmshLine])
            material (Material, optional): Defaults to None.
        """
        # FIXME: Material hat keinen Einfluss... Sollte standardmaeßig auf None gesetzt werden
        super().__init__(name=name, material=material, geo_list=geo_list)
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "PrimaryLine"
