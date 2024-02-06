"""Init for API subpackage"""
from ..script.material.material import Material

try:
    air = Material()
    air.loadMatFromDataBase("Material_new.db", "air")
    air.name = "Air"
    air.density = 1.2041
except FileNotFoundError:
    air = Material(
        name="Air",
        conductivity=None,
        relPermeability=1,
        remanence=None,
        density=1.204,
        thermalConductivity=0.0261,
        thermalCapacity=1.005,
    )
air.name = "PYEMMO_AIR"