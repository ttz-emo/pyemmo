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
"""
1. Nach dem Namen der Fläche suchen -> Hier PRODUCT('Surface_Rotorblech'
2. Blockende suchen mit dem Identifier -> PRODUCT_RELATED_PRODUCT_CATEGORY
3. Edge Curve gibt die "ID" der Punkte auf der Linie (VERTEX POINT)
4. Diese VERTEX POINTS finden und Koordinaten extrahieren
#Zeilen mit EDGE_CURVE (Wie sind die Kurven verbunden? -> #..., #... -> Nur ersten 2 Werte nötig!)
#Zeilen mit 'AXIS2_PLACEMENT_3D-> Danach kommt 'CARTESIAN_POINT' -> Mittelpunkt bei einem Kreis
#Zeilen mit 'VERTEX_POINT' -> Alle Punkte des Körpers

def loadFromStep(self, stepFile, unit, meshLength):
        stepData =  open(stepFile)
        textLineFromFile = stepData.readlines()
        trimStepData = self._trimStep(textLineFromFile)
        allObject = self._splitObjects(trimStepData)
        allDict = self.extractNeededInfo(allObject)
        allElement = self.extractPointandLine(allDict)
        self._createGeometry(allElement, unit, meshLength)

    def _trimStep(self, file):

        startId = "PRODUCT('Surface_Rotorblech'"
        endId = "PRODUCT_RELATED_PRODUCT_CATEGORY"
        for i1 in range(len(file)):
            idFind = file[i1].find(startId)
            if idFind == -1:
                pass
            else:
                file = file[i1:len(file)]
                break

        for i2 in range(len(file)):
            idFind2 = file[i2].find(endId)
            if idFind2 == -1:
                pass
            else:
                file = file[0:i2]
                break

        return file

    def _splitObjects(self, file):
        objectLib = []
        startId = "EDGE_CURVE"
        endId = "ORIENTED_EDGE"
        condFindObject = True

        allObject = []

        while condFindObject:
            for i1 in range(len(file)):
                idFind1 = file[i1].find(startId)
                if idFind1 != -1:
                    file = file[i1:len(file)]
                    break

            for i2 in range(len(file)):
                idFind2 = file[i2].find(endId)
                if idFind2 != -1 and i2 != len(file):
                    file2 = file.copy()
                    file2 = file2[0:i2]
                    file = file[i2:len(file)]
                    objectLib.append(file2)
                    break
                elif i2 == len(file)-1:
                    objectLib.append(file)
                    condFindObject = False

        for ob in objectLib:
            obDict = {}
            for i in range(len(ob)):
                if ob[i].find("LINE") != -1:
                    obDict['id'] = 'Line'
                    obDict['rawInfo'] = ob
                    allObject.append(obDict)
                    break
                elif ob[i].find("CIRCLE") != -1:
                    obDict['id'] = 'Circle'
                    obDict['rawInfo'] = ob
                    allObject.append(obDict)
                    break
        return allObject

    def extractNeededInfo(self, allObject):
        #Zeilen mit EDGE_CURVE (Wie sind die Kurven verbunden? -> #..., #... -> Nur ersten 2 Werte nötig!)
        #Zeilen mit 'AXIS2_PLACEMENT_3D-> Danach kommt 'CARTESIAN_POINT' -> Mittelpunkt bei einem Kreis
        #Zeilen mit 'VERTEX_POINT' -> Alle Punkte des Körpers
        newraw = []
        pointsArray = []

        for i in range(len(allObject)):
            objDict = {}
            objDict["description"] = allObject[i]['rawInfo'][0][allObject[i]['rawInfo'][0].find("EDGE_CURVE"):len(allObject[i]['rawInfo'][0])]
            objDict["id"] = allObject[i]["id"]
            if objDict["id"] == "Circle":
                for i2 in range(0, len(allObject[i]['rawInfo'])):
                    if allObject[i]['rawInfo'][i2].find('AXIS2_PLACEMENT_3D') != -1:
                        objDict["centrePoint"] = allObject[i]['rawInfo'][i2+1]
                        break
            newraw.append(objDict)

        for i3 in range(len(allObject)):
            infoRaw = allObject[i3]["rawInfo"].copy()
            for i4 in range(len(infoRaw)):
                if infoRaw[i4].find("VERTEX_POINT") != -1:
                    pointsArray.append(infoRaw[i4+1])

        objectDict = {'Objects':newraw, 'AllPoints':pointsArray}
        return objectDict

    def extractPointandLine(self, objectDict):
        #Point= {x,y,z,id}
        #Line={id,id}
        #Circle={id,id,id}
        allP = []
        allL = []
        for p in (objectDict["AllPoints"]):
            idP = int(p[1:p.find(" =")])
            coordText = p[p.find(",(")+2:p.find(")")]
            x = float(coordText[0:coordText.find(",")])
            coordText = coordText[coordText.find(",")+1:len(coordText)]
            y = float(coordText[0:coordText.find(",")])
            z = float(coordText[coordText.find(",")+1:len(coordText)])
            pointDict = {'id':idP, 'x':x, 'y':y, 'z':z}
            allP.append(pointDict)

        for l in (objectDict["Objects"]):
            if l["id"] == "Circle":
                idP = int(l["centrePoint"][1:l["centrePoint"].find(" =")])
                coordText = l["centrePoint"][l["centrePoint"].find(",(")+2:l["centrePoint"].find(")")]
                x = float(coordText[0:coordText.find(",")])
                coordText = coordText[coordText.find(",")+1:len(coordText)]
                y = float(coordText[0:coordText.find(",")])
                z = float(coordText[coordText.find(",")+1:len(coordText)])
                pointDict = {'id':idP, 'x':x, 'y':y, 'z':z}
                allP.append(pointDict)

        for ob in (objectDict["Objects"]):
            Text = ob["description"]
            Text = Text[Text.find(",")+1:len(Text)]
            idP1 = int(Text[1:Text.find(",")])
            Text = Text[Text.find(",")+1:len(Text)]
            idP2 = int(Text[1:Text.find(",")])
            lineDict = {'p1' : idP1, 'p2' : idP2}
            if ob["id"] == "Circle":
                idPC = int(ob["centrePoint"][1:ob["centrePoint"].find(" =")])
                lineDict['c'] = idPC
            allL.append(lineDict)
        allElement = {'Points' : allP, 'Curves' : allL}
        return allElement

    def _createGeometry(self, allDict, unit, meshLength):
        allP = []
        allL = []
        allCurve = []

        for p in allDict["Points"]:
            pointDict = {}
            pointDict["id"] = p["id"]
            p1 = Point('p', p['x']*unit, p['y']*unit, p['z']*unit, meshLength)
            p1.name = ('p_' + str(p1.id))
            pointDict["Point"] = p1
            allP.append(pointDict)

        for l in allDict["Curves"]:
            lineDict = {}
            for i in range(len(allP)):
                if l['p1']+1 == allP[i]["id"]:
                    lineDict['p1'] = allP[i]["Point"]
                    break
            for i2 in range(len(allP)):
                if l['p2']+1 == allP[i2]["id"]:
                    lineDict['p2'] = allP[i2]["Point"]
                    break
            if len(l.keys()) == 3:
                for i3 in range(len(allP)):
                    if l['c'] == allP[i3]["id"]:
                        lineDict['c'] = allP[i3]["Point"]
                        break
            allL.append(lineDict)

        for curve in allL:
            if len(curve.keys()) == 3:
                line1 = CircleArc('c', curve['p1'], curve['c'], curve['p2'])
                line1.name = ('curve_'+ str(line1.id))
            else:
                line1 = Line('l', curve['p1'], curve['p2'])
                line1.name = ('line_'+ str(line1.id))
            allCurve.append(line1)

        surface_Blech = Surface('Surface_Blech', allCurve)
        self._elements = [surface_Blech]
"""
