Getting Started
===============

Python and compatible versions
------------------------------
PyEMMO is tested and works for Python versions from 3.8 to 3.14.
The current development version is Python 3.12.10.
You can :link:`get the latest Python versions here <https://www.python.org/downloads/>`.
If you have never used Python before we recommend you get familiar with the basics of programming with Python.
`This video <https://www.youtube.com/watch?v=fWjsdhR3z3c>`_ or `the official Python Getting Started <https://www.python.org/about/gettingstarted/>`_ website can be good entry points.

Installation
------------
To use PyEMMO you need to install it as a Python library using `pip`, the Python package installer that comes with every Python installation.
If you have never used `pip` before, we encourage you to read the `pip - Getting Started <https://pip.pypa.io/en/stable/getting-started/>`_.
To install PyEMMO in your current Python installation (thats the one first found on your `PATH`), you must simply call:

.. code-block:: console

    $ pip install pyemmo

If you want to run simulations on electrical machines, which is probably the reason you install PyEMMO, you further need to install ONELAB (=Gmsh + GetDP) from the :link:`ONELAB website <https://onelab.info/>`_ 

If you have allready installed a version of PyEMMO and you want to upgrade to a **new** version:

.. code-block:: console

    $ pip install --upgrade pyemmo

If you want to install a specific PyEMMO version (`x.y.z` are placeholders for that version) than the version you have currently installed, use:

.. code-block:: console

    $ pip install pyemmo==x.y.z --force-reinstall

But keep in mind that this will also uninstall and reinstall the libraries that PyEMMO depends on.