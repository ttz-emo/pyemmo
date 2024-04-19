#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""Main module of pyleecan api"""
import os
from typing import Union
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

from ..json.json import main as json_api_main
from .translate_machine import translate_machine
from .create_pyleecan_simulation import create_simulation
from .create_param_dict import create_param_dict


def main(
    pyleecan_machine: Machine,
    model_dir: str,
    gmsh: Union[str, os.PathLike] = "",
    getdp: Union[str, os.PathLike] = "",
):
    simulation = create_simulation(pyleecan_machine, i_d=0, i_q=0, speed=1000)
    # make sure machine type is translatable
    if isinstance(
        pyleecan_machine, (MachineSIPMSM, MachineIPMSM, MachineSyRM)
    ):
        (
            allBands,
            geometryList,
            movingband_r,
            magnetizationDict,
            geo_translation_dict,
        ) = translate_machine(pyleecan_machine)
    else:
        raise ValueError("Machine type is not translatable!")

    paramDict = create_param_dict(
        pyleecan_machine, simulation, movingband_r, magnetizationDict
    )
    json_api_main(
        geo=geo_translation_dict,
        extInfo=paramDict,
        model=model_dir,
        gmsh=gmsh,
        getdp=getdp,
        # results=os.path.join(model_dir, "res")
    )
