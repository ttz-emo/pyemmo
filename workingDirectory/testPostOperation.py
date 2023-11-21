# %%
import os
from os import path
import shutil
from pygetdp import PostOperation
from pygetdp.postoperation import PostopItem
from pyemmo.definitions import ROOT_DIR
from pyemmo.script.script import Script
from pyemmo.script.script import default_param_dict

# %% copy testfile
#TODO: Test Überarbeiten!
# testProFile = path.join(ROOT_DIR, "\workingDirectory\pmsm\Test_SPMSM_Baukasten.pro")
# %% Create PostOperation code
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
# %% Append to the end of the pro file
with open(testProFile, "a") as proFile:
    proFile.write(myPO.code)
# %%
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
    path.abspath(path.join(ROOT_DIR, "workingDirectory", "testPostOperation")),
    default_param_dict,
    None,
)
myScript.addPostOperation(
    quantityName="b",
    name="User Defined PostOperation",
    OnGrid="{(r_AG)*Sin[Pi/nbSlots-$A*Pi/180],(r_AG)*Cos[Pi/nbSlots-$A*Pi/180],0}{0:360/SymmetryFactor,0,0}",
    File=path.abspath(path.join(myScript.getResultsPath(), "b_OnRadius.pos")),
)
print(myScript.postOperation.code)
# %%
