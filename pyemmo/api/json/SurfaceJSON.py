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

from numpy import pi

from ...script.geometry.circleArc import CircleArc
from ...script.geometry.line import Line
from ...script.geometry.spline import Spline
from ...script.geometry.surface import Surface
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

    # TODO: Update plot function to also plot tool surfaces
