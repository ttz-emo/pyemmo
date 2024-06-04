import subprocess
from datetime import datetime

"""
Script to run pytest in powershell and save summary to date-marked log.
"""
curr_date = datetime.now().strftime("%Y%m%d_%H%M%S")
subprocess.run(f"powershell.exe (pytest -vv ^| tee ./logs/test_summary_{curr_date}.log)", shell=True)
