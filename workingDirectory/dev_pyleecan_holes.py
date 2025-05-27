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
# %%

import logging
import os

import gmsh
from pyleecan.Classes.import_all import LamSlot, MachineSIPMSM, SurfLine

# from pyleecan.definitions import DATA_DIR as PYLEECAN_DATA_DIR
from pyleecan.Functions import load
from pyleecan.Functions.labels import get_obj_from_label

from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.api.pyleecan.build_pyemmo_material import build_pyemmo_material

# from pyemmo.api.pyleecan.create_LamSlot_segment import create_LamSlot_segment
from pyemmo.api.pyleecan.create_gmsh_surf import create_gmsh_surface
from pyemmo.api.pyleecan.label2part_id import label2part_id

# from pyemmo.api.pyleecan import main as pyleecanAPI
from pyemmo.definitions import TEST_DIR

# disable messages of matplotlib
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.INFO)

gmsh.initialize()
gmsh.model.add("test_model")
# %%
# pylint: disable=locally-disabled, no-member
machine: MachineSIPMSM = load.load(
    os.path.join(TEST_DIR, "data", "api", "pyleecan", "02_spmsm_muster_02.json")
)
lamination: LamSlot = machine.stator  # get stator with cooling ducts

# %%
nbr_segments = lamination.comp_periodicity_geo()[0]  # number of lamination segments
# build single segment geometry:
surfs: list[SurfLine] = lamination.build_geometry(sym=nbr_segments, alpha=0)
# for each surface, create a MachineSegmentSurface object and add it to the dict
# with part_id as key
segment_dict: dict[str, MachineSegmentSurface] = {}
for surf in surfs:
    gmsh_surf = create_gmsh_surface(surf)  # create surface in Gmsh
    machine_part = get_obj_from_label(machine, surf.label)  # get machine part
    # get material from machine part. Material attribute can be mat_type or mat_void
    try:
        material = machine_part.mat_type
    except AttributeError:
        try:
            material = machine_part.mat_void
        except Exception as e:
            raise e
    except Exception as e:
        raise e
    # get part_id from label (pyleecan label to pyemmo label)
    part_id = label2part_id(surf.label)
    # get number of segments for part. Holes can have multiple segments per lamination
    try:
        part_sym = machine_part.comp_periodicity_spacial()[0]
        if part_sym != nbr_segments:
            logging.warning(
                "Part %s has a different symmetry (%i) than the lamination (%i)",
                surf.label,
                part_sym,
                nbr_segments,
            )
    except AttributeError:
        # if the part does not have comp_periodicity_spacial, which seems to be the
        # case for magnets, we use the lamination symmetry, which should be the same
        # for a single pole.
        part_sym = nbr_segments
    except Exception as e:
        raise e

    segment_dict[part_id] = MachineSegmentSurface(
        part_id=part_id,
        material=build_pyemmo_material(material),
        tag=gmsh_surf.id,
        nbr_segments=part_sym,
        name=surf.label,
    )

# %%
