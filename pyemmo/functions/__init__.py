#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""
The ``functions`` subpackage provides a collection of utilities to be used in PyEMMO and by the user.

Modules
-------
- :mod:`~pyemmo.functions.clean_name`: defines function :func:`clean_name` to modify strings to be valid ONELAB variable names (C-programming style)
- :mod:`~pyemmo.functions.core_loss`: defines functions to calculate core losses from flux density simulation results.
- :mod:`~pyemmo.functions.init_environment`: defines functions to initialize the PyEMMO program environment.
- :mod:`~pyemmo.functions.maxwell`: defines functions to import and export data from ANSYS Maxwell.
- :mod:`~pyemmo.functions.import_results`: defines functions to import simulation results from ONELAB result files (.dat and .pos).
- :mod:`~pyemmo.functions.onelab_parameters`: defines functions to parse ONELAB parameters from .geo and .pro files.
- :mod:`~pyemmo.functions.phase`: defines functions to convert phase names and angles for three and multi-phase systems.
- :mod:`~pyemmo.functions.plot`: defines a general plot function to visualize PyEMMO geometries.
- :mod:`~pyemmo.functions.run_onelab`: defines functions to run ONELAB simulations.
- :mod:`~pyemmo.functions.transform_coords`: defines general functions for coordinate system transformations used in PyEMMO.
"""
from __future__ import annotations

SETUP_FILE_NAME = "pyemmo_sim_setup.json"
