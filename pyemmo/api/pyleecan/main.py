"""Main module of pyleecan api"""

import os
import argparse
import logging

from pyleecan.Functions import load
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM

from ...definitions import RESULT_DIR
from .. import logger, ch
from ..json.json import main as json_api_main
from .get_translated_machine import get_translated_machine
from .create_pyleecan_simulation import create_simulation
from .create_param_dict import create_param_dict


def main(
    pyleecan_machine: Machine,
    model_dir: os.PathLike,
    gmsh: os.PathLike = "",
    getdp: os.PathLike = "",
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


if __name__ == "__main__":
    # 1. Check that all argvs are valid!
    parser = argparse.ArgumentParser(
        description="Process Pyleecan machine data (saved as JSON file) to generate a Onelab Simulation."
    )
    parser.add_argument(
        "file",
        help="Path to the Pyleecan-Machine-JSON file",
        type=str,
    )
    # parser.add_argument(
    #     "extInfo",
    #     help="path to the extended info JSON file ('extendedInfo.json')",
    #     type=str,
    # )
    parser.add_argument(
        "--gmsh",
        help="path to the Gmsh executable",
        type=str,
        default="",
    )
    parser.add_argument(
        "--getdp", help="path to the GetDP executable", type=str, default=""
    )
    parser.add_argument(
        "--mod",
        help="path where the model files should be stored. Defaults to {PyEMMO_RESUTLS_DIR}\\pyleecan",
        type=str,
        default=os.path.join(RESULT_DIR, "pyleecan"),
    )
    parser.add_argument(
        "--log",
        help="logging level for execution. Options are: 'error', 'warning', 'info', 'debug'. Default is warning",
        type=str,
        default="WARNING",
    )
    parser.add_argument(
        "-v",
        help="set execution to verbose. Verbosity level equals logging level.",
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()

    # remove commandline handler if verbose
    if args.v:
        logger.removeHandler(ch)

    # set log level
    loglevel = args.log
    logLevelNum = getattr(logging, loglevel.upper(), None)
    if not isinstance(logLevelNum, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logger.setLevel(logLevelNum)

    main(
        pyleecan_machine=load.load(args.file),
        model_dir=args.mod,
        gmsh=args.gmsh,
        getdp=args.getdp,
    )
