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
        layers=machine.stator.winding.Nlayer,
        turns=machine.stator.winding.Ntcoil,
    )
    windSwat = winding.get_phases()

    return windSwat
