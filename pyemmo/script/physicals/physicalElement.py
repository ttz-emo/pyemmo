#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
# Applied Sciences Wuerzburg-Schweinfurt.
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
"""Module for class PhysicalElement"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import gmsh
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...definitions import LINE_COLOR
from ..geometry.circleArc import CircleArc
from ..geometry.line import Line
from ..geometry.spline import Spline
from ..geometry.surface import Surface
from ..gmsh.gmsh_line import GmshLine
from ..gmsh.gmsh_surface import GmshSurface
from ..material.material import Material

if TYPE_CHECKING:
    from ..script import Script


class PhysicalElement:
    """
    Eine Instanz der Klasse PhysicalElement ist die Gruppierung von Flächen/Linien im
    dreidimensionalen Raum.\n
    Input:
        name : string
        geo_list : [GmshLine] oder [GmshSurface]
        material : Material

    Beispiel:
        from pyemmo import *\n
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
    physicalID: int = 1000

    def __init__(
        self,
        name: str,
        geo_list: list[GmshSurface] | list[GmshLine],
        material: Material | None = None,
        phyID: int | None = None,
    ):
        # the physical element type can be used to identify physical elements
        self.physicalElementType = "PhysicalElement"

        self.name = name
        self.geo_list = geo_list  # set geo list to determine geo_type

        geo_type = 1 if self.geoElementType == Line else 2  # geo_type is Line or Surf
        tag_list = [elem.id for elem in geo_list]  # tag list for gmsh physical group
        if phyID is None:
            self.id = gmsh.model.addPhysicalGroup(geo_type, tag_list, name=name)
        else:
            self.id = gmsh.model.addPhysicalGroup(
                geo_type, tag_list, tag=phyID, name=name
            )
        self.material = material

    # ----- properties -----
    def __repr__(self):
        return f"{type(self)} - '{self.name}' - GmshID:{self.id} "

    @property
    def physicalElementType(self) -> str:
        """Type of physical element.
        This should be equal to class name...

        Returns:
            str: Physical element type, e.g. "PhysicalElement" or "Magnet"
        """
        return self._physicalElementType

    @physicalElementType.setter
    def physicalElementType(self, newPhysicalElementType: str) -> str:
        "setter for physicalElementType"
        if isinstance(newPhysicalElementType, str):
            self._physicalElementType = newPhysicalElementType
        else:
            raise TypeError(
                f"Type of physicalElementType must be string, but is {type(newPhysicalElementType)}"
            )

    @property
    def type(self) -> str:
        """The function getType of PhysicalElement returns a string with the PhysicalElement-Type"""
        return self._physicalElementType

    @property
    def name(self) -> str:
        """Phyiscal element name

        Returns:
            str: name
        """
        return self._name

    @name.setter
    def name(self, newName):
        "Setter for name"
        if isinstance(newName, (str)):
            self._name = newName
        else:
            raise TypeError("Type of name must be a string.")

    @property
    def material(self) -> Material | None:
        """Material of phyiscal element

        Returns:
            Material: material
        """
        return self._material

    @material.setter
    def material(self, newMaterial: Material | None):
        "Setter for material"
        if isinstance(newMaterial, Material) or newMaterial is None:
            self._material = newMaterial
        else:
            raise TypeError("Type of material must type pyemmo.Material!")

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """Physical element identification number.
        This is the ID that is used in ONELAB. Physical element IDs start at 1000
        and are counted automatically.

        Returns:
            int: Physical elemnt ID number.
        """
        return self._id

    @id.setter
    def id(self, newID: int):
        """setter of PhysicalElement ID

        Args:
            newID (int): new physical element ID.

        Raises:
            TypeError: If new id not is integer.
        """
        if not isinstance(newID, int):
            raise TypeError(f"PhysicalElement ID must be positive integer! {newID}")
        self._id = newID

    @property
    def geo_list(self) -> list[GmshSurface] | list[GmshLine]:
        """Geometrical enities of physical element.

        Returns:
            Union[List[GmshSurface], List[GmshLine]]: Geometrical Entities.
        """
        return self._geo_list

    @geo_list.setter
    def geo_list(self, geo_list: list[GmshSurface] | list[GmshLine]):
        """Geometrical elements

        Args:
            geo_list (Union[List[Surface], List[Line]]): Geometrical elements
        """
        # FIXME: PhysicalElement.geo_list can not be updated in Gmsh once the physical
        # is created! This should probably raise an error or delete and recreate the
        # physical group in Gmsh!
        # FIXME: No type checking implemented!
        self._geo_list = geo_list
        # run element type funtion to ensure there are not lines AND surfaces at the same time
        self.geoElementType

    # FIXME: TODO Rename geoElementType -> geo_type like in init!
    @property
    def geoElementType(self) -> Line | Surface | None:
        """get type of geometry elements.

        Raises:
            ValueError: If geometry element type is neither line nor surface.
            ValueError: If lines AND surface elements in geo element list.
            Exception: If element type could not be evaluated.

        Returns:
            Union[Line, Surface, None]: Type of geometric elements in geo list.
        """
        if len(self.geo_list) == 0:
            # if list is empty return None
            return None
        # Otherwise determine geometry type:
        isSurface = False
        isLine = False
        for GeoElement in self.geo_list:
            if isinstance(GeoElement, Surface):
                isSurface = True
            elif isinstance(GeoElement, (Line, CircleArc, Spline)):
                isLine = True
            else:
                raise ValueError(
                    f"Geometrical element of PhysicalElement '{self.name}' is neither Line"
                    f"nor Surface but: {type(GeoElement)}"
                )

        if isLine and isSurface:
            raise ValueError(
                "Geometical element list should not contain Lines and Surfaces!"
            )
        if isLine:
            return Line
        if isSurface:
            return Surface
        raise TypeError("GeoElement-Type was neither Line nor Surface...")

    # ---------- methods ----------

    def _getNewID(self):
        """Wird eine Instanz erzeugt, bekommt sie automatisch eine eindeutige ID zugewiesen.
        Mit getNewID() wird eine neue ID erzeugt."""
        PhysicalElement.physicalID = PhysicalElement.physicalID + 1
        return PhysicalElement.physicalID

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
    def addToScript(self, script: Script):
        """old add to script method

        Args:
            script (Script)
        """
        script._addPhysicalElement(self)

    def get_radial_position(self) -> float:
        """get the mean radial position of the PhsicalElement.\n
        This is useful when e.g. sorting the slots in radial direction.

        Returns:
            float: Mean radius of the physical elements geometry positions.
                - Mean radius of the center of the physical surface(s) in m
                - Mean radius of the middle point of the physical line(s) in m
        """
        radius_list: list[float] = []
        for elem in self.geo_list:
            if self.geoElementType == Surface:
                centerPoint = elem.calcCOG()
                radius_list.append(centerPoint.radius)
            elif self.geoElementType == Line:
                radius_list.append(elem.middle_point.radius)
            else:
                raise ValueError(
                    f"Can't determine radial position of physical {self.name}, because "
                    f"geometry element type is {self.geoElementType}. "
                    "Must be Surface or Line!"
                )
        return np.mean(radius_list)

    def get_circumferential_position(self) -> float:
        """get the circumferential position of a PhsicalElement.\n
        This is useful when e.g. sorting the rotor bars in circumfederal direction.

        float: Mean angle to x-axis of the physical elements geometry positions.
                - Mean angle of the center (COG) of the physical surface(s) in m
                - Mean angle of the middle point of the physical line(s) in m
        """
        if not self.geo_list:
            raise RuntimeError("No geometry to determine slot position.")
        angle_list: list[float] = []
        for elem in self.geo_list:
            if self.geoElementType == Surface:
                centerPoint = elem.calcCOG()
                angle_list.append(centerPoint.getAngleToX())
            elif self.geoElementType == Line:
                angle_list.append(elem.middle_point.getAngleToX())
            else:
                raise ValueError(
                    f"Can't determine circumferential position of physical {self.name}, "
                    f"because geometry element type is {self.geoElementType}. "
                    "Must be Surface or Line!"
                )
        return np.mean(angle_list)

    def setColor(self, colorName: str = None):
        """Set mesh color for PhysicalElement

        If no mesh color name is given, it will be selected randomly from a list of X11 color names.

        All available mesh colors are listed under
        `gmsh colors <https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_11_0/src/common/Colors.h>`__.

        Args:
            colorName (str, optional):
                `X11 color name <https://en.wikipedia.org/wiki/X11_color_names>`__
                as string. Defaults to None.
        """
        if not colorName:
            colorName = np.random.random(4)
            colorName[3] = 1.0  # set alpha to 1.0
        for geoElem in self.geo_list:
            if isinstance(geoElem, GmshSurface):
                geoElem.mesh_color = colorName
                # r, g, b, a = Colors[colorName]
                # gmsh.model.setColor([(2, geoElem.id)], r, g, b, a)
            else:
                logger = logging.getLogger(__name__)
                logger.warning(
                    "Could not set mesh color for surface %s, because it is not a GmshSurface!",
                    geoElem.name,
                )

    def plot(
        self,
        fig: Figure = None,
        linewidth=0.5,
        color=LINE_COLOR,
        marker=".",
        markersize=1,
        tag=False,
    ) -> tuple[Figure, Axes]:
        """
        2D Line plot of the surface
        """
        if fig is None:
            fig, ax = plt.subplots()
            fig.set_dpi(200)
            # xlim, ylim = self.getBoundingBox(scalingFactor=1.1)
            # fig.axes[0].set(xlim=xlim, ylim=ylim)
            ax.set_aspect("equal", adjustable="box")
        ax = fig.axes[0]
        for geo in self.geo_list:
            geo.plot(
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=False,
            )

        if tag:
            if self.geoElementType == Surface:
                for surf in self.geo_list:
                    cog = surf.calcCOG().coordinate
                    ax.annotate(
                        f"""S {self.id} ("{self.name}")""",
                        (cog[0], cog[1]),
                        textcoords="offset points",
                        xytext=(1, 1),
                        ha="left",
                    )
            else:
                # line plot
                curves: list[Line, CircleArc, Spline] = self.geo_list
                center = np.mean([c.middle_point.coordinate for c in curves], axis=0)
                ax.annotate(
                    f"""{self.__class__.__name__}: {self.name}""",
                    (center[0], center[1]),
                    textcoords="offset points",
                    xytext=(1, 1),
                    ha="left",
                )
        return fig, ax
