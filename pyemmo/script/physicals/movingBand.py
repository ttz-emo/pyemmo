#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
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
"""Module for class MovingBand"""
from __future__ import annotations

from ..geometry.circleArc import CircleArc
from ..material.material import Material
from ..script import DEFAULT_GEO_TOL
from .physicalElement import PhysicalElement


class MovingBand(PhysicalElement):
    """
    The :class:`MovingBand` describes the boundary lines on rotor and stator side used
    as the interface the the Movingband object in the airgap of the machine model.
    The Movingband method allows for the rotation of the rotor in a transient analysis
    by remeshing the interface between rotor and stator airgap, when the interface
    mesh elements get distorted too much.
    See `this message record <https://onelab.info/pipermail/getdp/2020/002191.html>`_ or
    the `implementation <https://gitlab.onelab.info/getdp/getdp/-/blob/master/src/kernel/MovingBand2D.cpp>`_
    for more details.

    The Movingband must describe a full circle on the rotor side:

    .. image:: ../../images/mb_Rotor.png
        :scale:  100%
        :alt: Example for the rotor Movingband physical curve.
        :align: center
    |
    For the stator side a symmetry segment is enough:

    .. image:: ../../images/mb_Stator.png
        :scale:  100%
        :alt: Example for the stator Movingband physical curve.
        :align: center
    |
    """

    def __init__(
        self,
        name: str,
        geo_list: list[CircleArc],
        material: Material = None,
        auxiliary: bool = False,
    ):
        """Create a moving band segment

        Args:
            name (str): Moving band segment name
            geo_list (List[CircleArc]): List of arc segments to build the mb segment.
            material (Material, optional): Airgap material. Defaults to None.
            auxiliary (bool, optional): Flag to determine if given rotor moving band
                segment is inside the model symmetry or outside (auxiliary).
                Defaults to False.
        """
        super().__init__(name=name, geo_list=geo_list, material=material)
        # call radius to make sure all geo elements are circle arcs with the same radius
        self.radius
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "MovingBand"
        ###Hilfslinien des Movingbands zur Ergänzung zum Vollkreis, bei einem Teilmodell.
        self._auxiliary = auxiliary

    @property
    def auxiliary(self) -> bool:
        """
        Returns:
            bool: If MovingBand object is outside model segment (symmetry) or not.
        """
        return self._auxiliary

    @property
    def radius(self) -> float:
        """Get the moving band radius"""
        radius = self.geo_list[0].radius
        for curve in self.geo_list:
            if abs(curve.radius - radius) > DEFAULT_GEO_TOL:
                raise (
                    ValueError(
                        f"Movingband '{self.name}' got arc objects with different radius:\n"
                        + f"Radius curve 0: {radius}\n"
                        + f"Radius curve {self.geo_list.index(curve)}: {curve.radius}\n"
                    )
                )
        return radius

    @radius.setter
    def radius(self):
        """
        Raises:
            AttributeError: MovingBand radius cannot be set!
                It is determined by the radius of the curve in geo_list.
        """
        raise AttributeError(
            "MovingBand radius cannot be set! "
            "It is determined by the radius of the curves in geo_list."
        )
