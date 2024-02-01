import sys
import os
import logging
from typing import List

from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    # sys.path.append("C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo\\tests")

from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR
from pyemmo.api.modelJSON import SurfaceAPI
import workingDirectory.translate_surfs
import workingDirectory.get_magnetization_dict


def test_get_magnetization_dict():
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

    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []

    logging.debug("Geometry translation started")

    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        logging.debug(
            "Geometry translation of %s started:", all_surfs_labels[i]
        )

        # translating the surface
        (
            pyemmo_surf,
            angle_point_ref_list,
        ) = workingDirectory.translate_surfs.translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    magnetization_dict = (
        workingDirectory.get_magnetization_dict.get_magnetization_dict(
            machine=machine,
            angle_point_ref_list=angle_point_ref_list,
            geometry_list=geometry_list,
        )
    )
    assert magnetization_dict["Mag0"] == 0.5462703245568578
    assert magnetization_dict["Mag1"] == 0.2391278388405909


test_get_magnetization_dict()
