#%% Add the top folder to the path so the software is recognized without being installed (as a package)
from sys import path
from os.path import abspath, join, dirname

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\Software_V2"
    # print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%% test database
from pydraft.script.material import materialManagement
from pydraft.functions import xml2pyDraft
from pydraft.definitions import ROOT_DIR


dataBaseName = "Material_new.db"

# matArray = xml2pyDraft.getMaterialArray(join(ROOT_DIR, "pydraft\\script\\material", ))
#%%
for mat in matArray:
    try:
        conductivity = mat["conductivity"]
    except KeyError:
        conductivity = 0

    try:
        relativePermeability = mat["relativePermeability"]
    except KeyError:
        relativePermeability = 0

    try:
        BH = mat["BH"]
    except KeyError:
        BH = None

    # materialManagement.addMaterial(
    #     dataBase, mat["name"], conductivity, relativePermeability, None, BH
    # )
