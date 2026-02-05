PyEMMO Documenation
===================
Here you can find the documentation for all classes, functions and properties in PyEMMO.
The structure of the documentation represents the PyEMMO project structure.
Every **Python package** (directory with ``__init__.py`` file) can have **submodules (.py files)** 
*and* **subpackages** (subdirectories with ``__init__.py`` file).
In addition every package documentation has a **Module contents** section which are the
contents of the ``__init__.py`` file.

The PyEMMO package contains 3 subdirectories/subpackages (*api*, *functions* and *script*)
and 4 modules (*colors*, *default_config_dict*, *definitions*, *version*) with different definitions.

* The :mod:`~pyemmo.api` package contains the part to interface external software (Pyleecan and arbitrary).
* The :mod:`~pyemmo.functions` package contains different functions to be used everywhere (in PyEMMO and by the user).
* The :mod:`~pyemmo.script` package contains the core functionality by the :py:class:`~pyemmo.script.script.Script`
  class and subpackages for :mod:`~pyemmo.script.geometry` and :mod:`~pyemmo.script.material` classes.


Subpackages
-----------

.. toctree::
   :maxdepth: 1

   pyemmo.api
   pyemmo.functions
   pyemmo.script

Submodules
----------

.. toctree::
   :maxdepth: 1

   pyemmo.colors
   pyemmo.default_config_dict
   pyemmo.definitions
   pyemmo.version

Module contents
---------------

.. automodule:: pyemmo
   :members:
   :show-inheritance:
   :undoc-members:
