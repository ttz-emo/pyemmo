from cmath import pi
from matplotlib import pyplot as plt
from types import SimpleNamespace
from typing import Dict, List, Literal, Union

from .physicalElement import PhysicalElement
from .surface import Surface, Point, Line
from .domain import Domain
from .rotor import Rotor
from .stator import Stator
from ...script import default_param_dict


###
# Eine Instanz der Klasse MachineAllType beschreibt eine elektrische Maschine im dreidimensionalen Raum.
# Um welchen Type Maschine es sich handelt, definiert der Nutzer selbst, durch die Definition seiner Physical Elements.
# Ist z. B. ein Objekt der Klasse Magnet (Unterklasse von PhysicalElement) vorhanden, werden die Domaine in rotor.py und stator.py automatisch für eine PMSM vorbereitet.
# Für die Verwendung des Baukastens, ist die Spezifizierung der Maschine sinnvoll.
# Hierfür sollte man deshalb bspw. die Klasse machineSPMSM (für Oberflächenmagnete) benutzen.
###
class MachineAllType(object):
    def __init__(
        self,
        nbrPolePairs: Union[int, float],
        symmetryFactor: int,
        rotor: Rotor,
        stator: Stator,
        name: str = "",
    ):
        """
        Constructor of class Machine
        Args:
            nbrPolePairs:   Union[int,float]
            rotor:          Rotor
            stator:         Stator
            name:           str = ""

        Returns:

        Raises:
            Nothing
        """
        ###Name des Objektes.
        self._name = name if name else "machine"
        self._nbrPolePairs = nbrPolePairs
        self._symmetryFactor = symmetryFactor
        ###Objekt der Klasse Rotor.
        self._rotor = rotor
        ###Objekt der Klasse Stator.
        self._stator = stator
        if rotor and stator:
            self.createMachineDomains()

    def getSimParams(self) -> SimpleNamespace:
        """
        Return geometical simulation parameters as SimpleNamespace
        - SYMMETRY_FACTOR
        - L_AX_R
        - L_AX_S
        - NBR_POLE_PAIRS
        - NBR_TURNS_IN_FACE
        - R_AIRGAP
        """
        paramDict = default_param_dict.GEO
        paramDict.SYMMETRY_FACTOR = self.symmetryFactor
        paramDict.L_AX_R = self.rotor.axialLength
        paramDict.L_AX_S = self.stator.axialLength
        paramDict.NBR_POLE_PAIRS = self.NbrPolePairs
        paramDict.NBR_SLOTS = self.stator.NbrSlots
        paramDict.NBR_TURNS_IN_FACE = (
            self.stator.winding.get_turns() / 2
        )  # divide by two because there are allways two slot sides
        paramDict.R_AIRGAP = self.rotor.movingBand[0].radius
        return paramDict

    def createMachineDomains(self) -> None:
        """Create the different Machine Domains"""
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
        ###mbRotor beinhaltet alle Physical Elements, die eine Moving Band auf der Rotorseite beschreiben.
        self._mbRotor = Domain("MB_Rotor", rotor._mb.physicals)
        ###mbStator beinhaltet alle Physical Elements, die eine Moving Band auf der Statorseite beschreiben.
        self._mbStator = Domain("MB_Stator", stator._mb.physicals)
        ###domain beinhaltet alle Physical Elements, die die elektrische Maschine beschreiben.
        self._domain = Domain(
            "Domain",
            rotor._domain.physicals + stator._domain.physicals,
        )
        ###domainL beinhaltet alle Physical Elements, die ein lineares Material besitzen.
        self._domainL = Domain(
            "DomainL",
            rotor._domainL.physicals + stator._domainL.physicals,
        )
        ###domainNL beinhaltet alle Physical Elements, die ein nicht lineares Material besitzen.
        self._domainNL = Domain(
            "DomainNL",
            rotor._domainNL.physicals + stator._domainNL.physicals,
        )

        ###rotorMoving beinhaltet alle Physical Elements, die während der Simulation rotiert werden müssen (Rotor).
        self._rotorMoving = Domain("Rotor_Moving", rotor._rotorMoving.physicals)
        ###mbBaux beinhaltet alle Hilfslinien des MovingBands (Ergänzung zum Vollkreis), die wegen der Symmetrie ergänzt werden mussten. MovingBand auf der Rotorseite muss ein vollständiger Kreis beschreiben.
        self._mbBaux = Domain("Rotor_Bnd_MBaux", rotor._mbBaux.physicals)
        ###DomainAirGapRotor beinhaltet alle Physical Elements, die einen Luftspalt auf der Rotorseite (Luftspalt bis zum Moving Band) beschreiben.
        self._domainAirGapRotor = Domain("Rotor_Airgap", rotor._domainAirGap.physicals)
        ###DomainAirGapStator beinhaltet alle Physical Elements, die einen Luftspalt auf der Statorseite (Luftspalt ab dem Moving Band bis Statorinnenseite) beschreiben.
        self._domainAirGapStator = Domain(
            "Stator_Airgap", stator._domainAirGap.physicals
        )

        if (
            len(self._rotor._domainPrimary.physicals + stator._domainPrimary.physicals)
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
    def symmetryFactor(self) -> int:
        """Getter of Symmetry Factor

        Returns:
            int: Symmetry Factor
        """
        return self._symmetryFactor

    @symmetryFactor.setter
    def symmetryFactor(self, symFactor: int):
        """Setter for Symmetry Factor

        Args:
            symFactor (int): Symmetry Factor
        """
        assert type(symFactor) == int
        self._symmetryFactor = symFactor

    @property
    def NbrPolePairs(self) -> int:
        """Getter of number of pole pairs"""
        return self._nbrPolePairs

    @NbrPolePairs.setter
    def setNbrPolePairs(self, nbrPolePairs: Union[int, float]) -> None:
        """Setter of number of pole pairs

        Args:
            nbrPolePairs (Union[int, float]): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        
        if isinstance(nbrPolePairs, int):
            self._nbrPolePairs = nbrPolePairs
            return None
        elif isinstance(nbrPolePairs, float):
            if nbrPolePairs.is_integer():
                self._nbrPolePairs = int(nbrPolePairs)
                return None
        else:
            raise TypeError(
                f"Given number of pole pairs was not an integer (p={nbrPolePairs})"
            )

    @property
    def rotor(self) -> Rotor:
        """Get the rotor object of the machine"""
        return self._rotor

    @property
    def stator(self) -> Stator:
        """Get the stator object of the machine"""
        return self._stator

    @property
    def domains(self) -> List[Domain]:
        """Return all Domains of the machine as list"""
        domainList: List[Domain] = list()
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
    def primaryLines(self) -> List[Line]:
        """get a list of primary lines of rotor and stator

        Returns:
            List[Line]: list of primary line geometrical elements
        """
        rotorDict = self.rotor.sortPhysicals()
        statorDict = self.stator.sortPhysicals()
        physicalPrimeLines = rotorDict["primary"] + statorDict["primary"]
        primeLines: List[Line] = list()
        for physicalPrimeLine in physicalPrimeLines:
            if physicalPrimeLine.geoElementType == Line:
                primeLines.extend(physicalPrimeLine.geometricalElement)
            else:
                raise (
                    TypeError(
                        f"Physical Element (Primary Line) must only contain Line objects!"
                    )
                )
        return primeLines

    def getSecondaryLines(self) -> List[Line]:
        """get a list of secondary lines of rotor and stator

        Returns:
            List[Line]: list of secondary line geometrical elements
        """
        rotorDict = self.rotor.sortPhysicals()
        statorDict = self.stator.sortPhysicals()
        physicalSecLines = rotorDict["slave"] + statorDict["slave"]
        secondaryLines: List[Line] = list()
        for physicalSecLine in physicalSecLines:
            if physicalSecLine.geoElementType == Line:
                secondaryLines.extend(physicalSecLine.geometricalElement)
            else:
                raise (
                    TypeError(
                        f"Physical Element (Primary Line) must only contain Line objects!"
                    )
                )
        return secondaryLines

    @property
    def physicalElements(self) -> List[PhysicalElement]:
        """_summary_

        Returns:
            List[PhysicalElement]: _description_
        """
        physicals: List[PhysicalElement] = list()
        for physical in (
            self.stator.physicalElements
            + self.rotor.physicalElements
        ):
            physicals.append(physical)
        return physicals

    def setFunctionMesh(
        self,
        functionType: Literal["linear", "quad"],
        meshGainFactor: float,
        basisMeshsize: float = None,
    ):
        """add functional mesh size setting for machine if you don't want to specify mesh sizes individually. Mesh size is set to increase from airgap to both sides (rotor and stator). Maximal mesh size will be basisMeshsize * meshGainFactor.
        If basisMeshsize is not given, its set to 2*Pi* Rotor_Movingband_Radius / 360.

        Args:
            functionType (Literal[&quot;linear&quot;, &quot;quad&quot;]): linear or quadratic function for mesh size.
            meshGainFactor (float): Gain factor for mesh size from airgap to outer machine limit.
            basisMeshsize (float, optional): Basis mesh size to use near the airgap (minimal mesh size). Defaults to None = 2*Pi* Rotor_Movingband_Radius / 360.
        """
        rMb = self.rotor.movingBandRadius
        # get max. stator radius:
        rS = 0
        for phys in self.stator._domainOuterLimit.physicals:
            for geo in phys.geometricalElement:
                if isinstance(geo, Line):
                    for p in geo.points:
                        if p.radius > rS:
                            rS = p.radius
        if not basisMeshsize:
            basisMeshsize = 2 * pi * rMb / 360

        # calculate linear mesh size functions (ax+b)
        if functionType == "linear":
            a1 = (1 - meshGainFactor) / rMb
            b1 = meshGainFactor

            a2 = (meshGainFactor - 1) / (rS - rMb)
            b2 = meshGainFactor - a2 * rS
        elif functionType == "quad":
            # calculate function coefficients for ax^2+bx+c
            c = meshGainFactor
            b = -2 * c / rMb
            a = -b / 2 / rMb
        else:
            mssg = f"Unknown function specifier '{functionType}' for functional mesh."
            raise (ValueError(mssg))
        for physical in self.physicalElements:
            for geo in physical.geometricalElement:
                points: List[Point] = []
                if isinstance(geo, Surface):
                    for curve in geo.curve:
                        points.extend(curve.points)
                # All curves should belong to a surface...
                # else:
                #     points.extend(geo.getPoints())
                for point in points:
                    rP = point.radius
                    if functionType == "linear":
                        if rP < rMb:
                            # meshSizeFaktor = (a1*rP+b1)
                            pMeshSize = (a1 * rP + b1) * basisMeshsize
                        else:
                            pMeshSize = (a2 * rP + b2) * basisMeshsize
                    elif functionType == "quad":
                        # faktor = 4770*rP**2 - 430 * rP + 10 # poly 2 fit
                        faktor = (a * rP**2 + b * rP + c) + 1
                        faktor = 1 if faktor < 1 else faktor
                        pMeshSize = faktor * basisMeshsize
                    point.meshLength = pMeshSize

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
            ax.set_aspect("equal", adjustable="box")
        domains = self.domains
        for domain in domains:
            for phys in domain.physicals:
                for geoElem in phys.geometricalElement:
                    geoElem.plot(
                        fig=fig,
                        linewidth=linewidth,
                        marker=marker,
                        markersize=markersize,
                    )
