# %% Imports
import fileinput
from shutil import copyfile
from sys import path
from os import getcwd
from os.path import abspath, dirname, isdir, isfile, join, normpath, realpath
from typing import List

# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)
#%%
from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script import Script
import time

# template file names
parameterTempFileName = join(rootname, "pyemmo", "script", "parameters_template.pro")
machineTempFileName = join(rootname, "pyemmo", "script", "machine_template.pro") 
# script file names
machineFile = join(rootname, "workingDirectory", "test_machine_copy.pro")
paramFile = join(rootname, "workingDirectory", "test_machine_parameters_copy.pro")

# %% Version with FileInput class
# copy templates
startTime = time.time()
copyfile(machineTempFileName, machineFile)
copyfile(parameterTempFileName, paramFile)

with fileinput.FileInput(machineFile, inplace=True) as file:
    # in this case we must iterate through the whole file to read and write every line...
    # This will be time consuming when replacing serveral parameters...
    for line in file:
        print(line.replace("PARAMETER_FILE", '"' + paramFile + '"'), end="")
        # break
endFileInputTime = time.time()
print(f"The FileInput Method took {endFileInputTime-startTime} seconds.")
#%% Version with open - read - close - open - write - close
# open and read file content
with open(machineTempFileName, "r") as tempFile:
    machineCode = tempFile.read()

# modify file content
machineCode = machineCode.replace("PARAMETER_FILE", '"' + paramFile + '"', 1)

# write file content to new file
with open(machineFile, "w") as file:
    file.write(machineCode)
endReadTime = time.time()
print(f"The read-write method took {endReadTime - endFileInputTime} seconds.")
# %%
