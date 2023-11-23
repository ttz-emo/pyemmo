"""Module for Class Rotor"""
from typing import Dict, List, Union
from matplotlib import pyplot as plt
from .magnet import Magnet
from .movingBand import MovingBand
from .surface import Surface
from .line import Line
from .domain import Domain
from .physicalElement import PhysicalElement
from ..material.electricalSteel import ElectricalSteel
from ...definitions import DEFAULT_GEO_TOL


class Rotor:
    """Eine Instanz der Klasse Rotor beschreibt den Rotor eine elektrische Maschine im
    dreidimensionalen Raum. Diese Klasse wird in Verbindung mit der Klasse machineAllType
    verwendet. Um welchen Typ Maschine es sich handelt, definiert der Nutzer selbst, durch die
    Definition seiner Physical Elements. Diese Klasse sollte man nur verwenden, wenn die Geometrie
    der Maschine als Import (bspw. Step) weiter verarbeitet wird. Für die Verwendung des Baukastens,
    ist die Spezifizierung der Maschine zunächst sinnvoll. Hierfür sollte man deshalb spezifische
    Klassen bspw. machineSPMSM (für Oberflächenmagnete) benutzen und die dazugehörige Klasse
    RotorSPMSM verwenden.
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
            physicalElements (List[PhysicalElement]): List of PhysicalElement objects defining geometry and materials.
            name (str): Defaults to "".
            axLen (float): Active axial length of stator lamination in [m]. Defaults to 1.0

        Raises:
            Nothing
        """
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
        """Create a dict with the physical elements sorted into different domains with
        domain names as keys
            The dict will look like
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
        domainS = []  # Eingeprägte Ströme
        domainM = []  # Magnete
        domainLam = []  # Lamination (part with material specified lamination)
        domainC = []  # Leitende Flächen z. B. Stäbe ASM
        domainCC = []  # alle elektrisch nicht leitenden Flächen
        allMbLines = []  # Moving Band

        domain = []  # Alle Flächen
        domainNL = []  # Alle nicht linearen Flächen
        domainL = []  # Alle linearen Flächen

        domainMoving = []  # Alle Teile die sich drehen, inkl. Moving Band (alle)
        movingBandAux = []  # Bei Teilmodell -> die restlichen Moving Band
        domainAirgap = []  # Luftspalt im Rotor

        primaryLines = []  # Teilmodell primarykante
        slaveLines = []  # Teilmodell Slavekante
        limitLines = []  # Randlinien ohne Primär- und Sekundärkanten
        for physElem in self.physicalElements:
            geoType = physElem.geoElementType
            if geoType == Surface:
                # domainC, domainL & domainNL
                material = physElem.material
                if material:
                    # if conductivity not None add to domainC
                    if material.conductivity:
                        domainC.append(physElem)
                    else:
                        domainCC.append(physElem)
                    # if material is linear
                    if material.isLinear():
                        domainL.append(physElem)
                    else:
                        domainNL.append(physElem)
                    # if material is laminated
                    if isinstance(material, ElectricalSteel):
                        domainLam.append(physElem)
                else:
                    physName = physElem.name
                    raise RuntimeError(
                        f"No Material defined: ({physName})", f"Material is {material}"
                    )

                # domainM zuweisen
                if physElem.type == "Magnet":
                    magnet: Magnet = physElem
                    domainM.append(magnet)
                    # remove magnet from C or CC because assignment is done by getdp
                    if magnet in domainC:
                        domainC.remove(magnet)
                    elif magnet in domainCC:
                        domainCC.remove(magnet)
                    continue

                # domainS zuweisen
                if physElem.type == "Slot":
                    domainS.append(physElem)
                    continue

                # airgap
                if physElem.type == "AirGap":
                    domainAirgap.append(physElem)

                # Stator lamination if not allready defined
                if physElem.type == "Lamination":
                    # pE could allready been added due to material
                    if physElem not in domainLam:
                        domainLam.append(physElem)

                domain.append(physElem)  # append Surface to main Domain
                # append Surface to rotorMoving Domain (rotorMoving also includes movingband lines!)
                domainMoving.append(physElem)
            ## GEOTYPE LINE:
            elif geoType == Line:
                # MB zuweisen
                if physElem.type == "MovingBand":
                    allMbLines.append(physElem)
                    if physElem.auxiliary:
                        movingBandAux.append(physElem)

                    domainMoving.append(physElem)
                    continue  # continue after because it cant be any other physicalElement type

                if physElem.type == "PrimaryLine":
                    primaryLines.append(physElem)
                    continue

                if physElem.type == "SlaveLine":
                    slaveLines.append(physElem)
                    continue

                if physElem.type == "LimitLine":
                    limitLines.append(physElem)

        sortedPhy = {
            "primary": primaryLines,
            "slave": slaveLines,
            "limit": limitLines,
            "mb_all": allMbLines,
            "mb_Mbaux": movingBandAux,
            "airGap": domainAirgap,
            "rotor_moving": domainMoving,
            "domainS": domainS,
            "domainM": domainM,
            "domainLam": domainLam,
            "domainC": domainC,
            "domainCC": domainCC,
            "domain": domain,
            "domainNL": domainNL,
            "domainL": domainL,
        }

        return sortedPhy

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
            for geoElem in phys.geometricalElement:
                geoElem.plot(**kwargs)
        if symFactor:
            radius = self.movingBandRadius
            if symFactor == 4:
                lim = -0.01 * radius
                axis.set_xlim(left=lim)
                axis.set_ylim(bottom=lim)
        return fig, axis

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
