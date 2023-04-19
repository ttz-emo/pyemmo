from sys import path
from os.path import abspath, join, dirname
from matplotlib import pyplot as plt
 
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\PyDraft_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)


from pydraft.script.material.material import Material
from pydraft.definitions import RESULT_DIR, MAIN_DIR

air = Material(
        name="Air",
        conductivity=None,
        relPermeability=1,
        remanence=None,
        density=1.225,
        thermalConductivity=0.0262,
        thermalCapacity=1.005,
        BH=None,
        linear=True,
    )

air.print()