"""test module for time derivative calculation"""
from pyemmo.functions.calcIronLoss import calcTimeDerivative
bRotorPath = r"C:\Users\ganser\AppData\Local\Programs\pyemmo\workingDirectory\testCalcDerivative\b_rotor.pos"
bStatorPath = r"C:\Users\ganser\AppData\Local\Programs\pyemmo\workingDirectory\testCalcDerivative\b_stator.pos"
calcTimeDerivative(bRotorPath)
