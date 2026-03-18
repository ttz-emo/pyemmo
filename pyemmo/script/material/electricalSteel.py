#
# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO,
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
"""
This module defines the class :class:`ElectricalSteel` for electrical steel materials
used in electromagnetic power transfomation.
"""
from __future__ import annotations

import json
import logging
import operator
import os

import numpy as np

from . import DATABASE_PATH
from .material import Material


# pylint: disable=locally-disabled,  too-many-arguments, too-many-positional-arguments
# pylint: disable=locally-disabled,  too-many-instance-attributes, line-too-long
class ElectricalSteel(Material):
    """Electrical Steel Material"""

    def __init__(
        self,
        name: str,
        sheetThickness: float,
        conductivity: float = 0.0,
        relPermeability: float = 1.0,
        BH: np.ndarray = np.empty(0),
        density: float = 0.0,
        thermalConductivity: float = 0.0,
        thermalCapacity: float = 0.0,
        lossParams: tuple[float, float, float] = None,
        referenceFrequency: float = None,
        referenceFluxDensity: float = None,
    ):
        """
        Initializes an instance of the electrical steel material class.

        Parameters:
            name (str): Name of the material.
            sheetThickness (float): Thickness of the steel sheet in meters.
            conductivity (float, optional): Electrical conductivity of the material in S/m.
            relPermeability (float, optional): Relative magnetic permeability (no unit).
            BH (numpy.ndarray, optional): B-H curve data as a NumPy array.
                Where B is the flux density in T and H is the magnetic field strength in A/m.
                Must be given by shape (X,2) as pairs of B and H:
                :code:`[[B1, H1],[B2, H2],[B3, H3],...]`.
            density (float, optional): Density of the material in kg/m³.
            thermalConductivity (float, optional): Thermal conductivity in W/(m·K).
            thermalCapacity (float, optional): Thermal capacity in J/(kg·K).
            lossParams (Tuple[float, float, float], optional): Loss parameters,
                possibly recalculated based on reference frequency and flux density in W/m³.
                The order in the tuple is:

                - hysteresis loss
                - eddy current loss
                - excess loss

                If the values are given in a range for W/kg (hysteresis value < 20 AND
                eddy current value < 5), the values will be adapted by the
                material density (kg/m³) to obtain the values in W/m³.
            referenceFrequency (float, optional): Reference frequency for loss
                calculations in Hz. This is used to adapt the loss parameters
                if they are given in W/kg.
            referenceFluxDensity (float, optional): Reference flux density for
                loss calculations in T.
        """
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
        self.sheetThickness = sheetThickness
        self.referenceFrequency = referenceFrequency
        self.referenceFluxDensity = referenceFluxDensity
        # NOTE: lossParams needs to be set at last, because it uses reference
        # frequency and flux density to recalculate loss parameters in case
        # they are given in W/kg
        self.lossParams = lossParams

    def __str__(self) -> str:
        """string representation of electrical steel material"""
        mat_str = super().__str__()
        return (
            mat_str
            + "\n"
            + "\n".join(
                f"{key:>35}: {value:<15}"
                for key, value in [
                    ("Sheet Thickness [mm]", self.sheetThickness),
                    (
                        "Hysteresis Loss Factor [W/m³]",
                        self.lossParams[0],
                    ),
                    (
                        "Eddy-Current Loss Factor [W/m³]",
                        self.lossParams[1],
                    ),
                    (
                        "Excess Loss Factor [W/m³]",
                        self.lossParams[2],
                    ),
                    (
                        "Reference Frequency [Hz]",
                        self.referenceFrequency if self.referenceFrequency else "None",
                    ),
                    (
                        "Reference Flux Density [T]",
                        (
                            self.referenceFluxDensity
                            if self.referenceFluxDensity
                            else "None"
                        ),
                    ),
                ]
            )
        )

    # TODO: Add overwrite of Material load class method

    @classmethod
    def load(cls, mat_name: str) -> ElectricalSteel:
        """Load object of type ElectricalSteel from json file by name

        Args:
            materialName (str): Material name to load the Material from the
                database.
        """
        if mat_name == "":
            raise ValueError("Material name must not be empty!")

        json_path = os.path.join(DATABASE_PATH, f"{mat_name}.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(
                f"Material {mat_name} does not exist in the material database!"
            )
        with open(json_path) as file:
            mat_dict: dict = json.load(file)
        # remove keys that are not kwargs of ElectricalSteel
        mat_dict.pop("ID")
        mat_dict.pop("linear")
        return cls.from_dict(mat_dict)

    @classmethod
    def from_dict(cls, mat_dict: dict) -> ElectricalSteel:
        """Create a ElectricalSteel object from a data dict"""
        if mat_dict["BHCurve"] == {}:
            bh_curve = np.empty(0)  # default value for empty
        else:
            bh_curve = mat_dict["BHCurve"]["default"]
        # Update mat_dict to use correct keyword "BH"
        mat_dict["BH"] = bh_curve
        mat_dict.pop("BHCurve")
        # remove unsetable properties of Material in ElectricalSteel
        # These are automatically added as we call super().as_dict in
        # ElectricalSteel.as_dict() from Material.save()
        for removal_key in ("remanence", "tempCoefRem", "linear"):
            if removal_key in mat_dict:
                mat_dict.pop(removal_key)
        if not "sheetThickness" in mat_dict:
            raise AttributeError("Missing parameter 'sheetThickness' from init dict!")
        return cls(**mat_dict)

    def as_dict(self) -> dict:
        """Get dict representation of Material"""
        mat_dict = super().as_dict()
        mat_dict["sheetThickness"] = self.sheetThickness
        mat_dict["lossParams"] = self.lossParams
        mat_dict["referenceFrequency"] = self.referenceFrequency
        mat_dict["referenceFluxDensity"] = self.referenceFluxDensity
        return mat_dict

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
                        "Value for material sheet thickness must be a "
                        f"positive number, but is '{newThickness}'"
                    )
                )
        else:
            raise (
                TypeError(
                    "Sheet thickness of material must be a numeric value but "
                    f"is '{type(newThickness)}':{newThickness}"
                )
            )

    @property
    def lossParams(self) -> tuple[float, float, float]:
        """
        Iron loss parameters for electircal steel sheet material in W/m³.
        If the values are given in a range for W/kg (hysteresis value < 20 AND
        eddy current value < 5). The values will be adapted by
        :meth:`_adapt_loss_params <pyemmo.script.material.electricalSteel.ElectricalSteel._adapt_loss_params>`
        method.

        The loss parameters will be used in the iron loss calculation routine.
        For more information about the calculation method see
        :py:mod:`calc_core_loss <pyemmo.functions.calcIronLoss>` module.
        Make sure to also define
        :attr:`reference frequency <pyemmo.script.material.electricalSteel.ElectricalSteel.referenceFrequency>`
        in Hz and the
        :attr:`reference flux density <pyemmo.script.material.electricalSteel.ElectricalSteel.referenceFluxDensity>`
        in T.

        Returns:
            Tuple[float,float,float]: Iron loss parameters for hysteresis,
            eddy current and excess losses

            - hysteresis
            - eddy current
            - excess
        """
        return self._lossParams

    @lossParams.setter
    def lossParams(self, newLossParams: tuple[float, float, float] | None) -> None:
        """Setter of iron loss parameters in W/m³.

        Args:
            newLossParams (Tuple[float,float,float] or None): New iron loss
                parameters (order in Tuple hysteresis, eddy current, excess)
        """
        if newLossParams is None or all(map(operator.eq, newLossParams, (0, 0, 0))):
            self._lossParams = (0, 0, 0)
        else:
            if len(newLossParams) != 3:
                raise ValueError(
                    "There must be exactly 3 loss parameters for "
                    f"hysteresis, eddy current and excess loss. lossParams: {newLossParams}"
                )
            for lossparam in newLossParams:
                if not isinstance(lossparam, (float, int)):
                    raise TypeError(
                        f"Given loss parameter has wrong type: {type(lossparam)}. "
                        "Must be float or int."
                    )
            # test if loss parameters are in W/kg or W/m³ by checking the value
            # range. Typically hysteresis loss value is between 1.0...5.0 W/kg;
            # eddy current value is between 0.2...2.0 W/kg.
            if newLossParams[0] < 20 and newLossParams[1] < 5:
                logging.getLogger(__name__).warning(
                    (
                        "Looks like the loss parameters for material %s are "
                        "given in W/kg (not W/m³). "
                        "Trying to calculate correct values..."
                    ),
                    self.name,
                )
                newLossParams = self._adapt_loss_params(newLossParams)
            self._lossParams = tuple(newLossParams)  # make sure its a tuple

    def _adapt_loss_params(
        self, lossParams: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """"""
        freq = self.referenceFrequency  # frequency in Hz
        if not freq:
            raise ValueError(
                "Adaption of core loss parameters failed. "
                "No reference frequency given!"
            )
        ind = self.referenceFluxDensity  # induction in T
        if not ind:
            raise ValueError(
                "Adaption of core loss parameters failed."
                "No reference induction given!"
            )
        # make sure density is given!
        if not self.density:
            raise ValueError(
                f"Material {self.name} missing value for attribute density!"
                " If values for loss parameter are given, "
                "you also need to specify material density!"
            )
        dens = self.density  # density in kg/m³
        lossParams[0] = lossParams[0] * dens / freq / (ind**2)
        lossParams[1] = lossParams[1] * dens / ((freq * ind) ** 2)
        lossParams[2] = lossParams[2] * dens / ((freq * ind) ** 1.5)
        return lossParams

    @property
    def referenceFrequency(self) -> float | int:
        """Reference frequency for given loss parameters in Hz. See
        :attr:`lossParams <pyemmo.script.material.electricalSteel.ElectricalSteel.lossParams>`

        Returns:
            Union[float, int]: Reference frequency in Hz
        """
        return self._referenceFrequency

    @referenceFrequency.setter
    def referenceFrequency(self, newReferenceFrequency: int | float | None):
        """Setter of reference frequency in Hz

        Args:
            newLossParams (Tuple[float,float,float]): New reference frequency in Hz
        """
        if newReferenceFrequency is None:
            self._referenceFrequency = None
            return
        if not isinstance(newReferenceFrequency, (float, int)):
            raise TypeError(
                "Given reference frequency for iron loss parameters has "
                f"wrong type: {type(newReferenceFrequency)}. "
                "Must be float or int."
            )
        self._referenceFrequency = newReferenceFrequency

    @property
    def referenceFluxDensity(self) -> float | int:
        """Reference flux density for given loss parameters in T. See
        :attr:`lossParams <pyemmo.script.material.electricalSteel.ElectricalSteel.lossParams>`
        for more details.

        Returns:
            Union[float, int]: Reference flux density in T
        """
        return self._referenceFluxDensity

    @referenceFluxDensity.setter
    def referenceFluxDensity(self, newReferenceFluxDensity: int | float | None):
        """Setter of reference flux density in T

        Args:
            newReferenceFluxDensity (Tuple[float,float,float]): New reference
                flux density in T
        """
        if newReferenceFluxDensity is None:
            self._referenceFluxDensity = None
            return
        if not isinstance(newReferenceFluxDensity, (float, int)):
            raise TypeError(
                "Given parameter for reference flux density has "
                f"wrong type: {type(newReferenceFluxDensity)}. "
                "Must be float or int."
            )
        self._referenceFluxDensity = newReferenceFluxDensity
