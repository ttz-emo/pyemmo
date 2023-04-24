"""Module for primary boundary Line"""
from typing import List
from .transformable import Transformable
from .physicalElement import PhysicalElement, Material


class PrimaryLine(PhysicalElement):
    """
    Eine Instanz der Klasse MasterLine beschreibt die Masterkante eines Teilmodells einer zu
    simulierenden elektischen Maschine.\n
        \\image html masterLine.png
    """

    def __init__(
        self,
        name: str,
        geometricalElement: List[Transformable],
        material: Material = None,
    ):
        """init of PrimaryLine boundary PhysicalElement

        Args:
            name (str)
            geometricalElement (List[Transformable])
            material (Material, optional): Defaults to None.
        """
        # FIXME: Material hat keinen Einfluss... Sollte standardmaeßig auf None gesetzt werden
        super().__init__(
            name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self._physicalElementType = "PrimaryLine"
