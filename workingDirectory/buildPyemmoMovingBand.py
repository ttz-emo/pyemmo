import math

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Machine import Machine

from pyemmo.api import air
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.line import Line
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.functions.plot import plot
from .createGeoDict import create_geo_dict
from .getCoordinatesForPoint import getXforPoint, getYforPoint


def build_bands_rotor(
    machine: Machine,
    band_radius_list: list,
    r_point_rotor_cont: Point,
    l_point_rotor_cont: Point,
    rotor_cont_line_list: list,
) -> tuple[SurfaceAPI, SurfaceAPI, float]:
    """Builds the air gap segments at the rotor side.

    Args:
        bandRadiusList (list): List with the radii of the bands
        centerPoint (Point): Center point of machine
        lowestYPointRotor (Point):
        biggestYPointRotor (Point): _description_
        rotorSymAngle (float): _description_
        rotorContourLineList (list): _description_
        nbrRotorSeg (int): _description_
        angleRotor (float): _description_

    Returns:
        tuple[SurfaceAPI, SurfaceAPI, float]: _description_
    """
    nbr_rotor_seg = machine.rotor.comp_periodicity_geo()[0]
    angle_rotor = 2 * math.pi / nbr_rotor_seg  # [rad]
    center_point = Point(
        name="centerPointBand", x=0, y=0, z=0, meshLength=1e-3
    )

    # -----------------
    # Rotor inner band:
    # -----------------
    # Points:
    mb_mesh_len = 2 * band_radius_list[1] * math.pi / 360
    point_m11 = Point(
        name="PointM11",
        x=band_radius_list[0],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )
    point_m12 = Point(
        name="PointM12",
        x=getXforPoint(band_radius_list[0], angle_rotor),
        y=getYforPoint(band_radius_list[0], angle_rotor),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    rotor_circle1 = CircleArc(
        name="rotorBand1",
        startPoint=point_m11,
        endPoint=point_m12,
        centerPoint=center_point,
    )

    # Adding curves to list:
    rotor_air_gap1_curves = rotor_cont_line_list
    rotor_air_gap1_curves.append(rotor_circle1)
    rotor_air_gap1_curves.append(
        Line(
            name="lowerLine1",
            startPoint=r_point_rotor_cont,
            endPoint=point_m11,
        )
    )
    rotor_air_gap1_curves.append(
        Line(
            name="upperLine1",
            startPoint=l_point_rotor_cont,
            endPoint=point_m12,
        )
    )

    # Assginment of rotorBand1 as surface:
    rotor_air_gap1 = SurfaceAPI(
        name="rotorAirGap1",
        idExt="LuR1",
        curves=rotor_air_gap1_curves,
        material=air,
        nbrSegments=nbr_rotor_seg,
        angle=angle_rotor,
        meshSize=1.0,
    )
    plot(rotor_air_gap1_curves, linewidth=1, markersize=3, tag=True)
    print("---")

    # -----------------
    # Rotor outer band:
    # -----------------
    # Points:
    point_m21 = Point(
        name="PointM21",
        x=band_radius_list[1],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )
    point_m22 = Point(
        name="PointM22",
        x=getXforPoint(band_radius_list[1], angle_rotor),
        y=getYforPoint(band_radius_list[1], angle_rotor),
        z=0,
        meshLength=mb_mesh_len,
    )
    # Curves:
    rotor_circle2 = CircleArc(
        name="MB_CurveRotor",
        startPoint=point_m21,
        endPoint=point_m22,
        centerPoint=center_point,
    )

    # Adding curves to list:
    rotor_air_gap2_curves = []
    rotor_air_gap2_curves.append(rotor_circle1)
    rotor_air_gap2_curves.append(rotor_circle2)
    rotor_air_gap2_curves.append(
        Line(name="lowerLine2", startPoint=point_m11, endPoint=point_m21)
    )
    rotor_air_gap2_curves.append(
        Line(name="upperLine2", startPoint=point_m12, endPoint=point_m22)
    )

    # Assginment of rotorBand2 as surface:
    rotor_air_gap2 = SurfaceAPI(
        name="rotorAirGap2",
        idExt="LuR2",
        curves=rotor_air_gap2_curves,
        material=air,
        nbrSegments=nbr_rotor_seg,
        angle=angle_rotor,
        meshSize=1.0,
    )
    mb_radius = rotor_circle2.startPoint.radius

    # --------------------------------
    # RotorBandsCurves only for plots:
    # --------------------------------
    rotor_air_cap_curves = []
    rotor_air_cap_curves.append(rotor_air_gap1_curves)
    rotor_air_cap_curves.append(rotor_air_gap2_curves)
    plot(rotor_air_cap_curves, linewidth=1, markersize=3, tag=True)
    print("---")

    return (
        rotor_air_gap1,
        rotor_air_gap2,
        mb_radius,
    )


def build_bands_stator(
    machine: Machine,
    stator_cont_line_list: list,
    band_radius_list: list,
) -> tuple[SurfaceAPI, SurfaceAPI]:
    """_summary_

    Args:
        statorContourLineList (list): _description_
        bandRadiusList (list): _description_
        statorSymAngle (float): _description_
        centerPoint (Point): _description_
        nbrStatorSeg (int): _description_
        angleStator (float): _description_

    Returns:
        tuple[SurfaceAPI, SurfaceAPI]: _description_
    """
    nbr_stator_seg = machine.stator.slot.Zs
    angle_stator = 2 * math.pi / nbr_stator_seg  # [rad]
    center_point = Point(
        name="centerPointBand", x=0, y=0, z=0, meshLength=1e-3
    )

    # ------------------
    # Stator outer band:
    # ------------------
    biggest_previous_y_stator = 0
    for curve in stator_cont_line_list:
        for point in curve.points:
            if point.coordinate[1] > biggest_previous_y_stator:
                biggest_previous_y_stator = point.coordinate[1]
                biggest_y_point_stator = point
            elif point.coordinate[1] == 0:
                lowest_y_point_stator = point

    # Points:
    mb_mesh_len = 2 * band_radius_list[2] * math.pi / 360

    point_m41 = Point(
        name="PointM41",
        x=band_radius_list[3],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )

    point_m42 = Point(
        name="PointM42",
        x=getXforPoint(band_radius_list[3], angle_stator),
        y=getYforPoint(band_radius_list[3], angle_stator),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    stator_circle4 = CircleArc(
        name="statorCircle4",
        startPoint=point_m41,
        endPoint=point_m42,
        centerPoint=center_point,
    )

    lower_line4 = Line(
        name="lowerLine4", startPoint=lowest_y_point_stator, endPoint=point_m41
    )

    upper_line4 = Line(
        name="upperLine4",
        startPoint=biggest_y_point_stator,
        endPoint=point_m42,
    )

    # Adding curves to list:
    curves_stlu1 = stator_cont_line_list
    curves_stlu1.append(stator_circle4)
    curves_stlu1.append(lower_line4)
    curves_stlu1.append(upper_line4)

    # Assginment of statorAirGap1 as surface:
    stator_air_gap1 = SurfaceAPI(
        name="statorAirGap1",
        idExt="StLu1",
        curves=curves_stlu1,
        material=air,
        nbrSegments=nbr_stator_seg,
        angle=angle_stator,
        meshSize=1.0,
    )

    plot(curves_stlu1, linewidth=1, markersize=3, tag=True)
    stator_air_gap1.plot()
    print("---")

    # ------------------
    # Stator inner band:
    # ------------------
    # Points:
    point_m31 = Point(
        name="PointM31",
        x=band_radius_list[2],
        y=0,
        z=0,
        meshLength=mb_mesh_len,
    )

    point_m32 = Point(
        name="PointM32",
        x=getXforPoint(band_radius_list[2], angle_stator),
        y=getYforPoint(band_radius_list[2], angle_stator),
        z=0,
        meshLength=mb_mesh_len,
    )

    # Curves:
    stator_circle3 = CircleArc(
        name="MB_CurveStator",
        startPoint=point_m31,
        endPoint=point_m32,
        centerPoint=center_point,
    )

    lower_line3 = Line(
        name="lowerLine3", startPoint=point_m31, endPoint=point_m41
    )

    upper_line3 = Line(
        name="upperLine3", startPoint=point_m32, endPoint=point_m42
    )

    # Adding curves to list 'curvesStLu2':
    curves_stlu2 = []
    curves_stlu2.append(stator_circle4)
    curves_stlu2.append(stator_circle3)
    curves_stlu2.append(lower_line3)
    curves_stlu2.append(upper_line3)

    # Assginment of statorBand3 as surface:
    stator_air_gap2 = SurfaceAPI(
        name="statorAirGap2",
        idExt="StLu2",
        curves=curves_stlu2,
        material=air,
        nbrSegments=nbr_stator_seg,
        angle=angle_stator,
        meshSize=1.0,
    )

    return stator_air_gap1, stator_air_gap2


def calcs_radii(machine: Machine, is_internal_rotor: bool) -> tuple[float, float]:
    """Calculation of the magnet-radii and of the distance between rotor/magnet and stator inner radius

    Args:
        machine (Machine): Pyleecan machine
        is_internal_rotor (bool): Is rotor internal or not

    Returns:
        tuple[float, float]: Gives back the 
    """
    
    rotor_rint = machine.rotor.Rint
    rotor_rext = machine.rotor.Rext
    stator_rint = machine.stator.Rint
    stator_rext = machine.stator.Rext

    if isinstance(machine, MachineSIPMSM):
        h0 = machine.rotor.slot.H0
        h1 = machine.rotor.slot.H1

        if is_internal_rotor:
            magnet_farthest_radius = rotor_rext + h1 - h0
            magnet_shortest_radius = rotor_rext - h0

            if rotor_rext > magnet_farthest_radius:
                diff_radius = stator_rint - rotor_rext
                max_radius = rotor_rext

            else:
                diff_radius = stator_rint - magnet_farthest_radius
                max_radius = magnet_farthest_radius

        else:
            magnet_farthest_radius = rotor_rint + h0
            magnet_shortest_radius = rotor_rint + h0 - h1

            if rotor_rint < magnet_shortest_radius:
                diff_radius = stator_rext - rotor_rint
                max_radius = rotor_rint

            else:
                diff_radius = stator_rext - magnet_shortest_radius
                max_radius = magnet_shortest_radius

    elif isinstance(machine, (MachineIPMSM, MachineSyRM)):
        if is_internal_rotor:
            max_radius = rotor_rext
            diff_radius = stator_rint - max_radius
        else:
            max_radius = rotor_rint
            diff_radius = stator_rext - max_radius

    return diff_radius, max_radius


def get_translated_machine(
    machine: Machine,
    is_internal_rotor: bool,
) -> tuple[list, list[SurfaceAPI], float]:
    """_summary_

    Args:
        machine (Machine): _description_
        is_internal_rotor (bool): _description_

    Raises:
        RuntimeError: _description_

    Returns:
        tuple[list, list[SurfaceAPI], float]: _description_
    """

    diff_radius, max_radius = calcs_radii(
        machine=machine, is_internal_rotor=is_internal_rotor
    )

    # =================================================================
    # Translation of geometry and creation of rotor and stator contour:
    # =================================================================
    (
        geometry_list,
        rotor_cont_line_list,
        stator_cont_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    ) = create_geo_dict(
        machine,
        is_internal_rotor,
    )

    # ====================================
    # Calculation of the MovingBand radii:
    # ====================================
    number_of_bands = 5
    wp = diff_radius / number_of_bands
    band_radius_list = []

    for i in range(1, number_of_bands + 1):
        band_radius_list.append(max_radius + wp * i)

    (
        rotor_air_gap1,
        rotor_air_gap2,
        mb_radius,
    ) = build_bands_rotor(
        machine=machine,
        band_radius_list=band_radius_list,
        r_point_rotor_cont=r_point_rotor_cont,
        l_point_rotor_cont=l_point_rotor_cont,
        rotor_cont_line_list=rotor_cont_line_list,
    )
    (
        stator_air_gap1,
        stator_air_gap2,
    ) = build_bands_stator(
        machine=machine,
        stator_cont_line_list=stator_cont_line_list,
        band_radius_list=band_radius_list,
    )

    # ----------
    # All bands:
    # ----------
    all_bands = []
    all_bands.append(rotor_air_gap1)
    all_bands.append(rotor_air_gap2)
    all_bands.append(stator_air_gap1)
    all_bands.append(stator_air_gap2)
    geometry_list.extend(all_bands)

    geo_translation_dict = {}
    for surf in geometry_list:
        if surf.idExt not in geo_translation_dict:
            geo_translation_dict[surf.idExt] = surf
        else:
            raise RuntimeError(
                f"Surface ID '{surf.idExt}' already in geometry dict!"
            )

    return (
        all_bands,
        geometry_list,
        mb_radius,
        magnetization_dict,
        geo_translation_dict,
    )
