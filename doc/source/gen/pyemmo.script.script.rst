pyemmo.script.script module
===========================

.. set the current python module for shorter links
.. currentmodule:: pyemmo.script

The **script** module defines the class for generating ONELAB simulation files from a :class:`~machine.Machine` object and a parameter dictionary.
For a ONELAB model we need a geometry file (.geo) for Gmsh to create the mesh (.msh file).
And we need a .pro input file for GetDP with a definition of the phyiscal problem and a connection to the geometry (mesh).
So the PyEMMO :class:`~script.Script` creates the following input files when :meth:`~script.Script.generate` is invoked:

.. list-table::

 * - **Model File**
   - **Description**
 * - *model\_name*.geo
   - Geometry (CAD), Mesh and Phyiscals Definition
 * - *model\_name*.pro
   - | Coupling of *model\_name*.geo Physicals into GetDP ``Group``,
     | ONELAB paramters, material properties and user defined
     | PostOperations
 * - *model\_name*\_param.geo
   - Global Machine and Simulation parameter initialization
 * - machine\_magstadyn\_a.pro
   - GetDP Problem Template for Electrical Machines
 * - Circuit.pro
   - | Optional Circuit for voltage source and squirrle cage
     | induction machine rotor

where *model\_name* is the :attr:`~script.Script.name` attribute.

When initializing the :class:`~script.Script` with a :class:`~machine.Machine` object like::

   my_script = Script(
      name="myscript name",
      scriptPath=r"/path/to/model/folder",
      simuParams=param_dict,
      machine=my_machine_obj,
   )

the :class:`~.domain.Domain` creation processs will be started.
This creates all groups of surfaces and boundary lines needed with the *model_name*.pro and machine\_magstadyn\_a.pro file.
So e.g. all :class:`~physicals.physicalElement.PhysicalElement` objects with a non-linear magnetic material definition (BH curve) are grouped in a Domain called ``domainNL``.
These domain names are defined in the GetDP machine model template and are linked to GetDP in the :mod:`~pyemmo.script` module by predefined constants.
In GetDP this are so called "Group" definitions and are located in a ``Group`` section.
See `GetDP Group <https://getdp.info/doc/texinfo/getdp.html#Group>`_ in the documentation.

.. graphviz::

   digraph script_pfc {

      rankdir=LR

      subgraph cluster_init {
        label="Machine Domain Creation";
        init [shape=circle, label="Script()"];
        amd [shape=box, label="add_machine_domains()"];
        cmd [shape=box, label="create_machine_domains()"];
        ad [shape=box, label="add_domain()"];
        init -> amd;
        amd -> cmd [arrowhead=normal];
        cmd -> ad [label=domain_list];
      }
      subgraph cluster_ad{
         label="Add Domain";
         aphys [shape=box, label="_add_physical()"];
         amat [shape=box, label="_add_material()"];
         amag [shape=box, label="_add_mag_function()"];
         ad -> aphys -> amat;
         aphys -> amag;
      }
   }

      /* subgraph cluster_cmd{ *\
      /*   label="Script.create_machine_domains"; *\
      /*   "create_machine_domains()" -> "machine.rotor.create_domains()"; *\
      /*   "create_machine_domains()" -> "machine.stator.create_domains()"; *\
      /*   "create_machine_domains()" -> "create_domains()"; *\
      /*   "create_machine_domains()" -> "add_machine_domains()" [label=domain_list]; *\
      /* } *\

|

The second step is to trigger the file generation process by calling the :meth:`~script.Script.generate` method::

   my_script.generate()

.. graphviz::

   digraph script_generate {

      rankdir=TB

      subgraph cluster_gen {
         label="File Generation";
         generate [shape=circle, label="generate()"]
      }
      subgraph cluster_wg {
         label="Create .geo File";
         wg [shape=box, label="write_geo()"];
         cmesh [shape=box, label="_create_mesh_code()"];
         cmove [shape=box, label="_create_moving_code()"];
         gwrite [shape=box, label="gmsh.write(geo_unrolled)"]
         gread [shape=box, label="read(geo_unrolled)"]
         add [shape=box, label="add additional code"]
         write [shape=box, label="write(geo)"]
         generate -> wg -> cmesh -> cmove -> gwrite -> gread -> add -> write;
      }
      subgraph cluster_wp {
         label="Create .pro Files";
         wp [shape=box, label="write_pro()"]
         wparam [shape=box, label="write param.geo"];
         cparam [shape=box, label="_create_param_code()"];
         read_template [shape=box, label="read(machine_template.pro)"];
         rep_param [shape=box, label="include param.geo"];
         rep_group [shape=box, label="add Group code"];
         cmat [shape=box, label="create material code"];
         rep_func [shape=box, label="add Function code"];
         copy_magstadyn [shape=box, label="copy\nmachine_magstadyn_a.pro"];
         copy_circuit [shape=box, label="copy Circuit.pro"];
         inc_msd [shape=box, label="include\nmachine_magstadyn_a.pro"];
         add_po [shape=box, label="add PostOperation code"];
         wpf [shape=box, label="write(pro)"];
         generate -> wp -> cparam -> wparam;
         wp -> read_template -> rep_param -> cmat -> rep_group -> rep_func -> inc_msd -> add_po -> wpf;
         wp -> copy_magstadyn -> copy_circuit;
      }
   }

|

.. automodule:: pyemmo.script.script
   :members:
   :show-inheritance:
   :undoc-members:

In the following you can find a list of the ONELAB model parameters given in the
template .geo and .pro files in PyEMMO.
These can be used to adjust and control the model and simulations.

.. you can include newlines in table items like this:
.. https://stackoverflow.com/a/72726476/26655964

.. include:: ../pyemmo.onelab_parameters.rst
