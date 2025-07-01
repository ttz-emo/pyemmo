#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Module for abstract class Transformable"""
# import abstrac base class (abc)
from abc import ABC, abstractmethod


class Transformable(ABC):
    """Abstract class Transformable for geometry entities.
    Das Interface Transformable dient als abstrakte Klasse für alle geometrischen
    Elemente und beinhaltet somit ausschließlich abstrakte Methoden.

    Args:
        abc (_type_): _description_
    """

    ###Gibt den Namen einer Transformable zurück.
    @property
    def name(self):
        """Entity name"""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise TypeError("Name must be a string.")

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
