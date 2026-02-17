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
"""
The script subpackage provides the all necessary functions and classes to create ONELAB
models.

1. The main class is the :class:`~pyemmo.script.script.Script` class, which creates
   the geometry (.geo) and model (.pro) files from a PyEMMO
   :class:`~pyemmo.script.machine.Machine` object and some
   additonal parameters.
2. The :mod:`~pyemmo.script.geometry` subpackage provides classes for **basic geometric
   objects**, like the :class:`~pyemmo.script.geometry.line.Line` class, which are the
   basis for the :class:`~pyemmo.script.gmsh.gmsh_geometry.GmshGeometry` classes in the
   :mod:`~pyemmo.script.gmsh` subpackage.
3. The :mod:`~pyemmo.script.gmsh` subpackage provides classes for **Gmsh geometry objects**,
   like the :class:`~pyemmo.script.gmsh.GmshLine` class, which are used to create the
   geometry of the ONELAB model through the
   `gmsh python api <https://gmsh.info/doc/texinfo/gmsh.html#Gmsh-application-programming-interface>`_.
4. The :mod:`~pyemmo.script.material` subpackage provides classes for handling of
   material properties.
5. The :mod:`~pyemmo.script.physicals` subpackage provides classes that represent the
   **PhyicalElement** objects according to the Gmsh/GetDP definition.
   This means groups of geometric objects (e.g. surfaces) with assigned physical
   properties (e.g. magnetization and material properties) or boundary conditions.
   The subpackage contains different types of **PhysicalElements**
   (= surfaces with phyiscal properties, e.g. :class:`~pyemmo.script.geometry.slot.Slot`
   , or boundary curves, e.g. :class:`~pyemmo.script.physicals.limitLine.LimitLine`)
6. The :class:`~pyemmo.script.domain.Domain` which represents groups of
   :class:`~pyemmo.script.geometry.physicalElement.PhysicalElement` objects with shared
   properties. These mirror the object structure of ONELAB models. See
   `GetDP Groups <https://getdp.info/doc/texinfo/getdp.html#Group>`_ documentation
   section for more details.

For a visual overview of the package structure see the graph below.

.. graph:: script_subpackage

   "script" -- "Script";
   "script" -- "geometry";
   "geometry" -- "Transformable";
   "Transformable" -- "Point";
   "Transformable" -- "Line";
   "Transformable" -- "Surface";
   "Line" -- "CircleArc";
   "Line" -- "Spline";
   "Surface" -- "SegmentSurface";
   "script" -- "material";
   "material" -- "Material";
   "Material" -- "ElectricalSteel";
   "script" -- "physicals";
   "physicals" -- "PhysicalElement";
   "PhysicalElement" -- "Magnet";
   "PhysicalElement" -- "LimitLine";
   "PhysicalElement" -- "...";
   "script" -- "gmsh";
   "gmsh" -- "GmshGeometry";
   "GmshGeometry" -- "GmshPoint";
   "GmshGeometry" -- "GmshLine";
   "GmshGeometry" -- "GmshSurface";
   "GmshLine" -- "GmshArc";
   "GmshLine" -- "GmshSpline";
   "GmshSurface" -- "GmshSegmentSurface";

|
|

More text

"""

from __future__ import annotations

import json
import logging
from os.path import dirname, join
from typing import Dict

from ..version import __version__, sha

colorDict: dict[str, str] = {}
logger = logging.getLogger(__name__)
try:
    with open(
        join(dirname(__file__), "default_color_dict.json"),
        encoding="utf-8",
    ) as infile:
        colorDict = json.load(infile)
except Exception as exce:
    logger.warning("Color Dict could not be imported...", exc_info=True)

# Define domain names globally
DOMAIN_PRIMARY = "primary"
DOMAIN_SECONDARY = "slave"
DOMAIN_LIMIT = "limit"
DOMAIN_MOVINGBAND = "mb_all"
DOMAIN_MOVINGBAND_AUX = "mb_Mbaux"
DOMAIN_AIRGAP = "airGap"
DOMAIN_ROTOR = "rotor_moving"
DOMAIN_STRANDED = "domainS"
DOMAIN_MAGNET = "domainM"
DOMAIN_LAMINATION = "domainLam"
DOMAIN_BAR = "domainBar"
DOMAIN_CONDUCTING = "domainC"
DOMAIN_NON_CONDUCTING = "domainCC"
DOMAIN = "domain"
DOMAIN_NON_LINEAR = "domainNL"
DOMAIN_LINEAR = "domainL"

