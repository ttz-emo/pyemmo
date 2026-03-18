#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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
"""Module for Class Machine"""
from __future__ import annotations

import logging
import warnings
from math import gcd
from typing import Literal

from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from . import default_param_dict
from .domain import Domain
from .geometry.line import Line
from .physicals.movingband import MovingBand
from .physicals.physical_element import PhysicalElement
from .rotor import Rotor
from .stator import Stator


class Machine:
    """The :class:`Machine` class represents a container for all :class:`PhysicalElement`
    objects of the ONELAB model and interfaces them from Gmsh to GetDP by prefined
    :class:`Domain` instances.
    E.g. all :class:`Slot` objects of the machine stator will be placed in Domain
    \"DomainS\" (defined by the PyEMMO machine model template) for model regions with
    imposed current density boundary.
    All predefined domains names can be found in :mod:`pyemmo.script`.

    Furthermore the :class:`Machine` class gathers all relevant machine parameters for
    the initialization of the ONELAB model.
    """

    def __init__(
        self,
        nbrPolePairs: int,
        rotor: Rotor,
        stator: Stator,
        name: str = "",
        symmetryFactor: int | None = None,
    ):
        """
        Constructor of class Machine

        Args:
            nbrPolePairs (int): Number of pole pairs of machine.
            rotor (Rotor): PyEMMO Rotor class object
            stator (Stator): PyEMMO Stator class object
            name (str, optional): Machine name. Defaults to "machine".
            symmetryFactor (Union[int, None]): Fixed given symmetry factor. If
                None is given, the symmetry factor will be calculated by number
                of slots and poles.

        """
        self.name = name if name else "machine"
        self.nbrPolePairs = nbrPolePairs
        self.rotor = rotor
        self.stator = stator

        # Setting outer given symmetry factor. Will only be used if not None.
        if not isinstance(symmetryFactor, (int, float)):
            raise TypeError(
                f"Symmetry factor must be integer but is {type(symmetryFactor)}"
            )
        if symmetryFactor % 1 != 0:
            raise ValueError(
                f"Symmetry factor must be integer number but is: {symmetryFactor}"
            )
        self._symmetry_factor = symmetryFactor
        # if rotor and stator are given, create machine domains
        if rotor and stator:
            self.create_domains()

    def get_sim_params(self) -> dict:
        """
        Return the machines **geometical** simulation parameters as dict with parameter
        names as keys:

            - SYMMETRY_FACTOR
            - L_AX_R
            - L_AX_S
            - NBR_POLE_PAIRS
            - NBR_TURNS_IN_FACE
            - R_AIRGAP
        """
        paramDict = default_param_dict["GEO"]
        paramDict["SYMMETRY_FACTOR"] = self.symmetry_factor
        paramDict["L_AX_R"] = self.rotor.axial_length
        paramDict["L_AX_S"] = self.stator.axial_length
        paramDict["NBR_POLE_PAIRS"] = self.nbrPolePairs
        paramDict["NBR_SLOTS"] = self.stator.nbr_slots
        nbr_turns = self.stator.winding.get_turns()
        if isinstance(nbr_turns, (int, float)):
            paramDict["NBR_TURNS_IN_FACE"] = nbr_turns
        else:
            raise ValueError(
                "PyEMMO cant handle individual number of turns per Coil!"
                "Number of winding turns must be single value in swat-em datamodel"
            )
        paramDict["R_AIRGAP"] = self.rotor.movingband[0].radius
        return paramDict

    def create_domains(self) -> None:
        """Create the different Machine Domains for the PyEMMO machine model template."""
        rotor = self.rotor
        stator = self.stator
        ###DomainS beinhaltet alle Physical Elements, die bestromt werden.
        self._domainS = Domain(
            "DomainS",
            rotor._domainS.physicals + stator._domainS.physicals,
        )
        ###DomainM beinhaltet alle Physical Elements, die magnetisiert sind.
        self._domainM = Domain("DomainM", rotor._domainM.physicals)
        ###DomainC beinhaltet alle Physical Elements, die leitend sind.
        self._domainC = Domain(
            "DomainC",
            rotor._domainC.physicals + stator._domainC.physicals,
        )
        ###mbRotor beinhaltet alle Physical Elements, die eine Moving Band auf der
        # Rotorseite beschreiben.
        self._mbRotor = Domain("MB_Rotor", rotor._mb.physicals)
        ###mbStator beinhaltet alle Physical Elements, die eine Moving Band auf der
        # Statorseite beschreiben.
        self._mbStator = Domain("MB_Stator", stator._mb.physicals)
        ###domain beinhaltet alle Physical Elements, die die elektrische Maschine
        # beschreiben.
        self._domain = Domain(
            "Domain",
            rotor._domain.physicals + stator._domain.physicals,
        )
        ###domainL beinhaltet alle Physical Elements, die ein lineares Material besitzen.
        self._domainL = Domain(
            "DomainL",
            rotor._domainL.physicals + stator._domainL.physicals,
        )
        ###domainNL beinhaltet alle Physical Elements, die ein nicht lineares Material
        # besitzen.
        self._domainNL = Domain(
            "DomainNL",
            rotor._domainNL.physicals + stator._domainNL.physicals,
        )

        ###rotorMoving beinhaltet alle Physical Elements, die während der Simulation
        # rotiert werden müssen (Rotor).
        self._rotorMoving = Domain("Rotor_Moving", rotor._rotorMoving.physicals)
        ###mbBaux beinhaltet alle Hilfslinien des MovingBands (Ergänzung zum Vollkreis),
        # die wegen der Symmetrie ergänzt werden mussten. MovingBand auf der Rotorseite
        # muss ein vollständiger Kreis beschreiben.
        self._mbBaux = Domain("Rotor_Bnd_MBaux", rotor._mbBaux.physicals)
        ###DomainAirGapRotor beinhaltet alle Physical Elements, die einen Luftspalt auf
        # der Rotorseite (Luftspalt bis zum Moving Band) beschreiben.
        self._domainAirGapRotor = Domain("Rotor_Airgap", rotor._domainAirGap.physicals)
        ###DomainAirGapStator beinhaltet alle Physical Elements, die einen Luftspalt auf
        # der Statorseite (Luftspalt ab dem Moving Band bis Statorinnenseite)
        # beschreiben.
        self._domainAirGapStator = Domain(
            "Stator_Airgap", stator._domainAirGap.physicals
        )

        if (
            len(self.rotor._domainPrimary.physicals + stator._domainPrimary.physicals)
            > 0
        ):
            ###primarykante der elektrischen Maschine.
            self._domainPrimary = Domain(
                "PrimaryRegion_Rotor",
                rotor._domainPrimary.physicals + stator._domainPrimary.physicals,
            )
            ###Slavekante der elektrischen Maschine.
            self._domainSlave = Domain(
                "SlaveRegion_Rotor",
                rotor._domainSlave.physicals + stator._domainSlave.physicals,
            )
        else:
            self._domainPrimary = None
            self._domainSlave = None
        ###Innengrenze an der Welle.
        self._domainInnerLimit = Domain(
            "InnerLimitLine", rotor._domainInnerLimit.physicals
        )
        ###Maschinenaußengrenze.
        self._domainOuterLimit = Domain(
            "OuterLimitLine", stator._domainOuterLimit.physicals
        )

    def domains_created(self) -> bool:
        """Check if the machine domains have been created.

        Returns:
            bool: True, if domains have been created; else False.
        """
        try:
            self.domains
        except AttributeError:
            return False
        return True

    @property
    def name(self) -> str:
        """name of machine"""
        return self._name

    @name.setter
    def name(self, nameVal: str):
        """Setter of machine name"""
        if isinstance(nameVal, str):
            self._name = nameVal
        else:
            raise TypeError(f"Given name was not type str, but '{type(nameVal)}'")

    @property
    def symmetry_factor(self) -> int:
        """Getter of Symmetry Factor

        Returns:
            int: Symmetry Factor
        """
        if self._symmetry_factor:
            # if external symmetry factor is given:
            return self._symmetry_factor
        # if sym is not given, try to calculate it
        if self.rotor and self.stator:
            nbr_poles = self.nbrPolePairs * 2
            sym_machine = gcd(self.stator.nbr_slots, nbr_poles)
            sym_winding = self.stator.winding.get_periodicity_t() * 2
            # logger.debug("Symmetry factor winding: %s",{sym_winding})
            sym_factor = min(sym_winding, sym_machine)
            return sym_factor
        raise RuntimeError("Tried to compute sym factor, but rotor/stator not defined!")

    # @symmetryFactor.setter
    # def symmetryFactor(self, symFactor: int):
    #     """Setter for Symmetry Factor

    #     Args:
    #         symFactor (int): Symmetry Factor
    #     """
    #     assert type(symFactor) == int
    #     self._symmetryFactor = symFactor

    @property
    def nbrPolePairs(self) -> int:
        """number of pole pairs"""
        return self._nbrPolePairs

    @nbrPolePairs.setter
    def nbrPolePairs(self, nbrPolePairs: int | float) -> None:
        """Setter of number of pole pairs

        Args:
            nbrPolePairs (Union[int, float]): Pole pair number of machine.

        Raises:
            TypeError: If number of pole pairs in not positiv integer.
        """

        if isinstance(nbrPolePairs, int):
            self._nbrPolePairs = nbrPolePairs
        elif isinstance(nbrPolePairs, float):
            if nbrPolePairs.is_integer():
                self._nbrPolePairs = int(nbrPolePairs)
        else:
            raise TypeError(
                f"Given number of pole pairs was not an integer (p={nbrPolePairs})"
            )

    @property
    def rotor(self) -> Rotor:
        """Get the rotor object of the machine"""
        return self._rotor

    @rotor.setter
    def rotor(self, newRotor: Rotor):
        if isinstance(newRotor, Rotor):
            self._rotor = newRotor
            if self.domains_created():
                # if domains have been created before, recreate them.
                self.create_domains()
        elif newRotor is None:
            self._rotor = None
        else:
            raise TypeError(f"Wrong type for rotor: {type(newRotor)}")

    @property
    def stator(self) -> Stator:
        """Get the stator object of the machine"""
        return self._stator

    @stator.setter
    def stator(self, newStator: Stator):
        if isinstance(newStator, Stator):
            self._stator = newStator
            if self.domains_created():
                # if domains have been created before, recreate them.
                self.create_domains()
        elif newStator is None:
            self._stator = None
        else:
            raise TypeError(f"Wrong type for stator: {type(newStator)}")

    @property
    def domains(self) -> list[Domain]:
        """Return all Domains of the machine as list

        Returns:
            list(Domain)
        """
        domainList: list[Domain] = []
        # Add primary and slave lines first!
        if self._domainPrimary != None:
            domainList.append(self._domainPrimary)
            domainList.append(self._domainSlave)
        # Add Movingband
        domainList.append(self._mbRotor)
        domainList.append(self._mbBaux)
        domainList.append(self._mbStator)
        domainList.append(self._rotorMoving)
        # Add outer an inner boundarys
        domainList.append(self._domainInnerLimit)
        domainList.append(self._domainOuterLimit)
        # Add Airgaps
        domainList.append(self._domainAirGapRotor)
        domainList.append(self._domainAirGapStator)
        # Add other physical Domains
        domainList.append(self._domainS)
        domainList.append(self._domainM)
        domainList.append(self._domainC)
        domainList.append(self._domain)
        domainList.append(self._domainL)
        domainList.append(self._domainNL)
        return domainList

    @property
    def primary_lines(self) -> list[Line]:
        """Get a list of primary lines of rotor and stator

        Returns:
            List[Line]: list of primary line geometrical elements
        """
        rotorDict = self.rotor.sortPhysicals()
        statorDict = self.stator.sortPhysicals()
        physicalPrimeLines = rotorDict["primary"] + statorDict["primary"]
        primeLines: list[Line] = []
        for physicalPrimeLine in physicalPrimeLines:
            if physicalPrimeLine.geo_type == Line:
                primeLines.extend(physicalPrimeLine.geo_list)
            else:
                raise (
                    TypeError("PrimaryLine physicals must only contain Line objects!")
                )
        primeLines.sort(key=_get_line_middle_raidus)
        return primeLines

    def get_secondary_lines(self) -> list[Line]:
        """Get a list of secondary lines of rotor and stator

        Returns:
            List[Line]: list of secondary line geometrical elements
        """
        rotorDict = self.rotor.sortPhysicals()
        statorDict = self.stator.sortPhysicals()
        secondary_physicals = rotorDict["secondary"] + statorDict["secondary"]
        lines: list[Line] = []
        for secondary_phys in secondary_physicals:
            if secondary_phys.geo_type == Line:
                lines.extend(secondary_phys.geo_list)
            else:
                raise (
                    TypeError("SecondaryLine physicals must only contain Line objects!")
                )
        lines.sort(key=_get_line_middle_raidus)
        return lines

    @property
    def physicals(self) -> list[PhysicalElement]:
        """Get a list of all physical elements

        Returns:
            List[PhysicalElement]: List of physical elements
        """
        return self.stator.physicals + self.rotor.physicals

    def setFunctionMesh(
        self,
        basisMeshsize: float = None,
        meshGainFactor: float = None,
        functionType: Literal["linear", "quad"] = None,
    ):
        """**Old function name for** ``set_function_mesh()``.

        Args:
            basisMeshsize (float, optional): Basis mesh size to use near the
                airgap (minimal mesh size).
                Defaults to 2 * Pi * Rotor_Movingband_Radius / 360.
            meshGainFactor (float): Gain factor for mesh size from airgap to
                outer machine limit. Defaults to (r_in / basisMeshsize / 3) or 30.
            functionType (Literal[&quot;linear&quot;, &quot;quad&quot;]):
                linear or quadratic function for mesh size. Defaults to linear

        :meta private:
        """
        warnings.warn(
            "Function setFunctionMesh() was renamed set_function_mesh()",
            DeprecationWarning,
        )
        # TODO: Remove in future.
        self.set_function_mesh(basisMeshsize, meshGainFactor, functionType)

    def set_function_mesh(
        self,
        basis_size: float = None,
        gain_factor: float = None,
        function_type: Literal["linear", "quad"] = None,
    ):
        """Add functional mesh size setting for machine if you don't want to
        specify mesh sizes individually. Mesh size is set to increase from
        airgap to both sides (rotor and stator). Maximal mesh size will be
        basis_size * gain_factor.
        If basis_size is not given, its set to:

        :attr:`basis_size` = :math:`\\frac{2\\pi}{360} \\cdot r_\\mathrm{MB,Rotor}`.

        Args:
            basis_size (float, optional): Basis mesh size to use near the
                airgap (minimal mesh size).
                Defaults to 2 * Pi * Rotor_Movingband_Radius / 360.
            gain_factor (float): Gain factor for mesh size from airgap to
                outer machine limit.
            function_type (Literal[&quot;linear&quot;, &quot;quad&quot;]):
                linear or quadratic function for mesh size.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Using automatic mesh generation.")
        if not basis_size:
            # calc movingband hight
            h_mb = abs(self.rotor.movingband_radius - self.stator.movingband_radius)
            basis_size = h_mb
            logger.debug(
                "Setting basis mesh size to movingband hight = %.3e",
                h_mb,
            )

        self.rotor.set_function_mesh(
            basis_size=basis_size,
            gain_factor=gain_factor,
            function_type=function_type,
        )
        self.stator.set_function_mesh(
            basis_size=basis_size,
            gain_factor=gain_factor,
            function_type=function_type,
        )
        # # get max. stator radius:
        # rS = 0
        # for phys in self.stator._domainOuterLimit.physicals:
        #     for geo in phys.geo_list:
        #         if isinstance(geo, Line):
        #             for p in geo.points:
        #                 if p.radius > rS:
        #                     rS = p.radius
        # # calculate linear mesh size functions (ax+b)
        # if functionType == "linear":
        #     a1 = (1 - meshGainFactor) / rMb
        #     b1 = meshGainFactor

        #     a2 = (meshGainFactor - 1) / (rS - rMb)
        #     b2 = meshGainFactor - a2 * rS
        # elif functionType == "quad":
        #     # calculate function coefficients for ax^2+bx+c
        #     c = meshGainFactor
        #     b = -2 * c / rMb
        #     a = -b / 2 / rMb
        # else:
        #     mssg = f"Unknown function specifier '{functionType}' for functional mesh."
        #     raise ValueError(mssg)
        # for physical in self.physicalElements:
        #     for geo in physical.geo_list:
        #         points: List[Point] = []
        #         if isinstance(geo, Surface):
        #             for curve in geo.curve:
        #                 points.extend(curve.points)
        #         elif isinstance(geo, Line):
        #             points.extend(geo.points)
        #         # All curves should belong to a surface...
        #         # else:
        #         #     points.extend(geo.getPoints())
        #         for point in points:
        #             rP = point.radius
        #             if functionType == "linear":
        #                 if rP < rMb:
        #                     # meshSizeFaktor = (a1*rP+b1)
        #                     pMeshSize = (a1 * rP + b1) * basisMeshsize
        #                 else:
        #                     pMeshSize = (a2 * rP + b2) * basisMeshsize
        #             elif functionType == "quad":
        #                 # faktor = 4770*rP**2 - 430 * rP + 10 # poly 2 fit
        #                 faktor = (a * rP**2 + b * rP + c) + 1
        #                 faktor = 1 if faktor < 1 else faktor
        #                 pMeshSize = faktor * basisMeshsize
        #             point.meshLength = pMeshSize

    def plot(
        self,
        fig: Figure | None = None,
        linewidth=0.5,
        marker=".",
        markersize=1,
        plot_mb: bool = False,
    ) -> Figure:
        """
        2D Line plot of the surface
        """
        if fig is None:
            fig, ax = plt.subplots(dpi=100)
            ax.set_aspect("equal", adjustable="box")
        else:
            ax = fig.axes
        # plot all physicals
        domains = self.domains
        for domain in domains:
            for phys in domain.physicals:
                if not plot_mb:
                    if isinstance(phys, MovingBand):
                        break
                for geoElem in phys.geo_list:
                    geoElem.plot(
                        fig=fig,
                        linewidth=linewidth,
                        marker=marker,
                        markersize=markersize,
                        color=[0, 0, 0],
                    )
        # # Set axes limits
        if self.symmetry_factor > 1 and not plot_mb:
            ## offset y axis
            # calc most upper point:
            #   TODO: Find a universal solution for the bounding box... Maybe with a
            #   new matplotlib version its easier to get the bbox of only lines or so.

            #   We need extra case for symmetry 2 and 3 because there then the most
            #   upper point is the outer radius
            # if self.symmetryFactor <=3:
            #     y_max = self.stator.outer_radius
            # else:
            #     # calc max. y point by angle and radius
            #     y_max = ...

            # y_bounds = fig.axes[0].get_ybound()
            # y_offset = self.stator.outer_radius / 10
            ax.set_ylim(
                bottom=-self.stator.outer_radius / 20,
                top=self.stator.outer_radius * 1.05,
            )
            if self.symmetry_factor > 2:
                ax.set_xlim(left=0)
        return fig


def _get_line_middle_raidus(line: Line) -> float:
    """
    Get the radius of the middlepoint of a Line object.
    Used for sorting primary and secondary lines by their radius.

    Args:
        line (Line): Line object

    Returns:
        float: Radius of ``Line.middle_point``

    :meta private:
    """
    return line.middle_point.radius
