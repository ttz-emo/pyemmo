"""Main module of pyleecan api"""

import os
import argparse
import logging

from pyleecan.Functions import load

from ...definitions import RESULT_DIR
from .. import logger, ch
from .main import main

if __name__ == "__main__":
    # 1. Check that all argvs are valid!
    parser = argparse.ArgumentParser(
        description=(
            "Process Pyleecan machine data (saved as JSON file) to generate "
            "a Onelab Simulation."
        )
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
