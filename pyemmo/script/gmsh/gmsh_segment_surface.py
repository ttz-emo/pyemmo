#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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
"""Module for GmshSegmentSurface class"""
from __future__ import annotations

import numpy as np

from ..geometry import defaultCenterPoint as gcp
from ..geometry.segment_surface import SegmentSurface
from .gmsh_arc import GmshArc
from .gmsh_line import GmshLine
from .gmsh_surface import GmshSurface


class GmshSegmentSurface(GmshSurface, SegmentSurface):
    """
    GmshSegmentSurface is a segmented surface object in parallel Gmsh representation
    through the Gmsh Python API.
    """

    def __init__(
        self,
        nbr_segments: int,
        tag: int = -1,
        curves: list[GmshLine | GmshArc | None] = None,
        name: str = "",
    ):
        """GmshSegmentSurface can be initialized with a existing gmsh surface ``tag`` or
        with a list of gmsh curves. But you cannot give both!
        If the surface ``tag`` is given, the curves are retrieved from the current gmsh
        model. See pyemmo.script.gmsh.GmshSurface for more information.
        If a list of ``GmshLine`` objects is given, a PlaneSurface object will be
        created in Gmsh with OCC kernel.
        The surface must be formed in a way that it can be copied around the z-axis
        ``nbrSegments`` times.

        Args:
            nbrSegments (int): number of segments in the full machine.
            tag (int, optional): Gmsh surface tag.
            curves (List[Line], optional): list of surface boundary lines
            name (str, optional): name of the surface
        """
        GmshSurface.__init__(self, tag=tag, curves=curves, name=name)
        SegmentSurface.__init__(
            self, name=self.name, curves=self.curve, nbr_segments=nbr_segments
        )

    def duplicate(self, name="") -> GmshSegmentSurface:
        """create a copy of the surface

        Args:
            name (str, optional): New name for copied surface.
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            SurfaceAPI: Duplicate of SurfaceAPI object.
        """
        # duplicate surface in Gmsh
        dup_gmsh_surf = GmshSurface.duplicate(self, name)
        # create new GmshSegmentSurface object from new tag
        dup_gs_surf = GmshSegmentSurface(
            tag=dup_gmsh_surf.id, nbr_segments=self.nbr_segments
        )
        return dup_gs_surf

    def rotate_duplicate(self, segment: int) -> GmshSegmentSurface:
        """
        Create a copy of the give surface and its tools surfaces + rotate it by
        :attr:`angle`.
        This also sets the property :attr:`segment_nbr` to the given segment value.

        Args:
            segment (float): Segment number.

        Returns:
            GmshSegmentSurface: Copied and rotated object.
        """
        if (
            not float(segment).is_integer()
            or segment < 0
            or segment >= self.nbr_segments
        ):
            raise ValueError(
                f"Segment number {segment=} must be valid integer from 0...{self.nbr_segments-1}!"
            )

        rot_angle = self.angle * segment

        if rot_angle != 0:  # if the rotation angle is not zero
            dup_surf = self.duplicate(name=f"{self.name} (Seg.: {segment})")
            dup_surf.rotateZ(gcp, rot_angle)
            # set the segment number
            dup_surf._segment_number = segment  # pylint: disable=protected-access
            # its ok to access the protected attribute here, because we are in the same
            # class. rotate_duplicate() is the only method that sets the segment number!
            # update tool:
            for tool_surf in dup_surf.tools:
                tool_surf.name = f"{tool_surf.name} (Seg.: {segment})"

            return dup_surf
        # if the angle is zero: give back the old surface
        return self

    def cutOut(self, tool: GmshSurface, keepTool: bool = True) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
        if not isinstance(tool, GmshSurface):
            raise TypeError(
                f"Tool surface is not a GmshSegmentSurface object! "
                f"But it type '{type(tool)}'!"
            )
        # check if tool has allready segment properties
        if isinstance(tool, GmshSegmentSurface):
            if tool.segment_nbr != 0:
                raise ValueError(
                    "Cutting out a tool from a segment surface is only allowed for the "
                    "first segment!"
                )
        else:
            # otherwise create segment surface from tool
            tool = GmshSegmentSurface(
                nbr_segments=self.nbr_segments,
                tag=tool.id,
                name=tool.name,
            )
        # check the number of segments
        if tool.nbr_segments != self.nbr_segments:
            # calculate total number of segments
            symmetry = np.gcd(tool.nbr_segments, self.nbr_segments)
            # create nbrSegments/symmetry copies
            for segment in range(1, int(self.nbr_segments / symmetry)):
                # rotate and duplicate parent surface if needed
                dup_parent = self.rotate_duplicate(segment)
                comb_surf = self.combine(dup_parent)  # combine the parent surfaces
                # update surface tag (without using set_tag() method!)
                self._id = comb_surf.id
            # update number of segments
            self.nbr_segments = symmetry
            for segment in range(int(tool.nbr_segments / symmetry)):
                dup_tool = tool.rotate_duplicate(segment)  # rotate and duplicate tool
                GmshSurface.cutOut(self, dup_tool, keepTool)  # cut out new tool
                dup_tool.nbr_segments = symmetry  # update number of segments
        else:
            # if the number of segments is the same, cut out the tool directly
            GmshSurface.cutOut(self, tool, keepTool)
