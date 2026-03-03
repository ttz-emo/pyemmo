#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO, Technical University of
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
"""This module implements the function :func:`extract_onelab_parameters` to get a list
of constants and ONELAB parameters from a list of .geo and .pro files by parsing."""

from __future__ import annotations

import re
import sys
from os.path import abspath


def extract_onelab_parameters(
    file_paths: list[str],
) -> tuple[dict[str, str], dict[str, str]]:
    """
    Extract all Onelab parameters from .geo and .pro files in a `DefineConstant` block.

    Args:
        file_paths (List[str]): List of file paths to .geo and .pro files.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary with file names as keys and nested dictionaries
        where each contains parameter details.
    """
    # Pattern to match DefineConstant parameters
    define_constant_pattern = re.compile(
        r"""
            (?P<prefix>[\/]{2,})?[ ]*     # catch // if DefineConstant is commented
            (?:\bDefineConstant\b\s*\[) # non-catch 'DefineConstant' + [
            # capture everything in brackets:
            (?P<code>[\w\s\,\.\*\/\[\]\=\{\}\(\)\"\'\-\+\&\^\|\!\?\°\<\>\:\²\³]*)
            (?:\] *\;) # non-capture final '];'
            """,
        re.VERBOSE,
    )

    # Pattern to extract key-value pairs within the DefineConstant

    const_pattern = re.compile(
        r"""(?P<prefix>[\/]{2,})?        # catch prefix with double backslash for comment
        (?P<name>\w+)                   # catch constant name
        \s*=\s*                         # equal sign must exactly be 1
        # catch value: word or sign + optional single forwart slash for division +
        # another word or number after division
        (?P<value>[\w \(\)\[\]*\-+]+\/?[\w \(\)\[\]*\-+]*)
        \s*(\,|\n|\/{2})""",  # line ends with comma, newline or comment (double forward slash)
        re.VERBOSE,
    )

    # Too difficult using re... Use function `find_onelab_params` instead!
    # onelab_const_pattern = re.compile(
    #     r"""(?P<prefix>[\/]{2,})?       # catch prefix with double backslash for comment
    #     (?P<name>\w+)                   # catch constant name
    #     \s*=\s*                         # equal sign must exactly be 1
    #     # catch value: word or sign + optional single forwart slash for division +
    #     # another word or number after division
    #     \{(?P<value>[\w \(\)\[\]*\-+]+\/?[\w \(\)\[\]*\-+]*)\}
    #     \s*(\,|\n|\/{2})""",  # line ends with comma, newline or comment (double forward slash)
    #     re.VERBOSE,
    # )

    constants = {}
    parameters = {}

    for file_path in file_paths:
        with open(file_path, encoding="utf-8") as file:
            # Find all DefineConstant blocks
            constant_blocks = define_constant_pattern.findall(file.read())

            const = {}
            for block_prefix, block in constant_blocks:
                if "//" in block_prefix:
                    continue  # pass block
                # Extract individual parameters within DefineConstant block
                # const_lines = const_pattern.findall(block)  # for debugging
                for match in const_pattern.finditer(block):
                    if match.group("prefix") and "//" in match.group("prefix"):
                        continue  # skip value
                    name = match.group("name")
                    value = match.group("value").strip()
                    const[name] = value
                onelab_params = find_onelab_params(block)

                parameters = parameters | onelab_params
                constants = constants | const
    return constants, parameters


def find_onelab_params(text: str) -> dict[str, str]:
    """It was too dificult to turn the onelab parameter syntax into a regular expression
    because of the multiply occuring {}-characters.
    This function uses regex to find the start of a parameter string like:

        `name = { ... }`

    then is searches the string until the final closing bracket '}' occurs.
    Finally is splits the result at the newlines, trims any whitespaces and
    removes comments starting with double slash '//'.
    """
    # start pattern for onelab string
    op_pat = re.compile(
        r"""(?P<prefix>[\/]{2,})?[ ]*(?P<name>\w+)\s*=\s*\{""",
    )
    onelab_params = {}  # init params
    # opstarts = op_pat.findall(text)
    for match in op_pat.finditer(text):
        if match.group("prefix") and "//" in match.group("prefix"):
            # if the parameters starts with a comment
            continue  # skip value
        name = match.group("name")  # get param value from regex
        nbr_close_brackets = (
            1  # set number of brackets to 1 because first { is included
        )
        # in regex
        value = ""  # add first bracket manually
        for c in text[match.span()[1] :]:
            if c == "{":
                # if another opening { occurs, increase the number of brackets to close
                nbr_close_brackets += 1
            elif c == "}":
                nbr_close_brackets -= 1
            if nbr_close_brackets == 0:
                break  # break loop if final bracket was found
            value += c  # add char to string:
            if nbr_close_brackets < 0:
                raise RuntimeError("Number of close brackets { to find cannot be < 0!")
        # strip of newline chars, whitespaces and comments with //
        striped = ""
        for line in value.split("\n"):
            line = line.strip()
            if "//" in line:
                try:
                    striped += line.split("//")[0]
                except:
                    pass
            else:
                striped += line
        # set param value
        onelab_params[name] = striped
    return onelab_params


if __name__ == "__main__":
    # Example usage:
    files = sys.argv[1:]
    if not files:
        files = [abspath("./pyemmo/script/machine_template.pro")]
    if files:
        constants, parameters = extract_onelab_parameters(files)
        for param_name, params in constants.items():
            print(f"Constant  {param_name:<20}: {params}")
        for param_name, params in parameters.items():
            print(f"Parameter {param_name:<24}: {params}")
