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
"""Module: pyemmo_create_geo_dict

This module provides functions to convert geometry elements from pyleecan to pyemmo format.

Functions:
    -   ``create_geo_dict``: Creates a dictionary containing geometry
        information for communication between Pyleecan and pyemmo.

Example:

    .. code:: python

        machine = MachineIPMSM(...)
        geometry_dict = create_geo_dict(machine)
        # Returns geometry objects suitable for pyemmo.

Raises:
    TypeError: If unable to generate contours of the given machine type.
"""

from __future__ import annotations

import logging

from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.Hole import Hole
from pyleecan.Classes.LamH import LamH
from pyleecan.Classes.LamSlot import LamSlot
from pyleecan.Classes.Material import Material as PyleecanMaterial
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.SurfLine import SurfLine
from pyleecan.Classes.SurfRing import SurfRing
from pyleecan.Functions.Geometry.transform_hole_surf import transform_hole_surf
from pyleecan.Functions.labels import AIRBOX_LAB  # "Airbox"
from pyleecan.Functions.labels import AIRGAP_LAB  # "Airgap"
from pyleecan.Functions.labels import BAR_LAB  # "Bar"
from pyleecan.Functions.labels import BORE_LAB  # "Bore"
from pyleecan.Functions.labels import HOLEM_LAB  # "HoleMag"
from pyleecan.Functions.labels import HOLEV_LAB  # "HoleVoid"
from pyleecan.Functions.labels import KEY_LAB  # "Key"
from pyleecan.Functions.labels import LAM_LAB  # "Lamination"
from pyleecan.Functions.labels import MAG_LAB  # "Magnet"
from pyleecan.Functions.labels import NO_MESH_LAB  # "NoMesh"
from pyleecan.Functions.labels import NOTCH_LAB  # "Notch"
from pyleecan.Functions.labels import SLID_LAB  # "SlidingBand"
from pyleecan.Functions.labels import SOP_LAB  # "SlotOpening"
from pyleecan.Functions.labels import TOOTH_LAB  # "Tooth"
from pyleecan.Functions.labels import VENT_LAB  # "Ventilation"
from pyleecan.Functions.labels import WEDGE_LAB  # "SlotWedge"
from pyleecan.Functions.labels import WIND_LAB  # "Winding"
from pyleecan.Functions.labels import YOKE_LAB  # "Yoke"
from pyleecan.Functions.labels import (
    get_obj_from_label,
)

from .. import air, logger
from ..machine_segment_surface import MachineSegmentSurface
from . import PyleecanAir, PyleecanMachine
from .build_pyemmo_material import build_pyemmo_material
from .create_gmsh_surf import create_gmsh_surface


