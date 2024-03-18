"""Module for Bar Physical Element"""

from typing import List, Union
from .physicalElement import PhysicalElement, Material, Surface


class Bar(PhysicalElement):
    """
    TODO
    """

    def __init__(
        self,
        name: str,
        geometricalElement: Union[Surface, List[Surface]],
        material: Material,
    ):
        """Bar defines a rotor bar for a induction machine

        Args:
            - name (str): Bar name
            - geometricalElement (Union[Surface, List[Surface]]):
                List of geometry objects
            - material (Material): Material of . Should be "air". Defaults to None.
        """
        # convert Surface to list of Surface for PhysicalElement init
        if isinstance(geometricalElement, Surface):
            geometricalElement = [geometricalElement]
        # make sure conductivity is defined for induced currents
        assert (
            material.conductivity > 0
        ), f"Material of Bar ({name}) must be elec. conducting!"
        super().__init__(
            name=name, material=material, geometricalElement=geometricalElement
        )
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "Bar"
        self.setColor("Orange")
