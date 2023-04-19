from os.path import join
#Verknüpft Ordnerpfad von Stepdatei mit dem Dateienamen und ergänzt diese mit der Endung .step
def joinStepPath(pathDir, fileNames):
    pathFiles = list()
    for file in fileNames:
        pathFiles.append(join(pathDir, file + '.step'))
    return pathFiles
    