import os
import sys
from typing import List
import pytest
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load
from pyemmo.api.json.modelJSON import SurfaceAPI
from pyemmo.functions.plot import plot
from pyemmo.definitions import TEST_DIR

import pyemmo.api.pyleecan.translate_surfs
import pyemmo.api.pyleecan.get_rotor_stator_cont
import pyemmo.api.pyleecan.get_translated_machine


def add_pyemmo_path():
    try:
        from pyemmo.script.script import Script
    except ImportError:
        rootname = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "pyemmo")
        )
        print(f"Could not determine root. Setting it manually to '{rootname}'")
        print(f'rootname is "{rootname}"')
        sys.path.append(rootname)


def split_labels(label):
    return [part.split("-") for part in label.split("_")]


def get_translated_surface(
    machine, surf, all_surfs_labels_split2, angle_point_ref_list
):
    (
        pyemmo_surf,
        angle_point_ref_list,
    ) = pyemmo.api.pyleecan.translate_surfs.translate_surface(
        name_split_list=all_surfs_labels_split2,
        machine=machine,
        surface=surf,
        angle_point_ref_list=angle_point_ref_list,
    )
    return pyemmo_surf, angle_point_ref_list


def get_translated_machine(machine: Machine):
    all_surfs_labels = []
    all_surfs_labels_split2 = []
    geometry_list: List[SurfaceAPI] = []
    angle_point_ref_list = []

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

    return geometry_list, machine.rotor.is_internal


def test_get_rotor_cont(get_rotor_cont_function, machine_file):
    machine: Machine = load(
        os.path.abspath(os.path.join(TEST_DIR, "data", machine_file))
    )
    geometry_list, is_internal = get_translated_machine(machine)
    result = get_rotor_cont_function(
        geometry_list=geometry_list,
        machine=machine,
        is_internal_rotor=is_internal,
    )

    # Verwende pytest, um die erwarteten Ergebnisse zu überprüfen
    assert result is not None

    # Plot für visuelle Überprüfung
    # plot(result, tag=True)
    # print("Plot rotor contour")


@pytest.mark.parametrize(
    "test_function",
    [
        (
            pyemmo.api.pyleecan.get_rotor_stator_cont.get_spmsm_rotor_cont,
            "02_spmsm_muster_02.json",
        ),
        (
            pyemmo.api.pyleecan.get_rotor_stator_cont.get_even_rotor_cont,
            "03_synrm_muster_Bachelor.json",
        ),
        (
            pyemmo.api.pyleecan.get_rotor_stator_cont.get_winding_cont,
            "03_synrm_muster_Bachelor.json",
        ),
    ],
)
def test_main_functions(test_function):
    add_pyemmo_path()
    get_rotor_cont_function, machine_file = test_function
    test_get_rotor_cont(get_rotor_cont_function, machine_file)


# Führe die Tests nur aus, wenn dieses Skript direkt ausgeführt wird
if __name__ == "__main__":
    test_main_functions()
