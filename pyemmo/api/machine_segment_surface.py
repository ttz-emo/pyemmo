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
"""Module for json api surface class"""
from __future__ import annotations

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
        """create a surface from a given tag

        Args:
            tag (int): GMSH tag of the surface

        Returns:
            MachineSegmentSurface: SurfaceAPI object
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
        """get the abbriviation of the surface name (literal Surface ID)

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
        """get the material of the GmshSegmentSurface surface

        Returns:
            Material: surface material
        """
        return self._material

    @material.setter
    def material(self, material: Material) -> None:
        """set the material of the API surface

        Args:
            material (Material): surface material

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
            SurfaceAPI: Duplicate of SurfaceAPI object.
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
            SurfaceAPI: Copied and rotated SurfaceAPI object.
        """
        return GmshSegmentSurface.rotate_duplicate(self, segment=segment)

    # TODO: Overload cutOut to type check for type(tool). Because it makes no sense to
    # cut out a standard GmshSurface from a MachineSegmentSurface unless the tool is
    # removed. If the tool stays it will a least need to have a material property.
    # def cutOut(self, ToolSurface: SegmentSurface, keepTool: bool = True) -> None:
    #     """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
