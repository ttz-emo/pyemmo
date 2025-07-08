# %%
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Module for test function to check existance of model files"""
import os
from os.path import isdir, join


def check_model_files(model_dir: os.PathLike, model_name: str):
    """Check a model directory for the existance of the model files.
    Model files are:

    1. model_name + "_param.geo"
    2. model_name + ".geo"
    3. model_name + ".pro"
    4. "machine_magstadyn_a"

    Args:
        model_dir (os.PathLike): File path to model directory.
        model_name (str): Model name to identify the model files.
    """
    model_file = join(model_dir, model_name + "_param.geo")
    assert os.path.isfile(model_file), f"Model file {model_file} did not exist."
    for ext in ("geo", "pro"):
        model_file = join(model_dir, model_name + "." + ext)
        assert os.path.isfile(model_file), f"Model file {model_file} did not exist."
    model_file = join(model_dir, "machine_magstadyn_a.pro")
    assert os.path.isfile(model_file)


def check_model_result_files(
    model_dir: os.PathLike, model_name: str, result_dir_name: str = ""
):
    """Check a model directory for ONELAB simulation result files and folder
    Model files are:

    1. model_name + ".msh"
    2. model_name + ".pre"
    3. model_name + ".res"
    4. result_dir_name (Defaults to "res_" + model_name)

    Args:
        model_dir (os.PathLike): File path to model directory.
        model_name (str): Model name to identify the simulation files.
        result_dir_name (str, optional): Result directory name. Defaults to
        ("res_" + model_name). This can be specified in the model generation
        process.
    """
    for ext in ("msh", "pre", "res"):
        model_file = join(model_dir, model_name + "." + ext)
        assert os.path.isfile(model_file), f"ONELAB file {model_file} did not exist."
    if not result_dir_name:
        result_dir_name = "res_" + model_name
    assert isdir(
        join(model_dir, result_dir_name)
    ), f"Result directory {result_dir_name} did not exist."

    # TODO: Make sure results files exist depented on the simulation parameters
