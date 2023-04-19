from os.path import abspath, join
filepath = abspath(join(__file__,".."))
with open(abspath(join(filepath,"placeholder.txt")) , "r") as testFile:
    fileContent = testFile.read()
print(fileContent)
newFileContent = fileContent.replace("{sample}", "apple")
print(newFileContent)
with open(abspath(join(filepath,"newPlaceholder.txt")), "w") as newTestFile:
    newTestFile.write(newFileContent)