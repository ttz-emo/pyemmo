"""Module for Class Domain"""
from typing import List, Union, TYPE_CHECKING
from pyemmo.script.geometry.physicalElement import PhysicalElement

if TYPE_CHECKING:
    from ..script import Script
# pylint: disable=locally-disabled, line-too-long


class Domain:
    """Eine Instanz der Klasse Domain ist die Gruppierung von PhysicalElement-Objekten.

    Input:
        name : string
        physicalElement : [PhysicalElement]

    Beispiel:
        Diese Magnetdomaine (siehe Bild) besteht aus 2 PhysicalElements-Objekten und 4
        Surface-Objekten.

        \\image html domain_Magnet.png
    """

    def __init__(
        self, name: str, physicalElements: Union[List[PhysicalElement], PhysicalElement]
    ):
        self.name = name
        self.physicals = physicalElements

    @property
    def name(self) -> str:
        """getter of domain Name

        Returns:
            str: Domain name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """setter of domain name

        Args:
            name (str): New domain name
        """
        self._name = name

    @property
    def physicals(self) -> List[PhysicalElement]:
        """List of physical surfaces/lines (PhysicalElement objects) belonging to
        the domain.

        Returns:
            List[PhysicalElement]: List of physical surfaces/lines
        """
        return self._physicals

    @physicals.setter
    def physicals(
        self, physicalElements: Union[PhysicalElement, List[PhysicalElement]]
    ):
        """setter of physical element list

        Args:
            physicalElements (PhysicalElement | List[PhysicalElement]): New physicals

        Raises:
            TypeError: If physicalElements not is list
        """
        if isinstance(physicalElements, list):
            if all(
                isinstance(physElem, PhysicalElement) for physElem in physicalElements
            ):
                self._physicals = physicalElements
                return None
        if isinstance(physicalElements, PhysicalElement):
            self._physicals = [physicalElements]
            return None
        raise TypeError(
            f"Should be List[PhysicalElement] or PhysicalElement but is: {type(physicalElements)}"
        )

    def addPhysicalElements(self, physicalElementList: List[PhysicalElement]):
        """append PhysicalElements to the domain"""
        if isinstance(physicalElementList, list):
            self.physicals.extend(physicalElementList)
        else:
            raise ValueError("Argument 'physicalElementList' was not type list!")

    ###
    # Mit addToScript wird die Domain zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    #   Beispiel:
    #
    #       myScript = Script(...)
    #       Domain1.addToScript(myScript)
    #
    ###
    def addToScript(self, script: "Script"):
        """call script._addDomain().
        Function is for development and testing reasons.

        Args:
            script (Script): Skript to add the Domain to.
        """
        script._addDomain(self)
