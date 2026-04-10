Voltage Source Simulation
=========================

This is a tutorial shows you how to create a machine model and run a
voltage source simulation. A simple current driven simulation was
already shown in the
`pyleecan_api.ipynp <https://github.com/ttz-emo/pyemmo/blob/master/tutorials/pyleecan_api.ipynb>`__
tutorial.

The notebook related to this tutorial is available on
`GitHub <https://github.com/ttz-emo/pyemmo/blob/master/tutorials/voltage_source_simulation.ipynb>`__.

1. Create a ONELAB Model from a Pyleecan Machine
------------------------------------------------

Frist we need to create a ONELAB Model using the PyEMMO-Pyleecan-API.

.. code:: ipython3

    # Load the machine
    from __future__ import annotations

    import logging
    from os.path import join

    from pyleecan.definitions import DATA_DIR
    from pyleecan.Functions.load import load

    from pyemmo.api.pyleecan import main as pyleecan_api
    from pyemmo.definitions import RESULT_DIR

    IPMSM_A = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))

    # you can set the output verbosity of the model creation using the pyemmo logger.
    # The logging module by default implements DEBUG, INFO, WARNING, ERROR, FATAL log
    # levels, which are simply constants for integer levels, e.g. logging.DEBUG == 10
    # You can use evel(logging.DEBUG -1) to trigger extended debugging, which shows
    # additional information in plots and opens the Gmsh GUI at different levels in the
    # model creation.
    logging.getLogger("pyemmo").setLevel(logging.INFO)

    # Run the main function of the pyleecan api:
    pyemmo_script = pyleecan_api.main(
        pyleecan_machine=IPMSM_A,
        model_dir=join(RESULT_DIR, "Toyota_Prius_ONELAB"),  # path for the model files
        use_gui=False,  # select if you want to open the final model in Gmsh.
        gmsh="",  # optional gmsh executable.
        # If use_gui is True, pyemmo will try to find a executable on your computer.
        getdp="",  # optional getdp executable. For simulation in the GUI.
    )


.. parsed-literal::

    WARNING - pyemmo.api.pyleecan.build_pyemmo_material - Material 'Copper1' used without magnetic properties. Replacing it with PYLEECAN default material 'Copper2'
    INFO - pyemmo.api.json.json - PyEMMO API started on 2026-04-10 11:35:46
    INFO - pyemmo.api.json.json - Creating complete model from segmented input...
    INFO - pyemmo.api.json.create_airgaps - Stator airgap missing from surfaces. Starting airgap creation.
    INFO - pyemmo.api.json.create_airgaps - Creating air closing surface for stator airgap interface.
    INFO - pyemmo.api.json.create_airgaps - Creating airgap surface for stator
    INFO - pyemmo.api.json.create_airgaps - Setting stator airgap mesh size to band height 0.000150 m
    INFO - pyemmo.api.json.create_airgaps - Rotor airgap missing from surfaces. Starting airgap creation.
    INFO - pyemmo.api.json.create_airgaps - Creating airgap surface for rotor
    INFO - pyemmo.api.json.create_airgaps - Setting rotor airgap mesh size to band height 0.000300 m
    INFO - pyemmo.api.json.json - Fixing mesh size for points without mesh size by searching for closest point and resetting to its mesh size.
    INFO - pyemmo.api.json.json - Identifying boundary curves...
    INFO - pyemmo.api.json.boundaryJSON - Identifying primary and secondary boundary lines on symmetry axes
    INFO - pyemmo.api.json.boundaryJSON - Creating Movingband boundary...
    INFO - pyemmo.api.json.boundaryJSON - Identifying outer limit curves...
    INFO - pyemmo.api.json.json - Creating physicals from geometry...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 1 for layer 0 from winding layout...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 2 for layer 0 from winding layout...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 3 for layer 0 from winding layout...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 4 for layer 0 from winding layout...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 5 for layer 0 from winding layout...
    INFO - pyemmo.api.json.modelJSON - Getting phase index of slot 6 for layer 0 from winding layout...
    INFO - pyemmo.api.json.json - Creating rotor object...
    INFO - pyemmo.api.json.json - Creating stator object...
    INFO - pyemmo.api.json.json - Creating Machine object for model Toyota_Prius...
    INFO - pyemmo.api.json.json - Creating automatic, function based mesh sizes...
    INFO - pyemmo.api.json.json - Generating the Script object in JSON API...
    INFO - pyemmo.api.json.json - Creating Gmsh and GetDP input files...
    WARNING - pyemmo.script.script - Creation of "Compound Mesh" for domain "rotor domainLam" failed, because "rotor lamination" has only one surface.
    WARNING - pyemmo.script.script - Creation of "Compound Mesh" for domain "rotor airGap" failed, because "rotor airgap" has only one surface.
    WARNING - pyemmo.script.script - Creation of "Compound Mesh" for domain "stator airGap" failed, because "stator airgap" has only one surface.


2. Setup and run a simple voltage source simulation in ONELAB
-------------------------------------------------------------

After creating a machine model you can start a simulation in the GUI by
adjusting the parameters and clicking the “Run” botton. Or you can use
the ``run_simulation`` function and start a simulation from Python as a
subprocess. Therefore you can specify the same parameters you find in
GUI using a parameter dictionary like in the example below
(``param_dict``). You can find all adjustable constants and parameters
in the
`documentation <https://ttz-emo.thws.de/fileadmin/ttz-emo/pyemmo_doc/source/gen/pyemmo.script.script.html#onelab-model-constants>`__
under **ONELAB Model Constants** and **ONELAB Model Parameters**.

Additionally you can find more information on the ONELAB interface and
how to setup and use model parameters on this `ONELAB Wiki
page <https://gitlab.onelab.info/doc/tutorials/-/wikis/ONELAB-syntax-for-Gmsh-and-GetDP>`__.

