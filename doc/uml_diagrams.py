"""
This module implements a script to create UML diagrams of PyEMMO class structure for
the documentation.
"""

from __future__ import annotations

import subprocess
from os import makedirs
from os.path import isdir, join

from pyemmo.definitions import MAIN_DIR

script_dir = join(MAIN_DIR, "script")
uml_out_dir = join(MAIN_DIR, "..", "doc", "images", "uml")
if not isdir(uml_out_dir):
    makedirs(uml_out_dir)


# # full script class and full package diagram.
# subprocess.check_call(
#     [
#         "pyreverse",
#         "-o",
#         "png",
#         "--output-directory",
#         uml_out_dir,
#         "--only-classnames",
#         "-p",
#         "PyEMMO",
#         MAIN_DIR,
#     ]
# )

# pyemmo subpackage class and module diagrams.
for subpackage in ("script", "api", "functions"):
    subprocess.check_call(
        [
            "pyreverse",
            "-o",
            "dot",
            "--output-directory",
            uml_out_dir,
            "-p",
            f"PyEMMO.{subpackage}",
            join(MAIN_DIR, subpackage),
        ]
    )


# script subpackage class and module diagrams.
for subpackage in ("geometry", "gmsh", "material", "physicals"):
    subprocess.check_call(
        [
            "pyreverse",
            "-o",
            "dot",
            "--output-directory",
            uml_out_dir,
            "-p",
            f"PyEMMO.script.{subpackage}",
            join(script_dir, subpackage),
        ]
    )
