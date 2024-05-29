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
"""This module holds the electrical steel lamination Material-class definition"""
import numpy
from typing import Tuple, Dict, Union
from .material import Material


class ElectricalSteel(Material):
    """Electrical Steel Material"""

    # pylint: disable=locally-disabled,  too-many-arguments
    def __init__(
        self,
        name: str = "",
        conductivity: float = None,
        relPermeability: float = None,
        BH: numpy.ndarray = None,
        density: float = None,
        thermalConductivity: float = None,
        thermalCapacity: float = None,
        sheetThickness: float = None,
        lossParams: Tuple[float, float, float] = None,
        referenceFrequency: float = None,
        referenceFluxDensity: float = None,
    ):
        super().__init__(
            name,
            conductivity,
            relPermeability,
            0,
            0,
            BH,
            density,
            thermalConductivity,
            thermalCapacity,
        )
        # make sure density is given since we need it to calculate loss
        # parameters in core loss calculation.
        assert (
            self.density
        ), "No value for electrical steel material density given!"
        self.sheetThickness = sheetThickness
        self.lossParams = lossParams
        self.referenceFrequency = referenceFrequency
        self.referenceFluxDensity = referenceFluxDensity

    @property
    def sheetThickness(self) -> float:
        """The sheet thickness of the lamination material in m

        Returns:
            float: lamination sheet thickness in m
        """
        return self._sheetThickness

    @sheetThickness.setter
    def sheetThickness(self, newThickness: float) -> None:
        """set the sheet thickness of the lamination material in m

        Args:
            newThickness (float): lamination sheet thickness in m

        Raises:
            TypeError: if given sheet thickness if not numeric or None
            ValueError: if the given sheet thickness is a negative number
        """
        if isinstance(newThickness, (int, float)):
            if newThickness > 0:
                self._sheetThickness = newThickness
            else:
                raise (
                    ValueError(
                        f"Value for material sheet thickness must be a positive number, but is '{newThickness}'"
                    )
                )
        else:
            raise (
                TypeError(
                    f"Sheet thickness of material must be a numeric value but is '{type(newThickness)}':{newThickness}"
                )
            )

    @property
    def lossParams(self) -> Tuple[float, float, float]:
        """
        Iron loss parameters for electircal steel sheet material in W/kg.
        These parameters will be used in the iron loss calculation routine. For more information about the calculation method
        see `Lin u. a., „A Dynamic Core Loss Model for Soft Ferromagnetic and Power Ferrite Materials in Transient Finite
        Element Analysis“ <https://ieeexplore.ieee.org/document/1284663>`_. Make sure to also define the :attr:`reference
        frequency <pyemmo.script.material.electricalSteel.ElectricalSteel.referenceFrequency>` in Hz and the
        :attr:`reference flux density <pyemmo.script.material.electricalSteel.ElectricalSteel.referenceFluxDensity>`

        Returns:
            Tuple[float,float,float]: Iron loss parameters for hysteresis, eddy current and excess losses

                - hysteresis
                - eddy current
                - excess
        """
        return self._lossParams

    @lossParams.setter
    def lossParams(self, newLossParams: Tuple[float, float, float]) -> None:
        """Setter of iron loss parameters in W/kg

        Args:
            newLossParams (Tuple[float,float,float]): New iron loss parameters
            (order in Tuple hysteresis, eddy current, excess)
        """
        assert (
            len(newLossParams) == 3
        ), "There must be exactly 3 loss parameters for hysteresis, eddy current and excess loss."
        for lossparam in newLossParams:
            assert isinstance(
                lossparam, (float, int)
            ), f"Given loss parameter has wrong type: {type(lossparam)}. Must be float or int."
        self._lossParams = newLossParams

    @property
    def referenceFrequency(self) -> Union[float, int]:
        """Reference frequency for given loss parameters in Hz. See :attr:`lossParams <pyemmo.script.material.electricalSteel.ElectricalSteel.lossParams>`

        Returns:
            Union[float, int]: Reference frequency in Hz
        """
        return self._referenceFrequency

    @referenceFrequency.setter
    def referenceFrequency(
        self, newReferenceFrequency: Union[int, float]
    ) -> None:
        """Setter of reference frequency in Hz

        Args:
            newLossParams (Tuple[float,float,float]): New reference frequency in Hz
        """
        assert isinstance(
            newReferenceFrequency, (float, int)
        ), f"Given reference frequency for iron loss parameters has wrong type: {type(newReferenceFrequency)}. Must be float or int."
        self._referenceFrequency = newReferenceFrequency

    @property
    def referenceFluxDensity(self) -> Union[float, int]:
        """Reference flux density for given loss parameters in T. See
        :attr:`lossParams <pyemmo.script.material.electricalSteel.ElectricalSteel.lossParams>` for more details.

        Returns:
            Union[float, int]: Reference flux density in T
        """
        return self._referenceFluxDensity

    @referenceFluxDensity.setter
    def referenceFluxDensity(
        self, newReferenceFluxDensity: Union[int, float]
    ) -> None:
        """Setter of reference flux density in T

        Args:
            newReferenceFluxDensity (Tuple[float,float,float]): New reference flux density in T
        """
        assert isinstance(
            newReferenceFluxDensity, (float, int)
        ), f"Given parameter for reference flux density has wrong type: {type(newReferenceFluxDensity)}. Must be float or int."
        self._referenceFluxDensity = newReferenceFluxDensity

    def print(self) -> None:
        """print electrical steel material to stdout"""
        table = [
            ["Name:", self.name],
            ["Is linear:", "Yes" if self.linear else "No"],
            ["Electrical Conductivity [S/m]:", self.conductivity],
            ["Relative Permeability []:", self.relPermeability],
            ["Remanence Flux Density[T]:", self.remanence],
            ["Density [kg/m³]:", self.density],
            ["Sheet Thickness [mm]:", self.sheetThickness],
            ["Thermal Conductivity [W/(m*K)]:", self.thermalConductivity],
            ["Thermal Capacity [J/(kg*K)]:", self.thermalCapacity],
        ]
        for row in table:
            if row[1] is None:
                row[1] = (
                    "None"  # set to string because formatting None not supported
                )
            print(f"{row[0]: >25} {row[1]: <15}")
        print("\n")
