import os
import subprocess
from datetime import datetime

from pyemmo.definitions import MAIN_DIR, ROOT_DIR

curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
log_folder = os.path.join(ROOT_DIR, "Results/bandit_log")
if not os.path.isdir(log_folder):
    os.makedirs(log_folder)
with open(os.path.join(log_folder, f"bandit_log_{curr_datetime}.log"), "w") as file:
    subprocess.run(f"bandit -r {MAIN_DIR} -c pyproject.toml", stdout=file, text=True)
