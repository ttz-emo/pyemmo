from typing import Union
from pyleecan.Classes.Machine import Machine
import swat_em as swatem


def translate_winding(
    machine: Machine,
) -> tuple[swatem.datamodel, list[
    Union[
        list[Union[list[int], list[int]]],
        list[Union[list[int], list[int]]],
        list[Union[list[int], list[int]]],
    ]]
]:
    """Translates the winding from pyleecan to pyemmo.

        TODO: Vielleicht hier nur das datamodel Objekt zurückgeben und dann
                einfach direkt in createParamDict die Funktion get_phases()
                aufrufen.
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
        w=machine.stator.winding.coil_pitch
        if machine.stator.winding.Nlayer > 1
        else -1,
        layers=machine.stator.winding.Nlayer,
        turns=machine.stator.winding.Ntcoil,
    )
    wind_swat = winding.get_phases()
    wind_test = machine.stator.winding.wind_mat
    wind_test_swat = [[[], []], [[], []], [[], []]]
    is_dbl_layer = bool(len(wind_test) > 1)
    if is_dbl_layer:
        for a in wind_test:
            for slot, conductor in enumerate(a[0]):
                if conductor[0] > 0:
                    wind_test_swat[0][0].append(slot + 1)
                elif conductor[0] < 0:
                    wind_test_swat[0][1].append(-(slot + 1))
                elif conductor[1] > 0:
                    wind_test_swat[1][0].append(slot + 1)
                elif conductor[1] < 0:
                    wind_test_swat[1][1].append(-(slot + 1))
                elif conductor[2] > 0:
                    wind_test_swat[2][0].append(slot + 1)
                elif conductor[2] < 0:
                    wind_test_swat[2][1].append(-(slot + 1))
    else:
        for a in wind_test:
            for slot, conductor in enumerate(a[0]):
                if conductor[0] > 0:
                    wind_test_swat[0][0].append(slot + 1)
                elif conductor[0] < 0:
                    wind_test_swat[0][0].append(-(slot + 1))
                elif conductor[1] > 0:
                    wind_test_swat[1][0].append(slot + 1)
                elif conductor[1] < 0:
                    wind_test_swat[1][0].append(-(slot + 1))
                elif conductor[2] > 0:
                    wind_test_swat[2][0].append(slot + 1)
                elif conductor[2] < 0:
                    wind_test_swat[2][0].append(-(slot + 1))
    return winding, wind_swat
