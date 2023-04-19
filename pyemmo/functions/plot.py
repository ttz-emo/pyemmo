from random import random
from typing import List, Tuple, Union
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..script.geometry.point import Point
from ..script.geometry.surface import Surface
from ..script.geometry.line import Line
from ..script.geometry.circleArc import CircleArc
from ..script.geometry.spline import Spline


def plot(
    geoList: List[Union[Surface, Line, CircleArc, Spline, Point]],
    fig: Figure = None,
    linewidth=0.5,
    color=[random() for i in range(3)],
    marker=".",
    markersize=1,
    tag=False,
) -> Tuple[Figure, Axes]:
    """
    2D Line plot of the surface
    """
    if not isinstance(geoList, list):
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
            geoObj.plot(
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=tag,
            )
    return fig, ax
