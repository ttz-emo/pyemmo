"""Module for AirArea Physical Element"""
from typing import List, Union
from .physicalElement import PhysicalElement, Material, Surface, Line, CircleArc, Spline


class AirArea(PhysicalElement):
    """
    Eine Instanz der Klasse AirArea beschreibt jeden beliebigen Luftraum innerhalb der
    elektrischen Maschine im dreidimensionalen Raum. Für den Luftspalt existiert eine eigene
    Klasse AirGap. Diese Klasse ist eine abgeleitete Klasse der Basisklasse PhysicalElement.
    Beim Verwenden vom Baukasten muss der Luftspalt vom Nutzer nicht manuell definiert werden.
    Die Ergänzung vom Luftraum muss bei der Erstellung vom Rotor bzw. Stator automatisch erfolgen
    (siehe RotorSPMSM.py).
        \\image html class_airArea.png
    """

    ###
    # Konstruktor der Klasse AirArea.
    #
    #   Attribute:
    #
    #       ID : Integer
    #       name : String
    #       material : Material
    #       geometricalElement : [Surface]
    #
    ###
    def __init__(
        self,
        name: str,
        geometricalElement: List[Surface],
        material: Material = None,
    ):
        """AirArea is any area defined with material air except from the Airgap surface

        Args:
            - name (str): Domain name
            - geometricalElement (List[Union[Surface, Line, CircleArc, Spline]):
            List of geometry objects
            - material (Material, optional): Material of AirArea. Should be "air". Defaults to None.
        """
        PhysicalElement.__init__(
            self, name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "AirArea"
        self.setColor("SkyBlue")
