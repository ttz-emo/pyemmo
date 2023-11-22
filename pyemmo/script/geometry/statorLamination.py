from typing import List
from pyemmo.script.material.material import Material
from .surface import Surface
from .physicalElement import PhysicalElement
from .. import colorDict
import math

###
# Eine Instanz der StatorLamination ist das Blechpaket des Stators. Eine beliebige Geometrie kann mit der Klasse StatorLamination definiert werden.
# Diese Klasse sollte man nur im Expertenmodus verwenden.
# Dies kann beispielsweise beim Import und Weiterverarbeitung von Step-Dateien geschehen.
# Eine einfachere Anwendung bietet der Maschinenbaukasten von pyemmo.
# \image html statorBlech.png
###
class StatorLamination(PhysicalElement):

    ###
    # Konstruktor der Klasse StatorLamination.
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
        phyID=None,
    ):
        PhysicalElement.__init__(
            self,
            name=name,
            geometricalElement=geometricalElement,
            material=material,
            phyID=phyID,
        )
        self.physicalElementType = "Lamination"  # the physical element type can be used to identify physical elements

        self.setColor("SteelBlue4")
