import os

from pyemmo.definitions import ROOT_DIR

# Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz
MODEL_NAME = "Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz"
MODEL_DIR = os.path.abspath(os.path.dirname(__file__) + r"\..")
print(MODEL_DIR)
MODEL_JSON_FILE = os.path.abspath(
    os.path.join(MODEL_DIR + r"\..", "1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz.json")
)
PARAM_FILE = os.path.join(MODEL_DIR, "simuInfo.json")
