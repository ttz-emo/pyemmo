"""Module for abstract class Transformable"""
# import abstrac base class (abc)
from abc import ABC, abstractclassmethod, abstractproperty, abstractmethod


class Transformable(ABC):
    """Abstract class Transformable for geometry entities.
    Das Interface Transformable dient als abstrakte Klasse für alle geometrischen
    Elemente und beinhaltet somit ausschließlich abstrakte Methoden.

    Args:
        abc (_type_): _description_
    """

    ###Mit getNewID() wird eine neue eindeutige ID für jede Transformable erzeugt.
    @classmethod
    @abstractclassmethod
    def _getNewID(cls):
        pass

    # pylint: disable=locally-disabled, invalid-name
    @property
    @abstractproperty
    def id(self) -> int:
        """Property id of geo classes"""

    @id.setter
    @abstractmethod
    def id(self, newID) -> None:
        """Setter for ID"""

    ###Gibt den Namen einer Transformable zurück.
    @property
    @abstractproperty
    def name(self):
        """Entity name"""

    ###Überschreibt den aktuellen Namen mit einem neuen Namen.
    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        pass

    ###translate() verschiebt Transformables um die Faktoren dx, dy und dz.
    @abstractmethod
    def translate(self, dx, dy, dz):
        pass

    ###rotateZ() rotiert Tansformables um einen Rotationspunkt und die Z-Achse.
    @abstractmethod
    def rotateZ(self, rotationPoint, angle):
        pass

    ###rotateX() rotiert Tansformables um einen Rotationspunkt und die X-Achse.
    @abstractmethod
    def rotateX(self, rotationPoint, angle):
        pass

    ###rotateY() rotiert Tansformables um einen Rotationspunkt und die Y-Achse.
    @abstractmethod
    def rotateY(self, rotationPoint, angle):
        pass

    ###duplicate() erzeugt ein Duplikat des Objektes.
    @abstractmethod
    def duplicate(self):
        pass

    ###mirror() erzeugt ein Duplikat und spiegelt diesen an einer definierten Ebene.
    @abstractmethod
    def mirror(self, planePoint, planeVector1, planeVector2):
        pass

    # ###Mit addToScript() wird ein Objekt im Skript in Gmsh Syntax erzeugt.
    # @classmethod
    # @abstractmethod
    # def addToScript(self, script):
    #     pass

    # ###Gibt die ID des Objektes zurück.
    # @abstractmethod
    # def getID(self):
    #     pass

    # ###Überschreibt die existierende ID mit einer neuen ID.
    # @abstractmethod
    # def _setID(self, newID):
    #     pass
