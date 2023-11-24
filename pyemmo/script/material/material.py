"""Module for Material-class"""
# pylint: disable=line-too-long

from typing import Union
import warnings
import numpy

from .materialManagement import getMaterial

class Material(object):
    """Class Material defines a material for the simulation with onelab"""

    def __init__(
        self,
        name: str = "",
        conductivity: float = None,
        relPermeability: float = None,
        remanence: float = None,
        tempCoefRem: float = None,
        BH: numpy.ndarray = None,
        density: float = None,
        thermalConductivity: float = None,
        thermalCapacity: float = None,
    ):
        # FIXME: Check input values for valid type
        self._name = name
        self._conductivity = conductivity
        self._relPermeability = relPermeability
        self._remanence = remanence
        self._tempCoefRem = (
            tempCoefRem  # coefficient for temperature dependency of remanent B
        )
        if tempCoefRem and not remanence:
            warnings.warn(
                "Temperature coefficient for Br is given without value for Br!"
            )
        if isinstance(BH, numpy.ndarray):
            self._BH = BH
            linear = (
                False if BH.size else True
            )  # material is linear if BH curve is given AND not empty
        elif BH is None:
            self._BH = numpy.empty(0)
            linear = True
        else:
            raise ValueError(f"BH curve must be numpy.ndarray, but is {type(BH)}!")

        self._density = density
        self._thermalConductivity = thermalConductivity
        self._thermalCapacity = thermalCapacity
        self._linear = linear

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            # check BH is equal:
            try:
                #FIXME: Maybe check shapes before...
                # if comparison results in ValueError, shapes could not be broadcasted
                bhComp = self.getBH() == __o.getBH()
            except ValueError:
                # comparison with empty array returns a ValueError
                return False
            except Exception as exce:
                raise exce
            if not isinstance(bhComp, bool):
                # comparison with not empty array returns ndarray with dtype:bool
                if isinstance(bhComp, numpy.ndarray):
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
            else:
                return False
        else:
            return False

    def loadMatFromDataBase(self, dataBase: str, name: str) -> None:
        """Load data for the material from a database by name.

        You could load a material with the following code:

        .. code:: python

            ndFe35 = Material() # create a Material object
            # load the data for this material
            ndFe35.loadMatFromDataBase("Material_new.db", "NdFe35")


        Args:
            dataBase (str): Name of the database (not path...).
            name (str): Material name.
        """
        rawMat = getMaterial(dataBase, name)
        self.setName(rawMat["name"])
        self.setConductivity(rawMat["conductivity"])
        self.setRelPermeability(rawMat["relPermeability"])
        # remanence can be string "no information"...
        if isinstance(rawMat["remanence"], str):
            self.setRemanence(0)
        else:
            self.setRemanence(rawMat["remanence"])
        self.setLinear(rawMat["linear"])
        if not self.isLinear():
            # if material is nonlinear load BH
            self.setBH(rawMat["BH"])

    def isLinear(self) -> bool:
        """check if the material is linear or has BH curve

        Returns:
            bool: True if material doesn't have a BH curve, but a relative permeability.
            Otherwise Flase
        """
        if self._linear and self.getBH().size:
            # pylint: disable=locally-disabled,  line-too-long
            warnings.warn(
                f"Linearity flag of material '{self.getName()}' is True although BH-curve is not empty!"
            )
        return self._linear

    def setLinear(self, linear: bool) -> None:
        """set the linearity of the material

        Args:
            linear (bool): True if material is linear, otherwise False
        """
        if isinstance(linear, bool):
            self._linear = linear
        else:
            raise ValueError("Attribute linear must be type bool.")

    def getName(self) -> str:
        """getter of material name

        Returns:
            str: name of the material
        """
        return self._name

    def getConductivity(self) -> Union[float, int, None]:
        """get electrical conductivity

        Returns:
            Union[float, int, None]: electrical conductivity in S/m
        """
        return self._conductivity

    def getRelPermeability(self) -> Union[float, int, None]:
        """get relative magnetic permeability

        Returns:
            Union[float, int, None]: relative permeability in []
        """
        return self._relPermeability

    def getRemanence(self) -> Union[float, int, None]:
        """get remanent flux density

        Returns:
            Union[float, int, None]: remanent flux density (Br) in T
        """
        return self._remanence

    def getTempCoefRem(self) -> Union[float, int, None]:
        """Get the temperature coefficient of the remanent flux density.

        Returns:
            Union[float, int, None]: temperatur coefficient of remanent flux density in 1/K
            ("one per Kelvin")
        """
        return self._tempCoefRem

    def getBH(self, temperature: float = None) -> numpy.ndarray:
        if not temperature:
            return self._BH
        if self._BH.ndim < 3:
            # pylint: disable=locally-disabled,  line-too-long
            warnings.warn(
                f"Tried to access the BH-curve for temperature {temperature}°C, but there is only one BH-curve specified!",
                UserWarning,
            )
            return self._BH
        # else:
        assert self._BH.ndim == 3
        # TODO: implement temperature depended bh curve

    def setName(self, name: str):
        """set the material name

        Args:
            name (str): new material name
        """
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Material name must be type str.")

    def setConductivity(self, conductivity: Union[float, int]):
        """set the electrical conductivity of the material

        Args:
            conductivity (Union[float, int]): electrical conductivity in S/m
        """
        if isinstance(conductivity, (int, float)) or conductivity is None:
            self._conductivity = conductivity
        else:
            raise ValueError("Conductivity must be numeric.")

    def setRelPermeability(self, relPermeability: Union[float, int]):
        """set the relative permeability of the material

        Args:
            relPermeability (Union[float, int]): relative permeability
        """
        if isinstance(relPermeability, (int, float)) or relPermeability is None:
            self._relPermeability = relPermeability
        else:
            raise ValueError("Relative permeability must be numeric.")

    def setRemanence(self, remanence: Union[float, int]):
        """set the remanence of the material

        Args:
            remanence (Union[float, int]): remanent flux density in [T]
        """
        if isinstance(remanence, (int, float)) or remanence is None:
            self._remanence = remanence
        else:
            raise ValueError("Remanent flux density must be numeric.")

    # pylint: disable=invalid-name
    def setBH(self, BH: numpy.ndarray):
        """setter of BH curve.

        Args:
            BH (numpy.ndarray): BH curve (2D array) with shape (X,2) ->
            [[B1, H1],[B2, H2],[B3, H3],...]
        """
        if BH is None:
            # if BH is None, set empty array
            self._BH = (numpy.empty(0),)
            return None
        if isinstance(BH, list):
            # if list is given, set numpy array
            self.setLinear(False)
            self._BH = numpy.array(BH)
            return None
        if isinstance(BH, numpy.ndarray):
            if BH.ndim == 2:
                # number of dimensions must be 2
                if BH.shape[1] == 2:
                    # number of coloums must be 2
                    self._BH = BH
                    if BH.size > 0:
                        # if the array is not empty, set nonlinear
                        self.setLinear(False)
                    return None
                else:
                    raise (
                        ValueError(
                            f"Wrong shape of array BH. Must be (X,2) but is {BH.shape}. "
                            + "BH must look like [[B1, H1],[B2, H2],[B3, H3],...]"
                        )
                    )
            else:
                raise (
                    ValueError(
                        f"Wrong number of dimensions of array BH. 'ndim' must be 2 but is {BH.ndim}. "
                        + "BH must look like [[B1, H1],[B2, H2],[B3, H3],...]"
                    )
                )
        else:
            raise (
                ValueError(
                    f"Wrong type for BH curve ({type(BH)}). BH curve must be type numpy.ndarraywith shape: "
                    + "[[B1, H1],[B2, H2],[B3, H3],...]"
                )
            )

    def getDensity(self):
        """Get density of the material in kg/m³

        Returns:
            Union[float, None]: Density in kg/m³
        """
        return self._density

    def setDensity(self, density: float) -> None:
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

    def getThermalConductivity(self):
        """get the thermal conductivity of the material in W/(m*K)

        Returns:
            float | None: thermal conductivity of the material in W/(m*K)
        """
        return self._thermalConductivity

    def setThermalConductivity(self, thermalConductivity: float) -> None:
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

    def getThermalCapacity(self):
        """get the thermalCapacity of the material in W/(m*K)

        Returns:
            float | None: thermalCapacity of the material in J/(kg*K)
        """
        return self._thermalConductivity

    def setThermalCapacity(self, thermalCapacity: float) -> None:
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

    def print(self) -> None:
        """print material to stdout"""
        table = [
            ["Name:", self.getName()],
            ["Is linear:", "Yes" if self.isLinear() else "No"],
            ["Electrical Conductivity [S/m]:", self.getConductivity()],
            ["Relative Permeability []:", self.getRelPermeability()],
            ["Remanence Flux Density[T]:", self.getRemanence()],
            ["Density [kg/m³]:", self.getDensity()],
            ["Thermal Conductivity [W/(m*K)]:", self.getThermalConductivity()],
            ["Thermal Capacity [J/(kg*K)]:", self.getThermalCapacity()],
        ]
        for row in table:
            if row[1] is None:
                row[1] = "None"  # set to string because formatting None not supported
            print(f"{row[0]: >30} {row[1]: <15}")
        print("\n")
