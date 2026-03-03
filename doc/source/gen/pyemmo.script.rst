pyemmo.script package
=====================

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
   , or boundary curves, e.g. :class:`~pyemmo.script.physicals.limitLine.LimitLine`).
6. The :class:`~pyemmo.script.domain.Domain` class represents groups of
   :class:`~pyemmo.script.geometry.physicalElement.PhysicalElement` objects with shared
   properties. These mirror the object structure of ONELAB models. See
   `GetDP Groups <https://getdp.info/doc/texinfo/getdp.html#Group>`_ documentation
   section for more details.
7. The :class:`~pyemmo.script.machine.Machine`, :class:`~pyemmo.script.rotor.Rotor` and :class:`~pyemmo.script.stator.Stator` classes act as containers for the :class:`~pyemmo.script.phyicals.physicalElement.PhysicalElement` objects of a model and implement the logic to create the :class:`~pyemmo.script.domain.Domain` objects needed in the :class:`~pyemmo.script.script.Script`.

For a visual overview of the package structure see the graph below.

.. graph:: script_subpackage

   dpi=300
   rankdir=LR


   "script" -- "Script";
   "script" -- "Domain";
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
   "script" -- "Machine";
   "script" -- "Rotor";
   "script" -- "Stator";

|

Subpackages
-----------

.. toctree::
   :maxdepth: 1

   pyemmo.script.geometry
   pyemmo.script.physicals
   pyemmo.script.gmsh
   pyemmo.script.material

Submodules
----------

.. toctree::
   :maxdepth: 2

   pyemmo.script.rotor
   pyemmo.script.stator
   pyemmo.script.machine
   pyemmo.script.domain
   pyemmo.script.script

script module
-------------

.. automodule:: pyemmo.script
   :members:
   :show-inheritance:
   :undoc-members:
