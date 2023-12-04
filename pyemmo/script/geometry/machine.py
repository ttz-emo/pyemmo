from ..script import Script
from .domain import Domain
from .rotor import Rotor
from .stator import Stator


class Machine:
    """
    The class machine describes the geometry of a electrical machine.
    It consists of a rotor and a stator object, which both have PhysicalElements describing their properties.
    """

    def __init__(
        self,
        name: str = "machine",
        rotor: Rotor = None,
        stator: Stator = None,
    ):
        """
        Constructor of the class Machine

        Args:
            rotor:  Rotor
            stator: Stator

        Returns:
            None

        Raises:
            Nothing
        """
        ###Name des Objektes.
        self._name: str = name
        ###Objekt der Klasse Rotor.
        self._rotor: Rotor = rotor
        ###Objekt der Klasse Stator.
        self._stator: Stator = stator
        
    @property
    def name(self) -> str:
        """name gibt den Namen der elektrischen Maschine als Stringvariable zurück."""
        return self._name
    
    @name.setter
    def name(self, newName: str):
        """Mit name kann man den Namen der Maschine ändern."""
        self._name = newName


