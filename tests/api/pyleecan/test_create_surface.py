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
"""
Module to test translate surface function of api
import pyemmo.api.pyleecan.create_gmsh_surface
"""
from os.path import abspath, join
from typing import List

import gmsh
import pytest
from pyleecan.Classes.Machine import Machine
from pyleecan.Functions.labels import HOLEM_LAB, HOLEV_LAB, MAG_LAB, get_obj_from_label

# pylint: disable=locally-disabled, no-name-in-module
from pyleecan.Functions.load import load

from pyemmo.api.machine_segment_surface import MachineSegmentSurface
from pyemmo.api.pyleecan.create_gmsh_surf import create_gmsh_surface
from pyemmo.functions.plot import plot
from tests.api.pyleecan import TEST_API_PYLCN_DATA_DIR


@pytest.fixture(scope="module", autouse=True)
def initialize_gmsh():
    """init gmsh function"""
    gmsh.initialize()
    gmsh.model.add("test_model")
    yield
    gmsh.finalize()


def test_create_gmsh_surface():
    """Function to test ``pyemmo.api.pyleecan.create_gmsh_surface``"""
    geometry_list: List[MachineSegmentSurface] = []
    machine: Machine = load(
        abspath(join(TEST_API_PYLCN_DATA_DIR, "00_prius_machine.json"))
    )
    sym, is_anti_periodic = machine.rotor.comp_periodicity_geo()
    rotor_surfs = machine.rotor.build_geometry(sym=sym, alpha=0)
    lam_surf = create_gmsh_surface(rotor_surfs.pop(0))
    geometry_list.append(lam_surf)
    for surf in rotor_surfs:
        # get pyleecan object for material identification
        pyleecan_obj = get_obj_from_label(machine, surf.label)
        try:
            material = pyleecan_obj.mat_type
        except AttributeError:
            try:
                material = pyleecan_obj.mat_void
            except AttributeError as e:
                raise RuntimeError(
                    f"Could not identify material of surface {surf} from object {pyleecan_obj}."
                ) from e
            except Exception as e:
                raise e
        except Exception as e:
            raise e

        # translating the surface
        pyemmo_surf = create_gmsh_surface(surf)
        pyemmo_surf.plot()
        if any(label in surf.label for label in (MAG_LAB, HOLEM_LAB, HOLEV_LAB)):
            lam_surf.cutOut(pyemmo_surf)
        else:
            geometry_list.append(pyemmo_surf)
    plot(geometry_list)
    assert len(geometry_list) == 8
