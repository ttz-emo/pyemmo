#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""Test module for spmsm toolkit machine model"""
# %%
# import os
# from os import mkdir, path
from collections import defaultdict

from pyemmo.functions.import_results import plot_all_dat

# from numpy import rad2deg, where
import math
from swat_em import datamodel

# from pyemmo.definitions import RESULT_DIR, MAIN_DIR
from pyemmo.script.geometry.point import Point

# from pyemmo.script.geometry.line import Line
from pyemmo.script.material.electricalSteel import Material, ElectricalSteel
from pyemmo.script.geometry.machineSPMSM import MachineSPMSM, RotorSPMSM, StatorPMSM
from pyemmo.script.script import Script
from pyemmo.functions.runOnelab import createCmdCommand
from pyemmo.definitions import ROOT_DIR

# %%


def SPMSM_test(test_params: dict) -> tuple[MachineSPMSM, RotorSPMSM, StatorPMSM]:
    """
    Function to prepare motor for testing.
    Accepts dictionary of test params, return a SPMSM motor, rotor, and stator objects ready for running test.
    Test params should contain the following:
    - Materials (dict of laminMat, magMat, , wireMat, airMat)
    - Slots no.
    - Poles no.
    - Magnet type (1, 2, 3)
    - Air gap size
    - windings (dict of count, layers, turns)
    - Slot type

    """
    # PBohrung = test_params["PBohrung"]

    # # Material aus Datenbank laden
    # steel_1010 = test_params["mats"]["laminMat"]
    # ndFe35 = test_params["mats"]["magMat"]
    # # ndFe35.setRemanence(0.01) # switch "off" remanence
    # air = test_params["mats"]["airMat"]
    # copper = test_params["mats"]["wireMat"]

    nbrSlots = test_params["slotCount"]
    nbrPoles = test_params["poleCount"]
    nbrPolePairs = nbrPoles / 2
    drehzahl = test_params["revols"]
    fel = drehzahl / 60 * nbrPolePairs
    simuSPMSMDict = {
        "analysisParameter": {
            # "freq": drehzahl / 60,
            "symmetryFactor": test_params["simuParams"]["symmetryFactor"],
            "nbrPolesTotal": nbrPoles,
            "nbrSlotTotal": nbrSlots,
            # "timeMax": 1
            # / 67,  # Winkel/wr 2*math.pi / (2 * math.pi * 67) = 1/67 für ganzen mech. Winkel mit f = 67 Hz
            # "timeStep": 1
            # / (
            #     180 * 67 * 2
            # ),  # Ein Grad pro Step -> math.pi/180/(2*math.pi*67) = 1/(180*2*67)
            # "analysisType": "timedomain",  #'timedomain', #'static'
            "startPosition": test_params["simuParams"]["startPosition"],
        },
        # "output": {"b": True, "az": True, "js": True},
    }

    # %% Maschine aus dem Baukasten parametrisieren
    SPMSM = MachineSPMSM(simuSPMSMDict)
    rotor = SPMSM.addRotorToMachine("sheet01_standard", test_params["magnet"]["id"])
    rotor.addLaminationParameter(test_params["magnet"]["laminationParams"])
    rotor.addMagnetParameter(test_params["magnet"]["magnetParams"])
    rotor.addAirGapParameter({"width": test_params["airGapWidth"], "material":test_params["mats"]["airMat"]})
    rotor.createRotor()
    # rotor.plot()
    # %%


    winding = datamodel()
    winding.genwdg(Q=nbrSlots, P=nbrPoles, 
                   m= test_params["windingParams"]["m"], 
                   layers= test_params["windingParams"]["layers"], 
                   turns= test_params["windingParams"]["turns"])
    
    stator = SPMSM.addStatorToMachine("sheet01_standard", test_params["slot"]["id"], winding)
    stator.addLaminationParameter(test_params["slot"]["laminationParams"])
    stator.addSlotParameter(test_params["slot"]["slotParams"])
    stator.addAirGapParameter({"width": test_params["airGapWidth"], "material":test_params["mats"]["airMat"]})

    stator.createStator()
    # stator.plot()
    # %% Create Machine
    SPMSM.createMachineDomains()
    SPMSM.setFunctionMesh("linear", 8)
    # SPMSM.plot()

    return SPMSM, rotor, stator
