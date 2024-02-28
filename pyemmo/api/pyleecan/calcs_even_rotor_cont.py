import math
from typing import Union

from ..json.SurfaceJSON import SurfaceAPI
from ...script.geometry.point import Point
from ...script.geometry.line import Line
from ...script.geometry.circleArc import CircleArc
from ...functions.plot import plot


def calc_even_rotor_cont(
    rotor_lam_surf_list: list[SurfaceAPI],
    radius: float,
) -> tuple[list[Union[Line, CircleArc]], Point, Point]:
    """Calculation for the rotor contour of an IPMSM machine.

    Args:
        geometryList (list): List with all surfaces of the machine (Pyemmo format)
        radius (float): Pyleecan machine

    Returns:
        tuple[list[Union[Line, CircleArc]], Point, Point]: _description_
    """

    rotor_cont_line_list = []

    # --------------------------------------------
    # Filtering the lines that lie at the air gap:
    # --------------------------------------------
    # rotor lamination:
    for curve in rotor_lam_surf_list[0].curve:
        if not (
            math.isclose(a=curve.startPoint.radius, b=radius, abs_tol=1e-6)
        ) and not math.isclose(
            a=curve.endPoint.radius, b=radius, abs_tol=1e-6
        ):
            rotor_cont_line_list.append(curve)
    print("---")
    print("Plot Überprüfung des Löschens der Seitenlinien.")
    plot(rotor_cont_line_list, linewidth=1, markersize=3)
    print("---")

    for point in rotor_cont_line_list[0].points:
        if math.isclose(a=point.coordinate[1], b=0, abs_tol=1e-6):
            r_point_rotor_cont = point
        else:
            l_point_rotor_cont = point

    return rotor_cont_line_list, r_point_rotor_cont, l_point_rotor_cont
