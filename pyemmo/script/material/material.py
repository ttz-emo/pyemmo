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
"""Module for Material-class"""


# pylint: disable=line-too-long

import json
import os
import warnings
from typing import Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.typing import NDArray

from pyemmo.definitions import ROOT_DIR

from ... import rootLogger as logger


class Material:
    """Class Material defines a material for the simulation with onelab"""

    def __init__(
        self,
        name: str = "",
        conductivity: float = None,
        relPermeability: float = None,
        remanence: float = None,
        tempCoefRem: float = None,
        BH: NDArray = None,
        density: float = None,
        thermalConductivity: float = None,
        thermalCapacity: float = None,
    ):
        self.name = name
        self.conductivity = conductivity
        self.relPermeability = relPermeability
        self.remanence = remanence
        self.tempCoefRem = tempCoefRem
        if tempCoefRem and not remanence:
            warnings.warn(
                "Temperature coefficient for Br is given without value for Br "
                f"in Material {name}!"
            )
        self.BH = BH

        self.density = density
        self.thermalConductivity = thermalConductivity
        self.thermalCapacity = thermalCapacity

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            # check BH is equal:
            try:
                # FIXME: Maybe check shapes before...
                # if comparison results in ValueError, shapes could not be broadcasted
                bhComp = np.array_equal(self.BH, __o.BH)
            except ValueError:
                # comparison with empty array returns a ValueError
                return False
            except Exception as exce:
                raise exce
            if not isinstance(bhComp, bool):
                # comparison with not empty array returns ndarray with dtype:bool
                if isinstance(bhComp, np.ndarray):
                    if bhComp.dtype == bool:
                        bhComp = bhComp.all()
                else:
                    raise (
                        ValueError(
                            f"Comparison of BH curve resulted in unknown type '{type(bhComp)}'"
                        )
                    )
            if bhComp:
                selfDict = self.__dict__.copy()
                del selfDict["_BH"]
                otherDict = __o.__dict__.copy()
                del otherDict["_BH"]
                return selfDict == otherDict
            return False
        else:
            return False

    def load(self, materialName: str = ""):
        """Function to load material from JSON database.

        Args:
            materialName (str, optional): Material name to load the Material from the
                database, if its not given in the Material init before. Defaults to the
                instance name (:func:`~material.Material.name`).

        Raises:
            RuntimeError: _description_
        """
        if materialName == "":
            if self.name == "":
                raise RuntimeError("Material name undefined, cannot load.")
            else:
                json_path = os.path.join(
                    ROOT_DIR,
                    f"pyemmo/script/material/material_json/{self.name}.json",
                )
        else:
            json_path = os.path.join(
                ROOT_DIR,
                f"pyemmo/script/material/material_json/{materialName}.json",
            )
        try:
            with open(json_path) as file:
                mat_dict = json.load(file)
            self.name = mat_dict["name"]
            self.conductivity = mat_dict["conductivity"]
            self.relPermeability = mat_dict["relPermeability"]
            if isinstance(mat_dict["remanence"], str):
                self.remanence = 0
            else:
                self.remanence = mat_dict["remanence"]
            self.linear = mat_dict["linear"]
            if not self.linear:
                for temp_key in mat_dict["BHCurve"].keys():
                    self.set_BH(mat_dict["BHCurve"][temp_key], temp_key)
        except FileNotFoundError:
            logger.error(FileNotFoundError)

    def save(self):
        if self.name == "":
            raise RuntimeError("Material needs to have a name!")
        else:
            material_folder = os.path.join(
                ROOT_DIR, "pyemmo/script/material/material_json"
            )
            mat_dict = {}
            mat_dict["ID"] = (
                len([f for f in os.listdir(material_folder) if ".json" in f]) + 1
            )
            mat_dict["name"] = self.name
            mat_dict["conductivity"] = self.conductivity
            mat_dict["relPermeability"] = self.relPermeability
            if self.remanence == None:
                mat_dict["remanence"] = "no information"
            else:
                mat_dict["remanence"] = self.remanence
            mat_dict["linear"] = self.linear
            mat_dict["BHCurve"] = {}
            if not self.linear:
                for temp_key in self._BH.keys():
                    mat_dict["BHCurve"][temp_key] = self.get_BH(temp_key).tolist()

            with open(os.path.join(material_folder, f"{self.name}.json"), "w") as file:
                json.dump(mat_dict, file, indent="\t")

    def delete(self):
        json_path = os.path.join(
            ROOT_DIR, f"pyemmo/script/material/material_json/{self.name}.json"
        )
        print(json_path)
        try:
            # pathlib.Path.unlink(json_path)
            os.remove(json_path)
        except FileNotFoundError:
            logger.warning(f"{self.name}.json is already deleted or does not exist.")

    # def addBHCurveFromFile(
    #     self, data, update_db: bool = False
    # ):
    #     try:
    #         file = pd.read_table(data)
    #     except UnicodeDecodeError:
    #         file = pd.read_excel(data)
    #     allValue = file.values
    #     try:
    #         temp_list = set([row[2] for row in allValue])
    #         for temp in temp_list:
    #             if temp == "no information": temp_key = "default"
    #             else: temp_key = temp
    #             self.set_BH(
    #                 [[row[0], row[1]] for row in allValue if row[2] == temp],
    #                 temp_key
    #             )
    #     except IndexError:
    #         self.set_BH(
    #                 [[row[0], row[1]] for row in allValue]
    #             )
    #     if update_db:
    #         self.save()

    def plotBHCurve(self, temp=None):
        """
        Function to plot BH curve
        Args:
            temp: chosen temperature for the curve. can be "default", or a specific temp.
                - if none is defined, all BH curves for all temps will be plotted
        Returns:
            None
        """
        if self.linear:
            warnings.warn("Material is linear, there is no curve")
            return
        if temp == None:
            for t in self._BH.keys():
                if self._BH[t].size:
                    h = [row[0] for row in self._BH[t]]
                    b = [row[1] for row in self._BH[t]]
                    label = lambda: "default" if t == "default" else f"{t}°C"
                    plt.plot(h, b, label=label())
        else:
            BH_vals = self.get_BH(temp)
            h = [row[0] for row in BH_vals]
            b = [row[1] for row in BH_vals]
            label = lambda: ("default" if temp not in self._BH.keys() else f"{t}°C")
            plt.plot(h, b, label=label())
        plt.grid(visible=True, which="major", color="#666666", linestyle="-")
        plt.minorticks_on()
        plt.grid(
            visible=True,
            which="minor",
            color="#999999",
            linestyle="-",
            alpha=0.2,
        )
        # plt.xlim(h[0], h[len(h) - 1])
        plt.title(f"BH-Curve for {self.name}")
        plt.xlabel("Field intensity H")
        plt.ylabel("Flux density B")
        plt.legend(loc="upper right")

    # def isLinear(self) -> bool:
    #     """check if the material is linear or has BH curve

    #     Returns:
    #         bool: True if material doesn't have a BH curve, but a relative permeability.
    #         Otherwise Flase
    #     """
    #     if self._linear and self.BH.size:
    #         # pylint: disable=locally-disabled,  line-too-long
    #         warnings.warn(
    #             f"Linearity flag of material '{self.name}' is True although BH-curve is not empty!"
    #         )
    #     return self._linear

    # def setLinear(self, linear: bool) -> None:
    #     """set the linearity of the material

    #     Args:
    #         linear (bool): True if material is linear, otherwise False
    #     """
    #     if isinstance(linear, bool):
    #         self._linear = linear
    #     else:
    #         raise ValueError("Attribute linear must be type bool.")

    @property
    def name(self) -> str:
        """getter of material name

        Returns:
            str: name of the material
        """
        return self._name

    @property
    def conductivity(self) -> Union[float, int, None]:
        """get electrical conductivity


        Returns:
            Union[float, int, None]: electrical conductivity in S/m or None if
            not conductive.
        """
        return self._conductivity

    @property
    def relPermeability(self) -> Union[float, int, None]:
        """get relative magnetic permeability

        Returns:
            Union[float, int, None]: relative permeability in []
        """
        return self._relPermeability

    @property
    def remanence(self) -> Union[float, int, None]:
        """get remanent flux density

        Returns:
            Union[float, int, None]: remanent flux density (Br) in T
        """
        return self._remanence

    @property
    def tempCoefRem(self) -> Union[float, int, None]:
        """Get the temperature coefficient of the remanent flux density.

        Returns:
            Union[float, int, None]: temperatur coefficient of remanent flux density in 1/K
            ("one per Kelvin")
        """
        return self._tempCoefRem

    @property
    def BH(self) -> NDArray:
        """getter property of BH
        Returns:
            numpy.ndarray: _description_:
        NOTE: This only returns BH curve for default temperature. Use get_BH() to get BH
        curve for specifc temperature instead!
        """
        return self.get_BH()
        # if self._BH.ndim < 3:
        #     # pylint: disable=locally-disabled,  line-too-long
        #     warnings.warn(
        #         f"Tried to access the BH-curve for temperature {temperature}°C, but there is only one BH-curve specified!",
        #         UserWarning,
        #     )
        #     return self._BH
        # # else:
        # assert self._BH.ndim == 3
        # TODO: implement temperature depended bh curve

    def get_BH(self, temperature: float = None):
        """getter of BH

        Args:
            temperature (float, optional): _description_. Defaults to None.

        Returns:
            numpy.ndarray: _description_
        """
        if not temperature:
            if not self._BH["default"]:
                warnings.warn(
                    "BH-Curve is linear, or default curve has not been set.\n Please set default curve (syntax: obj.BH = <NDArray>) or use get_BH(temperature)",
                    UserWarning,
                )
            return np.array(self._BH["default"])
        try:
            return np.array(self._BH[temperature])
        except KeyError:
            if self.linear:
                warnings.warn(
                    f"Tried to access the BH-curve for temperature {temperature}°C, "
                    "but BH-Curve is linear!",
                    UserWarning,
                )
                return np.empty(0)
            if len(self._BH.keys()) < 2:
                warnings.warn(
                    f"Tried to access the BH-curve for temperature {temperature}°C, "
                    "but there is only one BH-curve specified!",
                    UserWarning,
                )
                return np.array(self._BH["default"])
            warnings.warn(
                f"No BH-curve registered for temperature {temperature}°C!",
                UserWarning,
            )
            return np.empty(0)
        # if self._BH.ndim < 3:
        #     # pylint: disable=locally-disabled,  line-too-long
        #     warnings.warn(
        #         f"Tried to access the BH-curve for temperature {temperature}°C, but "
        #         "there is only one BH-curve specified!",
        #         UserWarning,
        #     )
        #     return self._BH
        # # else:
        # assert self._BH.ndim == 3

    # pylint: disable=invalid-name
    @BH.setter
    def BH(self, newBH: NDArray):
        """setter property of BH curve.

        Args:
            BH (numpy.ndarray): BH curve (2D array) with shape (X,2) ->
            [[B1, H1],[B2, H2],[B3, H3],...]
        Returns:
            None
        NOTE: this sets the curve for the default temperature only. Use set_BH() to set
        BH Curve for specific temperature
        """
        self.set_BH(newBH)

    def _set_BH_decorator(set_BH):
        """
        decorator to extend the function of set_BH to also accepts dict or file path
        """

        def setBHWrapper(self, data, temp: float = None):
            if isinstance(data, dict):
                if len(data) < 1:
                    raise (ValueError("There is no BH data to add!"))
                for temp in data.keys():
                    temp_key = lambda: ("default" if temp == "no information" else temp)
                    set_BH(self, data[temp], temp_key())
            elif isinstance(data, str):
                try:
                    file = pd.read_table(data)
                except UnicodeDecodeError:
                    file = pd.read_excel(data)
                except FileNotFoundError:
                    warnings.warn("Cannot load, file does not exist")
                    return
                allValue = file.values
                try:
                    temp_list = {row[2] for row in allValue}
                    for temp in temp_list:
                        if temp == "no information":
                            temp_key = "default"
                        else:
                            temp_key = temp
                        set_BH(
                            self,
                            [[row[0], row[1]] for row in allValue if row[2] == temp],
                            temp_key,
                        )
                except IndexError:
                    set_BH(self, [[row[0], row[1]] for row in allValue])
            else:
                set_BH(self, data)

        return setBHWrapper

    @_set_BH_decorator
    def set_BH(self, newBH: NDArray, temp: float = None):
        """setter of BH curve.

        Args:
            BH (numpy.ndarray): BH curve (2D array) with shape (X,2) ->
                [[B1, H1],[B2, H2],[B3, H3],...].
            temperature (float): temperature of the curve. defaults to None (meaning
                default temperature).
        """
        if not hasattr(self, "_BH"):
            self._BH = {}
        if not temp:
            temp_key = "default"
        else:
            temp_key = temp
        if newBH is None:
            # if BH is None, set empty array
            self._BH[temp_key] = np.empty(0)
            if temp_key == "default":
                self.linear = True
        elif isinstance(newBH, list):
            # if list is given, set numpy array
            # RECALL SETTER to check valid BH shape
            # self.linear = False # no need to set here because setter is
            # recalled
            self._BH[temp_key] = np.array(newBH)
            self.linear = False
        elif isinstance(newBH, np.ndarray):
            if newBH.ndim == 2:
                # number of dimensions must be 2
                if newBH.shape[1] == 2:
                    # number of coloums must be 2 for B and H
                    if newBH.shape[0] < 2:
                        raise ValueError(
                            (
                                "Too few points in BH curve of material %s! At least specify 2 value pairs.",
                                self.name,
                            )
                        )
                    if newBH.shape[0] < 6:
                        logger.warning(
                            "Only %i point in BH curve of material %s! Results might be inaccurate.",
                            newBH.shape[0],
                            self.name,
                        )
                    # set BH curve
                    self._BH[temp_key] = newBH
                    self.linear = False
                else:
                    raise (
                        ValueError(
                            f"Wrong shape of array BH. Must be (X,2) but is {newBH.shape}. "
                            + "BH must look like [[B1, H1],[B2, H2],[B3, H3],...]"
                        )
                    )
            else:
                raise (
                    ValueError(
                        f"Wrong number of dimensions of array BH. 'ndim' must be 2 but is {newBH.ndim}. "
                        + "BH must look like [[B1, H1],[B2, H2],[B3, H3],...]"
                    )
                )
        else:
            raise (
                ValueError(
                    f"Wrong type for BH curve ({type(newBH)}). BH curve must be type numpy.ndarraywith shape: "
                    + "[[B1, H1],[B2, H2],[B3, H3],...]"
                )
            )

    @name.setter
    def name(self, name: str):
        """set the material name

        Args:
            name (str): new material name
        """
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Material name must be type str.")

    @conductivity.setter
    def conductivity(self, conductivity: Union[float, int, None]):
        """set the electrical conductivity of the material

        Args:
            conductivity (Union[float, int]): electrical conductivity in S/m
        """
        if conductivity is None:
            self._conductivity = None
        elif isinstance(conductivity, (int, float)):
            if conductivity > 0:
                self._conductivity = conductivity
            elif conductivity == 0:
                # if zero than non-conductings
                self._conductivity = None
            else:
                # negative conductivity...
                raise ValueError(
                    "Conductivy can not be negative!" f"Given value: {conductivity}"
                )

        else:
            raise ValueError("Conductivity must be numeric.")

    @relPermeability.setter
    def relPermeability(self, relPermeability: Union[float, int]):
        """set the relative permeability of the material

        Args:
            relPermeability (Union[float, int]): relative permeability
        """
        if isinstance(relPermeability, (int, float)) or relPermeability is None:
            self._relPermeability = relPermeability
        else:
            raise ValueError("Relative permeability must be numeric.")

    @remanence.setter
    def remanence(self, remanence: Union[float, int]):
        """set the remanence of the material

        Args:
            remanence (Union[float, int]): remanent flux density in [T]
        """
        if isinstance(remanence, (int, float)) or remanence is None:
            self._remanence = remanence
        else:
            raise ValueError("Remanent flux density must be numeric.")

    @tempCoefRem.setter
    def tempCoefRem(self, new_temp_coef: float):
        """setter for temperature coefficient of Br

        Args:
            new_temp_coef (float): temperature coefficient of Br

        Raises:
            ValueError: If given value is not numeric.
        """
        # ("br_" = f"{br20} * (1 + ({tempCoef} * (tempMag - 20)))", "Reference temperatur is 20°C",
        if isinstance(new_temp_coef, (int, float)) or new_temp_coef is None:
            self._tempCoefRem = new_temp_coef
        else:
            raise ValueError(
                "Remanence flux density temperature coefficient must be numeric."
                f"But is type {type(new_temp_coef)} of value: {new_temp_coef}"
            )

    @property
    def density(self):
        """Get density of the material in kg/m³

        Returns:
            Union[float, None]: Density in kg/m³
        """
        return self._density

    @density.setter
    def density(self, density: float) -> None:
        """set the density of the material in kg/m³

        Args:
            density (float): density of the material in kg/m³

        Raises:
            TypeError: if given density if not numeric or None
            ValueError: if the given density is a negative number
        """
        if density is None:
            self._density = None
            return None
        elif isinstance(density, (int, float)):
            if density >= 0:
                self._density = density
                return None
            else:
                raise (
                    ValueError(
                        f"Value for material density must be a positive number, but is '{density}'"
                    )
                )
        else:
            raise (
                TypeError(
                    f"Density of material must be a numeric value but is '{type(density)}':{density}"
                )
            )

    @property
    def thermalConductivity(self):
        """get the thermal conductivity of the material in W/(m*K)

        Returns:
            float | None: thermal conductivity of the material in W/(m*K)
        """
        return self._thermalConductivity

    @thermalConductivity.setter
    def thermalConductivity(self, thermalConductivity: float) -> None:
        """set the thermal conductivity of the material in W/(m*K)

        Args:
            thermalConductivity (float): [description]
        Raises:
            TypeError: if given thermal conductivity if not numeric or None
            ValueError: if the given thermal conductivity is a negative number
        """
        if thermalConductivity is None:
            self._thermalConductivity = None
            return None
        elif isinstance(thermalConductivity, (int, float)):
            if thermalConductivity >= 0:
                self._thermalConductivity = thermalConductivity
                return None
            else:
                raise (
                    ValueError(
                        f"Value for material thermal conductivity must be a positive number, but is '{thermalConductivity}'"
                    )
                )
        else:
            raise (
                TypeError(
                    f"thermal conductivity of material must be a numeric value but is '{type(thermalConductivity)}':{thermalConductivity}"
                )
            )

    @property
    def thermalCapacity(self):
        """get the thermalCapacity of the material in W/(m*K)

        Returns:
            float | None: thermalCapacity of the material in J/(kg*K)
        """
        return self._thermalConductivity

    @thermalCapacity.setter
    def thermalCapacity(self, thermalCapacity: float) -> None:
        """set the thermalCapacity of the material in J/(kg*K)

        Args:
            thermalCapacity (float): thermal capacity in J/(kg*K)
        Raises:
            TypeError: if given thermalCapacity if not numeric or None
            ValueError: if the given thermalCapacity is a negative number
        """
        if thermalCapacity is None:
            self._thermalCapacity = None
            return None
        elif isinstance(thermalCapacity, (int, float)):
            if thermalCapacity >= 0:
                self._thermalCapacity = thermalCapacity
                return None
            else:
                raise (
                    ValueError(
                        f"Value for material thermalCapacity must be a positive number, but is '{thermalCapacity}'"
                    )
                )
        else:
            raise (
                TypeError(
                    f"thermalCapacity of material must be a numeric value but is '{type(thermalCapacity)}':{thermalCapacity}"
                )
            )

    @property
    def linear(self) -> bool:
        """Property for linearity of material. Material is linear if it has no
        ferromagnetic BH curve defined.

        Returns:
            bool: Flag if material is linear
        """
        return self._linear

    @linear.setter
    def linear(self, is_linear: bool):
        """setter of property linear

        Args:
            is_linear (bool): flag if material is linear (has no BH curve).
        """
        if isinstance(is_linear, bool):
            if is_linear and self.BH.size != 0:
                logger.warning(
                    "Material %s was set linear and has BH curve!", self.name
                )
            self._linear = is_linear
        else:
            raise ValueError("Attribute linear must be type bool.")

    def print(self) -> None:
        """print material to stdout"""
        table = [
            ["Name:", self.name],
            ["Is linear:", "Yes" if self.linear else "No"],
            ["Electrical Conductivity [S/m]:", self.conductivity],
            ["Relative Permeability []:", self.relPermeability],
            ["Remanence Flux Density[T]:", self.remanence],
            ["Density [kg/m³]:", self.density],
            ["Thermal Conductivity [W/(m*K)]:", self.thermalConductivity],
            ["Thermal Capacity [J/(kg*K)]:", self.thermalCapacity],
        ]
        for row in table:
            if row[1] is None:
                row[1] = "None"  # set to string because formatting None not supported
            print(f"{row[0]: >30} {row[1]: <15}")
        print("\n")