def create_geo_dict(
    machine: PyleecanMachine,
) -> dict[str, MachineSegmentSurface]:
    """
    Creates a dictionary containing geometry information for communication
    between Pyleecan and pyemmo.

    This function translates the machine geometry into a format suitable for
    communication with pyemmo.
    It generates geometry objects, contour lines, and magnetization dictionaries for the machine.

    Args:
        machine (PyleecanMachine): The machine object to translate into pyemmo-compatible geometry.
        is_internal_rotor (bool): True if the rotor is internal, False otherwise.

    Returns:
        tuple: A tuple containing:
            - list[SurfaceAPI]: List of geometry surfaces.
            - list[Union[Line, CircleArc]]: List of rotor contour lines.
            - list[Union[Line, CircleArc]]: List of stator contour lines.
            - Point: Rightmost point of the rotor contour.
            - Point: Leftmost point of the rotor contour.
            - dict: Dictionary containing magnetization information.
    """
    rotor_sym = machine.rotor.comp_periodicity_geo()[0]
    # NOTE: We need to extract the additional holes here, because they can cause the
    # lamination contour to be open if they lie on the boundary. This is something thats
    # different in Gmsh compared to FEMM (Pyleecan).
    # Since the holes are not part of the machine then anymore, we cant find their
    # material using `get_obj_from_label`. Thats why we create them separatly after the
    # laminations.
    rotor_holes: list[Hole] = machine.rotor.axial_vent.copy()
    machine.rotor.axial_vent = []
    rotor_surfs: list[SurfLine] = machine.rotor.build_geometry(  # type: ignore
        sym=rotor_sym, alpha=0  # type: ignore
    )
    # is_internal_rotor = machine.rotor.is_internal  # type: ignore
    stator_sym = machine.stator.comp_periodicity_geo()[0]
    stator_surfs: list[SurfLine] = machine.stator.build_geometry(sym=stator_sym, alpha=0)  # type: ignore

    # all_surfs_labels = []
    # all_surfs_labels_split2 = []
    pyemmo_geo_dict: dict[str, MachineSegmentSurface] = {}
    logger.debug("Geometry translation started")
    logger.debug("Identifying geometries by surface label:")
    for lam, pyleecan_surfs, sym in (
        (machine.rotor, rotor_surfs, rotor_sym),
        (machine.stator, stator_surfs, stator_sym),
    ):
        assert isinstance(lam, (LamH, LamSlot)), "lam is not type LamHole or LamSlot!"
        # create lamination surface separatly for subtraction
        lam_surf = create_gmsh_surface(
            pyleecan_surfs.pop(0), sym, build_pyemmo_material(lam.mat_type)
        )
        pyemmo_geo_dict[lam_surf.part_id] = lam_surf
        for surf in pyleecan_surfs:
            if SOP_LAB in surf.label:
                # slot opening surface -> skip because is created by airgap function.
                continue
            if WEDGE_LAB in surf.label:
                # slot wedge surface
                material = lam.slot.wedge_mat
            elif WIND_LAB in surf.label or BAR_LAB in surf.label:
                # NOTE: In case of winding or bar label the object returned is the
                # lamination and not the actual object itself. If so we have to get the
                # actual conductor material.
                material = lam.winding.conductor.cond_mat
            else:
                obj = get_obj_from_label(machine, surf.label)
                if hasattr(obj, "mat_type"):
                    material = obj.mat_type
                elif hasattr(obj, "mat_void"):
                    if obj.mat_void is None:
                        logging.warning(
                            "Material for object %s is None. Using Air instead!", obj
                        )
                        material = PyleecanAir
                    else:
                        material = obj.mat_void
                else:
                    raise AttributeError(f"Cant get material from object {obj}")
            # translating the surface
            pyemmo_surf = create_gmsh_surface(
                surface=surf,
                nbr_segments=sym,
                material=build_pyemmo_material(material),  # type:ignore
            )
            if HOLEM_LAB in surf.label or HOLEV_LAB in surf.label:
                lam_surf.cutOut(pyemmo_surf)
            else:
                pyemmo_geo_dict[pyemmo_surf.part_id] = pyemmo_surf

    # subtract additional holes
    machine.rotor.axial_vent.extend(rotor_holes)
    for duct in machine.rotor.axial_vent:
        # try to get material
        if not isinstance(duct.mat_void, PyleecanMaterial):
            logging.warning(
                "No valid material given for hole %s. Using air instead!", duct
            )
            material = PyleecanAir
        else:
            material = duct.mat_void
        try:
            material = build_pyemmo_material(material)
        except Exception as e:  # pylint: disable=bare-except, broad-exception-caught
            logging.warning(
                (
                    "Could not translate material %s of Hole %s with index %i due to error: %s. "
                    "Using air instead!"
                ),
                material.name,
                str(type(duct)),
                machine.rotor.axial_vent.index(duct),
                e.args[0],
            )
            material = air
        # build geometry
        if hasattr(duct, "build_geometry"):
            surfs = duct.build_geometry()
        else:
            raise AttributeError(f"Cant determine hole geometry for {duct}")
        surfs = transform_hole_surf(
            hole_surf_list=surfs,
            Zh=duct.Zh,
            sym=rotor_sym,
            is_split=True,
            alpha=0,
            delta=0,
        )
        for surf in surfs:
            pyemmo_geo_dict["rotor lamination"].cutOut(
                create_gmsh_surface(
                    surf,
                    rotor_sym,
                    material,
                )
            )

    # create shaft
    if machine.shaft:
        shaft: Shaft = machine.shaft
        surf: list[SurfLine] = shaft.build_geometry(machine.rotor.get_Zs())
        assert len(surf) == 1, "Shaft has more than one surface"
        pyemmo_geo_dict[surf[0].label] = create_gmsh_surface(
            surface=surf[0],
            nbr_segments=machine.rotor.get_Zs(),
            material=build_pyemmo_material(shaft.mat_type),
            name=surf[0].label,
        )
    # create frame
    if machine.frame:
        frame: Frame = machine.frame
        surf: list[SurfRing | SurfLine] = frame.build_geometry(machine.stator.get_Zs())
        if surf:
            # empty surf list -> no frame
            assert len(surf) == 1, "Frame has more than one surface"
            pyemmo_geo_dict[surf[0].label] = create_gmsh_surface(
                surface=surf[0],
                nbr_segments=machine.stator.get_Zs(),
                material=build_pyemmo_material(frame.mat_type),
                name=surf[0].label,
            )

    logger.debug("=======================================")
    logger.debug("End of geometry translation of machine.")
    logger.debug("=======================================")

    # plot(geoList=geometry_list, linewidth=1, markersize=3)

    logger.debug("End of geometry translation")
    logger.debug("===========================")

    return pyemmo_geo_dict
