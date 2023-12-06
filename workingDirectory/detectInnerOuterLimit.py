import math

from pyemmo.api.SurfaceJSON import SurfaceAPI


def detectInnerOuterLimit(
    geometryList: list[SurfaceAPI],
    rotorRint: float,
    statorRext: float,
    isShaft: bool,
) -> list[SurfaceAPI]:
    """Overwrites the name of the curve, if its the most outlying curve (-> ``OuterLimit``) or the most innerlying curve (-> ``InnerLimit``).

    Attention when making the function call:\n
    If the machine has an external rotor:\n
    ``rotorRint`` replaced with ``statorRint``\n
    ``statorRext`` replaced with ``rotorRext``

    Args:
        geometryList (list[SurfaceAPI]): list of the machine surfaces
        rotorRint (float): inner radius of the rotor
        statorRext (float): outer radius of the stator

    Returns:
        list[SurfaceAPI]: _description_
    """
    for surf in geometryList:
        for curve in surf.curve:
            if isShaft:
                if math.isclose(
                    a=curve.startPoint.radius, b=rotorRint, abs_tol=1e-6
                ) and math.isclose(
                    a=curve.endPoint.radius, b=rotorRint, abs_tol=1e-6
                ):
                    curve.name = "InnerLimit"
            if math.isclose(
                a=curve.startPoint.radius, b=statorRext, abs_tol=1e-6
            ) and math.isclose(
                a=curve.endPoint.radius, b=statorRext, abs_tol=1e-6
            ):
                curve.name = "OuterLimit"
    return geometryList
