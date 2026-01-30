pyemmo.api.json package
=======================

.. toctree::
   :maxdepth: 1

This section is about the PyEMMO JSON API.
It's working with two `JSON <https://de.wikipedia.org/wiki/JavaScript_Object_Notation>`_ formatted files, giving the geometry and the additional machine information.
You can call the API via the command line using the following command:

.. code-block:: console

   $ python -m pyemmo.api.json /path/to/geo.json /path/to/machineInfo.json

Or you can use a Python script to execute the :func:`~pyemmo.api.json.json.main` function of the :mod:`~pyemmo.api.json.json` module, like this:

.. code-block:: python

   import os
   from pyemmo.api.json.json import main

   model_folder = r"/path/to/model/folder"
   param_file_path = os.path.join(model_folder, "param.json")
   model_file_path = os.path.join(model_folder, "geometry.json")
   # run json api to create ONELAB Model
   pyemmo_script = main(
      geo=model_file_path,
      extInfo=param_file_path,
      model=model_folder,
      gmsh="",
      getdp="",
      results="",
   )

The api returns a PyEMMO :class:`~pyemmo.script.script.Script` object, which is the core to create the model files for ONELAB.

Input Structure
---------------
The input to the json api are two structures (Python dictionaries or json files), one for the geometry and material definition of the individual machine surfaces and another one for the machine properties.
This section highlights the format of those two structures.

