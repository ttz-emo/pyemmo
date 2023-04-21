from os.path import abspath, dirname, join, normpath
from sys import path


# Add Software_V2 to Path so pyemmo can be found
# This must be done since this is a script (not really a module) and we cannot guarante where it will run from
#   If it will be run as a module (from command line) __file__ will be the actual file path
#   But if its run cellwise, like in an interactive pyhton (IPython) shell, __file__ variable will not exist and we have to add the path manually
try:
    rootname = abspath(join(dirname(__file__), ".."))
except:
    print("Could not determine root. Setting it manually:")
    rootname = "c:\\Users\\ganser\\AppData\\Local\\Programs\\pyemmo_git\\Software_V2"
print(f'rootname is "{rootname}"')
path.append(rootname)

# ROOT_DIR sollte .../SoftwareV2 sein

#Pfad vom Ordner pyemmo ("Software_V2")
pathpyemmo = rootname
#Pfad der Gmsh.exe
pathGmsh = r'C:\Software\onelab-Windows64\gmsh.exe'
#Pfad der GetDP.exe
pathGetDP = r'C:\Software\onelab-Windows64\getdp.exe'
#Wo sollen die .geo- und .pro-Dateien abgespeichert werde
pathRes = join(rootname,'Results')

#       don't remove!!!!!!!!!!!!!
if pathpyemmo not in path:
    path.append(pathpyemmo)
