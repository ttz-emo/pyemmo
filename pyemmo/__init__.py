#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
"""
**Global pyemmo package contents**

- Overloads the function ``calc_phaseangle_starvoltage`` of site-package SWAT-EM, because
  there is a mistake in the original implementation.
- Defines global directories and logging specifications
- Updates the swat-em configuration: ``swat_em.config.config["num_MMF_points"] = 36000``
  to improve MMF accuracy.
- Sets the matplotlib font_manager log level to supress debug messages by
  ``logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)``
"""
from __future__ import annotations

import datetime
import logging
import os
import platform
from os.path import isdir
from typing import Literal

import numpy as np
from swat_em import analyse
from swat_em import config as swatem_config

from .version import __version__

# import debugpy
# debugpy.debug_this_thread()

PACKAGE_NAME = "pyemmo"
# User folder (to store machine/materials/config)
if platform.system() == "Windows":
    USER_DIR = os.path.join(os.environ["APPDATA"], PACKAGE_NAME)
    """System depended pyemmo user directory to store material data and default model
    results.
    For Windows this is ``%APPDATA%/pyemmo``. For ever other systems its
    ``%HOME%/.local/share/pyemmo``

    :meta hide-value:
    """
    USER_DIR = USER_DIR.replace("\\", "/")
else:
    USER_DIR = os.environ["HOME"] + "/.local/share/" + PACKAGE_NAME

# generate user dir if not exists
if not isdir(USER_DIR):
    os.makedirs(USER_DIR)

LOG_FORMAT = f"%(levelname)s - %(name)s - %(message)s"  # pylint: disable=W1309

# init pyemmo package logger
# NOTE: By creating a top-level package logger and adding a StreamHandler to it, we dont
# need to configure the root logger (logging.getLogger()).
# TODO: What to do if root logger allready initialized? Check for StreamHandler in root
# logger? How to handle logging in __main__ files in that case?

pyemmo_package_logger = logging.getLogger("pyemmo")
"""PyEMMO package logger. The default log level is set to ``logging.INFO``.

.. note:: Do not import this from pyemmo but access it by ``logging.getLogger("pyemmo")``.
"""

# set default pyemmo log level to info
pyemmo_package_logger.setLevel(logging.INFO)

# create global logging format:
# INITIALIZE LOGGING
log_formatter = logging.Formatter(LOG_FORMAT)
"""
Global pyemmo log formattern using logging format:

    :code:`"%(levelname)s - %(name)s - %(message)s"`
"""

# create console handler and use format
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# create global log file handler with format
# TODO: Replace simple file handler with rolling file handler
global_log_filehandler = logging.FileHandler(
    filename=os.path.join(USER_DIR, "pyemmo.log"), encoding="utf-8"
)
"""Global log file handler to file "pyemmo.log" in folder ``USER_DIR`` with default
level INFO

:meta hide-value:
"""
global_log_filehandler.setFormatter(log_formatter)  # set format
# set level of !file handler! to info, no need to log debug info in global log file:
global_log_filehandler.setLevel(logging.INFO)

# add handlers to package logger:
pyemmo_package_logger.addHandler(global_log_filehandler)
pyemmo_package_logger.addHandler(console_handler)

pyemmo_package_logger.info(
    "PyEMMO started on %s %s",
    datetime.date.today(),
    datetime.datetime.now().strftime("%H:%M:%S"),
)
# Update matplotlib logging level in case debugging because creates a lot of debugging
# outputs...
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)

# check if pyleecan is available
try_pyleecan = True  # set this to False to never use pyleecan
use_pyleecan = False
if try_pyleecan:
    try:
        import pyleecan

        use_pyleecan = True
    except ImportError:
        use_pyleecan = False
    except Exception as exce:
        raise exce

# set the number of datapoints in the MMF calculation in SWAT-EM so offset angle
# calculation is done correctly
swatem_config.config["num_MMF_points"] = 36000


def calc_phaseangle_starvoltage(volVecList):
    """
    .. note:: Reworked copy of ``swat_em.analyse.calc_phaseangle_starvoltage()``!
        This overloads the original function for PyEMMO, since the SWAT-EM project has
        not been updated on PyPi. See
        `SWAT-EM Merge Request <https://gitlab.com/martinbaun/swat-em/-/merge_requests/11>`_
        for all details.

    Calculates the phaseangle based on the slot voltage vectors. (corrected version)

    Args:
        volVecList (list[list[list[numpy.complex]]]): voltage vectors for every phase and every slot
            [nu][phase][slot]

    Returns:
        tuple[list, list]:
        - Phase angles for every harmonic number and phase: ``phaseangle[nu][phase]``
        - Sequence of the flux wave: 1 or -1
    """
    sequence: list[Literal[-1, 1]] = []
    phaseangle: list[list[float]] = []
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
            if np.abs(km_sum[2] - km_sum[0] * np.exp(1j * 2 * np.pi / 3)) < 1e-9:
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
analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltage
