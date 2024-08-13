import json
import os

from pyemmo.definitions import ROOT_DIR


def test_created_json():
    print("checking json..")
    json_path = os.path.join(ROOT_DIR, "pyemmo/script/material/material_json")
    for file_name in os.listdir(json_path):
        print(f"checking {file_name}..")
        with open(os.path.join(json_path, file_name)) as file:
            mat = json.load(file)
        assert (len(mat["BHCurve"]) > 0 and mat["linear"] == False) or (
            len(mat["BHCurve"]) == 0 and mat["linear"]
        ), f"error: linear and BH curve mismatch found in {file_name}"
        print(f"checking {file_name} done")
    print("check done.")


if __name__ == "__main__":
    test_created_json()