.. code:: ipython3

    from pyemmo.functions.run_onelab import run_simulation, find_getdp

    # Simulation parameters
    n = 1500  # rpm
    U_amp = 100  # V
    phase = 60  # degree, 3 phase system initial phase shift
    # You can calculate the winding resistance analytically from Pyleecan:
    R_S = IPMSM_A.stator.comp_resistance_wind(T=20)
    print(f"Analytical stator winding resistance is {R_S*1e3:.2f} mOhm")
    # But we use a higher measured value from literature to speed up settling process
    R_S = 0.069  # stator phase resistance in Ohm from literature

    # for the transient simulation setup you need to specify the initial and final rotor
    # position, as well as the angular step in mechanical degrees.
    # Using the speed, GetDP calculates the time step and end time of the simulation.
    nbr_stator_periods = 6
    end_pos = 360 / IPMSM_A.get_pole_pair_number() * nbr_stator_periods
    nbr_steps = 16  # number of steps for one electrical period
    angular_step = 360 / 4 / nbr_steps  # mechanical step (to calculate time step)
    res_id = "voltage_source"  # result ID (will be the name of the results subfolder)

    # create param dict for simulation
    # See `pyemmo.functions.run_onelab.run_simulation` for details
    param_dict = {
        "getdp": {
            # We need to specify a getdp.exe path! `find_getdp` will search your system path
            # for getdp. If you don't have installed ONELAB (GetDP and Gmsh), you will need
            # to download the (standalone) executables from: https://onelab.info/
            # You can specify the path to getdp.exe as string here if its not on your `path`
            "exe": find_getdp(),
            "verbosity level": 3,  # ONELAB command line output verbosity [1-5, 99]
            # Mechanical Parameters
            "RPM": n,  # speed in rpm
            "initrotor_pos": 0.0,  # initial rotor position in mech. degree
            "d_theta": angular_step,  # angular step in degree
            "finalrotor_pos": end_pos,  # final rotor position in mech. degrees
            # Electrical / source parameters
            "Flag_SrcType_Stator": 2,  # Stator source type: 2 = voltage source
            "Flag_Cir": 0,  # No circuit -> direct voltage over winding phase
            "VV": U_amp,  # voltage amplitude
            "pA_deg": phase,  # phase offset for source with Sin
            "R_S": R_S,  # stator phase resistance in Ohm
            "Flag_Relaxation": 1,  # use relaxation function for source voltage
            "NbTrelax": 2,  # number of stator periods to apply voltage relaxation
            # Analysis parameters
            "Flag_AnalysisType": 1,  # 1 = transient (0 = static)
            "Flag_EC_Magnets": 0,  # no eddy currents in magnets
            "Flag_Debug": 1,  # show debug information
            "stop_criterion": 1e-8,  # residuum threshold
            # Results parameters
            "res": pyemmo_script.results_path,  # result folder
            "ResId": res_id,  # simulation id = results subfolder name (in results folder)
            "Flag_ClearResults": 1,  # remove previous results (if present)
            "Flag_PrintFields": 0,  # show field results in GUI
            # "msh": "",  # path to predefined mesh file
        },
        "pro": pyemmo_script.pro_file_path,  # machine .pro file
        # Gmsh executable and Parameters
        "gmsh": {
            "exe": "",  # Here you can give the path to a gmsh.exe. If nothing given, PyEMMO
            # will try to find Gmsh. This usually uses Gmsh provided with the gmsh python
            # package: https://pypi.org/project/gmsh/
            "gmsf": 2,  # gmsh global mesh size factor (multiplier for point mesh sizes).
            # > 1 = coarser mesh (used here for faster calculation)
        },
        "info": f"Simple voltage driven simulation with {int(U_amp)} V peak phase voltage at "
        f"{n}rpm for {nbr_stator_periods} periods with 2 periods of relaxation",
        # Here you could specify additional postoperations to be executed AFTER the solution.
        # These can be defined in the PyEMMO `Script` object. See Pyleecan API Tutorial.
        "PostOp": [],  # "GetBOnRadius" - "Get_LocalFields_Post"
    }


.. parsed-literal::

    Analytical stator winding resistance is 35.95 mOhm


.. code:: ipython3

    # Run the simulation
    results = run_simulation(param_dict)


