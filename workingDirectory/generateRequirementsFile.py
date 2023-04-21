"""Module to return requirements of pyemmo via pipreqs"""
from os.path import join
import os

pyemmo_DIR = r"C:\Users\ganser\AppData\Local\Programs\pyemmo_git\pyemmo\pyemmo"
os.system(f"pipreqs {pyemmo_DIR} --force")

try:
    with open(join(pyemmo_DIR, "requirements.txt"), "r", encoding="utf-8") as reqFile:
        reqs = reqFile.readlines()
    print("\nRequired packages are:\n")
    for req in reqs:
        print(req, end=None)
except FileNotFoundError:
    print(f"Requirements file '{pyemmo_DIR}' not found!")
except Exception as exce:
    raise exce
