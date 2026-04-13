PyEMMO Core Loss Calculation Tutorial
=====================================

tbd

1. Create a Machine Model with Core Loss Information
----------------------------------------------------

.. raw:: html

   <!-- Pyleecan has a lot of useful tutorials under [Pyleecan tutorials][pylcn_tutorials].
   See those for futher details on how to use the pyleecan motor toolbox.

   There are two ways to get a Pyleecan machine:

   - Load a existing machine using the `load` function.
   - Create a machine with a python script by using the Pyleecan classes.
     See the [`01_tuto_Machine.ipynb`][pylcn_tutorial_machine] tutorial for that.


   You can load an existing Pyleecan model using:

   [pylcn_tutorials]: https://pyleecan.org/tutorials.html
   [pylcn_tutorial_machine]: https://pyleecan.org/01_tuto_Machine.html -->

.. code:: ipython3

    # set log level to disable necessary matplotlib log messages
    import logging

    logging.getLogger("matplotlib").setLevel(logging.ERROR)

.. code:: ipython3

    %matplotlib inline
    # Tell matlab to use the inline kernel to show the figures in the notebook:

.. code:: ipython3

    # Load the machine
    from __future__ import annotations

    from os.path import join

    from pyleecan.definitions import DATA_DIR
    from pyleecan.Functions.load import load
    from pyemmo.api.pyleecan import main as pyleecan_api
    import os
    import gmsh as gmsh_api
    from pyemmo.definitions import RESULT_DIR
    from pyemmo.api.json.json import main as json_api_main
    from pyemmo.api.pyleecan.create_param_dict import create_param_dict
    from pyemmo.api.pyleecan.create_pyleecan_simulation import create_simulation
    from pyemmo.api.pyleecan.translate_machine import translate_machine

    pyleecan_machine = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
    model_name = "Toyota_Prius"

    if not gmsh_api.isInitialized():
        gmsh_api.initialize()

    # suppress output of log messages to console.
    # See https://gitlab.onelab.info/gmsh/gmsh/-/issues/1901
    # Use gmsh.logger.start(), gmsh.logger.get(), gmsh.logger.stop() to catch logs.
    gmsh_api.option.setNumber("General.Terminal", 0)

    # add new gmsh model in case api is called multiple times:
    gmsh_api.model.add(model_name)

    # Create model parameter dict
    simulation = create_simulation(pyleecan_machine, i_d=0, i_q=0, speed=1000)
    paramDict = create_param_dict(pyleecan_machine, simulation, None)
    paramDict["flag_openGUI"] = True
    paramDict["calcIronLoss"] = True

    geo_translation_dict = translate_machine(pyleecan_machine)
    pyemmo_script = json_api_main(
        geo=geo_translation_dict,
        extInfo=paramDict,
        model="./core_loss_tutorial/",
        gmsh="",
        getdp="",
    )

This can be a default machine from the Pyleecan ``DATA`` directory or
you can create your own machine using the Pyleecan GUI. See `Pyleecan
Webinar on how to use the GUI <https://pyleecan.org/webinar_1.html>`__
or just try it yourself by running:

``python -m pyleecan``

in the command line.

4. How to run a simple simulation in ONELAB
-------------------------------------------

After creating a machine model you can start a simulation in the GUI by
adjusting the parameters and clicking the “Run” button. Or you can use
the ``run_simulation`` function and start a simulation from Python as a
subprocess. Therefore you can specify the same parameters you find in
GUI using a parameter dictionary like in the example below
(``param_dict``). You can find all adjustable constants and parameters
in the documentation under **ONELAB Model Constants** and **ONELAB Model
Parameters**.

For synchronous machines PyEMMO will try to calculate the dq-System
offset between rotor and stator. See **dq-Offset calculation** for more
details.

.. code:: ipython3

    import os
    import time

    import numpy as np

    from pyemmo.functions.run_onelab import run_simulation, find_getdp

    # Simulation parameters
    n = 5000
    id = -10
    iq = 50
    resId = "test_working_point"  # result identifier and result folder name

    # create param dict for simulation
    param_dict = {
        # model .pro file path
        "pro": pyemmo_script.pro_file_path,
        # Gmsh Parameters
        "gmsh": {"exe": r"", "gmsf": 2, "verbosity level": 2},
        # GetDP Parameters
        "getdp": {
            "exe": find_getdp(),  # GetDP executable, you can use the function findGetDP
            # which tries to find the exe on you PC.
            # change gmsh and getdp verbosity level (0-99)
            # 0 - fatal, 1 - error, 2 - warning, 3 - info, 5 - debug, 99 - extended debug
            "verbosity level": 2,
            "Flag_Debug": 0,  # epxort debug infos and results from GetDP
            ## Analysis Parameters
            "Flag_AnalysisType": 1,  # 0 - static, 1 - transient
            "Flag_SrcType_Stator": 1,  # 1 - current source, 2 - voltage source (not finally implemented)
            "initrotor_pos": 0.0,  # initial rotor position in °
            "d_theta": 2.8125,  # angular step size in °
            "finalrotor_pos": 90,  # final rotor position in °
            # "RPM": n, # rotational speed
            "Flag_EC_Magnets": 0,  # control magnet eddy current calculation
            #
            ## Result settings
            "res": pyemmo_script.results_path,  # main results folder
            "ResId": resId,  # current simulation result folder ID
            "Flag_PrintFields": 0,  # control field result output (.pos files, only last timestep)
            "Flag_ClearResults": 0,  # remove results if existing, otherwise existing results will be imported
            #
            ## Excitation parameters
            "ID_RMS": id / np.sqrt(2),
            "IQ_RMS": iq / np.sqrt(2),
        },
        # in combination with 'GetBIron' PostOp entry -> Core Loss calculation
        "hyst": 102,
        "eddy": 1.5,
        "exc": 0,
        "sym": 8,
        "axLen": pyemmo_script.machine.stator.axial_length,
        # "log": f"{resId}.log",  # optional: log file name
        "info": "",  # optional: info string to save with simulation config
        "datetime": time.ctime(),  # optional: current time
        "PostOp": ["GetBIron"],  # PostOperations to execute after simulation.
        # Standard Option is: GetBOnRadius
    }

