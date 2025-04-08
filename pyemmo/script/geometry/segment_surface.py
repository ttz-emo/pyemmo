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
"""Module for class SegmentSurface"""
from __future__ import annotations

import gmsh
from numpy import pi

from ..gmsh import DimTag
from ..gmsh.gmsh_surface import GmshSurface
from . import defaultCenterPoint as gcp
from .circleArc import CircleArc
from .line import Line
from .spline import Spline
from .surface import Surface


class SegmentSurface(Surface):
    """
    SegmentSurface is a child of geometry class Surface and has additional attributes:


        .. SegmentSurface_Params_Table:

        .. table:: SegmentSurface Parameters.

           +-----------------+-----------------------------+-----------------+
           | parameter       | description                 | format          |
           | name            |                             |                 |
           +=================+=============================+=================+
           | nbrSegments     | | Number of surface         | int             |
           |                 |   segements on a whole      |                 |
           |                 |   circle                    |                 |
           |                 | | (2D machine model).       |                 |
           +-----------------+-----------------------------+-----------------+
           | angle           | Angle of the segment (rad). | float           |
           |                 | Should be 2*Pi/nbrSegments  |                 |
           +-----------------+-----------------------------+-----------------+


    """

    def __init__(
        self,
        name: str,
        curves: list[Line],
        nbrSegments: int,
        segment_nbr: int = 0,
    ):
        """init of surface for API. This type of surface is special,
        because it allways forms a machine segment or a part of a segment.

        Args:
            name (str): name of the surface
            curves (List[Line]): list of surface boundary lines
            nbrSegments (int): number of segments to form the complete body.
            segment_nbr (optional, int): actual segment number of surface (default is 0).
        """
        super().__init__(name=name, curves=curves)
        # FIXME: Update by using setters to check init values!!
        self._nbrSegments: int = nbrSegments
        self._segment_number = segment_nbr  # default segment number is 0

    # @property
    # def tools(self) -> list[SegmentSurface]:
    #     """Subtraction surfaces"""
    #     return super().tools

    @property
    def angle(self) -> float:
        """Get the angle of one surface segmen in radians. This equals:
            2 * Pi / self.nbrSegments

        Returns:
            float: segment angle of that surface in rad.
        """
        return 2 * pi / self.nbrSegments

    @property
    def nbrSegments(self) -> int:
        """get the nbrSegments of segments of a API surface to form a whole circle (2*Pi)

        Returns:
            int: maximal number of segments to form a whole circle.
        """
        return self._nbrSegments

    @nbrSegments.setter
    def nbrSegments(self, nbrSegments: int) -> None:
        """set the nbrSegments of segments of a API surface to form a whole circle (2*Pi)

        Args:
            nbrSegments (int): number of segments to form a whole circle.
        """
        if nbrSegments % 1 != 0:
            msg = (
                f"Given number of segments for API surface '{self.name}'"
                f"was not an integer but type '{type(nbrSegments)}'!"
            )
            raise TypeError(msg)
        self._nbrSegments = nbrSegments

    @property
    def segment_nbr(self) -> int:
        """Actual segement number of SegmentSurface object. The default value is 0."""
        return self._segment_number

    def duplicate(self, name="", new_segment: int = 0) -> SegmentSurface:
        """create a copy of the SegmentSurface

        Args:
            name (str, optional): New name for copied surface.
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            SegmentSurface: Duplicate of SegmentSurface object.
        """
        # duplicate curves for new surface
        newCurves: list[Line | CircleArc | Spline] = []
        for curve in self.curve:
            newCurves.append(curve.duplicate())
        # create duplicate surfcace object
        dup_surf = super().duplicate(name)
        # create duplicate of SegmentSurface object
        dup_seg_surf = SegmentSurface(
            name=dup_surf.name,
            curves=dup_surf.curve,
            nbrSegments=self.nbrSegments,
            segment_nbr=new_segment if new_segment != 0 else self.segment_nbr,
        )
        return dup_seg_surf

    def rotateDuplicate(self, segment: int) -> SegmentSurface:
        """
        Create a copy of the give surface and its tools surfaces + rotate it by
        :attr:`angle`.
        This also sets the property :attr:`segment_nbr` to the given segment value.

        Args:
            segment (float): Segment number.

        Returns:
            SegmentSurface: Copied and rotated SegmentSurface object.
        """
        if (segment % 1) != 0 or segment >= self.nbrSegments:
            raise ValueError("Segment number must be valid integer!")

        rot_angle = self.angle * segment

        if rot_angle != 0:  # if the rotation angle is not zero
            dup_surf: SegmentSurface = self.duplicate(
                name=f"{self.name} (Seg.: {segment})", new_segment=segment
            )
            dup_surf.rotateZ(gcp, rot_angle)
            tools = dup_surf.tools  # init tools array
            while tools:
                new_tools = []  # init new tools
                for tool_surf in dup_surf.tools:
                    # rotate tools
                    tool_surf.rotateZ(gcp, rot_angle)
                    tool_surf.name = f"{tool_surf.name} (Seg.: {segment})"
                    if tool_surf.tools:
                        # if tool has tools
                        new_tools.extend(tool_surf.tools)  # extend new tools
                tools = new_tools  # update tools array

            return dup_surf
        # if the angle is zero: give back the old surface
        return self

    def cutOut(self, ToolSurface: SegmentSurface) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
        self._cut.append(ToolSurface)
        ToolSurface.setTool()  # set to the tool surface
        cut_dim_tags: list[DimTag] = [(2, ToolSurface.id)]
        # cut out tools of tools aswell!
        if ToolSurface.tools:
            raise RuntimeError("Tool surfaces can not have tools for now!")
            # TODO: Implement cutting out tools of tools, maybe be creating new united
            # surface from all tools.
            tools = ToolSurface.tools
            while tools:
                # while tools array is not empty
                new_tools = []
                for tool in tools:
                    # add tool surface to cut out
                    cut_dim_tags.append((2, tool.id))
                    if tool.tools:
                        # if tool itself has tools
                        new_tools.extend(tool.tools)  # update new_tools list
                tools = new_tools  # reset tools
        # fragment resutls in a list of new surfaces tags + a map that tells which of
        # the new surfaces together form the old surface. So for e.g. if surface 2,
        # which intersects surface 1 partly, is subtracted from surface 1, then 3 new
        # surfaces are created:
        # Tag 1: the part of surface 1 that is not intersected by surface 2
        # Tag 2: the part of surface 1 that is intersected by surface 2
        # Tag 3: the part of surface 2 that is not intersected by surface 1
        # And outDimTagsMap will tell you which of the new surfaces build the original
        # surface, like:
        #   [[(2,1),(2,2)],[(2,2),(2,3)]]
        # This means e.g. that the original surface with old tag 1 is build by the new
        # surfaces 1 and 2.
        out_dim_tags, out_dim_tags_map = gmsh.model.occ.fragment(
            [(2, self._id)], cut_dim_tags, removeTool=ToolSurface.delete
        )
        if len(out_dim_tags) == 1:
            # single output surface -> new surface should be the parent surface - tool
            if out_dim_tags_map[0] == out_dim_tags + cut_dim_tags:
                # old parent surface is new surface + tool
                # update id of parent surface to new surface id
                self.id = out_dim_tags[0][1]
                gmsh.model.setEntityName(
                    2, self.id, self.name
                )  # update name of surface
                return None
            else:
                raise RuntimeError("Unhandled fragment output!")
        if len(out_dim_tags) == 2:
            # the number of surfaces did not change (still one object and one tool)
            # check if one of the surface ids changed:
            if out_dim_tags[0][1] != self.id:
                # the parent surface id changed -> set new id
                old_id = self.id  # get old id
                self.id = out_dim_tags[0][1]  # set id to new surface tag
                gmsh.model.setEntityName(
                    2, self.id, self.name
                )  # update name of surface
                gmsh.model.occ.remove([(2, old_id)])  # remove old surface
            if out_dim_tags[1][1] != ToolSurface.id:
                # the tool surface id changed -> set new id
                old_id = ToolSurface.id  # get old id
                ToolSurface.id = out_dim_tags[1][1]
                gmsh.model.setEntityName(2, ToolSurface.id, ToolSurface.name)
                gmsh.model.occ.remove([(2, old_id)])  # remove old tool surface
            return None
        if len(out_dim_tags) > (len(cut_dim_tags) + 1):
            # extra surface(s) was/were created -> shift new surface by self.angle and
            # subtract from self:
            self.id = out_dim_tags[0][1]  # TODO: Check if this is the right surface
            gmsh.model.setEntityName(2, self.id, self.name)  # update name of surface

            new_tool_dimtags = out_dim_tags_map[-1]
            for dimtag in new_tool_dimtags:
                if dimtag not in out_dim_tags_map[0]:
                    # new (outer) tool surface since it is not part of the original
                    # surface
                    # rotate it, cut it out and add it to the tools list
                    gmsh.model.occ.rotate(
                        [dimtag], gcp.x, gcp.y, gcp.z, 0, 0, 1, self.angle
                    )
                    # There is no way to initialize SegmentSurface with a GmshSurface object
                    # directly so we need to create a GmshSurface first and extract the
                    # curve loop from it:
                    gmsh.model.occ.synchronize()
                    gmsh_surf = GmshSurface(tag=dimtag[1])
                    # somehow the rotation does not work here. Do rotation manually
                    # before creating the GmshSurface
                    # gmsh_surf.rotateZ(globalCenterPoint, self.angle)
                    # gmsh.model.occ.synchronize()

                    new_tool = SegmentSurface(
                        name=ToolSurface.name + "_1",
                        idExt=ToolSurface.idExt,
                        curves=gmsh_surf.curve,
                        material=ToolSurface.material,
                        nbrSegments=ToolSurface.nbrSegments,
                        angle=ToolSurface.angle,
                        meshSize=ToolSurface.meshSize,
                    )
                    # remove gmsh_surf since the new_tool has new id but is same surface
                    gmsh.model.occ.remove([dimtag])  # remove gmsh_surf
                    self.cutOut(new_tool, keepTool=keepTool)
                    # self.tools.append(new_tool)
                else:
                    # replace old tool surface with new (not rotated) tool surface
                    gmsh_surf = GmshSurface(tag=dimtag[1])
                    # There is no way to initialize SegmentSurface with a GmshSurface object
                    # directly so we need to create a GmshSurface first and extract the
                    # curve loop from it
                    replace_tool = SegmentSurface(
                        name=ToolSurface.name + "_0",
                        idExt=ToolSurface.idExt,
                        curves=gmsh_surf.curve,
                        material=ToolSurface.material,
                        nbrSegments=ToolSurface.nbrSegments,
                        angle=ToolSurface.angle,
                        meshSize=ToolSurface.meshSize,
                    )
                    # remove gmsh_surf since the new_tool has new id but is same surface
                    gmsh.model.occ.remove([dimtag])
                    self.tools[self.tools.index(ToolSurface)] = replace_tool
            # end of for loop remove original tool surface
            gmsh.model.occ.remove([(2, ToolSurface.id)])
        else:
            raise ValueError(
                "Unexpected number of output surfaces after cutting out tool surface!"
            )

    # TODO: Update plot function to also plot tool surfaces
