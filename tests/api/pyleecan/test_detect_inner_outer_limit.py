import pytest
import os
from typing import List


from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.load import load
from pyemmo.definitions import TEST_DIR

from pyemmo.api.json.SurfaceJSON import SurfaceAPI
from pyemmo.api.pyleecan.translate_surfs import translate_surface
from pyemmo.api.pyleecan.detect_inner_outer_limit import (
    detect_inner_outer_limit,
)


@pytest.mark.parametrize(
    "machine_sample",
    [
        "00_prius_machine.json",
        "02_spmsm_muster_02.json",
        "03_synrm_muster_Bachelor.json",
    ],
)
def test_detect_inner_outer_limit(machine_sample):
    machine: Machine = load(
        os.path.abspath(os.path.join(TEST_DIR, "data", machine_sample))
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

    for i, surf in enumerate(all_surfaces):
        save_space_temp = []
        all_surfs_labels_split1 = []
        all_surfs_labels.append(surf.label)
        all_surfs_labels_split1.extend(surf.label.split("_"))

        for split1 in all_surfs_labels_split1:
            save_space_temp.extend(split1.split("-"))
        all_surfs_labels_split2.append(save_space_temp)

        # translating the surface
        pyemmo_surf, angle_point_ref_list = translate_surface(
            name_split_list=all_surfs_labels_split2[i],
            machine=machine,
            surface=surf,
            angle_point_ref_list=angle_point_ref_list,
        )
        geometry_list.append(pyemmo_surf)

    # ------------------------------------------------------
    # Change names of rotorRint-Curve and statorRext-Curve:
    # ------------------------------------------------------

    has_shaft = bool(machine.rotor.Rint > 0)

    if machine.rotor.is_internal:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.rotor.Rint,
            outer_radius=machine.stator.Rext,
            has_shaft=has_shaft,
        )
    else:
        geometry_list = detect_inner_outer_limit(
            geometry_list=geometry_list,
            inner_radius=machine.stator.Rint,
            outer_radius=machine.rotor.Rext,
            has_shaft=has_shaft,
        )

    if machine_sample == "00_prius_machine.json":
        assert geometry_list[0].curve[3].name == "InnerLimit"
        assert geometry_list[6].curve[1].name == "OuterLimit"

    elif machine_sample == "02_spmsm_muster_02.json":
        assert geometry_list[2].curve[1].name == "OuterLimit"

    elif machine_sample == "03_synrm_muster_Bachelor.json":
        assert geometry_list[0].curve[3].name == "InnerLimit"
        assert geometry_list[4].curve[1].name == "OuterLimit"
