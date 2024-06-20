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
"""Function to get coil span from winding layout"""
from typing import List
import numpy as np


def get_min_coilspan(wind_layout: List[List[int]]) -> int:
    """Calculate the minimal coil span from a winding layout"""
    # fix empty second layer for lower numpy version
    if not wind_layout[0][1]:
        layers = 1
        for i, layer in enumerate(wind_layout):
            wind_layout[i] = layer[0]
    else:
        layers = 2
    wind_layout = np.array(wind_layout)
    nbrSlots = wind_layout.shape[-1] * 3  # phases
    if layers == 2:
        # double layer
        first_coil_side = wind_layout[0, 0, 0]
        # get array with slot distance to first slot side
        a = wind_layout[0, :, 1:] + first_coil_side
    else:
        # single layer
        first_coil_side = wind_layout[0, 0]
        # get array with slot distance to first slot side
        a = wind_layout[0, 1:] + first_coil_side
    is_positive_coil_side = first_coil_side > 0
    # filter oppvosit (positive/negative) winding directions
    a = -a[a < 0] if is_positive_coil_side else a[a > 0]
    for i in range(1, nbrSlots):
        # loop through distance to first slot and check if that slot is in a
        if i in a or nbrSlots - i in a:
            return i
