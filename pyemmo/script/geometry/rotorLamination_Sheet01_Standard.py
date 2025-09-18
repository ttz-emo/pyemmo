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

from ..gmsh.gmsh_arc import GmshArc
from ..gmsh.gmsh_line import GmshLine
from ..gmsh.gmsh_point import GmshPoint, Point
from ..gmsh.gmsh_surface import GmshSurface
from .rotorLamination import RotorLamination


class RotorLamination_Sheet01_Standard(RotorLamination):
    """Class RotorLamination_Sheet01_Standard"""

    def __init__(self, parameters: dict):
        """Konstruktor der Klasse RotorLamination Type Sheet01_Standard

        Args:
            parameters (dict): Machine parameter dict. Must contain the following values:
                - material
                - r_We
                - r_R
                - meshLength
                - startPosition
                - machineCentrePoint
                - angleGeoParts
        """
        self._machineDict = parameters
        super().__init__(
            name="RotorLamination_Sheet01_Standard",
            material=parameters["material"],
            geo_list=self._createGeometry(),  # creates the lamination surface
        )

    def _createGeometry(self):
        """Create the geometry of the half a lamination segment in Gmsh"""
        r_We = self._machineDict["r_We"]
        r_R = self._machineDict["r_R"]

        PCentre = self._machineDict["machineCentrePoint"].duplicate()
        coordCentre = PCentre.coordinate

        alpha = self._machineDict["angleGeoParts"]

        # Konstuktion der Punkte an der x-Achse
        # point inner curve on x-axis
        pWelle1 = GmshPoint.from_coordinates(
            (coordCentre[0] + r_We, coordCentre[1], coordCentre[2]),
            self._machineDict["meshLength"],
            "pWelle1",
        )
        # inner curve on symmetry axis
        pWelle2 = pWelle1.duplicate("pWelle2")
        pWelle2.rotateZ(PCentre, alpha)
        # outer curve on x-axis
        pRotor1 = pWelle1.duplicate("pRotor1")
        pRotor1.translate(r_R - r_We, 0, 0)
        # outer curve on symmetry axis
        pRotor2 = pRotor1.duplicate("pRotor2")
        pRotor2.rotateZ(PCentre, alpha)

        # Startposition berücksichtigen
        pWelle1.rotateZ(PCentre, self._machineDict["startPosition"])
        pWelle2.rotateZ(PCentre, self._machineDict["startPosition"])
        pRotor1.rotateZ(PCentre, self._machineDict["startPosition"])
        pRotor2.rotateZ(PCentre, self._machineDict["startPosition"])

        # Konstuktion der Linien
        lWelle = GmshArc.from_points(pWelle1, PCentre, pWelle2, "lWelle")
        lBlech1 = GmshLine.from_points(pWelle2, pRotor2, "lBlech1")
        lRotorAussen = GmshArc.from_points(pRotor2, PCentre, pRotor1, "lRotorAussen")
        lBlech2 = GmshLine.from_points(pRotor1, pWelle1, "lBlech2")

        # Flächenerzeugen
        surfaceRotor = GmshSurface.from_curve_loop(
            name="surfaceRotor", curve_loop=[lWelle, lBlech1, lRotorAussen, lBlech2]
        )

        # surfaceRotor.setMeshColor(colorDict["SteelBlue"])

        # every toolkit object needs the following attributes
        # outer limit lines towards the airgap:
        self._outerLinePart = [lRotorAussen]
        # Interface line on symmetry axis:
        self._betweenLinePart = [lBlech2]
        # outer curve lamination center point:
        self._airDockingPoint1 = [pRotor1]
        # outer lamination curve the symmetry axis:
        self._airDockingPoint2 = [pRotor2]

        # geo_list = [surfaceRotor] will be set in super().__init__()
        return [surfaceRotor]

    @property
    def outerLinePart(self) -> list[GmshArc | GmshLine]:
        """Get the boundary line(s) of the rotor lamination towards the airgap

        Returns:
            List[GmshLine | GmshArc]: outer boundary lines towards the airgap
        """
        return self._outerLinePart

    @property
    def betweenLinePart(self) -> list[GmshLine]:
        """Interface line(s) on the symmmetry axis of a lamination segment"""
        return self._betweenLinePart

    @property
    def airDockingPoint1(self) -> list[Point]:
        """Get point of lamination segment at airgap interface on the x-axis."""
        return self._airDockingPoint1

    @property
    def airDockingPoint2(self) -> list[Point]:
        """Get point of lamination segment at airgap interface on symmetry axis."""
        return self._airDockingPoint2
