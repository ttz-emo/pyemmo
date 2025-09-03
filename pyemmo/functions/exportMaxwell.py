#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied
# Sciences Wuerzburg-Schweinfurt.
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
"""Module to export data to Ansys Maxwell"""
from __future__ import annotations

from os import path


def exportTabMaxwell(data: list, identifier: list[str], filepath: str) -> None:
    """function to export any data in ANSYS Maxwell tab delimited format.

    Args:
        data (list): List of data vectors.
        identifier (list[str]): List of data identifier for Maxwell like
            "Time (s)", "H (A_per_meter)" or "B (tesla)".
        filepath (str): File path to write the results to. File
            extension must be ".tab"!

    Raises:
        ValueError: If extension is not .tab

    Example:

        ..code:: python

            time_data = [4, 5, 6]
            h_data = [1, 2, 3]

            data = [time_data, h_data]
            ids = ["Time (s)", "H (A_per_meter)"]

            file = (
                f"{RES_DIR}\testExportMaxwellData.tab"
            )
            exportTabMaxwell(data, ids, file)
    """
    if len(data) != len(identifier):
        raise ValueError("data and identifier length are not matching!")
    if path.isfile(filepath):
        raise FileExistsError(f"Given .tab file allready exists: {filepath}")
    if not path.isdir(path.dirname(filepath)):
        raise FileNotFoundError(
            f"Parent folder of given file path does not exist: {filepath}"
        )

    # check file path format
    _, ext = path.splitext(filepath)
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
