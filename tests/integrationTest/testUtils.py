#
# Copyright (c) 2018-2024 M. Schuler & Vu Nguyen, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""TODO: Module docstring"""

import glob
import os
import re
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime

from pyemmo.definitions import TEST_DIR  # ROOT_DIR,

from . import LOGGER


def updateConfig(test_type: str = "", test_id: int = "", test_case: str = ""):
    """
    Function to update config file to generate proper test file name
    """

    curr_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    parser = ConfigParser()
    config_path = os.path.join(os.path.abspath("."), "pytest.ini")
    config_path = os.path.join(os.path.abspath("."), "pytest.ini")
    parser.read(config_path)
    if test_type == "":
        dest_name = ""
    else:
        dest_name = (
            f"logs/{test_type}/{curr_datetime}/test_{test_id}_{test_case}/.log"
        )
    parser.set("pytest", "log_file", dest_name)

    with open(config_path, "w+") as config_file:
        parser.write(config_file)
    return curr_datetime, dest_name


def messagePrinter(msg: str = "Assert OK"):
    LOGGER.info(msg)
    return True


def count_files(folder_path: str) -> dict:
    """
    Function to count files of each type in a path.
    Args: folder_path: path to count in. Needs to be abs path to the dest folder
    Output: n-items Dict
        - 1st entry being folder_path,
        - 2nd till n-th entries: key = file type, value = count
    Output: n-items Dict
        - 1st entry being folder_path,
        - 2nd till n-th entries: key = file type, value = count
    """
    file_type_list_raw = glob.glob(os.path.join(folder_path, "*.*"))
    file_type_list = [
        x.split(".")[1]
        for x in [x.split("\\")[-1] for x in file_type_list_raw]
    ]
    file_type_list = [
        x.split(".")[1]
        for x in [x.split("\\")[-1] for x in file_type_list_raw]
    ]
    file_type_counter = defaultdict(list)
    file_type_counter["dir"] = folder_path
    for file_type in file_type_list:
        if file_type_counter[file_type] == []:
            file_type_counter[file_type] = 1
        else:
            file_type_counter[file_type] += 1
    return file_type_counter


def fileParser(raw_path: str):
    """
    Returns a list of line-by-line breakdown of file content, with comments removed.
    """
    comment_indicators = ["//"]
    exclude_indicators = [
        "Color",
        "PATH_RES",
    ]  # exclude lines whose values always get updated along with files
    with open(raw_path) as file:
        content = file.read()
        content_lines = content.split(";")
        temp = []
        # result = {}
        for line in content_lines:
            delete_target = []
            for ind in comment_indicators:
                delete_target += re.findall(f"{ind}.*\n*", line)
            for targ in delete_target:
                line = line.replace(targ, "")
            line = line.replace("\n", "")
            line = line.replace("\n", "")
            exclude_flags = [x for x in exclude_indicators if x in line]
            if exclude_flags == []:
                temp.append(line)
    return temp

    # TODO: parse result into things
    # for line in temp:
    #     cleaned = line.replace("\n","").replace(" ","").replace("\t","")
    #     if (cleaned.find("[")!=-1):
    #         # print(cleaned.find("["))
    #         # print(cleaned)
    #         split_index = cleaned.find("[")
    #         a = [cleaned[:split_index], cleaned[split_index+1 : -2]]
    #     else:
    #         a = cleaned.split("=")

    #     result[a[0]] = a[1]
    # TODO: parse result into things
    # for line in temp:
    #     cleaned = line.replace("\n","").replace(" ","").replace("\t","")
    #     if (cleaned.find("[")!=-1):
    #         # print(cleaned.find("["))
    #         # print(cleaned)
    #         split_index = cleaned.find("[")
    #         a = [cleaned[:split_index], cleaned[split_index+1 : -2]]
    #     else:
    #         a = cleaned.split("=")

    #     result[a[0]] = a[1]


def fileFilter(file_list: list, target_types: list) -> list:
    get_type = lambda x: x.split("\\")[-1].split(".")[-1]
    result = [file for file in file_list if get_type(file) in target_types]
    return result


def make_test_cases(test_type: str, fixed_test_flg: bool = False):
    """
    Create a list of tuples of test ids & test cases based on files in test data folder
    """
    # test_cases = {}
    headers = "test_id, test_case"
    # test_cases = {}
    test_cases_from_files = [headers]
    test_files = glob.glob(os.path.join(TEST_DIR, "data", test_type, "*.json"))
    test_names = list(
        map(
            lambda x: x.split(".")[0],
            map(lambda x: x.split("\\")[-1], test_files),
        )
    )
    for test_id, name in enumerate(test_names):
        # test_cases[id] = name
        test_cases_from_files.append((test_id, name))

    # test_cases_fixed = {
    #     0: "IPMSM_B",
    #     1: "SPMSM_002",
    #     2: "SPMSM_003",
    #     3: "Toyota_Prius",
    # }

    test_cases_fixed = [headers]
    if test_type == "api\\pyleecan":
        test_cases_fixed = test_cases_fixed + [
            (0, "IPMSM_B"),
            (1, "SPMSM_002"),
            (2, "SPMSM_003"),
            (3, "Toyota_Prius"),
        ]

    if fixed_test_flg:
        return test_cases_fixed
    else:
        return test_cases_from_files
