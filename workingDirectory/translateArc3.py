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
import sys

try:
    pass
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

import pyleecan.Classes.Arc3

from .build_pyemmo_point import build_pyemmo_point


# =======================================
# Definition of function 'translateArc3':
# =======================================
def translateArc3(line: pyleecan.Classes.Arc3.Arc3):
    """_summary_

    Args:
        line (pyleecan.Classes.Arc3.Arc3): _description_

    Returns:
        _type_: _description_
    """
    # Calculation for Arc3(Half circle define by two points))
    # Berechnung des Mittelpunkts eines Halbkreises
    startPoint = build_pyemmo_point(line.begin)
    endPoint = build_pyemmo_point(line.end)
    centerPoint = build_pyemmo_point(line.get_center())
    centerArcPoint = build_pyemmo_point(line.get_middle())

    return startPoint, endPoint, centerPoint, centerArcPoint
