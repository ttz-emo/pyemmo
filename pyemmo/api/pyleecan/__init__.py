#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
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
"""
Pyleecan API
============

Overview
--------
This subpackage provides the bridge between PyEMMO internal machine representations
and the `Pyleecan project <https://pyleecan.org/>`_. All conversion utilities and
helpers that translate Pyleecan machines into PyEMMO/Gmsh objects live here.
The integration is conditional on the project-level ``use_pyleecan`` flag:
when Pyleecan package is unavailable or the flag is disabled, Pyleecan-specific classes
are not imported and runtime calls that require Pyleecan will not be available.

Primary responsibilities
------------------------
- Translate Pyleecan machine structures so they can form the input to the PyEMMO :ref:`json api <section-pyemmo.api.json-package>`.
- Map Pyleecan materials into PyEMMO :class:`~pyemmo.script.material.material.Material` objects and provide a default air material for geometry surfaces without explicit material references.
- Produce geometry dictionaries and Gmsh primitives (points, lines, surfaces) used for the json api model generation workflow.
- Provide utilities to map Pyleecan surface labels to PyEMMO api part identifiers (``part_id``).

Module list
-----------
The subpackage contains focused modules that implement pieces of the translation workflow. Key modules (exposed in the docs toctree) are:

- :mod:`~pyemmo.api.pyleecan.build_pyemmo_material`: build and translate materials
- :mod:`~pyemmo.api.pyleecan.create_geo_dict`: assemble geometry dictionaries and ensure materials are assigned (uses a default air material when needed)
- :mod:`~pyemmo.api.pyleecan.create_gmsh_point`, :mod:`~pyemmo.api.pyleecan.create_gmsh_lines`, :mod:`~pyemmo.api.pyleecan.create_gmsh_surf`: create ``GmshGeometry`` primitives.
- :mod:`~pyemmo.api.pyleecan.create_param_dict`: prepare simulation parameters.
- :mod:`~pyemmo.api.pyleecan.create_pyleecan_simulation`: compose a full Pyleecan simulation object
- :mod:`~pyemmo.api.pyleecan.label2part_id`: map `Pyleecan surface label strings <https://www.pyleecan.org/_modules/pyleecan/Functions/labels.html>`_ to :ref:`part identifiers <section-pyemmo.api.json>` used in the json api.
- :mod:`~pyemmo.api.pyleecan.main`: Main function to trigger model translation and call the json api to create the ONELAB model files.

Pyleecan API workflow
---------------------
1. Create default machine and simulation parameters for the :mod:`~pyemmo.api.json` api using :func:`~pyemmo.api.pyleecan.create_param_dict.create_param_dict`. See the `Model Properties Structure <section-pyemmo.api.json-param>`_ section for details.
2. Translate the Pyleecan machine object to the geometry input dictionary for the PyEMMO :mod:`~pyemmo.api.json` api using :func:`~pyemmo.api.pyleecan.create_geo_dict.create_geo_dict`. This function executes the core mapping between Pyleecan surface and material definitions and the PyEMMO :class:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface` and :class:`~pyemmo.script.material.material.Material` objects. Therefore its using the ``create_gmsh_*`` helpers and :func:`~pyemmo.api.pyleecan.build_pyemmo_material.build_pyemmo_material`. It also handles the geometry symmetries and subtraction of tool surfaces independently for rotor and stator.
3. Call the :mod:`~pyemmo.api.json` api to create the Gmsh and GetDP model files. See `json api section <section-pyemmo.api.json-package>`_ for details on the expected input structures and file generation workflow.

Minimal usage sketch
--------------------
.. code-block:: python

    from os.path import join

    from pyleecan.Functions.load import load
    from pyleecan.definitions import DATA_DIR
    from pyemmo.api.pyleecan import main as pyleecan_api

    IPMSM_A = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
    # Run the main function of the pyleecan api:
    pyemmo_script = pyleecan_api.main(
        pyleecan_machine=IPMSM_A,
        model_dir=join(RESULT_DIR, "Toyota_Prius_ONELAB"),  # path for the model files
        use_gui=False,  # select if you want to open the final model in Gmsh.
        gmsh="",  # optional gmsh executable.
        # If use_gui is True, pyemmo will try to find a Gmsh executable on your computer.
        getdp="",  # optional getdp executable. For simulation in the GUI.
    )

See the pyleecan api tutorial for a more detailed walkthrough of the workflow and the expected input and output structures.  

Current Limitations
-------------------
TODO.


"""

from __future__ import annotations

from typing import Union

from ... import use_pyleecan

if use_pyleecan:
    from pyleecan.Classes.MachineDFIM import MachineDFIM  # induction machine
    from pyleecan.Classes.MachineIPMSM import MachineIPMSM
    from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
    from pyleecan.Classes.MachineSyRM import MachineSyRM
    from pyleecan.Classes.MachineWRSM import MachineWRSM

    # from pyleecan.Classes.MachineLSPM import MachineLSPM

    PyleecanMachine = Union[
        MachineDFIM, MachineSIPMSM, MachineIPMSM, MachineWRSM, MachineSyRM
    ]
    from pyleecan.Classes.Material import Material

    # Load default air material used in create_geo_dict function for surfaces without
    # referenced material.
    PyleecanAir = Material(name="Air")
POLE_HOLE_IDEXT = "Pole Hole"  # usused for now
