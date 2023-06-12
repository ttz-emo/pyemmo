"""Print flowcharts for python files"""
#%% 
import os
from pyflowchart import Flowchart

#%%
testfile = os.path.abspath("testIPMSM.py")
with open(testfile) as f:
    rawCode = f.read()

fChart = Flowchart.from_code(rawCode)
print(fChart.flowchart())