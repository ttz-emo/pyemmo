# %%
from os.path import join
from pyemmo.script.material import material  # , materialManagement
from pyemmo.definitions import ROOT_DIR

matAir = material.Material(name="Air")
matAir.loadMatFromDataBase(
    join(ROOT_DIR, "pyemmo\\script\\material\\Material_new.db"), name="air"
)
matAir.print()
# %%
