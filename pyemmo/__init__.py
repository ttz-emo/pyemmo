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
"""Init of pyemmo package. Overloads the function calc_phaseangle_starvoltageV2
of site-package swat-em, because there is a mistake in the original implementation."""
import os
import platform
from os.path import isdir
from typing import List, Literal
import logging
import datetime
from swat_em import analyse
import numpy as np

# import debugpy
# debugpy.debug_this_thread()

PACKAGE_NAME = "pyemmo"
# User folder (to store machine/materials/config)
if platform.system() == "Windows":
    USER_DIR = os.path.join(os.environ["APPDATA"], PACKAGE_NAME)
    USER_DIR = USER_DIR.replace("\\", "/")
else:
    USER_DIR = os.environ["HOME"] + "/.local/share/" + PACKAGE_NAME

# generate user dir if not exists
if not isdir(USER_DIR):
    os.makedirs(USER_DIR)

# init root logger:
# global logging format
logFmt = logging.Formatter("%(levelname)-7s: %(message)s")
globalLogFileHandler = logging.FileHandler(
    filename=os.path.join(USER_DIR, "pyemmo.log"), encoding="utf-8"
)
globalLogFileHandler.setFormatter(logFmt)
rootLogger = logging.getLogger()
rootLogger.addHandler(globalLogFileHandler)
# logging.basicConfig()
logging.info(
    "PyEMMO started on %s %s",
    datetime.date.today(),
    datetime.datetime.now().strftime("%H:%M:%S"),
)


def calcPhaseangleStarvoltageCorr(volVecList):
    """
    Calculates the phaseangle based on the slot voltage vectors. (corrected version)

    Parameters
    ----------
    volVecList :    list of lists of lists
                    voltage vectors for every phase and every slot
                    Ei[nu][phase][slot]

    Returns
    -------
    return phaseangle: list
                       phaseangle for every harmonic number and every
                       phase; phaseangle[nu][phase]
    return seqeunce:   list
                       sequence of the flux wave: 1 or -1
    """
    sequence: List[Literal[-1, 1]] = []
    phaseangle: List[List[float]] = []
    for knu in volVecList:  # for every nu
        phaseangle.append([])
        km_sum = [sum(km) for km in knu]  # get the sum phasor for every phase
        # calculate the phasor angle for every phase:
        phasor_angle = [np.angle(kPhase) * 180 / np.pi for kPhase in km_sum]
        if len(phasor_angle) > 1:
            # if phasor of w(=kmSum[2]) nearly equals phasor of u shifted by 120deg
            # (=kmSum[0]*np.exp(1j*2*np.pi/3); mathematically positive), then
            # the phase order is inverted (uwv instead of uvw) and the rotation direction
            # is clockwise.
            if (
                np.abs(km_sum[2] - km_sum[0] * np.exp(1j * 2 * np.pi / 3))
                < 1e-9
            ):
                sequence.append(-1)  # math. negative
            else:
                # otherwise its counter clockwise
                sequence.append(1)  # math. positive
        else:
            sequence.append(0)
        for angle in phasor_angle:
            while angle < 0:
                angle += 360.0
            phaseangle[-1].append(angle)
    return phaseangle, sequence


# Overload bug in swat_em.analyse package
analyse.calc_phaseangle_starvoltage = calcPhaseangleStarvoltageCorr
