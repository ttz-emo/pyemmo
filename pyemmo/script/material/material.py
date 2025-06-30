#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO,
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
"""Module for Material-class"""


# pylint: disable=line-too-long

import json
import os
import warnings
from typing import Union

import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray

from ... import rootLogger as logger
from . import DATABASE_PATH


class Material:
    """Class Material defines a material for the simulation with onelab"""

    def __init__(
        self,
        name: str,
        conductivity: float = 0.0,
        relPermeability: float = 1.0,
        remanence: float = 0.0,
        tempCoefRem: float = 0.0,
        BH: NDArray = np.empty(0),
        density: float = 0.0,
        thermalConductivity: float = 0.0,
        thermalCapacity: float = 0.0,
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
        if not isinstance(__o, self.__class__):
            return False  # Wrong compare instance type!
        # check BH is equal:
        try:
            if self.BH.shape == __o.BH.shape:
                # if comparison results in ValueError, shapes could not be broadcasted
                bh_comp = np.all(self.BH == __o.BH)
            else:
                return False  # wrong BH shape
        except ValueError:
            # comparison with empty array returns a ValueError
            return False
        except Exception as exce:
            raise exce
        if bh_comp:
            # matching BH arrays -> check rest of attributes by dict without BH
            selfDict = self.__dict__.copy()
            del selfDict["_BH"]
            otherDict = __o.__dict__.copy()
            del otherDict["_BH"]
            return selfDict == otherDict
        return False  # BH comparison was False

    def __str__(self) -> str:
        """string representation of material"""
        str_repr = []
        for key, value in [
            ("Name", self.name),
            ("Is linear", "Yes" if self.linear else "No"),
            ("Electrical Conductivity [S/m]", self.conductivity),
            ("Relative Permeability []", self.relPermeability),
            ("Remanence Flux Density[T]", self.remanence),
            ("Density [kg/m³]", self.density),
            ("Thermal Conductivity [W/(m*K)]", self.thermalConductivity),
            ("Thermal Capacity [J/(kg*K)]", self.thermalCapacity),
        ]:
            if value is not None:
                str_repr.append(f"{key:>35}: {value:<15}")
            else:
                str_repr.append(f"{key:>35}: None")
        return "\n".join(str_repr)

    @classmethod
    def load(cls, mat_name):
        """Function to load material from JSON database.

        Args:
            materialName (str): Material name to load the Material from the
                database.

        FIXME: save/load methods do not pay attention to properties:
            - tempCoefRem
            - density
            - thermalConductivity
            - thermalCapacity

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
        # remove keys that are not kwargs of Material
        mat_dict.pop("ID")
        mat_dict.pop("linear")
        return cls.from_dict(mat_dict)

    @classmethod
    def from_dict(cls, mat_dict: dict) -> "Material":
        """Create a instance of Material from a data dictionary, which contains
        all relevant material properties"""
        if mat_dict["BHCurve"] == {}:
            bh_curve = np.empty(0)  # default value for empty
        else:
            bh_curve = mat_dict["BHCurve"]["default"]

        mat_dict["BH"] = bh_curve
        mat_dict.pop("BHCurve")
        return cls(**mat_dict)

    def as_dict(self) -> dict:
        mat_dict = {}
        mat_dict["name"] = self.name
        mat_dict["conductivity"] = self.conductivity
        mat_dict["relPermeability"] = self.relPermeability
        mat_dict["remanence"] = self.remanence
        mat_dict["linear"] = self.linear
        mat_dict["BHCurve"] = {}
        if not self.linear:
            for temp_key in self._BH.keys():
                mat_dict["BHCurve"][temp_key] = self.get_BH(temp_key).tolist()
        mat_dict["tempCoefRem"] = self.tempCoefRem
        mat_dict["density"] = self.density
        mat_dict["thermalConductivity"] = self.thermalConductivity
        mat_dict["thermalCapacity"] = self.thermalCapacity
        return mat_dict

    def save(self):
        """Save the material to the material data base a JSON file.

        You can find the Material database under
        `pyemmo.script.material.DATABASE_PATH`.

        The default save path is 'DATABASE_PATH/*MATERIAL_NAME*.json'
        """
        if self.name == "":
            raise RuntimeError("Material needs to have a name!")
        # create dict from material object
        mat_dict = self.as_dict()
        # add ID to material
        mat_dict["ID"] = len([f for f in os.listdir(DATABASE_PATH) if ".json" in f]) + 1
        with open(
            os.path.join(DATABASE_PATH, f"{self.name}.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(mat_dict, file, indent="\t")

    def delete(self):
        json_path = os.path.join(DATABASE_PATH, f"{self.name}.json")
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
        """
        if self.linear:
            warnings.warn("Material is linear, there is no BH-curve")
            return
        if temp is None:
            for t in self.BH.keys():
                if self._BH[t].size:
                    h = [row[0] for row in self._BH[t]]
                    b = [row[1] for row in self._BH[t]]
                    if t == "default":
                        label = t
                    else:
                        label = f"{t}°C"
                    plt.plot(h, b, label=label)
        else:
            BH_vals = self.get_BH(temp)
            h = [row[0] for row in BH_vals]
            b = [row[1] for row in BH_vals]
            if temp not in self._BH.keys():
                label = "default"
            else:
                label = f"{temp}°C"
            plt.plot(h, b, label=label)
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
        plt.show(block=True)

    @property
    def name(self) -> str:
        """getter of material name

        Returns:
            str: name of the material
        """
        return self._name

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

    @property
    def conductivity(self) -> Union[float, int]:
        """get electrical conductivity

        Returns:
            Union[float, int]: electrical conductivity in S/m. 0 if
            not conductive.
        """
        return self._conductivity

    @conductivity.setter
    def conductivity(self, conductivity: Union[float, int]):
        """set the electrical conductivity of the material

        Args:
            conductivity (Union[float, int]): electrical conductivity in S/m
        """
        if isinstance(conductivity, (int, float)):
            if conductivity >= 0:
                self._conductivity = conductivity
            else:
                # negative conductivity...
                raise ValueError(
                    "Conductivy can not be negative!" f"Given value: {conductivity}"
                )
        else:
            raise TypeError("Conductivity must be numeric.")

    @property
    def relPermeability(self) -> Union[float, int]:
        """get linear relative magnetic permeability

        Returns:
            Union[float, int]: linear relative permeability
        """
        return self._relPermeability

    @relPermeability.setter
    def relPermeability(self, relPermeability: Union[float, int]):
        """set the relative permeability of the material

        Args:
            relPermeability (Union[float, int]): relative permeability
        """
        if isinstance(relPermeability, (int, float)):
            if relPermeability > 0:
                self._relPermeability = relPermeability
            else:
                raise ValueError(
                    "Relative permeability must be a positive number, but is "
                    f"'{relPermeability}'"
                )
        else:
            raise ValueError("Relative permeability must be numeric.")

    @property
    def remanence(self) -> Union[float, int]:
        """get remanent flux density at 20°C

        Returns:
            Union[float, int]: remanent flux density (Br) in T at 20°C
        """
        return self._remanence

    @remanence.setter
    def remanence(self, remanence: Union[float, int]):
        """Set the remanence flux density in T of permanent magnet material of
        the material. Must be a positive number or zero (no remanence).

        Args:
            remanence (Union[float, int]): remanent flux density in [T]
        """
        if isinstance(remanence, (int, float)):
            if remanence >= 0:
                self._remanence = remanence
            else:
                raise ValueError(
                    "Remanent flux density must be a positive number, but is "
                    f"'{remanence}'"
                )
        else:
            raise ValueError("Remanent flux density must be numeric.")

    @property
    def tempCoefRem(self) -> Union[float, int]:
        """Get the temperature coefficient of the remanent flux density.
        Formula for remanent flux density at temperature `tempMag` in °C is:

        .. math::
            B_{r}(tempMag) =  b_{r,20°C} * (1 + ({tempCoef} * (tempMag - 20)))"

        Returns:
            Union[float, int]: temperatur coefficient of remanent flux density in 1/K
        """
        return self._tempCoefRem

    @tempCoefRem.setter
    def tempCoefRem(self, new_temp_coef: Union[int, float]):
        """setter for temperature coefficient of Br

        Args:
            new_temp_coef (float): temperature coefficient of Br

        Raises:
            ValueError: If given value is not numeric.
        """
        # ("br_" = f"{br20} * (1 + ({tempCoef} * (tempMag - 20)))", "Reference temperatur is 20°C",
        if isinstance(new_temp_coef, (int, float)):
            if new_temp_coef < 0:
                raise ValueError(
                    "Remanence flux density temperature coefficient must be a positive number, "
                    f"but is '{new_temp_coef}'"
                )
            self._tempCoefRem = new_temp_coef
        else:
            raise ValueError(
                "Remanence flux density temperature coefficient must be numeric."
                f"But is type {type(new_temp_coef)} of value: {new_temp_coef}"
            )

    # pylint: disable=invalid-name
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
            return np.array(self._BH["default"])
        try:
            return np.array(self._BH[temperature])
        except KeyError:
            if self.linear:
                logger.warning(
                    (
                        "Tried to access the BH-curve for temperature %.2f°C, "
                        "but BH-Curve is linear!"
                    ),
                    temperature,
                )
                return np.empty(0)
            if len(self._BH.keys()) < 2:
                logger.warning(
                    (
                        "Tried to access the BH-curve for temperature %.2f°C, "
                        "but there is only one BH-curve specified!"
                    ),
                    temperature,
                )
                return np.array(self._BH["default"])
            logger.warning(
                "No BH-curve registered for temperature %.2f°C!", temperature
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

        NOTE: this sets the curve for the default temperature only. Use set_BH() to set
        BH Curve for specific temperature
        """

        self.set_BH(newBH)

    # def _set_BH_decorator(set_BH):
    #     """
    #     decorator to extend the function of set_BH to also accepts dict or file path
    #     """

    #     def setBHWrapper(self, data, temp: float = None):
    #         if isinstance(data, dict):
    #             if len(data) < 1:
    #                 raise (ValueError("There is no BH data to add!"))
    #             for temp in data.keys():
    #                 temp_key = lambda: ("default" if temp == "no information" else temp)
    #                 set_BH(self, data[temp], temp_key())
    #         elif isinstance(data, str):
    #             try:
    #                 file = pd.read_table(data)
    #             except UnicodeDecodeError:
    #                 file = pd.read_excel(data)
    #             except FileNotFoundError:
    #                 warnings.warn("Cannot load, file does not exist")
    #                 return
    #             allValue = file.values
    #             try:
    #                 temp_list = {row[2] for row in allValue}
    #                 for temp in temp_list:
    #                     if temp == "no information":
    #                         temp_key = "default"
    #                     else:
    #                         temp_key = temp
    #                     set_BH(
    #                         self,
    #                         [[row[0], row[1]] for row in allValue if row[2] == temp],
    #                         temp_key,
    #                     )
    #             except IndexError:
    #                 set_BH(self, [[row[0], row[1]] for row in allValue])
    #         else:
    #             set_BH(self, data)

    #     return setBHWrapper

    # @_set_BH_decorator
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
            raise TypeError("BH curve cant be of type None")
        if not isinstance(newBH, (np.ndarray, list)):
            raise TypeError("BH curve must be numpy.ndarray or list of lists")
        if len(newBH) == 0:
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

    @property
    def density(self):
        """Get density of the material in kg/m³

        Returns:
            Union[float]: Density in kg/m³
        """
        return self._density

    @density.setter
    def density(self, density: float):
        """set the density of the material in kg/m³

        Args:
            density (float): density of the material in kg/m³

        Raises:
            TypeError: if given density if not numeric
            ValueError: if the given density is a negative number
        """
        if isinstance(density, (int, float)):
            if density >= 0:
                self._density = density
            else:
                raise (
                    ValueError(
                        "Value for material density must be a positive number,"
                        f"but is '{density}'"
                    )
                )
        else:
            raise (
                TypeError(
                    "Density of material must be a numeric value but is "
                    f"'{type(density)}':{density}"
                )
            )

    @property
    def thermalConductivity(self):
        """get the thermal conductivity of the material in W/(m*K)

        Returns:
            float: thermal conductivity of the material in W/(m*K)
        """
        return self._thermalConductivity

    @thermalConductivity.setter
    def thermalConductivity(self, thermalConductivity: float):
        """set the thermal conductivity of the material in W/(m*K)

        Args:
            thermalConductivity (float): thermal conductivity in W/(m*K)
        Raises:
            TypeError: if given thermal conductivity if not numeric
            ValueError: if the given thermal conductivity is a negative number
        """
        if isinstance(thermalConductivity, (int, float)):
            if thermalConductivity >= 0:
                self._thermalConductivity = thermalConductivity
            else:
                raise (
                    ValueError(
                        "Value for material thermal conductivity must be a"
                        f"positive number, but is '{thermalConductivity}'"
                    )
                )
        else:
            raise (
                TypeError(
                    "thermal conductivity of material must be a numeric value "
                    f"but is '{type(thermalConductivity)}':{thermalConductivity}"
                )
            )

    @property
    def thermalCapacity(self):
        """get the thermalCapacity of the material in W/(m*K)

        Returns:
            float | None: thermalCapacity of the material in J/(kg*K)
        """
        return self._thermalCapacity

    @thermalCapacity.setter
    def thermalCapacity(self, thermalCapacity: Union[int, float]):
        """set the thermalCapacity of the material in J/(kg*K)

        Args:
            thermalCapacity (float): thermal capacity in J/(kg*K)
        Raises:
            TypeError: if given thermalCapacity if not numeric
            ValueError: if the given thermalCapacity is a negative number
        """
        if isinstance(thermalCapacity, (int, float)):
            if thermalCapacity >= 0:
                self._thermalCapacity = thermalCapacity
            else:
                raise (
                    ValueError(
                        "Value for material thermalCapacity must be a positive"
                        f" number, but is '{thermalCapacity}'"
                    )
                )
        else:
            raise (
                TypeError(
                    "thermalCapacity of material must be a numeric value but "
                    f"is '{type(thermalCapacity)}':{thermalCapacity}"
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
        """print the material information to console"""
        print(str(self))
