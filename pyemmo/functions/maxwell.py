#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""Module to import data from Ansys Maxwell"""
from __future__ import annotations

import csv
import os

import numpy as np

from ..definitions import RESULT_DIR
from ..script.material.material import Material
from . import clean_name


def import_tab(filepath: str) -> tuple[list[str], np.ndarray]:
    """Function to import data from an ANSYS Maxwell tab delimited file.

    Args:
        filepath (str): File path to read the data from. File extension must be ".tab"!

    Raises:
        ValueError: If extension is not .tab or file does not exist.

    Returns:
        Tuple[list[str], numpy.ndarray]]: A tuple containing a list of identifiers and
            a corresponding array of data.

    Example usage:

    .. code::

        file = f"{RES_DIR}/testExportMaxwellData.tab"
        ids, data = importTabMaxwell(file)
        print(ids)  # Should print the list of identifiers
        print(data)  # Should print the data array
    """
    # Check file path
    if not os.path.isfile(filepath):
        raise ValueError(f"File does not exist: {filepath}")

    _, ext = os.path.splitext(filepath)
    if ext != ".tab":
        raise ValueError("Wrong extension for Maxwell data import: " + ext)

    # Read the first line of the file
    with open(filepath, encoding="utf-8") as tabFile:
        line = tabFile.readline()
    # Extract identifiers from the first line
    identifiers = [id.strip('"\n') for id in line.split("\t")]

    data = np.loadtxt(filepath, dtype=float, skiprows=1, delimiter="\t")

    return identifiers, data


def import_csv(filepath: str) -> tuple[list[str], np.ndarray]:
    """Function to import data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Raises:
        FileNotFoundError: If the file at the given filepath does not exist.

    Returns:
        Tuple[List[str], np.ndarray]: A tuple containing a list of headers
            and a array of data values.

    Example usage:

    .. code::

        file = 'path_to_your_file.csv'
        headers, data = import_csv_data(file)
        print(headers)  # Should print the column headers
        print(data)     # Should print the rows of data
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File does not exist: {filepath}")

    headers = []
    rows = []

    with open(filepath, encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the first line as headers
        rows = list(csv_reader)  # Read the remaining rows

    # convert string array to numpy
    rows = np.array(rows, dtype=float)
    return headers, rows


def export_BH(material: Material, filepath: str = None) -> None:
    """function to export the BH-Curve in ANSYS Maxwell readable format.

    Args:
        material (Material): TODO
        filepath (str, optional): File path to write the results to. File
            extension must be ".tab"! Defaults to
            PYEMMO_RESULTS_FOLDER/MATERIAL_NAME_BH.tab .
    """
    if material.linear:
        raise ValueError(
            f"Material {material.name} is linear! Can not export BH curve!"
        )
    bh = material.BH
    b = bh[:, 0]
    h = bh[:, 1]
    header = ["H (A_per_meter)", "B (tesla)"]
    if not filepath:
        filepath = os.path.join(
            RESULT_DIR, clean_name.clean_name(material.getName()) + "_BH.tab"
        )
    export_tab([h, b], header, filepath)


def export_tab(data: list, identifier: list[str], filepath: str) -> None:
    """function to export any data in ANSYS Maxwell tab delimited format.

    Args:
        data (list): List of data vectors.
        identifier (list[str]): List of data identifier for Maxwell like
            \"Time (s)\", \"H (A_per_meter)\" or \"B (tesla)\".
        filepath (str): File path to write the results to. File
            extension must be ".tab"!

    Raises:
        ValueError: If extension is not .tab

    Example:
        >>> time = [4, 5, 6]  # time in seconds
        >>> H = [1, 2, 3]  # H field data in A/m
        >>> data = [time_data, h_data]
        >>> ids = ["Time (s)", "H (A_per_meter)"]
        >>> file = f"{RES_DIR}\\testExportMaxwellData.tab"
        >>> exportTabMaxwell(data, ids, file)

    """
    if len(data) != len(identifier):
        raise ValueError("data and identifier length are not matching!")
    if os.path.isfile(filepath):
        raise FileExistsError(f"Given .tab file allready exists: {filepath}")
    if not os.path.isdir(os.path.dirname(filepath)):
        raise FileNotFoundError(
            f"Parent folder of given file path does not exist: {filepath}"
        )

    # check file path format
    _, ext = os.path.splitext(filepath)
    if ext != ".tab":
        raise ValueError("Wrong extension for bh curve export: " + ext)

    fileContent = ""
    for ident in identifier:
        fileContent += '"' + ident + '"\t'
    fileContent = fileContent[:-1]
    fileContent += "\n"
    for i in range(len(data[0])):
        for dataVector in data:
            fileContent += f"{dataVector[i]}\t"
        fileContent = fileContent[:-1]
        fileContent += "\n"

    with open(filepath, encoding="utf-8", mode="w") as tabFile:
        tabFile.write(fileContent)
