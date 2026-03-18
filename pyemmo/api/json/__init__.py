#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
"""Global definitions for the pyemmo json interface.

Here part identifiers are defined to be used in the geometry interface or directly when
creating the :class:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface` objects as
for the values of :attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`
"""

from __future__ import annotations

import datetime

from ...script.geometry import defaultCenterPoint

globalCenterPoint = defaultCenterPoint

default_info_dict = {
    "winding": "auto",  # auto = try to create winding from number of slots and poles
    "Ntps": None,
    "z_pp": None,
    "Qs": None,
    "movingband_r": None,
    "axLen_S": None,
    "axLen_R": None,
    "symFactor": None,
    "magType": "",
    "magAngle": None,
    # Optional simulation parameters
    "modelName": f"model_{datetime.datetime.now().isoformat()}",
    "NpP": 1,
    "flag_openGUI": False,
    "rot_freq": 25,
    "startPos": 0,
    "endPos": 0,
    "nbrSteps": 1,
    "parkAngleOffset": None,
    "analysisType": 0,
    "tempMag": 20,
    "id": 0,
    "iq": 0,
    "calcIronLoss": False,
    "useFunctionMesh": False,
}

# Predefine IdExt of special surface api objects for identification
ROTOR_MAG_IDEXT = "magnet"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`) for magnets.
"""
ROTOR_BAR_IDEXT = "rotor bar"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for rotor bars of a squirel cage induction motor."""
ROTOR_SLOT_IDEXT = "rotor slot"
"""
Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for rotor slots of either a wound rotor induction motor or a electrical excitation
system.

NOTE: Not taken into account by API yet because rotor winding system not implemented!
"""
ROTOR_LAM_IDEXT = "rotor lamination"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for the rotor lamination."""
ROTOR_AIRGAP_IDEXT = "rotor airgap"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for the rotor airgap. The rotor airgap in pyemmo is defined as the most outer rotor
surface interfacing the movingband. See
:class:`~pyemmo.script.physicals.movingband.MovingBand` or
:mod:`~pyemmo.api.json.create_airgaps` for futher information."""
STATOR_SLOT_IDEXT = "stator slot"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for stator slot with winding."""
STATOR_LAM_IDEXT = "stator lamination"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for stator lamination."""
STATOR_AIRGAP_IDEXT = "stator airgap"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for stator airgap. The stator airgap in pyemmo is defined as the most inner stator
surface interfacing the movingband. See
:class:`~pyemmo.script.physicalsgeometry.movingband.MovingBand` or
:mod:`~pyemmo.api.json.create_airgaps` for futher information."""

# order defines user defined mesh setting order!
api_name_dict = {
    # rotor
    "shaft": "Shaft",
    "hole": "Holes",
    ROTOR_MAG_IDEXT: "Magnet",
    ROTOR_BAR_IDEXT: "Rotor Slot",
    ROTOR_LAM_IDEXT: "Rotor Lamination",
    ROTOR_AIRGAP_IDEXT: "Rotor Airgap",  # case 3 airgap segments
    "rotor air": "Rotor Air",
    # stator
    "housing": "Housing",
    STATOR_SLOT_IDEXT: "Stator Slot",
    STATOR_LAM_IDEXT: "Stator Lamination",
    STATOR_AIRGAP_IDEXT: "Stator Airgap",  # case 3 airgap segments
    "stator air": "Stator Air",  # case 5 airgap segments
}
"""
Dict to connect json api
:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id` to readable
name

:meta private:
"""
