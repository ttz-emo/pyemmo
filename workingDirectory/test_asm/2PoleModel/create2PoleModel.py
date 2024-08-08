"""Script to create ONELAB model of ASM: 1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz"""

import os
from pyemmo.api.json.json import main as api_main
from definitions import MODEL_DIR, MODEL_JSON_FILE

print(MODEL_DIR)

# folder where the model files should be stored:
model_dir = os.path.dirname(__file__)
PARAM_FILE = os.path.join(model_dir, "simuInfo.json")
api_main(
    MODEL_JSON_FILE, PARAM_FILE, model=model_dir, results=os.path.join(model_dir, "res")
)
