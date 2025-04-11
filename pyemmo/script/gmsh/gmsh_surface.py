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

from ..geometry import defaultCenterPoint
from ..geometry.point import Point
from ..geometry.surface import Surface
from ..gmsh import DimTag
from .gmsh_arc import GmshArc
from .gmsh_geometry import GmshGeometry
from .gmsh_line import GmshLine
from .gmsh_point import GmshPoint


class GmshSurface(GmshGeometry, Surface):
    """GmshSurface is a class that represents a 2D surface in the Gmsh model. It provides
    methods for creating, manipulating, and querying surfaces in the Gmsh geometry kernel.
    Attributes:
        dim (int): The dimension of the surface, which is always 2.
        curve (list[Union[GmshLine, GmshArc]]): The list of curves that form the surface.
        meanMeshLength (float): The mean mesh length of all points of the surface.
        area (float): The area of the surface as calculated by Gmsh.
    Methods:
        __init__(tag: int, name: str = ""):
            Initializes a GmshSurface object with a given tag and optional name.
        from_curve_loop(curve_loop: list[Union[GmshLine, GmshArc]], name: str = "") -> "GmshSurface":
            Creates a GmshSurface from a list of curves that form a closed loop.
        _get_lineloop(tag: int) -> list[Union[GmshLine, GmshArc]]:
            Retrieves the line loop of the surface from the Gmsh model.
        __str__() -> str:
            Returns a string representation of the GmshSurface object.
        setMeshLength(meshLength: float) -> None:
            Sets the mesh length of all points of the surface.
        getMinMeshLength() -> float:
            Retrieves the minimum mesh length of all points of the surface.
        translate(dx: float, dy: float, dz: float) -> None:
            Translates the surface by the specified distances in the x, y, and z directions.
        rotateZ(rotationPoint: Point, angle: float) -> None:
            Rotates the surface around the z-axis by a specified angle.
        rotateX(rotationPoint: Point, angle: float) -> None:
            Rotates the surface around the x-axis by a specified angle.
        rotateY(rotationPoint: Point, angle: float) -> None:
            Rotates the surface around the y-axis by a specified angle.
        duplicate(name: str = "") -> "GmshSurface":
            Duplicates the surface and returns the new surface.
        mirror(planePoint: Point, planeVector1: Point, planeVector2: Point, name: str = "") -> None:
            Not implemented. Intended to mirror the surface across a plane.
        combine(addSurf: "GmshSurface", removeObject: bool = True, removeTool: bool = True) -> "GmshSurface":
            Combines the current surface with another surface to create a new surface.
        sortCurves() -> None:
            No-op method. Curves are already sorted when retrieved from Gmsh.
        replaceCurve(oldCurve: GmshLine, newCurve: GmshLine) -> None:
            Raises an error. Replacing curves is not supported for GmshSurface.
        cutOut(tool: "GmshSurface", keepTool: bool = True) -> None:
            Cuts out a tool surface from the parent surface using a Boolean difference.
        calcCOG() -> Point:
            Calculates the center of gravity (COG) of the surface.
    Examples:
        >>> square_surf = GmshSurface(tag=gmsh_surface_tag)
    """

    @property
    def dim(self) -> int:
        return 2

    def __init__(self, tag: int, name: str = ""):
        """Initialize a GmshSurface object with a given tag and optional name.
        Optionally use ``GmshSurface.from_curve_loop()`` to create a new GmshSurface object from a
        list of curves.
        If a tag is given, the curves are retrieved from the current Gmsh model.

        Args:
            tag (int): Gmsh internal surface tag. Must be a positive integer.
            name (str, optional): Name of the surface to set or reset. Defaults to the
                internal Gmsh name if not provided.

        Raises:
            TypeError: If the tag is not an integer.
            ValueError: If the tag is negative, does not exist in the Gmsh model, or
                is not of type 'Plane'.

        Example:
            >>> from pyemmo.script.gmsh.gmsh_surface import GmshSurface
            >>> import gmsh
            >>> gmsh.initialize()
            >>> gmsh.model.add("model")
            >>> # create surface in gmsh:
            >>> square_id = gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)
            >>> # init GmshSurface with tag:
            >>> square_surf = GmshSurface(tag = square_id)

            >>> # init with curve loop
            >>> # ... create lines that form a closed loop in `line_list`
            >>> gmsh_surf = GmshSurface.from_curve_loop(curve_loop = line_list)
        """
        if not isinstance(tag, (int, np.integer)):
            raise TypeError("Gmsh tag must be positive integer!")

        if tag >= 0:
            # create GmshSurface from existing tag
            gmsh.model.occ.synchronize()
            if (2, tag) not in gmsh.model.get_entities(2):
                raise ValueError(f"Surface tag {tag} does not exist in the Gmsh model!")
            if not gmsh.model.get_type(2, tag) == "Plane":
                surf_type = gmsh.model.get_type(2, tag)
                raise ValueError(
                    f"Tag {tag} is not of type 'Plane' but is type '{surf_type}'!"
                )
            self._id = tag  # set private id because setter will try to reset the id!
            # if no name is given, get the name from the Gmsh model:
            #   Name attribute itself will be set through Surface.__init__().
            if not name:
                name = gmsh.model.get_entity_name(2, tag)
        else:
            raise ValueError(f"Bad Gmsh surface {tag=}!")
        Surface.__init__(self, name=name, curves=self.curve)

    @classmethod
    def from_curve_loop(
        cls, curve_loop: list[Union[GmshLine, GmshArc]], name: str = ""
    ) -> "GmshSurface":
        """Create a GmshSurface from a list of curves.

        Args:
            curve_loop (list[Union[GmshLine, GmshArc]]): List of curves that form a closed
                loop.

        Returns:
            GmshSurface: The created GmshSurface.
        """
        if not all(
            curve is not None and isinstance(curve, (GmshLine, GmshArc))
            for curve in curve_loop
        ):
            raise ValueError("All curves must be of type GmshLine or GmshArc!")
        # no tag given, but all curves are type GmshLine or GmshArc
        # FIXME: addCurveLoop() can create new line objects in gmsh to share touch
        # points
        curve_loop = gmsh.model.occ.addCurveLoop([curve.id for curve in curve_loop])
        tag = gmsh.model.occ.addPlaneSurface([curve_loop])
        return cls(tag=tag, name=name)

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
        raise ValueError(
            "Can not set the lineloop of a existing GmshSurface!"
            "Use transformation methods (translate, rotate, mirror) instead!"
        )

    @property
    def meanMeshLength(self) -> float:
        """get the mean mesh length of all points of the surface.

        Returns:
            float: mean of mesh length of all points in meter
        """
        points: list[GmshPoint] = (
            self.allPoints
        )  # TODO: Check if the usage of allPoints
        # is correct here...
        mlList = [p.meshLength for p in points]
        return np.mean(mlList)

    @property
    def area(self) -> float:
        """Surface area of gmsh surface by gmsh.model.occ.getMass(dim, tag)"""
        return gmsh.model.occ.getMass(self.dim, self.id)

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

    def rotateZ(self, rotationPoint: Point = defaultCenterPoint, angle: float = 0.0):
        """Rotates the surface around the z-axis.

        Args:
            rotationPoint (Point): The point around which the surface should be rotated.
                Defaults to `pyemmo.script.geometry.defaultCenterPoint`.
            angle (float): The angle in degrees by which the surface should be rotated.
                Defaults to 0.0.

        example:
            >>> from pyemmo.gmsh import GmshSurface, GmshPoint
            >>> from math import pi
            >>> surface = GmshSurface()
            >>> rotationPoint = GmshPoint()
            >>> surface.rotateZ(rotationPoint, pi/2)
        """
        GmshGeometry.rotateZ(self, rotationPoint, angle)
        # TODO: Also rotate tools?

    def duplicate(self, name: str = "") -> "GmshSurface":
        """Duplicates the surface.

        Args:
            name (str, optional): The name of the duplicated surface.

        Returns:
            GmshSurface: The duplicated surface.
        """
        dup_surf = GmshGeometry.duplicate(self, name)
        # TODO: Handle duplication of tools!
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
                self.name = gmsh.model.getEntityName(self.dim, old_id)
                gmsh.model.occ.remove([(2, old_id)])  # remove old tool surface
            return None
        if len(out_dim_tags) > 2:
            # extra surface(s) was/were created (additional to parent and tool), so
            # surfaces partly intersected.
            old_id = self.id
            self._id = out_dim_tags[0][1]  # update parent surface id
            # update name of new parent surface:
            self.name = gmsh.model.getEntityName(self.dim, old_id)
            # gmsh.model.setEntityName(2, self.id, self.name)  # update name of surface

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
