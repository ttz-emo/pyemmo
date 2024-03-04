"""Main module of pyleecan api"""
import os
from typing import Union
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

from ..json.json import main as json_api_main
from .get_translated_machine import get_translated_machine
from .create_pyleecan_simulation import create_simulation
from .create_param_dict import create_param_dict


def main(
    pyleecan_machine: Machine,
    model_dir: str,
    gmsh: Union[str ,os.PathLike] = "",
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
        ) = get_translated_machine(pyleecan_machine)
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
