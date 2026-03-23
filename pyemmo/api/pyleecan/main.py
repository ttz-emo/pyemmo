#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
Core module of PYLEECAN api which contains the :func:`main` function to build a ONELAB
model from a PYLEECAN machine object.
"""

from __future__ import annotations

import logging
import os

import gmsh as gmsh_api

from ... import use_pyleecan
from ...functions.clean_name import clean_name
from ..json.json import main as json_api_main

if use_pyleecan:
    from pyleecan.Classes.Machine import Machine
    from pyleecan.Classes.MachineIPMSM import MachineIPMSM
    from pyleecan.Classes.MachineLSPM import MachineLSPM
    from pyleecan.Classes.MachineSCIM import MachineSCIM
    from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
    from pyleecan.Classes.MachineSyRM import MachineSyRM
    from pyleecan.Functions.load import load  # pylint:disable=no-name-in-module

    from . import PyleecanMachine
    from .create_param_dict import create_param_dict
    from .create_pyleecan_simulation import create_simulation
    from .translate_machine import translate_machine
else:
    raise ModuleNotFoundError(
        "PYLEECAN is not available! Please install PYLEECAN first."
    )


def main(
    pyleecan_machine: PyleecanMachine | str,
    model_dir: str,
    gmsh: str | os.PathLike = "",
    getdp: str | os.PathLike = "",
    use_gui: bool = True,
    symmetry: int | None = None,
):
    """Main of PYLEECAN api to build a ONELAB model from a PYLEECAN machine.

    This uses the
    :func:`~pyemmo.api.pyleecan.translate_machine.translate_machine`
    function to create the geometry and simulation dicts for the
    :mod:`PyEMMO JSON-API <pyemmo.api.json.json>` interface and directly build
    the model by invoking the JSON-API.

    Args:
        pyleecan_machine (PyleecanMachine | str): PYLEECAN machine object to translate
            or path to machine json file.
        model_dir (str): Path to the directory where the model files should be
            stored.
        gmsh (Union[str ,os.PathLike], optional): Path to a Gmsh executable.
            Defaults to "".
            If none is given, the program tries to find a exe.
        getdp (Union[str, os.PathLike], optional): Path to a Gmsh executable.
            Defaults to "". If none is given, the program tries to find a exe.
        use_gui (): Flag to open the GUI after the model generation has finished.
        symmetry (int | None): Manually set symmetry factor. If None the api will
            calculate and use the highest symmetry from geometry and winding information.


    Raises:
        ValueError: If incompatible PYLEECAN Machine type is given.
            Currently only :class:`MachineSIPMSM`, :class:`MachineIPMSM`,
            :class:`MachineSCIM`, :class:`MachineLSPM`
            and :class:`MachineSyRM` work.
    """
    logger = logging.getLogger(__name__)

    if not isinstance(pyleecan_machine, Machine) and isinstance(pyleecan_machine, str):
        pyleecan_machine = load(pyleecan_machine)
    # make sure machine type is translatable
    if isinstance(
        pyleecan_machine,
        (MachineSIPMSM, MachineIPMSM, MachineSyRM, MachineSCIM, MachineLSPM),
    ):
        if not gmsh_api.isInitialized():
            gmsh_api.initialize()

        # supress output of log messages to console.
        # See https://gitlab.onelab.info/gmsh/gmsh/-/issues/1901
        # Use gmsh.logger.start(), gmsh.logger.get(), gmsh.logger.stop() to catch logs.
        logger.debug("Setting gmsh option General.Terminal to 0.")
        gmsh_api.option.setNumber("General.Terminal", 0)

        # add new gmsh model in case api is called multiple times:
        model_name = clean_name(pyleecan_machine.name)
        gmsh_api.model.add(model_name)

        # Create model parameter dict
        simulation = create_simulation(pyleecan_machine, i_d=0, i_q=0, speed=1000)
        paramDict = create_param_dict(pyleecan_machine, simulation, symmetry)
        paramDict["flag_openGUI"] = use_gui

        geo_translation_dict = translate_machine(pyleecan_machine)
    else:
        raise NotImplementedError(
            f"Machine type '{type(pyleecan_machine)}' is not translatable!"
        )

    script_obj = json_api_main(
        geo=geo_translation_dict,
        extInfo=paramDict,
        model=model_dir,
        gmsh=gmsh,
        getdp=getdp,
        # results=os.path.join(model_dir, "res")
    )
    return script_obj
