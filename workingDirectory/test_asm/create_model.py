"""Script to create ONELAB model of ASM: 1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz"""

import os
from pyemmo.api.json.json import main as api_main

from definitions import MODEL_JSON_FILE, PARAM_FILE

# folder where the model files should be stored:
model_dir = os.path.dirname(__file__)
api_main(
    MODEL_JSON_FILE,
    PARAM_FILE,
    model=model_dir,
    results=os.path.join(
        model_dir, "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz"
    ),
)
