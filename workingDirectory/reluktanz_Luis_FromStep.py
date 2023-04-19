from setPath import pathRes
import pydraft as pyd
import math
from stepToPyDraft import getAdaptedPath, changeToPyDraftObjects

myScript = pyd.Script('Reluktanz', pathRes)
pathStepDir = r'C:\Users\koenig\Desktop\Maschine_Luis'


objPath = getAdaptedPath(pathStepDir)
pyDraftObj = changeToPyDraftObjects(objPath, unit = 1)

phy_phase_U_pos = pyd.PhysicalElement('Phase_U_pos', pyDraftObj['sur_phase_U_pos'], None, 2100)
phy_phase_U_neg = pyd.PhysicalElement('Phase_U_neg', pyDraftObj['sur_phase_U_neg'], None, 2101)
phy_phase_V_pos = pyd.PhysicalElement('Phase_V_pos', pyDraftObj['sur_phase_V_pos'], None, 2102)
phy_phase_V_neg = pyd.PhysicalElement('Phase_V_neg', pyDraftObj['sur_phase_V_neg'], None, 2103)
phy_phase_W_pos = pyd.PhysicalElement('Phase_W_pos', pyDraftObj['sur_phase_W_pos'], None, 2104)
phy_phase_W_neg = pyd.PhysicalElement('Phase_W_neg', pyDraftObj['sur_phase_W_neg'], None, 2105)
phy_StatorSheet = pyd.PhysicalElement('StatorSheet', pyDraftObj['sur_StatorSheet'], None, 2001)
phy_AirSlot = pyd.PhysicalElement('AirSlot', pyDraftObj['sur_AirSlot'], None, 2002)
phy_AirGapStator = pyd.PhysicalElement('AirGapStator', pyDraftObj['sur_AirGapStator'], None, 2003)
phy_RotorSheet = pyd.PhysicalElement('RotorSheet', pyDraftObj['sur_RotorSheet'], None, 1001)
phy_RotorSeg = pyd.PhysicalElement('RotorSeg', pyDraftObj['sur_RotorSeg'], None, 1002)
phy_RotorAir = pyd.PhysicalElement('RotorAir', pyDraftObj['sur_RotorAir'], None, 1004)
phy_AirGapRotor = pyd.PhysicalElement('AirGapRotor', pyDraftObj['sur_AirGapRotor'], None, 1003)

phy_outerLineLimit = pyd.PhysicalElement('OuterLineLimit', pyDraftObj['curve_outerLineLimit'], None, 20001)
phy_statorSlave = pyd.PhysicalElement('StatorSlave', pyDraftObj['curve_statorSlave'], None, 20011)
phy_statorMaster = pyd.PhysicalElement('StatorMaster', pyDraftObj['curve_statorMaster'], None, 20012)
phy_statorMB = pyd.PhysicalElement('StatorMB', pyDraftObj['curve_statorMB'], None, 20020)

phy_innerLineLimit = pyd.PhysicalElement('InnerLineLimit', pyDraftObj['curve_innerLineLimit'], None, 10001)
phy_rotorSlave = pyd.PhysicalElement('RotorSlave', pyDraftObj['curve_rotorSlave'], None, 10011)
phy_rotorMaster = pyd.PhysicalElement('RotorMaster', pyDraftObj['curve_rotorMaster'], None, 10012)
phy_rotorMB1 = pyd.PhysicalElement('RotorMB1', pyDraftObj['curve_rotorMB1'], None, 10020)
phy_rotorMB2 = pyd.PhysicalElement('RotorMB2', pyDraftObj['curve_rotorMB2'], None, 10021)

phy_contour = pyd.PhysicalElement('Contour', pyDraftObj['curve_Contour'], None, 1111111)


domainMaschine = pyd.Domain('domainMaschine', [phy_phase_U_pos, phy_phase_U_neg, phy_phase_V_pos, phy_phase_V_neg, phy_phase_W_pos, phy_phase_W_neg, phy_StatorSheet, phy_AirSlot, \
    phy_AirGapStator, phy_RotorSheet, phy_RotorSeg, phy_RotorAir, phy_AirGapRotor, phy_outerLineLimit, phy_statorSlave, phy_statorMaster, phy_statorMB, \
    phy_innerLineLimit, phy_rotorSlave, phy_rotorMaster, phy_rotorMB1, phy_rotorMB2, phy_contour])
domainMaschine.addToScript(myScript)

#.geo-Datei erzeugen
myScript.generateScript()

print('done')