import pandas
import pyemmo as emmo

def getDataFrameFromCSV(pathCSV):
    try:
        dataFrame = pandas.read_csv(pathCSV, engine='python')
    except FileNotFoundError:
        dataFrame = None
    return dataFrame

def getMagnetSurfaces(dataFrame, name, mL = 1e-3):
    if type(dataFrame) == int:
        return None
    numLineObj = len(dataFrame['LineID'])
    listLine = [[]]

    startLine = 1
    for i in range(numLineObj):
        #Daten importieren
        x_P1 = dataFrame['ApX'][i]
        y_P1 = dataFrame['ApY'][i]
        z_P1 = dataFrame['ApZ'][i]
        x_P2 = dataFrame['EpX'][i]
        y_P2 = dataFrame['EpY'][i]
        z_P2 = dataFrame['EpZ'][i]

        #pyemmo-Objekte erzeugen
        P1 = emmo.Point('', x_P1, y_P1, z_P1, mL)
        P2 = emmo.Point('', x_P2, y_P2, z_P2, mL)
        P1.setName('p_' + str(P1.getID()))
        P2.setName('p_' + str(P2.getID()))

        if dataFrame['Typ'][i] == 'Arc':
            #Mittelpunkt importieren
            x_M = dataFrame['MpX'][i]
            y_M = dataFrame['MpY'][i]
            z_M = dataFrame['MpZ'][i]

            #Mittelpunkt erzeugen
            PM = emmo.Point('', x_M, y_M, z_M, mL)
            PM.setName('p_' + str(PM.getID()))

            l = emmo.CircleArc('', P1, PM, P2)
            l.setName('Arc_' + str(l.getID()))
        
        elif dataFrame['Typ'][i] == 'Line':
            l = emmo.Line('', P1, P2)
            l.setName('Line_' + str(l.getID()))
        
        else:
            print('linetype not found')
            break
        
        if dataFrame['surfaceID'][i] == startLine:
            listLine[startLine-1].append(l)
        else:
            startLine = dataFrame['surfaceID'][i]
            listLine.append([l])
        
    return {'listLine': listLine, 'name' : name}


def getSurfaceLineList(dataFrame, mL = 1e-3):

    if isinstance(dataFrame, int): # dataFrame should be instance 'pandas.core.frame.DataFrame'
        return None

    numLineObj = len(dataFrame['LineID'])
    LineList = list()

    for i in range(numLineObj): # for each line in dataFrame
        #Daten importieren
        x_P1 = dataFrame['ApX'][i]
        y_P1 = dataFrame['ApY'][i]
        z_P1 = dataFrame['ApZ'][i]
        x_P2 = dataFrame['EpX'][i]
        y_P2 = dataFrame['EpY'][i]
        z_P2 = dataFrame['EpZ'][i]

        #pyemmo-Objekte erzeugen
        P1 = emmo.Point('', x_P1, y_P1, z_P1, mL)
        P2 = emmo.Point('', x_P2, y_P2, z_P2, mL)
        P1.setName('p_' + str(P1.getID()))
        P2.setName('p_' + str(P2.getID()))

        if dataFrame['Typ'][i] == 'Arc':
            #Mittelpunkt importieren
            x_M = dataFrame['MpX'][i]
            y_M = dataFrame['MpY'][i]
            z_M = dataFrame['MpZ'][i]

            #Mittelpunkt erzeugen
            MP = emmo.Point('', x_M, y_M, z_M, mL)
            MP.setName('p_' + str(MP.getID()))

            line = emmo.CircleArc('', P1, MP, P2)
            line.setName('Arc_' + str(line.getID()))
        
        elif dataFrame['Typ'][i] == 'Line':
            line = emmo.Line('', P1, P2)
            line.setName('Line_' + str(line.getID()))
        
        else:
            print('linetype not found')
            break
        
        LineList.append(line)
    
    return LineList

def createSurface(lineList: list, name: str):
    if isinstance(lineList, list):
        surf = emmo.Surface(name, lineList)
    else:
        Warning("Parameter \"lineList\" is not Type List. Surface could not be created!")
        surf = None
    return surf