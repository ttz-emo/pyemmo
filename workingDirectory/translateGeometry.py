import sys
import copy
from math import pi, isclose
from numpy import angle

try:
    from pyemmo.script.script import Script
except:
    rootname = "C:\\Users\\k49976\\Desktop\\repositoryGibLab\\pyemmo"
    print(f"Could not determine root. Setting it manually to '{rootname}'")
    print(f'rootname is "{rootname}"')
    sys.path.append(rootname)

import pyleecan.Classes.Machine
import pyleecan.Classes.LamHole
import pyleecan.Classes.LamSlotMag
import pyleecan.Classes.LamSlotWind

from pyemmo.api.SurfaceJSON import SurfaceAPI
from pyemmo.script.geometry.point import Point
from pyemmo.script.geometry.circleArc import CircleArc
from workingDirectory.buildPyemmoMaterial import buildPyemmoMaterial
from workingDirectory.buildPyemmoLineList import buildPyemmoLineList
from workingDirectory.getCoordinatesForPoint import getXforPoint, getYforPoint


# ===========================================
# Definition of function 'translateGeometry':
# ===========================================
def translateGeometry(
    bauteil,  # Stator or Rotor
    detail,  # Lamination, HoleMag, HoleVoid
    machine: pyleecan.Classes.Machine.Machine,  # Import of motor
    label,
    surface,
    isInternalRotor: bool,
    magnetFarthestRadius,
    magnetShortestRadius,
):
    """_summary_

    Args:
        bauteil (_type_): _description_
        detail (_type_): _description_
        motor (pyleecan.Classes.Machine.Machine): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    isMag = False
    centerPoint = Point(name="centerPoint", x=0, y=0, z=0, meshLength=1.0)
    if bauteil == "Rotor":
        if detail == "Lamination":
            pyleecanMat = machine.rotor.mat_type
            IdExt = "Pol"  # "RoNut" "Rotorblech"
            name = "Rotorblech"

        elif isinstance(machine.rotor, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM, SPSMSM

            if detail == "HoleMag":
                pyleecanMat = machine.rotor.hole[0].magnet_0.mat_type
                IdExt = "Mag"  # "Magnet"
                name = "Magnet"

            elif detail == "HoleVoid":
                pyleecanMat = machine.rotor.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"
                name = "Loch"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.rotor, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = machine.rotor.magnet.mat_type
                IdExt = "Mag"
                name = "Magnet"
                anglePointRef = angle(surface.point_ref)
                isMag = True

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.rotor, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail in ("Winding", "Bar"):
                pyleecanMat = machine.rotor.winding.conductor.cond_mat
                IdExt = "RoCu"  # "Rotor-Nut"
                name = "Rotor-Nut"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=label,
            idExt=IdExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=machine.get_pole_pair_number() * 2,
            angle=(2 * pi / (machine.get_pole_pair_number() * 2)),
            meshSize=0,
        )

        # ----------------------------
        # Adding the S1 and S2 Points:
        # ----------------------------
        if isMag:
            pyemmoSurfaceCurveCopy = pyemmoSurface.curve.copy()
            for curve in pyemmoSurfaceCurveCopy:
                # S1
                if isclose(
                    a=curve.startPoint.radius, b=magnetShortestRadius, abs_tol=1e-6
                ) and isclose(
                    a=curve.endPoint.radius, b=magnetShortestRadius, abs_tol=1e-6
                ):
                    S1 = Point(
                        name="S1",
                        x=getXforPoint(magnetShortestRadius, anglePointRef),
                        y=getYforPoint(magnetShortestRadius, anglePointRef),
                        z=0,
                        meshLength=1.0,
                    )
                    magnetCurve1 = CircleArc(
                        name="magnetCurve1",
                        startPoint=curve.startPoint,
                        centerPoint=centerPoint,
                        endPoint=S1,
                    )
                    magnetCurve2 = CircleArc(
                        name="magnetCurve2",
                        startPoint=S1,
                        centerPoint=centerPoint,
                        endPoint=curve.endPoint,
                    )
                    pyemmoSurface.curve.remove(curve)
                    pyemmoSurface.curve.append(magnetCurve1)
                    pyemmoSurface.curve.append(magnetCurve2)

                # S2
                elif isclose(
                    a=curve.startPoint.radius, b=magnetFarthestRadius, abs_tol=1e-6
                ) and isclose(
                    a=curve.endPoint.radius, b=magnetFarthestRadius, abs_tol=1e-6
                ):
                    S2 = Point(
                        name="S2",
                        x=getXforPoint(magnetFarthestRadius, anglePointRef),
                        y=getYforPoint(magnetFarthestRadius, anglePointRef),
                        z=0,
                        meshLength=1.0,
                    )
                    magnetCurve3 = CircleArc(
                        name="magnetCurve3",
                        startPoint=curve.startPoint,
                        centerPoint=centerPoint,
                        endPoint=S2,
                    )
                    magnetCurve4 = CircleArc(
                        name="magnetCurve4",
                        startPoint=S2,
                        centerPoint=centerPoint,
                        endPoint=curve.endPoint,
                    )
                    pyemmoSurface.curve.remove(curve)
                    pyemmoSurface.curve.append(magnetCurve3)
                    pyemmoSurface.curve.append(magnetCurve4)

    # stator
    elif bauteil == "Stator":
        if detail == "Lamination":
            pyleecanMat = machine.stator.mat_type
            IdExt = "StNut"  # "Statorblech"
            name = "Statorblech"

        elif isinstance(machine.stator, pyleecan.Classes.LamHole.LamHole):
            # Entered if machine-type is: IPMSM

            if detail == "HoleMag":
                pyleecanMat = machine.stator.hole[0].magnet_0.mat_type
                IdExt = "Mag"
                name = "Magnet"

            elif detail == "HoleVoid":
                pyleecanMat = machine.stator.hole[0].mat_void
                IdExt = "Lpl"  # "Loch (Pollueke)"
                name = "Loch"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.stator, pyleecan.Classes.LamSlotMag.LamSlotMag):
            # Entered if machine-type is: SPMSM

            if detail == "Magnet":
                pyleecanMat = machine.rotor.magnet.mat_type
                IdExt = "Mag"
                name = "Magnet"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        elif isinstance(machine.stator, pyleecan.Classes.LamSlotWind.LamSlotWind):
            # Entered if machine-type is: IPMSM, SPMSM, SCIM

            if detail == "Winding":
                pyleecanMat = machine.stator.winding.conductor.cond_mat
                IdExt = "StCu0"  # "Stator-Nut"
                name = "Stator-Nut"

            else:
                raise ValueError(
                    f"Wrong input for 'detail'. Your input was '{detail}'."
                )

        else:
            raise ValueError(
                f"Wrong input for 'bauteil'. 'bauteil' must be 'Rotor' or 'Stator'. Your input was '{bauteil}'."
            )

        pyemmoMaterial = buildPyemmoMaterial(pyleecanMat)

        pyemmoSurface = SurfaceAPI(
            name=name,
            idExt=IdExt,
            curves=buildPyemmoLineList(surface.line_list),
            material=pyemmoMaterial,
            nbrSegments=machine.stator.slot.Zs,
            angle=(2 * pi / machine.stator.slot.Zs),
            meshSize=1.0,
        )

    return pyemmoSurface
