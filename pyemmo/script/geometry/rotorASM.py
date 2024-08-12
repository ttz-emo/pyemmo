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

from typing import Dict, List

from .physicalElement import PhysicalElement
from .rotor import Rotor


class RotorASM(Rotor):
    """TODO"""

    def __init__(
        self,
        physicalElementList: List[PhysicalElement],
        nbr_bars: int,
        name: str = "",
        axLen: float = 1.0,
    ):
        """
        Constructor of class Rotor
        Args:
            physicalElements (List[PhysicalElement]): List of PhysicalElement
                objects defining geometry and materials.
            nbr_bars (int) = Number of rotor bars.
            name (str): Defaults to "".
            axLen (float): Active axial length of stator lamination in [m].
                Defaults to 1.0

        """
        super().__init__(
            name=name, axLen=axLen, physicalElementList=physicalElementList
        )
        self.nbr_bars = nbr_bars
        self._createDomainForRotor()  # create rotor domains

    @property
    def nbr_bars(self) -> int:
        """Number of rotor bars

        Returns:
            int: Number of bars
        """
        return self._nbr_bars

    @nbr_bars.setter
    def nbr_bars(self, nbr_bars: int):
        if nbr_bars % 1 == 0.0:
            self._nbr_bars = nbr_bars
        else:
            raise ValueError(f"Number or rotor bars is not an integer: {nbr_bars}")

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
        # TODO: UPDATE
        # domainS = []  # Eingeprägte Ströme
        # domainM = []  # Magnete
        # domainLam = []  # Lamination (part with material specified lamination)
        # domainC = []  # Leitende Flächen z. B. Stäbe ASM
        # domainCC = []  # alle elektrisch nicht leitenden Flächen
        # allMbLines = []  # Moving Band

        # domain = []  # Alle Flächen
        # domainNL = []  # Alle nicht linearen Flächen
        # domainL = []  # Alle linearen Flächen

        # domainMoving = (
        #     []
        # )  # Alle Teile die sich drehen, inkl. Moving Band (alle)
        # movingBandAux = []  # Bei Teilmodell -> die restlichen Moving Band
        # domainAirgap = []  # Luftspalt im Rotor

        # primaryLines = []  # Teilmodell primarykante
        # slaveLines = []  # Teilmodell Slavekante
        # limitLines = []  # Randlinien ohne Primär- und Sekundärkanten
        # for physElem in self.physicalElements:
        #     geoType = physElem.geoElementType
        #     if geoType == Surface:
        #         # domainC, domainL & domainNL
        #         material = physElem.material
        #         if material:
        #             # if conductivity not None add to domainC
        #             if material.conductivity:
        #                 domainC.append(physElem)
        #             else:
        #                 domainCC.append(physElem)
        #             # if material is linear
        #             if material.linear:
        #                 domainL.append(physElem)
        #             else:
        #                 domainNL.append(physElem)
        #             # if material is laminated
        #             if isinstance(material, ElectricalSteel):
        #                 domainLam.append(physElem)
        #         else:
        #             physName = physElem.name
        #             raise RuntimeError(
        #                 f"No Material defined: ({physName})",
        #                 f"Material is {material}",
        #             )

        #         # domainM zuweisen
        #         if physElem.type == "Magnet":
        #             magnet: Magnet = physElem
        #             domainM.append(magnet)
        #             # remove magnet from C or CC because assignment is done by getdp
        #             if magnet in domainC:
        #                 domainC.remove(magnet)
        #             elif magnet in domainCC:
        #                 domainCC.remove(magnet)
        #             continue

        #         # domainS zuweisen
        #         if physElem.type == "Slot":
        #             domainS.append(physElem)
        #             continue

        #         # airgap
        #         if physElem.type == "AirGap":
        #             domainAirgap.append(physElem)

        #         # Stator lamination if not allready defined
        #         if physElem.type == "Lamination":
        #             # pE could allready been added due to material
        #             if physElem not in domainLam:
        #                 domainLam.append(physElem)

        #         domain.append(physElem)  # append Surface to main Domain
        #         # append Surface to rotorMoving Domain (rotorMoving also includes movingband lines!)
        #         domainMoving.append(physElem)
        #     ## GEOTYPE LINE:
        #     elif geoType == Line:
        #         # MB zuweisen
        #         if physElem.type == "MovingBand":
        #             allMbLines.append(physElem)
        #             if physElem.auxiliary:
        #                 movingBandAux.append(physElem)

        #             domainMoving.append(physElem)
        #             continue  # continue after because it cant be any other physicalElement type

        #         if physElem.type == "PrimaryLine":
        #             primaryLines.append(physElem)
        #             continue

        #         if physElem.type == "SlaveLine":
        #             slaveLines.append(physElem)
        #             continue

        #         if physElem.type == "LimitLine":
        #             limitLines.append(physElem)

        # sortedPhy = {
        #     "primary": primaryLines,
        #     "slave": slaveLines,
        #     "limit": limitLines,
        #     "mb_all": allMbLines,
        #     "mb_Mbaux": movingBandAux,
        #     "airGap": domainAirgap,
        #     "rotor_moving": domainMoving,
        #     "domainS": domainS,
        #     "domainM": domainM,
        #     "domainLam": domainLam,
        #     "domainC": domainC,
        #     "domainCC": domainCC,
        #     "domain": domain,
        #     "domainNL": domainNL,
        #     "domainL": domainL,
        # }
        # return sortedPhy
