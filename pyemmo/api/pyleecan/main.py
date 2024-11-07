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

from __future__ import annotations

import os

import gmsh as gmsh_api
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSCIM import MachineSCIM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

from ..json.json import main as json_api_main
from . import PyleecanMachine
from .create_param_dict import create_param_dict
from .create_pyleecan_simulation import create_simulation
from .translate_machine import translate_machine


def main(
    pyleecan_machine: PyleecanMachine,
    model_dir: str,
    gmsh: str | os.PathLike = "",
    getdp: str | os.PathLike = "",
    use_gui: bool = True,
):
    """Main of pyleecan api.

    This uses the
    :func:`~pyemmo.api.pyleecan.get_translated_machine.get_translated_machine`
    function to create the geometry and simulation dicts for the
    :mod:`PyEMMO JSON-API <pyemmo.api.json.json>` interface and directly build
    the model by invoking the JSON-API.

    Args:
        pyleecan_machine (PyleecanMachine): Pyleecan machine object to translate
        model_dir (str): Path to the directory where the model files should be
            stored.
        gmsh (Union[str ,os.PathLike], optional): Path to a Gmsh executable.
            Defaults to "".
            If none is given, the program tries to find a exe.
        getdp (Union[str, os.PathLike], optional): Path to a Gmsh executable.
            Defaults to "". If none is given, the program tries to find a exe.

    Raises:
        ValueError: If incompatible Pyleecan Machine type is given.
            Currently only :class:`MachineSIPMSM`, :class:`MachineIPMSM`
            and :class:`MachineSyRM` work.
    """
    simulation = create_simulation(pyleecan_machine, i_d=0, i_q=0, speed=1000)
    # make sure machine type is translatable
    if isinstance(
        pyleecan_machine,
        (MachineSIPMSM, MachineIPMSM, MachineSyRM, MachineSCIM),
    ):
        # create new gmsh model in case api is called multiple times:
        gmsh_api.model.add(pyleecan_machine.name)
        (
            movingband_r,
            magnetizationDict,
            geo_translation_dict,
        ) = translate_machine(pyleecan_machine)
    else:
        raise ValueError("Machine type is not translatable!")

    paramDict = create_param_dict(
        pyleecan_machine, simulation, movingband_r, magnetizationDict
    )
    paramDict["flag_openGUI"] = use_gui

    script_obj = json_api_main(
        geo=geo_translation_dict,
        extInfo=paramDict,
        model=model_dir,
        gmsh=gmsh,
        getdp=getdp,
        # results=os.path.join(model_dir, "res")
    )
    return script_obj
