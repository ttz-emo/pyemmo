"""Module of geometry class Line"""

from random import random
from typing import Tuple, Literal, TYPE_CHECKING

import matplotlib.pyplot as plt
from numpy import array
from numpy.linalg import norm

from ...definitions import DEFAULT_GEO_TOL
from ..geometry import defaultCenterPoint
from .point import Point
from .transformable import Transformable

if TYPE_CHECKING:
    from matplotlib.figure import Figure


class Line(Transformable):
    """
    Eine Instanz der Klasse Line ist eine Gerade zwischen zwei Punkten (Objekte der
    Klasse Point) im dreidimensionalen Raum.

    Beispiel:
        import pyemmo as pyd\n
        P1 = pyd.Point('p1', 0, 0, 0, 0.3)\n
        P2 = pyd.Point('p2', 1, 0, 0, 0.3)\n
        L1 = pyd.Line('l1', P1, P2)\n
    """

    # Die statische Variable ID wird durch die Methode getNewID() hochgezählt. Diese
    # Variable wird für die automatische ID-Vergabe der Geraden bzw. Kurven verwendet!
    ID: int = 0

    def __init__(
        self,
        name: str,
        startPoint: Point,
        endPoint: Point,
        force: bool = False,
    ):
        ###Name der Linie.
        self.name = name
        if not startPoint.isEqual(endPoint):
            ###Startpunkt des Kreisbogens.
            self.startPoint = startPoint
            ###Endpunkt des Kreisbogens.
            self.endPoint = endPoint
        else:
            raise (
                ValueError(
                    f"The coordinates of start and end point of Line '{name}' are equal: "
                    f"{startPoint.getCoordinate()} - {endPoint.getCoordinate()}."
                )
            )
        ###ID der Linie.
        self.id = self._getNewID()
        ###Todesmerker wird nur gesetzt, wenn das Objekt im Skript erzeugt wurde
        # (Aufruf von addToScript())!
        self._todesmerker = False
        self._force: bool = force

    def __eq__(self, other: "Line") -> bool:
        # check type:
        if isinstance(other, self.__class__):
            # check that all points are equal
            if self.arePointsEqual(other):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def _getNewID(cls) -> int:
        """
        Class method: Can not access self!
        Wird eine Linie erzeugt, bekommt sie automatisch eine eindeutige ID zugewiesen.
        Mit _getNewID() wird eine neue ID erzeugt.

        Returns:
            int: New unique line ID
        """
        Line.ID = Line.ID + 1
        return Line.ID

    @property
    def force(self) -> bool:
        """return false flag

        Returns:
            bool: Flag to determine if line generation in Script should be forced
        """
        return self._force

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """get global line ID

        Returns:
            int: ID of line
        """
        return self._id

    @id.setter
    def id(self, newID: int) -> None:
        """setter of line ID

        Args:
            newID (int): New ID of Line
        """
        if newID < self.ID:
            raise ValueError(
                "New ID of line is smaller than global ID count."
                "New ID mus be existing!"
            )
        Line.ID = newID
        self._id = newID

    @property
    def name(self) -> str:
        """Get name of line.

        Returns:
            str: name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name of line .

        Args:
            name (str): New line name
        """
        self._name = name

    @property
    def startPoint(self) -> Point:
        """Start point of line

        Returns:
            Point: Start points
        """
        return self._startPoint

    @startPoint.setter
    def startPoint(self, newStartPoint: Point) -> None:
        """setter of start point

        Args:
            newStartPoint (Point)
        """
        assert isinstance(newStartPoint, Point)
        self._startPoint = newStartPoint

    @property
    def endPoint(self) -> Point:
        """end point of curve

        Returns:
            Point: End point
        """
        return self._endPoint

    @endPoint.setter
    def endPoint(self, newEndPoint: Point) -> None:
        """setter of end point

        Args:
            newEndPoint (Point)
        """
        assert isinstance(newEndPoint, Point)
        self._endPoint = newEndPoint

    @property
    def points(self) -> Tuple["Point", "Point"]:
        """get the start and end point of a line

        Returns:
            Tuple[Point, Point]: start and end point of the line
        """
        startPoint = self.startPoint
        endPoint = self.endPoint
        return (startPoint, endPoint)
    
    @property
    def middlePoint(self) -> Point:
        """Get the center point between start and end point.

        Returns:
            Point: Center point in the middle between start and end point.
        """
        return Point(
            name=f"Middle point of {self.name}",
            x=(self.startPoint.coordinate[0] + self.endPoint.coordinate[0])
            / 2,
            y=(self.startPoint.coordinate[1] + self.endPoint.coordinate[1])
            / 2,
            z=(self.startPoint.coordinate[2] + self.endPoint.coordinate[2])
            / 2,
            meshLength=(self.startPoint.meshLength + self.endPoint.meshLength)
            / 2,
        )

    def switchPoints(self) -> None:
        """switch start and end point of curve (revert direction)

        Returns:
            nothing
        """
        oldP1 = self.startPoint
        oldP2 = self.endPoint
        self.startPoint = oldP2
        self.endPoint = oldP1

    @property
    def type(self) -> Literal["Line"]:
        """Get geometric element type

        Returns:
            Literial: "Line"
        """
        return "Line"

    def translate(self, dx: float, dy: float, dz: float):
        """Translate line

        Args:
            dx, dy, dz (float): offset in meter
        """
        if not self._todesmerker:
            self.startPoint.translate(dx, dy, dz)
            self.endPoint.translate(dx, dy, dz)

    def rotateZ(self, rotationPoint=defaultCenterPoint, angle=0.0):
        """Mit rotateZ() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Z-Achse mit einem definierten Winkel rotiert.

        Args:
            - rotationPoint (Point, optional): Rotation center point.
            Defaults to Point("tmpCenterPoint", 0, 0, 0, 1).
            - angle (float, optional): Rotation angle in rad. Defaults to 0.0.

        Beispiel:
            from math import pi\n
            L1 = Line('l1', P1, P2)\n
            L1.rotateZ(P0, pi)\n
        """
        if not self._todesmerker:
            self.startPoint.rotateZ(rotationPoint, angle)
            self.endPoint.rotateZ(rotationPoint, angle)

    def rotateY(self, rotationPoint: Point, angle: float):
        """
        Mit rotateY() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        Y-Achse mit einem definierten Winkel rotiert.

        Args:
           - rotationPoint (Point): rotation center point
           - angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            L1 = Line('l1', P1, P2)\n
            L1.rotateY(P0, pi)\n

        """
        if not self._todesmerker:
            self.startPoint.rotateY(rotationPoint, angle)
            self.endPoint.rotateY(rotationPoint, angle)

    def rotateX(self, rotationPoint, angle):
        """
        Mit rotateX() wird eine Gerade um einen Rotationspunkt (rotationPoint) und die
        X-Achse mit einem definierten Winkel rotiert.

        Args:
           - rotationPoint (Point): rotation center point
           - angle (float): rotation angle in rad

        Beispiel:
            from math import pi\n
            L1 = Line('l1', P1, P2)\n
            L1.rotateX(P0, pi)\n

        """
        if not self._todesmerker:
            self.startPoint.rotateX(rotationPoint, angle)
            self.endPoint.rotateX(rotationPoint, angle)

    def duplicate(self, name=""):
        """Mit duplicate() wird eine Kurve mit gleichen Eigenschaften zum Originalen
        erzeugt. Diese Kurve hat jedoch eine unterschiedliche ID.\n
        Args:
            name (str, optional): Name of duplicte. Defaults to "".\n
        Returns:
            CircleArc: Duplicate of CircleArc Object\n
        Beispiel:
            CA1 = Point('ca1', P1, C, P2)\n
            CA2 = CA1.duplicate()\n
        """
        newP1 = self.startPoint.duplicate()
        newP2 = self.endPoint.duplicate()
        dupLine = Line(name, newP1, newP2)
        # set new line name
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                dupLine.name = f"{parentName}_dup"
            else:
                dupLine.name = parentName
        return dupLine

    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        """Mit mirror() kann eine Kurve an einer definierten Ebene gespiegelt
        werden. Bildpunkte werden hierbei generiert und eine Kurve zwischen den Punkten
        erzeugt. Die Spiegelebene wird durch einen Aufpunkt (planePoint) und 2 Vektoren
        (planeVector1 und planeVector2) beschrieben.

        Args:
            planePoint (Point): Aufpunkt der Ebene
            planeVector1 (Line): Erster Ebenenvektor.
            planeVector2 (Line): Zweiter Ebenenvektor.
            name (str, optional): Name der neuen Linie. Defaults to "".\n
        Returns:
            CircleArc: Mirrored CircleArc object\n
        Beispiel:
            P0 = Point('P0', 0, 0, 0, 1)\n
            Py = Point('Py', 0, 1, 0, 1)\n
            Pz = Point('Pz', 0, 0, 1, 1)\n
            yAxis = Line(P0, Py)\n
            zAxis = Line(P0, Pz)\n
            P1 = Point('P1', 1, 0, 0, 0.3)\n
            P2 = Point('P1', 2, 0, 0, 0.3)\n
            L1 = Line('L1', P1, P2)\n
            L2 = L1.mirror(P0, yAxis, zAxis)\n

        """
        p1 = self.startPoint.mirror(planePoint, planeVector1, planeVector2)
        p2 = self.endPoint.mirror(planePoint, planeVector1, planeVector2)
        mirLine = Line(self._name, p2, p1)
        if name == "":
            mirLine.name = "L_" + str(abs(mirLine.id))
        else:
            mirLine.name = name
        return mirLine

    ###
    # Mit addToScript wird die Gerade zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Transformationen von Geraden sind nach dem Aufruf nicht mehr erlaubt, da die neuen
    # Koordinaten der Punkte nicht mehr erfasst werden.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode
    # von Script) verwendet werden.
    #
    #   Input:
    #
    #       script : Script
    #
    #   Output:
    #
    #       None
    #
    #   Beispiel:
    #
    #       myScript = Script(...)
    #       L1.addToScript(myScript)
    #
    ###
    def addToScript(self, script: "Script"):
        """old function add to script

        Args:
            script (Script)
        """
        self._todesmerker = True
        script._addCurve(self)

    def getPointDist(self) -> float:
        """calculate the distance between start and end point"""
        StartPoint = array(self.startPoint.coordinate)
        EndPoint = array(self.endPoint.coordinate)
        return norm(StartPoint - EndPoint)

    def plot(
        self,
        fig: "Figure" = None,
        marker=None,
        markersize=1.0,
        linewidth=0.5,
        color=[random() for i in range(3)],
        tag=False,
    ):
        """Line plot

        Args:
            fig (pyplot.Figure, optional): Defaults to None.
            marker (str, optional): Defaults to None.
            markersize (float, optional): Defaults to 1.
            linewidth (float): Defaults to 0.5.
            color (list, optional): Defaults to [random() for i in range(3)].
            tag (bool): Flag to print line id and name like "L `L_ID` ("`L_Name`")"
            and point tags if `marker` is given.
        """
        startPoint = self.startPoint
        endPoint = self.endPoint
        startCoords = startPoint.coordinate
        endCoords = endPoint.coordinate
        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect("equal", adjustable="box")
            fig.set_dpi(300)
        else:
            ax = fig.axes[0]
        ax.plot(
            [startCoords[0], endCoords[0]],
            [startCoords[1], endCoords[1]],
            linewidth=linewidth,
            color=color,
        )
        if tag:
            # add tag to line
            ax.annotate(
                f"""L {self.id} ("{self.name}")""",
                (
                    sum([startCoords[0], endCoords[0]]) / 2,
                    sum([startCoords[1], endCoords[1]]) / 2,
                ),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )
        if marker is not None:
            startPoint.plot(
                fig=fig,
                marker=marker,
                markersize=markersize,
                color=color,
                tag=tag,
            )
            endPoint.plot(
                fig=fig,
                marker=marker,
                markersize=markersize,
                color=color,
                tag=tag,
            )

    def arePointsEqual(self, compLine: "Line", tol=DEFAULT_GEO_TOL) -> bool:
        """
        Checks if start and end point of two lines are identical.
        The result is regardless of the direction.
        """
        originP1 = array(self.startPoint.coordinate)
        originP2 = array(self.endPoint.coordinate)
        compP1 = array(compLine.startPoint.coordinate)
        compP2 = array(compLine.endPoint.coordinate)
        # FIXME: Does not respect the type of line yet!
        if norm(originP1 - compP1) < tol:
            # oP1 and cP1 are identical
            if norm(originP2 - compP2) < tol:
                # if oP1=cP1, oP2 must be cP2 to return True
                return True
            return False
        if norm(originP1 - compP2) < tol:
            # oP1 and cP2 are identical
            if norm(originP2 - compP1) < tol:
                # if oP1=cP2, oP2 must be cP1 to return True
                return True
        return False

    def setMeshLength(self, meshLength: float) -> None:
        """set mesh length of start and endpoint

        Args:
            meshLength (float): Mesh length in meter
        """
        pStart, pEnd = self.points
        pStart.meshLength = meshLength
        pEnd.meshLength = meshLength

    def getMinMeshLength(self) -> float:
        """get the minimum mesh length of start and end point

        Returns:
            float: min mesh length of start and end point
        """
        pStart, pEnd = self.points
        return min(pStart.meshLength, pEnd.meshLength)

    def combine(self, addLine: "Line", touchPoint: Point = None) -> "Line":
        """combine two lines and return them as new line

        Args:
            addLine (Line): line to combine with this line
            touchPoint (Point): Point where the lines touch each other. Defaults to None.
            Trying to identify the point if its not given.
        """
        # pylint: disable=locally-disabled, unidiomatic-typecheck
        if not type(addLine) == type(
            self
        ):  # make sure the line types are equal
            raise (
                TypeError(
                    (
                        "Tried to combine lines, but the line types are different! "
                        f"{type(self)} != {type(addLine)}"
                    )
                )
            )
        if not touchPoint:
            for p in self.points:
                for addP in addLine.points:
                    if p.isEqual(addP):
                        touchPoint: Point = p
                        break
        if touchPoint:
            # get the two points excluding the docking point
            newPoints = [
                point
                for point in self.points + addLine.points
                if not point.isEqual(touchPoint)
            ]
            if len(newPoints) == 2:
                # replace the combined line pattern in the old names if they contained
                lName = self.name.replace("combinedLine_", "")
                addName = addLine.name.replace("combinedLine_", "")
                return Line(
                    f"combinedLine_{lName}_{addName}",
                    startPoint=newPoints[0],
                    endPoint=newPoints[1],
                )
            else:
                raise (
                    RuntimeError(
                        (
                            f"Combination of lines ({self.name} and {addLine.name}) failed."
                            f"{len(newPoints)} points to create a new line; should be 2!"
                        )
                    )
                )
        else:
            raise (
                RuntimeError(
                    (
                        f"Combination of lines ({self.name} and {addLine.name}) failed."
                        "Could not find touchpoint."
                    )
                )
            )

    def containsPoint(
        self, refPoint: Point, tol: float = DEFAULT_GEO_TOL
    ) -> bool:
        """This function checks if start or end point coordinates are equal to the given reference
        point.

        Args:
            refPoint (Point): Reference point to check for.
            tol (float): Geometric tolerance for the comparison of the coordinates.

        Returns:
            bool: True if line contains point, False if not.
        """
        assert isinstance(refPoint, Point)
        assert isinstance(tol, (int, float))
        for p in self.points:
            if p.isEqual(refPoint, tol=tol):
                return True
        return False


