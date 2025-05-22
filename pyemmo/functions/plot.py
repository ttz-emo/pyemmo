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
from __future__ import annotations

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..definitions import LINE_COLOR, POINT_COLOR
from ..script.geometry.circleArc import CircleArc
from ..script.geometry.line import Line
from ..script.geometry.point import Point
from ..script.geometry.spline import Spline
from ..script.geometry.surface import Surface


def plot(
    geoList: list[Surface | Line | CircleArc | Spline | Point],
    fig: Figure = None,
    linewidth=0.5,
    color=None,
    marker=".",
    markersize=1,
    tag=False,
) -> tuple[Figure, Axes]:
    """
    2D Line plot of the surface
    """
    if not isinstance(geoList, (list, tuple)):
        msg = f"Given object for geometry list was not type list, but {type(geoList)}"
        raise (TypeError(msg))
    if fig is None:
        fig, ax = plt.subplots()
        fig.set_dpi(200)
        # xlim, ylim = self.getBoundingBox(scalingFactor=1.1)
        # fig.axes[0].set(xlim=xlim, ylim=ylim)
        ax.set_aspect("equal", adjustable="box")
    else:
        ax = fig.axes
    for geoObj in geoList:
        if isinstance(geoObj, list):
            plot(
                geoObj,
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=tag,
            )
        else:
            if isinstance(geoObj, Point):
                # plot points separatly because they have no linewidth
                geoObj.plot(
                    fig=fig,
                    marker=marker,
                    markersize=markersize,
                    color=color if color else POINT_COLOR,
                    tag=tag,
                )
            else:
                geoObj.plot(
                    fig,
                    linewidth=linewidth,
                    color=color if color else LINE_COLOR,
                    marker=marker,
                    markersize=markersize,
                    tag=tag,
                )
    return fig, ax
