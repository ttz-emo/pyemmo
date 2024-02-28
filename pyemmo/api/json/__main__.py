import argparse
import logging
from ...definitions import RESULT_DIR
from .. import logger, ch
from .json import main

# 1. Check that all argvs are valid!
parser = argparse.ArgumentParser(
	description="Process Motor-JSON files to generate a Onelab Simulation."
)
parser.add_argument(
	"geo",
	help="path to the JSON geometry file ('geometry.json')",
	type=str,
)
parser.add_argument(
	"extInfo",
	help="path to the extended info JSON file ('extendedInfo.json')",
	type=str,
)
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
	help="path where the model files should be stored",
	type=str,
	default=RESULT_DIR,
)
parser.add_argument(
	"--res",
	help="path where the simulation results should be stored",
	type=str,
	default="",
)

parser.add_argument(
	"--log",
	help="logging level for execution. Options are: error, warning, info, debug. default is warning",
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
	geo=args.geo,
	extInfo=args.extInfo,
	gmsh=args.gmsh,
	getdp=args.getdp,
	model=args.mod,
	results=args.res,
)
