from typing import List, Union

from ..material.material import Material
from .circleArc import CircleArc
from .line import Line
from .spline import Spline
from .physicalElement import PhysicalElement

###
# TODO: Rename SLAVE -> LINKED/LINK
# Eine Instanz der Klasse SlaveLine beschreibt die Slavekante eines Teilmodells einer zu simulierenden elektischen Maschine.
# \image html slaveLine.png
###
class SlaveLine(PhysicalElement):
    ###
    # Konstruktor der Klasse SlaveLine.
    #
    #   Attribute:
    #
    #       ID : Integer
    #       name : String
    #       material : Material
    #       geometricalElement : [Line]
    #
    ###
    def __init__(
        self,
        name: str,
        geometricalElement: List[Union[Line, CircleArc, Spline]],
        material: Material = None,
    ):
        PhysicalElement.__init__(
            self, name=name, material=material, geometricalElement=geometricalElement
        )

        self.physicalElementType = "SlaveLine"  # the physical element type can be used to identify physical elements
