from ctypes import Union
from types import SimpleNamespace
from typing import Dict

from pydraft.script.geometry.machineAllType import MachineAllType
from ..script import default_param_dict
from ..script import Script
from .domain import Domain
from .rotorIPMSM import RotorIPMSM
from .statorSPMSM import StatorPMSM
from math import pi
import swat_em


class MachineIPMSM(MachineAllType):
    """IPMSM Class

    Args:
        simuParam (dict): dict with the essential machine parameters

        'analysisParameter':
    
        * 'symmetryFactor' : Integer,
        * 'nbrPolesTotal' : Integer,
        * 'nbrSlotTotal' : Integer,
        * 'timeMax' : Float,
        * 'timeStep' : Float,
        * 'analysisType' : String,
        * 'startPosition' : Float
    """
    def __init__(self, simuParam, name="Machine_IPMSM"):
        """Constructor of the class MachineIPMSM."""
        MachineAllType.__init__(
            self,
            nbrPolePairs=(simuParam["analysisParameter"]["nbrPolesTotal"] / 2),
            symmetryFactor=simuParam["analysisParameter"]["symmetryFactor"],
            rotor=None,
            stator=None,
            name=name,
        )
        ###Simulationsparameter gemäß der Eingabe.
        self._simuParam = simuParam
        # Calculate Poles and Slots for Model
        self._simuParam["analysisParameter"]["nbrPolesinModel"] = (
            self._simuParam["analysisParameter"]["nbrPolesTotal"]
            / self.getSymmetryFactor()
        )
        self._simuParam["analysisParameter"]["nbrSlotinModel"] = (
            self._simuParam["analysisParameter"]["nbrSlotTotal"]
            / self.getSymmetryFactor()
        )

    def getNbrPolesInModel(self):
        return int(self._simuParam["analysisParameter"]["nbrPolesinModel"])

    def getNbrPolePairs(self):
        """get the number of pole pairs

        Returns:
            int: the number of pole pairs of the IPMSM
        """
        simuParams = self._getSimuParamDict()
        nbrPolePairs = simuParams["analysisParameter"]["nbrPolesTotal"] / 2
        assert float(nbrPolePairs).is_integer()
        return nbrPolePairs

    def getSymmetryFactor(self):
        return int(self._symmetryFactor)

    def getStartPos(self):
        simuParams = self._getSimuParamDict()
        return simuParams["analysisParameter"]["startPosition"]

    def getRotor(self):
        """Get the rotor of the machine

        Returns:
            RotorIPMSM: rotor with internal permanent magnets
        """
        return self._rotor

    def getStator(self):
        """Get the stator of the machine

        Returns:
            Stator: Stator of the IMPSM
        """
        return self._stator

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
        paramDict.SYMMETRY_FACTOR = self.getSymmetryFactor()
        paramDict.L_AX_R = self.getRotor().getAxialLength()
        paramDict.L_AX_S = self.getStator().getAxialLength()
        paramDict.NBR_POLE_PAIRS = self.getNbrPolePairs()
        paramDict.NBR_SLOTS = self.getStator().getNbrSlots()
        slots = self.getStator().getSlots()
        nbrTurns = slots[0].nbrTurns
        slots.pop(0)
        for slot in slots:
            actNbrTurns = slot.nbrTurns
            if nbrTurns != actNbrTurns:
                raise ValueError(
                    f"Different number of turns in slots! {nbrTurns} != {actNbrTurns}"
                )
        paramDict.NBR_TURNS_IN_FACE = nbrTurns
        paramDict.R_AIRGAP = self.getRotor().getMovingBand()[0].radius
        return paramDict

    def _getSimuParamDict(self) -> Dict:
        """return the simulation parameter dict

        Returns:
            Dict: dict with simulation parameters. 
        
        Content of SimuParamDict under 'analysisParameter' is:
    
        * 'symmetryFactor' : Integer,
        * 'nbrPolesTotal' : Integer,
        * 'nbrSlotTotal' : Integer,
        * 'timeMax' : Float,
        * 'timeStep' : Float,
        * 'analysisType' : String,
        * 'startPosition' : Float
        """
        return self._simuParam

    def addRotorToMachine(self, laminationType: str, magnetType: str, axLen: float = 1):
        nbrPoles = self.getNbrPolePairs() * 2
        symFactor = self.getSymmetryFactor()
        angleGeoParts = 2 * pi / (nbrPoles) / 2  # half segment?
        userRot = self.getStartPos()
        # rotate half pole, because pole center is on x-axis
        startPosition = angleGeoParts + userRot
        nbrGeoParts = int(nbrPoles / symFactor) * 2  # half segment?

        self._rotor = RotorIPMSM(
            laminationType=laminationType,
            magnetType=magnetType,
            angleGeoParts=angleGeoParts,  # angle of one segment
            nbrGeoParts=nbrGeoParts,
            symmetryFactor=self._symmetryFactor,
            startPosition=startPosition,
            axLen=axLen,
        )
        return self._rotor

    def addStatorToMachine(
        self,
        laminationType: str,
        slotType: str,
        winding: swat_em.datamodel,
        axLen: float = 1,
    ):
        startPosition = (
            pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
            + self._simuParam["analysisParameter"]["startPosition"]
        )
        angleGeoParts = (
            pi
            / self._symmetryFactor
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
        )
        nbrGeoParts = self._simuParam["analysisParameter"]["nbrSlotinModel"] * 2
        statorSPMSM1 = StatorPMSM(
            laminationType=laminationType,
            slotType=slotType,
            nbrSlots=self._simuParam["analysisParameter"]["nbrSlotTotal"],
            angleGeoParts=angleGeoParts,
            nbrGeoParts=nbrGeoParts,
            symmetryFactor=self._symmetryFactor,
            startPosition=startPosition,
            axLen=axLen,
            winding=winding,
        )
        self._stator = statorSPMSM1
        return self._stator

    def createMachineDomains(self):
        if self._rotor != None and self._stator != None:
            self._domainS = Domain(
                "DomainS",
                self._rotor._domainS.physicals + self._stator._domainS.physicals,
            )
            self._domainM = Domain("DomainM", self._rotor._domainM.physicals)
            self._domainC = Domain(
                "DomainC",
                self._rotor._domainC.physicals + self._stator._domainC.physicals,
            )
            self._setMovingbandMesh()  # set the moving band mesh length
            self._mbRotor = Domain("MB_Rotor", self._rotor._mb.physicals)
            self._mbStator = Domain("MB_Stator", self._stator._mb.physicals)
            self._domain = Domain(
                "Domain",
                self._rotor._domain.physicals + self._stator._domain.physicals,
            )
            self._domainL = Domain(
                "DomainL",
                self._rotor._domainL.physicals + self._stator._domainL.physicals,
            )
            self._domainNL = Domain(
                "DomainNL",
                self._rotor._domainNL.physicals + self._stator._domainNL.physicals,
            )

            self._rotorMoving = Domain(
                "Rotor_Moving", self._rotor._rotorMoving.physicals
            )
            self._mbBaux = Domain("Rotor_Bnd_MBaux", self._rotor._mbBaux.physicals)
            self._domainAirGapRotor = Domain(
                "Rotor_Airgap", self._rotor._domainAirGap.physicals
            )
            self._domainAirGapStator = Domain(
                "Stator_Airgap", self._stator._domainAirGap.physicals
            )

            if (
                self._rotor._domainPrimary.physicals
                or self._stator._domainPrimary.physicals
            ):
                self._domainPrimary = Domain(
                    "primaryRegion_Rotor",
                    self._rotor._domainPrimary.physicals
                    + self._stator._domainPrimary.physicals,
                )
                self._domainSlave = Domain(
                    "SlaveRegion_Rotor",
                    self._rotor._domainSlave.physicals
                    + self._stator._domainSlave.physicals,
                )
            else:
                self._domainPrimary = None
                self._domainSlave = None
            self._domainInnerLimit = Domain(
                "InnerLimitLine", self._rotor._domainInnerLimit.physicals
            )
            self._domainOuterLimit = Domain(
                "OuterLimitLine", self._stator._domainOuterLimit.physicals
            )
        else:
            print("No definition of stator or rotor!")

    def _setMovingbandMesh(self) -> None:
        """Set the mesh size of the moving band point to the movingband heigth for resonable element quality

        Returns:
            Nothing
        """
        # calculate movingband heigth
        rotor = self.getRotor()
        stator = self.getStator()
        mbRadiusRotor = rotor.getMovingBand()[0].radius
        mbRadiusStator = stator.getMovingBand()[0].radius
        mbHeigth = abs(mbRadiusStator - mbRadiusRotor)
        # set the movingband mesh to mbHeigth
        for mb in rotor.getMovingBand() + stator.getMovingBand():
            for mbLine in mb.geometricalElement:
                mbLine.setMeshLength(mbHeigth)
        return None
