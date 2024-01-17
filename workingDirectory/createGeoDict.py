"""imports"""
from typing import List, Union
import logging

from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Machine import Machine

from pyemmo.functions.plot import plot
from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc
from pyemmo.script.geometry.point import Point
from .translateGeometry import translateGeometry
from .getRotorStatorContour import (
    get_spmsm_rotor_cont,
    get_winding_cont,
    get_even_rotor_cont,
)
from .detectInnerOuterLimit import detectInnerOuterLimit
from .getMagnetizationDict import get_magnetization_dict


def createGeoDict(
    machine: Machine,
    is_internal_rotor: bool,
) -> tuple[
    list[SurfaceAPI],
    list[Union[Line, CircleArc]],
    list[Union[Line, CircleArc]],
    Point,
    Point,
    dict,
]:
    """_summary_

    Args:
        machine (Machine): _description_
        is_internal_rotor (bool): _description_

    Raises:
        TypeError: _description_

    Returns:
        tuple[ list[SurfaceAPI], list[Union[Line, CircleArc]], list[Union[Line, CircleArc]], Point, Point, dict, ]: _description_
    """
    
    # TODO: Funktion heißt createGeoDict aber gibt Liste zurück...

    rotor_sym = machine.rotor.comp_periodicity_geo()[0]
    stator_sym = machine.stator.slot.Zs
    all_surfaces = []
    all_surfaces.extend(machine.rotor.build_geometry(sym=rotor_sym, alpha=0))
    all_surfaces.extend(machine.stator.build_geometry(sym=stator_sym, alpha=0))

    all_surfs_labels = []
    all_surfs_labels_split2 = []

    geometry_list: List[SurfaceAPI] = []
    magnetization_dict = {}
    angle_point_ref_list = []

    rotor_rint = machine.rotor.Rint
    stator_rext = machine.stator.Rext

    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        logging.debug("Geometry translation for %s:", all_surfs_labels[i])

        pyemmo_surf, angle_point_ref_list = translateGeometry(
            nameSplitList=all_surfs_labels_split2[i],
            machine=machine,
            label=all_surfs_labels[i],
            surface=surf,
            anglePointRefList=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    magnetization_dict = get_magnetization_dict(
        machine=machine,
        angle_point_ref_list=angle_point_ref_list,
        geometry_list=geometry_list,
        magnetization_dict=magnetization_dict,
    )

    # =============================================
    # CutOuts in rotorLamination if IPMSM or SynRM:
    # =============================================
    if isinstance(machine, (MachineIPMSM, MachineSyRM)):
        for surf_to_cutout in geometry_list:
            if surf_to_cutout.name != "Rotor-0_Lamination":
                surf_to_cutout_split = surf_to_cutout.name.split("-")
                if surf_to_cutout_split[0] == "Rotor":
                    geometry_list[0].cutOut(surf_to_cutout)

    logging.debug("==============================")
    logging.debug("End of Translation of machine.")
    logging.debug("==============================")

    plot(geoList=geometry_list, linewidth=1, markersize=3)

    logging.debug("Plot of machine")
    logging.debug("===============")
    logging.debug("End of geometry translation")
    logging.debug("===========================")

    # --------------------------------------
    # Generate the rotor and stator contour:
    # --------------------------------------
    logging.debug("Generating rotor and stator contour")
    if isinstance(machine, (MachineIPMSM, MachineSyRM)):
        (
            rotor_contour_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = get_even_rotor_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
        stator_contour_line_list = get_winding_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
    elif isinstance(machine, MachineSIPMSM):
        (
            rotor_contour_line_list,
            r_point_rotor_cont,
            l_point_rotor_cont,
        ) = get_spmsm_rotor_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
        stator_contour_line_list = get_winding_cont(
            geometry_list=geometry_list,
            machine=machine,
            is_internal_rotor=is_internal_rotor,
        )
    else:
        raise TypeError("Unable to generate contours of this machine type!")

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    has_shaft = bool(rotor_rint > 0)

    if is_internal_rotor:
        geometry_list = detectInnerOuterLimit(
            geometryList=geometry_list,
            innerRadius=rotor_rint,
            outerRadius=stator_rext,
            hasShaft=has_shaft,
        )
    else:
        geometry_list = detectInnerOuterLimit(
            geometryList=geometry_list,
            innerRadius=machine.stator.Rint,
            outerRadius=machine.rotor.Rext,
            hasShaft=has_shaft,
        )

    return (
        geometry_list,
        rotor_contour_line_list,
        stator_contour_line_list,
        r_point_rotor_cont,
        l_point_rotor_cont,
        magnetization_dict,
    )
