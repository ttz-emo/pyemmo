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
"""Module for Class Rotor"""

from __future__ import annotations

import copy
import logging
from math import pi
from typing import *

import gmsh
from matplotlib import pyplot as plt

from ..definitions import DEFAULT_GEO_TOL
from . import (
    DOMAIN,
    DOMAIN_AIRGAP,
    DOMAIN_BAR,
    DOMAIN_CONDUCTING,
    DOMAIN_LAMINATION,
    DOMAIN_LIMIT,
    DOMAIN_LINEAR,
    DOMAIN_MAGNET,
    DOMAIN_MOVINGBAND,
    DOMAIN_MOVINGBAND_AUX,
    DOMAIN_NON_CONDUCTING,
    DOMAIN_NON_LINEAR,
    DOMAIN_PRIMARY,
    DOMAIN_SECONDARY,
)
from .domain import Domain
from .geometry import default_domain_dict
from .geometry.line import Line
from .geometry.surface import Surface
from .gmsh.gmsh_point import GmshPoint
from .gmsh.utils import get_dim_tags, get_point_tags
from .material.electricalSteel import ElectricalSteel
from .physicals.magnet import Magnet
from .physicals.movingBand import MovingBand
from .physicals.physicalElement import PhysicalElement


class Rotor:
    """
    An instance of the Rotor class describes the rotor of an electrical
    machine in three-dimensional space. This class is used in conjunction with
    the class Machine. The user himself defines the type of machine by
    defining his physical elements. This class should only be used if the
    geometry of the machine is further processed as an import (e.g. Step). To
    use the construction kit, it makes sense to specify the machine first. You
    should therefore use specific classes for this, e.g. machineSPMSM (for
    surface magnets) and the associated class RotorSPMSM.

    """

    def __init__(
        self,
        physicalElementList: List[PhysicalElement],
        name: str = "",
        axLen: float = 1.0,
    ):
        """
        Constructor of class Rotor

        Args:
            physicalElements (List[PhysicalElement]): List of PhysicalElement
                objects defining geometry and materials.
            name (str): Defaults to \"\".
            axLen (float): Active axial length of stator lamination in [m].
                Defaults to 1.0

        """
        self.logger = logging.getLogger(__name__)
        self.name = name if name else "Rotor"  # rotor name
        self.physicalElements = physicalElementList  # rotor physical elements
        self.axialLength = axLen  # active axial length
        self._createDomainForRotor()  # create rotor domains

    @property
    def name(self) -> str:
        """Getter of rotor name

        Returns:
            str: _name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Setter of rotor name

        Args:
            name (str): _name
        """

        if isinstance(name, str):
            self._name = name

    @property
    def axialLength(self) -> float:
        """Getter of rotor axLen [m]

        Returns:
            float: _axLen
        """

        return self._axLen

    @axialLength.setter
    def axialLength(self, axLen: Union[float, int]) -> None:
        """Setter of rotor axial length axLen [m]

        Args:
            axLen (Union[float, int]): _description_

        Raises:
            TypeError: _description_
        """

        if isinstance(axLen, (float, int)):
            self._axLen = axLen
        else:
            raise TypeError(
                f"Given axial length axLen was not numeric but {type(axLen)}."
            )

    @property
    def physicalElements(self) -> List[PhysicalElement]:
        """Getter of PhysicalElements-list

        Returns:
            List[PhysicalElement]: _physicalElements
        """

        return self._physicalElements

    @physicalElements.setter
    def physicalElements(self, physicalElementsList: List[PhysicalElement]) -> None:
        """Setter of PhysicalElements-List

        Args:
            physicalElementsList (List[PhysicalElement]): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """

        if isinstance(physicalElementsList, List):
            self._physicalElements = physicalElementsList
            # pylint: disable=locally-disabled,  pointless-statement
            self._createDomainForRotor()  # recreate domains for rotor with new elements
            return None
        if isinstance(physicalElementsList, PhysicalElement):
            self._physicalElements = [physicalElementsList]
            self._createDomainForRotor()  # recreate domains for rotor with new elements
            return None
        raise TypeError(f"physicalElementList- type: {type(physicalElementsList)}.")

    def addPhysicalElements(self, physicalElementList: List[PhysicalElement]):
        """Append PhysicalElements to the rotor and recreate domains"""
        if isinstance(physicalElementList, list):
            for physicalElem in physicalElementList:
                if physicalElem not in self._physicalElements:
                    self._physicalElements.append(physicalElem)
            # pylint: disable=locally-disabled,  pointless-statement
            self._createDomainForRotor()  # recreate domains for rotor with new elements
        else:
            raise ValueError("'physicalElementList' was not type list!")

    ###Automatische Zuweisung der PhysicalElemente zu den passenden Domainen.
    def _createDomainForRotor(self) -> None:
        allPhy = self.sortPhysicals()

        ###DomainC beinhaltet alle Physical Elements, die leitend sind.
        self._domainC = Domain("DomainC_Rotor", allPhy["domainC"])
        self._domainCC = Domain("DomainCC_Rotor", allPhy["domainCC"])

        ###DomainAirGap beinhaltet alle Physical Elements, die einen Luftspalt auf der
        # Rotorseite (Luftspalt bis zum Moving Band) beschreiben.
        if not allPhy["airGap"]:
            self.logger.warning(
                "No physical elements for rotor airgap domain. "
                "Make sure your airgap physical surface is defined as AirGap object!"
            )
        self._domainAirGap = Domain("Rotor_Airgap", allPhy["airGap"])

        ###DomainM beinhaltet alle Physical Elements, die magnetisiert sind.
        self._domainM = Domain("DomainM_Rotor", allPhy["domainM"])

        ###DomainLam beinhaltet alle Physical Elements, die geblecht sind.
        self._domainLam = Domain("DomainLam_Rotor", allPhy["domainLam"])

        ###mb beinhaltet alle Physical Elements, die eine Moving Band auf der
        # Rotorseite beschreiben.
        self._mb = Domain("MB_Rotor", allPhy["mb_all"])
        ###mbBaux beinhaltet alle Hilfslinien des MovingBands (Ergänzung zum Vollkreis),
        # die wegen der Symmetrie ergänzt werden mussten. MovingBand auf der Rotorseite#
        # muss ein vollständiger Kreis beschreiben.
        self._mbBaux = Domain("Rotor_Bnd_MBaux", allPhy["mb_Mbaux"])

        ###DomainS beinhaltet alle Physical Elements, die bestromt werden.
        self._domainS = Domain("DomainS_Rotor", allPhy["domainS"])

        ###domain beinhaltet alle Physical Elements, die den gesamten Rotor beschreiben.
        self._domain = Domain("Domain_Rotor", allPhy["domain"])

        ###domainL und domainNL beinhaltet alle Physical Elements, die ein lineares bzw.
        # nicht-linears Material besitzen.
        self._domainL = Domain("DomainL_Rotor", allPhy["domainL"])
        self._domainNL = Domain("DomainNL_Rotor", allPhy["domainNL"])

        ###rotorMoving beinhaltet alle Physical Elements, die während der Simulation
        # rotiert werden müssen.
        self._rotorMoving = Domain("Rotor_Moving", allPhy["rotor_moving"])

        ###primarykante vom Rotor.
        self._domainPrimary = Domain("PrimaryRegion_Rotor", allPhy["primary"])
        ###Slavekante vom Rotor.
        self._domainSlave = Domain("SlaveRegion_Rotor", allPhy["slave"])
        ###Innengrenze der elektrischen Maschine (Welle).
        self._domainInnerLimit = Domain("InnerLimit_Rotor", allPhy["limit"])

    ###Sortierfunktion der PhysicalElements.
    def sortPhysicals(self) -> Dict[str, List[PhysicalElement]]:
        """
        Create a dict with the physical elements sorted into different domains with
        domain names as keys.
        The dict will look like

        .. code-block:: python

            {
                "domainS": phy_domainS,
                "domainM": phy_domainM,
                "domainLam": phy_domainLam,
                "domainC": phy_domainC,
                "domainCC": phy_domainCC,
                "mb_all": mb_all,
                "domain": phy_domain,
                "domainNL": phy_domainNL,
                "domainL": phy_domainL,
                "rotor_moving": phy_rotor_Moving,
                "mb_Mbaux": mb_Mbaux,
                "airGap": phy_airgap,
                "primary": phy_primaryLine,
                "slave": phy_slaveLine,
                "limit": limit_Line,
            }

        Returns:
            Dict[str, List[PhysicalElement]]: Sorted Physicals Dict

        """
        domain_dict: Dict[str, List[PhysicalElement]] = copy.deepcopy(
            default_domain_dict
        )
        # domainS = []  # Eingeprägte Ströme
        # domainM = []  # Magnete
        # domainLam = []  # Lamination (part with material specified lamination)
        # domainBar = []  # Conducting rotor bars of ASM
        # domainC = []  # Leitende Flächen z. B. Stäbe ASM
        # domainCC = []  # alle elektrisch nicht leitenden Flächen
        # allMbLines = []  # Moving Band

        # domain = []  # Alle Flächen
        # domainNL = []  # Alle nicht linearen Flächen
        # domainL = []  # Alle linearen Flächen

        # domainMoving = (
        # []
        # )  # Alle Teile die sich drehen, inkl. Moving Band (alle)
        # movingBandAux = []  # Bei Teilmodell -> die restlichen Moving Band
        # domainAirgap = []  # Luftspalt im Rotor

        # primaryLines = []  # Teilmodell primarykante
        # slaveLines = []  # Teilmodell Slavekante
        # limitLines = []  # Randlinien ohne Primär- und Sekundärkanten
        for physElem in self.physicalElements:
            geoType = physElem.geoElementType
            if geoType == Surface:
                # domainC, domainL & domainNL
                material = physElem.material
                if material:
                    # if conductivity not None add to domainC
                    if material.conductivity:
                        domain_dict[DOMAIN_CONDUCTING].append(physElem)
                    else:
                        domain_dict[DOMAIN_NON_CONDUCTING].append(physElem)
                    # if material is linear
                    if material.linear:
                        domain_dict[DOMAIN_LINEAR].append(physElem)
                    else:
                        domain_dict[DOMAIN_NON_LINEAR].append(physElem)
                    # if material is laminated
                    if isinstance(material, ElectricalSteel):
                        domain_dict[DOMAIN_LAMINATION].append(physElem)
                else:
                    physName = physElem.name
                    raise RuntimeError(
                        f"No Material defined: ({physName})",
                        f"Material is {material}",
                    )

                # domainM zuweisen
                if physElem.type == "Magnet":
                    magnet: Magnet = physElem
                    domain_dict[DOMAIN_MAGNET].append(magnet)
                    # remove magnet from C or CC because assignment is done by
                    # getdp. TODO: Improve this!
                    if magnet in domain_dict[DOMAIN_CONDUCTING]:
                        domain_dict[DOMAIN_CONDUCTING].remove(magnet)
                    elif magnet in domain_dict[DOMAIN_NON_CONDUCTING]:
                        domain_dict[DOMAIN_NON_CONDUCTING].remove(magnet)
                    continue

                # # domainS zuweisen
                # if physElem.type == "Slot":
                #     domainS.append(physElem)
                #     continue

                # airgap
                if physElem.type == "AirGap":
                    domain_dict[DOMAIN_AIRGAP].append(physElem)

                # Stator lamination if not allready defined
                if physElem.type == "Lamination":
                    # pE could allready been added due to material
                    if physElem not in domain_dict[DOMAIN_LAMINATION]:
                        domain_dict[DOMAIN_LAMINATION].append(physElem)

                # Stator lamination if not allready defined
                if physElem.type == "Bar":
                    domain_dict[DOMAIN_BAR].append(physElem)

                # append Surface to main Domain
                domain_dict[DOMAIN].append(physElem)

                # # append Surface to rotorMoving Domain (rotorMoving also
                # # includes movingband lines!)
                # domainMoving.append(physElem)

            ## GEOTYPE LINE:
            elif geoType == Line:
                # MB zuweisen
                if physElem.type == "MovingBand":
                    domain_dict[DOMAIN_MOVINGBAND].append(physElem)
                    if physElem.auxiliary:
                        domain_dict[DOMAIN_MOVINGBAND_AUX].append(physElem)

                    # domainMoving.append(physElem)
                    # # continue after because it can't be any other
                    # # physicalElement type
                    continue

                if physElem.type == "PrimaryLine":
                    domain_dict[DOMAIN_PRIMARY].append(physElem)
                    continue

                if physElem.type == "SlaveLine":
                    domain_dict[DOMAIN_SECONDARY].append(physElem)
                    continue

                if physElem.type == "LimitLine":
                    domain_dict[DOMAIN_LIMIT].append(physElem)
        return domain_dict

    @property
    def movingBand(self) -> List[MovingBand]:
        """Getter of MovingBand physical elements

        Returns:
            List[MovingBand]: _description_
        """
        domainMB = self._mb
        return domainMB.physicals

    @property
    def movingBandRadius(self) -> float:
        """determine the moving band radius.
        This is done by checking the radius of all moving band PhysicalElements for equality.

        Returns:
            float: Moving band radius in [m]

        Raises:
            ValueError: If there are no moving band objects.
            ValueError: If radius of different moving band arcs is not equal.
        """
        physicalMBList = self.movingBand
        if physicalMBList:
            mbRadius = physicalMBList[0].radius
            for physicalMB in physicalMBList:
                if abs(physicalMB.radius - mbRadius) > DEFAULT_GEO_TOL:
                    raise (
                        ValueError(
                            "Moving band got arc objects with different Radius:\n"
                            + f"Radius MB_0: {mbRadius}\n"
                            + f"Radius {physicalMB.name}: {physicalMB.radius}\n"
                        )
                    )
            return mbRadius
        else:
            raise (
                ValueError(
                    "Could not determine movingband radius: No movingband objects in the rotor."
                )
            )

    @property
    def inner_radius(self) -> float:
        """determine the most inner radius.
        This is done by checking the domain InnerLimit for the smallest radius.

        Returns:
            float: Most inner radius in meter.
        """
        # if _domainInnerLimit is empty, the most inner point is at (0,0,0)
        inner_limits = self._domainInnerLimit.physicals
        if not inner_limits:
            # no inner limit
            return 0.0
        else:
            r_in = inner_limits[0].geo_list[0].points[0].radius
            for phys in inner_limits:
                for geo in phys.geo_list:
                    if isinstance(geo, Line):
                        for p in geo.points:
                            if p.radius < r_in:
                                r_in = p.radius
        return r_in

    # def getMovingBand(self) -> List[AirGap]:
    #     """get the MovingBand physical elements"""
    #     domainMB = self._mb
    #     return domainMB.physicals

    def plot(self, fig=None, symFactor: int = None, **kwargs) -> None:
        """
        2D Line plot of the rotor physical elements

        Args:
            fig (matplotlib.Figure): Figure object to plot rotor on. If None is given, the
            function will automatically create one. Defaults to None.
            symFactor (int): If symmetry factor is given, the plot will be cutted to the
            correspoinding symmmetry (neglecting auxilliary moving band)
            **kwargs

        Default kwargs:
            linewidth: 0.5
            marker: "."
            markersize: 1
        """
        if "linewidth" not in kwargs:
            kwargs["linewidth"] = 0.5
        if "marker" not in kwargs:
            kwargs["marker"] = "."
        if "markersize" not in kwargs:
            kwargs["markersize"] = 1

        if fig is None:
            fig, axis = plt.subplots()
            fig.set_dpi(300)
            axis.set_aspect("equal", adjustable="box")
        kwargs["fig"] = fig
        for phys in self.physicalElements:
            for geoElem in phys.geo_list:
                geoElem.plot(**kwargs)
        if symFactor:
            radius = self.movingBandRadius
            if symFactor == 4:
                lim = -0.01 * radius
                axis.set_xlim(left=lim)
                axis.set_ylim(bottom=lim)
        return fig, axis

    def setFunctionMesh(
        self,
        basisMeshsize: float = None,
        meshGainFactor: float = None,
        functionType: Literal["linear", "quad"] = None,
    ):
        """add functional mesh size setting for machine if you don't want to
        specify mesh sizes individually. Mesh size is set to increase from
        airgap rotor inner radius. Maximal mesh size will be
        basisMeshsize * meshGainFactor.
        If basisMeshsize is not given, its set to
        2 * Pi * Rotor_Movingband_Radius / 360.
        If meshGainFactor is not given it will be derived from a empirically
        determined algorithm that rates the ratio of inner radius and basis
        mesh size. (This works best if basisMeshsize = Movingband hight!)

        Args:
            basisMeshsize (float, optional): Basis mesh size to use near the
                airgap (minimal mesh size).
                Defaults to 2 * Pi * Rotor_Movingband_Radius / 360.
            meshGainFactor (float): Gain factor for mesh size from airgap to
                outer machine limit. Defaults to (r_in / basisMeshsize / 3) or 30.
            functionType (Literal[&quot;linear&quot;, &quot;quad&quot;]):
                linear or quadratic function for mesh size. Defaults to linear
        """
        self.logger.debug("Started automatic mesh generation on rotor.")
        # get most inner radius
        r_in = self.inner_radius
        if not basisMeshsize:
            # get max. outer radius = moving band radius:
            basisMeshsize = 2 * pi * self.movingBandRadius / 360
            self.logger.debug(
                "Setting basis mesh size to 2 * pi * self.movingBandRadius / 360 = %.3e",
                basisMeshsize,
            )
        # set mesh gain factor to empirically developed default
        if not meshGainFactor:
            if r_in / basisMeshsize > 60:
                meshGainFactor = r_in / basisMeshsize / 3
            else:
                meshGainFactor = 30
            self.logger.debug(
                "Setting mesh gain factor to = %.1f",
                meshGainFactor,
            )
        if functionType == "linear" or functionType == None:
            self._set_linear_mesh(meshGainFactor, basisMeshsize)
        else:
            self._set_quad_mesh(meshGainFactor, basisMeshsize)
        gmsh.model.occ.synchronize()

    def _get_points(self) -> list[GmshPoint]:
        """Get a list of currently available gmsh points from gmsh model belonging to a
        stator physical element geometry.

        Returns:
            list[GmshPoint]: List of points belonging to stator physicals
        """
        phys_dim_tags = get_dim_tags(self.physicalElements)
        p_tags = get_point_tags(phys_dim_tags)
        return [GmshPoint(tag=p_tag) for p_tag in p_tags]

    def _set_linear_mesh(self, meshGainFactor: float, basisMeshsize: float):
        # calculate linear mesh size functions (ax+b)
        self.logger.debug("Setting linear mesh on rotor.")
        a1 = (1 - meshGainFactor) / self.movingBandRadius
        b1 = meshGainFactor
        # a2 = (meshGainFactor - 1) / (self.movingBandRadius - self.inner_radius)
        # b2 = meshGainFactor - a2 * self.movingBandRadius
        for point in self._get_points():
            rP = point.radius
            # if rP < rMb: # == rotor is allways true
            # meshSizeFaktor = (a1*rP+b1)
            pMeshSize = (a1 * rP + b1) * basisMeshsize
            point.meshLength = pMeshSize

    def _set_quad_mesh(self, meshGainFactor: float, basisMeshsize: float):
        self.logger.debug("Setting quadratic mesh on rotor.")
        # calculate function coefficients for ax^2+bx+c
        # c = meshGainFactor
        # b = -2 * c / self.inner_radius
        # a = -b / 2 / self.inner_radius
        r_in = self.inner_radius
        r_mb = self.movingBandRadius
        f1 = r_in**2 - 2 * r_in * r_mb + r_mb**2
        a = (meshGainFactor - 1) / f1
        b = -2 * a * r_mb
        c = (r_mb**2 * (meshGainFactor - 1)) / f1
        for point in self._get_points():
            rP = point.radius
            # faktor = 4770*rP**2 - 430 * rP + 10 # poly 2 fit
            gain_factor = (a * rP**2 + b * rP + c) + 1
            gain_factor = 1 if gain_factor < 1 else gain_factor
            point.meshLength = gain_factor * basisMeshsize

    def addToScript(self, script):
        """Mit addToScript wird der Rotor zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
        Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script)
        verwendet werden.

        Args:
            script (_type_): _description_
        """
        self._domainS.addToScript(script)
        self._domainM.addToScript(script)
        self._domainC.addToScript(script)
        self._mb.addToScript(script)
        self._domain.addToScript(script)
        self._domainL.addToScript(script)
        self._domainNL.addToScript(script)
        self._rotorMoving.addToScript(script)
        self._mbBaux.addToScript(script)
        self._domainAirGap.addToScript(script)
        self._domainPrimary.addToScript(script)
        self._domainSlave.addToScript(script)
        self._domainInnerLimit.addToScript(script)
