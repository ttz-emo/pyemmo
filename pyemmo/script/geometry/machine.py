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
