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
from math import pi
from typing import Dict

import swat_em

from ... import logging
from ..script import default_param_dict
from .domain import Domain
from .machineAllType import MachineAllType
from .rotorIPMSM import RotorIPMSM
from .statorSPMSM import StatorPMSM


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
        super().__init__(
            nbrPolePairs=(simuParam["analysisParameter"]["nbrPolesTotal"] / 2),
            rotor=None,
            stator=None,
            name=name,
        )
        ###Simulationsparameter gemäß der Eingabe.
        self._simuParam = simuParam
        # Calculate Poles and Slots for Model
        self._simuParam["analysisParameter"]["nbrPolesinModel"] = (
            self._simuParam["analysisParameter"]["nbrPolesTotal"]
            / simuParam["analysisParameter"]["symmetryFactor"]
        )
        self._simuParam["analysisParameter"]["nbrSlotinModel"] = (
            self._simuParam["analysisParameter"]["nbrSlotTotal"]
            / simuParam["analysisParameter"]["symmetryFactor"]
        )

    @property
    def startPos(self):
        """get the StartPos

        Returns:
            _type_: _description_
        """
        simuParams = self._simuParamDict
        return simuParams["analysisParameter"]["startPosition"]

    @property
    def symmetryFactor(self) -> int:
        """Getter of Symmetry Factor

        Returns:
            int: Symmetry Factor
        """
        try:
            sym_factor = super().symmetryFactor
            if self._simuParam["analysisParameter"]["symmetryFactor"] > sym_factor:
                logging.error(
                    "Given symmetry factor doesn't match maximal sym: %i != %i",
                    self._simuParam["analysisParameter"]["symmetryFactor"],
                    sym_factor,
                )
                return sym_factor
        except RuntimeError:
            # super() failed because rotor or stator was not given
            return self._simuParam["analysisParameter"]["symmetryFactor"]
        except Exception as exce:
            raise exce
        # noramlly we should return sym_factor here, but since the workflow is
        # that the sym_factor must be given from outside, we return that one
        # for now...
        # return sym_factor
        return self._simuParam["analysisParameter"]["symmetryFactor"]

    @property
    def simParams(self) -> dict:
        """
        Return geometical simulation parameters as dict
        - SYMMETRY_FACTOR
        - L_AX_R
        - L_AX_S
        - NBR_POLE_PAIRS
        - NBR_TURNS_IN_FACE
        - R_AIRGAP
        """
        paramDict = default_param_dict["GEO"]
        paramDict["SYMMETRY_FACTOR"] = self.symmetryFactor
        paramDict["L_AX_R"] = self.rotor.axialLength
        paramDict["L_AX_S"] = self.stator.axialLength
        paramDict["NBR_POLE_PAIRS"] = self.nbrPolePairs
        paramDict["NBR_SLOTS"] = self.stator.nbrSlots
        slots = self.stator.slots
        nbrTurns = slots[0].nbrTurns
        slots.pop(0)  # pop first one to don't compare the slot against itself
        for slot in slots:
            actNbrTurns = slot.nbrTurns
            if nbrTurns != actNbrTurns:
                raise ValueError(
                    f"Different number of turns in slots! {nbrTurns} != {actNbrTurns}"
                )
        paramDict["NBR_TURNS_IN_FACE"] = nbrTurns
        paramDict["R_AIRGAP"] = self.rotor.movingBand[0].radius
        return paramDict

    @property
    def _simuParamDict(self) -> Dict:
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
        nbrPoles = self.nbrPolePairs * 2
        symFactor = self.symmetryFactor
        angleGeoParts = 2 * pi / (nbrPoles) / 2  # half segment?
        userRot = self.startPos
        # rotate half pole, because pole center is on x-axis
        startPosition = angleGeoParts + userRot
        nbrGeoParts = int(nbrPoles / symFactor) * 2  # half segment?

        self.rotor = RotorIPMSM(
            laminationType=laminationType,
            magnetType=magnetType,
            angleGeoParts=angleGeoParts,  # angle of one segment
            nbrGeoParts=nbrGeoParts,
            symmetryFactor=self._simuParam["analysisParameter"]["symmetryFactor"],
            startPosition=startPosition,
            axLen=axLen,
        )
        return self.rotor

    def addStatorToMachine(
        self,
        laminationType: str,
        slotType: str,
        winding: swat_em.datamodel,
        axLen: float = 1,
    ):
        startPosition = (
            pi
            / self._simuParam["analysisParameter"]["symmetryFactor"]
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
            + self._simuParam["analysisParameter"]["startPosition"]
        )
        angleGeoParts = (
            pi
            / self._simuParam["analysisParameter"]["symmetryFactor"]
            / self._simuParam["analysisParameter"]["nbrSlotinModel"]
        )
        nbrGeoParts = self._simuParam["analysisParameter"]["nbrSlotinModel"] * 2
        statorSPMSM1 = StatorPMSM(
            laminationType=laminationType,
            slotType=slotType,
            nbrSlots=self._simuParam["analysisParameter"]["nbrSlotTotal"],
            angleGeoParts=angleGeoParts,
            nbrGeoParts=nbrGeoParts,
            symmetryFactor=self._simuParam["analysisParameter"]["symmetryFactor"],
            startPosition=startPosition,
            axLen=axLen,
            winding=winding,
        )
        self.stator = statorSPMSM1
        return self.stator

    def createMachineDomains(self):
        if self.rotor != None and self.stator != None:
            self._domainS = Domain(
                "DomainS",
                self.rotor._domainS.physicals + self.stator._domainS.physicals,
            )
            self._domainM = Domain("DomainM", self.rotor._domainM.physicals)
            self._domainC = Domain(
                "DomainC",
                self.rotor._domainC.physicals + self.stator._domainC.physicals,
            )
            self._setMovingbandMesh()  # set the moving band mesh length
            self._mbRotor = Domain("MB_Rotor", self.rotor._mb.physicals)
            self._mbStator = Domain("MB_Stator", self.stator._mb.physicals)
            self._domain = Domain(
                "Domain",
                self.rotor._domain.physicals + self.stator._domain.physicals,
            )
            self._domainL = Domain(
                "DomainL",
                self.rotor._domainL.physicals + self.stator._domainL.physicals,
            )
            self._domainNL = Domain(
                "DomainNL",
                self.rotor._domainNL.physicals + self.stator._domainNL.physicals,
            )

            self._rotorMoving = Domain(
                "Rotor_Moving", self.rotor._rotorMoving.physicals
            )
            self._mbBaux = Domain("Rotor_Bnd_MBaux", self.rotor._mbBaux.physicals)
            self._domainAirGapRotor = Domain(
                "Rotor_Airgap", self.rotor._domainAirGap.physicals
            )
            self._domainAirGapStator = Domain(
                "Stator_Airgap", self.stator._domainAirGap.physicals
            )

            if (
                self.rotor._domainPrimary.physicals
                or self.stator._domainPrimary.physicals
            ):
                self._domainPrimary = Domain(
                    "primaryRegion_Rotor",
                    self.rotor._domainPrimary.physicals
                    + self.stator._domainPrimary.physicals,
                )
                self._domainSlave = Domain(
                    "SlaveRegion_Rotor",
                    self.rotor._domainSlave.physicals
                    + self.stator._domainSlave.physicals,
                )
            else:
                self._domainPrimary = None
                self._domainSlave = None
            self._domainInnerLimit = Domain(
                "InnerLimitLine", self.rotor._domainInnerLimit.physicals
            )
            self._domainOuterLimit = Domain(
                "OuterLimitLine", self.stator._domainOuterLimit.physicals
            )
        else:
            print("No definition of stator or rotor!")

    def _setMovingbandMesh(self) -> None:
        """Set the mesh size of the moving band point to the movingband heigth for resonable element quality

        Returns:
            Nothing
        """
        # calculate movingband heigth
        rotor = self.rotor
        stator = self.stator
        mbRadiusRotor = rotor.movingBand[0].radius
        mbRadiusStator = stator.movingBand[0].radius
        mbHeigth = abs(mbRadiusStator - mbRadiusRotor)
        # set the movingband mesh to mbHeigth
        for mb in rotor.movingBand + stator.movingBand:
            for mbLine in mb.geo_list:
                mbLine.setMeshLength(mbHeigth)
        return None