.. parsed-literal::

    WARNING - pyemmo.functions.run_onelab - Removing previous results from folder: C:/Users/ganser/AppData/Roaming/pyemmo/Results/Toyota_Prius_ONELAB/res_Toyota_Prius\voltage_source
    INFO - pyemmo.functions.run_onelab - Running simulation for result-ID 'voltage_source'
    INFO - pyemmo.functions.run_onelab -
    INFO - pyemmo.functions.run_onelab - (.venv_312) d:\pyemmo\tutorials>echo on
    INFO - pyemmo.functions.run_onelab -
    INFO - pyemmo.functions.run_onelab - (.venv_312) d:\pyemmo\tutorials>echo d:\pyemmo\.venv_312\Scripts\gmsh.bat
    INFO - pyemmo.functions.run_onelab - d:\pyemmo\.venv_312\Scripts\gmsh.bat
    INFO - pyemmo.functions.run_onelab -
    INFO - pyemmo.functions.run_onelab - (.venv_312) d:\pyemmo\tutorials>where python
    INFO - pyemmo.functions.run_onelab - d:\pyemmo\.venv_312\Scripts\python.exe
    INFO - pyemmo.functions.run_onelab - C:\Users\ganser\AppData\Local\Programs\Python\Python312\python.exe
    INFO - pyemmo.functions.run_onelab -
    INFO - pyemmo.functions.run_onelab - (.venv_312) d:\pyemmo\tutorials>python "d:\pyemmo\.venv_312\Scripts\gmsh.bat\..\gmsh" "C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo" -run -setnumber gmsf 2
    INFO - pyemmo.functions.run_onelab - Info    : Running 'd:\pyemmo\.venv_312\Scripts\gmsh.bat\..\gmsh C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo -run -setnumber gmsf 2' [Gmsh 4.13.1, 1 node, max. 1 thread]
    INFO - pyemmo.functions.run_onelab - Info    : Started on Fri Apr 10 11:35:50 2026
    INFO - pyemmo.functions.run_onelab - Info    : Reading 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo'...
    INFO - pyemmo.functions.run_onelab - Info    : Starting subloop 1 in curve loop 14 (are you sure about this?)
    INFO - pyemmo.functions.run_onelab - Info    : Done reading 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo'
    INFO - pyemmo.functions.run_onelab - Info    : Reading 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo'...
    INFO - pyemmo.functions.run_onelab - Info    : Starting subloop 1 in curve loop 14 (are you sure about this?)
    INFO - pyemmo.functions.run_onelab - Info    : Done reading 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.geo'
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 163 - 160
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 181 - 180
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 230 - 168
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 249 - 247
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 252 - 250
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 255 - 253
    INFO - pyemmo.functions.run_onelab - Info    : Meshing 1D...
    INFO - pyemmo.functions.run_onelab - Info    : [  0%] Meshing curve 2 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 3 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 4 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 8 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 9 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 10 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 11 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 12 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 16 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 21 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 22 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 23 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 24 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 25 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 26 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 27 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 30 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing curve 31 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 41 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 42 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 43 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 44 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 46 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 47 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 60 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 61 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 62 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 63 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 64 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 65 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 66 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 67 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 68 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 82 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 83 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing curve 84 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 85 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 86 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 87 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 88 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 89 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 90 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 106 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 107 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 108 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 109 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 110 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 111 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 112 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 113 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 114 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 115 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 116 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing curve 117 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 131 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 132 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 133 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 134 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 135 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 136 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 144 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 145 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 146 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 147 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 148 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 149 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 150 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 151 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 152 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 153 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 154 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing curve 155 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 156 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 157 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 158 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 159 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 160 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 161 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 162 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 163 (Line) as a copy of curve 160
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 164 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 165 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 166 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 167 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 168 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 169 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 170 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 171 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 172 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing curve 173 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 174 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 175 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 176 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 177 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 178 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 179 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 180 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 181 (Line) as a copy of curve 180
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 182 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 183 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 184 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 185 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 186 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 187 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 188 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 189 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 190 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing curve 191 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 192 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 193 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 194 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 195 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 196 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 197 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 198 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 199 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 200 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 201 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 202 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 203 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 204 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 205 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 206 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 207 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 208 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing curve 209 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 210 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 211 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 212 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 213 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 214 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 215 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 216 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 217 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 218 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 219 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 220 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 221 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 222 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 223 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 224 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 225 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 226 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing curve 227 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 228 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 229 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 230 (Line) as a copy of curve 168
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 231 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 232 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 233 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 234 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 235 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 236 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 237 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 238 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 239 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 240 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 241 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 242 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 243 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 244 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing curve 245 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 246 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 247 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 248 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 249 (Line) as a copy of curve 247
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 250 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 251 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 252 (Line) as a copy of curve 250
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 253 (Line)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 254 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 255 (Line) as a copy of curve 253
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 256 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 257 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 258 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 259 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 260 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 261 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing curve 262 (Circle)
    INFO - pyemmo.functions.run_onelab - Info    : Done meshing 1D (Wall 0.209106s, CPU 0.09375s)
    INFO - pyemmo.functions.run_onelab - Info    : Meshing 2D...
    INFO - pyemmo.functions.run_onelab - Info    : [  0%] Meshing surface 2 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing surface 6 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 10%] Meshing surface 9 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing surface 12 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 20%] Meshing surface 14 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing surface 15 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 30%] Meshing surface 16 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing surface 17 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 40%] Meshing surface 18 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing surface 19 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 50%] Meshing surface 20 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing surface 21 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing surface 22 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 60%] Meshing surface 23 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing surface 24 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 70%] Meshing surface 25 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing surface 26 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 80%] Meshing surface 27 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing surface 28 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [ 90%] Meshing surface 29 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing surface 30 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : [100%] Meshing surface 31 (Plane, Frontal-Delaunay)
    INFO - pyemmo.functions.run_onelab - Info    : Done meshing 2D (Wall 0.183668s, CPU 0.171875s)
    INFO - pyemmo.functions.run_onelab - Info    : Meshing 3D...
    INFO - pyemmo.functions.run_onelab - Info    : Done meshing 3D (Wall 0.00103092s, CPU 0.015625s)
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 163 - 160
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 181 - 180
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 230 - 168
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 249 - 247
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 252 - 250
    INFO - pyemmo.functions.run_onelab - Info    : Reconstructing periodicity for curve connection 255 - 253
    INFO - pyemmo.functions.run_onelab - Info    : 6675 nodes 12360 elements
    INFO - pyemmo.functions.run_onelab - Info    : Writing 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.msh'...
    INFO - pyemmo.functions.run_onelab - Info    : Done writing 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.msh'
    INFO - pyemmo.functions.run_onelab - Info    : Saving database 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.db'...
    INFO - pyemmo.functions.run_onelab - Info    : Done saving database 'C:/Users/ganser/AppData/Roaming/pyemmo/Results\Toyota_Prius_ONELAB\Toyota_Prius.db'
    INFO - pyemmo.functions.run_onelab - Info    : Stopped on Fri Apr 10 11:35:50 2026 (From start: Wall 0.51412s, CPU 0.453125s)
    INFO - pyemmo.functions.run_onelab - Info    : Started (Fri Apr 10 11:35:51 2026, Wall = 0.00200009s, CPU = 0.015625s, Mem = 17.6055Mb)
    INFO - pyemmo.functions.run_onelab - [34m==== ANALYSIS PARAMETERS ====[0m
    INFO - pyemmo.functions.run_onelab - [34mMachine type: Synchronous Machine[0m
    INFO - pyemmo.functions.run_onelab - [34mAnalysis type: transient[0m
    INFO - pyemmo.functions.run_onelab - [34mStator Source type: voltage source[0m
    INFO - pyemmo.functions.run_onelab - [34mStart position [deg]: 0.0[0m
    INFO - pyemmo.functions.run_onelab - [34mEnd position (synchronous) [deg]: 540.0[0m
    INFO - pyemmo.functions.run_onelab - [34mStep size [deg]: 5.625000[0m
    INFO - pyemmo.functions.run_onelab - [34mMech. speed [rpm]: 1500.000[0m
    INFO - pyemmo.functions.run_onelab - [34mTotal number of time steps: 97.0[0m
    INFO - pyemmo.functions.run_onelab - [34mSymmetry Factor: 8[0m
    INFO - pyemmo.functions.run_onelab - [34mFlag Symmetry: 1[0m
    INFO - pyemmo.functions.run_onelab - [34mNumber of poles in Model: 1[0m
    INFO - pyemmo.functions.run_onelab - [34mResults folder: C:/Users/ganser/AppData/Roaming/pyemmo/Results/Toyota_Prius_ONELAB/res_Toyota_Prius[0m
    INFO - pyemmo.functions.run_onelab - [34mResults Id: voltage_source[0m
    INFO - pyemmo.functions.run_onelab - [34mClear Results: Yes[0m
    INFO - pyemmo.functions.run_onelab - [34mSave field results: No[0m
    INFO - pyemmo.functions.run_onelab - [34m[0m
    INFO - pyemmo.functions.run_onelab - [34m==== MACHINE PARAMETERS ====[0m
    INFO - pyemmo.functions.run_onelab - [34mNumber of poles total (NbrPolesTot) = 8[0m
    INFO - pyemmo.functions.run_onelab - [34mAirgap radius = 0.08050[0m
    INFO - pyemmo.functions.run_onelab - [34meccentricity_dynamic = 0.000000e+00 mm[0m
    INFO - pyemmo.functions.run_onelab - [34meccentricity_static =  0.000000e+00 mm[0m
    INFO - pyemmo.functions.run_onelab - [34mNumber of Movingband Segments (for PostProcessing) = 360[0m
    INFO - pyemmo.functions.run_onelab - [34mGlobal mesh size factor (for PostProcessing) = 1[0m
    INFO - pyemmo.functions.run_onelab - [34m[0m
    INFO - pyemmo.functions.run_onelab - [34mVoltage Source Excitation with parameters:[0m
    INFO - pyemmo.functions.run_onelab - [34m    Input Voltage Amplitude: 100.000 V[0m
    INFO - pyemmo.functions.run_onelab - [34m    Input Voltage RMS: 70.721 V[0m
    INFO - pyemmo.functions.run_onelab - [34m    Input Voltage Phase Offset (Phase A): 60.00 deg[0m
    INFO - pyemmo.functions.run_onelab - [34m    Input Voltage Phase Offset (Phase B): -60.00 deg[0m
    INFO - pyemmo.functions.run_onelab - [34m    Input Voltage Phase Offset (Phase C): 180.00 deg[0m
    INFO - pyemmo.functions.run_onelab - [34mFlag_Cir = 0[0m
    INFO - pyemmo.functions.run_onelab - [34mFlag_SrcType_Stator = 2[0m
    INFO - pyemmo.functions.run_onelab - [34mFlag_ImposedCurrentDensity = 0[0m
    INFO - pyemmo.functions.run_onelab - [34mFinal rotor position is 540.0 deg[0m
    INFO - pyemmo.functions.run_onelab - [34mSimulation Setup:[0m
    INFO - pyemmo.functions.run_onelab - [34m    Stop time = 6.000e-02 s[0m
    INFO - pyemmo.functions.run_onelab - [34m    TimeStep = 6.250e-04 s[0m
    INFO - pyemmo.functions.run_onelab - [34m    n: 25.000[0m
    INFO - pyemmo.functions.run_onelab - [34m    freq_stator: 100.000[0m
    INFO - pyemmo.functions.run_onelab - [34m    n_sync: 25.000[0m
    INFO - pyemmo.functions.run_onelab - [34m    slip: 0.00000[0m
    INFO - pyemmo.functions.run_onelab - [34m    asm_finalrotor_pos: 900.00000 = 360 * (nbr_stator_per / f_s) * n =  (10.0 / 100.00000) * 25.00000[0m
    INFO - pyemmo.functions.run_onelab - [34m    finalrotor_pos: 540.00000[0m
    INFO - pyemmo.functions.run_onelab - [34m    timemax: 0.060[0m
    INFO - pyemmo.functions.run_onelab - [34m    delta_time: 0.001[0m
    INFO - pyemmo.functions.run_onelab - [34mRemanence flux density of magnet material MagnetPrius at temperature 20.0 °C is 1.24000 T[0m
    INFO - pyemmo.functions.run_onelab - [34mResId is /voltage_source/[0m
    INFO - pyemmo.functions.run_onelab - [34mResults Directory is C:\Users\ganser\AppData\Roaming\pyemmo\Results\Toyota_Prius_ONELAB\res_Toyota_Prius\voltage_source\[0m
    INFO - pyemmo.functions.run_onelab - [34mIQ:  0[0m
    INFO - pyemmo.functions.run_onelab - [34mID:  0[0m
    INFO - pyemmo.functions.run_onelab - [34mI0:  0[0m
    INFO - pyemmo.functions.run_onelab - [34mTime loop from t_0 = 0.000000ms to t_max = 60.000000ms with dt = 0.625000ms[0m
    INFO - pyemmo.functions.run_onelab - [34mExecuting 96.0 steps[0m
    INFO - pyemmo.functions.run_onelab - [34mP r e - P r o c e s s i n g . . .[0m
    INFO - pyemmo.functions.run_onelab - Info    : System 1/1: 4470 Dofs
    INFO - pyemmo.functions.run_onelab - [34mE n d   P r e - P r o c e s s i n g[0m
    INFO - pyemmo.functions.run_onelab - [34mP r o c e s s i n g . . .[0m
    INFO - pyemmo.functions.run_onelab - [34mExecuting first static simulation at rotor position 0.000000 deg[0m
    INFO - pyemmo.functions.run_onelab - Info    : Discarded DtDof term in static analysis
    INFO - pyemmo.functions.run_onelab - [35mWarning : IterativeLoop did NOT converge (21 iterations, residual 0.181359)[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (6 iterations, residual 3.39589e-12)
    INFO - pyemmo.functions.run_onelab -  0 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.000625 s (TimeStep 1, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 1 / 96  -  1.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (8 iterations, residual 8.31206e-10)
    INFO - pyemmo.functions.run_onelab -  0.000625 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.00125 s (TimeStep 2, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 2 / 96  -  2.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (8 iterations, residual 8.20059e-12)
    INFO - pyemmo.functions.run_onelab -  0.00125 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.001875 s (TimeStep 3, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 3 / 96  -  3.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 7.86784e-13)
    INFO - pyemmo.functions.run_onelab -  0.001875 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0025 s (TimeStep 4, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 4 / 96  -  4.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (14 iterations, residual 3.07262e-13)
    INFO - pyemmo.functions.run_onelab -  0.0025 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.003125 s (TimeStep 5, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 5 / 96  -  5.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 4.10674e-11)
    INFO - pyemmo.functions.run_onelab -  0.003125 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.00375 s (TimeStep 6, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 6 / 96  -  6.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.11697e-09)
    INFO - pyemmo.functions.run_onelab -  0.00375 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.004375 s (TimeStep 7, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 7 / 96  -  7.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 5.78996e-10)
    INFO - pyemmo.functions.run_onelab -  0.004375 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.005 s (TimeStep 8, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 8 / 96  -  8.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.31142e-11)
    INFO - pyemmo.functions.run_onelab -  0.005 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.005625 s (TimeStep 9, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 9 / 96  -  9.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 4.36544e-12)
    INFO - pyemmo.functions.run_onelab -  0.005625 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.00625 s (TimeStep 10, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 9 / 96  -  9.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.09328e-10)
    INFO - pyemmo.functions.run_onelab -  0.006249999999999999 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.006875 s (TimeStep 11, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 10 / 96  -  10.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 7.95553e-12)
    INFO - pyemmo.functions.run_onelab -  0.006874999999999999 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0075 s (TimeStep 12, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 11 / 96  -  11.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 5.82939e-09)
    INFO - pyemmo.functions.run_onelab -  0.007499999999999999 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.008125 s (TimeStep 13, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 12 / 96  -  12.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 8.71491e-10)
    INFO - pyemmo.functions.run_onelab -  0.008124999999999999 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.00875 s (TimeStep 14, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 13 / 96  -  13.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.26671e-11)
    INFO - pyemmo.functions.run_onelab -  0.008749999999999999 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.009375 s (TimeStep 15, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 15 / 96  -  15.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (8 iterations, residual 6.51722e-10)
    INFO - pyemmo.functions.run_onelab -  0.009375 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.01 s (TimeStep 16, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 16 / 96  -  16.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 4.33736e-11)
    INFO - pyemmo.functions.run_onelab -  0.01 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.010625 s (TimeStep 17, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 17 / 96  -  17.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.2354e-13)
    INFO - pyemmo.functions.run_onelab -  0.010625 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.01125 s (TimeStep 18, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 18 / 96  -  18.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 3.22838e-11)
    INFO - pyemmo.functions.run_onelab -  0.01125 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.011875 s (TimeStep 19, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 19 / 96  -  19.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.55324e-10)
    INFO - pyemmo.functions.run_onelab -  0.011875 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0125 s (TimeStep 20, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 20 / 96  -  20.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 3.65102e-11)
    INFO - pyemmo.functions.run_onelab -  0.0125 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.013125 s (TimeStep 21, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 21 / 96  -  21.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 4.28129e-12)
    INFO - pyemmo.functions.run_onelab -  0.013125 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.01375 s (TimeStep 22, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 22 / 96  -  22.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 5.02668e-10)
    INFO - pyemmo.functions.run_onelab -  0.01375 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.014375 s (TimeStep 23, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 23 / 96  -  24.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 4.16561e-12)
    INFO - pyemmo.functions.run_onelab -  0.014375 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.015 s (TimeStep 24, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 24 / 96  -  25.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.47243e-09)
    INFO - pyemmo.functions.run_onelab -  0.015 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.015625 s (TimeStep 25, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 25 / 96  -  26.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.46263e-09)
    INFO - pyemmo.functions.run_onelab -  0.015625 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.01625 s (TimeStep 26, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 26 / 96  -  27.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.09414e-10)
    INFO - pyemmo.functions.run_onelab -  0.01625 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.016875 s (TimeStep 27, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 27 / 96  -  28.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.15105e-13)
    INFO - pyemmo.functions.run_onelab -  0.016875 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0175 s (TimeStep 28, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 28 / 96  -  29.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 6.74054e-10)
    INFO - pyemmo.functions.run_onelab -  0.01750000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.018125 s (TimeStep 29, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 29 / 96  -  30.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 5.89656e-10)
    INFO - pyemmo.functions.run_onelab -  0.01812500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.01875 s (TimeStep 30, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 30 / 96  -  31.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.31679e-13)
    INFO - pyemmo.functions.run_onelab -  0.01875000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.019375 s (TimeStep 31, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 31 / 96  -  32.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.3035e-11)
    INFO - pyemmo.functions.run_onelab -  0.01937500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.02 s (TimeStep 32, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 32 / 96  -  33.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 2.16914e-12)
    INFO - pyemmo.functions.run_onelab -  0.02000000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.020625 s (TimeStep 33, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 33 / 96  -  34.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 1.59383e-10)
    INFO - pyemmo.functions.run_onelab -  0.02062500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.02125 s (TimeStep 34, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 34 / 96  -  35.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 2.83744e-10)
    INFO - pyemmo.functions.run_onelab -  0.02125000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.021875 s (TimeStep 35, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 35 / 96  -  36.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.49115e-12)
    INFO - pyemmo.functions.run_onelab -  0.02187500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0225 s (TimeStep 36, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 36 / 96  -  37.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 6.85947e-09)
    INFO - pyemmo.functions.run_onelab -  0.02250000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.023125 s (TimeStep 37, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 37 / 96  -  38.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.17843e-09)
    INFO - pyemmo.functions.run_onelab -  0.02312500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.02375 s (TimeStep 38, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 38 / 96  -  39.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.38037e-11)
    INFO - pyemmo.functions.run_onelab -  0.02375000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.024375 s (TimeStep 39, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 39 / 96  -  40.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.3302e-10)
    INFO - pyemmo.functions.run_onelab -  0.02437500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.025 s (TimeStep 40, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 40 / 96  -  41.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 7.3379e-11)
    INFO - pyemmo.functions.run_onelab -  0.02500000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.025625 s (TimeStep 41, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 41 / 96  -  42.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 2.55356e-12)
    INFO - pyemmo.functions.run_onelab -  0.02562500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.02625 s (TimeStep 42, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 42 / 96  -  43.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 9.39335e-09)
    INFO - pyemmo.functions.run_onelab -  0.02625000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.026875 s (TimeStep 43, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 43 / 96  -  44.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 3.61105e-12)
    INFO - pyemmo.functions.run_onelab -  0.02687500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0275 s (TimeStep 44, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 44 / 96  -  45.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 7.05202e-09)
    INFO - pyemmo.functions.run_onelab -  0.02750000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.028125 s (TimeStep 45, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 45 / 96  -  46.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 3.90902e-09)
    INFO - pyemmo.functions.run_onelab -  0.02812500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.02875 s (TimeStep 46, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 46 / 96  -  47.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 3.98713e-10)
    INFO - pyemmo.functions.run_onelab -  0.02875000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.029375 s (TimeStep 47, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 47 / 96  -  49.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 4.65784e-11)
    INFO - pyemmo.functions.run_onelab -  0.02937500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.03 s (TimeStep 48, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 48 / 96  -  50.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.15977e-09)
    INFO - pyemmo.functions.run_onelab -  0.03000000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.030625 s (TimeStep 49, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 49 / 96  -  51.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 3.59248e-09)
    INFO - pyemmo.functions.run_onelab -  0.03062500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.03125 s (TimeStep 50, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 50 / 96  -  52.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 9.96804e-13)
    INFO - pyemmo.functions.run_onelab -  0.03125000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.031875 s (TimeStep 51, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 51 / 96  -  53.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 1.47448e-09)
    INFO - pyemmo.functions.run_onelab -  0.03187500000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0325 s (TimeStep 52, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 52 / 96  -  54.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 9.50773e-12)
    INFO - pyemmo.functions.run_onelab -  0.03250000000000001 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.033125 s (TimeStep 53, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 53 / 96  -  55.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 4.35875e-09)
    INFO - pyemmo.functions.run_onelab -  0.03312500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.03375 s (TimeStep 54, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 54 / 96  -  56.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.54106e-09)
    INFO - pyemmo.functions.run_onelab -  0.03375000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.034375 s (TimeStep 55, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 55 / 96  -  57.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 5.46173e-09)
    INFO - pyemmo.functions.run_onelab -  0.03437500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.035 s (TimeStep 56, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 56 / 96  -  58.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 2.28534e-12)
    INFO - pyemmo.functions.run_onelab -  0.03500000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.035625 s (TimeStep 57, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 57 / 96  -  59.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 4.78917e-10)
    INFO - pyemmo.functions.run_onelab -  0.03562500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.03625 s (TimeStep 58, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 58 / 96  -  60.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 4.70527e-11)
    INFO - pyemmo.functions.run_onelab -  0.03625000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.036875 s (TimeStep 59, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 59 / 96  -  61.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.87304e-11)
    INFO - pyemmo.functions.run_onelab -  0.03687500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0375 s (TimeStep 60, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 60 / 96  -  62.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 5.10199e-13)
    INFO - pyemmo.functions.run_onelab -  0.03750000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.038125 s (TimeStep 61, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 61 / 96  -  63.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (14 iterations, residual 9.58864e-12)
    INFO - pyemmo.functions.run_onelab -  0.03812500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.03875 s (TimeStep 62, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 62 / 96  -  64.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.20373e-09)
    INFO - pyemmo.functions.run_onelab -  0.03875000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.039375 s (TimeStep 63, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 63 / 96  -  65.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.77759e-11)
    INFO - pyemmo.functions.run_onelab -  0.03937500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.04 s (TimeStep 64, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 64 / 96  -  66.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 3.42826e-11)
    INFO - pyemmo.functions.run_onelab -  0.04000000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.040625 s (TimeStep 65, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 65 / 96  -  67.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 3.41277e-11)
    INFO - pyemmo.functions.run_onelab -  0.04062500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.04125 s (TimeStep 66, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 66 / 96  -  68.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 7.79734e-11)
    INFO - pyemmo.functions.run_onelab -  0.04125000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.041875 s (TimeStep 67, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 67 / 96  -  69.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 3.59111e-09)
    INFO - pyemmo.functions.run_onelab -  0.04187500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0425 s (TimeStep 68, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 68 / 96  -  70.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 3.77249e-10)
    INFO - pyemmo.functions.run_onelab -  0.04250000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.043125 s (TimeStep 69, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 69 / 96  -  71.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.35017e-12)
    INFO - pyemmo.functions.run_onelab -  0.04312500000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.04375 s (TimeStep 70, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 70 / 96  -  72.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 9.20444e-10)
    INFO - pyemmo.functions.run_onelab -  0.04375000000000002 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.044375 s (TimeStep 71, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 71 / 96  -  74.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 9.36457e-14)
    INFO - pyemmo.functions.run_onelab -  0.04437500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.045 s (TimeStep 72, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 72 / 96  -  75.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 4.67923e-10)
    INFO - pyemmo.functions.run_onelab -  0.04500000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.045625 s (TimeStep 73, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 73 / 96  -  76.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.66341e-09)
    INFO - pyemmo.functions.run_onelab -  0.04562500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.04625 s (TimeStep 74, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 74 / 96  -  77.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.99432e-09)
    INFO - pyemmo.functions.run_onelab -  0.04625000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.046875 s (TimeStep 75, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 75 / 96  -  78.1 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.5386e-10)
    INFO - pyemmo.functions.run_onelab -  0.04687500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0475 s (TimeStep 76, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 76 / 96  -  79.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 2.07315e-12)
    INFO - pyemmo.functions.run_onelab -  0.04750000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.048125 s (TimeStep 77, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 77 / 96  -  80.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (14 iterations, residual 1.77158e-13)
    INFO - pyemmo.functions.run_onelab -  0.04812500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.04875 s (TimeStep 78, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 78 / 96  -  81.2 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.64343e-09)
    INFO - pyemmo.functions.run_onelab -  0.04875000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.049375 s (TimeStep 79, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 79 / 96  -  82.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 5.22958e-11)
    INFO - pyemmo.functions.run_onelab -  0.04937500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.05 s (TimeStep 80, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 80 / 96  -  83.3 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.31784e-11)
    INFO - pyemmo.functions.run_onelab -  0.05000000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.050625 s (TimeStep 81, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 81 / 96  -  84.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 2.60181e-12)
    INFO - pyemmo.functions.run_onelab -  0.05062500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.05125 s (TimeStep 82, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 82 / 96  -  85.4 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 6.47918e-13)
    INFO - pyemmo.functions.run_onelab -  0.05125000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.051875 s (TimeStep 83, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 83 / 96  -  86.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (9 iterations, residual 4.25655e-09)
    INFO - pyemmo.functions.run_onelab -  0.05187500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0525 s (TimeStep 84, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 84 / 96  -  87.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 8.84042e-11)
    INFO - pyemmo.functions.run_onelab -  0.05250000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.053125 s (TimeStep 85, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 85 / 96  -  88.5 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 2.32559e-12)
    INFO - pyemmo.functions.run_onelab -  0.05312500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.05375 s (TimeStep 86, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 86 / 96  -  89.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.61176e-10)
    INFO - pyemmo.functions.run_onelab -  0.05375000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.054375 s (TimeStep 87, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 87 / 96  -  90.6 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.98015e-11)
    INFO - pyemmo.functions.run_onelab -  0.05437500000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.055 s (TimeStep 88, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 88 / 96  -  91.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (12 iterations, residual 1.57459e-12)
    INFO - pyemmo.functions.run_onelab -  0.05500000000000003 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.055625 s (TimeStep 89, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 89 / 96  -  92.7 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 8.8806e-13)
    INFO - pyemmo.functions.run_onelab -  0.05562500000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.05625 s (TimeStep 90, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 90 / 96  -  93.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 2.25663e-09)
    INFO - pyemmo.functions.run_onelab -  0.05625000000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.056875 s (TimeStep 91, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 91 / 96  -  94.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (10 iterations, residual 1.1205e-10)
    INFO - pyemmo.functions.run_onelab -  0.05687500000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.0575 s (TimeStep 92, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 92 / 96  -  95.8 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 2.2405e-12)
    INFO - pyemmo.functions.run_onelab -  0.05750000000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.058125 s (TimeStep 93, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 93 / 96  -  96.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (13 iterations, residual 6.54704e-11)
    INFO - pyemmo.functions.run_onelab -  0.05812500000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.05875 s (TimeStep 94, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 94 / 96  -  97.9 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 2.98291e-13)
    INFO - pyemmo.functions.run_onelab -  0.05875000000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.059375 s (TimeStep 95, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 95 / 96  -  99.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 8.91008e-14)
    INFO - pyemmo.functions.run_onelab -  0.05937500000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - Info    : Theta Time = 0.06 s (TimeStep 96, DTime 0.000625)
    INFO - pyemmo.functions.run_onelab - [34mStep 96 / 96  -  100.0 percent[0m
    INFO - pyemmo.functions.run_onelab - Info    : IterativeLoop converged (11 iterations, residual 1.91862e-09)
    INFO - pyemmo.functions.run_onelab -  0.06000000000000004 0.000213071537346573
    INFO - pyemmo.functions.run_onelab - [34mE n d   P r o c e s s i n g[0m
    INFO - pyemmo.functions.run_onelab - Info    : Stopped (Fri Apr 10 11:38:40 2026, Wall = 169.672s, CPU = 157.938s, Mem = 57.5391Mb)
    INFO - pyemmo.functions.run_onelab - Subprocess returned exit code 0
    INFO - pyemmo.functions.import_results - Import results for result-ID 'voltage_source'
    WARNING - pyemmo.functions.import_results - Could not find result file for winding voltage Ua_w
    WARNING - pyemmo.functions.import_results - Could not find result file for winding voltage Ub_w
    WARNING - pyemmo.functions.import_results - Could not find result file for winding voltage Uc_w
    WARNING - pyemmo.functions.run_onelab - Could not save results to json file!
    Traceback (most recent call last):
      File "D:\pyemmo\pyemmo\functions\run_onelab.py", line 687, in run_simulation
        core_loss.write_simple(core_loss_res_file, time, loss_data)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\ganser\AppData\Local\Programs\Python\Python312\Lib\json\__init__.py", line 179, in dump
        for chunk in iterable:
                     ^^^^^^^^
      File "C:\Users\ganser\AppData\Local\Programs\Python\Python312\Lib\json\encoder.py", line 432, in _iterencode
        yield from _iterencode_dict(o, _current_indent_level)
      File "C:\Users\ganser\AppData\Local\Programs\Python\Python312\Lib\json\encoder.py", line 406, in _iterencode_dict
        yield from chunks
      File "C:\Users\ganser\AppData\Local\Programs\Python\Python312\Lib\json\encoder.py", line 439, in _iterencode
        o = _default(o)
            ^^^^^^^^^^^
      File "C:\Users\ganser\AppData\Local\Programs\Python\Python312\Lib\json\encoder.py", line 180, in default
        raise TypeError(f'Object of type {o.__class__.__name__} '
    TypeError: Object of type ndarray is not JSON serializable


After the simulation has finished, PyEMMO automatically imports the
standard global result values using
``pyemmo.functions.import_results.main`` function and output the results
in a dictionary structure. Here we store this output in the variable
``results``.

Using ``print`` or ``pprint`` (pretty-print) we can show the dictionary
keys.

Depended on the simulation parameters defined in
``param_dict["getdp"]``, not all of the keys must contain result data.

.. code:: ipython3

    from pprint import pprint

    print("Result quantities:")
    pprint(list(results.keys()))
    print("\nVoltage result phase indices:")
    pprint(list(results["voltage"].keys()))


.. parsed-literal::

    Result quantities:
    ['time',
     'rotorPos',
     'current',
     'voltage',
     'torque',
     'torque_vw',
     'rotor torque',
     'stator torque',
     'flux',
     'inducedVoltage']

    Voltage result phase indices:
    ['a', 'b', 'c']


The simple voltage source simulation creates a 3 phase sine voltage
excitation over each of the winding phase objects. Where one winding
object consists of a voltage source describing the induced voltage
:math:`U_i` (voltage over the inductance) and a resistance :math:`R_S`
which was defined as model parameter. For each winding phase the
following condition must be true:

.. math::


   U_\mathrm{in} = R_S \cdot I_S + U_i

We use ``matplotlib.pyplot`` to plot the voltage results and calculate
the voltage drop over the resistance:

.. code:: ipython3

    from matplotlib import pyplot as plt

    %matplotlib inline

    colors = plt.get_cmap("tab10").colors

    # PLOT VOLTAGES:
    fig, ax = plt.subplots()

    for phase in "a":#bc":

        # plot input voltage over winding phase
        U_in = results["voltage"][phase]
        ax.plot(results["time"], U_in, label=f"$U_\\mathrm{{in,{phase}}}$")

        # plot induced voltage
        U_emf = results["inducedVoltage"][phase]
        ax.plot(
            results["time"][1:],  # induced voltage only available in second time step
            U_emf,
            label=f"$U_{{i,\mathrm{{{phase}}}}}$",
        )

        # remaining voltage is voltage drop over R_S
        ax.plot(
            results["time"][1:],
            U_in[1:] - U_emf,
            label=f"$U_{{R_S,\\mathrm{{{phase}}}}}=R_S \\cdot I_S$",
        )
    ax.set_ylabel("Voltage in V")
    ax.grid(True)
    _ = ax.legend()




.. image:: output_9_0.png


Using the current results we can show that the phase current and the
corresponding voltage drop over the resistance are in phase:

.. code:: ipython3

    # PLOT CURRENT AND RS VOLTAGE DROP
    fig, ax = plt.subplots()
    secax = ax.twinx()
    secax.set_ylabel("Voltage in V")
    for i, phase in enumerate("abc"):

        # plot phase current
        I = results["current"][phase]
        ax.plot(results["time"], I, label=f"$I_{{S,\\mathrm{{{phase}}}}}$")

        # Show that remaining voltage (voltage drop over R_S) is in phase with I_S
        U_in = results["voltage"][phase]
        U_emf = results["inducedVoltage"][phase]
        secax.plot(
            results["time"][1:],
            U_in[1:] - U_emf,
            linestyle="none",
            marker=".",
            alpha=0.8,
            color=colors[i],
            label=f"$U_{{R_S,\\mathrm{{{phase}}}}}=R_S \\cdot I_{{S,\\mathrm{{{phase}}}}}$",
        )

    ax.set_ylabel("Current in A")
    ax.grid(True)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.1), ncol=3)
    _ = secax.legend(loc=1)
    # ax.set_xlim([results["time"][-1] - T_s, results["time"][-1]])



.. image:: output_11_0.png


Finally we can have a look at the resulting torque and dq-flux results.
Due to the electrical time constant of the system
:math:`\tau = \frac{L_S}{R_S}` we notice a settling process. The
relaxation (ramping the voltage amplitude in a quarter sine wave) helps
with the stability of this settling process.

.. code:: ipython3

    # Plot torque and dq flux linkage

    fig, ax = plt.subplots()
    ax.plot(results["time"], results["torque"], ".-")
    ax.set_ylabel("Torque in Nm")
    ax.set_xlabel("Time in s")
    ax.grid()

    fig, ax = plt.subplots()
    ax.plot(results["time"], results["flux"]["d"], ".-", label="d-flux linkage")
    ax.plot(results["time"], results["flux"]["q"], ".-", label="q-flux linkage")
    ax.set_ylabel("Flux linkage in Wb")
    ax.set_xlabel("Time in s")
    ax.grid()
    _ = ax.legend()



.. image:: output_13_0.png



.. image:: output_13_1.png
