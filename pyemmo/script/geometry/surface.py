from random import random
from typing import TYPE_CHECKING, List, Tuple, Type, Union

import matplotlib.pyplot as plt
from numpy import mean

from .circleArc import CircleArc
from .line import Line
from .point import Point
from .spline import Spline
from .transformable import Transformable

if TYPE_CHECKING:
    from ..script import Script


###
# Eine Instanz der Klasse Surface ist eine Fläche im dreidimensionalen Raum.
#
#   Input:
#
#       name : string
#       curves : [Line]
#
#   Beispiel:
#
#       from pyemmo import *
#       P1 = Point('P1', 0, 0, 0, 1)
#       P2 = Point('P2', 1, 0, 0, 1)
#       P3 = Point('P3', 1, 1, 0, 1)
#       P4 = Point('P4', 0, 1, 0, 1)
#       L1 = Line('L1', P1, P2)
#       L2 = Line('L2', P2, P3)
#       L3 = Line('L3', P3, P4)
#       L4 = Line('L4', P4, P1)
#       S1 = Surface('S1', [L1, L3, L2, L4])
#
###
class Surface(Transformable):
    ###Statische Variable zur ID-Verwaltung
    ID = 0
    GroupID = 1000

    ###Konstruktor der Klasse Surface
    def __init__(self, name: str, curves: List[Union["Line", "CircleArc", "Spline"]]):
        ###Name des Objektes.
        self.name: str = name
        ###Kurven die eine Fläche umschließen.
        if isinstance(curves, list) and curves:
            self._curves = curves
        else:
            mssg = f"Given curve loop for surface {name} was emtpy not type list ({type(curves)})."
            raise (ValueError(mssg))
        ###ID der Fläche.
        self.id: int = self._getNewID()
        ###Todesmerker wird nur gesetzt, wenn das Objekt im Skript erzeugt wurde (Aufruf von addToScript())!
        self._todesmerker: bool = False
        ###Farbe vom Netz.
        self._color = ""
        self._cut: List["Surface"] = []
        self._isTool: bool = False
        self._delete: bool = False

    def __eq__(self, other: "Surface"):
        # check type and number of points
        if isinstance(other, self.__class__) and (
            len(self.allPoints) == len(other.allPoints)
        ):
            # check that all points are equal
            otherPoints = other.allPoints
            for point in self.allPoints:
                if point not in otherPoints:
                    return False

            return True
        return False

    ###Wird eine Fläche erzeugt, bekommt sie automatisch eine eindeutige ID zugewiesen. Mit getNewID() wird eine neue ID erzeugt.
    @classmethod
    def _getNewID(cls) -> int:
        Surface.ID = Surface.ID + 1
        return Surface.ID

    # pylint: disable=locally-disabled, invalid-name
    @property
    def id(self) -> int:
        """get global surface ID

        Returns:
            int: ID of surface
        """
        return self._id

    @id.setter
    def id(self, newID: int) -> None:
        """setter of surface ID

        Args:
            newID (int): New ID of surface
        """
        if newID < self.ID:
            raise ValueError(
                "New ID of surface is smaller than global ID count."
                "New ID mus be existing!"
            )
        Surface.ID = newID
        self._id = newID

    @property
    def name(self) -> str:
        """Get name of surface.

        Returns:
            str: name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set name of surface.

        Args:
            name (str): New surface name
        """
        self._name = name

    @property
    def curve(self) -> List[Union[Line, CircleArc, Spline]]:
        """Getter of curve

        Returns:
            List[Union[Line, CircleArc, Spline]]: _curves
        """
        return self._curves

    ###Mit translate() kann eine Fläche linear verschoben werden. Die Inputvariablen dx, dy und dz beschreiben die Verschiebungsfaktoren in der x-, y- und z- Richtung.
    #
    #   Input:
    #
    #       dx : float
    #       dy : float
    #       dz : float
    #
    #   Beispiel:
    #
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S1.translate(0, 1, 0)
    #
    ###
    def translate(self, dx, dy, dz):
        if self._todesmerker == True:
            ...  # TODO: Add warning
        else:
            allP = self.allPoints
            for p in allP:
                p.translate(dx, dy, dz)

    ###Mit rotateZ() wird eine Fläche um einen Rotationspunkt (rotationPoint) und die Z-Achse mit einem definierten Winkel rotiert.
    #
    #   Input:
    #
    #       rotaionPoint : Point
    #       angle : float
    #
    #   Beispiel:
    #
    #       from math import pi
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S1.rotateZ(P0, pi)
    #
    ###
    def rotateZ(self, rotationPoint, angle):
        if self._todesmerker == True:
            ...  # TODO: Add warning
        else:
            allP = self.allPoints

            for p in allP:
                p.rotateZ(rotationPoint, angle)

    ###Mit rotateX() wird eine Fläche um einen Rotationspunkt (rotationPoint) und die X-Achse mit einem definierten Winkel rotiert.
    #
    #   Input:
    #
    #       rotaionPoint : Point
    #       angle : float
    #
    #   Beispiel:
    #
    #       from math import pi
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S1.rotateX(P0, pi)
    #
    ###
    def rotateX(self, rotationPoint, angle):
        if self._todesmerker == True:
            ...  # TODO: Add warning
        else:
            allP = self.allPoints

            for p in allP:
                p.rotateX(rotationPoint, angle)

    ###Mit rotateY() wird eine Fläche um einen Rotationspunkt (rotationPoint) und die Y-Achse mit einem definierten Winkel rotiert.
    #
    #   Input:
    #
    #       rotaionPoint : Point
    #       angle : float
    #
    #   Beispiel:
    #
    #       from math import pi
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S1.rotateY(P0, pi)
    #
    ###
    def rotateY(self, rotationPoint, angle):
        if self._todesmerker == True:
            ...  # TODO: Add warning
        else:
            allP = self.allPoints
            for p in allP:
                p.rotateY(rotationPoint, angle)

    ###Mit duplicate() wird eine neue Fläche mit gleichen Eigenschaften zur Originalen erzeugt. Diese Fläche hat jedoch eine unterschiedliche ID.
    #
    #   Optionaler Input:
    #
    #       name : string
    #
    #   Output:
    #
    #       Surface
    #
    #   Beispiel:
    #
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S2 = S1.duplicate()
    #
    #   Akutelle ID von S1 und S2:
    #
    #       >> S1: ID = 1
    #       >> S2: ID = 2
    #
    ###
    def duplicate(self, name=""):
        newCurves: List[Union[Line, CircleArc, Spline]] = list()
        for curve in self.curve:
            newCurves.append(curve.duplicate())
        s = Surface(name, newCurves)
        if name == "":
            parentName = self.name
            if "_dup" not in parentName:
                s.name = f"{parentName}_dup"
            else:
                s.name = parentName
        s._color = self._color
        return s

    ###Mit mirror() kann eine Fläche an einer definierten Ebene gespiegelt werden. Bildpunkte werden hierbei generiert und eine Linie zwischen den Punkten erzeugt. Die Spiegelebene wird durch einen Aufpunkt (planePoint) und 2 Vektoren (planeVector1 und planeVector2) beschrieben.
    #
    #   Input:
    #
    #       planePoint : Point
    #       planeVector1 : Line
    #       planeVector2 : Line
    #
    #   Optionaler Input:
    #
    #       name : string
    #
    #   Output:
    #
    #       Surface
    #
    #   Beispiel:
    #
    #       P0 = Point('P0', 0, 0, 0, 1)
    #       Py = Point('Py', 0, 1, 0, 1)
    #       Pz = Point('Pz', 0, 0, 1, 1)
    #       yAxis = Line(P0, Py)
    #       zAxis = Line(P0, Pz)
    #       S1 = ('S1', [L1, L2, L3, L4])
    #       S2 = S1.mirror(P0, yAxis, zAxis)
    #
    ###
    def mirror(self, planePoint, planeVector1, planeVector2, name=""):
        allCurve = []
        for aC in self._curves:
            allCurve.append(aC)
        allCurve.reverse()
        allNewCurve = []
        for aC in allCurve:
            allNewCurve.append(aC.mirror(planePoint, planeVector1, planeVector2))

        s = Surface(self._name, allNewCurve)

        if name == "":
            s.name = f"s_{self.id}"
        else:
            s.name = name

        s.setMeshColor(self.getMeshColor())

        return s

    @property
    def allPoints(self) -> List[Point]:
        """Get all Points of a Surface (including rotation points of circle arcs)

        Returns:
            List[Point]: _description_
        """
        LineLoop = self.curve
        PointList: List[Point] = list()
        for line in LineLoop:
            if line.type == "CircleArc":
                CenterPoint = line.center
                if CenterPoint not in PointList:
                    PointList.append(CenterPoint)
            elif line.type == "Spline":
                for controlPoint in line.controlPoints:
                    if controlPoint not in PointList:
                        PointList.append(controlPoint)
            startPoint = line.startPoint
            endPoint = line.endPoint
            if startPoint not in PointList:
                PointList.append(startPoint)
            if endPoint not in PointList:
                PointList.append(endPoint)
        return PointList

    def combine(self, addSurf: "Surface") -> "Surface":
        """combine two surfaces.

        Args:
            addSurf (Surface): Surface to combine with this Surface

        Returns:
            Surface: Combined Surface with name "combinedLine_{surface name}_{addSurface name}"

        Raises:
            UserWarning: If there were matching intersection points, but the touching line types were different.
            RuntimeError: If no touching line was found.
        """
        if addSurf == self:
            return self
        touchpoints = None  # default setting of touching points (start and endpoint of interface line)
        curves = self.curve.copy()  # copy curve lists
        addCurves = addSurf.curve.copy()
        # compare each curve in the curve loop to check if there is a matching line = interface line
        for curve in curves:
            for addCurve in addCurves:
                if curve.arePointsEqual(addCurve):
                    # found matching curve! Make sure the line types are equal:
                    if curve.type == addCurve.type:
                        touchpoints = curve.points
                        break
                    else:
                        mssg = "Tried to combine surfaces, but the contact curves have different line types!"
                        raise (UserWarning(mssg))
            if touchpoints:
                # if touchpoints were found; remove docking lines from line lists:
                curves.remove(curve)
                addCurves.remove(addCurve)
                newCurves = curves + addCurves  # combine the remaining lines
                # check if the remaining lines containing the touch points can be combined:
                for dockPoint in touchpoints:
                    lines2combine: List[Union[Line, CircleArc, Spline]] = list()
                    # find the two lines in the two remaining curve lists containing the docking point:
                    for curve in newCurves:
                        for linePoint in curve.getPoints():
                            if linePoint.isEqual(dockPoint):
                                # if the line point and docking point coordinates are equal add the line to the combine lines-list:
                                lines2combine.append(curve)
                                break  # break the loop
                    if len(lines2combine) == 2:
                        # only combine lines of equal type
                        combine = False
                        if type(lines2combine[0]) == type(lines2combine[1]):
                            combine = True  # combine lines
                            # if they are arcs, make sure the centerpoint is equal:
                            if isinstance(lines2combine[0], CircleArc):
                                c1 = lines2combine[0].center
                                c2 = lines2combine[1].center
                                if not c1.isEqual(c2):
                                    # special case where circle arcs are touching but have different center point.
                                    combine = False
                                    # otherwise combine will stay True
                        if combine:
                            # remove curves after loop, because otherwise the next curve item in the loop will be skiped (static indexing):
                            newCurves.remove(lines2combine[0])
                            newCurves.remove(lines2combine[1])
                            combinedLine = lines2combine[0].combine(
                                lines2combine[1], dockPoint
                            )  # combine the two lines
                            newCurves.append(combinedLine)
                break  # break the outer curve for-loop, if the touchpoints where found
        if touchpoints:
            sName = self.name.replace("combinedLine_", "")
            addName = addSurf.name.replace("combinedLine_", "")
            newSurf = self.duplicate()  # TODO: avoid name repitition
            newSurf.name = f"combinedLine_{sName}_{addName}"
            newSurf.curve(curves=newCurves)
            return newSurf
        else:
            mssg = f"Cound not combine surfaces ({self.name} and {addSurf.name}). No intersection curve was found!"
            raise (RuntimeError(mssg))

    def recombineCurves(self) -> None:
        oldLoop = self.curve
        newLoop: List[Union[Line, CircleArc, Spline]] = list()
        while oldLoop:
            curve = oldLoop.pop()
            newCurve = None
            for otherCurve in oldLoop:
                try:
                    newCurve = curve.combine(otherCurve)
                    break
                except RuntimeError:
                    continue
                except ValueError:
                    continue
                except TypeError:
                    continue
                except Exception as e:
                    raise (e)
            if newCurve:
                oldLoop.remove(otherCurve)
                newLoop.append(newCurve)
            else:
                newLoop.append(curve)
        self.curve(newLoop)
        return None

    ###
    # Mit addToScript wird die Fläche zum Skriptobjekt übergeben und in gmsh-Syntax übersetzt.
    # Transformationen von Flächen sind nach dem Aufruf nicht mehr erlaubt, da die neuen Koordinaten der Punkte nicht mehr erfasst werden.
    # Diese Methode sollte stets nur in Kombination mit generateScript (Klassenmethode von Script) verwendet werden.
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
    #       S1.addToScript(myScript)
    #
    ###
    def addToScript(self, script: "Script"):
        # if addToScript was not allready done
        if not self._todesmerker:
            self._todesmerker = True
            script._addSurface(self)
        else:
            ...

    def isDrawn(self) -> bool:
        """
        Get the "todesmerker" status. todesmerker is set when the surface was drawn.
        The function returns true if the surface is allready in the script
        """
        return self._todesmerker

    def sortCurves(self) -> None:
        """sortiert die Kurven einer geschlossenen Fläche neu, um eine Curve Loop in Gmsh zu erstellen

        Returns:
            List[Union[Line, CircleArc, Spline]]: New sorted line loop
        """
        oldLoop: List[Line] = self.curve
        # direction: List[int] = list()
        # direction = 1  # append 1 for first line, cause it sets the direction
        newLoop: List[Line] = list()
        # add first line to newLoop, because it doesnt need to be checked
        newLoop.append(oldLoop.pop(0))
        nbrLines = len(oldLoop)  # get the remaining number of lines
        # for every line thats left:
        for i1 in range(nbrLines):
            # Check which line in oldLoop appends to the last line in newLoop
            # if that line was found get direction, append it to newLoop and remove it from oldLoop
            for i2 in range(0, len(oldLoop)):
                # if direction == 1:
                if oldLoop[i2].startPoint.isEqual(newLoop[-1].endPoint):
                    # direction = True # direction is equal
                    newLoop.append(oldLoop.pop(i2))
                    break
                elif oldLoop[i2].endPoint.isEqual(newLoop[-1].endPoint):
                    # direction = False # direction is inverted
                    oldLoop[i2].switchPoints()
                    newLoop.append(oldLoop.pop(i2))
                    break
        # old loop list must be empty in the end!
        if oldLoop:  # is not empty
            mssg = f"Lineloop of surface '{self.name}' was not closed!"
            raise (RuntimeError(mssg))
            # else:
            #     if oldLoop[i2].startPoint.isEqual(newLoop[-1].startPoint):
            #         direction = True # direction is equal
            #         newLoop.append(oldLoop.pop(i2))
            #         break
            #     elif oldLoop[i2].endPoint.isEqual(newLoop[-1].startPoint):
            #         direction = False # direction is inverted
            #         oldLoop[i2].switchPoints()
            #         newLoop.append(oldLoop.pop(i2))
            #         break
        self.curve = newLoop
        return None

    def replaceCurve(self, oldCurve: Line, newCurve: Line) -> None:
        """Die Methode replaceCurve() tauscht eine Kurve in der Liste gegen eine neue Kurve aus.

        Args:
            oldCurve (Line): Curve to be replaced.
            newCurve (Line): Curve that should be inserted instead.
        """
        for i, curve in enumerate(self.curve):
            if curve == oldCurve:
                self._curves[i] = newCurve

    # @property
    # def meshColor(self) -> str:
    #     """get the mesh color

    #     Returns:
    #         str: name of the color
    #     """
    #     return self._color

    # @meshColor.setter
    # def setMeshColor(self, color: str) -> str:
    #     """Setter for Mesh Color

    #     Args:
    #         color (str): _description_

    #     Returns:
    #         str: _description_
    #     """
    #     self._color = color

    def setMeshColor(self, color: str) -> None:
        """set the mesh color

        Args:
            color (str): _description_
        """
        self._color = color

    def getMeshColor(self) -> str:
        """get the mesh color

        Returns:
            str: name of the color
        """
        return self._color

    @property
    def type(self) -> str:
        """Mit getType() wird ein Identifier der Klasse als String zurück gegeben.

        Returns:
            str: "Surface"
        """
        return "Surface"


    @curve.setter
    def curve(self, curves:list[Line]) -> None:
        """Set line loop of surface

        Args:
            curves (list[Line]): Line loop with surface boundary lines.
        """
        # print("set new curves")
        self._curves = curves

    @property
    def delete(self) -> bool:
        """Get the delete-status of the surface"""
        return self._delete

    @delete.setter
    def delete(self, status: bool) -> None:
        """Delete Surface at the end of script generation"""
        if isinstance(status, bool):
            self._delete = True
        else:
            raise TypeError("Delete status was not type bool!")

    def cutOut(self, ToolSurface: "Surface", keepTool: bool = True) -> None:
        """Cut out a Tool Surface from the Parent surface by Boolean Difference"""
        self._cut.append(ToolSurface)
        ToolSurface.tool  # set the tool surface _isTool=True
        if not keepTool:
            ToolSurface.delete()

    @property
    def tools(self) -> List[Type["Surface"]]:
        """Get the list of tool surfaces to cut out of this surface

        Returns:
            list: _cut
        """
        return self._cut

    @tools.setter
    def tool(self) -> None:
        """set the surface as subtraction surface"""
        self._isTool = True

    def isTool(self) -> bool:
        """returns True if the surface has been subtracted from a other surface.

        Returns:
            bool: True if the surface has been subtracted, False if not.
        """
        return self._isTool

    def calcCOG(self) -> Point:
        """
        DEMO-VERSION!!! Calculate the geometric "Center of Gravity" (COG)
        Actually the algorithm just retruns the mean value of all point coordinates (Not the real center!) FIXME

        Args:

        Returns:
            CenterPoint: Point

        Raises:
            Nothing
        """
        points = self.points
        x = []
        y = []
        z = []
        for p in points:
            coords = p.coordinate
            x.append(coords[0])
            y.append(coords[1])
            z.append(coords[2])
        return Point(
            name=("CP_" + self.name), x=mean(x), y=mean(y), z=mean(z), meshLength=1
        )

    def plot(
        self,
        fig=None,
        linewidth=0.5,
        color=[random() for i in range(3)],
        marker=".",
        markersize=1,
        tag=False,
    ) -> None:
        """
        2D Line plot of the surface
        """
        if fig is None:
            fig, ax = plt.subplots()
            fig.set_dpi(200)
            xlim, ylim = self.getBoundingBox(scalingFactor=1.1)
            fig.axes[0].set(xlim=xlim, ylim=ylim)
            ax.set_aspect("equal", adjustable="box")
        for curve in self.curve:
            curve.plot(
                fig,
                linewidth=linewidth,
                color=color,
                marker=marker,
                markersize=markersize,
                tag=tag,
            )
        if tag:
            cog = self.calcCOG().coordinate
            ax.annotate(
                f"""S {self.id} ("{self.name}")""",
                (cog[0], cog[1]),
                textcoords="offset points",
                xytext=(1, 1),
                ha="left",
            )

    def getBoundingBox(
        self, scalingFactor: float = 1.0
    ) -> Tuple[List[float], List[float]]:
        """Get the minimum and maximum x and y values of the points

        Args:
            scalingFactor (float, optional): _description_. Defaults to 1.0.

        Returns:
            Tuple[List[float], List[float]]: _description_
        """
        minx, maxx, miny, maxy = 0.0, 0.0, 0.0, 0.0
        for point in self.points:
            x, y, z = point.coordinate
            if x < minx:
                minx = x
            elif x > maxx:
                maxx = x
            if y < miny:
                miny = y
            elif y > maxy:
                maxy = y
        return [minx * scalingFactor, maxx * scalingFactor], [
            miny * scalingFactor,
            maxy * scalingFactor,
        ]

    @property
    def points(self) -> List[Point]:
        """Get all Points on the contour of a Surface

        Returns:
            List[Point]: _description_
        """
        LineLoop = self.curve
        if LineLoop:
            PointList: List[Point] = list()
            for line in LineLoop:
                startPoint = line.startPoint
                endPoint = line.endPoint
                if startPoint not in PointList:
                    PointList.append(startPoint)
                if endPoint not in PointList:
                    PointList.append(endPoint)
            return PointList
        else:
            return []

    def setMeshLength(self, meshLength: float) -> None:
        """set the meshLength of all points of a surface.

        Args:
            meshLength (float): mesh length to be set for all points
        """
        pointList = self.allPoints
        for point in pointList:
            point._meshLength = meshLength

    @property
    def minMeshLength(self) -> float:
        """get the minimum meshLength of all points of the surface.

        Returns:
            float: min mesh length of all points
        """
        pointList = self.allPoints
        ml = pointList.pop().meshLength
        for point in pointList:
            nml = point.meshLength
            if nml < ml:
                ml = nml
        return ml

    @property
    def meanMeshLength(self) -> float:
        """get the mean mesh length of all points of the surface.

        Returns:
            float: mean of mesh length of all points in meter
        """
        pointList = self.allPoints
        mlList = [p.meshLength for p in pointList]
        return mean(mlList)
