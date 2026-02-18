# pylint: skip-file -> Do not scan this file with pylint
#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences
# Wuerzburg-Schweinfurt.
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

import os
import subprocess
import sys
from os.path import join

from pyemmo.definitions import MAIN_DIR
from pyemmo.functions.onelab_parameters import extract_onelab_parameters
from pyemmo.version import __version__

if not MAIN_DIR in sys.path:
    sys.path.insert(0, os.path.abspath("../pyemmo/"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyEMMO"
copyright = "2026, Technologietransferzentrum Elektromobilität TTZ-EMO"
author = "TTZ-EMO AG-EM"
release = __version__
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.apidoc", # auto generate .rst files of all pyemmo packages
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    # "sphinx.ext.intersphinx",  # used for links to existing online documentations
    #   see https://www.sphinx-doc.org/en/master/usage/quickstart.html#intersphinx
    # "sphinx.ext.autosectionlabel", # fix warning of duplicate label.
    "sphinx.ext.todo",  # enable todo directive
    "sphinx_rtd_theme",
    "sphinx.ext.graphviz",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "member_order": "bysource",
    "apidoc_module_first": True,
}
# Autosummary settings
autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Napolen settings
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/PyEMMO_Logo_2_small.png"

## default theme options
html_theme_options = {
    "version_selector": True,
    "language_selector": True,
    #     'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
    #     'analytics_anonymize_ip': False,
    #     'logo_only': False,
    # "display_version": True,
    #     'prev_next_buttons_location': 'bottom',
    #     'style_external_links': True,
    #     'vcs_pageview_mode': '',
    #     'style_nav_header_background': 'white',
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": False,
    #     'navigation_depth': 4,
    #     'includehidden': True,
    #     'titles_only': False
}

# parameter to control if a new pyemmo.onelab_parameters.rst file should be created.
create_param_file = True

if create_param_file:
    const, params = extract_onelab_parameters(
        [
            join(MAIN_DIR, "script", "machine_template.pro"),
            join(MAIN_DIR, "script", "machine_magstadyn_a.pro"),
            join(MAIN_DIR, "script", "Circuit_SC_ASM.pro"),
        ]
    )
    with open(
        join(".", "source", "pyemmo.onelab_parameters.rst"), "w", encoding="utf-8"
    ) as rst_file:
        heading = "ONELAB Model Constants"
        rst_file.write(heading + "\n")
        rst_file.write("".join(["'" for _ in range(len(heading))]) + "\n\n")
        rst_file.write(".. list-table::\n\t:widths: 12 28\n\t:header-rows: 1\n\n")
        heading = "\t*\t- Constant Name\n\t\t- Value"
        rst_file.write(heading + "\n")
        for name, code in const.items():
            line = f"\t*\t- {name}\n\t\t- {code}"
            rst_file.write(line + "\n")
        rst_file.write("\n")

        # create table for ONELAB Parameters
        heading = "ONELAB Model Parameters"
        rst_file.write(heading + "\n")
        rst_file.write("".join(["'" for _ in range(len(heading))]) + "\n\n")
        rst_file.write(".. list-table::\n\t:widths: 12 28\n\t:header-rows: 1\n\n")
        heading = "\t*\t- Parameter Name\n\t\t- Description"
        rst_file.write(heading + "\n")

        # TODO: Write separate description for R_, C_ and P_ parameters because they are
        # special ONELAB parameters. + add backslash like R\_ otherwise results in link.
        for name, code in params.items():
            # TODO: Extract "Help" from code and put in separate column
            line = f"\t*\t- {name}\n\t\t- {code}"
            rst_file.write(line + "\n")


def run_apidoc(app):
    """This function is connected to sphinx using its api. See :py:function::`setup`

    It runs the apidoc function to create new rst files for each module in
    PyEMMO. Note that existing files will not be overwritten!
    """
    apidoc_cmd = [
        "sphinx-apidoc",
        "--separate",  # create separate files for each module
        "--remove-old",  # remove rst files if modules were deleted in pyemmo!
        "-o",  # specify output directory
        os.path.join(app.srcdir, "source", "gen"),
        os.path.abspath(MAIN_DIR),
    ]
    subprocess.check_call(apidoc_cmd)


def setup(app):
    app.connect("builder-inited", run_apidoc)
    # change color of theme
    app.add_css_file("css/custom.css")
