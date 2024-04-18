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
"""init of geometry package"""

from .point import Point
from .. import (
    DOMAIN_PRIMARY,
    DOMAIN_SECONDARY,
    DOMAIN_LIMIT,
    DOMAIN_MOVINGBAND,
    DOMAIN_MOVINGBAND_AUX,
    DOMAIN_AIRGAP,
    DOMAIN_ROTOR,
    DOMAIN_STRANDED,
    DOMAIN_MAGNET,
    DOMAIN_LAMINATION,
    DOMAIN_BAR,
    DOMAIN_CONDUCTING,
    DOMAIN_NON_CONDUCTING,
    DOMAIN,
    DOMAIN_NON_LINEAR,
    DOMAIN_LINEAR,
)

default_domain_dict = {
    DOMAIN_PRIMARY: [],
    DOMAIN_SECONDARY: [],
    DOMAIN_LIMIT: [],
    DOMAIN_MOVINGBAND: [],
    DOMAIN_MOVINGBAND_AUX: [],
    DOMAIN_AIRGAP: [],
    DOMAIN_ROTOR: [],
    DOMAIN_STRANDED: [],
    DOMAIN_MAGNET: [],
    DOMAIN_LAMINATION: [],
    DOMAIN_BAR: [],
    DOMAIN_CONDUCTING: [],
    DOMAIN_NON_CONDUCTING: [],
    DOMAIN: [],
    DOMAIN_NON_LINEAR: [],
    DOMAIN_LINEAR: [],
}
# Translate PyEMMO Domain names to GetDP-Template Domain names
# domainDict = {
#     # domain key: domain name
#     "DomainS": "DomainS",  # domains with imposed current (js[] defined) = PhaseA + PhaseB + PhaseC
#     "DomainM": "DomainM",  # magnet domains, surfaces with Br[] defined
#     "DomainC": "DomainC",  # electrically conducting domains
#     "Domain": "Domain",  # whole domain
#     "DomainL": "DomainL",  # linear material
#     "DomainNL": "DomainNL",  # non linear material
#     #### Stator domains ####
#     "MB_Stator": "Stator_Bnd_MB",  # all moving band lines of stator
#     "Stator_Airgap": "Stator_Airgap",  # for maxwell stress tensor torque
#     "OuterLimitLine": "Surf_Inf",
#     #### Rotor domains ####
#     "DomainC_Rotor": "RotorC",  # conducting on rotor
#     "DomainCC_Rotor": "RotorCC",  # non conducting
#     # "Rotor_Moving": "Rotor_Moving", # grouping all domains rotating in simulation;
#     # -> Done by machine file
#     "Rotor_Airgap": "Rotor_Airgap",  # for maxwell stress tensor torque
#     "DomainM_Rotor": "Rotor_Magnets",  # magnet domains, surfaces with Br[] defined
#     "MB_Rotor": "Rotor_Bnd_MB",  # all moving band lines of rotor
#     "Rotor_Bnd_MBaux": "Rotor_Bnd_MBaux",  # outer rotor movingband line(s) rotor
#     "primaryRegion_Rotor": "Surf_cutA0",
#     "SlaveRegion_Rotor": "Surf_cutA1",
#     "InnerLimitLine": "Surf_bn0",
# }

physicalsDict = {"Rotor_MB_Line": "Rotor_Bnd_MB"}

defaultCenterPoint = Point("default center point", 0.0, 0.0, 0.0, 1)
