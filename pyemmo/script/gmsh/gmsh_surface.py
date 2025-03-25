#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
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
"""Module gmsh_surface.py for the class GmshSurface."""

from typing import Union

import gmsh
import numpy as np

from ..geometry.point import Point
from ..geometry.surface import Surface
from ..gmsh import DimTag
from .gmsh_arc import GmshArc
from .gmsh_geometry import GmshGeometry
from .gmsh_line import GmshLine
from .gmsh_point import GmshPoint


class GmshSurface(Surface, GmshGeometry):
    """
    GmshSurface class for Surfaces in Gmsh.
    """

    @property
    def dim(self) -> int:
        return 2

    def __init__(
        self,
        tag: int = -1,
        curves: list[Union[GmshLine, GmshArc]] = None,
        name: str = "",
    ):
        """GmshSurface init
        Possible initialization with gmsh tag OR curve loop (list of gmsh curve objects).


        Args:
            tag (int, optional): Gmsh internal surface tag. Defaults to -1.
            curves (list[Union[GmshLine, GmshArc]], optional): List of surfaces that
                form a closed curve loop to construct plane surface. Defaults to None.
            name (str, optional): Name of surface to set or reset. Defaults to internal.
                gmsh name.

        Example:
            >>> from pyemmo.gmsh import GmshSurface
            >>> import gmsh
            >>> gmsh.initialize()
            >>> gmsh.model.add("model")
            >>> # init with tag
            >>> square_id = gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)
            >>> square_surf = GmshSurface(tag = square_id)

            >>> # init with curve loop
            >>> ... create lines that form a closed loop in `line_list`
            >>> gmsh_surf = GmshSurface(tag = -1, curves = line_list)
        """
        if not isinstance(tag, (int, np.integer)):
            raise TypeError("Gmsh tag must be positive integer!")

        if tag >= 0:
            if curves is not None:
                raise ValueError(
                    "Can not create GmshSurface for input of tag AND line list!"
                )
            # create GmshSurface from existing tag
            self._init_with_tag(tag, name)
        elif tag == -1:
            if not all(
                l is not None and isinstance(l, (GmshLine, GmshArc)) for l in curves
            ):
                raise ValueError("All curves must be of type GmshLine or GmshArc!")
            # no tag given, but all curves are type GmshLine or GmshArc
            # FIXME: addCurveLoop() can create new line objects in gmsh to share touch
            # points
            curve_loop = gmsh.model.occ.addCurveLoop([curve.id for curve in curves])
            self._id = gmsh.model.occ.addPlaneSurface([curve_loop])
        else:
            raise ValueError(
                "Can not create GmshSurface for input of tag AND line list!"
            )
        super().__init__(name=name, curves=self.curve)

    def _init_with_tag(self, tag: int, name: str):
        gmsh.model.occ.synchronize()
        if (2, tag) not in gmsh.model.get_entities(2):
            raise ValueError(f"Surface tag {tag} does not exist in the Gmsh model!")
        if not gmsh.model.get_type(2, tag) == "Plane":
            surf_type = gmsh.model.get_type(2, tag)
            raise ValueError(
                f"Tag {tag} is not of type 'Plane' but is type '{surf_type}'!"
            )
        self._id = tag
        if not name:
            # if no name is given, get the name from the Gmsh model
            name = gmsh.model.get_entity_name(2, tag)
        # otherwise set the name to the given name
        self.name = name

    def _get_lineloop(self, tag: int) -> list[Union[GmshLine, GmshArc]]:
        """Get the lineloop of the surface from the Gmsh model.

        Args:
            tag (int): The tag of the surface in the Gmsh model.

        Raises:
            ValueError: If the line with the given tag is not of type Line or Circle.

        Returns:
            list[Union[GmshLine, GmshArc]]: The list of lines that form the lineloop.
        """
        gmsh.model.occ.synchronize()
        line_tags = np.abs(np.array(gmsh.model.get_boundary(dimTags=[(2, tag)]))[:, 1])
        curves: list[Union[GmshLine, GmshArc]] = []
        for ltag in line_tags:
            # TODO Add support for 'TrimmedCurve' curve type
            if gmsh.model.getType(1, ltag) in ("Line", "TrimmedCurve"):
                curves.append(GmshLine(tag=ltag))
            elif gmsh.model.getType(1, ltag) == "Circle":
                curves.append(GmshArc(tag=ltag))
            else:
                raise ValueError(f"Line with tag {ltag} is not of type Line or Circle!")
        return curves

    def __str__(self) -> str:
        msg = f"GmshSurface with ID {self.id}\n"
        msg += f"Name: {self.name}\n"
        msg += f"Loop contains {len(self.curve)} curves:\n"
        for curve in self.curve:
            msg += (
                f"  {type(curve)} ('{curve.id}'): Point ('{curve.start_point.id}') -> "
                f"Point ('{curve.end_point.id}')\n"
            )
        return msg

    @property
    def curve(self) -> list[Union[GmshLine, GmshArc]]:
        """Get the curves that form the surface.

        Returns:
            list[Union[GmshLine, GmshArc]]: The list of curves that form the surface.
        """
        return self._get_lineloop(self.id)

    @curve.setter
    def curve(self, curves: list[Union[GmshLine, GmshArc]]) -> None:
        """Set the curves that form the surface.

        Args:
            curves (list[Union[GmshLine, GmshArc]]): The list of curves that form the
            surface.
        """
        raise ValueError("Can not set the lineloop of a existing GmshSurface!")

    @property
    def meanMeshLength(self) -> float:
        """get the mean mesh length of all points of the surface.

        Returns:
            float: mean of mesh length of all points in meter
        """
        points: list[GmshPoint] = self.allPoints
        mlList = [p.meshLength for p in points]
        return np.mean(mlList)

    def setMeshLength(self, meshLength: float) -> None:
        """set the meshLength of all points of a surface.

        Args:
            meshLength (float): mesh length to be set for all points
        """
        points: list[GmshPoint] = self.allPoints
        for point in points:
            point.meshLength = meshLength

    def getMinMeshLength(self) -> float:
        """get the minimum meshLength of all points of the surface.

        Returns:
            float: min mesh length of all points
        """
        points: list[GmshPoint] = self.allPoints
        ml = points.pop().meshLength
        for point in points:
            nml = point.meshLength
            ml = min(ml, nml)
        return ml

    def translate(self, dx, dy, dz):
        """Translates the surface by the factors dx, dy and dz.

        Args:
            dx (float): Translation in x-direction.
            dy (float): Translation in y-direction.
            dz (float): Translation in z-direction.

        """
        return gmsh.model.occ.translate([(2, self.id)], dx, dy, dz)

    def rotateZ(self, rotationPoint: Point, angle: float):
        """Rotates the surface around the z-axis.

        Args:
            rotationPoint (Point): The point around which the surface should be rotated.
            angle (float): The angle in degrees by which the surface should be rotated.

        example:
            >>> from pyemmo.gmsh import GmshSurface, GmshPoint
            >>> from math import pi
            >>> surface = GmshSurface()
            >>> rotationPoint = GmshPoint()
            >>> surface.rotateZ(rotationPoint, pi/2)
        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(2, self.id)], x, y, z, 0, 0, 1, angle)

    def rotateX(self, rotationPoint: Point, angle: float):
        """Rotates the surface around the x-axis.

        Args:
            rotationPoint (Point): The point around which the surface should be rotated.
            angle (float): The angle in degrees by which the surface should be rotated.

        example:
            >>> from pyemmo.gmsh import GmshSurface, GmshPoint
            >>> from math import pi
            >>> surface = GmshSurface()
            >>> rotationPoint = GmshPoint()
            >>> surface.rotateX(rotationPoint, pi/2)
        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(2, self.id)], x, y, z, 1, 0, 0, angle)

    def rotateY(self, rotationPoint, angle):
        """Rotates the surface around the y-axis.

        Args:
            rotationPoint (Point): The point around which the surface should be rotated.
            angle (float): The angle in degrees by which the surface should be rotated.

        example:
            >>> from pyemmo.gmsh import GmshSurface, GmshPoint
            >>> from math import pi
            >>> surface = GmshSurface()
            >>> rotationPoint = GmshPoint()
            >>> surface.rotateY(rotationPoint, pi/2)
        """
        x, y, z = rotationPoint.coordinate
        gmsh.model.occ.rotate([(2, self.id)], x, y, z, 0, 1, 0, angle)

    def duplicate(self, name: str = "") -> "GmshSurface":
        """Duplicates the surface.

        Args:
            name (str, optional): The name of the duplicated surface.

        Returns:
            GmshSurface: The duplicated surface.
        """
        outDimTags: list[DimTag] = gmsh.model.occ.copy([(2, self.id)])
        if len(outDimTags) != 1:
            raise ValueError("Error in duplicating surface!")
        # reset name if not given
        if not name:
            name = self.name + "_dup"
        # create new GmshSurface object
        dup_surf = GmshSurface(tag=outDimTags[0][1], name=name)
        return dup_surf

    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        raise NotImplementedError("Method not implemented yet!")

    def combine(
        self, addSurf: "GmshSurface", removeObject: bool = True, removeTool: bool = True
    ) -> "GmshSurface":
        """Combines two surfaces to a new surface.

        Args:
            addSurf (GmshSurface): The surface to be added to the current surface.

        Returns:
            GmshSurface: The combined surface.
        """
        out = gmsh.model.occ.fuse(
            [(2, self.id)],
            [(2, addSurf.id)],
            removeObject=removeObject,
            removeTool=removeTool,
        )
        outDimTags: list[DimTag] = out[0]
        # outDimTagsMap: list[list[DimTag]] = out[1]
        if len(outDimTags) != 1:
            raise ValueError("Error in combining surfaces!")
        # TODO: add additional logic to check for correct fusion process
        comb_surf = GmshSurface(tag=outDimTags[0][1])
        return comb_surf

    def sortCurves(self):
        # no need to sort gmsh curves sind _get_lineloop() returns the curves in the
        # correct order
        pass

    def replaceCurve(self, oldCurve, newCurve):
        raise RuntimeError("No need to replace curves in GmshSurface!")

    def cutOut(self, tool: "GmshSurface", keepTool: bool = True) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
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
            [(2, self.id)], cut_dim_tags, removeTool=not keepTool
        )
        if len(out_dim_tags) == 1:
            # single output surface -> new surface should be the = ParentSurface-Tool
            if out_dim_tags_map[0] == out_dim_tags + cut_dim_tags:
                # old parent surface is new surface + tool
                if out_dim_tags[0][1] != self.id:
                    # the parent surface id changed -> set new id
                    old_id = self.id  # get old id
                    self._id = out_dim_tags[0][1]  # set id to new surface tag
                    gmsh.model.setEntityName(
                        2, self.id, self.name
                    )  # update name of surface
                    # gmsh.model.occ.remove(
                    #     [(2, old_id)]
                    # )  # remove old surface
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
                gmsh.model.setEntityName(
                    2, self.id, self.name
                )  # update name of surface
                gmsh.model.occ.remove([(2, old_id)])  # remove old surface
            if out_dim_tags[1][1] != tool.id:
                # the tool surface id changed -> set new id
                old_id = tool.id  # get old id
                tool._id = out_dim_tags[1][1]
                gmsh.model.setEntityName(2, tool.id, tool.name)
                gmsh.model.occ.remove([(2, old_id)])  # remove old tool surface
            return None
        if len(out_dim_tags) > 2:
            # extra surface(s) was/were created (additional to parent and tool), so
            # surfaces partly intersected.
            self._id = out_dim_tags[0][1]  # update parent surface id
            gmsh.model.setEntityName(2, self.id, self.name)  # update name of surface

            # TODO: handle the newly created tool surfaces
            # new_tool_dimtags = out_dim_tags_map[-1]
            # for dimtag in new_tool_dimtags:
            #     if dimtag not in out_dim_tags_map[0]:
            #         # new (outer) tool surface since it is not part of the original
            #         # surface
            #         # What to do with the new tool surface?
            #         outer_tool_part = GmshSurface(tag=dimtag[1])
            #     else:
            #         # replace old tool surface with new (not rotated) tool surface
            #         inner_tool_part = GmshSurface(tag=dimtag[1])
        else:
            raise ValueError(
                "Unexpected number of output surfaces after cutting out tool surface: "
                f"{len(out_dim_tags)}"
            )

    def calcCOG(self) -> Point:
        # TODO: test this works
        x, y, z = gmsh.model.occ.get_center_of_mass(2, self.id)
        return Point(f"COG of Surface {self.id}", x, y, z)
