#%%
from sys import path
from os.path import *

rootname = abspath(join(dirname(__file__), ".."))
print(rootname)
path.append(rootname)
# %%
