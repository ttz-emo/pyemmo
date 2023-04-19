#%%
from math import ceil
from typing import List
from numpy import sign
import swat_em

def genWindLayout_swat(windingList: List[str], Qs: int, onePole=False) -> List[List[int]]:
    windType = "integer" if windingList[0::2]==windingList[1::2] else "fractional"
    nbrSlotsInList = len(windingList)/2
    nbrRepeat = Qs/nbrSlotsInList
    if nbrRepeat.is_integer() and nbrSlotsInList.is_integer():
        nbrRepeat = int(nbrRepeat)
        nbrSlotsInList = int(nbrSlotsInList)
    # if windType == "integer":
    #     # only one phase per slot
    #     listU = [i for i,phase in enumerate(windingList) if phase=="+u"]
    #     listU.extend([-i for i,phase in enumerate(windingList) if phase=="-u"])
    if windType == "fractional":
        windLayout = [[[],[]],[[],[]],[[],[]]]
        for segment in range(nbrRepeat):
            offset = segment*nbrSlotsInList
            for slotID, phaseID in enumerate(windingList):
                phaseID = phaseID.replace("u","1")
                phaseID = phaseID.replace("v","2")
                phaseID = phaseID.replace("w","3")
                windLayout[abs(int(phaseID))-1][(slotID+1)%2].append(sign(int(phaseID))*(ceil((slotID+1)/2)+offset))
                # if slotID%2==0:
                #     # left slot side
                #     windLayout[abs(int(phaseID))-1][1].append(sign(int(phaseID))*ceil((slotID+1)/2))
                # else:
                #     #right slot side
                #     windLayout[abs(int(phaseID))-1][0].append(sign(int(phaseID))*ceil((slotID+1)/2))
    elif windType == "integer":
        windLayout = [[],[],[]]
        for segment in range(nbrRepeat):
            offset = segment*nbrSlotsInList
            if onePole:
                signChange = (-1 if segment%2 else 1)
            for slotID, phaseID in enumerate(windingList):
                if slotID%2==0:
                    phaseID = phaseID.replace("u","1")
                    phaseID = phaseID.replace("v","2")
                    phaseID = phaseID.replace("w","3")
                    phaseNum = abs(int(phaseID))-1
                    slotNum = ceil((slotID+1)/2)+offset
                    windDir = signChange*sign(int(phaseID))
                    windLayout[phaseNum].append(windDir*slotNum)
    else:
        raise(ValueError("Winding type is not 'integer' or 'factional'"))
    return windLayout

#%% WINDING 1: TOOTH COIL
# windList = ['+u', '-v', '+v', '-w', '+w', '-u'] # winding configuration import from matlab -> IPM
# Qs = 12
# pp = 4

# wdg1 = swat_em.datamodel()
# wdg1.set_machinedata(Q=Qs, p=pp, m=3)
# windLayout = genWindLayout_swat(windList, Qs)
# print(windLayout)

# wdg1.set_phases(S=windLayout)
# wdg1.analyse_wdg()
# wdg1.plot_layout(filename=".\test_swat-em_layout.png", res=[800,600], show=True)
# wdg1.plot_windingfactor(filename=".\test_swat-em_windFactor.png", res=[800,600], show=True)
#%% WICKLUNG 2: VERTEILT
from pydraft.api.emma_onelab import genWindLayout_swat
windList = ['+u','+u','+u','+u','+u','+u','-v','-v','-v','-v','-v','-v','+w','+w','+w','+w','+w','+w']
# windList = ['+u','+u','+u','+u','+u','+u','-w','-w','-w','-w','-w','-w','+v','+v','+v','+v','+v','+v']
# windListMod = [[[-3,-6,-9,-12], [1,4,7,10]], [[-1,-4,-7,-10], [2,5,8,11]], [[-2,-5,-8,-11],[3,6,9,12]]] # winding configuration import from matlab
Qs = 18
pp = 1

wdg2 = swat_em.datamodel()
wdg2.set_machinedata(Q=Qs, p=pp, m=3)
windLayout = genWindLayout_swat(windList, Qs, True)
print("\nWinding layout for swat-em:\n",windLayout)
wdg2.set_phases(S=windLayout)
wdg2.analyse_wdg()
#%% Post Processing
# wdg2.plot_layout(filename=".\test_swat-em_layout.png", res=[800,600], show=True)
# wdg2.plot_star(filename=".\test_swat-em_star.png", res=[800,600], show=True, ForceX=False)
kw1 = wdg2.get_windingfactor_el_by_nu(1)
print("\nWinding factor of first electrical harmonic:\n",kw1)
# %% Get phase angle of MMF fundamental
from numpy import where,rad2deg
(order, amp, phase) = wdg2.get_MMF_harmonics() 
FundPhase = round(float(rad2deg(phase[where(order==1)])),2)
print(f"Angle offset of fundamental is: {FundPhase}°")