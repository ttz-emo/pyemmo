from typing import List

from pyemmo.script.material.material import Material
from .surface import Surface
from .physicalElement import PhysicalElement
from .. import colorDict
import math

###
# Eine Instanz der RotorLamination ist das Blechpaket des Rotors. Eine beliebige Geometrie kann mit der Klasse RotorLamination definiert werden.
# Diese Klasse sollte nur im Expertenmodus angewandt werden.
# Dies kann beispielsweise beim Import und Weiterverarbeitung von Step-Dateien geschehen.
# Eine einfachere Anwendung bietet der Maschinenbaukasten von pyemmo.
# \image html RotorBlech.png
###


class RotorLamination(PhysicalElement):
    ###
    # Konstruktor der Klasse RotorLamination.
    #
    #   Input:
    #
    #       machineDict : dict
    #       geometricalElement : list
    #       material : Material
    #
    ###
    def __init__(
        self,
        name: str,
        geometricalElement: List[Surface],
        material: Material,
        phyID: int = None,
    ):
        PhysicalElement.__init__(
            self,
            name=name,
            material=material,
            geometricalElement=geometricalElement,
            phyID=phyID,
        )

        self._physicalElementType = "RotorLamination"  # the physical element type can be used to identify physical elements
        self.setColor("SteelBlue")
