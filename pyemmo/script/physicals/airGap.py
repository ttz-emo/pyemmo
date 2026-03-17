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
"""Module for AirArea Physical Element"""
from __future__ import annotations

from ..geometry.surface import Surface
from ..material.material import Material
from .physicalElement import PhysicalElement


class AirGap(PhysicalElement):
    """
    An instance of ``AirGap`` is the part of the airgap of an electric machine model.
    This class describes both the airgap surface on the rotor side and on the stator
    side.
    The airgap physical surface of rotor and stator are used for the force and torque
    calculation in the ONELAB simulation and act as the interface to the ``Movingband``
    which allows for the rotational movement in transient simulations.

    .. image:: ../../images/class_airGap.png
    """

    def __init__(
        self,
        name: str,
        geo_list: list[Surface],
        material: Material = None,
    ):
        """Construct a airgap from a list of Surfaces.

        Args:
            name (str): Airgap name.
            geo_list (List[Union[Surface]]): List of surfaces.
            material (Material, optional): Material of airgap. Defaults to None.
        """
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geo_list=geo_list,
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirGap"
        self.setColor("SkyBlue")
