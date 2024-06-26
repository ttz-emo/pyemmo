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
from __future__ import annotations
import shutil
from json import dump, load
from os.path import isdir, isfile, join
from matplotlib import font_manager
from ..default_config_dict import default_config_dict
from ..version import __version__


def save_config_dict(config_dict):
    """update the config file with config_dict values

    Parameters
    ----------
    config_dict : dict
        new values to put in the config file
    """
    # dynamic import to avoid loop
    module = __import__(
        "pyemmo.definitions",
        globals=globals(),
        locals=locals(),
        fromlist=["CONF_PATH"],
        level=0,
    )
    CONF_PATH = module.CONF_PATH
    with open(CONF_PATH, "w") as config_file:
        dump(
            config_dict,
            config_file,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )


def init_user_dir():
    """Initialize the USER DIR with the default files"""
    # dynamic import to avoid loop
    module = __import__(
        "pyemmo.definitions",
        globals=globals(),
        locals=locals(),
        fromlist=["USER_DIR", "MAIN_DIR"],
        level=0,
    )
    USER_DIR = module.USER_DIR
    MAIN_DIR = module.MAIN_DIR

    # # Data initialization
    # mach_path = join(USER_DIR, "Machine")
    # if not isdir(mach_path):
    #     shutil.copytree(join(MAIN_DIR, "Data", "Machine"), mach_path)

    mat_path = join(USER_DIR, "Material")
    if not isdir(mat_path):
        shutil.copytree(
            join(MAIN_DIR, "script", "material").replace("\\", "/"), mat_path
        )

    # plot_path = join(USER_DIR, "Plot")
    # if not isdir(plot_path):
    #     shutil.copytree(join(MAIN_DIR, "Data", "Plot"), plot_path)

    init_config_dict()


def update_user_dir():
    """Initialize the USER DIR with the default files"""
    # dynamic import to avoid loop
    module = __import__(
        "pyemmo.definitions",
        globals=globals(),
        locals=locals(),
        fromlist=["USER_DIR", "MAIN_DIR"],
        level=0,
    )
    USER_DIR = module.USER_DIR
    MAIN_DIR = module.MAIN_DIR

    # # Data initialization
    # mach_path = join(USER_DIR, "Machine")
    # if isdir(mach_path):
    #     shutil.rmtree(mach_path)
    # shutil.copytree(join(MAIN_DIR, "Data", "Machine"), mach_path)

    # mat_path = join(USER_DIR, "Material")
    # if isdir(mat_path):
    #     shutil.rmtree(mat_path)
    # shutil.copytree(join(MAIN_DIR, "Data", "Material"), mat_path)

    # plot_path = join(USER_DIR, "Plot")
    # if isdir(plot_path):
    #     shutil.rmtree(plot_path)
    # shutil.copytree(join(MAIN_DIR, "Data", "Plot"), plot_path)


def init_config_dict():
    """Create the default config dict and save it in USER_DIR"""
    # dynamic import to avoid loop
    module = __import__(
        "pyemmo.definitions",
        globals=globals(),
        locals=locals(),
        fromlist=["USER_DIR", "CONF_PATH"],
        level=0,
    )
    DEFAULT_FONT = module.DEFAULT_FONT

    # Initialization to make sure all the parameters exist
    config_dict = default_config_dict.copy()
    config_dict["version"] = __version__
    if config_dict["PLOT"]["FONT_NAME"] == "":
        config_dict["PLOT"]["FONT_NAME"] = DEFAULT_FONT
    save_config_dict(config_dict)


def get_config_dict():
    """Return the config dict (update with default to make sure all parameter exist)

    Returns
    -------
    config_dict: dict
        dictionary gather the parameters of the software
    """
    # dynamic import to avoid loop (pyemmo.definitions calls get_config_dict() function!!!)
    module = __import__(
        "pyemmo.definitions",
        globals=globals(),
        locals=locals(),
        fromlist=[
            "USER_DIR",
            "CONF_PATH",
            "DEFAULT_FONT",
            "DEFAULT_COLOR_MAP",
        ],
        level=0,
    )
    USER_DIR = module.USER_DIR
    CONF_PATH = module.CONF_PATH
    DEFAULT_FONT = module.DEFAULT_FONT
    DEFAULT_COLOR_MAP = module.DEFAULT_COLOR_MAP
    version = __version__

    # Make sure user dir exist
    if not isfile(CONF_PATH):
        init_user_dir()

    # Overwrite default config_dict with USER_DIR values
    config_dict = default_config_dict.copy()
    with open(CONF_PATH) as config_file:
        update_dict(source=config_dict, update=load(config_file))

    # Update Library if new version
    if "version" not in config_dict:
        config_dict["version"] = "No_version"
    if config_dict["version"] != version:
        update_user_dir()
    config_dict["version"] = version
    save_config_dict(config_dict)

    # # Register the colormap
    # cmap_name = config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"]
    # if "." not in cmap_name:
    #     cmap_path = join(USER_DIR, "Plot", cmap_name) + ".npy"
    # try:
    #     get_cmap(name=cmap_name)
    # except:
    #     if not isfile(cmap_path):  # Default colormap
    #         config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"] = DEFAULT_COLOR_MAP
    #     else:
    #         cmap = np_load(cmap_path)
    #         cmp = ListedColormap(cmap)
    #         register_cmap(name=config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"], cmap=cmp)

    # Check if font is available
    font_name = config_dict["PLOT"]["FONT_NAME"]
    if font_name not in [f.name for f in font_manager.fontManager.ttflist]:
        config_dict["PLOT"]["FONT_NAME"] = DEFAULT_FONT  # Default font

    # Update config_dict content
    if "MACHINE_DIR" not in config_dict["MAIN"] or not isdir(
        config_dict["MAIN"]["MACHINE_DIR"]
    ):
        config_dict["MAIN"]["MACHINE_DIR"] = join(USER_DIR, "Machine")
    if "MATLIB_DIR" not in config_dict["MAIN"] or not isdir(
        config_dict["MAIN"]["MATLIB_DIR"]
    ):
        config_dict["MAIN"]["MATLIB_DIR"] = join(USER_DIR, "Material")
    return config_dict


def update_dict(source, update):
    for key, value in update.items():
        if isinstance(value, dict):
            source[key] = update_dict(source.get(key, {}), value)
        else:
            source[key] = value
    return source
