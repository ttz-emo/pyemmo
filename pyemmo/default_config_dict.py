#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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
"""Module for default config dict. Copied from Pyleecan project!"""
# Default config_dict
default_config_dict = {"MAIN": {}, "GUI": {}, "PLOT": {}}

default_config_dict["MAIN"]["MACHINE_DIR"] = ""
default_config_dict["MAIN"]["MATLIB_DIR"] = ""
# Name of the color set to use
default_config_dict["PLOT"]["COLOR_DICT_NAME"] = "default_color_dict.json"
default_config_dict["PLOT"]["COLOR_DICT"] = {}
default_config_dict["PLOT"]["FONT_NAME"] = ""
default_config_dict["PLOT"]["FONT_FAMILY_PYVISTA"] = "courier"
default_config_dict["PLOT"]["FONT_SIZE_TITLE"] = 12
default_config_dict["PLOT"]["FONT_SIZE_LABEL"] = 10
default_config_dict["PLOT"]["FONT_SIZE_LEGEND"] = 8
default_config_dict["PLOT"]["LINE_STYLE"] = [
    "solid",
    "dashed",
    "dashdot",
    "dotted",
]
