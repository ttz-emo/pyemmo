"""Script to create ONELAB model of ASM: 1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz"""

import os

from definitions import MODEL_DIR, MODEL_JSON_FILE, PARAM_FILE

from pyemmo.api.json.json import main as api_main

print(MODEL_DIR)

# folder where the model files should be stored:
api_main(
    MODEL_JSON_FILE,
    PARAM_FILE,
    model=MODEL_DIR,
    results=os.path.join(MODEL_DIR, "res"),
)
