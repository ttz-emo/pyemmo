Getting Started
===============

Python and Compatible Versions
------------------------------
PyEMMO is tested and works for Python versions from 3.8 to 3.14.
The current development version is Python 3.12.10.
You can `get the latest Python versions here <https://www.python.org/downloads/>`_.
If you have never used Python before we recommend you get familiar with the basics of programming in Python.
`This video <https://www.youtube.com/watch?v=fWjsdhR3z3c>`_ or `the official Python Getting Started <https://www.python.org/about/gettingstarted/>`_ website can be good entry points.

Installation
------------
To use PyEMMO you need to install it as a Python library using `pip`, the Python package installer that comes with every Python installation.
If you have never used `pip` before, we encourage you to read the `pip - Getting Started <https://pip.pypa.io/en/stable/getting-started/>`_.
To install PyEMMO in your current Python installation (thats the one first found on your `PATH`), you must simply call:

.. code-block:: console

    $ pip install pyemmo

If you have allready installed a version of PyEMMO and you want to upgrade to a **new** version:

.. code-block:: console

    $ pip install --upgrade pyemmo

If you want to install a specific PyEMMO version (`x.y.z` are placeholders for that version) than the version you have currently installed, use:

.. code-block:: console

    $ pip install pyemmo==x.y.z --force-reinstall

But keep in mind that this will also uninstall and reinstall the libraries that PyEMMO depends on.

.. note:: **The PYLEECAN package is currently only a optional dependency of PyEMMO**

    This is because pyleecan depends on various older packages including GUI package `PySide2`.
    Thats why the `latest version 1.5.2 <https://pypi.org/project/pyleecan/1.5.2/>`_ is only compatible with ``Python<3.11``.
    While the process to update PYLEECAN to ``PySide6`` and upgrade futher dependencies is allready finished, these updates are currently not available in a new release. See `Issue 732 <https://github.com/Eomys/pyleecan/issues/732>`_ for the current state of the update process.
    To use PyEMMO with PYLEECAN you will currently need to install the PYLEECAN development version from Github:

    .. code-block:: console

        $ pip install pip install git+https://gitlab.com/Eomys/pyleecan/tree/update-python-version.git


Getting ONELAB
--------------

If you want to run simulations on electrical machines, which is probably the reason you install PyEMMO,
you further need to install ONELAB (= `Gmsh <http://gmsh.info>`_  + `GetDP <http://getdp.info>`_ )
from the `ONELAB website <https://onelab.info/>`_.
You can either install ONELAB as a bundle of Gmsh and GetDP or install both programms separately.
Just make sure the executables can be found on your system by setting the `PATH` variable.

.. note:: There is a known bug in the latest Gmsh versions when exporting geometries to the `old` **geo** format:

    For versions greater 4.14.0 the **geo_unrolled** formated output of OpenCascade instances
    is replaced by the .xao format which does not work properly for the current model generation workflow.
    Thats why the version of the `Gmsh Python library <https://pypi.org/project/gmsh/>`_ (which PyEMMO uses) is limited to version 4.13.
    Anyway, to visualize the geometry and create the mesh you can use the lastest Gmsh version.
    See `this issue <https://gitlab.onelab.info/gmsh/gmsh/-/issues/3214>`_ and
    `this comment <https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/src/geo/GModelIO_GEO.cpp?ref_type=heads#L1840>`_
    on the ONELAB GitLab website for more information.

.. Usage
.. =====
