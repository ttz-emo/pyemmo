import subprocess
from datetime import datetime
import os

"""
Script to run pytest in powershell and save summary to date-marked log.
"""

log_path = f".\\integrationTest\\logs"
if not os.path.isdir(log_path):
    os.makedirs(log_path)
curr_date = datetime.now().strftime("%Y%m%d_%H%M%S")

subprocess.run(
    f"powershell.exe (pytest integrationTest/apiTest.py -rA --show-capture=stdout --show-progress -vvv ^| tee ./integrationTest/logs/test_summary_{curr_date}.log)",
    shell=True,
)
