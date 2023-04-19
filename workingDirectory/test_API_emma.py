# %% Imports
from os.path import abspath, dirname, isdir, isfile, join, normpath, realpath
from sys import path

# Add Software_V2 to Path so pydraft can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\PyDraft"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%%
from pydraft.api import emma_onelab as api
from pydraft.functions.runOnelab import findGmsh

#%%
# try to find gmsh in system path
gmshExe = findGmsh()
if not gmshExe:  # if gmsh was not found set manually
    gmshExe = r"C:\Users\ganser\AppData\Local\Programs\onelab-Windows64-210904\gmsh.exe"
    print(f"Did not find gmsh executable. Setting it manually to '{gmshExe}'")
else:
    print(f'gmsh exe is "{gmshExe}"')

modelDir = r"C:\Users\ganser\AppData\Local\Programs\PyDraft_git\PyDraft\Results\matlab\Test_1FE1051-4HF11_TherCom"
geoJsonPath = abspath(
    join(
        modelDir,
        "Test_1FE1051-4HF11_TherCom.json",
    )
)
extInfoPath = abspath(
    join(
        modelDir,
        "simuInfo.json",
    )
)
#%%
api.main(geo=geoJsonPath, extInfo=extInfoPath, model=modelDir, gmsh=gmshExe)
