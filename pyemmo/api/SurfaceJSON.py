"""Module for json api surface class"""
from typing import List, Union

from numpy import pi
from ..script.geometry.line import Line
from ..script.geometry.circleArc import CircleArc
from ..script.geometry.spline import Spline
from ..script.geometry.surface import Surface
from ..script.material.material import Material


class SurfaceAPI(Surface):
    """
    SurfaceAPI is a child of geometry class Surface and has additional attributes:


        .. SurfaceAPI_Params_Table:

        .. table:: SurfaceAPI Parameters.

           +-----------------+-----------------------------+-----------------+
           | parameter       | description                 | format          |
           | name            |                             |                 |
           +=================+=============================+=================+
           | idExt           | | External ID which is an   | string          |
           |                 |   abbriviation of surface   |                 |
           |                 |   name.                     |                 |
           |                 | | E.g. rotor lamination     |                 |
           |                 |   → RoLam                   |                 |
           +-----------------+-----------------------------+-----------------+
           | material        | Surface material of type    | Material        |
           |                 | Material.                   |                 |
           +-----------------+-----------------------------+-----------------+
           | nbrSegments     | | Number of surface         | int             |
           |                 |   segements on a whole      |                 |
           |                 |   circle                    |                 |
           |                 | | (2D machine model).       |                 |
           +-----------------+-----------------------------+-----------------+
           | angle           | Angle of the segment (rad). | float           |
           |                 | Should be 2*Pi/nbrSegments  |                 |
           +-----------------+-----------------------------+-----------------+
           | meshSize        | | Mesh size of the surface  | float           |
           |                 |   (m). If no surface mesh   |                 |
           |                 | | should be created its None|                 |
           +-----------------+-----------------------------+-----------------+


    """

    def __init__(
        self,
        name: str,
        idExt: str,
        curves: List[Line],
        material: Material,
        nbrSegments: int,
        angle: float,
        meshSize: float,
    ):
        """init of surface for API. This type of surface is special,
        because it allways forms a machine segment or a part of a segment.

        Args:
            name (str): name of the surface
            idExt (str): abbriviation of surface name (short name)
            curves (List[Line]): list of surface boundary lines
            material (Material): surface material in simulation.
            nbrSegments (int): number of segments in the full machine.
            angle (float): angle of the segment. Should be 2*Pi/nbrSegments.
            meshSize (float): mesh size of the surface.
        """
        super().__init__(name=name, curves=curves)
        self._idExt: str = idExt
        self._material: Material = material
        self._nbrSegments: int = nbrSegments
        assert angle == 2 * pi / nbrSegments, (
            f"Segment angle ({angle}) of surface {name} "
            f"does not match 2*pi/nbrSegments ({2 * pi / nbrSegments})"
        )
        self._angle: float = angle
        self._meshSize: float = meshSize

    def getIdExt(self) -> str:
        """get the abbriviation of the surface name (literal Surface ID)

        Returns:
            str: abbriviation of surface name (short name)
        """
        return self._idExt

    def setIdExt(self, name: str) -> None:
        """set the abbriviation of the surface name (literal Surface ID)

        Args:
            name (str): abbriviation of surface name (short name)

        Returns:
            None
        """
        if isinstance(name, str):
            self._idExt = name
        else:
            raise ValueError(f"The given name was not type str: {name}!")

    def getMaterial(self) -> Material:
        """get the material of the API surface

        Returns:
            Material: surface material
        """
        return self._material

    def getAngle(self) -> float:
        """get the angle of one surface segment. Should be 2*Pi/self._nbrSegments

        Returns:
            float: segment angle of that surface in rad.
        """
        return self._angle

    def getNbrSegments(self) -> int:
        """get the nbrSegments of segments of a API surface to form a whole circle (2*Pi)

        Returns:
            int: maximal number of segments to form a whole circle.
        """
        return self._nbrSegments

    def getMeshSize(self) -> float:
        """get the mesh size of the points of the surface

        Returns:
            float: Mesh size of the surface points.
        """
        return self._meshSize

    def setMeshSize(self, meshSize: float) -> None:
        """set the mesh size of the points.

        Args:
            meshSize (float): Mesh size of the surface points.
        """
        if not isinstance(meshSize, (float, int)):
            msg = (
                f"Given mesh size for API surface '{self.name}'"
                f"was not a number but type '{type(meshSize)}'!"
            )
            raise TypeError(msg)
        self._meshSize = meshSize

    def duplicate(self, name="") -> "SurfaceAPI":
        """create a copy of the surface

        Args:
            name (str, optional): New name for copied surface. 
                Defaults to previous surface name + "_dup" for duplicate.

        Returns:
            SurfaceAPI: Duplicate of SurfaceAPI object.
        """
        # duplicate curves for new surface
        newCurves: List[Union[Line, CircleArc, Spline]] = []
        for curve in self.getCurve():
            newCurves.append(curve.duplicate())
        # create duplicate surfcace object
        duplicatSurf = SurfaceAPI(
            name=name,
            idExt=self.getIdExt(),
            curves=newCurves,
            material=self.getMaterial(),
            nbrSegments=self.getNbrSegments(),
            angle=self.getAngle(),
            meshSize=self.getMeshSize(),
        )
        # add "_dup" str to new surface name, if it was not duplicted before
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                duplicatSurf.name = f"{parentName}_dup"
            else:
                duplicatSurf.name = f"{parentName}_{duplicatSurf.id}"
        duplicatSurf.setMeshColor(self.getMeshColor())
        return duplicatSurf

    # def rotateDuplicate(self, symFactor: int) -> List["SurfaceAPI"]:
    #     """
    #     Create a duplicate of the API surface and rotate to the symmetry given by symFactor

    #     Args:
    #         symFactor (int): ...

    #     Returns:
    #         List[SurfaceAPI]: ...

    #     Raises:
    #         Nothing
    #     """
    #     nbrTurns = self.getnbrSegments() / symFactor
    #     if not nbrTurns.is_integer():
    #         raise (
    #             ValueError(
    #                 f"Trying to perform a uneven number of rotate-duplicate operations:{nbrTurns}"
    #             )
    #         )

    #     if Angle != 0:  # if the rotation angle is not zero
    #         DuplicatedGeoObj = GeoObj.duplicate()  # duplicate obj
    #         CenterPoint = Point(
    #             "TmpCenterPoint", 0, 0, 0, 1
    #         )  # Center point for rotation
    #         DuplicatedGeoObj.rotateZ(CenterPoint, Angle)  # rotate obj
    #         # if type(GeoObj) == Surface:
    #         #     replaceIdenticalLines(GeoObj, DuplicatedGeoObj)
    #         return DuplicatedGeoObj
    #     else:  # if the angle is zero: give back duplicate of the old surface
    #         return GeoObj.duplicate()


# ==================================================================================================
# ========================================= END API SURFACE ========================================
# ==================================================================================================
