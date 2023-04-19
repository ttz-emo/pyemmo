"""Module to return requirements of pydraft via pipreqs"""
from os.path import join
import os

PYDRAFT_DIR = r"C:\Users\ganser\AppData\Local\Programs\PyDraft_git\PyDraft\pydraft"
os.system(f"pipreqs {PYDRAFT_DIR} --force")

try:
    with open(join(PYDRAFT_DIR, "requirements.txt"), "r", encoding="utf-8") as reqFile:
        reqs = reqFile.readlines()
    print("\nRequired packages are:\n")
    for req in reqs:
        print(req, end=None)
except FileNotFoundError:
    print(f"Requirements file '{PYDRAFT_DIR}' not found!")
except Exception as exce:
    raise exce
