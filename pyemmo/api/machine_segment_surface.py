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
"""Module for PyEMMO api MachineSegmentSurface class"""
from __future__ import annotations

import logging

import gmsh
import numpy as np

from ..script.gmsh import DimTag
from ..script.gmsh.gmsh_line import GmshLine
from ..script.gmsh.gmsh_segment_surface import GmshSegmentSurface
from ..script.material.material import Material


class MachineSegmentSurface(GmshSegmentSurface):
    """
    MachineSegmentSurface is a segmented surface object in Gmsh with additional
    physical property ``material`` and a ``part_id`` specifing the machine part it
    is representing (e.g. "rotor lamination", "mag" for magent or "stator slot").


        .. MachineSegmentSurface_Params_Table:

        .. table:: MachineSegmentSurface Parameters.

           +-----------------+-----------------------------+-----------------+
           | parameter       | description                 | format          |
           | name            |                             |                 |
           +=================+=============================+=================+
           | part_id         | | External ID which is an   | string          |
           |                 |   abbriviation of surface   |                 |
           |                 |   name.                     |                 |
           |                 | | E.g. rotor lamination     |                 |
           +-----------------+-----------------------------+-----------------+
           | material        | Surface material of type    | Material        |
           |                 | Material.                   |                 |
           +-----------------+-----------------------------+-----------------+
           | nbr_segments    | | Number of surface         | int             |
           |                 |   segements on a whole      |                 |
           |                 |   circle                    |                 |
           |                 | | (2D machine model).       |                 |
           +-----------------+-----------------------------+-----------------+



    """

    def __init__(
        self,
        part_id: str,
        material: Material,
        tag: int,
        nbr_segments: int,
        name: str = "",
    ):
        """init of surface for API. This type of surface is special,
        because it allways forms a machine segment or a part of a segment.

        Args:
            part_id (str):
            material (Material): surface material in simulation.
            tag (int, optional): GMSH tag of the surface.
            nbr_segments (int): number of segments in the full machine.
            name (str, optional): name of the surface
        """
        GmshSegmentSurface.__init__(self, tag=tag, nbr_segments=nbr_segments, name=name)
        self.part_id: str = part_id
        self.material: Material = material
        self.nbr_segments: int = nbr_segments
        self._segment_number = 0

    # pylint: disable=arguments-differ, too-many-arguments, too-many-positional-arguments
    # Its ok that the number of arguments is higher than in the parent class because
    # this is like a __init__ method!
    @classmethod
    def from_curve_loop(
        cls,
        curve_loop: list[GmshLine],
        nbr_segments: int,
        part_id: str,
        material: Material,
        name: str = "",
    ) -> MachineSegmentSurface:
        """create a MachineSegmentSurface from a list of boundary curves.

        Args:
            tag (int): GMSH tag of the surface

        Returns:
            MachineSegmentSurface: MachineSegmentSurface object
        """
        gmsh_surf = GmshSegmentSurface.from_curve_loop(
            curve_loop=curve_loop, nbr_segments=nbr_segments, name=name
        )
        return cls(
            part_id=part_id,
            material=material,
            nbr_segments=nbr_segments,
            tag=gmsh_surf.id,
            name=name,
        )

    def __deepcopy__(self, memo):
        return self.duplicate()

    @property
    def part_id(self) -> str:
        """Name to specify the machine part thats represented by the
        MachineSegmentSurface, like "rotor lamination", "rotor airgap" or "stator slot".
        All relevant identifiers can be found under :mod:`~pyemmo.api.json`.

        Returns:
            str: abbriviation of surface name (short name)
        """
        return self._idExt

    @part_id.setter
    def part_id(self, idExt: str) -> None:
        """set the abbriviation of the surface name (literal Surface ID)

        Args:
            name (str): abbriviation of surface name (short name)

        Returns:
            None
        """
        if isinstance(idExt, str):
            self._idExt = idExt
        else:
            raise ValueError(f"The given name was not type str: {idExt}!")

    @property
    def material(self) -> Material:
        """get the material property of the MachineSegmentSurface surface

        Returns:
            Material: PyEMMO material object.
        """
        return self._material

    @material.setter
    def material(self, material: Material) -> None:
        """set the material of the MachineSegmentSurface.

        Args:
            material (Material): PyEMMO material object.

        Returns:
            None
        """
        if isinstance(material, Material):
            self._material = material
        else:
            raise TypeError(f"Material was not type Material: {material}!")

    def duplicate(self, name="") -> MachineSegmentSurface:
        """create a copy of the surface

        Args:
            name (str, optional): New name for copied surface.
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            MachineSegmentSurface: Duplicate of MachineSegmentSurface object.
        """
        # duplicate curves for new surface
        dup_gss = GmshSegmentSurface.duplicate(self, name)
        # create duplicate surfcace object
        dup_mss = MachineSegmentSurface(
            name=name,
            part_id=self.part_id,
            tag=dup_gss.id,
            material=self.material,
            nbr_segments=self.nbr_segments,
        )
        # copy the tools from the GmshSurface
        dup_mss._cut = dup_gss.tools  # pylint: disable=protected-access
        if dup_gss.isTool():
            dup_mss.setTool()
        return dup_mss

    def rotate_duplicate(self, segment: int) -> GmshSegmentSurface:
        """
        Create a copy of the give surface and its tools surfaces + rotate it by
        :attr:`angle`.
        This also sets the property :attr:`segment_nbr` to the given segment value.

        Args:
            segment (float): Segment number.

        Returns:
            MachineSegmentSurface: Copied and rotated MachineSegmentSurface object.
        """
        # FIXME: This should return a MSS object!
        return GmshSegmentSurface.rotate_duplicate(self, segment=segment)

    def cutOut(self, tool: MachineSegmentSurface, keepTool: bool = True) -> None:
        """
        Cut out a tool surface from the parent surface using a Boolean Difference operation.
        This method subtracts the geometry of the provided `tool` surface from the current surface.
        It supports cases where the number of segments in the tool and the parent surface differ,
        by duplicating and rotating surfaces as needed to match symmetries before performing the
        subtraction.

        Parameters:
            tool (MachineSegmentSurface): The tool surface to cut out from the
                parent surface. Must be an instance of MachineSegmentSurface and
                represent the first segment to cut.
            keepTool (bool, optional): If True, the tool surface is retained
                after the cut. Defaults to True.

        Raises:
            TypeError: If `tool` is not a MachineSegmentSurface instance.
            ValueError: If `tool` does not represent the first segment
                (i.e., `tool.segment_nbr != 0`).

        Notes:
            - If the number of segments in the tool and the parent surface differ,
              the method computes the greatest common divisor (GCD) of the segment
              counts to determine the symmetry, duplicates and rotates surfaces as
              necessary, and updates segment properties accordingly.
        """
        if not isinstance(tool, MachineSegmentSurface):
            raise TypeError(
                f"Tool surface is not a MachineSegmentSurface object! "
                f"But it type '{type(tool)}'!"
            )
        # check if tool has allready segment properties
        if tool.segment_nbr != 0:
            raise ValueError(
                "Cutting out a tool from a segment surface is only allowed for the "
                "first segment!"
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
            # NOTE: Need to update nbr_segments of the tools afterwards here,
            # because otherwise the rotate_duplicate() method will use a wrong
            # angle! (Angle is calculated from the number of segments!)
            for tool_obj in self.tools:  # "tool" var name allready used as parameter
                tool_obj.nbr_segments = symmetry  # update number of segments
                # pylint: disable=protected-access
                # its ok to update segment number here, because tool is also of type
                # MachineSegmentSurface.
                tool_obj._segment_number = self.segment_nbr  # update segment number
        else:
            # if the number of segments is the same, cut out the tool directly
            self._subtract_segment(tool, keepTool)

    def _subtract_segment(
        self, tool: MachineSegmentSurface, keep_tool: bool = True
    ) -> None:
        """Cut out a tool SegmentSurface from the Parent surface by Boolean Difference.

        This method is a duplicate of the GmshSurface.cutOut() method, but it
        additionally handles the case where the tool intersects the parent surface
        partly. In this case the remaining tool part will be rotated by the parent
        segment angle and subtracted again.

        Args:
            tool (MachineSegmentSurface): Tool surface to cut out.
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
                    outer_tool = MachineSegmentSurface(
                        part_id=tool.part_id,
                        material=tool.material,
                        nbr_segments=tool.nbr_segments,
                        tag=dimtag[1],
                        name=tool.name + "_outer",
                    )
                    self._handle_outer_tool(outer_tool, tool)
                else:
                    # replace inital tools surface with new inner tool surface
                    inner_tool = MachineSegmentSurface(
                        part_id=tool.part_id,
                        material=tool.material,
                        nbr_segments=tool.nbr_segments,
                        tag=dimtag[1],
                        name=tool.name + "_inner",
                    )
                    inner_tool.setTool()  # need to call setTool here because
                    # the new partial tool is allready cut out.
            # remove old tool surface
            self.tools.remove(tool)
            # gmsh.model.occ.remove([(2, tool.id)]) # NOTE: We need to keep the
            # original tool for rotate duplicate operation.
            self.tools.append(inner_tool)  # add new inner tool surface

        else:
            raise ValueError(
                "Unexpected number of output surfaces after cutting out tool surface: "
                f"{len(out_dim_tags)}"
            )
