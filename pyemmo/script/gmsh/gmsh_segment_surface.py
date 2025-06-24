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

import logging

import numpy as np
import gmsh

from ..geometry import defaultCenterPoint as gcp
from ..geometry.segment_surface import SegmentSurface
from ..gmsh import DimTag
from .gmsh_line import GmshLine
from .gmsh_surface import GmshSurface


class GmshSegmentSurface(GmshSurface, SegmentSurface):
    """
    GmshSegmentSurface is a segmented surface object in parallel Gmsh representation
    through the Gmsh Python API.
    """

    def __init__(
        self,
        tag: int,
        nbr_segments: int,
        name: str = "",
    ):
        """GmshSegmentSurface can be initialized with a existing gmsh surface ``tag`` or
        with a list of gmsh curves (see )
        If the surface ``tag`` is given, the curves are retrieved from the current gmsh
        model. See pyemmo.script.gmsh.GmshSurface for more information.
        If a list of ``GmshLine`` objects is given, a PlaneSurface object will be
        created in Gmsh with OCC kernel.
        The surface must be formed in a way that it can be copied around the z-axis
        ``nbrSegments`` times.

        Args:
            tag (int): Gmsh surface tag.
            nbr_segments (int): number of segments in the full model.
            name (str, optional): name of the surface
        """
        GmshSurface.__init__(self, tag=tag, name=name)
        # FIXME: calling self.curves does trigger the _get_lineloop() method which
        # calls synchronize() ... Maybe skip init of SegmentSurface parent class here?
        SegmentSurface.__init__(
            self, name=self.name, curves=self.curve, nbr_segments=nbr_segments
        )

    @property
    def tools(self) -> list[GmshSegmentSurface]:
        """Get the list of tool surfaces to cut out of this surface

        ``tools`` has NO SETTER, because is only accessed by method ``cutOut()``

        NOTE: Needed to reimplement property in GmshSegmentSurface class, because
        otherwise type hint for properties of tools are missing.

        Returns:
            list: List of tool surfaces
        """
        return self._cut

    # pylint: disable=arguments-differ
    #   Its ok that the number of arguments is higher than in the parent class because
    #   this is like a __init__ method!
    # pylint: disable=arguments-renamed
    #   This probably happens because the number of arguments is different from the parent
    #   implementation of from_curve_loop() method.
    @classmethod
    def from_curve_loop(
        cls, curve_loop: list[GmshLine], nbr_segments: int, name: str = ""
    ) -> GmshSegmentSurface:
        """Create a GmshSegmentSurface object from a curve loop.
        This method creates a GmshSegmentSurface object from a curve loop object.

        Args:
            curve_loop (list[GmshLine]): List of GmshLine objects.
            nbr_segments (int): Number of segments in the full model.
            name (str, optional): Name. Defaults to "".

        Returns:
            GmshSegmentSurface
        """
        gmsh_surf = GmshSurface.from_curve_loop(curve_loop=curve_loop, name=name)
        return cls(tag=gmsh_surf.id, nbr_segments=nbr_segments, name=name)

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
        # copy the tools from the GmshSurface
        dup_gs_surf._cut = dup_gmsh_surf.tools  # pylint: disable=protected-access
        if dup_gmsh_surf.isTool():
            dup_gs_surf.setTool()
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
        logging.debug(
            "Cutting out tool (%s) with %i segments from surface (%s) with %i segments!",
            tool.name,
            tool.nbr_segments,
            self.name,
            self.nbr_segments,
        )
        # check the number of segments
        if tool.nbr_segments != self.nbr_segments:
            # calculate total number of segments
            symmetry = np.gcd(tool.nbr_segments, self.nbr_segments)
            logging.debug(
                "New symmetry for GmshSegmentSurface (%s): %i", self.name, symmetry
            )
            if (self.nbr_segments / symmetry) > 1:
                # create nbrSegments/symmetry copies
                parent_name = self.name  # save name to update it later
                dup_surfs: list[GmshSegmentSurface] = []  # list of duplicate surfaces
                logging.debug(
                    "Rotating and duplicating %s %i times",
                    self.name,
                    int(self.nbr_segments / symmetry),
                )
                for segment in range(1, int(self.nbr_segments / symmetry)):
                    # rotate and duplicate parent surface if needed
                    dup_surfs.append(self.rotate_duplicate(segment))
                comb_surf = self.combine(dup_surfs)  # combine the parent surfaces
                # update surface tag (without using set_tag() method!)
                self._id = comb_surf.id
                self._cut = comb_surf.tools  # update tools
                self.nbr_segments = symmetry  # update number of segments
                logging.debug(
                    "New number of segments for GmshSegmentSurface (%s): %i",
                    parent_name,
                    self.nbr_segments,
                )
                self.name = parent_name  # update name
            for segment in range(int(tool.nbr_segments / symmetry)):
                dup_tool = tool.rotate_duplicate(segment)  # rotate and duplicate tool
                self._subtract_segment(dup_tool, keepTool)  # cut out new tool
            # NOTE: Need to update nbr_segments of the tools here, because otherwise the
            # rotate_duplicate() method will use a wrong angle! (Angle is caclulated from
            # the number of segments!)
            for tool in self.tools:
                tool.nbr_segments = symmetry  # update number of segments
                tool._segment_number = self.segment_nbr  # update segment number
        else:
            # if the number of segments is the same, cut out the tool directly
            self._subtract_segment(tool, keepTool)

    def _subtract_segment(
        self, tool: "GmshSegmentSurface", keep_tool: bool = True
    ) -> None:
        """Cut out a Tool SegmentSurface from the Parent surface by Boolean Difference.
        This method is a duplicate of the GmshSurface.cutOut() method, but it
        additionally handles the case where the tool intersects the parent surface
        partly. In this case the remaining tool part will be rotated by the parent
        segment angle and subtracted again.
        Args:
            tool (GmshSegmentSurface): Tool surface to cut out.
            keep_tool (bool, optional): If True, the tool surface will not be removed
                after cutting it out. Defaults to True.
        """
        self._cut.append(tool)
        tool.setTool()  # set to the tool surface
        cut_dim_tags: list[DimTag] = [(2, tool.id)]
        # cut out tools of tools aswell!
        if tool.tools:
            raise RuntimeError("Tool surfaces can not have tools for now!")
            # TODO: Implement cutting out tools of tools, maybe be creating new united
            # surface from all tools.
            tools = tool.tools
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
            [(2, self.id)], cut_dim_tags, removeTool=not keep_tool
        )
        if len(out_dim_tags) == 1:
            # single output surface -> new surface should be the = ParentSurface-Tool
            if out_dim_tags_map[0] == out_dim_tags + cut_dim_tags:
                # old parent surface is new surface + tool
                if out_dim_tags[0][1] != self.id:
                    # the parent surface id changed -> set new id
                    old_id = self.id  # get old id
                    self._id = out_dim_tags[0][1]  # set id to new surface tag
                    # update name of surface
                    self.name = gmsh.model.getEntityName(self.dim, old_id)
                    # # remove old surface
                    # gmsh.model.occ.remove([(2, old_id)])
                return None
            else:
                raise RuntimeError("Unhandled fragment output!")
        if len(out_dim_tags) == 2:
            # the number of surfaces did not change (still one object and one tool)
            # check if one of the surface ids changed:
            if out_dim_tags[0][1] != self.id:
                # the parent surface id changed -> set new id
                old_id = self.id  # get old id
                self._id = out_dim_tags[0][1]  # set id to new surface tag
                # update name of new surface
                self.name = gmsh.model.getEntityName(self.dim, old_id)
                gmsh.model.occ.remove([(2, old_id)])  # remove old surface
            if out_dim_tags[1][1] != tool.id:
                # the tool surface id changed -> set new id
                old_id = tool.id  # get old id
                tool._id = out_dim_tags[1][1]
                # update name of new tool
                tool.name = gmsh.model.getEntityName(self.dim, old_id)
                gmsh.model.occ.remove([(2, old_id)])  # remove old tool surface
            return None
        if len(out_dim_tags) > 2:
            # extra surface(s) was/were created (additional to parent and tool), so
            # surfaces partly intersected.

            # check and update parent id and name:
            old_id = self.id
            self._id = out_dim_tags[0][1]  # update parent surface id
            # update name of new parent surface:
            self.name = gmsh.model.getEntityName(self.dim, old_id)

            gmsh.model.occ.synchronize()  # synchronize model to update surface tags
            # handle the newly created tool surfaces
            new_tool_dimtags = out_dim_tags_map[-1]
            for dimtag in new_tool_dimtags:
                if dimtag not in out_dim_tags_map[0]:
                    # new (outer) tool surface since it is not part of the original
                    # surface
                    # FIXME: This is just a workaround since the cutOut() method
                    # can also be called from a child class of GmshSegmentSurface,
                    # like MaschineSegmentSurface.
                    assert type(tool) is GmshSegmentSurface, (
                        "Tool surface must be a GmshSegmentSurface object! "
                        f"But it is of type {type(tool)}!"
                    )
                    # create new outer tool GmshSegmentSurface object
                    outer_tool = GmshSegmentSurface(
                        name=tool.name,
                        tag=dimtag[1],
                        nbr_segments=tool.nbr_segments,
                    )
                    self._handle_outer_tool(outer_tool, tool)
                else:
                    # replace inital tools surface with new inner tool surface
                    inner_tool = tool.duplicate()
                    inner_tool._id = dimtag[1]  # update id of new tool
                    inner_tool.setTool()
                    self._cut.remove(tool)  # remove old tool surface
                    self._cut.append(inner_tool)  # add new inner tool surface

        else:
            raise ValueError(
                "Unexpected number of output surfaces after cutting out tool surface: "
                f"{len(out_dim_tags)}"
            )

    def _handle_outer_tool(
        self, outer_tool: GmshSegmentSurface, tool: GmshSegmentSurface
    ) -> None:
        """Handle outer tool surface after subtraction:
        - If the tool intersects in **negative** circumferential direction,
          rotate and subtract the original tool and subtract from the parent
          surface again.
        - If the tool intersects in **positive** circumferential direction,
          **the outer tool part will be removed for now**!
        - If the tool intersects in radial direction, throw an error for now.

        Args:
            outer_tool (GmshSegmentSurface): Outer tool surface that was created
                after cutting out the tool surface.
            tool (GmshSegmentSurface): Original tool surface that was cut out.
        
        NOTE: For some reason in OCC we can not rotate the original tool
        and subtract it again, but we need to duplicate it first and then
        rotate the duplicate. Otherwise OCC throws an error that the
        outline of the parent surface can not be recovered.
        FIXME: Workaround for tools intersecting the parent on the x-axis.
        We rotate a copy of the original (full) tool by parent segment angle and
        fragment it again, because the fragmented tool surface can have a
        arbitrary shape and is difficult to handle for OCC. This is just a
        workaround, because of the difficulties with OCC. **So in the case
        a tool part is outside the segment angle, it will be removed**.
            
        """
        cog_tool = outer_tool.calcCOG()
        angle_to_x = cog_tool.getAngleToX()
        if angle_to_x > np.pi:
            angle_to_x -= 2 * np.pi  # normalize angle to [-pi, pi]

        if angle_to_x < 0:
            # tool below x-axis -> rotate by self.angle and cut out again:
            # NOTE: For some reason in OCC we can neither rotate the remaining
            # outer tool part nor original tool and subtract it again, but we
            # need to duplicate the complete tool object first and then
            # rotate that copy. Otherwise OCC throws an error that the
            # outline of the parent surface/tool part can not be recovered.
            new_tool = tool.duplicate()
            new_tool.rotateZ(gcp, self.angle) # rotate tool by segment angle
            self._subtract_segment(new_tool) 
            # removing outer tool surface
            gmsh.model.occ.remove([(outer_tool.dim, outer_tool.id)])
            if outer_tool in self.tools:
                self.tools.remove(outer_tool)

        elif 0 < angle_to_x < self.angle:
            # tool intersects in radial direction. We can not handle it for now
            raise RuntimeError(
                "Tool surface intersects parent surface in radial direction! "
                "This is not supported for now!"
            )
        else:
            # tool probably intersects in positive circumferential direction

            # # rotate the tool surface by -self.angle and cut out again:
            # tool.rotateZ(gcp, -self.angle)
            # self._subtract_segments(tool)

            # NOTE: Workaround for tools intersecting the parent on the x-axis.
            # We rotate the original (full) tool by parent segment angle and
            # fragment it again, because the fragmented tool surface can have a
            # arbitrary shape and is difficult to handle for OCC. So in the case
            # every tool part that is outside the parent segment will be removed.
            logging.warning(
                "Tool surface (%s) is outside parent surface in positive circumferential "
                "direction! Removing outer tool part!",
                outer_tool,
            )
            gmsh.model.occ.remove([(outer_tool.dim, outer_tool.id)])
            if outer_tool in self.tools:
                self.tools.remove(outer_tool)
