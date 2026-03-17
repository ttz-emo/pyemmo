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
from __future__ import annotations

import logging
from typing import Literal

import gmsh
import numpy as np
from matplotlib import pyplot as plt
from swat_em import datamodel

from .domain import Domain
from .geometry.line import Line
from .geometry.surface import Surface
from .gmsh.gmsh_point import GmshPoint
from .gmsh.utils import get_dim_tags, get_point_tags
from .material.electricalSteel import ElectricalSteel
from .physicals.airgap import AirGap
from .physicals.movingband import MovingBand
from .physicals.physicalElement import PhysicalElement
from .physicals.slot import Slot

# from ... import calc_phaseangle_starvoltageV2


# analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltageV2
###
# Eine Instanz der Klasse Stator beschreibt den Stator eine elektrische Maschine im dreidimensionalen Raum.
# Diese Klasse wird in Verbindung mit der Klasse Machine verwendet.
# Um welchen Type Maschine es sich handelt, definiert der Nutzer selbst, durch die Definition seiner Physical Elements.
# Diese Klasse sollte man nur verwenden, wenn die Geometrie der Maschine als Import (bspw. Step) weiter verarbeitet wird.
# Für die Verwendung des Baukastens, ist die Spezifizierung der Maschine zunächst sinnvoll.
# Hierfür sollte man deshalb spezifische Klassen bspw. machineSPMSM (für Oberflächenmagnete) benutzen und die dazugehörige Klasse StatorSPMSM verwenden.
###
class Stator:
    def __init__(
        self,
        nbrSlots: int,
        physicalElements: list[PhysicalElement] = list(),
        name: str = "",
        axLen: float = 1.0,
        winding: datamodel = None,
    ):
        """
        Constructor of class Stator

        Args:
            nbrSlots (int): number of stator slots (Qs).
            physicalElements (List[PhysicalElement]): list of physical elements of the stator.
            name (str): name of the stator. Defaults to "".
            axLen (float): active axial length of stator lamination in meter. Defaults to 1.
            winding (swat_em.datamodel): winding object from swat_em module. Defaults to None.


        Returns:
            Stator: the stator object.

        Raises:
            Nothing
        """
        self.logger = logging.getLogger(__name__)
        self.name = name if name else "Stator"  # name of the stator
        self.nbrSlots = nbrSlots
        self.axialLength = axLen  # active axial length
        self.winding = winding
        self.physicalElements = physicalElements
        # only generate domains if they are physical elements
        if self.physicalElements:
            self._createDomainForStator()

    @property
    def name(self) -> str:
        """Getter of stator name"""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Setter of stator name

        Args:
            name (str): _description_

        Raises:
            TypeError: _description_
        """
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError(f"Given name was not type str, but '{type(name)}'")

    @property
    def nbrSlots(self) -> int:
        """Getter of number of slots (Qs)"""
        return self._nbrSlots

    @nbrSlots.setter
    def nbrSlots(self, nbrSlots: int) -> None:
        """Setter for the Number of Slots

        Args:
            nbrSlots (int): _description_

        Raises:
            TypeError: _description_
        """
        if isinstance(nbrSlots, (int, float)):
            self._nbrSlots = nbrSlots
        else:
            raise TypeError(
                f"Given number of slots was not Type int but {type(nbrSlots)}."
            )

    @property
    def axialLength(self) -> float:
        """Getter of axLen [m]"""
        return self._axLen

    @axialLength.setter
    def axialLength(self, axLen: float | int) -> None:
        """Setter for axLen [m]

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
    def physicalElements(self) -> list[PhysicalElement]:
        """Getter of PhysicalElements-list"""
        return self._physicalElements

    @physicalElements.setter
    def physicalElements(self, physicalElementsList: list[PhysicalElement]) -> None:
        """Setter of PhysicalElement-List

        Args:
            physicalElementsList (List[PhysicalElement]): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        if isinstance(physicalElementsList, list):
            self._physicalElements = physicalElementsList
            self._createDomainForStator()
            return None
        elif isinstance(physicalElementsList, PhysicalElement):
            self._physicalElements = [physicalElementsList]
            self._createDomainForStator()
            return None
        else:
            raise TypeError(
                f"Given attribute physicalElementList was not type List or PhysicalElement but {type(physicalElementsList)}."
            )

    def addPhysicalElements(self, physicalElementList: list[PhysicalElement]):
        """Append PhysicalElements to the stator and recreate domains"""
        if type(physicalElementList) == list:
            for physicalElem in physicalElementList:
                if physicalElem not in self._physicalElements:
                    self._physicalElements.append(physicalElem)
            self._createDomainForStator()  # recreate domains for stator with new elements
        else:
            raise ValueError(f"Argument 'physicalElementList' was not type list!")

    @property
    def slots(self) -> list[Slot]:
        """getSlots returns a list of physical elements of type slot in stator.physicalElementList.
        The List is sortet in circumferderal (mathematically positive) and radial direction so the
        first slot in the list is the one closest to the x-axis

        Returns:
            List[Slot]: List of slots
        """
        physicalElements = self.physicalElements
        slotList: list[Slot] = []
        for physElem in physicalElements:
            if physElem.type == "Slot":
                slotList.append(physElem)
        # if self.winding.get_coilspan()<1:
        #     # tooth coil winding -> radial position sort
        slotList.sort(key=Slot.get_circumferential_position)
        wind = self.winding
        if wind.get_num_layers() == 2:
            layout = np.array(wind.get_phases())
            # check if first and second layer are not equal
            if (
                not np.array_equal(layout[0, 0, :], layout[0, 1, :])
                and wind.get_coilspan() > 1
            ):
                # Distributed winding with differnet layers
                for i in range(wind.get_num_slots()):
                    # sort the two slot sides separately in upper and lowee slot
                    slotsides = slotList[2 * i : 2 * i + 2]
                    # reverse because outer slot has index 0 according to swat-em
                    slotsides.sort(key=Slot.get_radial_position, reverse=True)
                    slotList[2 * i : 2 * i + 2] = slotsides
        return slotList

    @property
    def movingBand(self) -> list[MovingBand]:
        """get the MovingBand physical elements"""
        domainMB = self._mb
        return domainMB.physicals

    @property
    def movingBandRadius(self) -> float:
        """Getter for the Moving Band radius

        Returns:
            float: Moving Band radius
        """
        physicalMBList = self.movingBand
        if physicalMBList:
            mbRadius = physicalMBList[0].radius
            for physicalMB in physicalMBList:
                if physicalMB.radius != mbRadius:
                    raise (
                        ValueError(
                            f"Rotor Movingband domain got Circle Arc objects with different Radius:\n"
                            + f"Radius MB_0: {mbRadius}\n"
                            + f"Radius {physicalMB.name}: {physicalMB.radius}\n"
                        )
                    )
            return mbRadius
        else:
            raise (
                ValueError(
                    f"Could not determine movingband radius, because there were no movingband objects in the rotor."
                )
            )

    @property
    def outer_radius(self) -> float:
        """Stator most outer radius determined from domain OuterLimit

        Returns:
            float: Most outer radius in meter.
        """
        if not self.physicalElements:
            raise RuntimeError(
                "Cannot determine outer radius since there are no physical elements in Stator."
            )
        outer_radius = 0.0
        for phys in self._domainOuterLimit.physicals:
            for geo in phys.geo_list:
                if isinstance(geo, Line):
                    for p in geo.points:
                        if p.radius > outer_radius:
                            outer_radius = p.radius
        return outer_radius

    @property
    def winding(self) -> datamodel:
        """Get the Swat-em datamodel object of the winding

        Returns:
            datamodel: swat-em winding object
        """
        return self._winding

    @winding.setter
    def winding(self, winding: datamodel):
        """Set the winding of the stator.

        Args:
            winding (datamodel): swat_em datamodel object of the winding.

        Raises:
            ValueError: If number of slots of winding and stator are missmatching
            TypeError: If winding is not type swat_em.datamodel
        """
        if isinstance(winding, datamodel):
            if winding.get_num_slots() == self.nbrSlots:
                try:
                    if (
                        not winding.get_fundamental_windingfactor()
                    ):  # if winding was analysed before, the windingfactors are allready calculated. Otherwise the function returns None and the winding has to be analysed!
                        winding.analyse_wdg()
                except Exception as exc:
                    raise ValueError(
                        "Winding could not be generated! It might be missing some parameters. See SWAT-EM documentation for more infos!"
                    ) from exc
                self._winding = winding
                return None
            else:
                raise (
                    ValueError(
                        f"Given Winding object (Qs={winding.get_num_slots()}) doesn't have the same number of slots as the stator (Qs={self.nbrSlots})."
                    )
                )
        else:
            raise (
                TypeError(
                    f"Winding was not type swat_em.datamodel, but {type(winding)}."
                )
            )

    def _setWindingParamInSlots(self):
        """
        This function sets the winding parameters in the ``Slot`` objects from the
        SWAT-EM winding layout in ``Stator.winding``.
        By determining the slot sequence and slot side the winding parameters can be
        set:

            - Winding direction: + or -
            - Winding phase: u, v or w
            - Number of winding turns

        """
        # get_layers returns right/upper and left/lower slot side as
        # list of phases (1,2 or 3) and winding direction (+ or -)
        (layout, _, _) = self.winding.get_layers()
        for slotPos, slot in enumerate(self.slots):
            # Slot list is sorted in circumferential direction
            if self.winding.get_num_layers() == 2:
                # if there are two layers, we have to alternate the right/left
                # or outer/inner layer, while keeping the slot number
                # (slotIDLayout) constant.
                # E.g. the first slot side in the first slot gets layer=0,
                # slotIDLayout=0; second slot gets layer=1, slotIDLayout=0;...
                # BUG:  Sorting of slots by circumferential position probably
                #       does not work for outer/inner slot division
                layer = slotPos % 2  # alternate layers
                # create row like: 0,0,1,1,2,2,3,3,...
                slotIDLayout = int(slotPos / 2 + (((-1) ** slotPos) - 1) / 4)
            else:
                layer = 0  # there is only one layer
                slotIDLayout = slotPos
            # Finally get winding direction and phase number (0,1,2 = u,v,w)
            slot.windDirection = np.sign(layout[layer, slotIDLayout])
            # recalculate phase angle in rad
            slot.phase = (abs(layout[layer, slotIDLayout]) - 1) * 2 * np.pi / 3
            slot.nbrTurns = self.winding.get_turns()
            slot.setColor()

    def _createDomainForStator(self):
        """Automatische Zuweisung der PhysicalElements zu den passenden Domainen"""
        self._setWindingParamInSlots()
        allPhy = self.sortPhysicals()
        ###DomainS beinhaltet alle Physical Elements, die bestromt werden.
        self._domainS = Domain("DomainS_Stator", allPhy["domainS"])
        ###DomainC beinhaltet alle Physical Elements, die leitend sind.
        self._domainC = Domain("DomainC_Stator", allPhy["domainC"])
        ###mb beinhaltet alle Physical Elements, die eine Moving Band auf der Statorseite beschreiben.
        self._mb = Domain("MB_Stator", allPhy["mb_all"])
        ###domain beinhaltet alle Physical Elements, die den gesamten Stator beschreiben.
        self._domain = Domain("Domain_Stator", allPhy["domain"])
        ###domainL beinhaltet alle Physical Elements, die ein lineares Material besitzen.
        self._domainL = Domain("DomainL_Stator", allPhy["domainL"])
        ###domainNL beinhaltet alle Physical Elements, die ein nicht lineares Material besitzen.
        self._domainNL = Domain("DomainNL_Stator", allPhy["domainNL"])

        ### DomainAirGap contains all physicals, that create the airgap are containing
        # the stator movingband.
        if not allPhy["airGap"]:
            self.logger.warning(
                "No physical elements for stator airgap domain. "
                "Make sure your airgap physical surface is defined as AirGap object!"
            )
        self._domainAirGap = Domain("Stator_Airgap", allPhy["airGap"])
        ###primarykante vom Stator.
        self._domainPrimary = Domain("PrimaryRegion_Stator", allPhy["primary"])
        ###Slavekante vom Stator.
        self._domainSlave = Domain("SlaveRegion_Stator", allPhy["slave"])
        ###Außengrenze der elektrischen Maschine (Rotoraußenkante).
        self._domainOuterLimit = Domain("OuterLimit_Stator", allPhy["limit"])

        ###DomainLam beinhaltet alle Physical Elements, die geblecht sind.
        self._domainLam = Domain("DomainLam_Stator", allPhy["domainLam"])

    ###Sortierfunktion der PhysicalElements.
    def sortPhysicals(self) -> dict[str, list[PhysicalElement]]:
        """Create a dict with the physical elements sorted into different domains with domain names as keys
            The dict will look like

            .. code-block:: python

                {
                    "domainS": phy_domainS,
                    "domainLam": phy_domainLam,
                    "domainC": phy_domainC,
                    "domainCC": phy_domainCC,
                    "mb_all": mb_all,
                    "domain": phy_domain,
                    "domainNL": phy_domainNL,
                    "domainL": phy_domainL,
                    "airGap": phy_airgap,
                    "primary": phy_primaryLine,
                    "slave": phy_slaveLine,
                    "limit": limit_Line,
                }

        Raises:
            Exception: If material of a surface is unknown or None. Surface physical element must have material.

        Returns:
            Dict[str, List[PhysicalElement]]: dict with sorted physical elements
        """
        phy_domainS: list[Slot] = []  # Eingeprägte Ströme
        phy_domainLam = []  # lamination
        phy_domainC = []  # Leitende Flächen z. B. Stäbe ASM
        phy_domainCC = []  # alle elektrisch nicht leitenden Flächen
        mb_all: list[MovingBand] = []  # Moving Band
        phy_domain = []  # Alle Flächen
        phy_domainNL = []  # Alle nicht linearen Flächen
        phy_domainL = []  # Alle linearen Flächen
        phy_airgap: list[AirGap] = []  # Luftspalt im Rotor

        phy_primaryLine = []  # Teilmodell primarykante
        phy_slaveLine = []  # Teilmodell Slavekante
        limit_Line = []
        for physicalElement in self._physicalElements:
            geoType = physicalElement.geo_type
            if geoType == Surface:
                # domainC, domainL & domainNL
                material = physicalElement.material
                if material:
                    # if conductivity not None add to domainC
                    if material.conductivity:
                        phy_domainC.append(physicalElement)
                    else:
                        phy_domainCC.append(physicalElement)
                    # if material is linear
                    if material.linear:
                        phy_domainL.append(physicalElement)
                    else:
                        phy_domainNL.append(physicalElement)
                    # if material is laminated
                    if isinstance(material, ElectricalSteel):
                        phy_domainLam.append(physicalElement)
                else:
                    raise Exception(
                        f"physicalElement ({physicalElement.name}) of type Surface should have a material! Material is {material}"
                    )

                # domainS zuweisen
                if physicalElement.type == "Slot":
                    phy_domainS.append(physicalElement)
                    physicalElement.setColor()
                    continue

                # Stator airgap
                if physicalElement.type == "AirGap":
                    phy_airgap.append(physicalElement)

                # Stator lamination if not allready defined
                if physicalElement.type == "Lamination":
                    # pE could allready been added due to material
                    if physicalElement not in phy_domainLam:
                        phy_domainLam.append(physicalElement)

                phy_domain.append(physicalElement)  # append Surface to main Domain
            elif geoType == Line:
                # MB zuweisen
                if physicalElement.type == "MovingBand":
                    mb_all.append(physicalElement)
                    continue  # continue after because it cant be any other physicalElement type
                elif physicalElement.type == "PrimaryLine":
                    phy_primaryLine.append(physicalElement)
                    continue
                elif physicalElement.type == "SlaveLine":
                    phy_slaveLine.append(physicalElement)
                    continue
                elif physicalElement.type == "LimitLine":
                    limit_Line.append(physicalElement)

        sortedPhy = {
            "primary": phy_primaryLine,
            "slave": phy_slaveLine,
            "limit": limit_Line,
            "mb_all": mb_all,
            "airGap": phy_airgap,
            "domainS": phy_domainS,
            "domainLam": phy_domainLam,
            "domainC": phy_domainC,
            "domainCC": phy_domainCC,
            "domain": phy_domain,
            "domainNL": phy_domainNL,
            "domainL": phy_domainL,
        }

        return sortedPhy

    def plot(
        self,
        fig=None,
        linewidth=0.5,
        marker=".",
        markersize=1,
    ) -> None:
        """
        2D Line plot of the surface
        """
        if fig is None:
            fig, ax = plt.subplots()
            fig.set_dpi(300)
            ax.set_aspect("equal")
            # ax.set_aspect("equal", adjustable="box")
        for phys in self.physicalElements:
            for geoElem in phys.geo_list:
                geoElem.plot(
                    fig=fig,
                    linewidth=linewidth,
                    marker=marker,
                    markersize=markersize,
                )
        lim = 0.01 * self.movingBandRadius
        ax.set_xlim(left=-lim)
        ax.set_ylim(bottom=-lim)

    def setFunctionMesh(
        self,
        basisMeshsize: float = None,
        functionType: Literal["linear", "quad"] = None,
        meshGainFactor: float = None,
    ):
        """add functional mesh size setting for stator if you don't want to
        specify mesh sizes individually. Mesh size is set to increase from
        airgap to stator outer radius. Maximal mesh size will be
        basisMeshsize * meshGainFactor.
        If basisMeshsize is not given, its set to
        2 * Pi * Movingband_Radius / 360.

        Args:
            functionType (Literal[&quot;linear&quot;, &quot;quad&quot;]):
                linear or quadratic function for mesh size.
            meshGainFactor (float): Gain factor for mesh size from airgap to
                outer machine limit.
            basisMeshsize (float, optional): Basis mesh size to use near the
                airgap (minimal mesh size).
                Defaults to 2 * Pi * Movingband_Radius / 360.
        """
        self.logger.debug("Started automatic mesh generation on stator.")
        # get max. outer radius:
        r_out = self.outer_radius
        if not basisMeshsize:
            basisMeshsize = 2 * np.pi * self.movingBandRadius / 360
            self.logger.debug(
                "Setting basis mesh size to 2 * np.pi * self.movingBandRadius / 360 = %.3e",
                basisMeshsize,
            )
        # set mesh gain factor to empirically developed default
        if not meshGainFactor:
            if r_out / basisMeshsize > 100:
                meshGainFactor = r_out / basisMeshsize / 20
                if not functionType:
                    functionType = "linear"
            else:
                meshGainFactor = 20
                if not functionType:
                    functionType = "quad"
            self.logger.debug(
                "Setting mesh gain factor to = %.1f",
                meshGainFactor,
            )
        if functionType == "linear":
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
        self.logger.debug("Setting linear mesh on stator.")
        # calculate linear mesh size functions (ax+b)
        a = (meshGainFactor - 1) / (self.outer_radius - self.movingBandRadius)
        b = meshGainFactor - a * self.outer_radius
        for point in self._get_points():
            rP = point.radius
            pMeshSize = (a * rP + b) * basisMeshsize
            point.meshLength = pMeshSize

    def _set_quad_mesh(self, meshGainFactor: float, basisMeshsize: float):
        """set mesh by parabolic function.

        Args:
            meshGainFactor (float): _description_
            basisMeshsize (float): _description_
        """
        self.logger.debug("Setting quadratic mesh on stator.")
        # calculate function coefficients for ax^2+bx+c
        r_mb = self.movingBandRadius
        c = meshGainFactor
        b = -2 * c / r_mb
        a = -b / 2 / r_mb
        for point in self._get_points():
            rP = point.radius
            # faktor = 4770*rP**2 - 430 * rP + 10 # poly 2 fit
            gain_factor = (a * rP**2 + b * rP + c) + 1
            gain_factor = 1 if gain_factor < 1 else gain_factor
            point.meshLength = gain_factor * basisMeshsize

    ###
    # Mit addToScript wird der Stator zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    ###
    def addToScript(self, script):
        self._domainS.addToScript(script)
        self._domainC.addToScript(script)
        self._mb.addToScript(script)
        self._domain.addToScript(script)
        self._domainL.addToScript(script)
        self._domainNL.addToScript(script)
        self._domainAirGap.addToScript(script)
        self._domainPrimary.addToScript(script)
        self._domainSlave.addToScript(script)
        self._domainOuterLimit.addToScript(script)
