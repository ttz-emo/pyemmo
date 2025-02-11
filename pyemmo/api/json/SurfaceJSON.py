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
"""Module for json api surface class"""
from __future__ import annotations

import gmsh
from numpy import pi

from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line
from ...script.geometry.spline import Spline
from ...script.geometry.surface import Surface
from ...script.gmsh import DimTag
from ...script.gmsh.gmsh_surface import GmshSurface
from ...script.material.material import Material
from . import globalCenterPoint


class SurfaceAPI(Surface):
    """
    SurfaceAPI is a child of geometry class Surface and has additional attributes:


        .. SurfaceAPI_Params_Table:

        .. table:: SurfaceAPI Parameters.

           +-----------------+-----------------------------+-----------------+
           | parameter       | description                 | format          |
           | name            |                             |                 |
           +=================+=============================+=================+
           | idExt           | | External ID which is an   | string          |
           |                 |   abbriviation of surface   |                 |
           |                 |   name.                     |                 |
           |                 | | E.g. rotor lamination     |                 |
           |                 |   → RoLam                   |                 |
           +-----------------+-----------------------------+-----------------+
           | material        | Surface material of type    | Material        |
           |                 | Material.                   |                 |
           +-----------------+-----------------------------+-----------------+
           | nbrSegments     | | Number of surface         | int             |
           |                 |   segements on a whole      |                 |
           |                 |   circle                    |                 |
           |                 | | (2D machine model).       |                 |
           +-----------------+-----------------------------+-----------------+
           | angle           | Angle of the segment (rad). | float           |
           |                 | Should be 2*Pi/nbrSegments  |                 |
           +-----------------+-----------------------------+-----------------+
           | meshSize        | | Mesh size of the surface  | float           |
           |                 |   (m). If no surface mesh   |                 |
           |                 | | should be created its None|                 |
           +-----------------+-----------------------------+-----------------+


    """

    def __init__(
        self,
        name: str,
        idExt: str,
        curves: list[Line],
        material: Material,
        nbrSegments: int,
        angle: float,
        meshSize: float,
        segment_nbr: int = 0,
    ):
        """init of surface for API. This type of surface is special,
        because it allways forms a machine segment or a part of a segment.

        Args:
            name (str): name of the surface
            idExt (str): abbriviation of surface name (short name)
            curves (List[Line]): list of surface boundary lines
            material (Material): surface material in simulation.
            nbrSegments (int): number of segments in the full machine.
            angle (float): angle of the segment. Should be 2*Pi/nbrSegments.
            meshSize (float): mesh size of the surface.
            segment_nbr (int): actual segment number of surface in model
        """
        super().__init__(name=name, curves=curves)
        # FIXME: Update by using setters to check init values!!
        self._idExt: str = idExt
        self._material: Material = material
        self._nbrSegments: int = nbrSegments
        if not angle == 2 * pi / nbrSegments:
            raise ValueError(
                f"Segment angle ({angle}) of surface {name} "
                f"does not match 2*pi/nbrSegments ({2 * pi / nbrSegments})"
            )
        self._angle: float = angle
        self._meshSize: float = meshSize

        self._segment_number = segment_nbr  # default segment number is 0

        # curve_loop = gmsh.model.occ.addCurveLoop(curves)
        # self._id = gmsh.model.occ.addPlaneSurface(curve_loop)

    @property
    def tools(self) -> list[SurfaceAPI]:
        """Subtraction surfaces"""
        return super().tools

    @property
    def idExt(self) -> str:
        """get the abbriviation of the surface name (literal Surface ID)

        Returns:
            str: abbriviation of surface name (short name)
        """
        return self._idExt

    def setIdExt(self, newName: str) -> None:
        """set the abbriviation of the surface name (literal Surface ID)

        Args:
            name (str): abbriviation of surface name (short name)

        Returns:
            None
        """
        if isinstance(newName, str):
            self._idExt = newName
        else:
            raise ValueError(f"The given name was not type str: {newName}!")

    @property
    def material(self) -> Material:
        """get the material of the API surface

        Returns:
            Material: surface material
        """
        return self._material

    @property
    def angle(self) -> float:
        """get the angle of one surface segment. Should be 2*Pi/self._nbrSegments

        Returns:
            float: segment angle of that surface in rad.
        """
        return self._angle

    @property
    def NbrSegments(self) -> int:
        """get the nbrSegments of segments of a API surface to form a whole circle (2*Pi)

        Returns:
            int: maximal number of segments to form a whole circle.
        """
        return self._nbrSegments

    @property
    def meshSize(self) -> float:
        """get the mesh size of the points of the surface

        Returns:
            float: Mesh size of the surface points.
        """
        return self._meshSize

    @meshSize.setter
    def meshSize(self, meshSize: float) -> None:
        """set the mesh size of the points.

        Args:
            meshSize (float): Mesh size of the surface points.
        """
        if not isinstance(meshSize, (float, int)):
            msg = (
                f"Given mesh size for API surface '{self.name}'"
                f"was not a number but type '{type(meshSize)}'!"
            )
            raise TypeError(msg)
        self._meshSize = meshSize

    @property
    def segment_nbr(self) -> int:
        """Actual segement number of SurfaceAPI object"""
        return self._segment_number

    def duplicate(self, name="", segment=0) -> SurfaceAPI:
        """create a copy of the surface

        Args:
            name (str, optional): New name for copied surface.
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            SurfaceAPI: Duplicate of SurfaceAPI object.
        """
        # duplicate curves for new surface
        newCurves: list[Line | CircleArc | Spline] = []
        for curve in self.curve:
            newCurves.append(curve.duplicate())
        # create duplicate surfcace object
        dup_surf = SurfaceAPI(
            name=name,
            idExt=self.idExt,
            curves=newCurves,
            material=self.material,
            nbrSegments=self.NbrSegments,
            angle=self.angle,
            meshSize=self.meshSize,
            segment_nbr=segment,
        )
        for tool in self.tools:
            new_tool = tool.duplicate(segment=segment)
            dup_surf.cutOut(new_tool)
        # add "_dup" str to new surface name, if it was not duplicted before
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                dup_surf.name = f"{parentName}_dup"
            else:
                dup_surf.name = f"{parentName}_{dup_surf.id}"
        dup_surf.setMeshColor(self.getMeshColor())
        return dup_surf

    def rotateDuplicate(self, segment: int) -> SurfaceAPI:
        """
        Create a copy of the give surface and its tools surfaces + rotate it by
        :attr:`angle`.
        This also sets the property :attr:`segment_nbr` to the given segment value.

        Args:
            segment (float): Segment number.

        Returns:
            SurfaceAPI: Copied and rotated SurfaceAPI object.
        """
        if (segment % 1) != 0 or segment >= self.NbrSegments:
            raise ValueError("Segment number must be valid integer!")

        rot_angle = self.angle * segment

        if rot_angle != 0:  # if the rotation angle is not zero
            dup_surf: SurfaceAPI = self.duplicate(
                name=f"{self.name} (Seg.: {segment})", segment=segment
            )
            dup_surf.rotateZ(globalCenterPoint, rot_angle)
            tools = dup_surf.tools  # init tools array
            while tools:
                new_tools = []  # init new tools
                for tool in dup_surf.tools:
                    # rotate tools
                    tool.rotateZ(globalCenterPoint, rot_angle)
                    tool.name = f"{tool.name} (Seg.: {segment})"
                    if tool.tools:
                        # if tool has tools
                        new_tools.extend(tool.tools)  # extend new tools
                tools = new_tools  # update tools array

            return dup_surf
        # if the angle is zero: give back the old surface
        return self

    def cutOut(self, ToolSurface: SurfaceAPI, keepTool: bool = True) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
        self._cut.append(ToolSurface)
        ToolSurface.setTool()  # set to the tool surface
        if not keepTool:
            ToolSurface.delete = True
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
        if (
            out_dim_tags_map[1] == cut_dim_tags
            and out_dim_tags_map[0] == out_dim_tags + cut_dim_tags
        ):
            # tool surface did not change and parent surface is fromed by
            # new surface + tool
            self.id = out_dim_tags[0][1]  # set id to new surface tag
            return None
        if out_dim_tags_map[0] == out_dim_tags and out_dim_tags_map[1] == [
            out_dim_tags[1]
        ]:
            # same as first test but tool surface was copied with new tag
            self.id = out_dim_tags[0][1]  # set id to new surface tag
            ToolSurface.id = out_dim_tags[1][1]  # set id of tool surfacee to new tag
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
                        [dimtag],
                        globalCenterPoint.x,
                        globalCenterPoint.y,
                        globalCenterPoint.z,
                        0,
                        0,
                        1,
                        self.angle,
                    )
                    # There is no way to initialize SurfaceAPI with a GmshSurface object
                    # directly so we need to create a GmshSurface first and extract the
                    # curve loop from it:
                    gmsh.model.occ.synchronize()
                    gmsh_surf = GmshSurface(tag=dimtag[1])
                    # somehow the rotation does not work here. Do rotation manually
                    # before creating the GmshSurface
                    # gmsh_surf.rotateZ(globalCenterPoint, self.angle)
                    # gmsh.model.occ.synchronize()

                    new_tool = SurfaceAPI(
                        name=ToolSurface.name + "_1",
                        idExt=ToolSurface.idExt,
                        curves=gmsh_surf.curve,
                        material=ToolSurface.material,
                        nbrSegments=ToolSurface.NbrSegments,
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
                    # There is no way to initialize SurfaceAPI with a GmshSurface object
                    # directly so we need to create a GmshSurface first and extract the
                    # curve loop from it
                    replace_tool = SurfaceAPI(
                        name=ToolSurface.name + "_0",
                        idExt=ToolSurface.idExt,
                        curves=gmsh_surf.curve,
                        material=ToolSurface.material,
                        nbrSegments=ToolSurface.NbrSegments,
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
                "Number of output surfaces is less than number of input surfaces!"
            )

    # TODO: Update plot function to also plot tool surfaces
