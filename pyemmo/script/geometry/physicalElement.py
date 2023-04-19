"""Module for class PhysicalElement"""
from random import random
from typing import List, Union, TYPE_CHECKING

from .. import colorDict
from ..material.material import Material
from .circleArc import CircleArc
from .line import Line
from .spline import Spline
from .surface import Surface

if TYPE_CHECKING:
    from ..script import Script


class PhysicalElement:
    """
    Eine Instanz der Klasse PhysicalElement ist die Gruppierung von Flächen/Linien im
    dreidimensionalen Raum.\n
    Input:
        name : string
        geometricalElement : [Line] oder [Surface]
        material : Material

    Beispiel:
        from pydraft import *\n
        P1 = Point('P1', 0, 0, 0, 1)\n
        P2 = Point('P2', 1, 0, 0, 1)\n
        P3 = Point('P3', 1, 1, 0, 1)\n
        P4 = Point('P4', 0, 1, 0, 1)\n
        L1 = Line('L1', P1, P2)\n
        L2 = Line('L2', P2, P3)\n
        L3 = Line('L3', P3, P4)\n
        L4 = Line('L4', P4, P1)\n
        S1 = Surface('S1', [L1, L3, L2, L4])\n
        Blech1 = PhysicalElement('Blech1', [S1], steel1010)\n
    """

    # Statische Variable zur ID-Verwaltung
    Physical_ID: int = 1000

    def __init__(
        self,
        name: str,
        geometricalElement: List[Union[Surface, Line, CircleArc, Spline]],
        material: Material = None,
        phyID: int = None,
    ):
        # the physical element type can be used to identify physical elements
        self._physicalElementType = "PhysicalElement"

        self._name = name
        self.geometricalElement = geometricalElement
        self._material = material
        if phyID is None:
            # pylint: disable=locally-disabled, invalid-name
            self.id = self._getNewID()
        else:
            self.id = phyID

    def _getNewID(self):
        """Wird eine Instanz erzeugt, bekommt sie automatisch eine eindeutige ID zugewiesen.
        Mit getNewID() wird eine neue ID erzeugt."""
        PhysicalElement.Physical_ID = PhysicalElement.Physical_ID + 1
        return PhysicalElement.Physical_ID

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """PhysicalElement ID"""
        return self._id

    @id.setter
    def id(self, newID: int):
        """setter of PhysicalElement ID

        Args:
            newID (int): new ID
        """
        if not isinstance(newID, int):
            raise TypeError(f"PhysicalElement ID must be positive integer! {newID}")
        if 1000 < newID < PhysicalElement.Physical_ID:
            raise ValueError(
                "New ID of PhysicalElement is smaller than global ID count."
                "Given newID must be existing!"
            )
        PhysicalElement.Physical_ID = newID  # set global ID to not overcount newID
        self._id = newID

    @property
    def geometricalElement(self) -> Union[List[Surface], List[Line]]:
        """geometricalElement sind alle geometrischen Elemente einer Klasse.

        Input:

            None

        Output:

            [Surface] oder [Line]
        """
        return self._geometricalElement

    @geometricalElement.setter
    def geometricalElement(self, geometricalElement: Union[List[Surface], List[Line]]):
        """setter of geo elements"""
        self._geometricalElement = geometricalElement
        # run element type funtion to ensure there are not lines AND surfaces
        self.getGeoElementType()

    def getMaterial(self) -> Material:
        """getter of Material"""
        return self._material

    def setMaterial(self, material: Material):
        """setter of Material"""
        self._material = material

    def getName(self):
        """getter of name"""
        return self._name

    def setName(self, name):
        """setter of name"""
        self._name = name

    def getType(self) -> str:
        """The function getType of PhysicalElement returns a string with the PhysicalElement-Type"""
        return self._physicalElementType

    def getGeoElementType(self) -> Union[Line, Surface, None]:
        """get type of geometry elements.

        Raises:
            ValueError: If geometry element type is neither line nor surface.
            ValueError: If lines AND surface elements in geo element list.
            Exception: If element type could not be evaluated.

        Returns:
            Union[Line, Surface, None]: Type of geometric elements in geo list.
        """
        if len(self.geometricalElement) == 0:
            # if list is empty return None
            return None
        # Otherwise determine geometry type:
        isSurface = False
        isLine = False
        for GeoElement in self.geometricalElement:
            if isinstance(GeoElement, Surface):
                isSurface = True
            elif isinstance(GeoElement, (Line, CircleArc, Spline)):
                isLine = True
            else:
                raise ValueError(
                    (
                        f"Geometrical element of PhysicalElement '{self.getName()}' is neither Line"
                        f"nor Surface but: {type(GeoElement)}"
                    )
                )

        if isLine and isSurface:
            raise ValueError(
                "Geometical element list should not contain Lines and Surfaces!"
            )
        if isLine:
            return Line
        if isSurface:
            return Surface
        raise Exception("GeoElement-Type was neither Line nor Surface...")

    ###
    # Mit addToScript wird das PhysicalElement zum Skriptobjekt übergeben und in gmsh-Syntax
    # übersetzt. Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode
    # von Script) verwendet werden.
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
    #       PhysicalElement1.addToScript(myScript)
    #
    ###
    def addToScript(self, script: "Script"):
        """old add to script method

        Args:
            script (Script)
        """
        script._addPhysicalElement(self)

    def setColor(self, colorName: str = None):
        """Set mesh color for PhysicalElement

        If no mesh color name is given, it will be selected randomly from a list of X11 color names.

        All available mesh colors are listed under
        `gmsh colors <https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_11_0/src/common/Colors.h>`__.

        Args:
            colorName (str, optional): `X11 color name <https://en.wikipedia.org/wiki/X11_color_names>`__
                as string. Defaults to None.
        """
        if not colorName:
            index = round((len(colorDict) - 1) * random())
            colorName = list(colorDict.keys())[index]
            # colorName = colorName.replace("Light", "") # FIXME: This leads to an error in case of
            # "LightGoldenrodYellow"... Maybe skip that color in the color-dict or implement better
            # algorithm to catch light colors
        for geoElem in self.geometricalElement:
            if isinstance(geoElem, Surface):
                geoElem.setMeshColor(colorName)
