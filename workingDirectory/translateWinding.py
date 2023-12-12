from typing import Union
from pyleecan.Classes.Machine import Machine
import swat_em as swatem


def translateWinding(
    machine: Machine,
) -> list[
    Union[
        list[Union[list[int], list[int]]],
        list[Union[list[int], list[int]]],
        list[Union[list[int], list[int]]],
    ]
]:
    """Translates the winding from pyleecan to pyemmo.

    Args:
        machine (Machine): Pyleecan machine

    Returns:
        list[ Union[ list[Union[list[int], list[int]]], list[Union[list[int], list[int]]], list[Union[list[int], list[int]]], ] ]: ``windSwat``
    """
    winding = swatem.datamodel()

    winding.genwdg(
        Q=machine.stator.slot.Zs,
        P=machine.stator.winding.p * 2,
        m=machine.stator.winding.qs,
        w=machine.stator.winding.coil_pitch,
        layers=machine.stator.winding.Nlayer,
        turns=machine.stator.winding.Ntcoil,
    )
    windSwat = winding.get_phases()
    windTest = machine.stator.winding.wind_mat
    windTestSwat = [[[], []], [[], []], [[], []]]
    isDblLayer = bool(len(windTest) > 1)
    if isDblLayer:
        for a in windTest:
            for slot, conductor in enumerate(a[0]):
                if conductor[0] > 0:
                    windTestSwat[0][0].append(slot + 1)
                elif conductor[0] < 0:
                    windTestSwat[0][1].append(-(slot + 1))
                elif conductor[1] > 0:
                    windTestSwat[1][0].append(slot + 1)
                elif conductor[1] < 0:
                    windTestSwat[1][1].append(-(slot + 1))
                elif conductor[2] > 0:
                    windTestSwat[2][0].append(slot + 1)
                elif conductor[2] < 0:
                    windTestSwat[2][1].append(-(slot + 1))
    else:
        for a in windTest:
            for slot, conductor in enumerate(a[0]):
                if conductor[0] > 0:
                    windTestSwat[0][0].append(slot + 1)
                elif conductor[0] < 0:
                    windTestSwat[0][0].append(-(slot + 1))
                elif conductor[1] > 0:
                    windTestSwat[1][0].append(slot + 1)
                elif conductor[1] < 0:
                    windTestSwat[1][0].append(-(slot + 1))
                elif conductor[2] > 0:
                    windTestSwat[2][0].append(slot + 1)
                elif conductor[2] < 0:
                    windTestSwat[2][0].append(-(slot + 1))
            
    return windSwat
