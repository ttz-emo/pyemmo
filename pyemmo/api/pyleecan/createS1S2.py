from math import isclose

from pyemmo.definitions import DEFAULT_GEO_TOL
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from ..json.SurfaceJSON import SurfaceAPI
from .get_coords_for_point import get_x_for_point, get_y_for_point



def createS1S2(
    pyemmoSurface: SurfaceAPI,
    anglePointRef: tuple,
    centerPoint: Point,
    magnetShortestRadius: float,
    magnetFarthestRadius: float,
):
    """_summary_

    Args:
        pyemmoSurface (SurfaceAPI): _description_
        anglePointRef (tuple): _description_
        centerPoint (Point): _description_
        magnetShortestRadius (float): _description_
        magnetFarthestRadius (float): _description_
    """
    pyemmoSurfaceCurveCopy = pyemmoSurface.curve.copy()
    for curve in pyemmoSurfaceCurveCopy:
        # S1
        if isclose(
            a=curve.startPoint.radius, b=magnetShortestRadius, abs_tol=DEFAULT_GEO_TOL
        ) and isclose(
            a=curve.endPoint.radius, b=magnetShortestRadius, abs_tol=DEFAULT_GEO_TOL
        ):
            S1 = Point(
                name="S1",
                x=get_x_for_point(magnetShortestRadius, anglePointRef),
                y=get_y_for_point(magnetShortestRadius, anglePointRef),
                z=0,
                meshLength=1.0,
            )
            magnetCurve1 = CircleArc(
                name="magnetCurve1",
                startPoint=curve.startPoint,
                centerPoint=centerPoint,
                endPoint=S1,
            )
            magnetCurve2 = CircleArc(
                name="magnetCurve2",
                startPoint=S1,
                centerPoint=centerPoint,
                endPoint=curve.endPoint,
            )
            pyemmoSurface.curve.remove(curve)
            pyemmoSurface.curve.append(magnetCurve1)
            pyemmoSurface.curve.append(magnetCurve2)

        # S2
        elif isclose(
            a=curve.startPoint.radius, b=magnetFarthestRadius, abs_tol=DEFAULT_GEO_TOL
        ) and isclose(
            a=curve.endPoint.radius, b=magnetFarthestRadius, abs_tol=DEFAULT_GEO_TOL
        ):
            S2 = Point(
                name="S2",
                x=get_x_for_point(magnetFarthestRadius, anglePointRef),
                y=get_y_for_point(magnetFarthestRadius, anglePointRef),
                z=0,
                meshLength=1.0,
            )
            magnetCurve3 = CircleArc(
                name="magnetCurve3",
                startPoint=curve.startPoint,
                centerPoint=centerPoint,
                endPoint=S2,
            )
            magnetCurve4 = CircleArc(
                name="magnetCurve4",
                startPoint=S2,
                centerPoint=centerPoint,
                endPoint=curve.endPoint,
            )
            pyemmoSurface.curve.remove(curve)
            pyemmoSurface.curve.append(magnetCurve3)
            pyemmoSurface.curve.append(magnetCurve4)
