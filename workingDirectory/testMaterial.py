from sys import path
from os.path import abspath, join, dirname
from matplotlib import pyplot as plt

try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
print(f'rootname is "{rootname}"')
path.append(rootname)


from pyemmo.script.material.material import Material
from pyemmo.definitions import RESULT_DIR, MAIN_DIR

air = Material(
    name="Air",
    conductivity=None,
    relPermeability=1,
    remanence=None,
    density=1.225,
    thermalConductivity=0.0262,
    thermalCapacity=1.005,
    BH=None,
)
air.print()

from pyemmo.script.material.electricalSteel import ElectricalSteel
import numpy as np

b = [0.0,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,2.0,2.1,2.2,2.3]
h = [0.0,70.0,95.0,120.0,140.0,160.0,180.0,220.0,250.0,280.0,330.0,360.0,400.0,450.0,530.0,640.0,760.0,930.0,1220.0,2100.0,3200.0,4400.0,5700.0,7400.0,9500.0,12000.0,15000.0,23840.0,37100.0,63625.0,143202.0]
steel = ElectricalSteel(
    name="steel_1010",
    conductivity=5e6,
    relPermeability=None,
    BH=np.array([b, h]),
    sheetThickness=0.5e-3,
    lossParams=(0, 0, 0),
    referenceFrequency=0,
    referenceFluxDensity=0
)

plt.plot(h,b, '.-')
