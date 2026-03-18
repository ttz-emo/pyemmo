#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
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
"""
The physicals subpackage provides classes that represent the :class:`PhyicalElement`
objects according to the Gmsh/GetDP definition.
This means groups of geometric objects (e.g. surfaces) with assigned physical properties
(e.g. magnetization and material properties) or boundary conditions.
The subpackage contains different types of PhysicalElements (= surfaces with phyiscal
properties, e.g. :class:`~pyemmo.script.physicals.slot.Slot` , or boundary curves, e.g.
:class:`~pyemmo.script.physicals.limitLine.LimitLine`).

In the following graph you can find a class overview for the physicals subpackage:

.. graphviz:: ../../images/uml/classes_PyEMMO.script.physicals.dot
    :caption: `physicals` subpackage class diagram

"""
from __future__ import annotations

from typing import Literal, Tuple

DimTag = tuple[Literal[0, 1, 2], int]
SurfDimTag = tuple[Literal[2], int]
