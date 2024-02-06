import sys
import os
from typing import List

from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

from pyemmo.api.json.modelJSON import SurfaceAPI
from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR
import pyemmo.api.pyleecan.translate_surfs


def test_translate_surfs():
    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []
    machine: Machine = load(
        os.path.abspath(
            os.path.join(TEST_DIR, "data", "00_prius_machine.json")
        )
    )
    all_surfaces: list = machine.rotor.build_geometry(
        sym=machine.rotor.comp_periodicity_geo()[0], alpha=0
    )

    all_surfaces.extend(
        machine.stator.build_geometry(sym=machine.stator.slot.Zs, alpha=0)
    )
    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        # translating the surface
        (
            pyemmo_surf,
            angle_point_ref_list,
        ) = pyemmo.api.pyleecan.translate_surfs.translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    plot(geometry_list)
    print("Plot")


test_translate_surfs()
