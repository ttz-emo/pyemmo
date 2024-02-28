import math

from ..json.SurfaceJSON import SurfaceAPI


def detect_inner_outer_limit(
    geometry_list: list[SurfaceAPI],
    inner_radius: float,
    outer_radius: float,
    has_shaft: bool,
) -> list[SurfaceAPI]:
    """Overwrites the name of the curve, if its the most outlying curve (-> ``OuterLimit``) or the most innerlying curve (-> ``InnerLimit``).

    Attention when making the function call:\n
    If the machine has an external rotor:\n
    ``inner_radius``: ``rotorRint`` or ``statorRint``\n
    ``outer_radius``: ``statorRext`` or ``rotorRext``\n
    Combinations that work:
    * ``rotorRint`` and ``statorRext``
    * ``statorRint`` and ``rotorRext``

    Args:
        geometryList (list[SurfaceAPI]): list of the machine surfaces
        inner_radius (float): inner radius
        outer_radius (float): outer radius

    Returns:
        list[SurfaceAPI]: geometryList
    """
    for surf in geometry_list:
        for curve in surf.curve:
            if has_shaft:
                if math.isclose(
                    a=curve.startPoint.radius, b=inner_radius, abs_tol=1e-6
                ) and math.isclose(
                    a=curve.endPoint.radius, b=inner_radius, abs_tol=1e-6
                ):
                    curve.name = "InnerLimit"
            if math.isclose(
                a=curve.startPoint.radius, b=outer_radius, abs_tol=1e-6
            ) and math.isclose(
                a=curve.endPoint.radius, b=outer_radius, abs_tol=1e-6
            ):
                curve.name = "OuterLimit"

    return geometry_list
