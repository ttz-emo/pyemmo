#%% 
import json
from os import path
filepath = path.abspath(path.join(path.dirname(__file__),"extendedInfo.json"))
#%%
with open(filepath, encoding='utf-8') as jsonFile:
    content = json.load(jsonFile)
    print(content[0])

#%%
filepath = path.abspath(path.join(path.dirname(__file__),"geometry.json"))
with open(filepath, encoding='utf-8') as jsonFile:
    content = json.load(jsonFile)
    print(content[0])

# %%
