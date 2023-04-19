# %%
import os
from os import path
import shutil
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

#%% copy testfile
testProFile = shutil.copyfile(
    src=path.abspath(path.join(rootname, "Results", "TestIPMSM", "Test_IPMSM.pro")),
    dst=path.abspath(path.join(rootname, "workingDirectory", "testPostOperation.pro")),
)
#%% Create PostOperation code
from pygetdp import PostOperation
from pygetdp.postoperation import PostopItem

myPO = PostOperation()
# kwargsDict = 'Print[ bn, OnElementsOf Rotor_Magnets, Name "B_normal (Magnets)", File StrCat[ResDir, "Bn_Mag", ExtGmsh]]'
poItem = myPO.add(
    Name="testName",
    NameOfPostProcessing="MagStaDyn_a_2D",
    Hidden="0",
    Format="Gmsh",
    TimeValue="{0,0.1,0.2,0.3}",
)
# poBase = poItem.add()
# poBase.add(quantity="myQuantity", OnElementsOf="Domain", File="TestFile")
poItem.add().add(
    quantity="myQuantity",
    OnElementsOf="Domain",
    File='StrCat[ResDir,"brad_Domain",ExtGmsh]',
    AppendTimeStepToFileName="Flag_SaveAllSteps",
    LastTimeStepOnly="",
)
print(myPO.code)
#%% Append to the end of the pro file
with open(testProFile, "a") as proFile:
    proFile.write(myPO.code)
#%%
os.remove(testProFile)
# %%
default_param_dict = {
    "init_rotor_pos": 0,
    "angle_increment": 1,
    "final_rotor_pos": 90,
    "Id_eff": 0,
    "Iq_eff": 0,
    "rot_speed": 1000,
    "park_angle_offset": 0,
    "analysis_type": 1,
    "magTemp": 20,
}
myScript = Script(
    "testPostOperation",
    path.abspath(path.join(rootname, "workingDirectory")),
    default_param_dict,
    None,
)
myScript.addPostOperation(
    quantityName="b",
    name="User Defined PostOperation",
    OnGrid="{(r_AG)*Sin[Pi/nbSlots-$A*Pi/180],(r_AG)*Cos[Pi/nbSlots-$A*Pi/180],0}{0:360/SymmetryFactor,0,0}",
    File=path.abspath(
        path.join(
            rootname, "workingDirectory", "testPostOperationRes", "b_OnRadius.pos"
        )
    ),
)
print(myScript.postOperation.code)
# %%
