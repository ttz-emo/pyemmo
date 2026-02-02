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
"""Global definitions for the pyemmo json interface.

Here part identifiers are defined to be used in the geometry interface or directly when
creating the :class:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface` objects as
for the values of :attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`
"""

from __future__ import annotations

from ...script.geometry import defaultCenterPoint
import datetime

# TODO: Clean up unused definitions here!

globalCenterPoint = defaultCenterPoint
# Movingband line Identification dicts
RotorMBLineDict = {
    "LuR2": [
        ["MB_CurveRotor"],
        ["LuA2", "LuM2"],
        ["LuAa", "LuBa"],
    ],  # double airgap
    "RoLu2": ["LuA2", "LuM2"],  # double airgap
    "RoLu": ["LuA", "LuM"],  # single airgap
    "LuR": ["LuAa", "LuBa"],  # single airgap
}
StatorMBLineDict = {
    "StLu2": [["MB_CurveStator"], ["LuA2", "LuM2"]],
    "StLu": ["LuA", "LuM"],
}

# Outer limit lines
OuterLimitLineDict = {
    "Geh": [  # first case: no inner shaft radius; second case: with radius
        ["OuterLimit"],
        ["G1", "G3"],  # first case: zylindrical housing
        [
            [
                "G1",
                "G2a",
            ],  # second case: quadratic or "kreuzprofil" with rounding
            ["G2a", "G2e"],
            ["G2e", "G3"],
            ["G2", "G1"],  # without rounding
            ["G2", "G3"],
        ],
    ],
    # if there is no housing, use stator iron outer line
    "StNut": [
        ["OuterLimit"],
        ["InnerLimit"],
        ["SZ", "SN"],
    ],
}

# Inner limit lines
InnerLimitLineDict = {
    "Wel": [
        ["InnerLimit"],
        # ["W2", "MP"], # first case: no inner shaft radius -> no limit line!
        ["W4", "W3"],  # second case: with radius -> inner limit line
    ],
    "Hul": ["H3", "H4"],
    "Pol": [
        ["InnerLimit"],
        ["OuterLimit"],
        ["RMi", "RI"],  # first case:IPM
        ["RndI", "RndM"],  # second case:APM
    ],
    "RoNut": ["SZ", "SN"],
}

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
"""NOTE: Not taken into account by API yet because rotor winding system not implemented!
Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for rotor slots of either a wound rotor induction motor or a electrical excitation
system."""
ROTOR_LAM_IDEXT = "rotor lamination"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for the rotor lamination."""
ROTOR_AIRGAP_IDEXT = "rotor airgap"
"""Literal part identifier
(:attr:`~pyemmo.api.machine_segment_surface.MachineSegmentSurface.part_id`)
for the rotor airgap. The rotor airgap in pyemmo is defined as the most outer rotor
surface interfacing the movingband. See
:class:`~pyemmo.script.geometry.movingBand.MovingBand` or
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
:class:`~pyemmo.script.geometry.movingBand.MovingBand` or
:mod:`~pyemmo.api.json.create_airgaps` for futher information."""

# order defines user defined mesh setting order.
apiNameDict = {
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
