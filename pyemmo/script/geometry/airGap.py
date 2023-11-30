"""Module for AirArea Physical Element"""
from typing import List, Union
from .physicalElement import PhysicalElement, Material, Surface, Line, CircleArc, Spline


class AirGap(PhysicalElement):
    """Eine Instanz der AirGap ist ein Teil des Luftspalts einer elektrischen Maschine im
    dreidimensionalen Raum. Diese Klasse beschreibt sowohl den Luftraum auf der Rotor sowie auf
    der Stator-Seite.
        \\image html class_airGap.png
    Beim Verwenden vom Baukasten muss der Luftspalt vom Nutzer nicht manuell definiert werden.
    Die Ergänzung vom Luftraum muss bei der Erstellung vom Rotor bzw. Stator automatisch erfolgen
    (siehe RotorSPMSM.py).

    """

    def __init__(
        self,
        name: str,
        geometricalElement: List[Union[Surface, Line, CircleArc, Spline]],
        material: Material = None,
    ):
        """AirGap

        Args:
            name (str): Physical Element Name
            geometricalElement (List[Union[Surface, Line, CircleArc, Spline]]):
            List of geo elements
            material (Material, optional): Material of airgap. Defaults to None.
        """
        PhysicalElement.__init__(
            self, name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirGap"
        self.setColor("SkyBlue")
