# pylint: skip-file -> Do not scan this file with pylint
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

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyEMMO"
copyright = "2022, TTZ-EMO AG-EM"
author = "TTZ-EMO AG-EM"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "member_order": "bysource",
}
# Autosummary settings
autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Napolen settings
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

## default theme options
html_theme_options = {
    #     'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
    #     'analytics_anonymize_ip': False,
    #     'logo_only': False,
    #     'display_version': True,
    #     'prev_next_buttons_location': 'bottom',
    #     'style_external_links': True,
    #     'vcs_pageview_mode': '',
    #     'style_nav_header_background': 'white',
    #     # Toc options
    #     'collapse_navigation': True,
    #     'sticky_navigation': True,
    #     'navigation_depth': 4,
    #     'includehidden': True,
    #     'titles_only': False
}


# change color of theme
def setup(app):
    app.add_css_file("css/custom.css")