.. code:: ipython3

    # run simulation:
    results = run_simulation(param_dict)

.. code:: ipython3

    from pprint import pprint

    pprint(results.keys())
    try:
        pprint(results["coreLoss"].keys())
        pprint(results["coreLoss"]["rotor"].keys())
    except:
        pass

.. code:: ipython3

    # Plot core loss data
    from matplotlib import pyplot as plt

    fig, axes = plt.subplots(1, 2)
    for i, side in enumerate(("rotor", "stator")):
        ax = axes[i]
        for param in ("hyst", "eddy"):
            ax.plot(
                results["time"][1:],
                results["coreLoss"][side][param],
                label=f"{side} - {param}",
            )
        ax.legend()
        ax.grid()
        ax.set_xlabel("Time in s")
    axes[0].set_ylabel("Core Loss in W")

.. code:: ipython3

    print(param_dict["getdp"]["res"])

.. code:: ipython3

    # Show core loss fields in gmsh GUI
    gmsh_api.finalize()
    gmsh_api.initialize()
    for side in ("rotor", "stator"):
        for param in ("core", "hyst", "eddy"):
            gmsh_api.merge(
                join(param_dict["getdp"]["res"], resId, f"p_{param}_from_b_{side}.pos")
            )
    gmsh_api.fltk.run()

.. code:: ipython3

    # Trigger frequency domain core loss
    from pyemmo.functions.core_loss import calc_freq_domain_core_loss

    freq_loss_dict = {}
    for i, side in enumerate(("rotor", "stator")):
        side_obj = getattr(pyemmo_script.machine, side)
        freq_loss_dict[side], freqs = calc_freq_domain_core_loss(
            b_filepath=join(param_dict["getdp"]["res"], resId, f"b_{side}.pos"),
            axial_length=side_obj.axial_length,
            loss_factor={
                "hyst": 102,
                "eddy": 1.5,
                "exc": 0,
            },
            sym_factor=8,
        )

.. code:: ipython3

    fig, axes = plt.subplots(2, 1)
    for i, side in enumerate(("rotor", "stator")):
        ax = axes[i]
        for param in ("hyst", "eddy"):
            ax.stem(
                freqs,
                freq_loss_dict[side][param],
                label=f"{side} - {param}",
                basefmt="none",
            )
        ax.legend()
        ax.set_ylabel("Core loss portion in W")
        ax.grid()
    ax.set_xlabel("Frequency in Hz")

    gmsh_api.fltk.run()

We can use ``matplotlib.pyplot`` to plot some time depended results:

.. code:: ipython3

    # Plot torque, flux and induced voltage results
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots()
    if isinstance(results["torque"], dict):
        ax.plot(results["time"], results["torque"]["rotor"], ".-")
    else:
        ax.plot(results["time"], results["torque"], ".-")

    ax.set_ylabel("Torque in Nm")
    ax.set_ylabel("Torque in Nm")
    ax.set_xlabel("Time in s")
    ax.grid()

    fig, ax = plt.subplots()
    ax.plot(results["time"], results["flux"]["d"], ".-", label="d-flux linkage")
    ax.plot(results["time"], results["flux"]["q"], ".-", label="q-flux linkage")
    ax.set_ylabel("Flux linkage in Wb")
    ax.set_xlabel("Time in s")
    ax.grid()
    ax.legend()

    fig, ax = plt.subplots()
    ax.plot(results["time"][1:], results["inducedVoltage"]["a"], ".-", label="Phase A")
    ax.plot(results["time"][1:], results["inducedVoltage"]["b"], ".-", label="Phase B")
    ax.plot(results["time"][1:], results["inducedVoltage"]["c"], ".-", label="Phase C")
    ax.set_ylabel("Induced Voltage in V")
    ax.set_xlabel("Time in s")
    ax.grid()
    ax.legend()
