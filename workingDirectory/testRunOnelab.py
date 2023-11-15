# %%
from os import path
from pyemmo.definitions import ROOT_DIR
from pyemmo.functions.runOnelab import createCmdCommand, findGetDP, findGmsh

# %% testfiles
scriptName = "TTZ_1FE1051-4HF11_TherCom"
testScriptPath = path.abspath(
    path.join(ROOT_DIR, "workingDirectory", "dummyScripts", scriptName)
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
# %%
