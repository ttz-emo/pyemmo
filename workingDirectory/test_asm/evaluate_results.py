# %%
import os
import json
import numpy as np

# from runSim import NumpyEncoder, proFile


# class NumpyDecoder(json.JSONDecoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return json.JSONDecoder(self, obj)


proFile = r"C:\Users\ganser\AppData\Local\Programs\pyemmo/Results/matlab/Test_1PH8135-1_D0_W92_P14k4W_ohneRotNutSchlitz\Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz.pro"

RES_DIR = os.path.join(
    os.path.dirname(proFile),
    "res_Test_1PH8135_1_D0_W92_P14k4W_ohneRotNutSchlitz",
)
resId = "240320_01"

# with open(
#     os.path.join(RES_DIR, resId, f"{resId}.json"),
#     "r",
#     encoding="utf-8",
# ) as jFile:
#     out_dict = json.load(jFile, indent=4, cls=NumpyEncoder)

out_dict = json.loads(os.path.join(RES_DIR, resId, f"{resId}.json"))

# %%
