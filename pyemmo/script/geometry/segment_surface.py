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

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ...definitions import LINE_COLOR
from . import defaultCenterPoint as gcp
from .line import Line
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
    ):
        """init of surface for API. This type of surface is special,
        because it allways forms a machine segment or a part of a segment.

        Args:
            name (str): name of the surface
            curves (List[Line]): list of surface boundary lines
            nbrSegments (int): number of segments to form the complete body.
        """
        super().__init__(name=name, curves=curves)
        self.nbrSegments: int = nbrSegments
        # there is no setter for segment number_number because its fixed!
        self._segment_number = 0

    @property
    def angle(self) -> float:
        """Get the angle of one surface segmen in radians. This equals:
            2 * Pi / self.nbrSegments

        Returns:
            float: segment angle of that surface in rad.
        """
        return 2 * np.pi / self.nbrSegments

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
        if not float(nbrSegments).is_integer():
            msg = (
                f"Given number of segments for API surface '{self.name}'"
                f"was not an integer '{nbrSegments=}'!"
            )
            raise TypeError(msg)
        self._nbrSegments = int(nbrSegments)

    @property
    def segment_nbr(self) -> int:
        """Actual segement number of SegmentSurface object. The default value is 0."""
        return self._segment_number

    def duplicate(self, name="") -> SegmentSurface:
        """create a copy of the SegmentSurface

        Args:
            name (str, optional): New name for copied surface.
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            SegmentSurface: Duplicate of SegmentSurface object.
        """
        # create duplicate surfcace object
        dup_surf = super().duplicate(name)
        # create duplicate of SegmentSurface object
        dup_seg_surf = SegmentSurface(
            name=dup_surf.name,
            curves=dup_surf.curve,
            nbrSegments=self.nbrSegments,
        )
        return dup_seg_surf

    def rotate_duplicate(self, segment: int) -> SegmentSurface:
        """
        Create a copy of the give surface and its tools surfaces + rotate it by
        :attr:`angle`.
        This also sets the property :attr:`segment_nbr` to the given segment value.

        Args:
            segment (float): Segment number.

        Returns:
            SegmentSurface: Copied and rotated SegmentSurface object.
        """
        if (
            not float(segment).is_integer()
            or 0 > segment
            or segment >= self.nbrSegments
        ):
            raise ValueError(f"Segment number must be valid integer, but is {segment}!")

        if segment != 0:
            # duplicate the segment and its tools and give new name
            dup_surf: SegmentSurface = self.duplicate(
                name=f"{self.name} (Seg.: {segment})"
            )
            # rotate the surface by the given angle:
            rot_angle = self.angle * segment
            dup_surf.rotateZ(gcp, rot_angle)
            # set the segment number
            dup_surf._segment_number = segment  # pylint: disable=protected-access
            # its ok to access the protected attribute here, because we are in the same
            # class. rotate_duplicate() is the only method that sets the segment number!
            # update tool names
            for tool_surf in dup_surf.tools:
                tool_surf.name = f"{tool_surf.name} (Seg.: {segment})"

            return dup_surf
        # if the segment number is zero: give back the original surface
        return self

    def cutOut(self, tool: SegmentSurface) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
        if not isinstance(tool, SegmentSurface):
            raise TypeError(
                f"Tool surface is not a SegmentSurface object! "
                f"But it type '{type(tool)}'!"
            )
        if self.segment_nbr != 0:
            raise ValueError(
                "Cutting out a tool from a segment surface is only allowed for the "
                "first segment!"
            )
        # check the number of segments
        if tool.nbrSegments != self.nbrSegments:
            # calculate total number of segments
            symmetry = np.gcd(tool.nbrSegments, self.nbrSegments)
            # create nbrSegments/symmetry copies
            for segment in range(1, int(self.nbrSegments / symmetry)):
                # rotate and duplicate parent surface if needed
                dup_parent = self.rotate_duplicate(segment)
                comb_surf = self.combine(dup_parent)  # combine the parent surfaces
                # update curve loop
                self.curve = comb_surf.curve
            self.nbrSegments = symmetry  # update number of segments
            for segment in range(int(tool.nbrSegments / symmetry)):
                dup_tool = tool.rotate_duplicate(segment)  # rotate and duplicate tool
                super().cutOut(dup_tool)  # cut out new tool
                dup_tool.nbrSegments = symmetry  # update number of segments
        else:
            # if the number of segments is the same, cut out the tool directly
            super().cutOut(tool)

    def plot(
        self,
        fig: Figure = None,
        linewidth=0.5,
        color=LINE_COLOR,
        marker=".",
        markersize=1,
        tag=False,
        symmetry=None,
    ) -> None:
        """
        2D Line plot of the surface

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            linewidth (float): Line width in points. Defaults to 0.5.
            color (list, optional): Line color. Defaults to
                ``pyemmo.definitions.LINE_COLOR``. See
                `Matplotlib Colors<https://matplotlib.org/stable/users/explain/colors/colors.html#color-formats>`_
                for more details.
            marker (str, optional): Defaults to None. Examples are '.', 'o', 'x', '+',
                ... See
                `Matplotlib Markers<https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers>`_
                for more details.
            markersize (float, optional): Marker size in points. Defaults to 1.
            tag (bool): Flag to print surface and line namea like "S ("`Surface_Name`")"
                and point tags if `marker` is given.
            symmetry (int|None, optional): Number of segments to plot. Defaults to None
                which means that only one segment will be shown. For symmetry = 1 the
                whole model will be shown.

        Returns:
            Figure: Matplotlib figure object.
        """  # noqa
        if fig is None:
            fig, ax = plt.subplots()
            fig.set_dpi(200)
            xlim, ylim = self.getBoundingBox(scalingFactor=1.1)
            fig.axes[0].set(xlim=(-xlim[1], xlim[1]), ylim=(-xlim[1], xlim[1]))
            ax.set_aspect("equal", adjustable="box")
        ax = fig.axes[0]
        # If there is no symmetry given plot the surface as it is and return
        if symmetry is None:
            super().plot(
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=tag,
            )
            return fig
        # otherwise calculate number of segments to plot:
        nbr_segments_plot = self.nbrSegments / symmetry
        if not float(nbr_segments_plot).is_integer():
            raise ValueError(
                f"Bad symmetry value {symmetry} for SegmentSurface with "
                f"{self.nbrSegments} segments! Number of segments to plot must be an "
                f"integer! But it is {nbr_segments_plot}."
            )
        # rotate and duplicate segments and recall plot-method without symmetry
        for segment in range(int(nbr_segments_plot)):
            # rotate and duplicate surface
            dup_surf = self.rotate_duplicate(segment)
            # plot the duplicate with out symmetry
            dup_surf.plot(
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=tag,
                symmetry=None,
            )
        return fig  # return figure object for further usage
