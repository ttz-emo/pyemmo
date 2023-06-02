# %% Imports
from sys import path
from os.path import abspath, dirname, isfile, join
import json

# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
# from pyemmo.script.script import Script
# from pyemmo.script.geometry.primaryLine import PrimaryLine
# from pyemmo.script.geometry.slaveLine import SlaveLine
# from pyemmo.script.geometry.limitLine import LimitLine
# from pyemmo.script.geometry.rotor import Rotor
# from pyemmo.script.geometry.stator import Stator
# from pyemmo.script.geometry.machineAllType import MachineAllType
from pyemmo.api.json import main
from pyemmo.functions.runOnelab import findGmsh

# import subprocess
# from matplotlib import pyplot as plt
# import gmsh

# %%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')

workingDir = abspath(join(rootname, "Results", "Test_API_JSON"))
modelFileDir = join(workingDir, "model_files")
geoJsonFile = join(workingDir, "test_API_geometry.json")
infoJsonFile = join(workingDir, "test_API_simuInfo.json")
# %% NEW API ALGO
# check if json files exist
if isfile(geoJsonFile) and isfile(infoJsonFile):
    # call main with file path:
    main(geoJsonFile, infoJsonFile, modelFileDir)

#     # load json as dict and call main with dict
#     with open(geoJsonFile, "r", encoding="utf-8") as jf:
#         geoDictList = json.load(jf)
#     with open(infoJsonFile, "r", encoding="utf-8") as jf:
#         infoDict = json.load(jf)
#     main(geoDictList, infoDict, modelFileDir)
else:
    raise (
        FileNotFoundError(
            f"Given json file(s) did not exist! Check '{geoJsonFile}' or '{infoJsonFile}'."
        )
    )

#%%
