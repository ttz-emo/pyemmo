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


def import_tab_maxwell(filepath: str) -> tuple[list[str], list[list[str]]]:
    """Function to import data from an ANSYS Maxwell tab delimited file.

    Args:
        filepath (str): File path to read the data from. File extension must be ".tab"!

    Raises:
        ValueError: If extension is not .tab or file does not exist.

    Returns:
        Tuple[list[str], list[list[str]]]: A tuple containing a list of identifiers and
                                            a list of data vectors.

    Example usage:

    .. code::

        file = f"{RES_DIR}/testExportMaxwellData.tab"
        ids, data = importTabMaxwell(file)
        print(ids)  # Should print the list of identifiers
        print(data)  # Should print the list of data vectors
    """
    # Check file path
    if not os.path.isfile(filepath):
        raise ValueError(f"File does not exist: {filepath}")

    _, ext = os.path.splitext(filepath)
    if ext != ".tab":
        raise ValueError("Wrong extension for Maxwell data import: " + ext)

    # Read the content of the file
    with open(filepath, encoding="utf-8") as tabFile:
        lines = tabFile.readlines()

    # Extract identifiers from the first line
    identifiers = [id.strip('"\n') for id in lines[0].split("\t")]

    # Extract data from the remaining lines
    data = []
    for line in lines[1:]:
        values = line.strip().split("\t")
        data.append(values)

    # Transpose the data to match the format
    data = list(map(list, zip(*data)))

    return identifiers, data


def import_csv_data(filepath: str) -> tuple[list[str], list[list[str]]]:
    """Function to import data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Raises:
        FileNotFoundError: If the file at the given filepath does not exist.

    Returns:
        Tuple[List[str], List[List[str]]]: A tuple containing a list of headers
                                           and a list of rows.

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
        rows = [row for row in csv_reader]  # Read the remaining rows

    return headers, rows
