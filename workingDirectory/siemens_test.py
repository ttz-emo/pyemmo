import scipy.io as sio
# from setPath import pathRes
import pyemmo as emmo
import sys

if len(sys.argv) > 2:
    pathRes = sys.argv[2]
    #Skriptobjekt
    myScript = emmo.Script("Modell_Siemens", pathRes)

    #benötigte Informatationen
    pfadMatlabStruct = sys.argv[1]
    meshLaenge = 1e-3

    structAusMatlab = sio.loadmat(pfadMatlabStruct)

    flaechenAnzahl = len(sys.argv)
    if flaechenAnzahl > 3:
        flaecheAll = []
        for i in range(3, flaechenAnzahl):
            flaechenName = sys.argv[i]
            #Werte aus FlächenListe
            flaechenListe = structAusMatlab[flaechenName]
            listenLaenge = len(flaechenListe)
            lineListe = []

            for i in range (1, listenLaenge):
                #Punkte für Linien erstellen
                x1 = flaechenListe[i][1].flat[0]
                y1 = flaechenListe[i][2].flat[0]
                x2 = flaechenListe[i][5].flat[0]
                y2 = flaechenListe[i][6].flat[0]

                point1 = emmo.Point('', x1, y1, 0, meshLaenge)
                point1.setName('point' + str(point1.getID()))
                point2 = emmo.Point('', x2, y2, 0, meshLaenge)
                point2.setName('point' + str(point2.getID()))

                #Kreis braucht noch zusätzlich ein Mittelpunkt
                if flaechenListe[i][13].flat[0] == 'Arc':
                    x3 = flaechenListe[i][9].flat[0]
                    y3 = flaechenListe[i][10].flat[0]
                    point3 = emmo.Point('', x3, y3, 0, meshLaenge)
                    point3.setName('point' + str(point3.getID()))
                    line1 = emmo.CircleArc('', point1, point3, point2)
                
                elif flaechenListe[i][13].flat[0] == 'Line':
                    line1 = emmo.Line('', point1, point2)
                
                line1.setName('Curve' + str(line1.getID()))
                lineListe.append(line1)

            flaeche1 = emmo.Surface(flaechenName, lineListe)
            flaecheAll.append(flaeche1)

        for s in flaecheAll:
            s.addToScript(myScript)

        myScript.generateScript()
        print('.geo-Datei wurde erzeugt!')
    else:
        print('Keine Flaeche als Argument angegeben.')

else:
    print('Achtung: Dieses Skript soll aus MATLAB gestartet werden. Ist die Anwendung aus MATLAB gestartet worden, wurden nicht alle noetigen Informationen uebergeben. Pfade pruefen!')
    print('Als erstes Argument muss der Pfad der .mat Datei uebergeben werden und als zweites der Ergebnispfad. Alle nachfolgenden Argumenten sind die zu erzeugenden Flaechen.')