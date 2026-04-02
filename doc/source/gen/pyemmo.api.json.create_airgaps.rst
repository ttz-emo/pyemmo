pyemmo.api.json.create\_airgaps module
======================================

Automatic Airgap Creation
-------------------------
This module implements a function :func:`~pyemmo.api.json.create_airgaps.create_airgap_surfaces`.
If no airgaps (stator or rotor) given with the segmented input for the :mod:`pyemmo.api.json` API, create the airgap surfaces by extracting the inner/outer boundary of stator/rotor and the information about the movingband radius given with the `model information dict <ref_sim_param_tabel>`_.

Here is an example for the workflow described in :func:`~pyemmo.api.json.create_airgaps.create_airgap_surfaces` using the Toyota Prius model of Pyleecan. See the function description for a more detailed explanation.

.. figure:: ../../images/create_airgaps/prius_model.png
   :scale: 30 %
   :alt: Final Prius Model with symmetry of 8.
   :align: center

   ONELAB model of Toyota Prius machine in Gmsh created by PyEMMO.

1. Extract the boundary lines.

   .. image:: ../../images/create_airgaps/prius_stator_boundary.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

2. Filter the lines on the symmetry axis.

   .. image:: ../../images/create_airgaps/prius_stator_boundary_without_sym_axis.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

3. Find the point thats closest to the airgap on the x-axis.

   .. image:: ../../images/create_airgaps/prius_stator_boundary_closestPoint.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

4. Find the interface curves connecting to that point.

   .. image:: ../../images/create_airgaps/prius_stator_airgap_interface.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

5. Create the airgap surface(s) depending on if the found contour is purely cylindrical.
   For this stator the interface found is not cylindrical because of the slot openings.
   Thats why two airgap surfaces are created (one closing the stator interface and one
   purely cylindrical).

   .. image:: ../../images/create_airgaps/prius_stator_airgaps.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

   .. image:: ../../images/create_airgaps/prius_stator_airgaps_zoomed.png
      :scale: 30 %
      :alt: Final Prius Model with symmetry of 8.
      :align: center

.. note:: *Full model airgap creation*

   For a full machine model (symmetry = 1) the workflow differs slightly.
   The filering of the interface curve is similar.
   But for the creation of the airgap surfaces we need to create full surface objects
   and (by boolean difference) subtract circle surfaces from that to create the hollow
   cylindrical structures. See :func:`~pyemmo.api.json.create_airgaps._create_band_surf`
   for more details.


.. automodule:: pyemmo.api.json.create_airgaps
   :members:
   :show-inheritance:
   :undoc-members:
