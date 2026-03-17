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
"""Module for Class LimitLine"""
from __future__ import annotations

from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from ..geometry.spline import Spline
from ..material.material import Material
from .physicalElement import PhysicalElement


class LimitLine(PhysicalElement):
    """:class:`LimitLine` defines a outer or inner boundary line of the machine model.
    These lines will get the boundary condition :math:`A_z = 0` so no magnetic flux goes
    across them.

    .. image:: ../../images/outerLimit.png
        :scale:  100%
        :alt: Example for a outer ``LimitLine`` physical curve.
        :align: center
    """

    def __init__(
        self,
        name: str,
        geo_list: list[Line | CircleArc | Spline],
        material: Material = None,
    ):
        """Create a boundary line

        Args:
            name (str): Name of boundary line. E.g. "OuterLimitLine"
            geo_list (List[Union[Line, CircleArc, Spline]]): List of geo curves
            material (Material, optional): Material of boundary. Defaults to None.
        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geo_list=geo_list,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "LimitLine"