1. Geometry Structure
'''''''''''''''''''''
The geometry is defined by a list of segmented surface structures.
Every surface represents a minimal segment of the full model geometry and has the following attributes:

.. list-table:: PyEMMO Segmented Surface Structure Attributes
   :header-rows: 1

   * - Attribute
     - Description
   * - Name
     - Surface name
   * - IdExt
     - Surface identifier defined in the api module :mod:`definitions <~pyemmo.api.json>`
   * - Lines
     - Curve loop to draw the surface outline defined by a list of *line structures*
   * - Material
     - PyEMMO :class:`~pyemmo.script.material.material.Material` structure
   * - Quantity
     - Number of surface segments to form a full model (circle)
   * - Meshsize
     - Optional surface mesh size

Example:

.. code-block:: python

   # Example dict for stator lamination
   stator_lam_dict = {
      "Name": "stator core",
      "IdExt": "stator lamination",
      "Lines": [...],
      "Material": {
         "name": "steel material",
         "conductivity": 1.9e6,
         "relPermeability": 1000,
         "BHCurve": {"default": []},
         "density": 7680,
         "sheetThickness": 0.5e-3,
         "lossParams": [5000, 18e3, 0],
      },
      "Quantity": 4, # symmetry = 4
      "Meshsize": None,
   }

Each curve of the surface outline should have the following attributes:

.. list-table:: PyEMMO Line Structure Attributes
   :header-rows: 1

   * - Attribute
     - Description
   * - LineName
     - Line name
   * - Typ
     - Line type. Can be "Arc" for circle arc or "Line" for a straight curve.
   * - ApName
     - Start point name.
   * - ApX
     - Start point x-coordinate.
   * - ApY
     - Start point y-coordinate.
   * - ApZ
     - Start point z-coordinate.
   * - ApMesh
     - Start point mesh size.
   * - EpName
     - End point name.
   * - EpX
     - End point x-coordinate.
   * - EpY
     - End point y-coordinate.
   * - EpZ
     - End point z-coordinate.
   * - EpMesh
     - End point mesh size.
   * - MpName
     - Middle point name. Only for arc.
   * - MpX
     - Middle point x-coordinate. Only for arc.
   * - MpY
     - Middle point y-coordinate. Only for arc.
   * - MpZ
     - Middle point z-coordinate. Only for arc.
   * - MpMesh
     - Middle point mesh size. Only for arc.

Example:

.. code-block:: python

   arc_structure = {
      "LineName": "individual line name",
      "Typ": "Arc",
      "ApName": "Start point name",
      "ApX": 0.028731988729135773,
      "ApY": 5E-6,
      "ApZ": 0,
      "ApMesh": 0.0011827808408478094,
      "EpName": "End point name",
      "EpX": 0.027681988729135774,
      "EpY": 0.0010550000000000004,
      "EpZ": 0,
      "EpMesh": 0.0011827808408478094,
      "MpName": "Center point name",
      "MpX": 0.027681988729135777,
      "MpY": 5E-6,
      "MpZ": 0,
      "MpMesh": 0.0011827808408478094
   }

Command-line Interface
----------------------

.. role:: bash(code)
   :language: bash

You can call :bash:`python -m pyemmo.api.json -h` to get the following information about the command line options:

.. You MUST add a empty line between the 'code-block' directive and the actual code you want to display.
.. using the code-block-"role" without syntax highlighting (-> "text")
.. code-block:: text

   usage: json.py [-h] [--gmsh GMSH] [--getdp GETDP] [--mod MOD] [--res RES] geo extInfo

   Process Motor-JSON files to generate a Onelab Simulation.

   positional arguments:
      geo            path to the JSON geometry file ('geometry.json')
      extInfo        path to the extended info JSON file ('extendedInfo.json')

   optional arguments:
      -h, --help     show this help message and exit
      --gmsh GMSH    path to the Gmsh executable
      --getdp GETDP  path to the GetDP executable
      --mod MOD      path where the model files should be stored
      --res RES      path where the simulation results should be stored
      --log LOG      logging level for execution. Options are: error, warning, info, debug. default is warning
      -v             set execution to verbose. Verbosity level equals logging level.

The arguments `gmsh`, `getdp`, `mod` and `res` are optional. If you don't specify the paths for Gmsh or GetDP, the program will try to find them in the system path.
The default path for the model result files (`mod` path) is a new folder in the user directory created at install time.
For Windows this will be something like :file:`C:/Users/USER_NAME/AppData/Roaming/pyemmo/Results`.
By default the results directory for the simulation results will be stored in the same folder as the onelab simulation files created by PyEMMO. The folder name defaults to :file:`/res_MODEL_NAME`.

.. _ref_sim_param_tabel:

.. table:: Simulation parameter in the JSON file.

   +-----------------+-----------------------------+-----------------+
   | parameter       | description                 | format          |
   | name            |                             |                 |
   +=================+=============================+=================+
   | winding         | winding layout              | List of str     |
   |                 | for given geometry          |                 |
   +-----------------+-----------------------------+-----------------+
   | NpP             | number of parallel paths per| int             |
   |                 | winding phase               |                 |
   +-----------------+-----------------------------+-----------------+
   | z_pp            | number of pole pairs        | int             |
   +-----------------+-----------------------------+-----------------+
   | Qs              | number of stator slots      | int             |
   +-----------------+-----------------------------+-----------------+
   | movingband_r    | moving band radius in meter | float           |
   +-----------------+-----------------------------+-----------------+
   | axLen_S         | axial length of stator      | float           |
   +-----------------+-----------------------------+-----------------+
   | axLen_R         | axial length of rotor       | float           |
   +-----------------+-----------------------------+-----------------+
   | symFactor       | symmetry factor for model   | int             |
   +-----------------+-----------------------------+-----------------+
   | startPos        | start rotor position in °   | float           |
   +-----------------+-----------------------------+-----------------+
   | endPos          | end rotor position in °     | float           |
   +-----------------+-----------------------------+-----------------+
   | nbrSteps        | number of time steps for    | int             |
   |                 | simulation                  |                 |
   +-----------------+-----------------------------+-----------------+
   | rot_freq        | rotational frequency in Hz  | float           |
   +-----------------+-----------------------------+-----------------+
   | parkAngleOffset | park transfomation offset   | float           |
   |                 | angle in elec. °            |                 |
   +-----------------+-----------------------------+-----------------+
   | analysisType    | 0 = static;                 | 0 or 1          |
   |                 | 1 = transient               |                 |
   +-----------------+-----------------------------+-----------------+
   | tempMag         | magnet temperature °C       | float           |
   +-----------------+-----------------------------+-----------------+
   | r_z             | tooth radius in meter       | float           |
   +-----------------+-----------------------------+-----------------+
   | r_j             | yoke radius in meter        | float           |
   +-----------------+-----------------------------+-----------------+
   | id              | d-axis current in A         | float           |
   +-----------------+-----------------------------+-----------------+
   | iq              | q-axis current in A         | float           |
   +-----------------+-----------------------------+-----------------+
   | modelName       | name of the model files     | string          |
   +-----------------+-----------------------------+-----------------+
   | magDirection    | | magnetization direction/  | string          |
   |                 |   type of permament magnets |                 |
   |                 | | ("parallel", "radial"     |                 |
   |                 |   or "tangential")          |                 |
   +-----------------+-----------------------------+-----------------+
   | flag_openGUI    | open Gmsh GUI after model   | bool            |
   |                 | generation                  |                 |
   +-----------------+-----------------------------+-----------------+
..   | flag_openGUI    | open Gmsh GUI after model   | bool            |
..   |                 | generation                  |                 |
..   +-----------------+-----------------------------+-----------------+
.. TODO: Update simulation parameters automatically

.. +-----------------+-----------------------------+-----------------+
.. | cuFillFactor    | copper fill symFactor       | float           |
.. +-----------------+-----------------------------+-----------------+
.. | R_S             | phase resistance in Ohm     | float           |

Here is an example of how the `extInfo` JSON file content could look like.
There can be more infos like the copper fill factor or the stator resistance, which will be used in the future.

.. code:: json

   {
      "winding": ["+u","+u","+u","-v","-v","-v","+w","+w","+w"],
      "NpP": 2,
      "Ntps": 25,
      "cuFillFactor": 0.5,
      "R_S": 0.75,
      "z_pp": 2,
      "Qs": 36,
      "movingband_r": 0.032,
      "axLen_S": 0.05,
      "axLen_R": 0.05,
      "symFactor": 4,
      "startPos": 0,
      "endPos": 90,
      "nbrSteps": 18,
      "rot_freq": 16.666666666666668,
      "parkAngleOffset": null,
      "analysisType": 0,
      "tempMag": 20,
      "r_z": 0.038,
      "r_j": 0.0475,
      "id": 0,
      "iq": 0,
      "modelName": "Example_Maschine",
      "magDirection": "parallel",
      "flag_openGUI": true
   }


Submodules
----------

.. toctree::
   :maxdepth: 4

   pyemmo.api.json.boundaryJSON
   pyemmo.api.json.create_airgaps
   pyemmo.api.json.get_coilspan
   pyemmo.api.json.importJSON
   pyemmo.api.json.json
   pyemmo.api.json.modelJSON

Module contents
---------------

.. automodule:: pyemmo.api.json
   :members:
   :show-inheritance:
   :undoc-members:
