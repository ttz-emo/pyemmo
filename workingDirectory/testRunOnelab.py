# %%
from os import path
import sys

try:
    from pydraft.script.script import Script
except:
    try:
        rootname = path.abspath(path.join(path.dirname(__file__), ".."))
    except:
        rootname = (
            "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\Software_V2"
        )
        print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)
    from pydraft.script.script import Script

from pydraft.script.script import default_param_dict
from pydraft.functions.runOnelab import createCmdCommand, findGetDP, findGmsh

#%% testfiles
scriptName = "TTZ_1FE1051-4HF11_TherCom"
testScriptPath = path.abspath(
    path.join(rootname, "workingDirectory", "dummyScrips", scriptName)
)
testProFile = path.abspath(path.join(testScriptPath, scriptName + ".pro"))
# %% create cmd command
myCommand = createCmdCommand(
    onelabFile=testProFile,
    useGUI=False,
    gmshPath=findGmsh(),
    getdpPath=findGetDP(),
    paramDict={"finalrotor_pos": 10},
    postOperations=["GetBOnRadius", "Torque"],
)
print("\n\n" + myCommand)
#%%
