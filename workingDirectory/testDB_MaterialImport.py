#%%
from sys import path
from os.path import abspath, join, dirname

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\Software_V2"
    # print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)

#%%
from pydraft.script.material import material, materialManagement

matAir = material.Material(name="Air")
matAir.loadMatFromDataBase(
    join(rootname, "pydraft\\script\\material\\Material_new.db"), name="air"
)
matAir.print()
# %%