# define default parameters in parameter dict
default_param_dict: dict[str, dict] = {"GEO": {}, "SYM": {}, "MAT": {}}
"""Default parameter dict used in the :class:`~pyemmo.script.script.Script` class to
initialize the ``Script.simulation_parameters`` attribute.

The default vlaues looks like:

.. code-block:: python

    {
        "GEO": {
            "SYMMETRY_FACTOR": 1,
            "L_AX_R": 1.0,
            "L_AX_S": 1.0,
            "NBR_POLE_PAIRS": 4,
            "NBR_SLOTS": 12,
            "NBR_TURNS_IN_FACE": 20,
            "R_AIRGAP": 0.1,
        },
        "SYM": {
            "INIT_ROTOR_POS": 0.0,
            "ANGLE_INCREMENT": 0.5,
            "FINAL_ROTOR_POS": 90.0,
            "Id_eff": 0,
            "Iq_eff": 1,
            "FLAG_NL": 1,
            "SPEED_RPM": 1000,
            "PATH_RES": "",
            "ParkAngOffset": None,  # optional
            "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient
            "FLAG_CHANGE_ROT_DIR": 0,
            "NBR_PARALLEL_PATHS": 1,
            "CALC_MAGNET_LOSSES": 0,
            "R_ENDRING_SEGMENT": 0.,
            "L_ENDRING_SEGMENT": 0.,
        },
        "MAT": {
            "VALUE_DENSITY_LAM": 7800,
            "TEMP_MAG": 20,
        }
    }

:meta hide-value:
"""
default_param_dict["GEO"] = {
    "SYMMETRY_FACTOR": 1,
    "L_AX_R": 1.0,
    "L_AX_S": 1.0,
    "NBR_POLE_PAIRS": 4,
    "NBR_SLOTS": 12,
    "NBR_TURNS_IN_FACE": 20,
    "R_AIRGAP": 0.1,
}
default_param_dict["SYM"] = {
    "INIT_ROTOR_POS": 0.0,
    "ANGLE_INCREMENT": 0.5,
    "FINAL_ROTOR_POS": 90.0,
    "Id_eff": 0,
    "Iq_eff": 1,
    "FLAG_NL": 1,
    "SPEED_RPM": 1000,
    "PATH_RES": "",
    "ParkAngOffset": None,  # optional
    "ANALYSIS_TYPE": 1,  # optional; 0: static, 1: transient
    "FLAG_CHANGE_ROT_DIR": 0,
    "NBR_PARALLEL_PATHS": 1,
    "CALC_MAGNET_LOSSES": 0,
    "R_ENDRING_SEGMENT": 0.0,
    "L_ENDRING_SEGMENT": 0.0,
}
default_param_dict["MAT"] = {
    "VALUE_DENSITY_LAM": 7800,
    "TEMP_MAG": 20,
}

# Translate Domain names from pyemmo -> GetDP template
# ONLY DOMAINS SPECIFIED HERE WILL BE CREATED!
boundaryDomainDict = {
    DOMAIN_PRIMARY: "Surf_cutA0",
    DOMAIN_SECONDARY: "Surf_cutA1",
}
# stator specific domains
statorDomainDict = {
    # "domainS": "",
    DOMAIN_CONDUCTING: "StatorC",
    DOMAIN_NON_CONDUCTING: "StatorCC",
    DOMAIN_MOVINGBAND: "Stator_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    DOMAIN_AIRGAP: "Stator_Airgap",
    DOMAIN_LIMIT: "Surf_Inf",
}
# rotor specific domains:
rotorDomainDict = {
    # "domainS": "",
    DOMAIN_MAGNET: "Rotor_Magnets",
    DOMAIN_BAR: "Rotor_Bars",
    DOMAIN_CONDUCTING: "RotorC",
    DOMAIN_NON_CONDUCTING: "RotorCC",
    DOMAIN_MOVINGBAND: "Rotor_Bnd_MB",
    # "domain": "",
    # "domainNL": "",
    # "domainL": "",
    # "rotor_moving": "",
    DOMAIN_MOVINGBAND_AUX: "Rotor_Bnd_MBaux",
    DOMAIN_AIRGAP: "Rotor_Airgap",
    DOMAIN_LIMIT: "Surf_bn0",
}

# additional line for pyemmo version in geo and pro files
versionStr = f"// This script was created with pyemmo (Version {__version__}"
# if git module is available, sha is the commit hash. Then add that too
if sha:
    versionStr += f", git {sha[0:6]}"
versionStr += ")\n\n"  # finalize version string
