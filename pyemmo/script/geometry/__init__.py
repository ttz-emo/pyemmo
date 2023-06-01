"""init of geometry package"""
from .point import Point

domainDict = {
    # domain key: domain name
    "DomainS": "DomainS",  # domains with imposed current (js[] defined) = PhaseA + PhaseB + PhaseC
    "DomainM": "DomainM",  # magnet domains, surfaces with Br[] defined
    "DomainC": "DomainC",  # electrically conducting domains
    "Domain": "Domain",  # whole domain
    "DomainL": "DomainL",  # linear material
    "DomainNL": "DomainNL",  # non linear material
    #### Stator domains ####
    "MB_Stator": "Stator_Bnd_MB",  # all moving band lines of stator
    "Stator_Airgap": "Stator_Airgap",  # for maxwell stress tensor torque
    "OuterLimitLine": "Surf_Inf",
    #### Rotor domains ####
    "DomainC_Rotor": "RotorC",  # conducting on rotor
    "DomainCC_Rotor": "RotorCC",  # non conducting
    # "Rotor_Moving": "Rotor_Moving", # grouping all domains rotating in simulation;
    # -> Done by machine file
    "Rotor_Airgap": "Rotor_Airgap",  # for maxwell stress tensor torque
    "DomainM_Rotor": "Rotor_Magnets",  # magnet domains, surfaces with Br[] defined
    "MB_Rotor": "Rotor_Bnd_MB",  # all moving band lines of rotor
    "Rotor_Bnd_MBaux": "Rotor_Bnd_MBaux",  # outer rotor movingband line(s) rotor
    "primaryRegion_Rotor": "Surf_cutA0",
    "SlaveRegion_Rotor": "Surf_cutA1",
    "InnerLimitLine": "Surf_bn0",
}

physicalsDict = {"Rotor_MB_Line": "Rotor_Bnd_MB"}

defaultCenterPoint = Point("default center point", 0.0, 0.0, 0.0, 1)
