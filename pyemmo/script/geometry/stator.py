from typing import Dict, List, Union
from matplotlib import pyplot as plt
from numpy import pi, sign
from swat_em import datamodel
from .line import Line
from .movingBand import MovingBand
from .airGap import AirGap
from .physicalElement import PhysicalElement
from .slot import Slot
from .surface import Surface
from .domain import Domain
from ..material.electricalSteel import ElectricalSteel

# from ... import calc_phaseangle_starvoltageV2


# analyse.calc_phaseangle_starvoltage = calc_phaseangle_starvoltageV2
###
# Eine Instanz der Klasse Stator beschreibt den Stator eine elektrische Maschine im dreidimensionalen Raum.
# Diese Klasse wird in Verbindung mit der Klasse machineAllType verwendet.
# Um welchen Type Maschine es sich handelt, definiert der Nutzer selbst, durch die Definition seiner Physical Elements.
# Diese Klasse sollte man nur verwenden, wenn die Geometrie der Maschine als Import (bspw. Step) weiter verarbeitet wird.
# Für die Verwendung des Baukastens, ist die Spezifizierung der Maschine zunächst sinnvoll.
# Hierfür sollte man deshalb spezifische Klassen bspw. machineSPMSM (für Oberflächenmagnete) benutzen und die dazugehörige Klasse StatorSPMSM verwenden.
###
class Stator(object):
    def __init__(
        self,
        nbrSlots: int,
        physicalElements: List[PhysicalElement] = list(),
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
        self.name = name if name else "Stator"  # name of the stator
        self.physicalElements = physicalElements
        self.nbrSlots = nbrSlots
        self.axialLength = axLen  # active axial length
        self.winding = winding
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
        if isinstance(nbrSlots, int):
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
    def axialLength(self, axLen: Union[float, int]) -> None:
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
    def physicalElements(self) -> List[PhysicalElement]:
        """Getter of PhysicalElements-list"""
        return self._physicalElements

    @physicalElements.setter
    def physicalElements(self, physicalElementsList: List[PhysicalElement]) -> None:
        """Setter of PhysicalElement-List

        Args:
            physicalElementsList (List[PhysicalElement]): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        if isinstance(physicalElementsList, List):
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

    def addPhysicalElements(self, physicalElementList: List[PhysicalElement]):
        """Append PhysicalElements to the stator and recreate domains"""
        if type(physicalElementList) == list:
            for physicalElem in physicalElementList:
                if physicalElem not in self._physicalElements:
                    self._physicalElements.append(physicalElem)
            self._createDomainForStator()  # recreate domains for stator with new elements
        else:
            raise ValueError(f"Argument 'physicalElementList' was not type list!")

    @property
    def slots(self) -> List[Slot]:
        """getSlots returns a list of physical elements of type slot in stator.physicalElementList.
        The List is sortet in circumferderal (mathematically positive) direction so the first slot in the list is the one closest to the x-axis

        Returns:
            List[Slot]: List of slots
        """
        physicalElements = self.physicalElements
        slotList: List[Slot] = []
        for physElem in physicalElements:
            if physElem.type == "Slot":
                slotList.append(physElem)
        slotList.sort(key=Slot.getRadialPosition)
        return slotList

    @property
    def movingBand(self) -> List[MovingBand]:
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

    def _createDomainForStator(self):
        """Automatische Zuweisung der PhysicalElements zu den passenden Domainen"""
        # Set winding parameters in slots
        (layout, strLayout, colorLayout) = self.winding.get_layers()
        for slotPos, slot in enumerate(self.slots):
            if self.winding.get_num_layers() == 2:
                layer = (slotPos + 1) % 2  # alternate layers
                slotIDLayout = int(
                    slotPos / 2 + (((-1) ** slotPos) - 1) / 4
                )  # create row like: 0,0,1,1,2,2,3,3,...
            else:
                layer = 0  # there is only one layer
                slotIDLayout = slotPos

            slot.windDirection = sign(layout[layer, slotIDLayout])
            slot.phase = (abs(layout[layer, slotIDLayout]) - 1) * 2 * pi / 3
            slot.nbrTurns = self.winding.get_turns()

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

        ###DomainAirGap beinhaltet alle Physical Elements, die einen Luftspalt auf der Statorseite (Luftspalt bis zum Moving Band) beschreiben.
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
    def sortPhysicals(self) -> Dict[str, List[PhysicalElement]]:
        """Create a dict with the physical elements sorted into different domains with domain names as keys
            The dict will look like
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
        phy_domainS: List[Slot] = []  # Eingeprägte Ströme
        phy_domainLam = []  # lamination
        phy_domainC = []  # Leitende Flächen z. B. Stäbe ASM
        phy_domainCC = []  # alle elektrisch nicht leitenden Flächen
        mb_all: List[MovingBand] = []  # Moving Band
        phy_domain = []  # Alle Flächen
        phy_domainNL = []  # Alle nicht linearen Flächen
        phy_domainL = []  # Alle linearen Flächen
        phy_airgap: List[AirGap] = []  # Luftspalt im Rotor

        phy_primaryLine = []  # Teilmodell primarykante
        phy_slaveLine = []  # Teilmodell Slavekante
        limit_Line = []
        for physicalElement in self._physicalElements:
            geoType = physicalElement.geoElementType
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
                    if material.isLinear():
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
            for geoElem in phys.geometricalElement:
                geoElem.plot(
                    fig=fig,
                    linewidth=linewidth,
                    marker=marker,
                    markersize=markersize,
                )
        lim = 0.01 * self.movingBandRadius
        ax.set_xlim(left=-lim)
        ax.set_ylim(bottom=-lim)

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
