"""Module for Class LimitLine"""
from typing import List, Union

from .physicalElement import CircleArc, Line, Material, PhysicalElement, Spline


class LimitLine(PhysicalElement):
    """Eine Instanz der Klasse LimitLine beschreibt jede beliebige Linie, die die Grenze des
    Systems der elektrischen Maschine definiert bspw. die Außenkante vom Stator.
    Beim Verwenden vom Baukasten werden die Grenzlinien automatisch definiert.
    \\image html outerLimit.png
    """

    def __init__(
        self,
        name: str,
        geometricalElement: List[Union[Line, CircleArc, Spline]],
        material: Material = None,
    ):
        """Create a boundary line

        Args:
            name (str): Name of boundary line. E.g. "OuterLimitLine"
            geometricalElement (List[Union[Line, CircleArc, Spline]]): List of geo curves
            material (Material, optional): Material of boundary. Defaults to None.
        """
        PhysicalElement.__init__(
            self, name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self._physicalElementType = "LimitLine"
