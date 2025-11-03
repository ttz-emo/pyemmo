#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of
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

Functions:
- create_curve: Function to create a GmshLine, GmshArc or GmshSpline object from a 
    gmsh curve tag. It also handles the case of a OCC TrimmedCurve object and tries
    to detect its line type.
    NOTE: Needed to move this function to a separate module instead of putting it into
     utils, because it lead to a circular import with GmshSurface and PhysicalElement.

The module is part of the PyEMMO project, developed by TTZ-EMO at the Technical
University of Applied Sciences Würzburg-Schweinfurt.

Author:
    Max Schuler
"""
from __future__ import annotations

import gmsh
import numpy as np

from ...definitions import DEFAULT_GEO_TOL
from .gmsh_arc import GmshArc
from .gmsh_line import GmshLine
from .gmsh_spline import GmshSpline


def create_curve(gmsh_id: int) -> GmshLine | GmshArc | GmshSpline:
    """Create a curve object based on the given id.

    Args:
        id (int): The id of the curve in the Gmsh model.

    Returns:
        Union[GmshLine, GmshArc]: The created curve object.

    Raises:
        ValueError: If the line with the given id is not of type Line or Circle.
    """
    line_type = gmsh.model.getType(1, gmsh_id)
    if line_type == "Line":
        return GmshLine(tag=gmsh_id)
    if line_type == "Circle":
        return GmshArc(tag=gmsh_id)
    if line_type == "TrimmedCurve":
        # check if its a straight line or arc by comparing length with point distance
        test_line = GmshLine(gmsh_id)  # create test object (not sure if its really a line)
        line_length = gmsh.model.occ.getMass(1, gmsh_id)  # get length of TrimmedCurve
        if np.isclose(test_line.getPointDist(), line_length, atol=DEFAULT_GEO_TOL):
            # its a straight line, because length = distance between start and end point
            return test_line
        test_line = GmshArc(gmsh_id)  # create test arc to check curve point distance
        try:
            if np.isclose(
                abs(test_line.radius * np.diff(test_line.getAnglesToX())),
                line_length,
                atol=DEFAULT_GEO_TOL,
            ):
                # its a circle arc because r*phi (=2*r*pi*(phi/2/pi)) = length
                return test_line
            raise ValueError("Line length is not equal length of circle arc")
        except Exception as e:
            # catch test_line.radius raising ValueError because radius of start and end
            # point does not match. In this case its also not a circle arc.
            raise TypeError(
                f"Gmsh curve {gmsh_id} is neither Line nor Arc! Can't determine line type!"
            ) from e
    if line_type in ("BSpline", "Bezier", "Spline"):
        return GmshSpline(tag=gmsh_id)
    raise ValueError(f"Line with tag {gmsh_id} is not of type Line or Circle!")
