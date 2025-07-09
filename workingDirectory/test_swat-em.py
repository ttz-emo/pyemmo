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

from __future__ import annotations

# %%
import os
from math import ceil

import swat_em
from numpy import sign

from pyemmo.definitions import RESULT_DIR

TEST_RES_DIR = os.path.join(RESULT_DIR, "swat-em")


# %%
def genWindLayout_swat(
    windingList: list[str], Qs: int, onePole=False
) -> list[list[int]]:
    windType = "integer" if windingList[0::2] == windingList[1::2] else "fractional"
    nbrSlotsInList = len(windingList) / 2
    nbrRepeat = Qs / nbrSlotsInList
    if nbrRepeat.is_integer() and nbrSlotsInList.is_integer():
        nbrRepeat = int(nbrRepeat)
        nbrSlotsInList = int(nbrSlotsInList)
    # if windType == "integer":
    #     # only one phase per slot
    #     listU = [i for i,phase in enumerate(windingList) if phase=="+u"]
    #     listU.extend([-i for i,phase in enumerate(windingList) if phase=="-u"])
    if windType == "fractional":
        windLayout = [[[], []], [[], []], [[], []]]
        for segment in range(nbrRepeat):
            offset = segment * nbrSlotsInList
            for slotID, phaseID in enumerate(windingList):
                phaseID = phaseID.replace("u", "1")
                phaseID = phaseID.replace("v", "2")
                phaseID = phaseID.replace("w", "3")
                windLayout[abs(int(phaseID)) - 1][(slotID + 1) % 2].append(
                    sign(int(phaseID)) * (ceil((slotID + 1) / 2) + offset)
                )
                # if slotID%2==0:
                #     # left slot side
                #     windLayout[abs(int(phaseID))-1][1].append(sign(int(phaseID))*ceil((slotID+1)/2))
                # else:
                #     #right slot side
                #     windLayout[abs(int(phaseID))-1][0].append(sign(int(phaseID))*ceil((slotID+1)/2))
    elif windType == "integer":
        windLayout = [[], [], []]
        for segment in range(nbrRepeat):
            offset = segment * nbrSlotsInList
            if onePole:
                signChange = -1 if segment % 2 else 1
            for slotID, phaseID in enumerate(windingList):
                if slotID % 2 == 0:
                    phaseID = phaseID.replace("u", "1")
                    phaseID = phaseID.replace("v", "2")
                    phaseID = phaseID.replace("w", "3")
                    phaseNum = abs(int(phaseID)) - 1
                    slotNum = ceil((slotID + 1) / 2) + offset
                    windDir = signChange * sign(int(phaseID))
                    windLayout[phaseNum].append(windDir * slotNum)
    else:
        raise (ValueError("Winding type is not 'integer' or 'factional'"))
    return windLayout


# %% WINDING 1: TOOTH COIL
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
# %% WICKLUNG 2: VERTEILT
from pyemmo.api.modelJSON import genWindLayoutSwatEM

windList = [
    "+u",
    "+u",
    "+u",
    "+u",
    "+u",
    "+u",
    "-v",
    "-v",
    "-v",
    "-v",
    "-v",
    "-v",
    "+w",
    "+w",
    "+w",
    "+w",
    "+w",
    "+w",
]
# windList = ['+u','+u','+u','+u','+u','+u','-w','-w','-w','-w','-w','-w','+v','+v','+v','+v','+v','+v']
# windListMod = [[[-3,-6,-9,-12], [1,4,7,10]], [[-1,-4,-7,-10], [2,5,8,11]], [[-2,-5,-8,-11],[3,6,9,12]]] # winding configuration import from matlab
Qs = 18
pp = 1

wdg2 = swat_em.datamodel()
wdg2.set_machinedata(Q=Qs, p=pp, m=3)
windLayout = genWindLayoutSwatEM(windingList=windList, nbrSlots=Qs, onePole=True)
print("\nWinding layout for swat-em:\n", windLayout)
wdg2.set_phases(S=windLayout)
wdg2.analyse_wdg()
# %% Post Processing
# wdg2.plot_layout(filename=".\test_swat-em_layout.png", res=[800,600], show=True)
# wdg2.plot_star(filename=".\test_swat-em_star.png", res=[800,600], show=True, ForceX=False)
kw1 = wdg2.get_windingfactor_el_by_nu(1)
print("\nWinding factor of first electrical harmonic:\n", kw1)
# %% Get phase angle of MMF fundamental
from numpy import rad2deg, where

(order, amp, phase) = wdg2.get_MMF_harmonics()
FundPhase = round(float(rad2deg(phase[where(order == 1)])), 2)
print(f"Angle offset of fundamental is: {FundPhase}°")

# %% Test Simple Winding
wdg3 = swat_em.datamodel()
Qs = 18
pp = 1
wdg3.genwdg(Q=Qs, P=pp * 2, m=3, layers=1, turns=1)
wdg3.analyse_wdg()
print(wdg3.get_layers())
wdg3.plot_layout(filename=os.path.join(TEST_RES_DIR, "layout_18_1.png"), show=True)
wdg3.plot_MMK(filename=os.path.join(TEST_RES_DIR, "MMK_18_1.png"), show=True)
