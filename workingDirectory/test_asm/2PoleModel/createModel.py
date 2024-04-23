"""Script to create ONELAB model of ASM: 1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz"""

import os
from pyemmo.api.json.json import main as api_main
from pyemmo.definitions import ROOT_DIR

MODEL_DIR = os.path.abspath(
    os.path.join(
        ROOT_DIR, "Results/matlab/Test_1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz"
    )
)
print(MODEL_DIR)
MODEL_FILE = os.path.join(
    MODEL_DIR, "Test_1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz.json"
)
PARAM_FILE = os.path.join(MODEL_DIR, "simuInfo.json")
# folder where the model files should be stored:
model_dir = os.path.dirname(__file__)
api_main(
    MODEL_FILE, PARAM_FILE, model=model_dir, results=os.path.join(model_dir, "res")
)
