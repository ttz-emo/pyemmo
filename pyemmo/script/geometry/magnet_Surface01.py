#
# Copyright (c) 2018-2025 M. Schuler, TTZ-EMO,
# Technical University of Applied Sciences Wuerzburg-Schweinfurt.
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
from __future__ import annotations

from typing import Literal

from ..gmsh.gmsh_arc import GmshArc
from ..gmsh.gmsh_line import GmshLine
from ..gmsh.gmsh_point import GmshPoint
from ..gmsh.gmsh_surface import GmshSurface
from .magnet import Magnet


class Magnet_Surface01(Magnet):
    """Class Magnet_Surface01

    The parameters must be given by a dict with the exact matching parameter names!

    Parameters:
        rA_Rotor (float): Rotor outer radius
        h_M (float): Magnet hight
        angularWidth_i (float): Inner angular width in radians.
        angularWidth_a (float): Outer angular width in radians.
        magnetisationDirection (Literial[-1,1]): see definition in Class
            :class:`~pyemmo.script.geometry.magnet.Magnet`
        magnetisationType (str): see definition in Class
            :class:`~pyemmo.script.geometry.magnet.Magnet`
        material (Material): Material of magnet.
        meshLength (float):

    .. figure:: ../images/magnet_Surface01.png
        :align: center

        Parameter description for Magnet_Surface01
    """

    def __init__(
        self,
        properties: dict,
        magnetisationDirection: Literal[1, -1],
        magnetisationType: str,
    ):
        """Magnet Surface01

        Args:
            machineDict (dict): Dict with machine parameters. Must contain values for
                - material (Material): Material of magnet.
                - rA_Rotor (float): Rotor outer radius.
                - h_M (float): Magnet height.
                - angularWidth_i (float): Inner angular width of the magnet in radians.
                - angularWidth_a (float): Outer angular width of the magnet in radians.
            magnetisationDirection (Literal[-1, 1]): magnetization direction (north or
                south pole)
            magnetisationType (str): magnetization type ("parallel", "radial",
                "tangential")
        """
        self._machineDict = properties

        self.id = self._getNewID()
        magName = "Magnet_Surface01_" + str(self.id)
        super().__init__(
            magName,
            self._createGeometry(),
            properties["material"],
            magnetisationDirection,
            magnetisationType,
            0.0,
        )

    def _createGeometry(self):
        """Create the magnet geometry"""
        dockingLength = self._machineDict["rA_Rotor"]
        h_M = self._machineDict["h_M"]
        angle_ri = (
            self._machineDict["angularWidth_i"] / 2
        )  # over 2 because only half pole is modeled
        angle_ra = (
            self._machineDict["angularWidth_a"] / 2
        )  # over 2 because only half pole is modeled
        magnet_centre = self._machineDict["machineCentrePoint"]

        PCentre = magnet_centre.duplicate()
        coordCentre = PCentre.coordinate
        mesh_size = (
            self._machineDict["meshLength"]
            if "meshLength" in self._machineDict
            else h_M / 4
        )

        # Konstuktion der Punkte an der x-Achse
        pMagnet1 = GmshPoint.from_coordinates(
            (coordCentre[0] + dockingLength, coordCentre[1], coordCentre[2]),
            meshLength=mesh_size,
            name="pMagnet1",
        )
        pMagnet2 = pMagnet1.duplicate()
        pMagnet2.name = "pMagnet2"
        pMagnet3 = GmshPoint.from_coordinates(
            (coordCentre[0] + dockingLength + h_M, coordCentre[1], coordCentre[2]),
            meshLength=mesh_size,
            name="pMagnet3",
        )
        pMagnet4 = pMagnet3.duplicate()
        pMagnet4.name = "pMagnet4"
        pMagnet2.rotateZ(PCentre, angle_ri)
        pMagnet4.rotateZ(PCentre, angle_ra)

        # Startposition berücksichtigen
        pMagnet1.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet2.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet3.rotateZ(PCentre, self._machineDict["startPosition"])
        pMagnet4.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lMagnet1 = GmshArc.from_points(pMagnet1, PCentre, pMagnet2, "lMagnet1")
        lMagnet2 = GmshLine.from_points(pMagnet2, pMagnet4, "lMagnet2")
        lMagnet3 = GmshArc.from_points(pMagnet4, PCentre, pMagnet3, "lMagnet3")
        lMagnet4 = GmshLine.from_points(pMagnet3, pMagnet1, "lMagnet4")

        # Flächenerzeugen
        surfaceMagnet = GmshSurface.from_curve_loop(
            name="surfaceMagnet", curve_loop=[lMagnet1, lMagnet2, lMagnet3, lMagnet4]
        )

        # Bei jedem Baukasten muss diese Definition identisch sein
        ###Fläche des halben Magneten in einer Liste.
        ###Schnittkante des halben Magneten.
        self._innerLinePart = [lMagnet1]
        ###Punkt zwischen Magnet und Luft an der Schnittkante.
        self._airDockingPoint = [pMagnet3]
        ###Alle Linien in einer Liste, die den Luftraum schneiden.
        self._airLinePart = [lMagnet3, lMagnet2]
        ###Punkt zwischen Blechpaket und Magneten an der Schnittkante.
        self._laminationDockingPoint = [pMagnet1]

        return [surfaceMagnet]

        # for s in self._geo_list:
        #     if self.magDir == 1:
        #         s.setMeshColor(colorDict["Red"])
        #     elif self.magDir == -1:
        #         s.setMeshColor(colorDict["Green"])

    @property
    def innerLinePart(self) -> list[GmshArc]:
        """curve(s) on the boundary between magnet and lamination"""
        return self._innerLinePart

    @property
    def airDockingPoint(self) -> list[GmshPoint]:
        """Outer point of magnet on the symmetry axis."""
        return self._airDockingPoint

    @property
    def airLinePart(self) -> list[GmshLine | GmshArc]:
        """curves on the boundary between magnet and airgap"""
        return self._airLinePart

    @property
    def laminationDockingPoint(self) -> list[GmshPoint]:
        """Boundary point of magnet and lamination on the symmetry axis."""
        return self._laminationDockingPoint
